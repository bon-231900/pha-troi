import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { DatabaseSync } from 'node:sqlite';

import { createApp, type Env } from '../src/index.ts';
import {
  EXPECTED_GOOGLE_CLIENT_ID,
  SESSION_TTL_SEC,
  base64UrlEncode,
  constantTimeEqual,
} from '../src/auth.ts';
import { SHIELD_BREAK_DURATION_MS, VAULT_CONFIGS } from '../src/vaults.ts';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const SCHEMA_SQL = fs.readFileSync(path.resolve(__dirname, '../schema.sql'), 'utf8');

const TEST_SESSION_SECRET = 'super-secret-session-key-at-least-32-chars!';
const TEST_ADMIN_KEY = 'super-secret-admin-key-for-tests';

/**
 * Real SQLite-backed D1Database test double executing actual schema.sql and D1 queries.
 */
function createTestD1(): { db: D1Database; raw: DatabaseSync } {
  const sqlite = new DatabaseSync(':memory:');
  sqlite.exec(SCHEMA_SQL);

  const makeStatement = (sql: string, bound: unknown[] = []): D1PreparedStatement => {
    const stmt: D1PreparedStatement = {
      bind(...values: unknown[]) {
        return makeStatement(sql, values);
      },
      async first<T = Record<string, unknown>>(colName?: string): Promise<T | null> {
        const prepared = sqlite.prepare(sql);
        const row = prepared.get(...(bound as Array<string | number | bigint | Uint8Array | null>)) as
          | Record<string, unknown>
          | undefined;
        if (!row) return null;
        if (colName) {
          return (row[colName] as T) ?? null;
        }
        return row as T;
      },
      async run<T = Record<string, unknown>>(): Promise<D1Result<T>> {
        const prepared = sqlite.prepare(sql);
        const info = prepared.run(...(bound as Array<string | number | bigint | Uint8Array | null>));
        return {
          success: true,
          results: [] as T[],
          meta: {
            duration: 0,
            size_after: 0,
            rows_read: 0,
            rows_written: Number(info.changes),
            last_row_id: Number(info.lastInsertRowid ?? 0),
            changed_db: Number(info.changes) > 0,
            changes: Number(info.changes),
          },
        };
      },
      async all<T = Record<string, unknown>>(): Promise<D1Result<T>> {
        const prepared = sqlite.prepare(sql);
        const rows = prepared.all(...(bound as Array<string | number | bigint | Uint8Array | null>)) as T[];
        return {
          success: true,
          results: rows,
          meta: {
            duration: 0,
            size_after: 0,
            rows_read: rows.length,
            rows_written: 0,
            last_row_id: 0,
            changed_db: false,
            changes: 0,
          },
        };
      },
      async raw<T = unknown[]>(): Promise<T[]> {
        const prepared = sqlite.prepare(sql);
        return prepared.all(...(bound as Array<string | number | bigint | Uint8Array | null>)) as T[];
      },
    };
    return stmt;
  };

  const db: D1Database = {
    prepare(query: string) {
      return makeStatement(query);
    },
    async dump(): Promise<ArrayBuffer> {
      return new ArrayBuffer(0);
    },
    async batch<T = unknown>(statements: D1PreparedStatement[]): Promise<D1Result<T>[]> {
      const results: D1Result<T>[] = [];
      for (const s of statements) {
        results.push(await s.run<T>());
      }
      return results;
    },
    async exec(query: string): Promise<D1ExecResult> {
      sqlite.exec(query);
      return { count: 1, duration: 0 };
    },
  };

  return { db, raw: sqlite };
}

async function generateRsaTestKey(kid: string) {
  const pair = (await crypto.subtle.generateKey(
    {
      name: 'RSASSA-PKCS1-v1_5',
      modulusLength: 2048,
      publicExponent: new Uint8Array([1, 0, 1]),
      hash: 'SHA-256',
    },
    true,
    ['sign', 'verify']
  )) as CryptoKeyPair;

  const exportedPub = (await crypto.subtle.exportKey('jwk', pair.publicKey)) as JsonWebKey & {
    kid?: string;
    use?: string;
    alg?: string;
  };
  exportedPub.kid = kid;
  exportedPub.use = 'sig';
  exportedPub.alg = 'RS256';

  return { privateKey: pair.privateKey, publicJwk: exportedPub };
}

