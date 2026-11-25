// ==============================================================================
// CỬU TRỌNG THIÊN CẤM - 9-FLOOR CELESTIAL VAULTS CONFIG & STATE RECONCILIATION
// Synced 1:1 with CELESTIAL_VAULTS & SHIELD_BREAK_DURATION_SEC in frontend/src/game/rules.ts
// ==============================================================================

export const SHIELD_BREAK_DURATION_SEC = 30;
export const SHIELD_BREAK_DURATION_MS = SHIELD_BREAK_DURATION_SEC * 1000;

export const MIN_VAULT_ID = 1;
export const MAX_VAULT_ID = 9;
export const DEFAULT_SERVER_ANVIL_HP = 10_000;
export const MAX_SERVER_FURNACE_HEAT = 10_000;

export interface VaultConfig {
  vaultId: number;
  name: string;
  maxHp: number;
  maxArmor: number;
  armorRegenPerSec: number;
  meltingThreshold: number;
}

export interface BossStateRecord {
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

export const VAULT_CONFIGS: Record<number, VaultConfig> = {
  1: {
    vaultId: 1,
    name: 'Thiết Vân Vòm',
    maxHp: 1_500_000_000,
    maxArmor: 500,
    armorRegenPerSec: 15,
    meltingThreshold: 1500,
  },
  2: {
    vaultId: 2,
    name: 'Cổ Đồng Thiên',
    maxHp: 4_500_000_000,
    maxArmor: 1000,
    armorRegenPerSec: 30,
    meltingThreshold: 2200,
  },
  3: {
    vaultId: 3,
    name: 'Lôi Tiêu Điện',
    maxHp: 12_000_000_000,
    maxArmor: 1800,
    armorRegenPerSec: 55,
    meltingThreshold: 3000,
  },
  4: {
    vaultId: 4,
    name: 'Hàn Băng Thần',
    maxHp: 30_000_000_000,
    maxArmor: 2800,
    armorRegenPerSec: 85,
    meltingThreshold: 4200,
  },
  5: {
    vaultId: 5,
    name: 'Xích Diễm Giới',
    maxHp: 75_000_000_000,
    maxArmor: 4200,
    armorRegenPerSec: 120,
    meltingThreshold: 8500,
  },
  6: {
    vaultId: 6,
    name: 'Huyền Thủy Hải',
    maxHp: 180_000_000_000,
    maxArmor: 6000,
    armorRegenPerSec: 165,
    meltingThreshold: 5500,
  },
  7: {
    vaultId: 7,
    name: 'Bát Quái Phong',
    maxHp: 420_000_000_000,
    maxArmor: 8500,
    armorRegenPerSec: 220,
    meltingThreshold: 6500,
  },
  8: {
    vaultId: 8,
    name: 'Hư Không Đoạn',
    maxHp: 950_000_000_000,
    maxArmor: 12000,
    armorRegenPerSec: 280,
    meltingThreshold: 7500,
  },
  9: {
    vaultId: 9,
    name: 'Hỗn Độn Thiên',
    maxHp: 2_500_000_000_000,
    maxArmor: 18000,
    armorRegenPerSec: 380,
    meltingThreshold: 8800,
  },
};

export function getVaultConfig(vaultId: number): VaultConfig | null {
  if (!Number.isInteger(vaultId) || vaultId < MIN_VAULT_ID || vaultId > MAX_VAULT_ID) {
    return null;
  }
  return VAULT_CONFIGS[vaultId] ?? null;
}

/**
 * Strictly parses a vaultId as an integer in [1..9].
 * Returns null for non-integers, out-of-range numbers, empty strings, or malformed strings like "1abc".
 */
export function parseStrictVaultId(raw: unknown): number | null {
  if (typeof raw === 'number') {
    return Number.isInteger(raw) && raw >= MIN_VAULT_ID && raw <= MAX_VAULT_ID ? raw : null;
  }
  if (typeof raw === 'string') {
    const trimmed = raw.trim();
    if (!/^\d+$/.test(trimmed)) return null;
    const parsed = Number(trimmed);
    return Number.isInteger(parsed) && parsed >= MIN_VAULT_ID && parsed <= MAX_VAULT_ID ? parsed : null;
  }
  return null;
}

export function createCanonicalBossState(vaultId: number, now: number): BossStateRecord {
  const config = getVaultConfig(vaultId);
  if (!config) {
    throw new Error(`Invalid vaultId: ${vaultId}`);
  }
  return {
    vault_id: config.vaultId,
    name: config.name,
    current_hp: config.maxHp,
    max_hp: config.maxHp,
    current_armor: config.maxArmor,
    max_armor: config.maxArmor,
    server_furnace_heat: 0,
    server_anvil_hp: DEFAULT_SERVER_ANVIL_HP,
    shatter_until: 0,
    last_strike_at: now,
    updated_at: now,
  };
}

function scaleProportionalValue(current: number, oldMax: number, newMax: number): number {
  if (!Number.isFinite(current)) return newMax;
  if (current <= 0) return 0;
  if (oldMax !== newMax) {
    if (oldMax > 0) {
      const ratio = Math.max(0, Math.min(1, current / oldMax));
      return Math.max(0, Math.min(newMax, Math.round(ratio * newMax)));
    }
    return newMax;
  }
  return Math.max(0, Math.min(newMax, current));
}

/**
 * Self-heals stale floor metadata (name, max_hp, max_armor) proportionally without losing
 * dealt damage, and restores expired shield-break windows cleanly.
 */
export function reconcileBossStateRow(
  row: BossStateRecord,
  config: VaultConfig,
  now: number
): { state: BossStateRecord; changed: boolean } {
  const nextHp = scaleProportionalValue(row.current_hp, row.max_hp, config.maxHp);
  let nextArmor = scaleProportionalValue(row.current_armor, row.max_armor, config.maxArmor);
  let nextShatterUntil = Number.isFinite(row.shatter_until) ? row.shatter_until : 0;

  if (nextArmor <= 0 && now >= nextShatterUntil) {
    nextArmor = config.maxArmor;
    nextShatterUntil = 0;
  } else if (nextShatterUntil > 0 && now >= nextShatterUntil) {
    nextShatterUntil = 0;
  }

  const nextFurnaceHeat = Number.isFinite(row.server_furnace_heat)
    ? Math.max(0, Math.min(MAX_SERVER_FURNACE_HEAT, row.server_furnace_heat))
    : 0;
  const nextAnvilHp = Number.isFinite(row.server_anvil_hp)
    ? Math.max(0, Math.min(DEFAULT_SERVER_ANVIL_HP, row.server_anvil_hp))
    : DEFAULT_SERVER_ANVIL_HP;

  const changed =
    row.name !== config.name ||
    nextHp !== row.current_hp ||
    row.max_hp !== config.maxHp ||
    nextArmor !== row.current_armor ||
    row.max_armor !== config.maxArmor ||
    nextShatterUntil !== row.shatter_until ||
    nextFurnaceHeat !== row.server_furnace_heat ||
    nextAnvilHp !== row.server_anvil_hp;

  const state: BossStateRecord = {
    vault_id: config.vaultId,
    name: config.name,
    current_hp: nextHp,
    max_hp: config.maxHp,
    current_armor: nextArmor,
    max_armor: config.maxArmor,
    server_furnace_heat: nextFurnaceHeat,
    server_anvil_hp: nextAnvilHp,
    shatter_until: nextShatterUntil,
    last_strike_at: row.last_strike_at,
    updated_at: changed ? now : row.updated_at,
  };

  return { state, changed };
}

export function isBossShieldBroken(
  state: Pick<BossStateRecord, 'current_armor' | 'shatter_until'>,
  now: number
): boolean {
  return state.current_armor <= 0 || now < state.shatter_until;
}
