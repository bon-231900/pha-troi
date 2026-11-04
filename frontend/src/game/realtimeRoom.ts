// ============================================================================
// DỰ ÁN WEBGAME "PHÁ TRỜI" - THE CELESTIAL FORGE (phatroi.com)
// REAL-TIME MULTIPLAYER P2P & BROADCAST NETWORK ROOM
// Kết nối trực tiếp giữa các trình duyệt và thiết bị (0ms tab-to-tab, <30ms P2P)
// ============================================================================

import { joinRoom } from '@trystero-p2p/nostr';
import { safeStorage } from './storage';
import { StanceKey } from './rules';

export interface PeerPresence {
  [key: string]: any;
  id: string;
  name: string;
  guildId: string;
  stance: StanceKey;
  slotIndex: number; // 0..17 (slots on panoramic terraces)
  lastSeen: number;
}

export interface RemoteStrikeMessage {
  [key: string]: any;
  peerId: string;
  name: string;
  slotIndex: number;
  stance: StanceKey;
  damage: number;
  isGolden: boolean;
  isCrit?: boolean;
  timestamp: number;
}

export interface RemoteChatMessage {
  [key: string]: any;
  id: string;
  peerId: string;
  author: string;
  guildId?: string;
  text: string;
  timestamp: number;
}

export interface WorldStateSyncMessage {
  [key: string]: any;
  senderId: string;
  senderName: string;
  vaultId: number;
  bossHp: number;
  bossTrailHp: number;
  serverFurnaceHeat: number;
  serverAnvilHp: number;
  activeArmorBreakPoints: number;
  isShieldBroken: boolean;
  shieldBreakTimeLeft: number;
  timestamp: number;
  isLeader?: boolean;
}

export interface RealtimeRoomCallbacks {
  onPeerJoined?: (peer: PeerPresence) => void;
  onPeerLeft?: (peerId: string) => void;
  onRemoteStrike?: (strike: RemoteStrikeMessage) => void;
  onRemoteChat?: (chat: RemoteChatMessage) => void;
  onPeersChange?: (peers: PeerPresence[]) => void;
  onWorldStateSync?: (state: WorldStateSyncMessage) => void;
  onRequestWorldState?: () => WorldStateSyncMessage | null;
}

const BROADCAST_CHANNEL_NAME = 'phatroi_celestial_room_v1';
const TRYSTERO_APP_ID = 'pha-troi-phatroi-com';

export class RealtimeRoomClient {
  private localPlayerId: string;
  private localPlayerName: string;
  private localGuildId: string = 'guild_thien_thai';
  private localStance: StanceKey = 'Q';
  private assignedSlotIndex: number = 1; // Default first peer slot

  private peers: Map<string, PeerPresence> = new Map();
  private broadcastChannel: BroadcastChannel | null = null;
  private p2pRoom: ReturnType<typeof joinRoom> | null = null;
  private sendP2PStrike: ((data: RemoteStrikeMessage) => void) | null = null;
  private sendP2PPresence: ((data: PeerPresence) => void) | null = null;
  private sendP2PChat: ((data: RemoteChatMessage) => void) | null = null;
  private sendP2PWorldSync: ((data: WorldStateSyncMessage) => void) | null = null;
  private sendP2PWorldReq: ((data: { peerId: string }) => void) | null = null;

  private heartbeatTimer: ReturnType<typeof setInterval> | null = null;
  private pruneTimer: ReturnType<typeof setInterval> | null = null;
  private callbacks: RealtimeRoomCallbacks;

  constructor(callbacks: RealtimeRoomCallbacks = {}) {
    this.callbacks = callbacks;

    // Generate a unique per-tab player ID so multiple tabs in the same browser can co-exist
    const tabNonce = Math.floor(Math.random() * 89999 + 10000);
    this.localPlayerId = `forger_${Date.now().toString(36)}_${tabNonce}`;

    // Player display name from storage or generated
    const savedName = safeStorage.getItem('phatroi_user_name');
    if (savedName && typeof savedName === 'string') {
      this.localPlayerName = savedName;
    } else {
      this.localPlayerName = `Thợ Rèn #${tabNonce.toString().slice(-4)}`;
      safeStorage.setItem('phatroi_user_name', this.localPlayerName);
    }
  }

