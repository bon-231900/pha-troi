import test from 'node:test';
import assert from 'node:assert/strict';
import {
  RealtimeRoomClient,
  type BroadcastChannelLike,
  type PeerPresence,
} from './realtimeRoom';

class FakeSessionStorage implements Pick<Storage, 'getItem' | 'setItem'> {
  private store = new Map<string, string>();
  getItem(key: string): string | null {
    return this.store.get(key) ?? null;
  }
  setItem(key: string, value: string): void {
    this.store.set(key, value);
  }
}

function createBroadcastBus() {
  const channels = new Map<string, Set<BroadcastChannelLike>>();

  return {
    create(name: string): BroadcastChannelLike {
      if (!channels.has(name)) channels.set(name, new Set());
      const group = channels.get(name)!;
      const channel: BroadcastChannelLike = {
        onmessage: null,
        postMessage(message: any) {
          for (const target of group) {
            if (target !== channel) {
              target.onmessage?.({ data: message });
            }
          }
        },
        close() {
          group.delete(channel);
        },
      };
      group.add(channel);
      return channel;
    },
  };
}

function createFakeP2PNetwork() {
  type RoomHandlers = {
    actions: Map<string, ((data: any, context: { peerId: string }) => void) | null>;
    onPeerJoin: ((peerId: string) => void) | null;
    onPeerLeave: ((peerId: string) => void) | null;
    transportPeerId: string;
    roomId: string;
  };

  const roomsByVault = new Map<string, Map<string, RoomHandlers>>();
  let seq = 0;

  const joinRoomFn = (_config: any, roomId: string) => {
    seq += 1;
    const transportPeerId = `trystero_peer_${seq}`;
    if (!roomsByVault.has(roomId)) roomsByVault.set(roomId, new Map());
    const peersInRoom = roomsByVault.get(roomId)!;

    const handlers: RoomHandlers = {
      actions: new Map(),
      onPeerJoin: null,
      onPeerLeave: null,
      transportPeerId,
      roomId,
    };
    peersInRoom.set(transportPeerId, handlers);

    const api: any = {
      makeAction(namespace: string) {
        const action: any = {
          onMessage: null as ((data: any, context: { peerId: string }) => void) | null,
          send(data: any) {
            for (const [otherTransportId, other] of peersInRoom.entries()) {
              if (otherTransportId === transportPeerId) continue;
              const cb = other.actions.get(namespace);
              cb?.(data, { peerId: transportPeerId });
            }
            return Promise.resolve();
          },
        };
        Object.defineProperty(action, 'onMessage', {
          get: () => handlers.actions.get(namespace) ?? null,
          set: (fn) => {
            handlers.actions.set(namespace, fn);
          },
        });
        return action;
      },
      leave() {
        peersInRoom.delete(transportPeerId);
        for (const other of peersInRoom.values()) {
          other.onPeerLeave?.(transportPeerId);
        }
        return Promise.resolve();
      },
      set onPeerJoin(fn: ((peerId: string) => void) | null) {
        handlers.onPeerJoin = fn;
      },
      get onPeerJoin() {
        return handlers.onPeerJoin;
      },
      set onPeerLeave(fn: ((peerId: string) => void) | null) {
        handlers.onPeerLeave = fn;
      },
      get onPeerLeave() {
        return handlers.onPeerLeave;
      },
    };

    return api;
  };

  return {
    joinRoomFn: joinRoomFn as any,
    disconnectTransport(roomId: string, transportPeerId: string) {
      const peersInRoom = roomsByVault.get(roomId);
      if (!peersInRoom) return;
      peersInRoom.delete(transportPeerId);
      for (const other of peersInRoom.values()) {
        other.onPeerLeave?.(transportPeerId);
      }
    },
  };
}

