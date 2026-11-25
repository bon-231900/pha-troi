// ==============================================================================
// AUTHENTICATION & CRYPTOGRAPHIC VERIFICATION MODULE
// - Google ID Token RS256 verification against Google JWKS (with Cache-Control)
// - Google OAuth2 Access Token verification via tokeninfo + userinfo
// - HMAC-SHA256 Session JWT signing & verification for Cloud Save/Load
// - Constant-time secret comparison for Admin endpoints
// ==============================================================================

export const EXPECTED_GOOGLE_CLIENT_ID =
  '325984073866-an8facrtq5edm0aetm5ok3qmrf00oq7t.apps.googleusercontent.com';

export const SESSION_TTL_SEC = 604_800; // 7 days
export const MIN_SESSION_SECRET_LENGTH = 16;

export const GOOGLE_JWKS_URL = 'https://www.googleapis.com/oauth2/v3/certs';
export const GOOGLE_TOKENINFO_URL = 'https://oauth2.googleapis.com/tokeninfo';
export const GOOGLE_USERINFO_URL = 'https://www.googleapis.com/oauth2/v3/userinfo';

const VALID_GOOGLE_ISSUERS = new Set(['https://accounts.google.com', 'accounts.google.com']);
const CLOCK_SKEW_SEC = 30;
const DEFAULT_JWKS_CACHE_MS = 300_000;

const textEncoder = new TextEncoder();
const textDecoder = new TextDecoder();

export type FetchLike = typeof fetch;

export interface GoogleIdentity {
  sub: string;
  email: string;
  name: string;
  picture: string;
}

export interface SessionPayload {
  sub: string;
  email: string;
  iat: number;
  exp: number;
}

export interface SignedSession {
  token: string;
  expiresAt: number;
  payload: SessionPayload;
}

export interface GoogleJwk extends JsonWebKey {
  kid?: string;
  use?: string;
  alg?: string;
}

export interface JwksCache {
  keys: GoogleJwk[] | null;
  expiresAt: number;
}

export interface VerifyGoogleTokenOptions {
  fetchFn?: FetchLike;
  nowMs?: number;
  jwksCache?: JwksCache;
}

export function createJwksCache(): JwksCache {
  return { keys: null, expiresAt: 0 };
}

const defaultJwksCache: JwksCache = createJwksCache();

export function clearGoogleJwksCache(): void {
  defaultJwksCache.keys = null;
  defaultJwksCache.expiresAt = 0;
}

export function getSessionSecretError(secret?: string): string | null {
  if (!secret || secret.trim().length < MIN_SESSION_SECRET_LENGTH) {
    return 'Server authentication not configured: SESSION_SECRET missing';
  }
  return null;
}

