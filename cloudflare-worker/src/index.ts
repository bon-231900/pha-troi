// ==============================================================================
// DỰ ÁN WEBGAME "PHÁ TRỜI" (PHATROI.COM) - CLOUDFLARE WORKERS API
// Single Source of Truth cho Máu Boss, Giáp, Đe Rèn & Google Sign-In Cloud Save
// ==============================================================================

import {
  EXPECTED_GOOGLE_CLIENT_ID,
  constantTimeEqual,
  createJwksCache,
  extractBearerToken,
  getSessionSecretError,
  signSessionToken,
  verifyGoogleAccessToken,
  verifyGoogleIdToken,
  verifySessionToken,
} from './auth.ts';
import type { FetchLike, GoogleIdentity, JwksCache } from './auth.ts';
import {
  DEFAULT_SERVER_ANVIL_HP,
  MAX_SERVER_FURNACE_HEAT,
  SHIELD_BREAK_DURATION_MS,
  VAULT_CONFIGS,
  createCanonicalBossState,
  isBossShieldBroken,
  parseStrictVaultId,
  reconcileBossStateRow,
} from './vaults.ts';
import type { BossStateRecord } from './vaults.ts';

export interface Env {
  DB?: D1Database;
  PHATROI_KV?: KVNamespace;
  ADMIN_API_KEY?: string;
  SESSION_SECRET?: string;
  GOOGLE_CLIENT_ID?: string;
}

export interface LeaderboardRecord {
  player_id: string;
  player_name: string;
  guild_id: string;
  total_damage: number;
  raid_score: number;
  last_hit_at: number;
}

export interface PlayerProfileRecord {
  google_id: string;
  email: string;
  display_name: string;
  avatar_url: string;
  save_data: string;
  last_sync_at: number;
  created_at: number;
}

export interface MemoryStore {
  bossState: Record<number, BossStateRecord>;
  leaderboard: Map<string, LeaderboardRecord>;
  profiles: Map<string, PlayerProfileRecord>;
}

export interface WorkerDeps {
  fetch?: FetchLike;
  now?: () => number;
  jwksCache?: JwksCache;
  memoryStore?: MemoryStore;
}

const MAX_SAVE_DATA_BYTES = 512_000;
const utf8Encoder = new TextEncoder();

export function createMemoryStore(): MemoryStore {
  return {
    bossState: {},
    leaderboard: new Map<string, LeaderboardRecord>(),
    profiles: new Map<string, PlayerProfileRecord>(),
  };
}

const defaultMemoryStore: MemoryStore = createMemoryStore();