test('same tab sessionStorage reuses identical localPlayerId across refresh/recreation so 1 player only occupies 1 slot', (t) => {
  const bus = createBroadcastBus();
  const net = createFakeP2PNetwork();
  const tabAStorage = new FakeSessionStorage();
  const tabBStorage = new FakeSessionStorage();
  let now = 1_000_000;

  let peersSeenByA: PeerPresence[] = [];
  const roomA = new RealtimeRoomClient(
    {
      onPeersChange: (peers) => {
        peersSeenByA = peers;
      },
    },
    {
      now: () => now,
      sessionStorage: tabAStorage,
      createBroadcastChannel: (name) => bus.create(name),
      joinRoomFn: net.joinRoomFn,
    }
  );
  const roomB1 = new RealtimeRoomClient(
    {},
    {
      now: () => ++now,
      sessionStorage: tabBStorage,
      createBroadcastChannel: (name) => bus.create(name),
      joinRoomFn: net.joinRoomFn,
    }
  );
  const roomB2 = new RealtimeRoomClient(
    {},
    {
      now: () => ++now,
      sessionStorage: tabBStorage,
      createBroadcastChannel: (name) => bus.create(name),
      joinRoomFn: net.joinRoomFn,
    }
  );
  t.after(() => {
    roomB2.destroy();
    roomB1.destroy();
    roomA.destroy();
  });

  roomA.init('guild_thien_thai', 'Q', 1);
  roomB1.init('guild_thien_thai', 'Q', 1);
  assert.equal(peersSeenByA.length, 1);
  const firstSlot = peersSeenByA[0].slotIndex;

  // Player B reloads (F5) even if pagehide/leave was skipped -> same sessionStorage ID, still 1 slot
  roomB2.init('guild_phan_thien', 'W', 1);

  assert.equal(peersSeenByA.length, 1);
  assert.equal(peersSeenByA[0].id, roomB1.getLocalPlayer().id);
  assert.equal(peersSeenByA[0].guildId, 'guild_phan_thien');
  assert.equal(peersSeenByA[0].stance, 'W');
  assert.equal(peersSeenByA[0].slotIndex, firstSlot);
});

test('P2P onPeerLeave removes mapped playerId immediately even when transport peerId differs from forger_* playerId', (t) => {
  const net = createFakeP2PNetwork();
  let now = 2_000_000;

  let peersSeenByA: PeerPresence[] = [];
  let leftIds: string[] = [];
  const roomA = new RealtimeRoomClient(
    {
      onPeersChange: (peers) => {
        peersSeenByA = peers;
      },
      onPeerLeft: (id) => {
        leftIds.push(id);
      },
    },
    {
      playerId: 'forger_alpha',
      now: () => ++now,
      createBroadcastChannel: () => null,
      joinRoomFn: net.joinRoomFn,
    }
  );
  const roomB = new RealtimeRoomClient(
    {},
    {
      playerId: 'forger_beta',
      now: () => ++now,
      createBroadcastChannel: () => null,
      joinRoomFn: net.joinRoomFn,
    }
  );
  t.after(() => {
    roomB.destroy();
    roomA.destroy();
  });

  roomA.init('guild_thien_thai', 'Q', 1);
  roomB.init('guild_van_kiem', 'E', 1);

  assert.equal(peersSeenByA.length, 1);
  assert.equal(peersSeenByA[0].id, 'forger_beta');

  // Simulate abrupt WebRTC disconnect (only Trystero transportPeerId 'trystero_peer_2' drops)
  net.disconnectTransport('vault_1', 'trystero_peer_2');

  assert.equal(peersSeenByA.length, 0);
  assert.deepEqual(leftIds, ['forger_beta']);
});