export function base64UrlEncode(bytes: Uint8Array): string {
  let binary = '';
  for (let i = 0; i < bytes.length; i++) {
    binary += String.fromCharCode(bytes[i]);
  }
  return btoa(binary).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

export function base64UrlDecode(input: string): Uint8Array | null {
  if (!input || !/^[A-Za-z0-9_-]+$/.test(input) || input.length % 4 === 1) {
    return null;
  }
  try {
    const padded = input.replace(/-/g, '+').replace(/_/g, '/') + '='.repeat((4 - (input.length % 4)) % 4);
    const binary = atob(padded);
    const bytes = new Uint8Array(binary.length);
    for (let i = 0; i < binary.length; i++) {
      bytes[i] = binary.charCodeAt(i);
    }
    return bytes;
  } catch {
    return null;
  }
}

function decodeJwtJsonPart(part: string): Record<string, unknown> | null {
  const bytes = base64UrlDecode(part);
  if (!bytes) return null;
  try {
    const parsed: unknown = JSON.parse(textDecoder.decode(bytes));
    if (!parsed || typeof parsed !== 'object' || Array.isArray(parsed)) {
      return null;
    }
    return parsed as Record<string, unknown>;
  } catch {
    return null;
  }
}

/**
 * Constant-time string comparison via SHA-256 digests so neither length nor prefix leaks via timing.
 */
export async function constantTimeEqual(a: string, b: string): Promise<boolean> {
  const [digestA, digestB] = await Promise.all([
    crypto.subtle.digest('SHA-256', textEncoder.encode(a)),
    crypto.subtle.digest('SHA-256', textEncoder.encode(b)),
  ]);
  const bytesA = new Uint8Array(digestA);
  const bytesB = new Uint8Array(digestB);
  let diff = 0;
  for (let i = 0; i < bytesA.length; i++) {
    diff |= bytesA[i] ^ bytesB[i];
  }
  return diff === 0;
}

export function extractBearerToken(request: Request): string | null {
  const authHeader = request.headers.get('Authorization');
  if (!authHeader) return null;
  const match = authHeader.match(/^Bearer\s+(\S+)$/i);
  if (!match) return null;
  const token = match[1].trim();
  return token.length > 0 ? token : null;
}

function parseCacheMaxAgeMs(cacheControlHeader: string | null): number {
  if (!cacheControlHeader) return DEFAULT_JWKS_CACHE_MS;
  if (/\bno-store\b/i.test(cacheControlHeader) || /\bno-cache\b/i.test(cacheControlHeader)) {
    return 0;
  }
  const match = cacheControlHeader.match(/\bmax-age\s*=\s*(\d+)/i);
  if (!match) return DEFAULT_JWKS_CACHE_MS;
  const seconds = Number(match[1]);
  return Number.isFinite(seconds) && seconds > 0 ? seconds * 1000 : 0;
}

async function getGoogleJwks(
  fetchFn: FetchLike,
  nowMs: number,
  forceRefresh: boolean,
  cache: JwksCache
): Promise<{ keys: GoogleJwk[]; fromCache: boolean } | null> {
  if (!forceRefresh && cache.keys && nowMs < cache.expiresAt) {
    return { keys: cache.keys, fromCache: true };
  }

  let res: Response;
  try {
    res = await fetchFn(GOOGLE_JWKS_URL, {
      headers: { Accept: 'application/json' },
    });
  } catch {
    return null;
  }

  if (!res.ok) return null;

  let data: unknown;
  try {
    data = await res.json();
  } catch {
    return null;
  }

  if (!data || typeof data !== 'object' || !Array.isArray((data as { keys?: unknown }).keys)) {
    return null;
  }

  const keys = (data as { keys: GoogleJwk[] }).keys;
  const ttlMs = parseCacheMaxAgeMs(res.headers.get('Cache-Control'));
  if (ttlMs > 0) {
    cache.keys = keys;
    cache.expiresAt = nowMs + ttlMs;
  } else {
    cache.keys = null;
    cache.expiresAt = 0;
  }

  return { keys, fromCache: false };
}

function findMatchingRsaJwk(keys: GoogleJwk[], kid: string): GoogleJwk | null {
  for (const jwk of keys) {
    if (
      jwk &&
      jwk.kty === 'RSA' &&
      jwk.kid === kid &&
      (!jwk.use || jwk.use === 'sig') &&
      (!jwk.alg || jwk.alg === 'RS256') &&
      typeof jwk.n === 'string' &&
      typeof jwk.e === 'string'
    ) {
      return jwk;
    }
  }
  return null;
}

async function resolveSigningJwk(
  kid: string,
  fetchFn: FetchLike,
  nowMs: number,
  cache: JwksCache
): Promise<GoogleJwk | null> {
  const initial = await getGoogleJwks(fetchFn, nowMs, false, cache);
  if (!initial) return null;

  const matched = findMatchingRsaJwk(initial.keys, kid);
  if (matched) return matched;

  // Single forced refresh when kid is missing from cached JWKS (handles Google key rotation)
  if (initial.fromCache) {
    const refreshed = await getGoogleJwks(fetchFn, nowMs, true, cache);
    if (refreshed) {
      return findMatchingRsaJwk(refreshed.keys, kid);
    }
  }

  return null;
}

export async function verifyGoogleIdToken(
  credential: string,
  expectedClientId: string,
  options: VerifyGoogleTokenOptions = {}
): Promise<GoogleIdentity | null> {
  const fetchFn = options.fetchFn ?? fetch;
  const nowMs = options.nowMs ?? Date.now();
  const cache = options.jwksCache ?? defaultJwksCache;

  const parts = credential.split('.');
  if (parts.length !== 3 || !parts[0] || !parts[1] || !parts[2]) {
    return null;
  }

  const [headerB64, payloadB64, signatureB64] = parts;
  const header = decodeJwtJsonPart(headerB64);
  const payload = decodeJwtJsonPart(payloadB64);
  if (!header || !payload) {
    return null;
  }

  if (header.alg !== 'RS256' || typeof header.kid !== 'string' || header.kid.trim().length === 0) {
    return null;
  }

  const signatureBytes = base64UrlDecode(signatureB64);
  if (!signatureBytes || signatureBytes.length === 0) {
    return null;
  }

  const jwk = await resolveSigningJwk(header.kid, fetchFn, nowMs, cache);
  if (!jwk) {
    return null;
  }

  let signatureValid = false;
  try {
    const key = await crypto.subtle.importKey(
      'jwk',
      jwk as JsonWebKey,
      { name: 'RSASSA-PKCS1-v1_5', hash: 'SHA-256' },
      false,
      ['verify']
    );
    const signingInput = textEncoder.encode(`${headerB64}.${payloadB64}`);
    signatureValid = await crypto.subtle.verify(
      'RSASSA-PKCS1-v1_5',
      key,
      signatureBytes,
      signingInput
    );
  } catch {
    return null;
  }

  if (!signatureValid) {
    return null;
  }

  const nowSec = Math.floor(nowMs / 1000);
  if (typeof payload.iss !== 'string' || !VALID_GOOGLE_ISSUERS.has(payload.iss)) {
    return null;
  }
  if (payload.aud !== expectedClientId) {
    return null;
  }
  if (typeof payload.exp !== 'number' || !Number.isFinite(payload.exp) || payload.exp <= nowSec - CLOCK_SKEW_SEC) {
    return null;
  }
  if (
    payload.nbf !== undefined &&
    (typeof payload.nbf !== 'number' || !Number.isFinite(payload.nbf) || payload.nbf > nowSec + CLOCK_SKEW_SEC)
  ) {
    return null;
  }
  if (typeof payload.sub !== 'string' || payload.sub.trim().length === 0) {
    return null;
  }
  if (typeof payload.email !== 'string' || payload.email.trim().length === 0) {
    return null;
  }
  if (payload.email_verified !== true) {
    return null;
  }

  const sub = payload.sub.trim();
  const email = payload.email.trim();
  const name =
    typeof payload.name === 'string' && payload.name.trim().length > 0
      ? payload.name.trim()
      : 'Thợ Rèn Google';
  const picture = typeof payload.picture === 'string' ? payload.picture.trim() : '';

  return { sub, email, name, picture };
}

export async function verifyGoogleAccessToken(
  accessToken: string,
  expectedClientId: string,
  options: Pick<VerifyGoogleTokenOptions, 'fetchFn' | 'nowMs'> = {}
): Promise<GoogleIdentity | null> {
  const fetchFn = options.fetchFn ?? fetch;
  const nowMs = options.nowMs ?? Date.now();
  const nowSec = Math.floor(nowMs / 1000);

  let tokenInfoRes: Response;
  try {
    tokenInfoRes = await fetchFn(
      `${GOOGLE_TOKENINFO_URL}?access_token=${encodeURIComponent(accessToken)}`,
      { headers: { Accept: 'application/json' } }
    );
  } catch {
    return null;
  }

  if (!tokenInfoRes.ok) return null;

  let tokenInfo: Record<string, unknown>;
  try {
    const parsed: unknown = await tokenInfoRes.json();
    if (!parsed || typeof parsed !== 'object' || Array.isArray(parsed)) return null;
    tokenInfo = parsed as Record<string, unknown>;
  } catch {
    return null;
  }

  if (tokenInfo.aud !== expectedClientId && tokenInfo.azp !== expectedClientId) {
    return null;
  }

  const hasExpiresIn =
    tokenInfo.expires_in !== undefined &&
    tokenInfo.expires_in !== null &&
    String(tokenInfo.expires_in).trim() !== '';
  const hasExp =
    tokenInfo.exp !== undefined &&
    tokenInfo.exp !== null &&
    String(tokenInfo.exp).trim() !== '';

  if (!hasExpiresIn && !hasExp) {
    return null;
  }
  if (hasExpiresIn) {
    const expiresIn = Number(tokenInfo.expires_in);
    if (!Number.isFinite(expiresIn) || expiresIn <= 0) return null;
  }
  if (hasExp) {
    const exp = Number(tokenInfo.exp);
    if (!Number.isFinite(exp) || exp <= nowSec) return null;
  }

  const isEmailVerifiedFlag = (value: unknown): boolean => value === true || value === 'true';

  if (tokenInfo.email_verified !== undefined && !isEmailVerifiedFlag(tokenInfo.email_verified)) {
    return null;
  }

  let userInfoRes: Response;
  try {
    userInfoRes = await fetchFn(GOOGLE_USERINFO_URL, {
      headers: {
        Authorization: `Bearer ${accessToken}`,
        Accept: 'application/json',
      },
    });
  } catch {
    return null;
  }

  if (!userInfoRes.ok) return null;

  let userInfo: Record<string, unknown>;
  try {
    const parsed: unknown = await userInfoRes.json();
    if (!parsed || typeof parsed !== 'object' || Array.isArray(parsed)) return null;
    userInfo = parsed as Record<string, unknown>;
  } catch {
    return null;
  }

  if (typeof userInfo.sub !== 'string' || userInfo.sub.trim().length === 0) {
    return null;
  }
  if (typeof userInfo.email !== 'string' || userInfo.email.trim().length === 0) {
    return null;
  }
  if (userInfo.email_verified !== undefined && !isEmailVerifiedFlag(userInfo.email_verified)) {
    return null;
  }
  if (!isEmailVerifiedFlag(tokenInfo.email_verified) && !isEmailVerifiedFlag(userInfo.email_verified)) {
    return null;
  }

  const sub = userInfo.sub.trim();
  const tokenInfoSub = typeof tokenInfo.sub === 'string' ? tokenInfo.sub.trim() : '';
  if (tokenInfoSub.length > 0 && tokenInfoSub !== sub) {
    return null;
  }

  const email = userInfo.email.trim();
  const name =
    typeof userInfo.name === 'string' && userInfo.name.trim().length > 0
      ? userInfo.name.trim()
      : email;
  const picture = typeof userInfo.picture === 'string' ? userInfo.picture.trim() : '';

  return { sub, email, name, picture };
}

async function importHmacKey(secret: string, usages: Array<'sign' | 'verify'>): Promise<CryptoKey> {
  return crypto.subtle.importKey(
    'raw',
    textEncoder.encode(secret),
    { name: 'HMAC', hash: 'SHA-256' },
    false,
    usages
  );
}

export async function signSessionToken(
  identity: { sub: string; email: string },
  secret: string,
  nowMs: number = Date.now()
): Promise<SignedSession> {
  const secretErr = getSessionSecretError(secret);
  if (secretErr) {
    throw new Error(secretErr);
  }

  const iat = Math.floor(nowMs / 1000);
  const exp = iat + SESSION_TTL_SEC;
  const payload: SessionPayload = {
    sub: identity.sub,
    email: identity.email,
    iat,
    exp,
  };

  const headerB64 = base64UrlEncode(textEncoder.encode(JSON.stringify({ alg: 'HS256', typ: 'JWT' })));
  const payloadB64 = base64UrlEncode(textEncoder.encode(JSON.stringify(payload)));
  const signingInput = `${headerB64}.${payloadB64}`;

  const key = await importHmacKey(secret, ['sign']);
  const sigBuffer = await crypto.subtle.sign('HMAC', key, textEncoder.encode(signingInput));
  const sigB64 = base64UrlEncode(new Uint8Array(sigBuffer));

  return {
    token: `${signingInput}.${sigB64}`,
    expiresAt: exp * 1000,
    payload,
  };
}

export async function verifySessionToken(
  token: string,
  secret: string,
  nowMs: number = Date.now()
): Promise<SessionPayload | null> {
  if (getSessionSecretError(secret)) {
    return null;
  }

  const parts = token.split('.');
  if (parts.length !== 3 || !parts[0] || !parts[1] || !parts[2]) {
    return null;
  }

  const [headerB64, payloadB64, sigB64] = parts;
  const header = decodeJwtJsonPart(headerB64);
  const payload = decodeJwtJsonPart(payloadB64);
  if (!header || !payload) {
    return null;
  }

  if (header.alg !== 'HS256') {
    return null;
  }

  const sigBytes = base64UrlDecode(sigB64);
  if (!sigBytes || sigBytes.length === 0) {
    return null;
  }

  let valid = false;
  try {
    const key = await importHmacKey(secret, ['verify']);
    valid = await crypto.subtle.verify('HMAC', key, sigBytes, textEncoder.encode(`${headerB64}.${payloadB64}`));
  } catch {
    return null;
  }

  if (!valid) {
    return null;
  }

  const nowSec = Math.floor(nowMs / 1000);
  if (typeof payload.sub !== 'string' || payload.sub.trim().length === 0) {
    return null;
  }
  if (typeof payload.exp !== 'number' || !Number.isFinite(payload.exp) || payload.exp <= nowSec) {
    return null;
  }

  return {
    sub: payload.sub.trim(),
    email: typeof payload.email === 'string' ? payload.email : '',
    iat: typeof payload.iat === 'number' && Number.isFinite(payload.iat) ? payload.iat : 0,
    exp: payload.exp,
  };
}
