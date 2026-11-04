// ==============================================================================
// DỰ ÁN WEBGAME "PHÁ TRỜI" (PHATROI.COM) - CLOUDFLARE WORKERS API
// Single Source of Truth cho Máu Boss, Giáp, Đe Rèn & Google Sign-In Cloud Save
// ==============================================================================

export interface Env {
  DB?: D1Database;
  PHATROI_KV?: KVNamespace;
  ADMIN_API_KEY?: string;
}

const EXPECTED_GOOGLE_CLIENT_ID = '325984073866-an8facrtq5edm0aetm5ok3qmrf00oq7t.apps.googleusercontent.com';

interface BossStateRecord {
  vault_id: number;
  name: string;
  current_hp: number;
  max_hp: number;
  current_armor: number;
  max_armor: number;
  server_furnace_heat: number;
  server_anvil_hp: number;
  shatter_until: number;
  last_strike_at: number;
  updated_at: number;
}

interface LeaderboardRecord {
  player_id: string;
  player_name: string;
  guild_id: string;
  total_damage: number;
  raid_score: number;
  last_hit_at: number;
}

interface PlayerProfileRecord {
  google_id: string;
  email: string;
  display_name: string;
  avatar_url: string;
  save_data: string;
  last_sync_at: number;
  created_at: number;
}

// In-Memory Fallback nếu chưa kết nối D1 Database
const memoryBossState: Record<number, BossStateRecord> = {
  1: {
    vault_id: 1,
    name: 'Thiết Vân Vòm',
    current_hp: 1500000000,
    max_hp: 1500000000,
    current_armor: 500,
    max_armor: 500,
    server_furnace_heat: 0,
    server_anvil_hp: 10000,
    shatter_until: 0,
    last_strike_at: Date.now(),
    updated_at: Date.now(),
  },
};

const memoryLeaderboard = new Map<string, LeaderboardRecord>();
const memoryProfiles = new Map<string, PlayerProfileRecord>();

const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Admin-Key',
  'Content-Type': 'application/json; charset=utf-8',
};

function jsonResponse(data: unknown, status: number = 200): Response {
  return new Response(JSON.stringify(data), {
    status,
    headers: CORS_HEADERS,
  });
}

