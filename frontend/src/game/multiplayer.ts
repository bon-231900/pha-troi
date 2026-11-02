// ============================================================================
// DỰ ÁN WEBGAME "PHÁ TRỜI" - THE CELESTIAL FORGE (phatroi.com)
// REAL-TIME MULTIPLAYER WEBSOCKET SYNC CLIENT (Task 2 & Anti-Cheat Batched Ticks)
// ============================================================================

export interface BatchedHit {
  stance: string;
  quality: string;
  damage: number;
  resonance: number;
  offsetMs: number;
  isCrit: boolean;
}

export interface ServerHeartbeat {
  t: number;
  layer: number;
  name: string;
  hp: string;
  maxHp: string;
  dps: number;
  res: number;
  resReq: number;
  shatter_sec: number;
  golden_shower_sec: number;
  ccu: number;
  districtId?: string;
  districtSparks?: Array<{ x: number; y: number; stance: string; intensity: number }>;
  globalPulse?: {
    phase: 'countdown' | 'pulse_window' | 'buff_active';
    timeRemaining: number;
    perfectRatio: number;
    buffActive: boolean;
    buffMultiplier: number;
  };
  fx?: number[];
}

export interface MultiplayerCallbacks {
  onConnected?: (districtId: string) => void;
  onDisconnected?: () => void;
  onHeartbeat?: (heartbeat: ServerHeartbeat) => void;
  onPeerSparks?: (count: number) => void;
}

export class MultiplayerClient {
  private ws: WebSocket | null = null;
  private serverUrl: string;
  private playerId: string;
  private districtId: string = "D-1";
  private isConnected: boolean = false;
  private pendingHits: BatchedHit[] = [];
  private batchTimer: ReturnType<typeof setInterval> | null = null;
  private reconnectTimer: ReturnType<typeof setTimeout> | null = null;
  private callbacks: MultiplayerCallbacks;

  constructor(callbacks: MultiplayerCallbacks = {}) {
    this.callbacks = callbacks;
    const isLocal = typeof window !== 'undefined' && (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1');
    const protocol = typeof window !== 'undefined' && window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    this.serverUrl = isLocal ? 'ws://localhost:8080' : `${protocol}//api.phatroi.com`;
    this.playerId = typeof localStorage !== 'undefined' && localStorage.getItem('phatroi_user')
      ? localStorage.getItem('phatroi_user')!
      : `Thợ_Rèn_${Math.floor(Math.random() * 89999 + 10000)}`;

    if (typeof localStorage !== 'undefined' && !localStorage.getItem('phatroi_user')) {
      localStorage.setItem('phatroi_user', this.playerId);
    }
  }

  public connect() {
    if (typeof window === 'undefined') return;

    try {
      this.ws = new WebSocket(this.serverUrl);

      this.ws.onopen = () => {
        this.isConnected = true;
        this.ws?.send(JSON.stringify({
          type: 'join_district',
          playerId: this.playerId,
          districtId: this.districtId
        }));
        this.startBatchLoop();
        this.callbacks.onConnected?.(this.districtId);
      };

      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          if (data.type === 'init') {
            if (data.districtId) this.districtId = data.districtId;
            this.callbacks.onHeartbeat?.(data);
          } else if (data.hp) {
            if (data.districtId) this.districtId = data.districtId;
            this.callbacks.onHeartbeat?.(data);
            if (Array.isArray(data.districtSparks) && data.districtSparks.length > 0) {
              this.callbacks.onPeerSparks?.(data.districtSparks.length);
            }
          }
        } catch {
          // Ignore invalid frames
        }
      };

      this.ws.onclose = () => {
        this.handleDisconnect();
      };

      this.ws.onerror = () => {
        this.handleDisconnect();
      };
    } catch {
      this.handleDisconnect();
    }
  }

  private handleDisconnect() {
    this.isConnected = false;
    this.stopBatchLoop();
    this.callbacks.onDisconnected?.();
    this.scheduleReconnect();
  }

  private scheduleReconnect() {
    if (this.reconnectTimer) return;
    this.reconnectTimer = setTimeout(() => {
      this.reconnectTimer = null;
      this.connect();
    }, 12000);
  }

  public recordStrike(hit: BatchedHit) {
    this.pendingHits.push(hit);
    if (this.pendingHits.length >= 15) {
      this.flushBatch();
    }
  }

  private startBatchLoop() {
    if (this.batchTimer) clearInterval(this.batchTimer);
    this.batchTimer = setInterval(() => this.flushBatch(), 1000);
  }

  private stopBatchLoop() {
    if (this.batchTimer) {
      clearInterval(this.batchTimer);
      this.batchTimer = null;
    }
  }

  private flushBatch() {
    if (!this.isConnected || !this.ws || this.ws.readyState !== WebSocket.OPEN) return;
    if (this.pendingHits.length === 0) return;

    const packet = {
      type: 'batch_strike',
      playerId: this.playerId,
      districtId: this.districtId,
      timestamp: Date.now(),
      hits: this.pendingHits
    };

    try {
      this.ws.send(JSON.stringify(packet));
      this.pendingHits = [];
    } catch {
      // Keep in queue for next tick
    }
  }

  public disconnect() {
    this.stopBatchLoop();
    if (this.reconnectTimer) clearTimeout(this.reconnectTimer);
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
    this.isConnected = false;
  }

  public getOnlineStatus(): boolean {
    return this.isConnected;
  }

  public getPlayerId(): string {
    return this.playerId;
  }

  public getDistrictId(): string {
    return this.districtId;
  }
}