  public init(guildId: string, stance: StanceKey, vaultId: number = 1) {
    this.localGuildId = guildId;
    this.localStance = stance;

    // Layer 1: Setup Local BroadcastChannel for 0ms cross-tab & cross-window sync
    if (typeof window !== 'undefined' && 'BroadcastChannel' in window) {
      try {
        this.broadcastChannel = new BroadcastChannel(BROADCAST_CHANNEL_NAME);
        this.broadcastChannel.onmessage = (event) => {
          this.handleIncomingMessage(event.data);
        };
      } catch (err) {
        console.warn('[RealtimeRoom] BroadcastChannel init error:', err);
      }
    }

    // Layer 2: Setup Serverless WebRTC P2P Room via Nostr Relays for cross-browser / cross-device
    try {
      const roomId = `vault_${vaultId}`;
      this.p2pRoom = joinRoom(
        {
          appId: TRYSTERO_APP_ID,
          relayConfig: {
            urls: [
              'wss://nos.lol',
              'wss://nostr.mom',
              'wss://relay.primal.net',
              'wss://purplerelay.com',
            ],
          },
        },
        roomId
      );

      const strikeAction = this.p2pRoom.makeAction<RemoteStrikeMessage>('strike');
      strikeAction.onMessage = (data) => {
        if (data && data.peerId !== this.localPlayerId) {
          this.handleIncomingStrike(data);
        }
      };

      const presenceAction = this.p2pRoom.makeAction<PeerPresence>('presence');
      presenceAction.onMessage = (data) => {
        if (data && data.id !== this.localPlayerId) {
          this.handleIncomingPresence(data);
        }
      };

      const chatAction = this.p2pRoom.makeAction<RemoteChatMessage>('chat');
      chatAction.onMessage = (data) => {
        if (data && data.peerId !== this.localPlayerId) {
          this.handleIncomingChat(data);
        }
      };

      const worldSyncAction = this.p2pRoom.makeAction<WorldStateSyncMessage>('world_sync');
      worldSyncAction.onMessage = (data) => {
        if (data && data.senderId !== this.localPlayerId) {
          this.handleIncomingWorldSync(data);
        }
      };

      const worldReqAction = this.p2pRoom.makeAction<{ peerId: string }>('world_req');
      worldReqAction.onMessage = (data) => {
        if (data && data.peerId !== this.localPlayerId) {
          this.handleIncomingWorldReq();
        }
      };

      this.sendP2PStrike = (data: RemoteStrikeMessage) => {
        strikeAction.send(data).catch(() => {});
      };
      this.sendP2PPresence = (data: PeerPresence) => {
        presenceAction.send(data).catch(() => {});
      };
      this.sendP2PChat = (data: RemoteChatMessage) => {
        chatAction.send(data).catch(() => {});
      };
      this.sendP2PWorldSync = (data: WorldStateSyncMessage) => {
        worldSyncAction.send(data).catch(() => {});
      };
      this.sendP2PWorldReq = (data: { peerId: string }) => {
        worldReqAction.send(data).catch(() => {});
      };

      this.p2pRoom.onPeerJoin = (peerId) => {
        console.log('[RealtimeRoom] P2P Peer connected:', peerId);
        // Send our presence immediately to newly joined peer
        this.broadcastPresence();
        // If we are leader or established peer, send our world state to the newcomer
        const state = this.callbacks.onRequestWorldState?.();
        if (state) {
          this.broadcastWorldState(state);
        }
      };

      this.p2pRoom.onPeerLeave = (peerId) => {
        console.log('[RealtimeRoom] P2P Peer left:', peerId);
        this.handlePeerLeave(peerId);
      };
    } catch (err) {
      console.warn('[RealtimeRoom] P2P Room init error:', err);
    }

    // Periodically broadcast local presence & heartbeat
    this.broadcastPresence();
    this.heartbeatTimer = setInterval(() => {
      this.broadcastPresence();
    }, 3000);

    // Prune stale peers (inactive for > 10 seconds)
    this.pruneTimer = setInterval(() => {
      const now = Date.now();
      let changed = false;
      for (const [id, peer] of this.peers.entries()) {
        if (now - peer.lastSeen > 10000) {
          this.peers.delete(id);
          this.callbacks.onPeerLeft?.(id);
          changed = true;
        }
      }
      if (changed) {
        this.callbacks.onPeersChange?.(Array.from(this.peers.values()));
      }
    }, 4000);
  }