function decodeGoogleJwt(jwt: string): { sub: string; email: string; name: string; picture?: string; aud: string; exp: number } | null {
  try {
    const parts = jwt.split('.');
    if (parts.length !== 3) return null;
    const base64Url = parts[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map((c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    );
    return JSON.parse(jsonPayload);
  } catch {
    return null;
  }
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    // 1. Xử lý CORS Preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        status: 204,
        headers: CORS_HEADERS,
      });
    }

    const url = new URL(request.url);
    const pathname = url.pathname.replace(/\/+$/, '') || '/';

    try {
      // 2. Health check endpoint
      if (pathname === '/health' || pathname === '/' || pathname === '/api') {
        return jsonResponse({
          status: 'online',
          title: 'Toàn Dân Phá Trời - Cloudflare Edge Gateway',
          domain: 'phatroi.com',
          edgeTime: Date.now(),
        });
      }

      // 3. GET /api/boss - Lấy máu Boss & trạng thái Cửu Trọng Thiên
      if (request.method === 'GET' && pathname === '/api/boss') {
        const vaultId = parseInt(url.searchParams.get('vaultId') || '1', 10);
        const state = await getBossState(env, vaultId);
        const count = await getContributorCount(env);

        return jsonResponse({
          success: true,
          vaultId: state.vault_id,
          name: state.name,
          currentHp: state.current_hp,
          maxHp: state.max_hp,
          currentArmor: state.current_armor,
          maxArmor: state.max_armor,
          serverFurnaceHeat: state.server_furnace_heat,
          serverAnvilHp: state.server_anvil_hp,
          shatterUntil: state.shatter_until,
          isShieldBroken: state.current_armor <= 0 || Date.now() < state.shatter_until,
          totalContributors: count,
          serverTime: Date.now(),
        });
      }

      // 4. POST /api/boss/strike - Gom đòn sát thương (Batched Strike) & Trừ máu nguyên tử
      if (request.method === 'POST' && pathname === '/api/boss/strike') {
        const body = (await request.json().catch(() => ({}))) as Record<string, unknown>;

        const playerId = String(body.playerId || 'anonymous').trim().slice(0, 64);
        const playerName = String(body.playerName || 'Thợ Rèn Ẩn Danh').trim().slice(0, 64);
        const vaultId = Math.max(1, Math.min(9, parseInt(String(body.vaultId || '1'), 10)));
        const damage = Math.max(0, Math.min(100_000_000, Number(body.damage) || 0)); // Chống exploit
        const raidContribution = Math.max(0, Math.min(500_000, Number(body.raidContribution) || 0));
        const shatterPoints = Math.max(0, Math.min(500, Number(body.shatterPoints) || 0));
        const furnaceCooling = Math.max(-500, Math.min(500, Number(body.furnaceCooling) || 0));
        const anvilRepair = Math.max(0, Math.min(1000, Number(body.anvilRepair) || 0));

        const updatedState = await applyStrikeToBoss(env, {
          vaultId,
          playerId,
          playerName,
          damage,
          raidContribution,
          shatterPoints,
          furnaceCooling,
          anvilRepair,
        });

        return jsonResponse({
          success: true,
          appliedDamage: damage,
          state: {
            vaultId: updatedState.vault_id,
            name: updatedState.name,
            currentHp: updatedState.current_hp,
            maxHp: updatedState.max_hp,
            currentArmor: updatedState.current_armor,
            maxArmor: updatedState.max_armor,
            serverFurnaceHeat: updatedState.server_furnace_heat,
            serverAnvilHp: updatedState.server_anvil_hp,
            shatterUntil: updatedState.shatter_until,
            isShieldBroken: updatedState.current_armor <= 0 || Date.now() < updatedState.shatter_until,
            serverTime: Date.now(),
          },
        });
      }

      // 5. GET /api/leaderboard - Bảng xếp hạng Vạn Dân
      if (request.method === 'GET' && pathname === '/api/leaderboard') {
        const limit = Math.max(1, Math.min(100, parseInt(url.searchParams.get('limit') || '20', 10)));
        const leaderboard = await getLeaderboard(env, limit);

        return jsonResponse({
          success: true,
          leaderboard,
          serverTime: Date.now(),
        });
      }

      // 6. POST /api/auth/google - Xác thực Đăng Nhập Google & Nạp Hồ Sơ Cloud
      if (request.method === 'POST' && pathname === '/api/auth/google') {
        const body = (await request.json().catch(() => ({}))) as Record<string, unknown>;
        const credential = String(body.credential || '').trim();
        const accessToken = String(body.accessToken || '').trim();
        const localSaveData = typeof body.localSaveData === 'string' ? body.localSaveData : '';

        let userSub = '';
        let userEmail = '';
        let userName = '';
        let userPicture = '';

        if (credential) {
          const decoded = decodeGoogleJwt(credential);
          if (decoded && decoded.sub && decoded.email) {
            userSub = decoded.sub;
            userEmail = decoded.email;
            userName = decoded.name || 'Thợ Rèn Google';
            userPicture = decoded.picture || '';
          }
        } else if (accessToken) {
          try {
            const googleRes = await fetch('https://www.googleapis.com/oauth2/v3/userinfo', {
              headers: { Authorization: `Bearer ${accessToken}` },
            });
            if (googleRes.ok) {
              const info = (await googleRes.json()) as Record<string, unknown>;
              userSub = String(info.sub || '');
              userEmail = String(info.email || '');
              userName = String(info.name || info.email || 'Thợ Rèn Google');
              userPicture = String(info.picture || '');
            }
          } catch (e) {
            console.error('[Google UserInfo Error]', e);
          }
        }

        if (!userSub || !userEmail) {
          return jsonResponse({ success: false, error: 'Xác thực tài khoản Google không thành công' }, 401);
        }

        const now = Date.now();
        const existingProfile = await getPlayerProfile(env, userSub);

        if (existingProfile) {
          return jsonResponse({
            success: true,
            isNew: false,
            profile: {
              googleId: existingProfile.google_id,
              email: existingProfile.email,
              name: existingProfile.display_name,
              avatar: existingProfile.avatar_url,
            },
            saveData: existingProfile.save_data,
            lastSyncAt: existingProfile.last_sync_at,
          });
        }

        // Tạo hồ sơ mới & liên kết tiến trình Guest hiện tại lên Cloud
        const newProfile: PlayerProfileRecord = {
          google_id: userSub,
          email: userEmail,
          display_name: userName || 'Thợ Rèn Google',
          avatar_url: userPicture || '',
          save_data: localSaveData || '{}',
          last_sync_at: now,
          created_at: now,
        };

        await upsertPlayerProfile(env, newProfile);

        return jsonResponse({
          success: true,
          isNew: true,
          profile: {
            googleId: newProfile.google_id,
            email: newProfile.email,
            name: newProfile.display_name,
            avatar: newProfile.avatar_url,
          },
          saveData: newProfile.save_data,
          lastSyncAt: now,
        });
      }

      // 7. POST /api/player/cloud-save - Lưu trữ tiến độ lên Mây (Cloud Save)
      if (request.method === 'POST' && pathname === '/api/player/cloud-save') {
        const body = (await request.json().catch(() => ({}))) as Record<string, unknown>;
        const googleId = String(body.googleId || '').trim();
        const saveData = typeof body.saveData === 'string' ? body.saveData : '';

        if (!googleId || !saveData) {
          return jsonResponse({ success: false, error: 'Thiếu googleId hoặc saveData' }, 400);
        }

        const now = Date.now();
        const updated = await updatePlayerSaveData(env, googleId, saveData, now);

        if (updated) {
          return jsonResponse({
            success: true,
            lastSyncAt: now,
          });
        }
        return jsonResponse({ success: false, error: 'Không tìm thấy hồ sơ người chơi' }, 404);
      }

      // 8. GET /api/player/cloud-load - Tải tiến độ từ Mây
      if (request.method === 'GET' && pathname === '/api/player/cloud-load') {
        const googleId = String(url.searchParams.get('googleId') || '').trim();
        if (!googleId) {
          return jsonResponse({ success: false, error: 'Thiếu googleId' }, 400);
        }

        const profile = await getPlayerProfile(env, googleId);
        if (profile) {
          return jsonResponse({
            success: true,
            profile: {
              googleId: profile.google_id,
              email: profile.email,
              name: profile.display_name,
              avatar: profile.avatar_url,
            },
            saveData: profile.save_data,
            lastSyncAt: profile.last_sync_at,
          });
        }
        return jsonResponse({ success: false, error: 'Không tìm thấy hồ sơ' }, 404);
      }

      // 9. POST /api/boss/reset - Admin Reset Boss (Kiểm tra Secret Key)
      if (request.method === 'POST' && pathname === '/api/boss/reset') {
        const adminKey = request.headers.get('X-Admin-Key') || url.searchParams.get('key');
        if (env.ADMIN_API_KEY && adminKey !== env.ADMIN_API_KEY) {
          return jsonResponse({ success: false, error: 'Unauthorized' }, 401);
        }

        const vaultId = parseInt(url.searchParams.get('vaultId') || '1', 10);
        await resetBossState(env, vaultId);

        return jsonResponse({
          success: true,
          message: `Đã reset trạng thái Tầng ${vaultId} về ban đầu!`,
          serverTime: Date.now(),
        });
      }

      return jsonResponse({ error: 'Endpoint Not Found' }, 404);
    } catch (err: unknown) {
      const errorMsg = err instanceof Error ? err.message : String(err);
      return jsonResponse({ success: false, error: errorMsg }, 500);
    }
  },
};