async function signRs256Jwt(
  header: Record<string, unknown>,
  payload: Record<string, unknown>,
  privateKey: CryptoKey
): Promise<string> {
  const enc = new TextEncoder();
  const h = base64UrlEncode(enc.encode(JSON.stringify(header)));
  const p = base64UrlEncode(enc.encode(JSON.stringify(payload)));
  const input = `${h}.${p}`;
  const sig = await crypto.subtle.sign('RSASSA-PKCS1-v1_5', privateKey, enc.encode(input));
  return `${input}.${base64UrlEncode(new Uint8Array(sig))}`;
}

function makeUnsignedJwt(header: Record<string, unknown>, payload: Record<string, unknown>): string {
  const enc = new TextEncoder();
  const h = base64UrlEncode(enc.encode(JSON.stringify(header)));
  const p = base64UrlEncode(enc.encode(JSON.stringify(payload)));
  return `${h}.${p}.fakesig`;
}

async function readJson(res: Response): Promise<Record<string, unknown>> {
  return (await res.json()) as Record<string, unknown>;
}

describe('9-Floor CELESTIAL_VAULTS Sync & Schema', () => {
  it('schema.sql seeds all 9 canonical floors with exact HP, Armor, and Names', async () => {
    const { db } = createTestD1();
    const app = createApp({ now: () => 1_700_000_000_000 });
    const env: Env = { DB: db };

    for (let id = 1; id <= 9; id++) {
      const cfg = VAULT_CONFIGS[id];
      const res = await app.fetch(new Request(`https://phatroi.com/api/boss?vaultId=${id}`), env);
      assert.equal(res.status, 200);
      const body = await readJson(res);
      assert.equal(body.success, true);
      assert.equal(body.vaultId, cfg.vaultId);
      assert.equal(body.name, cfg.name);
      assert.equal(body.maxHp, cfg.maxHp);
      assert.equal(body.currentHp, cfg.maxHp);
      assert.equal(body.maxArmor, cfg.maxArmor);
      assert.equal(body.currentArmor, cfg.maxArmor);
    }

    assert.equal(VAULT_CONFIGS[5].meltingThreshold, 8500);
    assert.equal(VAULT_CONFIGS[9].maxHp, 2_500_000_000_000);
    assert.equal(VAULT_CONFIGS[9].maxArmor, 18000);
    assert.equal(VAULT_CONFIGS[9].armorRegenPerSec, 380);
  });

  it('rejects invalid vaultId (0, 10, abc, 1.5, 1abc) with 400 across boss endpoints', async () => {
    const { db } = createTestD1();
    const app = createApp({ now: () => 1_700_000_000_000 });
    const env: Env = { DB: db, ADMIN_API_KEY: TEST_ADMIN_KEY };

    for (const invalid of ['0', '10', '-1', 'abc', '1.5', '1abc', '']) {
      const getRes = await app.fetch(
        new Request(`https://phatroi.com/api/boss?vaultId=${encodeURIComponent(invalid)}`),
        env
      );
      assert.equal(getRes.status, 400, `GET /api/boss should reject vaultId=${JSON.stringify(invalid)}`);

      const strikeRes = await app.fetch(
        new Request('https://phatroi.com/api/boss/strike', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            vaultId: invalid === '' ? '' : Number.isNaN(Number(invalid)) ? invalid : Number(invalid),
            damage: 100,
          }),
        }),
        env
      );
      assert.equal(strikeRes.status, 400, `POST /api/boss/strike should reject vaultId=${JSON.stringify(invalid)}`);

      const resetRes = await app.fetch(
        new Request(`https://phatroi.com/api/boss/reset?vaultId=${encodeURIComponent(invalid)}`, {
          method: 'POST',
          headers: { 'X-Admin-Key': TEST_ADMIN_KEY },
        }),
        env
      );
      assert.equal(resetRes.status, 400, `POST /api/boss/reset should reject vaultId=${JSON.stringify(invalid)}`);
    }
  });

  it('self-heals stale floor metadata proportionally without losing dealt damage', async () => {
    const { db, raw } = createTestD1();
    raw
      .prepare(
        `UPDATE boss_state
         SET name = 'Tầng 2', current_hp = 750000000, max_hp = 1500000000, current_armor = 250, max_armor = 500
         WHERE vault_id = 2`
      )
      .run();

    const app = createApp({ now: () => 1_700_000_000_000 });
    const res = await app.fetch(new Request('https://phatroi.com/api/boss?vaultId=2'), { DB: db });
    assert.equal(res.status, 200);
    const body = await readJson(res);

    assert.equal(body.name, 'Cổ Đồng Thiên');
    assert.equal(body.maxHp, 4_500_000_000);
    assert.equal(body.currentHp, 2_250_000_000); // 50% preserved
    assert.equal(body.maxArmor, 1000);
    assert.equal(body.currentArmor, 500); // 50% preserved

    const persisted = raw.prepare('SELECT name, max_hp, current_hp, max_armor, current_armor FROM boss_state WHERE vault_id = 2').get() as Record<string, unknown>;
    assert.equal(persisted.name, 'Cổ Đồng Thiên');
    assert.equal(persisted.max_hp, 4_500_000_000);
    assert.equal(persisted.current_hp, 2_250_000_000);
  });

  it('handles 30s shield break trigger, mid-shatter immunity, and automatic expiry restoration', async () => {
    const { db } = createTestD1();
    let fakeNow = 1_700_000_000_000;
    const app = createApp({ now: () => fakeNow });
    const env: Env = { DB: db };

    // Break floor 1 shield (maxArmor = 500) via two 250-point strikes
    let res = await app.fetch(
      new Request('https://phatroi.com/api/boss/strike', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ playerId: 'p1', playerName: 'Thợ Rèn 1', vaultId: 1, damage: 1000, shatterPoints: 300 }),
      }),
      env
    );
    let data = await readJson(res);
    let state = data.state as Record<string, unknown>;
    assert.equal(state.currentArmor, 200);
    assert.equal(state.shatterUntil, 0);
    assert.equal(state.isShieldBroken, false);

    fakeNow += 1_000;
    res = await app.fetch(
      new Request('https://phatroi.com/api/boss/strike', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ playerId: 'p1', playerName: 'Thợ Rèn 1', vaultId: 1, damage: 2000, shatterPoints: 250 }),
      }),
      env
    );
    data = await readJson(res);
    state = data.state as Record<string, unknown>;
    assert.equal(state.currentArmor, 0);
    assert.equal(state.shatterUntil, fakeNow + SHIELD_BREAK_DURATION_MS);
    assert.equal(state.isShieldBroken, true);

    const expectedShatterEnd = fakeNow + SHIELD_BREAK_DURATION_MS;

    // Mid-shatter strike (+10s) must NOT overwrite shatterUntil
    fakeNow += 10_000;
    res = await app.fetch(
      new Request('https://phatroi.com/api/boss/strike', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ playerId: 'p1', playerName: 'Thợ Rèn 1', vaultId: 1, damage: 5000, shatterPoints: 100 }),
      }),
      env
    );
    data = await readJson(res);
    state = data.state as Record<string, unknown>;
    assert.equal(state.currentArmor, 0);
    assert.equal(state.shatterUntil, expectedShatterEnd);
    assert.equal(state.isShieldBroken, true);

    // At expiry, GET /api/boss restores currentArmor = maxArmor and shatterUntil = 0
    fakeNow = expectedShatterEnd;
    res = await app.fetch(new Request('https://phatroi.com/api/boss?vaultId=1'), env);
    data = await readJson(res);
    assert.equal(data.currentArmor, 500);
    assert.equal(data.shatterUntil, 0);
    assert.equal(data.isShieldBroken, false);

    // Also test direct strike right after a shatter expires without GET first
    res = await app.fetch(
      new Request('https://phatroi.com/api/boss/strike', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ playerId: 'p1', vaultId: 1, damage: 100, shatterPoints: 500 }),
      }),
      env
    );
    data = await readJson(res);
    state = data.state as Record<string, unknown>;
    const secondShatterEnd = fakeNow + SHIELD_BREAK_DURATION_MS;
    assert.equal(state.shatterUntil, secondShatterEnd);

    fakeNow = secondShatterEnd + 500;
    res = await app.fetch(
      new Request('https://phatroi.com/api/boss/strike', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ playerId: 'p1', vaultId: 1, damage: 100, shatterPoints: 40 }),
      }),
      env
    );
    data = await readJson(res);
    state = data.state as Record<string, unknown>;
    assert.equal(state.currentArmor, 460);
    assert.equal(state.shatterUntil, 0);
    assert.equal(state.isShieldBroken, false);
  });
});