  public updateIdentity(stance?: StanceKey, guildId?: string, name?: string) {
    if (stance) this.localStance = stance;
    if (guildId) this.localGuildId = guildId;
    if (name) {
      this.localPlayerName = name;
      safeStorage.setItem('phatroi_user_name', name);
    }
    this.broadcastPresence();
  }

  private getNextAvailableSlot(): number {
    // Available terrace slots in order of proximity to center Main Hero:
    // 1 (Right front), 0 (Left front), 3 (Right mid), 2 (Left mid), 5, 4, 7, 6...
    const preferredOrder = [1, 0, 3, 2, 5, 4, 7, 6, 9, 8, 11, 10, 13, 12, 15, 14, 17, 16];
    const occupied = new Set<number>();
    for (const peer of this.peers.values()) {
      occupied.add(peer.slotIndex);
    }
    for (const slot of preferredOrder) {
      if (!occupied.has(slot)) return slot;
    }
    return 1;
  }

  private broadcastPresence() {
    // Choose an available slot if our current one collides
    const occupied = new Set<number>();
    for (const [id, peer] of this.peers.entries()) {
      if (id !== this.localPlayerId) occupied.add(peer.slotIndex);
    }
    if (occupied.has(this.assignedSlotIndex)) {
      this.assignedSlotIndex = this.getNextAvailableSlot();
    }

    const presence: PeerPresence = {
      id: this.localPlayerId,
      name: this.localPlayerName,
      guildId: this.localGuildId,
      stance: this.localStance,
      slotIndex: this.assignedSlotIndex,
      lastSeen: Date.now(),
    };

    // BroadcastChannel (local tabs)
    try {
      this.broadcastChannel?.postMessage({
        type: 'presence',
        payload: presence,
      });
    } catch {}

    // P2P WebRTC (remote peers)
    try {
      this.sendP2PPresence?.(presence);
    } catch {}
  }

  public broadcastStrike(damage: number, isGolden: boolean, isCrit: boolean = false) {
    const packet: RemoteStrikeMessage = {
      peerId: this.localPlayerId,
      name: this.localPlayerName,
      slotIndex: this.assignedSlotIndex,
      stance: this.localStance,
      damage,
      isGolden,
      isCrit,
      timestamp: Date.now(),
    };

    // 1. BroadcastChannel (0ms to other tabs on same machine)
    try {
      this.broadcastChannel?.postMessage({
        type: 'strike',
        payload: packet,
      });
    } catch {}

    // 2. WebRTC P2P DataChannel
    try {
      this.sendP2PStrike?.(packet);
    } catch {}
  }

  public broadcastChat(text: string) {
    const packet: RemoteChatMessage = {
      id: `chat_${Date.now()}_${Math.random().toString(36).substring(2, 6)}`,
      peerId: this.localPlayerId,
      author: this.localPlayerName,
      guildId: this.localGuildId,
      text,
      timestamp: Date.now(),
    };

    try {
      this.broadcastChannel?.postMessage({
        type: 'chat',
        payload: packet,
      });
    } catch {}

    try {
      this.sendP2PChat?.(packet);
    } catch {}
  }

  private handleIncomingMessage(msg: any) {
    if (!msg || typeof msg !== 'object') return;
    const { type, payload } = msg;

    if (type === 'presence' && payload && payload.id !== this.localPlayerId) {
      this.handleIncomingPresence(payload);
    } else if (type === 'strike' && payload && payload.peerId !== this.localPlayerId) {
      this.handleIncomingStrike(payload);
    } else if (type === 'chat' && payload && payload.peerId !== this.localPlayerId) {
      this.handleIncomingChat(payload);
    } else if (type === 'world_sync' && payload && payload.senderId !== this.localPlayerId) {
      this.handleIncomingWorldSync(payload);
    } else if (type === 'world_req' && payload && payload.peerId !== this.localPlayerId) {
      this.handleIncomingWorldReq();
    }
  }