// ==============================================================================
// DATABASE ACCESS ADAPTER (D1 -> Memory Fallback)
// ==============================================================================

async function getBossState(env: Env, vaultId: number): Promise<BossStateRecord> {
  if (env.DB) {
    try {
      const row = await env.DB.prepare(
        'SELECT * FROM boss_state WHERE vault_id = ?'
      ).bind(vaultId).first<BossStateRecord>();

      if (row) return row;

      const defaultState: BossStateRecord = {
        vault_id: vaultId,
        name: `Tầng ${vaultId}`,
        current_hp: 1500000000,
        max_hp: 1500000000,
        current_armor: 500,
        max_armor: 500,
        server_furnace_heat: 0,
        server_anvil_hp: 10000,
        shatter_until: 0,
        last_strike_at: Date.now(),
        updated_at: Date.now(),
      };

      await env.DB.prepare(`
        INSERT OR IGNORE INTO boss_state (vault_id, name, current_hp, max_hp, current_armor, max_armor, server_furnace_heat, server_anvil_hp, shatter_until, last_strike_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
      `).bind(
        vaultId, defaultState.name, defaultState.current_hp, defaultState.max_hp,
        defaultState.current_armor, defaultState.max_armor, defaultState.server_furnace_heat,
        defaultState.server_anvil_hp, defaultState.shatter_until, defaultState.last_strike_at, defaultState.updated_at
      ).run();

      return defaultState;
    } catch (e) {
      console.error('[D1 Error getBossState]', e);
    }
  }

  if (!memoryBossState[vaultId]) {
    memoryBossState[vaultId] = {
      vault_id: vaultId,
      name: `Tầng ${vaultId}`,
      current_hp: 1500000000,
      max_hp: 1500000000,
      current_armor: 500,
      max_armor: 500,
      server_furnace_heat: 0,
      server_anvil_hp: 10000,
      shatter_until: 0,
      last_strike_at: Date.now(),
      updated_at: Date.now(),
    };
  }

  return memoryBossState[vaultId];
}

