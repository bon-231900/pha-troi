import { describe, it } from 'node:test';
import assert from 'node:assert/strict';

import {
  createApp,
  createMemoryStore,
  type Env,
  type LeaderboardRecord,
  type PlayerProfileRecord,
} from './index.ts';
import {
  EXPECTED_GOOGLE_CLIENT_ID,
  GOOGLE_JWKS_URL,
  GOOGLE_TOKENINFO_URL,
  GOOGLE_USERINFO_URL,
  SESSION_TTL_SEC,
  base64UrlEncode,
  signSessionToken,
} from './auth.ts';
import {
  DEFAULT_SERVER_ANVIL_HP,
  MAX_SERVER_FURNACE_HEAT,
  SHIELD_BREAK_DURATION_MS,
  VAULT_CONFIGS,
  type BossStateRecord,
} from './vaults.ts';

const TEST_SESSION_SECRET = 'phatroi-test-session-secret-32chars!';
const TEST_ADMIN_KEY = 'phatroi-test-admin-secret-key';
const BASE_NOW_MS = 1_700_000_000_000;
const textEncoder = new TextEncoder();

interface ExpectedVaultSpec {
  vaultId: number;
  name: string;
  maxHp: number;
  maxArmor: number;
}

const CANONICAL_CELESTIAL_VAULTS: ExpectedVaultSpec[] = [
  { vaultId: 1, name: 'Thiết Vân Vòm', maxHp: 1_500_000_000, maxArmor: 500 },
  { vaultId: 2, name: 'Cổ Đồng Thiên', maxHp: 4_500_000_000, maxArmor: 1000 },
  { vaultId: 3, name: 'Lôi Tiêu Điện', maxHp: 12_000_000_000, maxArmor: 1800 },
  { vaultId: 4, name: 'Hàn Băng Thần', maxHp: 30_000_000_000, maxArmor: 2800 },
  { vaultId: 5, name: 'Xích Diễm Giới', maxHp: 75_000_000_000, maxArmor: 4200 },
  { vaultId: 6, name: 'Huyền Thủy Hải', maxHp: 180_000_000_000, maxArmor: 6000 },
  { vaultId: 7, name: 'Bát Quái Phong', maxHp: 420_000_000_000, maxArmor: 8500 },
  { vaultId: 8, name: 'Hư Không Đoạn', maxHp: 950_000_000_000, maxArmor: 12000 },
  { vaultId: 9, name: 'Hỗn Độn Thiên', maxHp: 2_500_000_000_000, maxArmor: 18000 },
];

interface MockD1Options {
  seedBossStates?: BossStateRecord[];
  seedProfiles?: PlayerProfileRecord[];
  forcedSaveUpdateChanges?: number;
}

interface MockD1Handle {
  db: D1Database;
  bossStates: Map<number, BossStateRecord>;
  leaderboard: Map<string, LeaderboardRecord>;
  profiles: Map<string, PlayerProfileRecord>;
  setForcedSaveUpdateChanges: (changes: number | undefined) => void;
}

/**
 * Pure TypeScript D1Database test double supporting every SQL statement issued by index.ts.
 */
