// ============================================================================
// DỰ ÁN WEBGAME "PHÁ TRỜI" - THE CELESTIAL FORGE (phatroi.com)
// REAL-TIME MULTIPLAYER P2P & BROADCAST NETWORK ROOM
// Kết nối trực tiếp giữa các trình duyệt và thiết bị (0ms tab-to-tab, <30ms P2P)
// ============================================================================

import { joinRoom } from '@trystero-p2p/nostr';
import { safeStorage } from './storage';
import { getCelestialVault, StanceKey } from './rules';

export interface PeerPresence {
  [key: string]: any;
  id: string;
  name: string;
  guildId: string;
  stance: StanceKey;
  slotIndex: number; // 0..23 (slots on panoramic terraces)
  skinId?: string;
  sessionEpoch?: number;
  presenceSeq?: number;
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
  sessionEpoch?: number;
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

export interface LeaveMessage {
  [key: string]: any;
  peerId: string;
  vaultId: number;
  sessionEpoch?: number;
  timestamp: number;
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

export interface BroadcastChannelLike {
  onmessage: ((event: { data: any }) => void) | null;
  postMessage: (message: any) => void;
  close: () => void;
}

export interface RealtimeRoomDeps {
  playerId?: string;
  now?: () => number;
  createBroadcastChannel?: (name: string) => BroadcastChannelLike | null;
  joinRoomFn?: typeof joinRoom;
  sessionStorage?: Pick<Storage, 'getItem' | 'setItem'> | null;
}

const BROADCAST_CHANNEL_PREFIX = 'phatroi_celestial_room_v1';
const TRYSTERO_APP_ID = 'pha-troi-phatroi-com';
const TAB_PLAYER_ID_STORAGE_KEY = 'phatroi_tab_player_id';
const LEFT_GUARD_TTL_MS = 10_000;
const PEER_STALE_TTL_MS = 10_000;

const PREFERRED_SLOT_ORDER = [
  3, 4, 2, 5, 1, 6, 0, 7,
  12, 15, 11, 16, 13, 14, 10, 17, 9, 18, 8, 19,
  21, 22, 20, 23,
];

let fallbackPagePlayerId: string | null = null;
let epochSequence = 0;

function generateTabPlayerId(): string {
  const tabNonce = Math.floor(Math.random() * 89999 + 10000);
  return `forger_${Date.now().toString(36)}_${tabNonce}`;
}

function getBroadcastChannelName(vaultId: number): string {
  return `${BROADCAST_CHANNEL_PREFIX}_vault_${vaultId}`;
}

function resolveTabPlayerId(sessionStore?: Pick<Storage, 'getItem' | 'setItem'> | null): string {
  const store =
    sessionStore !== undefined
      ? sessionStore
      : typeof window !== 'undefined' && typeof window.sessionStorage !== 'undefined'
        ? window.sessionStorage
        : null;

  if (store) {
    try {
      const existing = store.getItem(TAB_PLAYER_ID_STORAGE_KEY);
      if (existing && typeof existing === 'string' && existing.trim().length > 0) {
        return existing;
      }
      const created = generateTabPlayerId();
      store.setItem(TAB_PLAYER_ID_STORAGE_KEY, created);
      return created;
    } catch {
      // Fallback cleanly when sessionStorage is blocked (private browsing / sandboxed iframe)
    }
  }

  if (!fallbackPagePlayerId) {
    fallbackPagePlayerId = generateTabPlayerId();
  }
  return fallbackPagePlayerId;
}

export class RealtimeRoomClient {
  private localPlayerId: string;
  private localPlayerName: string;
  private localGuildId: string = 'guild_thien_thai';
  private localStance: StanceKey = 'Q';
  private localSkinId: string = 'skin_default';
  private currentVaultId: number = 1;
  private sessionEpoch: number = 0;
  private presenceSeq: number = 0;
  private assignedSlotIndex: number = 1; // Default first peer slot

  private peers: Map<string, PeerPresence> = new Map();
  private transportPeerToPlayerId: Map<string, string> = new Map();
  private recentlyLeftPeers: Map<string, { leftAt: number; sessionEpoch?: number }> = new Map();