test('evicts old playerId when same transport peer reconnects with new playerId and blocks zombie strikes after leave', (t) => {
  const bus = createBroadcastBus();
  const net = createFakeP2PNetwork();
  let now = 3_000_000;

  let peersSeenByA: PeerPresence[] = [];
  const roomA = new RealtimeRoomClient(
    {
      onPeersChange: (peers) => {
        peersSeenByA = peers;
      },
    },
    {
      playerId: 'forger_host_1',
      now: () => ++now,
      createBroadcastChannel: (name) => bus.create(name),
      joinRoomFn: net.joinRoomFn,
    }
  );
  const channelB = bus.create('phatroi_celestial_room_v1_vault_1');
  t.after(() => {
    channelB.close();
    roomA.destroy();
  });

  roomA.init('guild_thien_thai', 'Q', 1);

  channelB.postMessage({
    type: 'presence',
    vaultId: 1,
    payload: {
      id: 'forger_ghost_old',
      name: 'Khách 1',
      guildId: 'guild_thien_thai',
      stance: 'Q',
      slotIndex: 3,
      sessionEpoch: 100,
      lastSeen: now,
    },
  });
  assert.equal(peersSeenByA.length, 1);

  channelB.postMessage({
    type: 'leave',
    vaultId: 1,
    payload: {
      peerId: 'forger_ghost_old',
      vaultId: 1,
      sessionEpoch: 100,
      timestamp: now,
    },
  });
  assert.equal(peersSeenByA.length, 0);

  // Delayed strike/presence from the same dead sessionEpoch must NOT resurrect ghost slot
  channelB.postMessage({
    type: 'strike',
    vaultId: 1,
    payload: {
      peerId: 'forger_ghost_old',
      name: 'Khách 1',
      slotIndex: 3,
      stance: 'Q',
      damage: 100,
      isGolden: false,
      sessionEpoch: 100,
      timestamp: now,
    },
  });
  channelB.postMessage({
    type: 'presence',
    vaultId: 1,
    payload: {
      id: 'forger_ghost_old',
      name: 'Khách 1',
      guildId: 'guild_thien_thai',
      stance: 'Q',
      slotIndex: 3,
      sessionEpoch: 100,
      lastSeen: now,
    },
  });
  assert.equal(peersSeenByA.length, 0);

  // New sessionEpoch after F5 with the same tab ID IS admitted cleanly into 1 slot
  channelB.postMessage({
    type: 'presence',
    vaultId: 1,
    payload: {
      id: 'forger_ghost_old',
      name: 'Khách 1',
      guildId: 'guild_thien_thai',
      stance: 'Q',
      slotIndex: 3,
      sessionEpoch: 200,
      lastSeen: now,
    },
  });
  assert.equal(peersSeenByA.length, 1);
});

test('two distinct tabs assign unique non-colliding slots without ping-ponging', (t) => {
  const bus = createBroadcastBus();
  const net = createFakeP2PNetwork();
  let now = 4_000_000;

  const roomA = new RealtimeRoomClient(
    {},
    {
      playerId: 'forger_100',
      now: () => ++now,
      createBroadcastChannel: (name) => bus.create(name),
      joinRoomFn: net.joinRoomFn,
    }
  );
  const roomB = new RealtimeRoomClient(
    {},
    {
      playerId: 'forger_200',
      now: () => ++now,
      createBroadcastChannel: (name) => bus.create(name),
      joinRoomFn: net.joinRoomFn,
    }
  );
  t.after(() => {
    roomB.destroy();
    roomA.destroy();
  });

  roomA.init('guild_thien_thai', 'Q', 1);
  roomB.init('guild_phan_thien', 'W', 1);

  const slotA = roomA.getLocalPlayer().slotIndex;
  const slotB = roomB.getLocalPlayer().slotIndex;
  assert.notEqual(slotA, slotB);
  assert.equal(roomA.getPeers().length, 1);
  assert.equal(roomB.getPeers().length, 1);
  assert.equal(roomA.getPeers()[0].slotIndex, slotB);
  assert.equal(roomB.getPeers()[0].slotIndex, slotA);
});

test('evicts previous playerId immediately when same P2P transportPeerId announces a new playerId', (t) => {
  const net = createFakeP2PNetwork();
  let now = 5_000_000;

  let peersSeenByA: PeerPresence[] = [];
  const roomA = new RealtimeRoomClient(
    {
      onPeersChange: (peers) => {
        peersSeenByA = peers;
      },
    },
    {
      playerId: 'forger_host_p2p',
      now: () => ++now,
      createBroadcastChannel: () => null,
      joinRoomFn: net.joinRoomFn,
    }
  );
  const fakeJoin = net.joinRoomFn({}, 'vault_1');
  const sendPresence = fakeJoin.makeAction('presence');
  t.after(() => {
    roomA.destroy();
  });

  roomA.init('guild_thien_thai', 'Q', 1);

  sendPresence.send({
    id: 'forger_old_tab',
    name: 'Đồng Môn A',
    guildId: 'guild_thien_thai',
    stance: 'Q',
    slotIndex: 1,
    lastSeen: now,
  });
  assert.equal(peersSeenByA.length, 1);
  assert.equal(peersSeenByA[0].id, 'forger_old_tab');

  // Same underlying transportPeerId now sends presence with a new playerId -> old ID must be evicted
  sendPresence.send({
    id: 'forger_new_tab',
    name: 'Đồng Môn A',
    guildId: 'guild_phan_thien',
    stance: 'W',
    slotIndex: 3,
    lastSeen: now,
  });
  assert.equal(peersSeenByA.length, 1);
  assert.equal(peersSeenByA[0].id, 'forger_new_tab');
  assert.equal(peersSeenByA[0].slotIndex, 3);
});