function createMockD1(options: MockD1Options = {}): MockD1Handle {
  const bossStates = new Map<number, BossStateRecord>();
  const leaderboard = new Map<string, LeaderboardRecord>();
  const profiles = new Map<string, PlayerProfileRecord>();
  let forcedSaveUpdateChanges = options.forcedSaveUpdateChanges;

  for (const row of options.seedBossStates ?? []) {
    bossStates.set(row.vault_id, { ...row });
  }
  for (const profile of options.seedProfiles ?? []) {
    profiles.set(profile.google_id, { ...profile });
  }

  const normalizeSql = (sql: string) => sql.replace(/\s+/g, ' ').trim();

  const makeMeta = (changes: number, rowsRead: number = 0): D1Meta & Record<string, unknown> => ({
    duration: 0,
    size_after: 0,
    rows_read: rowsRead,
    rows_written: changes,
    last_row_id: 0,
    changed_db: changes > 0,
    changes,
  });

  const makeResult = <T>(results: T[], changes: number, rowsRead: number = results.length): D1Result<T> => ({
    success: true,
    results,
    meta: makeMeta(changes, rowsRead),
  });

  const executeQuery = (sql: string, bound: unknown[]) => {
    const q = normalizeSql(sql);

    if (q === 'SELECT * FROM boss_state WHERE vault_id = ?') {
      const vaultId = Number(bound[0]);
      const row = bossStates.get(vaultId);
      return { rows: row ? [{ ...row }] : [], changes: 0 };
    }

    if (q.startsWith('INSERT OR IGNORE INTO boss_state')) {
      const vaultId = Number(bound[0]);
      if (!bossStates.has(vaultId)) {
        bossStates.set(vaultId, {
          vault_id: vaultId,
          name: String(bound[1]),
          current_hp: Number(bound[2]),
          max_hp: Number(bound[3]),
          current_armor: Number(bound[4]),
          max_armor: Number(bound[5]),
          server_furnace_heat: Number(bound[6]),
          server_anvil_hp: Number(bound[7]),
          shatter_until: Number(bound[8]),
          last_strike_at: Number(bound[9]),
          updated_at: Number(bound[10]),
        });
        return { rows: [], changes: 1 };
      }
      return { rows: [], changes: 0 };
    }

    if (q.startsWith('UPDATE boss_state SET name = ?,')) {
      const vaultId = Number(bound[9]);
      const row = bossStates.get(vaultId);
      if (!row) return { rows: [], changes: 0 };
      bossStates.set(vaultId, {
        ...row,
        name: String(bound[0]),
        current_hp: Number(bound[1]),
        max_hp: Number(bound[2]),
        current_armor: Number(bound[3]),
        max_armor: Number(bound[4]),
        server_furnace_heat: Number(bound[5]),
        server_anvil_hp: Number(bound[6]),
        shatter_until: Number(bound[7]),
        updated_at: Number(bound[8]),
      });
      return { rows: [], changes: 1 };
    }

    if (q.startsWith('UPDATE boss_state SET current_hp = MAX(0, current_hp - ?),')) {
      const damage = Number(bound[0]);
      const now = Number(bound[1]);
      const shatterPoints = Number(bound[2]);
      const shatterDurationMs = Number(bound[7]);
      const maxHeat = Number(bound[12]);
      const furnaceCooling = Number(bound[13]);
      const defaultAnvilHp = Number(bound[14]);
      const anvilRepair = Number(bound[15]);
      const vaultId = Number(bound[18]);

      const row = bossStates.get(vaultId);
      if (!row) return { rows: [], changes: 0 };

      const wasExpired = row.current_armor <= 0 && row.shatter_until <= now;
      const nextHp = Math.max(0, row.current_hp - damage);
      const nextArmor = wasExpired
        ? Math.max(0, row.max_armor - shatterPoints)
        : Math.max(0, row.current_armor - shatterPoints);

      let nextShatterUntil = row.shatter_until;
      if (wasExpired) {
        nextShatterUntil = row.max_armor - shatterPoints <= 0 ? now + shatterDurationMs : 0;
      } else if (nextArmor <= 0 && row.shatter_until <= now) {
        nextShatterUntil = now + shatterDurationMs;
      }

      const nextHeat = Math.max(0, Math.min(maxHeat, row.server_furnace_heat + furnaceCooling));
      const nextAnvil = Math.min(defaultAnvilHp, Math.max(0, row.server_anvil_hp + anvilRepair));

      bossStates.set(vaultId, {
        ...row,
        current_hp: nextHp,
        current_armor: nextArmor,
        shatter_until: nextShatterUntil,
        server_furnace_heat: nextHeat,
        server_anvil_hp: nextAnvil,
        last_strike_at: now,
        updated_at: now,
      });
      return { rows: [], changes: 1 };
    }

    if (q.startsWith('INSERT INTO boss_state')) {
      const vaultId = Number(bound[0]);
      bossStates.set(vaultId, {
        vault_id: vaultId,
        name: String(bound[1]),
        current_hp: Number(bound[2]),
        max_hp: Number(bound[3]),
        current_armor: Number(bound[4]),
        max_armor: Number(bound[5]),
        server_furnace_heat: Number(bound[6]),
        server_anvil_hp: Number(bound[7]),
        shatter_until: Number(bound[8]),
        last_strike_at: Number(bound[9]),
        updated_at: Number(bound[10]),
      });
      return { rows: [], changes: 1 };
    }

    if (q.startsWith('INSERT INTO leaderboard')) {
      const playerId = String(bound[0]);
      const playerName = String(bound[1]);
      const damage = Number(bound[2]);
      const raidScore = Number(bound[3]);
      const lastHitAt = Number(bound[4]);
      const existing = leaderboard.get(playerId);
      if (existing) {
        existing.total_damage += damage;
        existing.raid_score += raidScore;
        existing.player_name = playerName;
        existing.last_hit_at = lastHitAt;
      } else {
        leaderboard.set(playerId, {
          player_id: playerId,
          player_name: playerName,
          guild_id: 'Vạn Dân',
          total_damage: damage,
          raid_score: raidScore,
          last_hit_at: lastHitAt,
        });
      }
      return { rows: [], changes: 1 };
    }

    if (q.startsWith('SELECT player_id, player_name, guild_id, total_damage, raid_score, last_hit_at FROM leaderboard')) {
      const limit = Number(bound[0]);
      const rows = Array.from(leaderboard.values())
        .sort((a, b) => b.total_damage - a.total_damage)
        .slice(0, limit)
        .map((r) => ({ ...r }));
      return { rows, changes: 0 };
    }

    if (q === 'SELECT COUNT(*) as count FROM leaderboard') {
      return { rows: [{ count: leaderboard.size }], changes: 0 };
    }

    if (q.startsWith('SELECT google_id, email, display_name, avatar_url, save_data, last_sync_at, created_at FROM player_profiles')) {
      const googleId = String(bound[0]);
      const profile = profiles.get(googleId);
      return { rows: profile ? [{ ...profile }] : [], changes: 0 };
    }

    if (q.startsWith('INSERT INTO player_profiles')) {
      const googleId = String(bound[0]);
      const existing = profiles.get(googleId);
      if (existing) {
        existing.display_name = String(bound[2]);
        existing.avatar_url = String(bound[3]);
        existing.save_data = String(bound[4]);
        existing.last_sync_at = Number(bound[5]);
      } else {
        profiles.set(googleId, {
          google_id: googleId,
          email: String(bound[1]),
          display_name: String(bound[2]),
          avatar_url: String(bound[3]),
          save_data: String(bound[4]),
          last_sync_at: Number(bound[5]),
          created_at: Number(bound[6]),
        });
      }
      return { rows: [], changes: 1 };
    }

    if (q === 'UPDATE player_profiles SET save_data = ?, last_sync_at = ? WHERE google_id = ?') {
      if (forcedSaveUpdateChanges !== undefined) {
        return { rows: [], changes: forcedSaveUpdateChanges };
      }
      const saveData = String(bound[0]);
      const lastSyncAt = Number(bound[1]);
      const googleId = String(bound[2]);
      const existing = profiles.get(googleId);
      if (!existing) {
        return { rows: [], changes: 0 };
      }
      existing.save_data = saveData;
      existing.last_sync_at = lastSyncAt;
      return { rows: [], changes: 1 };
    }

    throw new Error(`Unexpected SQL in MockD1: ${q}`);
  };

  const makeStatement = (sql: string, bound: unknown[] = []): D1PreparedStatement => ({
    bind(...values: unknown[]) {
      return makeStatement(sql, values);
    },
    async first<T = unknown>(colName?: string): Promise<T | null> {
      const { rows } = executeQuery(sql, bound);
      const firstRow = rows[0] as Record<string, unknown> | undefined;
      if (!firstRow) return null;
      if (colName !== undefined) {
        return (firstRow[colName] as T) ?? null;
      }
      return firstRow as T;
    },
    async run<T = Record<string, unknown>>(): Promise<D1Result<T>> {
      const { rows, changes } = executeQuery(sql, bound);
      return makeResult(rows as T[], changes, 0);
    },
    async all<T = Record<string, unknown>>(): Promise<D1Result<T>> {
      const { rows } = executeQuery(sql, bound);
      return makeResult(rows as T[], 0, rows.length);
    },
    async raw<T = unknown[]>(options?: { columnNames?: boolean }): Promise<any> {
      const { rows } = executeQuery(sql, bound);
      if (options?.columnNames) {
        const columns = rows[0] ? Object.keys(rows[0] as Record<string, unknown>) : [];
        return [columns, ...(rows as T[])];
      }
      return rows as T[];
    },
  }) as D1PreparedStatement;

  const db: D1Database = {
    prepare(query: string) {
      return makeStatement(query);
    },
    withSession(): D1DatabaseSession {
      return {
        prepare: (query: string) => makeStatement(query),
        batch: <T = unknown>(statements: D1PreparedStatement[]) => db.batch<T>(statements),
        getBookmark: () => null,
      };
    },
    async dump(): Promise<ArrayBuffer> {
      return new ArrayBuffer(0);
    },
    async batch<T = unknown>(statements: D1PreparedStatement[]): Promise<D1Result<T>[]> {
      const results: D1Result<T>[] = [];
      for (const stmt of statements) {
        results.push(await stmt.run<T>());
      }
      return results;
    },
    async exec(): Promise<D1ExecResult> {
      return { count: 0, duration: 0 };
    },
  };

  return {
    db,
    bossStates,
    leaderboard,
    profiles,
    setForcedSaveUpdateChanges(changes: number | undefined) {
      forcedSaveUpdateChanges = changes;
    },
  };
}

interface TestRsaKeyPair {
  kid: string;
  privateKey: CryptoKey;
  publicJwk: JsonWebKey & { kid: string; use: string; alg: string };
}

async function generateRsaKeyPair(kid: string): Promise<TestRsaKeyPair> {
  const keyPair = (await crypto.subtle.generateKey(
    {
      name: 'RSASSA-PKCS1-v1_5',
      modulusLength: 2048,
      publicExponent: new Uint8Array([1, 0, 1]),
      hash: 'SHA-256',
    },
    true,
    ['sign', 'verify']
  )) as CryptoKeyPair;

  const exported = (await crypto.subtle.exportKey('jwk', keyPair.publicKey)) as JsonWebKey & {
    kid?: string;
    use?: string;
    alg?: string;
  };

  return {
    kid,
    privateKey: keyPair.privateKey,
    publicJwk: {
      ...exported,
      kid,
      use: 'sig',
      alg: 'RS256',
    },
  };
}

