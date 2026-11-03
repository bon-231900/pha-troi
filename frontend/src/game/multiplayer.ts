// ============================================================================
// DỰ ÁN WEBGAME "PHÁ TRỜI" - THE CELESTIAL FORGE (phatroi.com)
// REAL-TIME MULTIPLAYER WEBSOCKET SYNC CLIENT & ROBUST OFFLINE FALLBACK
// ============================================================================

import { safeStorage } from './storage';

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
  onOfflineMode?: (isOffline: boolean) => void;
}

export class MultiplayerClient {
  private ws: WebSocket | null = null;
  private serverUrl: string;
  private playerId: string;
  private districtId: string = 'D-1';
  private isConnected: boolean = false;
  private isOffline: boolean = true;
  private pendingHits: BatchedHit[] = [];
  private batchTimer: ReturnType<typeof setInterval> | null = null;
  private reconnectTimer: ReturnType<typeof setTimeout> | null = null;
  private reconnectIntervalMs: number = 30000; // Start backoff at 30s
  private callbacks: MultiplayerCallbacks;

  constructor(callbacks: MultiplayerCallbacks = {}) {
    this.callbacks = callbacks;
    const isLocal =
      typeof window !== 'undefined' &&
      (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1');
    const protocol =
      typeof window !== 'undefined' && window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    this.serverUrl = isLocal ? 'ws://localhost:8080' : `${protocol}//api.phatroi.com`;

    const storedUser = safeStorage.getItem('phatroi_user');
    if (storedUser) {
      this.playerId = storedUser;
    } else {
      this.playerId = `Thợ_Rèn_${Math.floor(Math.random() * 89999 + 10000)}`;
      safeStorage.setItem('phatroi_user', this.playerId);
    }
  }

  public connect() {
    if (typeof window === 'undefined') return;

    try {
      this.ws = new WebSocket(this.serverUrl);

      this.ws.onopen = () => {
        this.isConnected = true;
        this.isOffline = false;
        this.reconnectIntervalMs = 30000; // Reset backoff on success
        this.callbacks.onOfflineMode?.(false);

        this.ws?.send(
          JSON.stringify({
            type: 'join_district',
            playerId: this.playerId,
            districtId: this.districtId,
          })
        );
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
        // Suppress uncaught exception and trigger gentle offline mode
        this.handleDisconnect();
      };
    } catch {
      this.handleDisconnect();
    }
  }

  private handleDisconnect() {
    this.isConnected = false;
    this.isOffline = true;
    this.stopBatchLoop();
    this.callbacks.onDisconnected?.();
    this.callbacks.onOfflineMode?.(true);
    this.scheduleReconnect();
  }

  private scheduleReconnect() {
    if (this.reconnectTimer) return;
    // Exponential backoff capped at 120 seconds to prevent console pollution
    this.reconnectTimer = setTimeout(() => {
      this.reconnectTimer = null;
      this.reconnectIntervalMs = Math.min(120000, this.reconnectIntervalMs * 1.5);
      this.connect();
    }, this.reconnectIntervalMs);
  }

  public recordStrike(hit: BatchedHit) {
    this.pendingHits.push(hit);
    // When offline, keep queue limited to 30 strikes to prevent memory leak
    if (this.isOffline && this.pendingHits.length > 30) {
      this.pendingHits = this.pendingHits.slice(-15);
    }
    if (this.isConnected && this.pendingHits.length >= 15) {
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
      hits: this.pendingHits,
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
      try {
        this.ws.close();
      } catch {}
      this.ws = null;
    }
    this.isConnected = false;
    this.isOffline = true;
  }

  public getOnlineStatus(): boolean {
    return this.isConnected;
  }

  public getIsOffline(): boolean {
    return this.isOffline;
  }

  public getPlayerId(): string {
    return this.playerId;
  }

  public getDistrictId(): string {
    return this.districtId;
  }
}