  private handleIncomingPresence(peer: PeerPresence) {
    const isNew = !this.peers.has(peer.id);
    this.peers.set(peer.id, {
      ...peer,
      lastSeen: Date.now(),
    });

    if (isNew) {
      this.callbacks.onPeerJoined?.(peer);
      // Immediately reply with our presence so the new peer knows about us right away
      this.broadcastPresence();
      // Send current world state to new peer
      const state = this.callbacks.onRequestWorldState?.();
      if (state) {
        this.broadcastWorldState(state);
      }
    }
    this.callbacks.onPeersChange?.(Array.from(this.peers.values()));
  }

  private handleIncomingStrike(strike: RemoteStrikeMessage) {
    // Refresh peer lastSeen
    const existing = this.peers.get(strike.peerId);
    if (existing) {
      existing.lastSeen = Date.now();
      existing.stance = strike.stance;
    } else {
      // Auto register unknown peer
      this.peers.set(strike.peerId, {
        id: strike.peerId,
        name: strike.name,
        guildId: 'guild_thien_thai',
        stance: strike.stance,
        slotIndex: strike.slotIndex,
        lastSeen: Date.now(),
      });
      this.callbacks.onPeersChange?.(Array.from(this.peers.values()));
    }

    this.callbacks.onRemoteStrike?.(strike);
  }

  private handleIncomingChat(chat: RemoteChatMessage) {
    this.callbacks.onRemoteChat?.(chat);
  }

  private handleIncomingWorldSync(state: WorldStateSyncMessage) {
    this.callbacks.onWorldStateSync?.(state);
  }

  private handleIncomingWorldReq() {
    const currentState = this.callbacks.onRequestWorldState?.();
    if (currentState) {
      this.broadcastWorldState(currentState);
    }
  }

  public broadcastWorldState(state: Partial<WorldStateSyncMessage>) {
    const packet: WorldStateSyncMessage = {
      senderId: this.localPlayerId,
      senderName: this.localPlayerName,
      vaultId: state.vaultId ?? 1,
      bossHp: state.bossHp ?? 1_500_000_000,
      bossTrailHp: state.bossTrailHp ?? state.bossHp ?? 1_500_000_000,
      serverFurnaceHeat: state.serverFurnaceHeat ?? 1500,
      serverAnvilHp: state.serverAnvilHp ?? 10000,
      activeArmorBreakPoints: state.activeArmorBreakPoints ?? 0,
      isShieldBroken: state.isShieldBroken ?? false,
      shieldBreakTimeLeft: state.shieldBreakTimeLeft ?? 0,
      timestamp: Date.now(),
      isLeader: this.isLeader(),
    };

    // 1. Local BroadcastChannel (0ms to other tabs on same machine)
    try {
      this.broadcastChannel?.postMessage({
        type: 'world_sync',
        payload: packet,
      });
    } catch {}

    // 2. WebRTC P2P DataChannel (cross-browser and cross-device)
    try {
      this.sendP2PWorldSync?.(packet);
    } catch {}
  }

  public requestWorldState() {
    const packet = { peerId: this.localPlayerId };

    try {
      this.broadcastChannel?.postMessage({
        type: 'world_req',
        payload: packet,
      });
    } catch {}

    try {
      this.sendP2PWorldReq?.(packet);
    } catch {}
  }

  public isLeader(): boolean {
    const allIds = [this.localPlayerId, ...Array.from(this.peers.keys())].sort();
    return allIds[0] === this.localPlayerId;
  }

  private handlePeerLeave(peerId: string) {
    if (this.peers.has(peerId)) {
      this.peers.delete(peerId);
      this.callbacks.onPeerLeft?.(peerId);
      this.callbacks.onPeersChange?.(Array.from(this.peers.values()));
    }
  }

  public getPeers(): PeerPresence[] {
    return Array.from(this.peers.values());
  }

  public getLocalPlayer() {
    return {
      id: this.localPlayerId,
      name: this.localPlayerName,
      guildId: this.localGuildId,
      stance: this.localStance,
      slotIndex: this.assignedSlotIndex,
    };
  }

  public destroy() {
    if (this.heartbeatTimer) clearInterval(this.heartbeatTimer);
    if (this.pruneTimer) clearInterval(this.pruneTimer);
    if (this.broadcastChannel) {
      try {
        this.broadcastChannel.close();
      } catch {}
      this.broadcastChannel = null;
    }
    if (this.p2pRoom) {
      try {
        this.p2pRoom.leave();
      } catch {}
      this.p2pRoom = null;
    }
  }
}