function encodeJwtPart(obj: Record<string, unknown>): string {
  return base64UrlEncode(textEncoder.encode(JSON.stringify(obj)));
}

async function signRs256Jwt(
  header: Record<string, unknown>,
  payload: Record<string, unknown>,
  privateKey: CryptoKey
): Promise<string> {
  const signingInput = `${encodeJwtPart(header)}.${encodeJwtPart(payload)}`;
  const signature = await crypto.subtle.sign(
    'RSASSA-PKCS1-v1_5',
    privateKey,
    textEncoder.encode(signingInput)
  );
  return `${signingInput}.${base64UrlEncode(new Uint8Array(signature))}`;
}

async function signHs256Jwt(
  header: Record<string, unknown>,
  payload: Record<string, unknown>,
  secret: string
): Promise<string> {
  const signingInput = `${encodeJwtPart(header)}.${encodeJwtPart(payload)}`;
  const key = await crypto.subtle.importKey(
    'raw',
    textEncoder.encode(secret),
    { name: 'HMAC', hash: 'SHA-256' },
    false,
    ['sign']
  );
  const signature = await crypto.subtle.sign('HMAC', key, textEncoder.encode(signingInput));
  return `${signingInput}.${base64UrlEncode(new Uint8Array(signature))}`;
}

function createUnsignedJwt(
  header: Record<string, unknown>,
  payload: Record<string, unknown>,
  signaturePart: string = ''
): string {
  return `${encodeJwtPart(header)}.${encodeJwtPart(payload)}.${signaturePart}`;
}

function getRequestUrl(input: RequestInfo | URL): string {
  if (typeof input === 'string') return input;
  if (input instanceof URL) return input.toString();
  return input.url;
}

function createJwksFetchMock(keysProvider: () => Array<JsonWebKey & { kid?: string }>) {
  let jwksCalls = 0;
  const fetchFn: typeof fetch = async (input) => {
    const url = getRequestUrl(input);
    if (url === GOOGLE_JWKS_URL) {
      jwksCalls += 1;
      return new Response(JSON.stringify({ keys: keysProvider() }), {
        status: 200,
        headers: {
          'Content-Type': 'application/json',
          'Cache-Control': 'public, max-age=300',
        },
      });
    }
    return new Response('Not Found', { status: 404 });
  };
  return {
    fetchFn,
    getJwksCalls: () => jwksCalls,
  };
}