  private broadcastChannel: BroadcastChannelLike | null = null;
  private p2pRoom: ReturnType<typeof joinRoom> | null = null;
  private sendP2PStrike: ((data: RemoteStrikeMessage) => void) | null = null;
  private sendP2PPresence: ((data: PeerPresence) => void) | null = null;
  private sendP2PChat: ((data: RemoteChatMessage) => void) | null = null;
  private sendP2PWorldSync: ((data: WorldStateSyncMessage) => void) | null = null;
  private sendP2PWorldReq: ((data: { peerId: string }) => void) | null = null;
  private sendP2PLeave: ((data: LeaveMessage) => void) | null = null;

  private heartbeatTimer: ReturnType<typeof setInterval> | null = null;
  private pruneTimer: ReturnType<typeof setInterval> | null = null;
  private unloadHandler: (() => void) | null = null;

  private callbacks: RealtimeRoomCallbacks;
  private nowFn: () => number;
  private createBroadcastChannelFn: (name: string) => BroadcastChannelLike | null;
  private joinRoomFn: typeof joinRoom;

  constructor(callbacks: RealtimeRoomCallbacks = {}, deps: RealtimeRoomDeps = {}) {
    this.callbacks = callbacks;
    this.nowFn = deps.now ?? (() => Date.now());
    this.joinRoomFn = deps.joinRoomFn ?? joinRoom;
    this.createBroadcastChannelFn =
      deps.createBroadcastChannel ??
      ((name: string) => {
        if (typeof window !== 'undefined' && 'BroadcastChannel' in window) {
          return new BroadcastChannel(name) as unknown as BroadcastChannelLike;
        }
        return null;
      });

    // Keep one stable per-tab player ID across React room recreations and page reloads
    this.localPlayerId = deps.playerId || resolveTabPlayerId(deps.sessionStorage);

    // Player display name from storage or generated
    const savedName = safeStorage.getItem('phatroi_user_name');
    if (savedName && typeof savedName === 'string') {
      this.localPlayerName = savedName;
    } else {
      const suffix = this.localPlayerId.slice(-4);
      this.localPlayerName = `Thợ Rèn #${suffix}`;
      safeStorage.setItem('phatroi_user_name', this.localPlayerName);
    }
  }