async function applyStrikeToBoss(
  env: Env,
  strike: {
    vaultId: number;
    playerId: string;
    playerName: string;
    damage: number;
    raidContribution: number;
    shatterPoints: number;
    furnaceCooling: number;
    anvilRepair: number;
  }
): Promise<BossStateRecord> {
  const now = Date.now();

  if (env.DB) {
    try {
      await getBossState(env, strike.vaultId);

      await env.DB.prepare(`
        UPDATE boss_state
        SET 
          current_hp = MAX(0, current_hp - ?),
          current_armor = MAX(0, current_armor - ?),
          server_furnace_heat = MAX(0, MIN(10000, server_furnace_heat + ?)),
          server_anvil_hp = MIN(10000, MAX(0, server_anvil_hp + ?)),
          last_strike_at = ?,
          updated_at = ?
        WHERE vault_id = ?
      `).bind(
        strike.damage,
        strike.shatterPoints,
        strike.furnaceCooling,
        strike.anvilRepair,
        now,
        now,
        strike.vaultId
      ).run();

      if (strike.playerId && (strike.damage > 0 || strike.raidContribution > 0)) {
        await env.DB.prepare(`
          INSERT INTO leaderboard (player_id, player_name, total_damage, raid_score, last_hit_at)
          VALUES (?, ?, ?, ?, ?)
          ON CONFLICT(player_id) DO UPDATE SET
            total_damage = total_damage + excluded.total_damage,
            raid_score = raid_score + excluded.raid_score,
            player_name = excluded.player_name,
            last_hit_at = excluded.last_hit_at
        `).bind(strike.playerId, strike.playerName, strike.damage, strike.raidContribution, now).run();
      }

      return await getBossState(env, strike.vaultId);
    } catch (e) {
      console.error('[D1 Error applyStrikeToBoss]', e);
    }
  }

  const state = await getBossState(env, strike.vaultId);
  state.current_hp = Math.max(0, state.current_hp - strike.damage);
  state.current_armor = Math.max(0, state.current_armor - strike.shatterPoints);
  state.server_furnace_heat = Math.max(0, Math.min(10000, state.server_furnace_heat + strike.furnaceCooling));
  state.server_anvil_hp = Math.max(0, Math.min(10000, state.server_anvil_hp + strike.anvilRepair));
  state.last_strike_at = now;
  state.updated_at = now;

  if (strike.playerId && (strike.damage > 0 || strike.raidContribution > 0)) {
    const existing = memoryLeaderboard.get(strike.playerId) || {
      player_id: strike.playerId,
      player_name: strike.playerName,
      guild_id: 'Vạn Dân',
      total_damage: 0,
      raid_score: 0,
      last_hit_at: now,
    };
    existing.total_damage += strike.damage;
    existing.raid_score += strike.raidContribution;
    existing.player_name = strike.playerName;
    existing.last_hit_at = now;
    memoryLeaderboard.set(strike.playerId, existing);
  }

  return state;
}