const CORS_HEADERS: Record<string, string> = {
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

function formatBossStateResponse(state: BossStateRecord, now: number, totalContributors?: number) {
  return {
    vaultId: state.vault_id,
    name: state.name,
    currentHp: state.current_hp,
    maxHp: state.max_hp,
    currentArmor: state.current_armor,
    maxArmor: state.max_armor,
    serverFurnaceHeat: state.server_furnace_heat,
    serverAnvilHp: state.server_anvil_hp,
    shatterUntil: state.shatter_until,
    isShieldBroken: isBossShieldBroken(state, now),
    ...(totalContributors !== undefined ? { totalContributors } : {}),
    serverTime: now,
  };
}

function clampFiniteNumber(raw: unknown, min: number, max: number, fallback: number = 0): number {
  if (raw === undefined || raw === null || raw === '') return fallback;
  const num = typeof raw === 'number' ? raw : Number(raw);
  if (!Number.isFinite(num)) return fallback;
  return Math.max(min, Math.min(max, num));
}

async function readJsonBodyObject(request: Request): Promise<Record<string, unknown> | null> {
  let rawText: string;
  try {
    rawText = await request.text();
  } catch {
    return null;
  }
  if (!rawText || rawText.trim().length === 0) {
    return null;
  }
  try {
    const parsed: unknown = JSON.parse(rawText);
    if (!parsed || typeof parsed !== 'object' || Array.isArray(parsed)) {
      return null;
    }
    return parsed as Record<string, unknown>;
  } catch {
    return null;
  }
}

async function readOptionalJsonBodyObject(
  request: Request
): Promise<{ ok: true; body: Record<string, unknown> | null } | { ok: false }> {
  let rawText: string;
  try {
    rawText = await request.text();
  } catch {
    return { ok: false };
  }
  if (!rawText || rawText.trim().length === 0) {
    return { ok: true, body: null };
  }
  try {
    const parsed: unknown = JSON.parse(rawText);
    if (!parsed || typeof parsed !== 'object' || Array.isArray(parsed)) {
      return { ok: false };
    }
    return { ok: true, body: parsed as Record<string, unknown> };
  } catch {
    return { ok: false };
  }
}

export function createApp(defaultDeps: WorkerDeps = {}) {
  const appJwksCache = defaultDeps.jwksCache ?? createJwksCache();
  const appMemoryStore = defaultDeps.memoryStore ?? createMemoryStore();

  return {
    fetch(request: Request, env: Env, overrideDeps: WorkerDeps = {}): Promise<Response> {
      return handleRequest(request, env, {
        fetch: overrideDeps.fetch ?? defaultDeps.fetch,
        now: overrideDeps.now ?? defaultDeps.now,
        jwksCache: overrideDeps.jwksCache ?? appJwksCache,
        memoryStore: overrideDeps.memoryStore ?? appMemoryStore,
      });
    },
  };
}

export async function handleRequest(
  request: Request,
  env: Env,
  deps: WorkerDeps = {}
): Promise<Response> {
  // 1. CORS Preflight
  if (request.method === 'OPTIONS') {
    return new Response(null, {
      status: 204,
      headers: CORS_HEADERS,
    });
  }

  const nowFn = deps.now ?? (() => Date.now());
  const now = nowFn();
  const fetchFn = deps.fetch ?? fetch;
  const memoryStore = deps.memoryStore ?? defaultMemoryStore;
  const url = new URL(request.url);
  const pathname = url.pathname.replace(/\/+$/, '') || '/';

  try {
    // 2. Health check endpoint
    if (request.method === 'GET' && (pathname === '/health' || pathname === '/' || pathname === '/api')) {
      return jsonResponse({
        status: 'online',
        title: 'Toàn Dân Phá Trời - Cloudflare Edge Gateway',
        domain: 'phatroi.com',
        edgeTime: now,
      });
    }

    // 3. GET /api/boss - Lấy máu Boss & trạng thái Cửu Trọng Thiên (9 tầng)
    if (request.method === 'GET' && pathname === '/api/boss') {
      const rawVaultId = url.searchParams.get('vaultId');
      const vaultId = rawVaultId === null ? 1 : parseStrictVaultId(rawVaultId);
      if (vaultId === null) {
        return jsonResponse(
          { success: false, error: 'vaultId không hợp lệ (chỉ chấp nhận số nguyên 1..9)' },
          400
        );
      }

      const state = await getBossState(env, vaultId, now, memoryStore);
      const count = await getContributorCount(env, memoryStore);

      return jsonResponse({
        success: true,
        ...formatBossStateResponse(state, now, count),
      });
    }

    // 4. POST /api/boss/strike - Gom đòn sát thương (Batched Strike) & Trừ máu nguyên tử
    if (request.method === 'POST' && pathname === '/api/boss/strike') {
      const body = await readJsonBodyObject(request);
      if (!body) {
        return jsonResponse({ success: false, error: 'Invalid JSON request body' }, 400);
      }

      const vaultId = body.vaultId === undefined ? 1 : parseStrictVaultId(body.vaultId);
      if (vaultId === null) {
        return jsonResponse(
          { success: false, error: 'vaultId không hợp lệ (chỉ chấp nhận số nguyên 1..9)' },
          400
        );
      }

      const rawPlayerId = typeof body.playerId === 'string' ? body.playerId.trim() : '';
      const playerId = (rawPlayerId || 'anonymous').slice(0, 64);
      const rawPlayerName = typeof body.playerName === 'string' ? body.playerName.trim() : '';
      const playerName = (rawPlayerName || 'Thợ Rèn Ẩn Danh').slice(0, 64);

      const damage = clampFiniteNumber(body.damage, 0, 100_000_000, 0);
      const raidContribution = clampFiniteNumber(body.raidContribution, 0, 500_000, 0);
      const shatterPoints = clampFiniteNumber(body.shatterPoints, 0, 500, 0);
      const furnaceCooling = clampFiniteNumber(body.furnaceCooling, -500, 500, 0);
      const anvilRepair = clampFiniteNumber(body.anvilRepair, 0, 1000, 0);

      const updatedState = await applyStrikeToBoss(
        env,
        {
          vaultId,
          playerId,
          playerName,
          damage,
          raidContribution,
          shatterPoints,
          furnaceCooling,
          anvilRepair,
        },
        now,
        memoryStore
      );

      return jsonResponse({
        success: true,
        appliedDamage: damage,
        state: formatBossStateResponse(updatedState, now),
      });
    }

    // 5. GET /api/leaderboard - Bảng xếp hạng Vạn Dân
    if (request.method === 'GET' && pathname === '/api/leaderboard') {
      const rawLimit = url.searchParams.get('limit');
      const parsedLimit = rawLimit !== null ? parseInt(rawLimit, 10) : 20;
      const limit = Number.isFinite(parsedLimit) ? Math.max(1, Math.min(100, parsedLimit)) : 20;
      const leaderboard = await getLeaderboard(env, limit, memoryStore);

      return jsonResponse({
        success: true,
        leaderboard,
        serverTime: now,
      });
    }

    // 6. POST /api/auth/google - Xác thực Google ID Token / Access Token & cấp Session JWT
    if (request.method === 'POST' && pathname === '/api/auth/google') {
      const secretError = getSessionSecretError(env.SESSION_SECRET);
      if (secretError) {
        return jsonResponse({ success: false, error: secretError }, 503);
      }

      const body = await readJsonBodyObject(request);
      if (!body) {
        return jsonResponse({ success: false, error: 'Invalid JSON request body' }, 400);
      }

      const credential = typeof body.credential === 'string' ? body.credential.trim() : '';
      const accessToken = typeof body.accessToken === 'string' ? body.accessToken.trim() : '';
      const expectedClientId = env.GOOGLE_CLIENT_ID?.trim() || EXPECTED_GOOGLE_CLIENT_ID;

      let identity: GoogleIdentity | null = null;
      if (credential) {
        identity = await verifyGoogleIdToken(credential, expectedClientId, {
          fetchFn,
          nowMs: now,
          jwksCache: deps.jwksCache,
        });
      } else if (accessToken) {
        identity = await verifyGoogleAccessToken(accessToken, expectedClientId, {
          fetchFn,
          nowMs: now,
        });
      }

      if (!identity) {
        return jsonResponse(
          { success: false, error: 'Xác thực tài khoản Google không thành công' },
          401
        );
      }

      const session = await signSessionToken(
        { sub: identity.sub, email: identity.email },
        env.SESSION_SECRET!,
        now
      );

      const existingProfile = await getPlayerProfile(env, identity.sub, memoryStore);
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
          sessionToken: session.token,
          sessionExpiresAt: session.expiresAt,
        });
      }

      // Tạo hồ sơ mới độc lập hoàn toàn với chế độ Khách
      const newProfile: PlayerProfileRecord = {
        google_id: identity.sub,
        email: identity.email,
        display_name: identity.name || 'Thợ Rèn Google',
        avatar_url: identity.picture || '',
        save_data: '{}',
        last_sync_at: now,
        created_at: now,
      };

      await upsertPlayerProfile(env, newProfile, memoryStore);

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
        sessionToken: session.token,
        sessionExpiresAt: session.expiresAt,
      });
    }

    // 7. POST /api/player/cloud-save - Lưu tiến độ lên Cloud (Yêu cầu Bearer Session JWT)
    if (request.method === 'POST' && pathname === '/api/player/cloud-save') {
      const secretError = getSessionSecretError(env.SESSION_SECRET);
      if (secretError) {
        return jsonResponse({ success: false, error: secretError }, 503);
      }

      const bearerToken = extractBearerToken(request);
      if (!bearerToken) {
        return jsonResponse({ success: false, error: 'Unauthorized: missing Bearer token' }, 401);
      }

      const session = await verifySessionToken(bearerToken, env.SESSION_SECRET!, now);
      if (!session) {
        return jsonResponse({ success: false, error: 'Unauthorized: invalid or expired session' }, 401);
      }

      const body = await readJsonBodyObject(request);
      if (!body) {
        return jsonResponse({ success: false, error: 'Invalid JSON request body' }, 400);
      }

      if (
        body.googleId !== undefined &&
        (typeof body.googleId !== 'string' || body.googleId.trim() !== session.sub)
      ) {
        return jsonResponse({ success: false, error: 'Forbidden: googleId mismatch' }, 403);
      }

      const googleId = session.sub;
      const saveData = typeof body.saveData === 'string' ? body.saveData : '';
      if (saveData.trim().length === 0) {
        return jsonResponse({ success: false, error: 'Thiếu hoặc sai định dạng saveData' }, 400);
      }

      if (utf8Encoder.encode(saveData).byteLength > MAX_SAVE_DATA_BYTES) {
        return jsonResponse(
          { success: false, error: 'saveData vượt quá giới hạn 512000 bytes' },
          400
        );
      }

      try {
        JSON.parse(saveData);
      } catch {
        return jsonResponse({ success: false, error: 'saveData phải là chuỗi JSON hợp lệ' }, 400);
      }

      const updated = await updatePlayerSaveData(env, googleId, saveData, now, memoryStore);
      if (updated) {
        return jsonResponse({
          success: true,
          lastSyncAt: now,
        });
      }

      return jsonResponse({ success: false, error: 'Không tìm thấy hồ sơ người chơi' }, 404);
    }

    // 8. GET /api/player/cloud-load - Tải tiến độ từ Cloud (Yêu cầu Bearer Session JWT)
    if (request.method === 'GET' && pathname === '/api/player/cloud-load') {
      const secretError = getSessionSecretError(env.SESSION_SECRET);
      if (secretError) {
        return jsonResponse({ success: false, error: secretError }, 503);
      }

      const bearerToken = extractBearerToken(request);
      if (!bearerToken) {
        return jsonResponse({ success: false, error: 'Unauthorized: missing Bearer token' }, 401);
      }

      const session = await verifySessionToken(bearerToken, env.SESSION_SECRET!, now);
      if (!session) {
        return jsonResponse({ success: false, error: 'Unauthorized: invalid or expired session' }, 401);
      }

      const requestedGoogleId = url.searchParams.get('googleId');
      if (requestedGoogleId !== null && requestedGoogleId.trim() !== session.sub) {
        return jsonResponse({ success: false, error: 'Forbidden: googleId mismatch' }, 403);
      }

      const profile = await getPlayerProfile(env, session.sub, memoryStore);
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

    // 9. POST /api/boss/reset - Admin Reset Boss (Fail-Closed & Header-Only X-Admin-Key)
    if (request.method === 'POST' && pathname === '/api/boss/reset') {
      if (!env.ADMIN_API_KEY || env.ADMIN_API_KEY.trim().length === 0) {
        return jsonResponse(
          { success: false, error: 'Admin endpoint disabled: ADMIN_API_KEY is not configured' },
          503
        );
      }

      const adminKey = request.headers.get('X-Admin-Key');
      if (!adminKey || !(await constantTimeEqual(adminKey, env.ADMIN_API_KEY))) {
        return jsonResponse({ success: false, error: 'Unauthorized' }, 401);
      }

      const rawQueryVaultId = url.searchParams.get('vaultId');
      let vaultId: number | null;
      if (rawQueryVaultId !== null) {
        vaultId = parseStrictVaultId(rawQueryVaultId);
      } else {
        const parsedBody = await readOptionalJsonBodyObject(request);
        if (!parsedBody.ok) {
          return jsonResponse({ success: false, error: 'Invalid JSON request body' }, 400);
        }
        vaultId =
          parsedBody.body && parsedBody.body.vaultId !== undefined
            ? parseStrictVaultId(parsedBody.body.vaultId)
            : 1;
      }

      if (vaultId === null) {
        return jsonResponse(
          { success: false, error: 'vaultId không hợp lệ (chỉ chấp nhận số nguyên 1..9)' },
          400
        );
      }

      const state = await resetBossState(env, vaultId, now, memoryStore);

      return jsonResponse({
        success: true,
        vaultId,
        message: `Đã reset trạng thái Tầng ${vaultId} (${state.name}) về ban đầu!`,
        state: formatBossStateResponse(state, now),
        serverTime: now,
      });
    }

    return jsonResponse({ success: false, error: 'Endpoint Not Found' }, 404);
  } catch (err: unknown) {
    const errorMsg = err instanceof Error ? err.message : String(err);
    return jsonResponse({ success: false, error: errorMsg }, 500);
  }
}