function postJson(path: string, body: unknown, headers: Record<string, string> = {}): Request {
  return new Request(`https://phatroi.com${path}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...headers,
    },
    body: typeof body === 'string' ? body : JSON.stringify(body),
  });
}

async function readJson<T = Record<string, unknown>>(res: Response): Promise<T> {
  return (await res.json()) as T;
}

// ==============================================================================
// 1. GOOGLE ID TOKEN (JWKS RS256) VERIFICATION ON POST /api/auth/google
// ==============================================================================

describe('1. Google ID Token (JWKS RS256) verification on POST /api/auth/google', () => {
  it('accepts valid RS256 ID token and returns 200, 3-part sessionToken, and profile', async () => {
    const { db } = createMockD1();
    const primaryKey = await generateRsaKeyPair('rsa-kid-primary');
    const nowSec = Math.floor(BASE_NOW_MS / 1000);
    const { fetchFn, getJwksCalls } = createJwksFetchMock(() => [primaryKey.publicJwk]);

    const app = createApp({ fetch: fetchFn, now: () => BASE_NOW_MS });
    const env: Env = { DB: db, SESSION_SECRET: TEST_SESSION_SECRET };

    const validToken = await signRs256Jwt(
      { alg: 'RS256', kid: primaryKey.kid, typ: 'JWT' },
      {
        iss: 'https://accounts.google.com',
        aud: EXPECTED_GOOGLE_CLIENT_ID,
        sub: 'google-sub-001',
        email: 'thoren01@phatroi.com',
        email_verified: true,
        name: 'Lôi Thần Chùy',
        picture: 'https://phatroi.com/avatar1.png',
        iat: nowSec,
        exp: nowSec + 3600,
      },
      primaryKey.privateKey
    );

    const res = await app.fetch(postJson('/api/auth/google', { credential: validToken }), env);
    assert.equal(res.status, 200);
    assert.equal(getJwksCalls(), 1);

    const data = await readJson<{
      success: boolean;
      isNew: boolean;
      sessionToken: string;
      sessionExpiresAt: number;
      saveData: string;
      profile: { googleId: string; email: string; name: string; avatar: string };
    }>(res);

    assert.equal(data.success, true);
    assert.equal(data.isNew, true);
    assert.equal(data.saveData, '{}');
    assert.equal(data.sessionExpiresAt, (nowSec + SESSION_TTL_SEC) * 1000);
    assert.deepEqual(data.profile, {
      googleId: 'google-sub-001',
      email: 'thoren01@phatroi.com',
      name: 'Lôi Thần Chùy',
      avatar: 'https://phatroi.com/avatar1.png',
    });

    const jwtParts = data.sessionToken.split('.');
    assert.equal(jwtParts.length, 3);
    assert.ok(jwtParts.every((part) => part.length > 0));
  });

  it('rejects tampered payload and wrong RSA signature with 401', async () => {
    const { db } = createMockD1();
    const trustedKey = await generateRsaKeyPair('kid-trusted');
    const attackerKey = await generateRsaKeyPair('kid-trusted');
    const nowSec = Math.floor(BASE_NOW_MS / 1000);
    const { fetchFn } = createJwksFetchMock(() => [trustedKey.publicJwk]);

    const app = createApp({ fetch: fetchFn, now: () => BASE_NOW_MS });
    const env: Env = { DB: db, SESSION_SECRET: TEST_SESSION_SECRET };

    const legitimateClaims = {
      iss: 'https://accounts.google.com',
      aud: EXPECTED_GOOGLE_CLIENT_ID,
      sub: 'user-honest',
      email: 'honest@phatroi.com',
      email_verified: true,
      exp: nowSec + 3600,
    };

    const validJwt = await signRs256Jwt(
      { alg: 'RS256', kid: 'kid-trusted', typ: 'JWT' },
      legitimateClaims,
      trustedKey.privateKey
    );
    const [headerB64, , sigB64] = validJwt.split('.');
    const tamperedPayloadB64 = encodeJwtPart({ ...legitimateClaims, sub: 'user-victim' });
    const tamperedJwt = `${headerB64}.${tamperedPayloadB64}.${sigB64}`;

    const wrongSignatureJwt = await signRs256Jwt(
      { alg: 'RS256', kid: 'kid-trusted', typ: 'JWT' },
      legitimateClaims,
      attackerKey.privateKey
    );

    for (const badToken of [tamperedJwt, wrongSignatureJwt]) {
      const res = await app.fetch(postJson('/api/auth/google', { credential: badToken }), env);
      assert.equal(res.status, 401);
      const body = await readJson(res);
      assert.equal(body.success, false);
    }
  });

  it('rejects alg=none and alg=HS256 JWT confusion attacks with 401', async () => {
    const { db } = createMockD1();
    const rsaKey = await generateRsaKeyPair('kid-rsa');
    const nowSec = Math.floor(BASE_NOW_MS / 1000);
    const { fetchFn } = createJwksFetchMock(() => [rsaKey.publicJwk]);

    const app = createApp({ fetch: fetchFn, now: () => BASE_NOW_MS });
    const env: Env = { DB: db, SESSION_SECRET: TEST_SESSION_SECRET };

    const claims = {
      iss: 'https://accounts.google.com',
      aud: EXPECTED_GOOGLE_CLIENT_ID,
      sub: 'attacker-sub',
      email: 'attacker@phatroi.com',
      email_verified: true,
      exp: nowSec + 3600,
    };

    const algNoneEmptySig = createUnsignedJwt({ alg: 'none', kid: rsaKey.kid }, claims, '');
    const algNoneWithSig = createUnsignedJwt({ alg: 'none', kid: rsaKey.kid }, claims, 'fakesig');
    const algHs256Unsigned = createUnsignedJwt({ alg: 'HS256', kid: rsaKey.kid }, claims, 'fakesig');
    const algHs256KeyConfusion = await signHs256Jwt(
      { alg: 'HS256', kid: rsaKey.kid, typ: 'JWT' },
      claims,
      JSON.stringify(rsaKey.publicJwk)
    );

    for (const token of [algNoneEmptySig, algNoneWithSig, algHs256Unsigned, algHs256KeyConfusion]) {
      const res = await app.fetch(postJson('/api/auth/google', { credential: token }), env);
      assert.equal(res.status, 401);
    }
  });

  it('rejects wrong aud, wrong iss, expired exp, and email_verified=false with 401', async () => {
    const { db } = createMockD1();
    const rsaKey = await generateRsaKeyPair('kid-claims');
    const nowSec = Math.floor(BASE_NOW_MS / 1000);
    const { fetchFn } = createJwksFetchMock(() => [rsaKey.publicJwk]);

    const app = createApp({ fetch: fetchFn, now: () => BASE_NOW_MS });
    const env: Env = { DB: db, SESSION_SECRET: TEST_SESSION_SECRET };

    const baseClaims = {
      iss: 'https://accounts.google.com',
      aud: EXPECTED_GOOGLE_CLIENT_ID,
      sub: 'claim-user',
      email: 'claim@phatroi.com',
      email_verified: true,
      exp: nowSec + 3600,
    };

    const invalidClaimPayloads: Array<Record<string, unknown>> = [
      { ...baseClaims, aud: '123456-other-client.apps.googleusercontent.com' },
      { ...baseClaims, iss: 'https://evil.accounts.example.com' },
      { ...baseClaims, exp: nowSec - 60 },
      { ...baseClaims, email_verified: false },
      { ...baseClaims, email_verified: 'true' },
    ];

    for (const claims of invalidClaimPayloads) {
      const token = await signRs256Jwt(
        { alg: 'RS256', kid: rsaKey.kid, typ: 'JWT' },
        claims,
        rsaKey.privateKey
      );
      const res = await app.fetch(postJson('/api/auth/google', { credential: token }), env);
      assert.equal(res.status, 401);
    }
  });

  it('fails closed with 503 when SESSION_SECRET is missing or too short', async () => {
    const { db } = createMockD1();
    let fetchCalled = false;
    const app = createApp({
      now: () => BASE_NOW_MS,
      fetch: async () => {
        fetchCalled = true;
        return new Response('{}', { status: 200 });
      },
    });

    for (const secret of [undefined, '', '   ', 'short-secret-15']) {
      const res = await app.fetch(
        postJson('/api/auth/google', { credential: 'header.payload.signature' }),
        { DB: db, SESSION_SECRET: secret }
      );
      assert.equal(res.status, 503);
      const body = await readJson(res);
      assert.equal(body.success, false);
      assert.equal(body.error, 'Server authentication not configured: SESSION_SECRET missing');
    }

    assert.equal(fetchCalled, false);
  });
});

// ==============================================================================
// 2. GOOGLE ACCESS TOKEN (TOKENINFO + USERINFO) VERIFICATION ON POST /api/auth/google
// ==============================================================================

describe('2. Google Access Token (tokeninfo + userinfo) verification on POST /api/auth/google', () => {
  function createOAuthFetchMock() {
    let userInfoRequests = 0;
    const fetchFn: typeof fetch = async (input, init) => {
      const url = getRequestUrl(input);

      if (url.startsWith(GOOGLE_TOKENINFO_URL)) {
        const parsed = new URL(url);
        const token = parsed.searchParams.get('access_token');

        if (token === 'valid-aud-token') {
          return new Response(
            JSON.stringify({
              aud: EXPECTED_GOOGLE_CLIENT_ID,
              sub: 'oauth-user-aud',
              expires_in: '3600',
              email_verified: 'true',
            }),
            { status: 200 }
          );
        }

        if (token === 'valid-azp-token') {
          return new Response(
            JSON.stringify({
              azp: EXPECTED_GOOGLE_CLIENT_ID,
              sub: 'oauth-user-azp',
              expires_in: 1800,
              email_verified: true,
            }),
            { status: 200 }
          );
        }

        if (token === 'unverified-omitted-token') {
          return new Response(
            JSON.stringify({
              aud: EXPECTED_GOOGLE_CLIENT_ID,
              sub: 'oauth-user-unverified-omitted',
              expires_in: '3600',
            }),
            { status: 200 }
          );
        }

        if (token === 'unverified-false-token') {
          return new Response(
            JSON.stringify({
              aud: EXPECTED_GOOGLE_CLIENT_ID,
              sub: 'oauth-user-unverified-false',
              expires_in: '3600',
            }),
            { status: 200 }
          );
        }

        if (token === 'wrong-client-token') {
          return new Response(
            JSON.stringify({
              aud: '999999-foreign-app.apps.googleusercontent.com',
              azp: '999999-foreign-app.apps.googleusercontent.com',
              sub: 'oauth-user-foreign',
              expires_in: '3600',
              email_verified: 'true',
            }),
            { status: 200 }
          );
        }

        return new Response(JSON.stringify({ error_description: 'Invalid token' }), { status: 400 });
      }

      if (url === GOOGLE_USERINFO_URL) {
        userInfoRequests += 1;
        const headers = new Headers(init?.headers);
        const auth = headers.get('Authorization');

        if (auth === 'Bearer valid-aud-token') {
          return new Response(
            JSON.stringify({
              sub: 'oauth-user-aud',
              email: 'aud@phatroi.com',
              email_verified: true,
              name: 'Thợ Rèn AUD',
              picture: 'https://phatroi.com/aud.png',
            }),
            { status: 200 }
          );
        }

        if (auth === 'Bearer valid-azp-token') {
          return new Response(
            JSON.stringify({
              sub: 'oauth-user-azp',
              email: 'azp@phatroi.com',
              email_verified: 'true',
              name: 'Thợ Rèn AZP',
              picture: 'https://phatroi.com/azp.png',
            }),
            { status: 200 }
          );
        }

        if (auth === 'Bearer unverified-omitted-token') {
          return new Response(
            JSON.stringify({
              sub: 'oauth-user-unverified-omitted',
              email: 'unverified-omitted@phatroi.com',
              name: 'Chưa Xác Minh',
            }),
            { status: 200 }
          );
        }

        if (auth === 'Bearer unverified-false-token') {
          return new Response(
            JSON.stringify({
              sub: 'oauth-user-unverified-false',
              email: 'unverified-false@phatroi.com',
              email_verified: false,
              name: 'Từ Chối Email',
            }),
            { status: 200 }
          );
        }

        return new Response('Unauthorized', { status: 401 });
      }

      return new Response('Not Found', { status: 404 });
    };

    return {
      fetchFn,
      getUserInfoRequests: () => userInfoRequests,
    };
  }

  it('verifies valid accessToken where tokeninfo aud or azp matches EXPECTED_GOOGLE_CLIENT_ID', async () => {
    const { db } = createMockD1();
    const { fetchFn, getUserInfoRequests } = createOAuthFetchMock();
    const app = createApp({ fetch: fetchFn, now: () => BASE_NOW_MS });
    const env: Env = { DB: db, SESSION_SECRET: TEST_SESSION_SECRET };

    for (const [accessToken, expectedSub, expectedEmail] of [
      ['valid-aud-token', 'oauth-user-aud', 'aud@phatroi.com'],
      ['valid-azp-token', 'oauth-user-azp', 'azp@phatroi.com'],
    ] as const) {
      const res = await app.fetch(postJson('/api/auth/google', { accessToken }), env);
      assert.equal(res.status, 200);
      const data = await readJson<{
        success: boolean;
        sessionToken: string;
        profile: { googleId: string; email: string };
      }>(res);
      assert.equal(data.success, true);
      assert.equal(data.sessionToken.split('.').length, 3);
      assert.equal(data.profile.googleId, expectedSub);
      assert.equal(data.profile.email, expectedEmail);
    }

    assert.equal(getUserInfoRequests(), 2);
  });

  it('rejects accessToken whose tokeninfo aud/azp belongs to another client with 401', async () => {
    const { db } = createMockD1();
    const { fetchFn, getUserInfoRequests } = createOAuthFetchMock();
    const app = createApp({ fetch: fetchFn, now: () => BASE_NOW_MS });
    const env: Env = { DB: db, SESSION_SECRET: TEST_SESSION_SECRET };

    const wrongClientRes = await app.fetch(
      postJson('/api/auth/google', { accessToken: 'wrong-client-token' }),
      env
    );
    assert.equal(wrongClientRes.status, 401);
    assert.equal(getUserInfoRequests(), 0);

    const invalidTokenRes = await app.fetch(
      postJson('/api/auth/google', { accessToken: 'revoked-token' }),
      env
    );
    assert.equal(invalidTokenRes.status, 401);
    assert.equal(getUserInfoRequests(), 0);
  });

  it('rejects accessToken when email_verified is omitted everywhere or false with 401', async () => {
    const { db } = createMockD1();
    const { fetchFn, getUserInfoRequests } = createOAuthFetchMock();
    const app = createApp({ fetch: fetchFn, now: () => BASE_NOW_MS });
    const env: Env = { DB: db, SESSION_SECRET: TEST_SESSION_SECRET };

    const omittedRes = await app.fetch(
      postJson('/api/auth/google', { accessToken: 'unverified-omitted-token' }),
      env
    );
    assert.equal(omittedRes.status, 401);

    const falseRes = await app.fetch(
      postJson('/api/auth/google', { accessToken: 'unverified-false-token' }),
      env
    );
    assert.equal(falseRes.status, 401);
    assert.equal(getUserInfoRequests(), 2);
  });
});

// ==============================================================================
// 3. HMAC SESSION TOKEN & IDOR PROTECTION ON CLOUD SAVE / CLOUD LOAD
// ==============================================================================

describe('3. HMAC Session Token & IDOR protection on /api/player/cloud-save & /api/player/cloud-load', () => {
  async function createAuthenticatedUser(
    app: ReturnType<typeof createApp>,
    env: Env,
    sub: string,
    email: string
  ): Promise<string> {
    const session = await signSessionToken({ sub, email }, env.SESSION_SECRET!, BASE_NOW_MS);
    const now = BASE_NOW_MS;
    if (env.DB) {
      await env.DB.prepare(
        `INSERT INTO player_profiles (google_id, email, display_name, avatar_url, save_data, last_sync_at, created_at)
         VALUES (?, ?, ?, ?, ?, ?, ?)`
      )
        .bind(sub, email, `User ${sub}`, '', '{}', now, now)
        .run();
    }
    return session.token;
  }

  it('fails closed with 503 when SESSION_SECRET is missing', async () => {
    const { db } = createMockD1();
    const app = createApp({ now: () => BASE_NOW_MS });
    const validJwt = (
      await signSessionToken({ sub: 'user-a', email: 'a@phatroi.com' }, TEST_SESSION_SECRET, BASE_NOW_MS)
    ).token;

    const saveRes = await app.fetch(
      postJson(
        '/api/player/cloud-save',
        { saveData: '{"gold":1}' },
        { Authorization: `Bearer ${validJwt}` }
      ),
      { DB: db }
    );
    assert.equal(saveRes.status, 503);

    const loadRes = await app.fetch(
      new Request('https://phatroi.com/api/player/cloud-load', {
        headers: { Authorization: `Bearer ${validJwt}` },
      }),
      { DB: db }
    );
    assert.equal(loadRes.status, 503);
  });

  it('returns 401 when Authorization Bearer header is missing, forged, tampered, or expired', async () => {
    const { db } = createMockD1();
    let fakeNow = BASE_NOW_MS;
    const app = createApp({ now: () => fakeNow });
    const env: Env = { DB: db, SESSION_SECRET: TEST_SESSION_SECRET };

    const validToken = await createAuthenticatedUser(app, env, 'user-a', 'a@phatroi.com');
    const [hB64, , sigB64] = validToken.split('.');
    const tamperedPayloadB64 = encodeJwtPart({
      sub: 'user-b',
      email: 'b@phatroi.com',
      iat: Math.floor(BASE_NOW_MS / 1000),
      exp: Math.floor(BASE_NOW_MS / 1000) + SESSION_TTL_SEC,
    });
    const tamperedToken = `${hB64}.${tamperedPayloadB64}.${sigB64}`;

    const wrongSecretToken = (
      await signSessionToken({ sub: 'user-a', email: 'a@phatroi.com' }, 'another-secret-at-least-16-chars', BASE_NOW_MS)
    ).token;

    const algNoneToken = createUnsignedJwt(
      { alg: 'none', typ: 'JWT' },
      { sub: 'user-a', email: 'a@phatroi.com', exp: Math.floor(BASE_NOW_MS / 1000) + 3600 },
      'sig'
    );

    // Missing or malformed Authorization header -> 401
    const invalidAuthHeaders: Array<Record<string, string>> = [
      {},
      { Authorization: 'Basic dXNlcjpwYXNz' },
      { Authorization: 'Bearer ' },
      { Authorization: `Bearer ${tamperedToken}` },
      { Authorization: `Bearer ${wrongSecretToken}` },
      { Authorization: `Bearer ${algNoneToken}` },
    ];
    for (const headers of invalidAuthHeaders) {
      const saveRes = await app.fetch(
        postJson('/api/player/cloud-save', { saveData: '{"gold":10}' }, headers),
        env
      );
      assert.equal(saveRes.status, 401);

      const loadRes = await app.fetch(
        new Request('https://phatroi.com/api/player/cloud-load', { headers }),
        env
      );
      assert.equal(loadRes.status, 401);
    }

    // Expired session token -> 401
    fakeNow = BASE_NOW_MS + (SESSION_TTL_SEC + 5) * 1000;
    const expiredSaveRes = await app.fetch(
      postJson(
        '/api/player/cloud-save',
        { saveData: '{"gold":10}' },
        { Authorization: `Bearer ${validToken}` }
      ),
      env
    );
    assert.equal(expiredSaveRes.status, 401);

    const expiredLoadRes = await app.fetch(
      new Request('https://phatroi.com/api/player/cloud-load', {
        headers: { Authorization: `Bearer ${validToken}` },
      }),
      env
    );
    assert.equal(expiredLoadRes.status, 401);
  });

  it('blocks cross-user IDOR attempts with 403 on cloud-save and cloud-load', async () => {
    const { db, profiles } = createMockD1();
    const app = createApp({ now: () => BASE_NOW_MS });
    const env: Env = { DB: db, SESSION_SECRET: TEST_SESSION_SECRET };

    const tokenA = await createAuthenticatedUser(app, env, 'user-a', 'a@phatroi.com');
    await createAuthenticatedUser(app, env, 'user-b', 'b@phatroi.com');

    // Seed user B with protected save data
    profiles.get('user-b')!.save_data = '{"linhThach":999999}';

    const idorSaveRes = await app.fetch(
      postJson(
        '/api/player/cloud-save',
        { googleId: 'user-b', saveData: '{"linhThach":0}' },
        { Authorization: `Bearer ${tokenA}` }
      ),
      env
    );
    assert.equal(idorSaveRes.status, 403);
    assert.equal((await readJson(idorSaveRes)).error, 'Forbidden: googleId mismatch');
    assert.equal(profiles.get('user-b')!.save_data, '{"linhThach":999999}');

    const idorNonStringSaveRes = await app.fetch(
      postJson(
        '/api/player/cloud-save',
        { googleId: 12345, saveData: '{"linhThach":0}' },
        { Authorization: `Bearer ${tokenA}` }
      ),
      env
    );
    assert.equal(idorNonStringSaveRes.status, 403);

    const idorLoadRes = await app.fetch(
      new Request('https://phatroi.com/api/player/cloud-load?googleId=user-b', {
        headers: { Authorization: `Bearer ${tokenA}` },
      }),
      env
    );
    assert.equal(idorLoadRes.status, 403);
    assert.equal((await readJson(idorLoadRes)).error, 'Forbidden: googleId mismatch');
  });

  it('saves and loads JSON saveData with valid sessionToken (both in-memory and mock D1)', async () => {
    const rsaKey = await generateRsaKeyPair('kid-save-roundtrip');
    const nowSec = Math.floor(BASE_NOW_MS / 1000);
    const { fetchFn } = createJwksFetchMock(() => [rsaKey.publicJwk]);

    const idToken = await signRs256Jwt(
      { alg: 'RS256', kid: rsaKey.kid, typ: 'JWT' },
      {
        iss: 'https://accounts.google.com',
        aud: EXPECTED_GOOGLE_CLIENT_ID,
        sub: 'player-roundtrip',
        email: 'roundtrip@phatroi.com',
        email_verified: true,
        name: 'Đại Thợ Rèn',
        exp: nowSec + 3600,
      },
      rsaKey.privateKey
    );

    const mockD1 = createMockD1();
    const memoryStore = createMemoryStore();
    const targets: Array<{ label: string; env: Env }> = [
      { label: 'mock D1', env: { DB: mockD1.db, SESSION_SECRET: TEST_SESSION_SECRET } },
      { label: 'in-memory', env: { SESSION_SECRET: TEST_SESSION_SECRET } },
    ];

    for (const target of targets) {
      let currentNow = BASE_NOW_MS;
      const app = createApp({ fetch: fetchFn, now: () => currentNow, memoryStore });

      const loginRes = await app.fetch(
        postJson('/api/auth/google', { credential: idToken }),
        target.env
      );
      assert.equal(loginRes.status, 200, target.label);
      const loginData = await readJson<{ sessionToken: string }>(loginRes);

      currentNow += 5_000;
      const expectedSave = JSON.stringify({ vaultId: 4, linhThach: 42000, weaponLevel: 12 });
      const saveRes = await app.fetch(
        postJson(
          '/api/player/cloud-save',
          { saveData: expectedSave },
          { Authorization: `Bearer ${loginData.sessionToken}` }
        ),
        target.env
      );
      assert.equal(saveRes.status, 200, target.label);
      const saveBody = await readJson<{ success: boolean; lastSyncAt: number }>(saveRes);
      assert.equal(saveBody.success, true);
      assert.equal(saveBody.lastSyncAt, currentNow);

      const loadRes = await app.fetch(
        new Request('https://phatroi.com/api/player/cloud-load?googleId=player-roundtrip', {
          headers: { Authorization: `Bearer ${loginData.sessionToken}` },
        }),
        target.env
      );
      assert.equal(loadRes.status, 200, target.label);
      const loadBody = await readJson<{
        success: boolean;
        saveData: string;
        lastSyncAt: number;
        profile: { googleId: string };
      }>(loadRes);
      assert.equal(loadBody.success, true);
      assert.equal(loadBody.saveData, expectedSave);
      assert.equal(loadBody.lastSyncAt, currentNow);
      assert.equal(loadBody.profile.googleId, 'player-roundtrip');
    }
  });

  it('returns 404 (not 200) when Mock D1 updatePlayerSaveData returns meta: { changes: 0 }', async () => {
    const mockD1 = createMockD1();
    const app = createApp({ now: () => BASE_NOW_MS });
    const env: Env = { DB: mockD1.db, SESSION_SECRET: TEST_SESSION_SECRET };

    const token = await createAuthenticatedUser(app, env, 'user-changes-zero', 'zero@phatroi.com');

    // Even when profile exists, simulate D1 UPDATE returning meta: { changes: 0 }
    mockD1.setForcedSaveUpdateChanges(0);
    const res = await app.fetch(
      postJson(
        '/api/player/cloud-save',
        { saveData: '{"gold":123}' },
        { Authorization: `Bearer ${token}` }
      ),
      env
    );
    assert.equal(res.status, 404);
    const body = await readJson(res);
    assert.equal(body.success, false);

    // Also verify missing profile row naturally yields changes: 0 -> 404
    mockD1.setForcedSaveUpdateChanges(undefined);
    mockD1.profiles.delete('user-changes-zero');
    const missingRowRes = await app.fetch(
      postJson(
        '/api/player/cloud-save',
        { saveData: '{"gold":123}' },
        { Authorization: `Bearer ${token}` }
      ),
      env
    );
    assert.equal(missingRowRes.status, 404);
  });

  it('returns 400 for invalid JSON, empty saveData, non-string saveData, or oversized saveData', async () => {
    const { db } = createMockD1();
    const app = createApp({ now: () => BASE_NOW_MS });
    const env: Env = { DB: db, SESSION_SECRET: TEST_SESSION_SECRET };
    const token = await createAuthenticatedUser(app, env, 'user-bad-save', 'bad@phatroi.com');
    const headers = { Authorization: `Bearer ${token}` };

    const badPayloads: unknown[] = [
      { saveData: '' },
      { saveData: '   ' },
      { saveData: '{invalid-json' },
      { saveData: 12345 },
      { saveData: { nested: true } },
      {},
      { saveData: JSON.stringify({ data: 'a'.repeat(512_001) }) },
    ];

    for (const payload of badPayloads) {
      const res = await app.fetch(postJson('/api/player/cloud-save', payload, headers), env);
      assert.equal(res.status, 400);
    }

    const malformedBodyRes = await app.fetch(
      postJson('/api/player/cloud-save', '{not-json', headers),
      env
    );
    assert.equal(malformedBodyRes.status, 400);
  });
});

// ==============================================================================
// 4. /api/boss/reset FAIL-CLOSED SECURITY
// ==============================================================================

describe('4. /api/boss/reset fail-closed security', () => {
  it('returns 503 fail-closed when ADMIN_API_KEY is missing even if X-Admin-Key is sent', async () => {
    const { db } = createMockD1();
    const app = createApp({ now: () => BASE_NOW_MS });

    for (const adminSecret of [undefined, '', '   ']) {
      const res = await app.fetch(
        postJson(
          '/api/boss/reset?vaultId=1',
          {},
          { 'X-Admin-Key': TEST_ADMIN_KEY }
        ),
        { DB: db, ADMIN_API_KEY: adminSecret }
      );
      assert.equal(res.status, 503);
      const body = await readJson(res);
      assert.equal(body.success, false);
      assert.equal(body.error, 'Admin endpoint disabled: ADMIN_API_KEY is not configured');
    }
  });

  it('returns 401 when X-Admin-Key header is missing, wrong, or passed only in ?key= query string', async () => {
    const { db } = createMockD1();
    const app = createApp({ now: () => BASE_NOW_MS });
    const env: Env = { DB: db, ADMIN_API_KEY: TEST_ADMIN_KEY };

    // Missing header
    const missingRes = await app.fetch(postJson('/api/boss/reset?vaultId=1', {}), env);
    assert.equal(missingRes.status, 401);

    // Wrong X-Admin-Key values (different lengths & single-char diff)
    for (const wrongKey of ['', 'wrong-key', `${TEST_ADMIN_KEY}x`, `${TEST_ADMIN_KEY.slice(0, -1)}Z`]) {
      const wrongRes = await app.fetch(
        postJson('/api/boss/reset?vaultId=1', {}, { 'X-Admin-Key': wrongKey }),
        env
      );
      assert.equal(wrongRes.status, 401);
    }

    // Valid secret passed in ?key= query param only -> 401
    const queryKeyRes = await app.fetch(
      new Request(`https://phatroi.com/api/boss/reset?vaultId=1&key=${encodeURIComponent(TEST_ADMIN_KEY)}`, {
        method: 'POST',
      }),
      env
    );
    assert.equal(queryKeyRes.status, 401);
  });

  it('returns 200 with valid X-Admin-Key and resets Boss HP/armor to canonical floor values', async () => {
    const { db } = createMockD1();
    const app = createApp({ now: () => BASE_NOW_MS });
    const env: Env = { DB: db, ADMIN_API_KEY: TEST_ADMIN_KEY };

    // Damage and shatter floor 5 (maxArmor=4200; server clamps shatterPoints to 500 per strike)
    let struckState: Record<string, unknown> = {};
    for (let i = 0; i < 9; i++) {
      const strikeRes = await app.fetch(
        postJson('/api/boss/strike', {
          vaultId: 5,
          playerId: 'tester',
          damage: 25_000_000,
          shatterPoints: 500,
          furnaceCooling: 300,
        }),
        env
      );
      assert.equal(strikeRes.status, 200);
      struckState = (await readJson<{ state: Record<string, unknown> }>(strikeRes)).state;
    }
    assert.equal(struckState.currentHp, 75_000_000_000 - 9 * 25_000_000);
    assert.equal(struckState.currentArmor, 0);
    assert.equal(struckState.shatterUntil, BASE_NOW_MS + SHIELD_BREAK_DURATION_MS);
    assert.equal(struckState.isShieldBroken, true);

    // Reset via JSON body vaultId
    const resetRes = await app.fetch(
      postJson('/api/boss/reset', { vaultId: 5 }, { 'X-Admin-Key': TEST_ADMIN_KEY }),
      env
    );
    assert.equal(resetRes.status, 200);
    const resetBody = await readJson<{
      success: boolean;
      vaultId: number;
      state: {
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
      };
    }>(resetRes);

    assert.equal(resetBody.success, true);
    assert.equal(resetBody.vaultId, 5);
    assert.equal(resetBody.state.name, 'Xích Diễm Giới');
    assert.equal(resetBody.state.currentHp, 75_000_000_000);
    assert.equal(resetBody.state.maxHp, 75_000_000_000);
    assert.equal(resetBody.state.currentArmor, 4200);
    assert.equal(resetBody.state.maxArmor, 4200);
    assert.equal(resetBody.state.serverFurnaceHeat, 0);
    assert.equal(resetBody.state.serverAnvilHp, DEFAULT_SERVER_ANVIL_HP);
    assert.equal(resetBody.state.shatterUntil, 0);
    assert.equal(resetBody.state.isShieldBroken, false);
  });
});