  public init(guildId: string, stance: StanceKey, vaultId: number = 1) {
    // Ensure repeated init() calls never leak old rooms, channels, timers, or stale peers
    if (this.broadcastChannel || this.p2pRoom || this.heartbeatTimer || this.pruneTimer) {
      this.destroy();
    }

    this.localGuildId = guildId;
    this.localStance = stance;
    this.currentVaultId = vaultId;
    epochSequence += 1;
    this.sessionEpoch = this.nowFn() * 1000 + (epochSequence % 1000);

    // Layer 1: Setup Local BroadcastChannel scoped per vault for 0ms cross-tab sync
    try {
      this.broadcastChannel = this.createBroadcastChannelFn(getBroadcastChannelName(vaultId));
      if (this.broadcastChannel) {
        this.broadcastChannel.onmessage = (event) => {
          this.handleIncomingMessage(event.data);
        };
      }
    } catch (err) {
      console.warn('[RealtimeRoom] BroadcastChannel init error:', err);
    }

    // Layer 2: Setup Serverless WebRTC P2P Room via Nostr Relays for cross-browser / cross-device
    try {
      const roomId = `vault_${vaultId}`;
      this.p2pRoom = this.joinRoomFn(
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
      strikeAction.onMessage = (data, context) => {
        if (data && data.peerId !== this.localPlayerId) {
          this.bindTransportPeer(context?.peerId, data.peerId);
          this.handleIncomingStrike(data);
        }
      };

      const presenceAction = this.p2pRoom.makeAction<PeerPresence>('presence');
      presenceAction.onMessage = (data, context) => {
        if (data && data.id !== this.localPlayerId) {
          this.bindTransportPeer(context?.peerId, data.id);
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

      const leaveAction = this.p2pRoom.makeAction<LeaveMessage>('leave');
      leaveAction.onMessage = (data, context) => {
        if (data && data.peerId && data.peerId !== this.localPlayerId) {
          if (typeof data.vaultId === 'number' && data.vaultId !== this.currentVaultId) return;
          if (context?.peerId && this.transportPeerToPlayerId.get(context.peerId) === data.peerId) {
            this.transportPeerToPlayerId.delete(context.peerId);
          }
          this.handlePeerLeave(data.peerId, data.sessionEpoch);
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
      this.sendP2PLeave = (data: LeaveMessage) => {
        leaveAction.send(data).catch(() => {});
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

      this.p2pRoom.onPeerLeave = (transportPeerId) => {
        console.log('[RealtimeRoom] P2P Peer left:', transportPeerId);
        const mappedPlayerId = this.transportPeerToPlayerId.get(transportPeerId);
        this.transportPeerToPlayerId.delete(transportPeerId);
        this.handlePeerLeave(mappedPlayerId || transportPeerId);
      };
    } catch (err) {
      console.warn('[RealtimeRoom] P2P Room init error:', err);
    }

    if (typeof window !== 'undefined' && typeof window.addEventListener === 'function') {
      this.unloadHandler = () => {
        this.broadcastLeave();
      };
      window.addEventListener('pagehide', this.unloadHandler);
      window.addEventListener('beforeunload', this.unloadHandler);
    }

    // Periodically broadcast local presence & heartbeat
    this.broadcastPresence();
    this.heartbeatTimer = setInterval(() => {
      this.broadcastPresence();
    }, 3000);

    // Prune stale peers (inactive for > 10 seconds) & expire zombie leave guards
    this.pruneTimer = setInterval(() => {
      const now = this.nowFn();
      let changed = false;
      for (const [id, peer] of this.peers.entries()) {
        if (now - peer.lastSeen > PEER_STALE_TTL_MS) {
          this.removePeerMappings(id);
          this.peers.delete(id);
          this.callbacks.onPeerLeft?.(id);
          changed = true;
        }
      }
      for (const [id, guard] of this.recentlyLeftPeers.entries()) {
        if (now - guard.leftAt > LEFT_GUARD_TTL_MS) {
          this.recentlyLeftPeers.delete(id);
        }
      }
      if (changed) {
        this.emitPeersChange();
      }
    }, 4000);
  }

  public updateIdentity(stance?: StanceKey, guildId?: string, name?: string, skinId?: string) {
    if (stance) this.localStance = stance;
    if (guildId) this.localGuildId = guildId;
    if (skinId) this.localSkinId = skinId;
    if (name) {
      this.localPlayerName = name;
      safeStorage.setItem('phatroi_user_name', name);
    }
    this.broadcastPresence();
  }

  private bindTransportPeer(transportPeerId: string | undefined, playerId: string) {
    if (!transportPeerId || !playerId || playerId === this.localPlayerId) return;
    const previousPlayerId = this.transportPeerToPlayerId.get(transportPeerId);
    if (previousPlayerId && previousPlayerId !== playerId) {
      // Same WebRTC peer switched player ID (e.g. fast reconnect without leave): evict ghost immediately
      if (this.peers.has(previousPlayerId)) {
        this.peers.delete(previousPlayerId);
        this.callbacks.onPeerLeft?.(previousPlayerId);
        this.emitPeersChange();
      }
    }
    this.transportPeerToPlayerId.set(transportPeerId, playerId);
  }

  private removePeerMappings(playerId: string) {
    for (const [transportId, mappedPlayerId] of this.transportPeerToPlayerId.entries()) {
      if (mappedPlayerId === playerId) {
        this.transportPeerToPlayerId.delete(transportId);
      }
    }
  }

  private isStaleLeftPacket(playerId: string, packetEpoch?: number): boolean {
    const guard = this.recentlyLeftPeers.get(playerId);
    if (!guard) return false;
    if (this.nowFn() - guard.leftAt > LEFT_GUARD_TTL_MS) {
      this.recentlyLeftPeers.delete(playerId);
      return false;
    }
    if (typeof packetEpoch === 'number' && typeof guard.sessionEpoch === 'number') {
      // A newer page session with the same tab ID after F5 has a higher epoch and must be admitted
      if (packetEpoch > guard.sessionEpoch) {
        this.recentlyLeftPeers.delete(playerId);
        return false;
      }
      return true;
    }
    return packetEpoch === undefined;
  }

  private emitPeersChange() {
    this.callbacks.onPeersChange?.(Array.from(this.peers.values()));
  }

  private getNextAvailableSlot(): number {
    const occupied = new Set<number>();
    for (const peer of this.peers.values()) {
      occupied.add(peer.slotIndex);
    }
    for (const slot of PREFERRED_SLOT_ORDER) {
      if (!occupied.has(slot)) return slot;
    }
    return 3;
  }

  private shouldYieldCurrentSlot(): boolean {
    for (const [id, peer] of this.peers.entries()) {
      if (id !== this.localPlayerId && peer.slotIndex === this.assignedSlotIndex) {
        // Deterministic tie-breaker: only the lexicographically larger ID relocates
        if (id < this.localPlayerId) {
          return true;
        }
      }
    }
    return false;
  }

  private broadcastPresence() {
    if (this.shouldYieldCurrentSlot()) {
      this.assignedSlotIndex = this.getNextAvailableSlot();
    }

    const mySeq = ++this.presenceSeq;
    const presence: PeerPresence = {
      id: this.localPlayerId,
      name: this.localPlayerName,
      guildId: this.localGuildId,
      stance: this.localStance,
      slotIndex: this.assignedSlotIndex,
      skinId: this.localSkinId,
      sessionEpoch: this.sessionEpoch,
      presenceSeq: mySeq,
      lastSeen: this.nowFn(),
    };

    // BroadcastChannel (local tabs)
    try {
      this.broadcastChannel?.postMessage({
        type: 'presence',
        vaultId: this.currentVaultId,
        payload: presence,
      });
    } catch {}

    // If re-entrant tie-breaker already emitted a newer presence, skip sending stale P2P payload
    if (this.presenceSeq !== mySeq) return;

    // P2P WebRTC (remote peers)
    try {
      this.sendP2PPresence?.(presence);
    } catch {}
  }

  private broadcastLeave() {
    const leaveMsg: LeaveMessage = {
      peerId: this.localPlayerId,
      vaultId: this.currentVaultId,
      sessionEpoch: this.sessionEpoch,
      timestamp: this.nowFn(),
    };

    try {
      this.broadcastChannel?.postMessage({
        type: 'leave',
        vaultId: this.currentVaultId,
        payload: leaveMsg,
      });
    } catch {}

    try {
      this.sendP2PLeave?.(leaveMsg);
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
      sessionEpoch: this.sessionEpoch,
      timestamp: this.nowFn(),
    };

    // 1. BroadcastChannel (0ms to other tabs on same machine)
    try {
      this.broadcastChannel?.postMessage({
        type: 'strike',
        vaultId: this.currentVaultId,
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
      id: `chat_${this.nowFn()}_${Math.random().toString(36).substring(2, 6)}`,
      peerId: this.localPlayerId,
      author: this.localPlayerName,
      guildId: this.localGuildId,
      text,
      timestamp: this.nowFn(),
    };

    try {
      this.broadcastChannel?.postMessage({
        type: 'chat',
        vaultId: this.currentVaultId,
        payload: packet,
      });
    } catch {}

    try {
      this.sendP2PChat?.(packet);
    } catch {}
  }

  private handleIncomingMessage(msg: any) {
    if (!msg || typeof msg !== 'object') return;
    if (typeof msg.vaultId === 'number' && msg.vaultId !== this.currentVaultId) return;

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
    } else if (type === 'leave' && payload && payload.peerId && payload.peerId !== this.localPlayerId) {
      this.handlePeerLeave(payload.peerId, payload.sessionEpoch);
    }
  }

  private handleIncomingPresence(peer: PeerPresence) {
    if (!peer || !peer.id || peer.id === this.localPlayerId) return;
    if (this.isStaleLeftPacket(peer.id, peer.sessionEpoch)) return;

    const existing = this.peers.get(peer.id);
    if (
      existing &&
      typeof peer.sessionEpoch === 'number' &&
      peer.sessionEpoch === existing.sessionEpoch &&
      typeof peer.presenceSeq === 'number' &&
      typeof existing.presenceSeq === 'number' &&
      peer.presenceSeq < existing.presenceSeq
    ) {
      return;
    }

    const isNew = !existing;
    const isFreshSession = !existing || existing.sessionEpoch !== peer.sessionEpoch;
    this.peers.set(peer.id, {
      ...peer,
      lastSeen: this.nowFn(),
    });

    if (isNew || isFreshSession || this.shouldYieldCurrentSlot()) {
      if (isNew) {
        this.callbacks.onPeerJoined?.(peer);
      }
      // Reply with our presence (and relocate cleanly if a smaller ID claimed our slot)
      this.broadcastPresence();
      if (isFreshSession) {
        const state = this.callbacks.onRequestWorldState?.();
        if (state) {
          this.broadcastWorldState(state);
        }
      }
    }
    this.emitPeersChange();
  }

  private handleIncomingStrike(strike: RemoteStrikeMessage) {
    if (!strike || !strike.peerId || strike.peerId === this.localPlayerId) return;
    if (this.isStaleLeftPacket(strike.peerId, strike.sessionEpoch)) return;

    const existing = this.peers.get(strike.peerId);
    if (existing) {
      existing.lastSeen = this.nowFn();
      existing.stance = strike.stance;
      if (typeof strike.slotIndex === 'number' && strike.slotIndex !== existing.slotIndex) {
        existing.slotIndex = strike.slotIndex;
        this.emitPeersChange();
      }
    } else {
      // Auto register unknown active peer (blocked for recently-left peers to avoid zombie resurrection)
      this.peers.set(strike.peerId, {
        id: strike.peerId,
        name: strike.name,
        guildId: 'guild_thien_thai',
        stance: strike.stance,
        slotIndex: strike.slotIndex,
        sessionEpoch: strike.sessionEpoch,
        lastSeen: this.nowFn(),
      });
      this.emitPeersChange();
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
    const fallbackHp = getCelestialVault(state.vaultId ?? 1).maxHp;
    const packet: WorldStateSyncMessage = {
      senderId: this.localPlayerId,
      senderName: this.localPlayerName,
      vaultId: state.vaultId ?? 1,
      bossHp: state.bossHp ?? fallbackHp,
      bossTrailHp: state.bossTrailHp ?? state.bossHp ?? fallbackHp,
      serverFurnaceHeat: state.serverFurnaceHeat ?? 1500,
      serverAnvilHp: state.serverAnvilHp ?? 10000,
      activeArmorBreakPoints: state.activeArmorBreakPoints ?? 0,
      isShieldBroken: state.isShieldBroken ?? false,
      shieldBreakTimeLeft: state.shieldBreakTimeLeft ?? 0,
      timestamp: this.nowFn(),
      isLeader: this.isLeader(),
    };

    // 1. Local BroadcastChannel (0ms to other tabs on same machine)
    try {
      this.broadcastChannel?.postMessage({
        type: 'world_sync',
        vaultId: this.currentVaultId,
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
        vaultId: this.currentVaultId,
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

  private handlePeerLeave(peerId: string, sessionEpoch?: number) {
    const existing = this.peers.get(peerId);
    const guardEpoch =
      typeof sessionEpoch === 'number' ? sessionEpoch : existing?.sessionEpoch;
    this.recentlyLeftPeers.set(peerId, {
      leftAt: this.nowFn(),
      sessionEpoch: guardEpoch,
    });
    this.removePeerMappings(peerId);

    if (this.peers.has(peerId)) {
      this.peers.delete(peerId);
      this.callbacks.onPeerLeft?.(peerId);
      this.emitPeersChange();
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
    this.broadcastLeave();

    if (this.heartbeatTimer) {
      clearInterval(this.heartbeatTimer);
      this.heartbeatTimer = null;
    }
    if (this.pruneTimer) {
      clearInterval(this.pruneTimer);
      this.pruneTimer = null;
    }
    if (this.unloadHandler && typeof window !== 'undefined' && typeof window.removeEventListener === 'function') {
      window.removeEventListener('pagehide', this.unloadHandler);
      window.removeEventListener('beforeunload', this.unloadHandler);
      this.unloadHandler = null;
    }
    if (this.broadcastChannel) {
      try {
        this.broadcastChannel.close();
      } catch {}
      this.broadcastChannel = null;
    }
    if (this.p2pRoom) {
      try {
        void Promise.resolve(this.p2pRoom.leave()).catch(() => {});
      } catch {}
      this.p2pRoom = null;
    }

    this.sendP2PStrike = null;
    this.sendP2PPresence = null;
    this.sendP2PChat = null;
    this.sendP2PWorldSync = null;
    this.sendP2PWorldReq = null;
    this.sendP2PLeave = null;

    this.peers.clear();
    this.transportPeerToPlayerId.clear();
    this.recentlyLeftPeers.clear();
  }
}