async function getLeaderboard(env: Env, limit: number): Promise<LeaderboardRecord[]> {
  if (env.DB) {
    try {
      const { results } = await env.DB.prepare(`
        SELECT player_id, player_name, guild_id, total_damage, raid_score, last_hit_at
        FROM leaderboard
        ORDER BY total_damage DESC
        LIMIT ?
      `).bind(limit).all<LeaderboardRecord>();
      return results || [];
    } catch (e) {
      console.error('[D1 Error getLeaderboard]', e);
    }
  }

  return Array.from(memoryLeaderboard.values())
    .sort((a, b) => b.total_damage - a.total_damage)
    .slice(0, limit);
}

async function getContributorCount(env: Env): Promise<number> {
  if (env.DB) {
    try {
      const res = await env.DB.prepare('SELECT COUNT(*) as count FROM leaderboard').first<{ count: number }>();
      return res?.count || 1;
    } catch {
      return 1;
    }
  }
  return Math.max(1, memoryLeaderboard.size);
}

async function resetBossState(env: Env, vaultId: number): Promise<void> {
  if (env.DB) {
    try {
      await env.DB.prepare(`
        UPDATE boss_state
        SET current_hp = max_hp, current_armor = max_armor, server_furnace_heat = 0, server_anvil_hp = 10000, updated_at = ?
        WHERE vault_id = ?
      `).bind(Date.now(), vaultId).run();
      return;
    } catch (e) {
      console.error('[D1 Error resetBossState]', e);
    }
  }

  if (memoryBossState[vaultId]) {
    memoryBossState[vaultId].current_hp = memoryBossState[vaultId].max_hp;
    memoryBossState[vaultId].current_armor = memoryBossState[vaultId].max_armor;
    memoryBossState[vaultId].server_furnace_heat = 0;
    memoryBossState[vaultId].server_anvil_hp = 10000;
  }
}

// ==============================================================================
// PLAYER PROFILE & CLOUD SAVE D1 ADAPTER
// ==============================================================================

async function getPlayerProfile(env: Env, googleId: string): Promise<PlayerProfileRecord | null> {
  if (env.DB) {
    try {
      const row = await env.DB.prepare(
        'SELECT google_id, email, display_name, avatar_url, save_data, last_sync_at, created_at FROM player_profiles WHERE google_id = ?'
      ).bind(googleId).first<PlayerProfileRecord>();
      if (row) return row;
    } catch (e) {
      console.error('[D1 Error getPlayerProfile]', e);
    }
  }
  return memoryProfiles.get(googleId) || null;
}

async function upsertPlayerProfile(env: Env, profile: PlayerProfileRecord): Promise<void> {
  if (env.DB) {
    try {
      await env.DB.prepare(`
        INSERT INTO player_profiles (google_id, email, display_name, avatar_url, save_data, last_sync_at, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(google_id) DO UPDATE SET
          display_name = excluded.display_name,
          avatar_url = excluded.avatar_url,
          save_data = excluded.save_data,
          last_sync_at = excluded.last_sync_at
      `).bind(
        profile.google_id,
        profile.email,
        profile.display_name,
        profile.avatar_url,
        profile.save_data,
        profile.last_sync_at,
        profile.created_at
      ).run();
      return;
    } catch (e) {
      console.error('[D1 Error upsertPlayerProfile]', e);
    }
  }
  memoryProfiles.set(profile.google_id, profile);
}

async function updatePlayerSaveData(env: Env, googleId: string, saveData: string, syncTime: number): Promise<boolean> {
  if (env.DB) {
    try {
      const res = await env.DB.prepare(
        'UPDATE player_profiles SET save_data = ?, last_sync_at = ? WHERE google_id = ?'
      ).bind(saveData, syncTime, googleId).run();
      return res.success;
    } catch (e) {
      console.error('[D1 Error updatePlayerSaveData]', e);
    }
  }
  const existing = memoryProfiles.get(googleId);
  if (existing) {
    existing.save_data = saveData;
    existing.last_sync_at = syncTime;
    return true;
  }
  return false;
}