// ==============================================================================
// 5. 9-FLOOR CELESTIAL_VAULTS SYNC & SELF-HEALING
// ==============================================================================

describe('5. 9-Floor CELESTIAL_VAULTS sync across GET /api/boss, POST /api/boss/strike, and POST /api/boss/reset', () => {
  it('syncs all 9 floors (vaultId 1..9) on GET, strike, and reset in both in-memory and mock D1', async () => {
    const mockD1 = createMockD1();
    const memoryStore = createMemoryStore();
    const backends: Array<{ label: string; env: Env }> = [
      { label: 'in-memory', env: { ADMIN_API_KEY: TEST_ADMIN_KEY } },
      { label: 'mock D1', env: { DB: mockD1.db, ADMIN_API_KEY: TEST_ADMIN_KEY } },
    ];

    for (const backend of backends) {
      const app = createApp({ now: () => BASE_NOW_MS, memoryStore });

      for (const expected of CANONICAL_CELESTIAL_VAULTS) {
        assert.equal(VAULT_CONFIGS[expected.vaultId].name, expected.name);
        assert.equal(VAULT_CONFIGS[expected.vaultId].maxHp, expected.maxHp);
        assert.equal(VAULT_CONFIGS[expected.vaultId].maxArmor, expected.maxArmor);

        // GET /api/boss
        const getRes = await app.fetch(
          new Request(`https://phatroi.com/api/boss?vaultId=${expected.vaultId}`),
          backend.env
        );
        assert.equal(getRes.status, 200, `${backend.label} GET floor ${expected.vaultId}`);
        const getBody = await readJson<{
          success: boolean;
          vaultId: number;
          name: string;
          currentHp: number;
          maxHp: number;
          currentArmor: number;
          maxArmor: number;
        }>(getRes);
        assert.equal(getBody.success, true);
        assert.equal(getBody.vaultId, expected.vaultId);
        assert.equal(getBody.name, expected.name);
        assert.equal(getBody.maxHp, expected.maxHp);
        assert.equal(getBody.currentHp, expected.maxHp);
        assert.equal(getBody.maxArmor, expected.maxArmor);
        assert.equal(getBody.currentArmor, expected.maxArmor);

        // POST /api/boss/strike
        const damage = 10_000;
        const shatterPoints = 100;
        const strikeRes = await app.fetch(
          postJson('/api/boss/strike', {
            vaultId: expected.vaultId,
            playerId: 'sync-tester',
            playerName: 'Kiểm Chứng Sư',
            damage,
            shatterPoints,
            furnaceCooling: 250,
          }),
          backend.env
        );
        assert.equal(strikeRes.status, 200, `${backend.label} strike floor ${expected.vaultId}`);
        const strikeBody = await readJson<{
          success: boolean;
          state: {
            vaultId: number;
            name: string;
            currentHp: number;
            maxHp: number;
            currentArmor: number;
            maxArmor: number;
            serverFurnaceHeat: number;
          };
        }>(strikeRes);
        assert.equal(strikeBody.success, true);
        assert.equal(strikeBody.state.vaultId, expected.vaultId);
        assert.equal(strikeBody.state.name, expected.name);
        assert.equal(strikeBody.state.maxHp, expected.maxHp);
        assert.equal(strikeBody.state.currentHp, expected.maxHp - damage);
        assert.equal(strikeBody.state.maxArmor, expected.maxArmor);
        assert.equal(strikeBody.state.currentArmor, expected.maxArmor - shatterPoints);
        assert.ok(strikeBody.state.serverFurnaceHeat <= MAX_SERVER_FURNACE_HEAT);

        // POST /api/boss/reset
        const resetRes = await app.fetch(
          postJson(
            `/api/boss/reset?vaultId=${expected.vaultId}`,
            {},
            { 'X-Admin-Key': TEST_ADMIN_KEY }
          ),
          backend.env
        );
        assert.equal(resetRes.status, 200, `${backend.label} reset floor ${expected.vaultId}`);
        const resetBody = await readJson<{
          success: boolean;
          vaultId: number;
          state: {
            vaultId: number;
            name: string;
            currentHp: number;
            maxHp: number;
            currentArmor: number;
            maxArmor: number;
            serverFurnaceHeat: number;
            shatterUntil: number;
            isShieldBroken: boolean;
          };
        }>(resetRes);
        assert.equal(resetBody.success, true);
        assert.equal(resetBody.state.vaultId, expected.vaultId);
        assert.equal(resetBody.state.name, expected.name);
        assert.equal(resetBody.state.maxHp, expected.maxHp);
        assert.equal(resetBody.state.currentHp, expected.maxHp);
        assert.equal(resetBody.state.maxArmor, expected.maxArmor);
        assert.equal(resetBody.state.currentArmor, expected.maxArmor);
        assert.equal(resetBody.state.serverFurnaceHeat, 0);
        assert.equal(resetBody.state.shatterUntil, 0);
        assert.equal(resetBody.state.isShieldBroken, false);
      }
    }
  });

  it('self-heals stale D1 row for floor 2 with wrong 1500000000 HP / 500 armor to 4500000000 / 1000', async () => {
    const staleFullD1 = createMockD1({
      seedBossStates: [
        {
          vault_id: 2,
          name: 'Thiết Vân Vòm',
          current_hp: 1_500_000_000,
          max_hp: 1_500_000_000,
          current_armor: 500,
          max_armor: 500,
          server_furnace_heat: 0,
          server_anvil_hp: DEFAULT_SERVER_ANVIL_HP,
          shatter_until: 0,
          last_strike_at: BASE_NOW_MS - 10_000,
          updated_at: BASE_NOW_MS - 10_000,
        },
      ],
    });

    const app = createApp({ now: () => BASE_NOW_MS });
    const res = await app.fetch(new Request('https://phatroi.com/api/boss?vaultId=2'), {
      DB: staleFullD1.db,
    });
    assert.equal(res.status, 200);
    const body = await readJson<{
      vaultId: number;
      name: string;
      currentHp: number;
      maxHp: number;
      currentArmor: number;
      maxArmor: number;
    }>(res);

    assert.equal(body.vaultId, 2);
    assert.equal(body.name, 'Cổ Đồng Thiên');
    assert.equal(body.currentHp, 4_500_000_000);
    assert.equal(body.maxHp, 4_500_000_000);
    assert.equal(body.currentArmor, 1000);
    assert.equal(body.maxArmor, 1000);

    const persisted = staleFullD1.bossStates.get(2)!;
    assert.equal(persisted.name, 'Cổ Đồng Thiên');
    assert.equal(persisted.current_hp, 4_500_000_000);
    assert.equal(persisted.max_hp, 4_500_000_000);
    assert.equal(persisted.current_armor, 1000);
    assert.equal(persisted.max_armor, 1000);

    // Also verify proportional preservation when stale row already took damage (50% HP & 50% armor)
    const staleDamagedD1 = createMockD1({
      seedBossStates: [
        {
          vault_id: 2,
          name: 'Tầng 2 cũ',
          current_hp: 750_000_000,
          max_hp: 1_500_000_000,
          current_armor: 250,
          max_armor: 500,
          server_furnace_heat: 0,
          server_anvil_hp: DEFAULT_SERVER_ANVIL_HP,
          shatter_until: 0,
          last_strike_at: BASE_NOW_MS - 10_000,
          updated_at: BASE_NOW_MS - 10_000,
        },
      ],
    });
    const damagedRes = await app.fetch(new Request('https://phatroi.com/api/boss?vaultId=2'), {
      DB: staleDamagedD1.db,
    });
    assert.equal(damagedRes.status, 200);
    const damagedBody = await readJson<{
      currentHp: number;
      maxHp: number;
      currentArmor: number;
      maxArmor: number;
    }>(damagedRes);
    assert.equal(damagedBody.maxHp, 4_500_000_000);
    assert.equal(damagedBody.currentHp, 2_250_000_000);
    assert.equal(damagedBody.maxArmor, 1000);
    assert.equal(damagedBody.currentArmor, 500);
  });

  it('returns 400 for invalid vaultId (0, 10, abc, -1, 1.5, 1abc, empty)', async () => {
    const { db } = createMockD1();
    const app = createApp({ now: () => BASE_NOW_MS });
    const env: Env = { DB: db, ADMIN_API_KEY: TEST_ADMIN_KEY };

    const invalidInputs: Array<{ query: string; jsonValue: unknown }> = [
      { query: '0', jsonValue: 0 },
      { query: '10', jsonValue: 10 },
      { query: 'abc', jsonValue: 'abc' },
      { query: '-1', jsonValue: -1 },
      { query: '1.5', jsonValue: 1.5 },
      { query: '1abc', jsonValue: '1abc' },
      { query: '', jsonValue: '' },
    ];

    for (const item of invalidInputs) {
      const getRes = await app.fetch(
        new Request(`https://phatroi.com/api/boss?vaultId=${encodeURIComponent(item.query)}`),
        env
      );
      assert.equal(getRes.status, 400, `GET /api/boss vaultId=${JSON.stringify(item.query)}`);

      const strikeRes = await app.fetch(
        postJson('/api/boss/strike', { vaultId: item.jsonValue, damage: 100 }),
        env
      );
      assert.equal(strikeRes.status, 400, `POST /api/boss/strike vaultId=${JSON.stringify(item.jsonValue)}`);

      const resetQueryRes = await app.fetch(
        postJson(
          `/api/boss/reset?vaultId=${encodeURIComponent(item.query)}`,
          {},
          { 'X-Admin-Key': TEST_ADMIN_KEY }
        ),
        env
      );
      assert.equal(resetQueryRes.status, 400, `POST /api/boss/reset query vaultId=${JSON.stringify(item.query)}`);

      const resetBodyRes = await app.fetch(
        postJson(
          '/api/boss/reset',
          { vaultId: item.jsonValue },
          { 'X-Admin-Key': TEST_ADMIN_KEY }
        ),
        env
      );
      assert.equal(resetBodyRes.status, 400, `POST /api/boss/reset body vaultId=${JSON.stringify(item.jsonValue)}`);
    }
  });
});
