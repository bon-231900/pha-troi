# -*- coding: utf-8 -*-
"""
Full Balance Patch v3.0 script for rules.ts
"""
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

with open(r'd:\tieu-thuyet\frontend\src\game\rules.ts', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Fix typo in rollLootDrop
c = c.replace("if (grade === 'miss') return null;", "if (grade === 'MISS') return null;")
c = c.replace("if (grade === 'perfect') dropChance = 0.12;", "if (grade === 'PERFECT') dropChance = 0.12;")
c = c.replace("else if (grade === 'perfect' || isOverdrive) {", "else if (grade === 'PERFECT' || isOverdrive) {")

# 2. Add EquipmentSetId, EQUIPMENT_SETS, CoreStats, and updated ArsenalBonuses
old_arsenal_block = """export type EquipmentSlotKey = 'hammer' | 'anvil' | 'bellows' | 'gauntlets' | 'apron' | 'relic';

export type ItemRarity = 'common' | 'rare' | 'epic' | 'legendary' | 'mythic';

export const MAX_INVENTORY_SLOTS = 24;

export interface ItemAffix {
  id: string;
  type: 'prefix' | 'suffix';
  name: string;
  label: string;
  statKey:
    | 'flatDamage'
    | 'damageMultiplier'
    | 'critChancePct'
    | 'perfectWindowMs'
    | 'heatGainPerHit'
    | 'heatDecayReductionPct'
    | 'resonanceBonus'
    | 'linhThachPerHit'
    | 'afkLinhThachPerMin'
    | 'essenceDropChancePct'
    | 'synergyChargeBonusPct';
  value: number;
}

export type QuenchType = 'ice' | 'magma' | 'thunder';

export interface EquipmentItem {
  id: string;
  slotKey: EquipmentSlotKey;
  slotName: string;
  baseName: string;
  name: string;
  rarity: ItemRarity;
  itemLevel: number;
  baseStatLabel: string;
  baseStatValue: number;
  baseStatUnit: string;
  prefixes: ItemAffix[];
  suffixes: ItemAffix[];
  loreDescription: string;
  droppedAt?: number;
  quench?: QuenchType;
}

export interface ArsenalBonuses {
  flatDamage: number;
  damageMultiplier: number;
  resonanceBonus: number;
  heatPerHitBonus: number;
  critChancePct: number;
  perfectWindowMs: number;
  heatDecayReductionPct: number;
  dropLinhThachBonus: number;
  afkLinhThachPerMin: number;
  essenceDropChancePct: number;
  synergyChargeBonusPct: number;
  totalEquippedCount: number;
}"""

new_arsenal_block = """export type EquipmentSlotKey = 'hammer' | 'anvil' | 'bellows' | 'gauntlets' | 'apron' | 'relic';

export type ItemRarity = 'common' | 'rare' | 'epic' | 'legendary' | 'mythic';

export const MAX_INVENTORY_SLOTS = 24;

export type EquipmentSetId = 'set_thunder' | 'set_fire' | 'set_gravity' | 'set_mystic';

export interface EquipmentSetDef {
  id: EquipmentSetId;
  name: string;
  stanceKey: StanceKey;
  color: string;
  twoPieceBonusDesc: string;
  fourPieceBonusDesc: string;
  sixPieceBonusDesc: string;
}

export const EQUIPMENT_SETS: Record<EquipmentSetId, EquipmentSetDef> = {
  set_thunder: {
    id: 'set_thunder',
    name: 'Thiên Lôi Phá Khởi',
    stanceKey: 'Q',
    color: '#00F0FF',
    twoPieceBonusDesc: '+12% Nạp Cực Nhịp (SPI) & +8 ms Cửa Sổ Hoàng Kim',
    fourPieceBonusDesc: 'Vào Overdrive tăng +25% Phá Phách (PEN) trong 8s',
    sixPieceBonusDesc: 'Chuỗi Hoàng Kim tăng sát thương Sét Lan +8%/nhát (tối đa +80%)',
  },
  set_fire: {
    id: 'set_fire',
    name: 'Xích Diễm Phần Thiên',
    stanceKey: 'W',
    color: '#FF3B30',
    twoPieceBonusDesc: '+4°C Hỏa Hẩu/hit (INT) & giảm 30% tốc độ nguội lò',
    fourPieceBonusDesc: 'Sát thương Thiêu Đốt (Tro Tàn) có thể Bạo Kích theo 50% DEX Crit Rate',
    sixPieceBonusDesc: 'Khi Hỏa Hẩu >= 800°C, đòn đánh bỏ qua thêm 20% Giáp Boss',
  },
  set_gravity: {
    id: 'set_gravity',
    name: 'Thái Sơn Trọng Áp',
    stanceKey: 'E',
    color: '#A855F7',
    twoPieceBonusDesc: '+20% Lực Chùy (STR) & +1 Điểm Phá Giáp/hit',
    fourPieceBonusDesc: 'Chuyển hóa 25% Phá Phách (PEN) thành Sát Thương Bạo Kích',
    sixPieceBonusDesc: 'Gõ vào Boss Vỡ Giáp gây nổ chấn động bằng 180% tổng STR + PEN',
  },
  set_mystic: {
    id: 'set_mystic',
    name: 'Huyền Âm Vạn Dân',
    stanceKey: 'R',
    color: '#10B981',
    twoPieceBonusDesc: '+30% Sản Lượng Linh Thạch & +15% Cộng Hưởng (SPI)',
    fourPieceBonusDesc: 'Nhát gõ Hoàng Kim hồi +1°C Hỏa Hẩu & tăng +10% DMG thợ rèn lân cận',
    sixPieceBonusDesc: 'Kéo dài trạng thái Vỡ Giáp +5s & nhân đôi tỷ lệ rơi Tinh Hoa (TH)',
  },
};

export interface CoreStats {
  str: number; // Lực Chùy (Damage base + Stance E scaling)
  dex: number; // Chuẩn Xác (Crit chance, Crit dmg, Golden window)
  int: number; // Nhiệt Lực (Heating speed, Max heat, Burn DoT)
  pen: number; // Phá Phách (Armor break points, Direct Pierce %)
  spi: number; // Cộng Hưởng (Overdrive speed, drops, sync)
}

export interface ItemAffix {
  id: string;
  type: 'prefix' | 'suffix';
  name: string;
  label: string;
  statKey:
    | 'flatDamage'
    | 'damageMultiplier'
    | 'critChancePct'
    | 'perfectWindowMs'
    | 'heatGainPerHit'
    | 'heatDecayReductionPct'
    | 'resonanceBonus'
    | 'linhThachPerHit'
    | 'afkLinhThachPerMin'
    | 'essenceDropChancePct'
    | 'synergyChargeBonusPct';
  value: number;
}

export type QuenchType = 'ice' | 'magma' | 'thunder';

export interface EquipmentItem {
  id: string;
  slotKey: EquipmentSlotKey;
  slotName: string;
  baseName: string;
  name: string;
  rarity: ItemRarity;
  itemLevel: number;
  baseStatLabel: string;
  baseStatValue: number;
  baseStatUnit: string;
  prefixes: ItemAffix[];
  suffixes: ItemAffix[];
  loreDescription: string;
  droppedAt?: number;
  quench?: QuenchType;
  setId?: EquipmentSetId;
  setName?: string;
}

export interface ArsenalBonuses {
  flatDamage: number;
  damageMultiplier: number;
  resonanceBonus: number;
  heatPerHitBonus: number;
  critChancePct: number;
  perfectWindowMs: number;
  heatDecayReductionPct: number;
  dropLinhThachBonus: number;
  afkLinhThachPerMin: number;
  essenceDropChancePct: number;
  synergyChargeBonusPct: number;
  totalEquippedCount: number;
  coreStats: CoreStats;
  setCounts: Record<EquipmentSetId, number>;
  activeSetPerks: string[];
  glancingHitPenalty: boolean;
  critRateEffective: number;
  piercePct: number;
}"""

if old_arsenal_block in c:
    c = c.replace(old_arsenal_block, new_arsenal_block)
    print("1. Đã cập nhật Arsenal & CoreStats blocks!")
else:
    print("LỖI: Không tìm thấy old_arsenal_block!")
    sys.exit(1)

# 3. Cập nhật INITIAL_EQUIPPED_SLOTS & calculateArsenalBonuses
old_calc_block_start = "export const INITIAL_EQUIPPED_SLOTS: Record<EquipmentSlotKey, EquipmentItem> = {"
old_calc_block_end = "export interface StrikeInput {"

s_idx = c.find(old_calc_block_start)
e_idx = c.find(old_calc_block_end)

if s_idx == -1 or e_idx == -1:
    print("LỖI: Không tìm thấy INITIAL_EQUIPPED_SLOTS hoặc StrikeInput!")
    sys.exit(1)

new_calc_block = """export const INITIAL_EQUIPPED_SLOTS: Record<EquipmentSlotKey, EquipmentItem> = {
  hammer: {
    id: 'starter_hammer',
    slotKey: 'hammer',
    slotName: 'Thần Chùy',
    baseName: 'Búa Sắt Thiên Thai',
    name: 'Sắc Bén Búa Sắt Thiên Thai',
    rarity: 'common',
    itemLevel: 1,
    baseStatLabel: 'Sát Thương Cơ Bản',
    baseStatValue: 1,
    baseStatUnit: 'DMG',
    prefixes: [{ id: 'p_init_1', type: 'prefix', name: 'Sắc Bén', label: '+1 Sát thương cơ bản', statKey: 'flatDamage', value: 1 }],
    suffixes: [],
    loreDescription: 'Cây búa sắt thô sơ từ thung lũng Thiên Thai, vết rỉ sét ghi dấu ngày đầu khởi nghĩa phá trời.',
    setId: 'set_gravity',
    setName: 'Thái Sơn Trọng Áp',
  },
  anvil: {
    id: 'starter_anvil',
    slotKey: 'anvil',
    slotName: 'Thần Đe',
    baseName: 'Đe Thép Cổ Vân',
    name: 'Đe Thép Cổ Vân chi Phong Nhịp',
    rarity: 'common',
    itemLevel: 1,
    baseStatLabel: 'Vùng Hoàng Kim',
    baseStatValue: 6,
    baseStatUnit: 'ms',
    prefixes: [],
    suffixes: [{ id: 's_init_1', type: 'suffix', name: 'chi Phong Nhịp', label: '+8 ms Dung sai nhịp gõ', statKey: 'perfectWindowMs', value: 8 }],
    loreDescription: 'Khối đe thép tôi qua vạn lớp nước suối mây, bề mặt đanh chắc tạo âm vang dội.',
    setId: 'set_mystic',
    setName: 'Huyền Âm Vạn Dân',
  },
  bellows: {
    id: 'starter_bellows',
    slotKey: 'bellows',
    slotName: 'Hỏa Lò',
    baseName: 'Ống Bễ Da Hổ Lôi',
    name: 'Xích Diễm Ống Bễ Da Hổ Lôi',
    rarity: 'common',
    itemLevel: 1,
    baseStatLabel: 'Tích Nhiệt Đe',
    baseStatValue: 3,
    baseStatUnit: '°C/hit',
    prefixes: [{ id: 'p_init_2', type: 'prefix', name: 'Xích Diễm', label: '+2 °C/hit Hỏa Hầu', statKey: 'heatGainPerHit', value: 2 }],
    suffixes: [],
    loreDescription: 'May từ da hổ sấm, mỗi nhịp thổi bùng ngọn lửa đỏ rực công trường.',
    setId: 'set_fire',
    setName: 'Xích Diễm Phần Thiên',
  },
  gauntlets: {
    id: 'starter_gauntlets',
    slotKey: 'gauntlets',
    slotName: 'Bao Tay Rèn',
    baseName: 'Bao Tay Da Thô',
    name: 'Bao Tay Da Thô chi Bạo Kích',
    rarity: 'common',
    itemLevel: 1,
    baseStatLabel: 'Tỷ Lệ Bạo Kích',
    baseStatValue: 2,
    baseStatUnit: '%',
    prefixes: [],
    suffixes: [{ id: 's_init_2', type: 'suffix', name: 'chi Bạo Kích', label: '+2% Tỷ lệ Bạo Kích', statKey: 'critChancePct', value: 2 }],
    loreDescription: 'Bảo vệ lòng bàn tay khỏi những tia tàn tro đỏ rực tóe ra từ mặt đe.',
    setId: 'set_thunder',
    setName: 'Thiên Lôi Phá Khởi',
  },
  apron: {
    id: 'starter_apron',
    slotKey: 'apron',
    slotName: 'Tạp Dề Thiết Hộ',
    baseName: 'Tạp Dề Bì Hộ',
    name: 'Tạp Dề Bì Hộ',
    rarity: 'common',
    itemLevel: 1,
    baseStatLabel: 'Linh Thạch Treo Máy',
    baseStatValue: 15,
    baseStatUnit: 'LT/phút',
    prefixes: [],
    suffixes: [],
    loreDescription: 'Tạp dề lót giáp sắt mỏng, che chắn lồng ngực thợ rèn trước xung lực rực lửa.',
    setId: 'set_mystic',
    setName: 'Huyền Âm Vạn Dân',
  },
  relic: {
    id: 'starter_relic',
    slotKey: 'relic',
    slotName: 'Định Thiên Pháp Bảo',
    baseName: 'Thạch Bàn Đông Sơn',
    name: 'Thạch Bàn Đông Sơn',
    rarity: 'common',
    itemLevel: 1,
    baseStatLabel: 'Sát Thương Toàn Thể',
    baseStatValue: 5,
    baseStatUnit: '%',
    prefixes: [],
    suffixes: [],
    loreDescription: 'Mảnh thạch bàn khắc họa chim Lạc sải cánh, tượng trưng cho ý chí người thợ rèn Việt cổ.',
    setId: 'set_thunder',
    setName: 'Thiên Lôi Phá Khởi',
  },
};

export function calculateArsenalBonuses(
  equipped: Record<EquipmentSlotKey, EquipmentItem | null> | EquipmentItem[],
  upgrades?: ForgeUpgrade[]
): ArsenalBonuses {
  let flatDamage = 0;
  let damageMultiplier = 1.0;
  let resonanceBonus = 0;
  let heatPerHitBonus = 0;
  let critChancePct = 3; // Base character crit rate: 3%
  let perfectWindowMs = 0;
  let heatDecayReductionPct = 0;
  let dropLinhThachBonus = 0;
  let afkLinhThachPerMin = 0;
  let essenceDropChancePct = 0;
  let synergyChargeBonusPct = 0;
  let totalEquippedCount = 0;

  const setCounts: Record<EquipmentSetId, number> = {
    set_thunder: 0,
    set_fire: 0,
    set_gravity: 0,
    set_mystic: 0,
  };

  const items: EquipmentItem[] = Array.isArray(equipped)
    ? equipped.filter(Boolean)
    : (Object.values(equipped).filter(Boolean) as EquipmentItem[]);

  for (const item of items) {
    totalEquippedCount += 1;
    if (item.setId && item.setId in setCounts) {
      setCounts[item.setId] += 1;
    }

    switch (item.slotKey) {
      case 'hammer':
        flatDamage += item.baseStatValue;
        break;
      case 'anvil':
        perfectWindowMs += item.baseStatValue;
        break;
      case 'bellows':
        heatPerHitBonus += item.baseStatValue;
        break;
      case 'gauntlets':
        critChancePct += item.baseStatValue;
        break;
      case 'apron':
        afkLinhThachPerMin += item.baseStatValue;
        break;
      case 'relic':
        damageMultiplier += item.baseStatValue / 100;
        break;
    }

    if (item.quench) {
      if (item.quench === 'ice') {
        essenceDropChancePct += 15;
        afkLinhThachPerMin += 25;
      } else if (item.quench === 'magma') {
        flatDamage += 8;
      } else if (item.quench === 'thunder') {
        critChancePct += 8;
      }
    }

    const allAffixes = [...item.prefixes, ...item.suffixes];
    for (const aff of allAffixes) {
      switch (aff.statKey) {
        case 'flatDamage':
          flatDamage += aff.value;
          break;
        case 'damageMultiplier':
          damageMultiplier += aff.value;
          break;
        case 'critChancePct':
          critChancePct += aff.value;
          break;
        case 'perfectWindowMs':
          perfectWindowMs += aff.value;
          break;
        case 'heatGainPerHit':
          heatPerHitBonus += aff.value;
          break;
        case 'heatDecayReductionPct':
          heatDecayReductionPct += aff.value;
          break;
        case 'resonanceBonus':
          resonanceBonus += aff.value;
          break;
        case 'linhThachPerHit':
          dropLinhThachBonus += aff.value;
          break;
        case 'afkLinhThachPerMin':
          afkLinhThachPerMin += aff.value;
          break;
        case 'essenceDropChancePct':
          essenceDropChancePct += aff.value;
          break;
        case 'synergyChargeBonusPct':
          synergyChargeBonusPct += aff.value;
          break;
      }
    }
  }

  // Active Set Perks evaluation (2 / 4 / 6 Món)
  const activeSetPerks: string[] = [];
  if (setCounts.set_thunder >= 2) {
    synergyChargeBonusPct += 12;
    perfectWindowMs += 8;
    activeSetPerks.push('Thiên Lôi 2/6: +12% Nạp Cực Nhịp (SPI) & +8 ms Cửa Sổ Hoàng Kim');
  }
  if (setCounts.set_thunder >= 4) {
    activeSetPerks.push('Thiên Lôi 4/6: Vào Overdrive tăng +25% Phá Phách (PEN)');
  }
  if (setCounts.set_thunder >= 6) {
    activeSetPerks.push('Thiên Lôi 6/6: Chuỗi Hoàng Kim tăng sát thương Sét Lan +8%/nhát (tối đa +80%)');
  }

  if (setCounts.set_fire >= 2) {
    heatPerHitBonus += 4;
    heatDecayReductionPct += 30;
    activeSetPerks.push('Xích Diễm 2/6: +4°C Hỏa Hẩu/hit (INT) & giảm 30% tốc độ nguội lò');
  }
  if (setCounts.set_fire >= 4) {
    activeSetPerks.push('Xích Diễm 4/6: Sát thương Thiêu Đốt (Tro Tàn) có thể Bạo Kích');
  }
  if (setCounts.set_fire >= 6) {
    activeSetPerks.push('Xích Diễm 6/6: Khi Hỏa Hẩu >= 800°C, đòn đánh bỏ qua thêm 20% Giáp Boss');
  }

  if (setCounts.set_gravity >= 2) {
    activeSetPerks.push('Thái Sơn 2/6: +20% Lực Chùy (STR) & +1 Điểm Phá Giáp/hit');
  }
  if (setCounts.set_gravity >= 4) {
    activeSetPerks.push('Thái Sơn 4/6: Chuyển hóa 25% Phá Phách (PEN) thành Sát Thương Bạo Kích');
  }
  if (setCounts.set_gravity >= 6) {
    activeSetPerks.push('Thái Sơn 6/6: Gõ vào Boss Vỡ Giáp gây nổ chấn động bằng 180% tổng STR + PEN');
  }

  if (setCounts.set_mystic >= 2) {
    dropLinhThachBonus += 3;
    activeSetPerks.push('Huyền Âm 2/6: +30% Sản Lượng Linh Thạch & +15% Cộng Hưởng (SPI)');
  }
  if (setCounts.set_mystic >= 4) {
    activeSetPerks.push('Huyền Âm 4/6: Hoàng Kim hồi +1°C Hỏa Hẩu & tăng +10% DMG thợ rèn lân cận');
  }
  if (setCounts.set_mystic >= 6) {
    activeSetPerks.push('Huyền Âm 6/6: Kéo dài trạng thái Vỡ Giáp +5s & nhân đôi tỷ lệ rơi Tinh Hoa');
  }

  // Ngũ Đại Thuộc Tính Rèn (Core Stats)
  const hammerLvl = upgrades?.find((u) => u.id === 'celestial_hammer_core')?.level ?? 1;
  const quenchLvl = upgrades?.find((u) => u.id === 'thunder_quench_oil')?.level ?? 0;
  const bellowsLvl = upgrades?.find((u) => u.id === 'nine_heavens_bellows')?.level ?? 0;
  const anvilLvl = upgrades?.find((u) => u.id === 'ancient_anvil_rune')?.level ?? 0;

  let rawSTR = hammerLvl * 2 + flatDamage + 5;
  if (setCounts.set_gravity >= 2) {
    rawSTR = Math.round(rawSTR * 1.2);
  }

  const rawDEX = Math.round(critChancePct * 3 + perfectWindowMs);
  const rawINT = bellowsLvl * 3 + heatPerHitBonus * 4 + 10;
  const rawPEN = quenchLvl * 2 + anvilLvl * 2 + Math.round(flatDamage * 0.5) + (setCounts.set_gravity >= 2 ? 5 : 0);
  let rawSPI = Math.round(synergyChargeBonusPct + resonanceBonus * 2 + afkLinhThachPerMin * 0.4 + 10);
  if (setCounts.set_mystic >= 2) {
    rawSPI = Math.round(rawSPI * 1.15);
  }

  // Soft Cap 1: Crit Rate (55% Soft Cap, Hard Cap 80%)
  const rawCrit = Math.round(critChancePct);
  const critRateEffective = rawCrit <= 55 ? rawCrit : Math.min(80, Math.round(55 + (rawCrit - 55) * 0.5));

  // Soft Cap 2: Golden Window (+30 ms max)
  const cappedPerfectWindowMs = Math.min(30, Math.round(perfectWindowMs));

  // Glancing Hit (Dội Búa): If STR > 2.5 * INT
  const glancingHitPenalty = rawSTR > 2.5 * Math.max(1, rawINT);

  // Penetration percentage
  const piercePct = Math.min(0.65, Number((rawPEN / (rawPEN + 50)).toFixed(3)));

  return {
    flatDamage: Math.round(flatDamage),
    damageMultiplier: Number(damageMultiplier.toFixed(2)),
    resonanceBonus: Math.round(resonanceBonus),
    heatPerHitBonus: Math.round(heatPerHitBonus),
    critChancePct: critRateEffective,
    perfectWindowMs: cappedPerfectWindowMs,
    heatDecayReductionPct: Math.min(75, Math.round(heatDecayReductionPct)),
    dropLinhThachBonus: Math.round(dropLinhThachBonus),
    afkLinhThachPerMin: Math.round(afkLinhThachPerMin),
    essenceDropChancePct: Math.round(essenceDropChancePct),
    synergyChargeBonusPct: Math.round(synergyChargeBonusPct),
    totalEquippedCount,
    coreStats: {
      str: rawSTR,
      dex: rawDEX,
      int: rawINT,
      pen: rawPEN,
      spi: rawSPI,
    },
    setCounts,
    activeSetPerks,
    glancingHitPenalty,
    critRateEffective,
    piercePct,
  };
}

"""

c = c[:s_idx] + new_calc_block + c[e_idx:]
print("2. Đã cập nhật INITIAL_EQUIPPED_SLOTS & calculateArsenalBonuses!")

# 4. Cập nhật StrikeInput, StrikeOutcome và calculateStrikeOutcome
old_strike_start = "export interface StrikeInput {"
old_strike_end = "export interface ForgeUpgrade {"

s_strike = c.find(old_strike_start)
e_strike = c.find(old_strike_end)

new_strike_block = """export interface StrikeInput {
  grade: JudgmentGrade;
  stance: StanceKey;
  basePower: number; // 1 at Lv1, 12 at Lv10, 50 at Lv25
  combo: number;
  overdriveCharge: number; // 0 to 8
  overdriveActive: boolean;
  bossShieldPct: number; // 0 to 100
  spiritBonusMult: number; // >= 1.0
  globalBurstActive: boolean;
  anvilHeat?: number; // 100 to 1000 °C
  sealDamageReductionPct?: number; // 80, 60, 40, 0
  isShieldBroken?: boolean;
  arsenalBonuses?: ArsenalBonuses;
  stanceSkillBonuses?: Record<string, number>;
  forgerRankMultiplier?: number;
  currentFloorId?: number;
  stanceWeave?: { previousStance: StanceKey; timeLeftSec: number } | null;
}

export interface StrikeOutcome {
  damage: number;
  displayMultiplier: number;
  nextCombo: number;
  nextOverdriveCharge: number;
  triggeredOverdrive: boolean;
  heatGain: number;
  resonanceGain: number;
  linhThachEarned: number;
  tinhHoaEarned: number;
  isCrit?: boolean;
  isGolden?: boolean;
  isGlancingHit?: boolean;
  effectivePiercePct?: number;
}

export function calculateStrikeOutcome(input: StrikeInput): StrikeOutcome {
  const stanceCfg = HAMMER_STANCES[input.stance];

  if (input.grade === 'MISS') {
    return {
      damage: 0,
      displayMultiplier: 0,
      nextCombo: 0,
      nextOverdriveCharge: Math.max(0, input.overdriveCharge - 2),
      triggeredOverdrive: false,
      heatGain: -50,
      resonanceGain: 0,
      linhThachEarned: 0,
      tinhHoaEarned: 0,
    };
  }

  const isGolden = input.grade === 'PERFECT';
  const isGreat = input.grade === 'GREAT';

  // 1. Timing Multiplier (Hoàng Kim x2.5 / x3.2 streak, Thuần Thục x1.25, Chuẩn Xác x1.0)
  const timingMult = isGolden ? (input.combo >= 5 ? 3.2 : 2.5) : isGreat ? 1.25 : 1.0;
  const nextCombo = input.combo + 1;

  // 2. Overdrive Charging
  const chargeGain = isGolden ? 1 : 0.5;
  let nextOverdriveCharge = input.overdriveCharge;
  let triggeredOverdrive = false;

  if (!input.overdriveActive) {
    nextOverdriveCharge = Math.min(OVERDRIVE_MAX, input.overdriveCharge + chargeGain);
    if (nextOverdriveCharge >= OVERDRIVE_MAX) {
      triggeredOverdrive = true;
    }
  }

  const isOverdriveNow = input.overdriveActive || triggeredOverdrive;
  const overdriveMult = isOverdriveNow ? 2.0 : 1.0;
  const globalBurstMult = input.globalBurstActive ? 2.0 : 1.0;

  // 3. Core Stats & Thermal Synchronization (M_Thermal)
  const arsenal = input.arsenalBonuses;
  const str = arsenal?.coreStats.str ?? input.basePower;
  const dex = arsenal?.coreStats.dex ?? 10;
  const intStat = arsenal?.coreStats.int ?? 10;
  const pen = arsenal?.coreStats.pen ?? 10;

  const currentHeat = Math.max(100, Math.min(1000, input.anvilHeat ?? 100));
  let thermalMult = currentHeat < 400 ? 0.8 : currentHeat <= 700 ? 1.15 : 1.35;

  // Glancing Hit (Dội Búa): If STR > 2.5 * INT
  const isGlancingHit = str > 2.5 * Math.max(1, intStat);
  if (isGlancingHit) {
    thermalMult *= 0.65; // -35% damage penalty on glancing hits
  }

  // 4. Critical Strike (DEX Scaling & Soft Cap 55% -> 80%)
  const stanceBonuses = input.stanceSkillBonuses;
  const stanceCritAdd = stanceBonuses ? stanceBonuses.critChanceAdd ?? 0 : 0;
  const critChance = Math.min(80, (arsenal ? arsenal.critRateEffective : 5) + stanceCritAdd);
  const isCrit = Math.random() * 100 < critChance;

  let critMult = 1.0;
  if (isCrit) {
    const override = stanceBonuses ? stanceBonuses.critMultOverride ?? 0 : 0;
    critMult = override > 0 ? override : input.stance === 'E' ? 2.2 : 2.0;
  }

  // 5. Boss Armor & Direct Penetration (Hyperbolic formula)
  const floorId = input.currentFloorId ?? 1;
  const kFloor = floorId <= 2 ? 50 : floorId <= 5 ? 80 : floorId <= 7 ? 120 : 160;
  let basePierce = Math.min(0.65, pen / (pen + kFloor));

  // Set Bonus: Xích Diễm 6/6 grants +20% armor ignore when Heat >= 800°C
  if ((arsenal?.setCounts.set_fire ?? 0) >= 6 && currentHeat >= 800) {
    basePierce = Math.min(0.85, basePierce + 0.20);
  }

  const baseBossArmor = (input.sealDamageReductionPct ?? 80) / 100;
  let armorFactor = 1.0;

  if (input.isShieldBroken || input.bossShieldPct <= 0) {
    armorFactor = 1.5; // 1.5x vulnerability on shield break
  } else {
    const effectiveReduction = baseBossArmor * (1 - basePierce);
    armorFactor = Math.max(0.04, 1 - effectiveReduction);

    // Stat neglect penalty on Floors 4-9
    if (floorId >= 4 && pen < floorId * 8) {
      armorFactor *= 0.5;
    }
  }

  // 6. Stance Weaving (Combo Chuyển Thế)
  let stanceMult = stanceCfg.damageMult;
  if (input.stanceWeave) {
    const prevCfg = HAMMER_STANCES[input.stanceWeave.previousStance];
    stanceMult += (prevCfg.damageMult - 1.0) * 0.5;
  }

  const effectiveBasePower = input.basePower + (arsenal ? arsenal.flatDamage : 0) + Math.round(pen * 0.2);
  const forgerRankMult = input.forgerRankMultiplier ?? 1.0;

  // 7. Final Damage Equation
  const rawDamage =
    effectiveBasePower *
    timingMult *
    thermalMult *
    critMult *
    overdriveMult *
    globalBurstMult *
    forgerRankMult *
    input.spiritBonusMult *
    stanceMult *
    armorFactor;

  const finalDamage = Math.max(isGolden ? 3 : 1, Math.round(rawDamage));

  // 8. Loot & Drops
  const baseLinhThach = isGolden || isCrit ? 4 : isGreat ? 2 : 1;
  const extraLTDrops = arsenal ? arsenal.dropLinhThachBonus : 0;
  const linhThachEarned = Math.round(
    (baseLinhThach + extraLTDrops) * (isOverdriveNow ? 2 : 1) * (stanceBonuses?.linhThachMult ?? 1.0)
  );

  const tinhHoaChance = (isGolden || isCrit ? 0.20 : 0.08) * (stanceBonuses?.essenceDropMult ?? 1.0);
  const tinhHoaEarned = Math.random() < tinhHoaChance ? 1 : 0;

  // Heat & Resonance
  const extraHeat = (arsenal ? arsenal.heatPerHitBonus : 0) + (stanceBonuses?.heatGainAdd ?? 0);
  const heatGain = (isGolden ? 25 : 12) + extraHeat;

  let baseResonance = input.stance === 'E' ? 2 : 1;
  if ((arsenal?.setCounts.set_gravity ?? 0) >= 2) baseResonance += 1;
  const resonanceGain = Math.round(baseResonance + (arsenal ? arsenal.resonanceBonus : 0));

  const displayMultiplier = Number(
    (timingMult * (isOverdriveNow ? 2 : 1) * (isCrit ? 2 : 1) * (isGlancingHit ? 0.65 : 1)).toFixed(1)
  );

  return {
    damage: finalDamage,
    displayMultiplier,
    nextCombo,
    nextOverdriveCharge,
    triggeredOverdrive,
    heatGain,
    resonanceGain,
    linhThachEarned,
    tinhHoaEarned,
    isCrit,
    isGolden,
    isGlancingHit,
    effectivePiercePct: Math.round(basePierce * 100),
  };
}

"""

c = c[:s_strike] + new_strike_block + c[e_strike:]
print("3. Đã cập nhật calculateStrikeOutcome!")

# 5. Cập nhật INITIAL_UPGRADES (Cấp 1-100) & checkForgeEquilibrium
old_upgrades_start = "export const INITIAL_UPGRADES: ForgeUpgrade[] = ["
old_upgrades_end = "export function calculateBasePower(upgrades: ForgeUpgrade[]): number {"

s_upg = c.find(old_upgrades_start)
e_upg = c.find(old_upgrades_end)

new_upgrades_block = """export const INITIAL_UPGRADES: ForgeUpgrade[] = [
  {
    id: 'celestial_hammer_core',
    name: 'Búa Rèn Thiên Cương',
    subtitle: 'Tăng Lực Chùy (STR) & Sát Thương Gốc (Cấp 1-100)',
    level: 1,
    maxLevel: 100,
    baseCost: 10,
    costScale: 1.18,
    powerPerLevel: 1,
  },
  {
    id: 'thunder_quench_oil',
    name: 'Dầu Tôi Lôi Đình',
    subtitle: 'Tăng Phá Phách (PEN) & Xuyên Giáp Trực Tiếp (Cấp 1-100)',
    level: 0,
    maxLevel: 100,
    baseCost: 20,
    costScale: 1.20,
    powerPerLevel: 1,
  },
  {
    id: 'nine_heavens_bellows',
    name: 'Ống Bễ Cửu Trọng',
    subtitle: 'Tăng Nhiệt Lực (INT) & Hỏa Hầu Tối Đa (Cấp 1-100)',
    level: 0,
    maxLevel: 100,
    baseCost: 35,
    costScale: 1.22,
    powerPerLevel: 1,
  },
  {
    id: 'ancient_anvil_rune',
    name: 'Cổ Văn Mặt Đe',
    subtitle: 'Tăng Phá Giáp, Linh Thạch & Chống Dội Búa (Cấp 1-100)',
    level: 0,
    maxLevel: 100,
    baseCost: 50,
    costScale: 1.25,
    powerPerLevel: 1,
  },
];

export function getUpgradeCost(upgrade: ForgeUpgrade): number {
  if (upgrade.id === 'celestial_hammer_core') {
    return getForgeUpgradeCost(upgrade.level, 1.0);
  }
  return Math.round(upgrade.baseCost * Math.pow(upgrade.costScale, upgrade.level));
}

export function checkForgeEquilibrium(
  upgrades: ForgeUpgrade[],
  targetUpgradeId: string
): { allowed: boolean; minLevel: number; maxLevel: number; maxAllowedLevel: number; reason?: string } {
  const currentLevels = upgrades.map((u) => u.level);
  const minLevel = Math.min(...currentLevels);
  const target = upgrades.find((u) => u.id === targetUpgradeId);
  if (!target) return { allowed: false, minLevel, maxLevel: minLevel, maxAllowedLevel: minLevel + 15 };

  const nextLevel = target.level + 1;
  const maxAllowedLevel = minLevel + 15;
  if (nextLevel > maxAllowedLevel) {
    return {
      allowed: false,
      minLevel,
      maxLevel: Math.max(...currentLevels),
      maxAllowedLevel,
      reason: `Ràng buộc Đồng Bộ Lò Rèn: Cấp cao nhất không được vượt quá cấp thấp nhất (Cấp ${minLevel}) quá 15 cấp! Hãy nâng cấp các hạng mục khác để giữ cân bằng lò rèn.`,
    };
  }
  return { allowed: true, minLevel, maxLevel: Math.max(...currentLevels), maxAllowedLevel };
}

"""

c = c[:s_upg] + new_upgrades_block + c[e_upg:]
print("4. Đã cập nhật INITIAL_UPGRADES & checkForgeEquilibrium!")

# 6. Cập nhật FORGER_RANKS (10 Bậc Danh Hiệu)
old_ranks_start = "export const FORGER_RANKS: ForgerRank[] = ["
old_ranks_end = "export function getForgerRank(totalDamage: number): ForgerRank {"

s_rnk = c.find(old_ranks_start)
e_rnk = c.find(old_ranks_end)

new_ranks_block = """export const FORGER_RANKS: ForgerRank[] = [
  {
    id: 'rank_1',
    tier: 1,
    title: 'Tân Thủ Thợ Rèn (Apprentice)',
    badge: '🔨',
    damageRequired: 0,
    bonusDesc: 'Tân thủ khai lò tại thung lũng Thiên Thai.',
    damageMultiplier: 1.0,
    essenceBonusPct: 0,
    synergyRateBonusPct: 0,
  },
  {
    id: 'rank_2',
    tier: 2,
    title: 'Thợ Rèn Tập Sự (Furnace Smith)',
    badge: '🔥',
    damageRequired: 10_000,
    bonusDesc: 'Tăng vĩnh viễn +5% Sát thương & +10% Tinh Hoa rơi.',
    damageMultiplier: 1.05,
    essenceBonusPct: 10,
    synergyRateBonusPct: 5,
  },
  {
    id: 'rank_3',
    tier: 3,
    title: 'Thợ Rèn Chuyên Nghiệp (Ancient Forger)',
    badge: '⚡',
    damageRequired: 100_000,
    bonusDesc: 'Tăng vĩnh viễn +12% Sát thương & mở khóa Kỹ Pháp Tầng 4 & 5.',
    damageMultiplier: 1.12,
    essenceBonusPct: 25,
    synergyRateBonusPct: 15,
  },
  {
    id: 'rank_4',
    tier: 4,
    title: 'Tông Sư Phá Thiên (Heaven Breaker Master)',
    badge: '👑',
    damageRequired: 1_000_000,
    bonusDesc: 'Được tạc tượng đá. Tăng vĩnh viễn +25% Sát thương & +50% Tốc độ nạp Cực Nhịp!',
    damageMultiplier: 1.25,
    essenceBonusPct: 50,
    synergyRateBonusPct: 50,
  },
  {
    id: 'rank_5',
    tier: 5,
    title: 'Đại Tông Sư Luyện Khí (Grand Artificer)',
    badge: '🌟',
    damageRequired: 10_000_000,
    bonusDesc: 'Tăng vĩnh viễn +45% Sát thương & mở Ô Khảm Tinh Thể Bậc 1.',
    damageMultiplier: 1.45,
    essenceBonusPct: 75,
    synergyRateBonusPct: 70,
  },
  {
    id: 'rank_6',
    tier: 6,
    title: 'Thần Tượng Chưởng Lò (Furnace Sovereign)',
    badge: '⚔️',
    damageRequired: 50_000_000,
    bonusDesc: 'Tăng vĩnh viễn +75% Sát thương & +2 Điểm Phá Giáp mỗi nhát gõ.',
    damageMultiplier: 1.75,
    essenceBonusPct: 100,
    synergyRateBonusPct: 90,
  },
  {
    id: 'rank_7',
    tier: 7,
    title: 'Thiên Công Khai Vật (Celestial Artificer)',
    badge: '🌌',
    damageRequired: 250_000_000,
    bonusDesc: 'Tăng vĩnh viễn +120% Sát thương & mở khóa Thiên Phú Đa Thế (Cross-Stance).',
    damageMultiplier: 2.2,
    essenceBonusPct: 150,
    synergyRateBonusPct: 120,
  },
  {
    id: 'rank_8',
    tier: 8,
    title: 'Chí Tôn Đúc Thần (Divine Forge Paragon)',
    badge: '💎',
    damageRequired: 1_000_000_000,
    bonusDesc: 'Tăng vĩnh viễn +180% Sát thương & bỏ qua 15% Kháng Giảm Sát Thương của Cổ Thần.',
    damageMultiplier: 2.8,
    essenceBonusPct: 200,
    synergyRateBonusPct: 160,
  },
  {
    id: 'rank_9',
    tier: 9,
    title: 'Vạn Cổ Phá Trời (Eternal Skybreaker)',
    badge: '🪐',
    damageRequired: 5_000_000_000,
    bonusDesc: 'Tăng vĩnh viễn +280% Sát thương & kích hoạt Hào Quang Bất Diệt toàn server.',
    damageMultiplier: 3.8,
    essenceBonusPct: 300,
    synergyRateBonusPct: 220,
  },
  {
    id: 'rank_10',
    tier: 10,
    title: 'Hỗn Độn Khai Thiên (Chaos Primordial)',
    badge: '🔱',
    damageRequired: 10_000_000_000,
    bonusDesc: 'Đỉnh phong tạo hóa. Tăng vĩnh viễn +450% Sát thương & mở khóa Chuyển Sinh Thợ Rèn.',
    damageMultiplier: 5.5,
    essenceBonusPct: 500,
    synergyRateBonusPct: 300,
  },
];

"""

c = c[:s_rnk] + new_ranks_block + c[e_rnk:]
print("5. Đã cập nhật FORGER_RANKS 10 bậc!")

with open(r'd:\tieu-thuyet\frontend\src\game\rules.ts', 'w', encoding='utf-8') as f:
    f.write(c)

print("Toàn bộ cập nhật rules.ts đã thành công rực rỡ!")