describe('Google Authentication & JWKS Verification', () => {
  it('verifies RS256 ID token via JWKS, caches with Cache-Control, and refreshes once on rotated kid', async () => {
    const { db } = createTestD1();
    const key1 = await generateRsaTestKey('kid-1');
    const key2 = await generateRsaTestKey('kid-2');

    let fakeNow = 1_700_000_000_000;
    let jwksFetchCount = 0;
    let serveRotatedKeys = false;

    const mockFetch: typeof fetch = async (input) => {
      const url = typeof input === 'string' ? input : input.url;
      if (url === 'https://www.googleapis.com/oauth2/v3/certs') {
        jwksFetchCount++;
        const keys = serveRotatedKeys ? [key1.publicJwk, key2.publicJwk] : [key1.publicJwk];
        return new Response(JSON.stringify({ keys }), {
          status: 200,
          headers: {
            'Content-Type': 'application/json',
            'Cache-Control': 'public, max-age=120',
          },
        });
      }
      return new Response('Not found', { status: 404 });
    };

    const app = createApp({ fetch: mockFetch, now: () => fakeNow });
    const env: Env = { DB: db, SESSION_SECRET: TEST_SESSION_SECRET };

    const nowSec = Math.floor(fakeNow / 1000);
    const idToken1 = await signRs256Jwt(
      { alg: 'RS256', kid: 'kid-1', typ: 'JWT' },
      {
        iss: 'https://accounts.google.com',
        aud: EXPECTED_GOOGLE_CLIENT_ID,
        sub: 'google-user-123',
        email: 'thoren@phatroi.com',
        email_verified: true,
        name: 'Thợ Rèn Lão Luyện',
        picture: 'https://example.com/avatar.png',
        exp: nowSec + 3600,
      },
      key1.privateKey
    );

    const res1 = await app.fetch(
      new Request('https://phatroi.com/api/auth/google', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ credential: idToken1, localSaveData: '{"ignored":true}' }),
      }),
      env
    );
    assert.equal(res1.status, 200);
    const body1 = await readJson(res1);
    assert.equal(body1.success, true);
    assert.equal(body1.isNew, true);
    assert.equal(body1.saveData, '{}');
    assert.equal(typeof body1.sessionToken, 'string');
    assert.equal(body1.sessionExpiresAt, (nowSec + SESSION_TTL_SEC) * 1000);
    assert.equal(jwksFetchCount, 1);

    // Second request within max-age=120 uses cache
    fakeNow += 30_000;
    const res2 = await app.fetch(
      new Request('https://phatroi.com/api/auth/google', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ credential: idToken1 }),
      }),
      env
    );
    assert.equal(res2.status, 200);
    const body2 = await readJson(res2);
    assert.equal(body2.isNew, false);
    assert.equal(jwksFetchCount, 1);

    // Rotated kid triggers single forced refresh even before Cache-Control expiry
    serveRotatedKeys = true;
    const idToken2 = await signRs256Jwt(
      { alg: 'RS256', kid: 'kid-2', typ: 'JWT' },
      {
        iss: 'accounts.google.com',
        aud: EXPECTED_GOOGLE_CLIENT_ID,
        sub: 'google-user-123',
        email: 'thoren@phatroi.com',
        email_verified: true,
        exp: Math.floor(fakeNow / 1000) + 3600,
      },
      key2.privateKey
    );

    const res3 = await app.fetch(
      new Request('https://phatroi.com/api/auth/google', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ credential: idToken2 }),
      }),
      env
    );
    assert.equal(res3.status, 200);
    assert.equal(jwksFetchCount, 2);

    // Unknown kid refreshes once and returns 401
    const unknownKey = await generateRsaTestKey('kid-unknown');
    const badKidToken = await signRs256Jwt(
      { alg: 'RS256', kid: 'kid-unknown', typ: 'JWT' },
      {
        iss: 'https://accounts.google.com',
        aud: EXPECTED_GOOGLE_CLIENT_ID,
        sub: 'google-user-123',
        email: 'thoren@phatroi.com',
        email_verified: true,
        exp: Math.floor(fakeNow / 1000) + 3600,
      },
      unknownKey.privateKey
    );
    const res4 = await app.fetch(
      new Request('https://phatroi.com/api/auth/google', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ credential: badKidToken }),
      }),
      env
    );
    assert.equal(res4.status, 401);
    assert.equal(jwksFetchCount, 3);
  });

  it('rejects alg=none, HS256, unverified email, wrong aud/iss, expired exp, and forged signatures with 401', async () => {
    const { db } = createTestD1();
    const key1 = await generateRsaTestKey('kid-1');
    const attackerKey = await generateRsaTestKey('kid-1');
    const fakeNow = 1_700_000_000_000;
    const nowSec = Math.floor(fakeNow / 1000);

    const app = createApp({
      now: () => fakeNow,
      fetch: async () =>
        new Response(JSON.stringify({ keys: [key1.publicJwk] }), {
          status: 200,
          headers: { 'Cache-Control': 'max-age=300' },
        }),
    });
    const env: Env = { DB: db, SESSION_SECRET: TEST_SESSION_SECRET };

    const baseClaims = {
      iss: 'https://accounts.google.com',
      aud: EXPECTED_GOOGLE_CLIENT_ID,
      sub: 'user-1',
      email: 'user@example.com',
      email_verified: true,
      exp: nowSec + 3600,
    };

    const invalidTokens = [
      makeUnsignedJwt({ alg: 'none', kid: 'kid-1' }, baseClaims),
      makeUnsignedJwt({ alg: 'HS256', kid: 'kid-1' }, baseClaims),
      await signRs256Jwt({ alg: 'RS256', kid: 'kid-1' }, baseClaims, attackerKey.privateKey),
      await signRs256Jwt({ alg: 'RS256', kid: 'kid-1' }, { ...baseClaims, iss: 'https://evil.com' }, key1.privateKey),
      await signRs256Jwt({ alg: 'RS256', kid: 'kid-1' }, { ...baseClaims, aud: 'wrong-client-id' }, key1.privateKey),
      await signRs256Jwt({ alg: 'RS256', kid: 'kid-1' }, { ...baseClaims, exp: nowSec - 60 }, key1.privateKey),
      await signRs256Jwt({ alg: 'RS256', kid: 'kid-1' }, { ...baseClaims, email_verified: false }, key1.privateKey),
      await signRs256Jwt({ alg: 'RS256' }, baseClaims, key1.privateKey),
    ];

    for (const token of invalidTokens) {
      const res = await app.fetch(
        new Request('https://phatroi.com/api/auth/google', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ credential: token }),
        }),
        env
      );
      assert.equal(res.status, 401);
    }
  });

  it('verifies OAuth2 accessToken via tokeninfo + userinfo and rejects mismatched or unverified tokens', async () => {
    const { db } = createTestD1();
    const fakeNow = 1_700_000_000_000;

    const mockFetch: typeof fetch = async (input) => {
      const url = typeof input === 'string' ? input : input.url;
      if (url.startsWith('https://oauth2.googleapis.com/tokeninfo')) {
        if (url.includes('good-token')) {
          return new Response(
            JSON.stringify({
              azp: EXPECTED_GOOGLE_CLIENT_ID,
              sub: 'oauth-sub-1',
              expires_in: '3599',
              email_verified: 'true',
            }),
            { status: 200 }
          );
        }
        if (url.includes('wrong-aud')) {
          return new Response(
            JSON.stringify({ aud: 'other-app', expires_in: '3599', email_verified: 'true' }),
            { status: 200 }
          );
        }
        if (url.includes('sub-mismatch')) {
          return new Response(
            JSON.stringify({ aud: EXPECTED_GOOGLE_CLIENT_ID, sub: 'different-sub', expires_in: '3599' }),
            { status: 200 }
          );
        }
        return new Response(JSON.stringify({ error_description: 'Invalid Value' }), { status: 400 });
      }
      if (url === 'https://www.googleapis.com/oauth2/v3/userinfo') {
        return new Response(
          JSON.stringify({
            sub: 'oauth-sub-1',
            email: 'oauth@phatroi.com',
            name: 'OAuth Thợ Rèn',
            picture: 'https://example.com/pic.jpg',
          }),
          { status: 200 }
        );
      }
      return new Response('Not Found', { status: 404 });
    };

    const app = createApp({ fetch: mockFetch, now: () => fakeNow });
    const env: Env = { DB: db, SESSION_SECRET: TEST_SESSION_SECRET };

    const okRes = await app.fetch(
      new Request('https://phatroi.com/api/auth/google', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ accessToken: 'good-token' }),
      }),
      env
    );
    assert.equal(okRes.status, 200);
    const okData = await readJson(okRes);
    assert.equal(okData.success, true);
    assert.equal(typeof okData.sessionToken, 'string');

    for (const bad of ['wrong-aud', 'sub-mismatch', 'expired-or-bad']) {
      const badRes = await app.fetch(
        new Request('https://phatroi.com/api/auth/google', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ accessToken: bad }),
        }),
        env
      );
      assert.equal(badRes.status, 401);
    }
  });
});