export default {
  fetch(request: Request, env: Env): Promise<Response> {
    return handleRequest(request, env);
  },
};

// ==============================================================================
// DATABASE ACCESS ADAPTER (D1 -> Memory Fallback when DB binding omitted)
// ==============================================================================

async function getBossState(
  env: Env,
  vaultId: number,
  now: number,
  memoryStore: MemoryStore
): Promise<BossStateRecord> {
  const config = VAULT_CONFIGS[vaultId];
  if (!config) {
    throw new Error(`Invalid vaultId: ${vaultId}`);
  }

  if (env.DB) {
    let row = await env.DB.prepare('SELECT * FROM boss_state WHERE vault_id = ?')
      .bind(vaultId)
      .first<BossStateRecord>();

    if (!row) {
      const initial = createCanonicalBossState(vaultId, now);
      await env.DB.prepare(
        `
        INSERT OR IGNORE INTO boss_state (
          vault_id, name, current_hp, max_hp, current_armor, max_armor,
          server_furnace_heat, server_anvil_hp, shatter_until, last_strike_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
      `
      )
        .bind(
          initial.vault_id,
          initial.name,
          initial.current_hp,
          initial.max_hp,
          initial.current_armor,
          initial.max_armor,
          initial.server_furnace_heat,
          initial.server_anvil_hp,
          initial.shatter_until,
          initial.last_strike_at,
          initial.updated_at
        )
        .run();

      row = await env.DB.prepare('SELECT * FROM boss_state WHERE vault_id = ?')
        .bind(vaultId)
        .first<BossStateRecord>();
      if (!row) {
        return initial;
      }
    }

    const { state, changed } = reconcileBossStateRow(row, config, now);
    if (changed) {
      await env.DB.prepare(
        `
        UPDATE boss_state
        SET
          name = ?,
          current_hp = ?,
          max_hp = ?,
          current_armor = ?,
          max_armor = ?,
          server_furnace_heat = ?,
          server_anvil_hp = ?,
          shatter_until = ?,
          updated_at = ?
        WHERE vault_id = ?
      `
      )
        .bind(
          state.name,
          state.current_hp,
          state.max_hp,
          state.current_armor,
          state.max_armor,
          state.server_furnace_heat,
          state.server_anvil_hp,
          state.shatter_until,
          state.updated_at,
          vaultId
        )
        .run();
    }

    return state;
  }

  if (!memoryStore.bossState[vaultId]) {
    memoryStore.bossState[vaultId] = createCanonicalBossState(vaultId, now);
    return { ...memoryStore.bossState[vaultId] };
  }

  const { state, changed } = reconcileBossStateRow(memoryStore.bossState[vaultId], config, now);
  if (changed) {
    memoryStore.bossState[vaultId] = state;
  }
  return { ...state };
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
  },
  now: number,
  memoryStore: MemoryStore
): Promise<BossStateRecord> {
  const config = VAULT_CONFIGS[strike.vaultId];
  if (!config) {
    throw new Error(`Invalid vaultId: ${strike.vaultId}`);
  }

  // Ensures floor exists, matches canonical VAULT_CONFIGS, and expired shatter is restored first.
  const currentState = await getBossState(env, strike.vaultId, now, memoryStore);

  if (env.DB) {
    await env.DB.prepare(
      `
      UPDATE boss_state
      SET
        current_hp = MAX(0, current_hp - ?),
        current_armor = CASE
          WHEN current_armor <= 0 AND shatter_until <= ? THEN MAX(0, max_armor - ?)
          ELSE MAX(0, current_armor - ?)
        END,
        shatter_until = CASE
          WHEN current_armor <= 0 AND shatter_until <= ? THEN
            CASE WHEN max_armor - ? <= 0 THEN ? + ? ELSE 0 END
          WHEN MAX(0, current_armor - ?) <= 0 AND shatter_until <= ? THEN ? + ?
          ELSE shatter_until
        END,
        server_furnace_heat = MAX(0, MIN(?, server_furnace_heat + ?)),
        server_anvil_hp = MIN(?, MAX(0, server_anvil_hp + ?)),
        last_strike_at = ?,
        updated_at = ?
      WHERE vault_id = ?
    `
    )
      .bind(
        strike.damage,
        now,
        strike.shatterPoints,
        strike.shatterPoints,
        now,
        strike.shatterPoints,
        now,
        SHIELD_BREAK_DURATION_MS,
        strike.shatterPoints,
        now,
        now,
        SHIELD_BREAK_DURATION_MS,
        MAX_SERVER_FURNACE_HEAT,
        strike.furnaceCooling,
        DEFAULT_SERVER_ANVIL_HP,
        strike.anvilRepair,
        now,
        now,
        strike.vaultId
      )
      .run();

    if (strike.playerId && (strike.damage > 0 || strike.raidContribution > 0)) {
      await env.DB.prepare(
        `
        INSERT INTO leaderboard (player_id, player_name, total_damage, raid_score, last_hit_at)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(player_id) DO UPDATE SET
          total_damage = total_damage + excluded.total_damage,
          raid_score = raid_score + excluded.raid_score,
          player_name = excluded.player_name,
          last_hit_at = excluded.last_hit_at
      `
      )
        .bind(strike.playerId, strike.playerName, strike.damage, strike.raidContribution, now)
        .run();
    }

    const updatedRow = await env.DB.prepare('SELECT * FROM boss_state WHERE vault_id = ?')
      .bind(strike.vaultId)
      .first<BossStateRecord>();

    if (updatedRow) {
      return reconcileBossStateRow(updatedRow, config, now).state;
    }
    return currentState;
  }

  const state = memoryStore.bossState[strike.vaultId];
  state.current_hp = Math.max(0, state.current_hp - strike.damage);
  state.current_armor = Math.max(0, state.current_armor - strike.shatterPoints);
  if (state.current_armor <= 0 && state.shatter_until <= now) {
    state.shatter_until = now + SHIELD_BREAK_DURATION_MS;
  }
  state.server_furnace_heat = Math.max(
    0,
    Math.min(MAX_SERVER_FURNACE_HEAT, state.server_furnace_heat + strike.furnaceCooling)
  );
  state.server_anvil_hp = Math.max(
    0,
    Math.min(DEFAULT_SERVER_ANVIL_HP, state.server_anvil_hp + strike.anvilRepair)
  );
  state.last_strike_at = now;
  state.updated_at = now;

  if (strike.playerId && (strike.damage > 0 || strike.raidContribution > 0)) {
    const existing = memoryStore.leaderboard.get(strike.playerId) || {
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
    memoryStore.leaderboard.set(strike.playerId, existing);
  }

  return { ...state };
}

async function getLeaderboard(
  env: Env,
  limit: number,
  memoryStore: MemoryStore
): Promise<LeaderboardRecord[]> {
  if (env.DB) {
    const { results } = await env.DB.prepare(
      `
      SELECT player_id, player_name, guild_id, total_damage, raid_score, last_hit_at
      FROM leaderboard
      ORDER BY total_damage DESC
      LIMIT ?
    `
    )
      .bind(limit)
      .all<LeaderboardRecord>();
    return results || [];
  }

  return Array.from(memoryStore.leaderboard.values())
    .sort((a, b) => b.total_damage - a.total_damage)
    .slice(0, limit);
}

async function getContributorCount(env: Env, memoryStore: MemoryStore): Promise<number> {
  if (env.DB) {
    try {
      const res = await env.DB.prepare('SELECT COUNT(*) as count FROM leaderboard').first<{
        count: number;
      }>();
      return res?.count || 1;
    } catch {
      return 1;
    }
  }
  return Math.max(1, memoryStore.leaderboard.size);
}

async function resetBossState(
  env: Env,
  vaultId: number,
  now: number,
  memoryStore: MemoryStore
): Promise<BossStateRecord> {
  const canonical = createCanonicalBossState(vaultId, now);

  if (env.DB) {
    await env.DB.prepare(
      `
      INSERT INTO boss_state (
        vault_id, name, current_hp, max_hp, current_armor, max_armor,
        server_furnace_heat, server_anvil_hp, shatter_until, last_strike_at, updated_at
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
      ON CONFLICT(vault_id) DO UPDATE SET
        name = excluded.name,
        current_hp = excluded.current_hp,
        max_hp = excluded.max_hp,
        current_armor = excluded.current_armor,
        max_armor = excluded.max_armor,
        server_furnace_heat = excluded.server_furnace_heat,
        server_anvil_hp = excluded.server_anvil_hp,
        shatter_until = excluded.shatter_until,
        last_strike_at = excluded.last_strike_at,
        updated_at = excluded.updated_at
    `
    )
      .bind(
        canonical.vault_id,
        canonical.name,
        canonical.current_hp,
        canonical.max_hp,
        canonical.current_armor,
        canonical.max_armor,
        canonical.server_furnace_heat,
        canonical.server_anvil_hp,
        canonical.shatter_until,
        canonical.last_strike_at,
        canonical.updated_at
      )
      .run();
    return canonical;
  }

  memoryStore.bossState[vaultId] = canonical;
  return { ...canonical };
}

// ==============================================================================
// PLAYER PROFILE & CLOUD SAVE D1 ADAPTER
// ==============================================================================

async function getPlayerProfile(
  env: Env,
  googleId: string,
  memoryStore: MemoryStore
): Promise<PlayerProfileRecord | null> {
  if (env.DB) {
    const row = await env.DB.prepare(
      'SELECT google_id, email, display_name, avatar_url, save_data, last_sync_at, created_at FROM player_profiles WHERE google_id = ?'
    )
      .bind(googleId)
      .first<PlayerProfileRecord>();
    return row ?? null;
  }
  return memoryStore.profiles.get(googleId) || null;
}

async function upsertPlayerProfile(
  env: Env,
  profile: PlayerProfileRecord,
  memoryStore: MemoryStore
): Promise<void> {
  if (env.DB) {
    await env.DB.prepare(
      `
      INSERT INTO player_profiles (google_id, email, display_name, avatar_url, save_data, last_sync_at, created_at)
      VALUES (?, ?, ?, ?, ?, ?, ?)
      ON CONFLICT(google_id) DO UPDATE SET
        display_name = excluded.display_name,
        avatar_url = excluded.avatar_url,
        save_data = excluded.save_data,
        last_sync_at = excluded.last_sync_at
    `
    )
      .bind(
        profile.google_id,
        profile.email,
        profile.display_name,
        profile.avatar_url,
        profile.save_data,
        profile.last_sync_at,
        profile.created_at
      )
      .run();
    return;
  }
  memoryStore.profiles.set(profile.google_id, profile);
}

async function updatePlayerSaveData(
  env: Env,
  googleId: string,
  saveData: string,
  syncTime: number,
  memoryStore: MemoryStore
): Promise<boolean> {
  if (env.DB) {
    const res = await env.DB.prepare(
      'UPDATE player_profiles SET save_data = ?, last_sync_at = ? WHERE google_id = ?'
    )
      .bind(saveData, syncTime, googleId)
      .run();
    return (res.meta?.changes ?? 0) > 0;
  }

  const existing = memoryStore.profiles.get(googleId);
  if (existing) {
    existing.save_data = saveData;
    existing.last_sync_at = syncTime;
    return true;
  }
  return false;
}
