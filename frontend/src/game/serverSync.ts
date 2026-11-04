// ==============================================================================
// DỰ ÁN WEBGAME "PHÁ TRỜI" - THE CELESTIAL FORGE (phatroi.com)
// CLOUDFLARE WORKER API CLIENT - Bền vững, Single Source of Truth
// ==============================================================================

import { safeStorage } from './storage';

export interface ServerBossState {
  success: boolean;
  vaultId: number;
  name: string;
  currentHp: number;
  maxHp: number;
  currentArmor: number;
  maxArmor: number;
  serverFurnaceHeat: number;
  serverAnvilHp: number;
  shatterUntil: number;
  isShieldBroken: boolean;
  totalContributors: number;
  serverTime: number;
}

export interface ServerStrikePayload {
  playerId: string;
  playerName: string;
  vaultId: number;
  damage: number;
  raidContribution: number;
  shatterPoints: number;
  furnaceCooling: number;
  anvilRepair: number;
}

export interface LeaderboardEntry {
  player_id: string;
  player_name: string;
  guild_id?: string;
  total_damage: number;
  raid_score: number;
  last_hit_at: number;
}

class ServerSyncClient {
  private primaryBaseUrl: string;
  private isConnected: boolean = false;
  private lastSuccessfulSync: number = 0;
  private consecutiveFailures: number = 0;

  constructor() {
    if (typeof window !== 'undefined') {
      const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
      // Nếu chạy local thử nghiệm, thử cổng 8787 của wrangler hoặc cùng domain
      if (isLocal) {
        this.primaryBaseUrl = 'https://phatroi-api.beanbinh2000.workers.dev/api';
      } else {
        // Trên môi trường production phatroi.com hoặc github.io
        this.primaryBaseUrl = 'https://phatroi-api.beanbinh2000.workers.dev/api';
      }
    } else {
      this.primaryBaseUrl = 'https://phatroi.com/api';
    }
  }

  public isServerConnected(): boolean {
    return this.isConnected;
  }

  public getLastSyncTime(): number {
    return this.lastSuccessfulSync;
  }

  /**
   * Lấy trạng thái Boss toàn cầu từ Cloudflare Worker API
   */
  public async fetchBossState(vaultId: number = 1): Promise<ServerBossState | null> {
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 4000); // 4s timeout

      const res = await fetch(`${this.primaryBaseUrl}/boss?vaultId=${vaultId}&_t=${Date.now()}`, {
        method: 'GET',
        headers: { 'Accept': 'application/json' },
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!res.ok) {
        this.markFailure();
        return null;
      }

      const data = (await res.json()) as ServerBossState;
      if (data && typeof data.currentHp === 'number') {
        this.markSuccess();
        return data;
      }
      return null;
    } catch {
      this.markFailure();
      return null;
    }
  }

  /**
   * Gửi gói gom đòn sát thương (Batched Strikes) lên Cloudflare Worker để trừ máu nguyên tử
   */
  public async sendBatchedStrike(payload: ServerStrikePayload): Promise<ServerBossState | null> {
    if (payload.damage <= 0 && payload.raidContribution <= 0 && payload.shatterPoints <= 0) {
      return null;
    }

    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 4500);

      const res = await fetch(`${this.primaryBaseUrl}/boss/strike`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify(payload),
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!res.ok) {
        this.markFailure();
        return null;
      }

      const json = await res.json() as { success: boolean; state?: ServerBossState };
      if (json && json.success && json.state) {
        this.markSuccess();
        return json.state;
      }
      return null;
    } catch {
      this.markFailure();
      return null;
    }
  }

  /**
   * Lấy bảng xếp hạng Top cống hiến toàn server
   */
  public async fetchLeaderboard(limit: number = 20): Promise<LeaderboardEntry[]> {
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 4000);

      const res = await fetch(`${this.primaryBaseUrl}/leaderboard?limit=${limit}`, {
        method: 'GET',
        headers: { 'Accept': 'application/json' },
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (res.ok) {
        const json = await res.json() as { success: boolean; leaderboard?: LeaderboardEntry[] };
        if (json && json.leaderboard) {
          return json.leaderboard;
        }
      }
    } catch {
      // Bỏ qua lỗi leaderboard
    }
    return [];
  }

  private markSuccess() {
    this.isConnected = true;
    this.consecutiveFailures = 0;
    this.lastSuccessfulSync = Date.now();
  }

  private markFailure() {
    this.consecutiveFailures++;
    if (this.consecutiveFailures >= 3) {
      this.isConnected = false;
    }
  }
}

export const serverSyncClient = new ServerSyncClient();