describe('Fail-Closed SESSION_SECRET, Cloud Save/Load & Admin Reset', () => {
  it('returns 503 when SESSION_SECRET is missing or < 16 chars', async () => {
    const { db } = createTestD1();
    const app = createApp();

    for (const badSecret of [undefined, '', 'too-short', '               short']) {
      const env: Env = { DB: db, SESSION_SECRET: badSecret };
      for (const req of [
        new Request('https://phatroi.com/api/auth/google', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ credential: 'x.y.z' }),
        }),
        new Request('https://phatroi.com/api/player/cloud-save', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ saveData: '{}' }),
        }),
        new Request('https://phatroi.com/api/player/cloud-load'),
      ]) {
        const res = await app.fetch(req, env);
        assert.equal(res.status, 503);
        const body = await readJson(res);
        assert.equal(body.error, 'Server authentication not configured: SESSION_SECRET missing');
      }
    }
  });

  it('enforces Bearer JWT auth, googleId binding (403), saveData JSON/size validation (400), and D1 changes>0 (404)', async () => {
    const { db } = createTestD1();
    const key1 = await generateRsaTestKey('kid-1');
    let fakeNow = 1_700_000_000_000;

    const app = createApp({
      now: () => fakeNow,
      fetch: async () =>
        new Response(JSON.stringify({ keys: [key1.publicJwk] }), {
          status: 200,
          headers: { 'Cache-Control': 'max-age=300' },
        }),
    });
    const env: Env = { DB: db, SESSION_SECRET: TEST_SESSION_SECRET };

    const idToken = await signRs256Jwt(
      { alg: 'RS256', kid: 'kid-1' },
      {
        iss: 'https://accounts.google.com',
        aud: EXPECTED_GOOGLE_CLIENT_ID,
        sub: 'player-google-1',
        email: 'player1@phatroi.com',
        email_verified: true,
        exp: Math.floor(fakeNow / 1000) + 3600,
      },
      key1.privateKey
    );

    const loginRes = await app.fetch(
      new Request('https://phatroi.com/api/auth/google', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ credential: idToken }),
      }),
      env
    );
    const loginData = await readJson(loginRes);
    const sessionToken = loginData.sessionToken as string;

    // Missing / invalid Bearer token -> 401
    assert.equal(
      (
        await app.fetch(
          new Request('https://phatroi.com/api/player/cloud-save', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ saveData: '{"gold":10}' }),
          }),
          env
        )
      ).status,
      401
    );
    assert.equal(
      (
        await app.fetch(
          new Request('https://phatroi.com/api/player/cloud-load', {
            headers: { Authorization: 'Bearer invalid.jwt.token' },
          }),
          env
        )
      ).status,
      401
    );

    // Mismatched googleId -> 403
    const mismatchSave = await app.fetch(
      new Request('https://phatroi.com/api/player/cloud-save', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${sessionToken}`,
        },
        body: JSON.stringify({ googleId: 'victim-google-id', saveData: '{"gold":999}' }),
      }),
      env
    );
    assert.equal(mismatchSave.status, 403);
    assert.equal((await readJson(mismatchSave)).error, 'Forbidden: googleId mismatch');

    const mismatchLoad = await app.fetch(
      new Request('https://phatroi.com/api/player/cloud-load?googleId=victim-google-id', {
        headers: { Authorization: `Bearer ${sessionToken}` },
      }),
      env
    );
    assert.equal(mismatchLoad.status, 403);
    assert.equal((await readJson(mismatchLoad)).error, 'Forbidden: googleId mismatch');

    // Invalid saveData (empty, malformed JSON, > 512000 bytes) -> 400
    for (const badSave of ['', '   ', '{broken-json', JSON.stringify({ blob: 'x'.repeat(512_001) })]) {
      const badRes = await app.fetch(
        new Request('https://phatroi.com/api/player/cloud-save', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${sessionToken}`,
          },
          body: JSON.stringify({ saveData: badSave }),
        }),
        env
      );
      assert.equal(badRes.status, 400);
    }

    // Valid cloud-save (omitting googleId OR matching googleId) & cloud-load roundtrip
    const payloadStr = JSON.stringify({ currentVaultId: 3, linhThach: 12345 });
    const saveRes = await app.fetch(
      new Request('https://phatroi.com/api/player/cloud-save', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${sessionToken}`,
        },
        body: JSON.stringify({ googleId: 'player-google-1', saveData: payloadStr }),
      }),
      env
    );
    assert.equal(saveRes.status, 200);
    assert.equal((await readJson(saveRes)).success, true);

    const loadRes = await app.fetch(
      new Request('https://phatroi.com/api/player/cloud-load', {
        headers: { Authorization: `Bearer ${sessionToken}` },
      }),
      env
    );
    assert.equal(loadRes.status, 200);
    const loadData = await readJson(loadRes);
    assert.equal(loadData.saveData, payloadStr);

    // Deleting row in D1 yields changes === 0 -> 404 (not false positive 200 from res.success)
    await db.prepare('DELETE FROM player_profiles WHERE google_id = ?').bind('player-google-1').run();
    const missingRowSave = await app.fetch(
      new Request('https://phatroi.com/api/player/cloud-save', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${sessionToken}`,
        },
        body: JSON.stringify({ saveData: payloadStr }),
      }),
      env
    );
    assert.equal(missingRowSave.status, 404);

    // Expired session token (> 7 days) -> 401
    fakeNow += (SESSION_TTL_SEC + 1) * 1000;
    const expiredRes = await app.fetch(
      new Request('https://phatroi.com/api/player/cloud-load', {
        headers: { Authorization: `Bearer ${sessionToken}` },
      }),
      env
    );
    assert.equal(expiredRes.status, 401);
  });

  it('enforces fail-closed /api/boss/reset with header-only X-Admin-Key and canonical 9-floor reset', async () => {
    const { db } = createTestD1();
    const app = createApp({ now: () => 1_700_000_000_000 });

    // Missing ADMIN_API_KEY -> 503
    const disabledRes = await app.fetch(
      new Request('https://phatroi.com/api/boss/reset?vaultId=5', { method: 'POST' }),
      { DB: db }
    );
    assert.equal(disabledRes.status, 503);
    assert.equal(
      (await readJson(disabledRes)).error,
      'Admin endpoint disabled: ADMIN_API_KEY is not configured'
    );

    const env: Env = { DB: db, ADMIN_API_KEY: TEST_ADMIN_KEY };

    // ?key= query param MUST NOT authenticate -> 401
    const queryKeyRes = await app.fetch(
      new Request(`https://phatroi.com/api/boss/reset?vaultId=5&key=${TEST_ADMIN_KEY}`, {
        method: 'POST',
      }),
      env
    );
    assert.equal(queryKeyRes.status, 401);

    // Wrong header -> 401
    const wrongHeaderRes = await app.fetch(
      new Request('https://phatroi.com/api/boss/reset?vaultId=5', {
        method: 'POST',
        headers: { 'X-Admin-Key': 'wrong-key' },
      }),
      env
    );
    assert.equal(wrongHeaderRes.status, 401);

    // Damage and shatter floor 5 first
    await app.fetch(
      new Request('https://phatroi.com/api/boss/strike', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ vaultId: 5, damage: 50_000_000, shatterPoints: 500 }),
      }),
      env
    );

    // Valid X-Admin-Key resets floor 5 cleanly to canonical VAULT_CONFIGS[5]
    const okReset = await app.fetch(
      new Request('https://phatroi.com/api/boss/reset?vaultId=5', {
        method: 'POST',
        headers: { 'X-Admin-Key': TEST_ADMIN_KEY },
      }),
      env
    );
    assert.equal(okReset.status, 200);
    const resetBody = await readJson(okReset);
    const state = resetBody.state as Record<string, unknown>;
    assert.equal(state.vaultId, 5);
    assert.equal(state.name, 'Xích Diễm Giới');
    assert.equal(state.currentHp, 75_000_000_000);
    assert.equal(state.maxHp, 75_000_000_000);
    assert.equal(state.currentArmor, 4200);
    assert.equal(state.maxArmor, 4200);
    assert.equal(state.shatterUntil, 0);
    assert.equal(state.isShieldBroken, false);
  });

  it('constantTimeEqual handles same/different lengths accurately and leaderboard handles NaN limit', async () => {
    assert.equal(await constantTimeEqual('abc', 'abc'), true);
    assert.equal(await constantTimeEqual('abc', 'abd'), false);
    assert.equal(await constantTimeEqual('abc', 'abcd'), false);

    const { db } = createTestD1();
    const app = createApp({ now: () => 1_700_000_000_000 });
    await app.fetch(
      new Request('https://phatroi.com/api/boss/strike', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          playerId: 'top1',
          playerName: 'Đại Sư',
          vaultId: 1,
          damage: 1000,
          raidContribution: 50,
        }),
      }),
      { DB: db }
    );

    const lbRes = await app.fetch(
      new Request('https://phatroi.com/api/leaderboard?limit=not-a-number'),
      { DB: db }
    );
    assert.equal(lbRes.status, 200);
    const lbData = await readJson(lbRes);
    const rows = lbData.leaderboard as Array<Record<string, unknown>>;
    assert.equal(rows.length, 1);
    assert.equal(rows[0].player_id, 'top1');
  });
});
