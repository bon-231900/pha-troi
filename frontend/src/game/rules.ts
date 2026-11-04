export type StanceKey = 'Q' | 'W' | 'E' | 'R';
export type DivineStanceId = 'THUNDER' | 'FIRE' | 'GRAVITY' | 'MYSTIC';

export type JudgmentGrade = 'PERFECT' | 'GREAT' | 'MISS';

export interface HammerStance {
  key: StanceKey;
  stanceId: DivineStanceId;
  name: string;
  title: string;
  role: string;
  color: string;
  secondaryColor: string;
  damageMult: number;
  shieldMult: number;
  synergyMult: number;
  resourceMult: number;
}

export const HAMMER_STANCES: Record<StanceKey, HammerStance> = {
  Q: {
    key: 'Q',
    stanceId: 'THUNDER',
    name: 'Lôi Đỉnh',
    title: 'Thiên Lôi Tốc Kích',
    role: 'Tia sét xanh neon · Sát thương Lôi x1.45',
    color: '#00F0FF',
    secondaryColor: '#0099FF',
    damageMult: 1.45,
    shieldMult: 1.1,
    synergyMult: 1.15,
    resourceMult: 1.1,
  },
  W: {
    key: 'W',
    stanceId: 'FIRE',
    name: 'Viêm Dương',
    title: 'Thiên Hỏa Phần Thiên',
    role: 'Khói lửa đỏ cam · Thiêu đốt HP x1.65',
    color: '#FF3B30',
    secondaryColor: '#FF6B00',
    damageMult: 1.65,
    shieldMult: 0.9,
    synergyMult: 1.0,
    resourceMult: 1.0,
  },
  E: {
    key: 'E',
    stanceId: 'GRAVITY',
    name: 'Trọng Lực',
    title: 'Tử Tinh Phá Giáp',
    role: 'Hào quang tím chấn địa · Phá Giáp x2.5',
    color: '#A855F7',
    secondaryColor: '#7E22CE',
    damageMult: 1.25,
    shieldMult: 2.5,
    synergyMult: 1.2,
    resourceMult: 1.15,
  },
  R: {
    key: 'R',
    stanceId: 'MYSTIC',
    name: 'Huyền Âm',
    title: 'Ngọc Bích Cộng Hưởng',
    role: 'Sóng âm ngọc bích · Tích Cực Nhịp x2.2',
    color: '#10B981',
    secondaryColor: '#2DD4BF',
    damageMult: 1.2,
    shieldMult: 1.25,
    synergyMult: 2.2,
    resourceMult: 1.8,
  },
};

export const STANCE_KEY_BY_ID: Record<DivineStanceId, StanceKey> = {
  THUNDER: 'Q',
  FIRE: 'W',
  GRAVITY: 'E',
  MYSTIC: 'R',
};

export const FORGE_BPM = 100;
export const TARGET_RIM_PROGRESS = 0.78;
export const PERFECT_TOLERANCE = 0.095;
export const GREAT_TOLERANCE = 0.22;
export const OVERDRIVE_MAX = 8;

export const HAMMER_IDLE_ANGLE_RAD = Math.PI / 4; // 45 degrees above anvil
export const HAMMER_DOWNSTROKE_SEC = 0.08; // 0.08s fast slam down to perpendicular (0 rad)
export const HAMMER_REBOUND_SEC = 0.24; // Smooth sine rebound back to 45 deg

/**
 * Computes the Divine Hammer angle (in radians) during a strike animation:
 * - Idle (elapsed < 0 or elapsed >= 0.32s): 45 deg (Math.PI / 4)
 * - Downstroke (0 <= elapsed <= 0.08s): interpolates smoothly from 45 deg down to 0 rad (perpendicular to anvil face)
 * - Rebound (0.08s < elapsed <= 0.32s): rebounds smoothly from 0 rad back to 45 deg with slight overshoot
 */
export function computeHammerStrikeAngle(elapsedStrikeSec: number, idleTimeSec: number = 0): number {
  const idleBob = Math.sin(idleTimeSec * 2.8) * 0.045;
  if (elapsedStrikeSec < 0 || elapsedStrikeSec >= HAMMER_DOWNSTROKE_SEC + HAMMER_REBOUND_SEC) {
    return HAMMER_IDLE_ANGLE_RAD + idleBob;
  }

  if (elapsedStrikeSec <= HAMMER_DOWNSTROKE_SEC) {
    // 0.08s downstroke using smooth sine ease-in-out from 45 deg -> 0 rad
    const t = elapsedStrikeSec / HAMMER_DOWNSTROKE_SEC;
    const s = Math.sin((t * Math.PI) / 2);
    return HAMMER_IDLE_ANGLE_RAD * (1 - s);
  }

  // Rebound phase from 0 rad back to 45 deg
  const r = (elapsedStrikeSec - HAMMER_DOWNSTROKE_SEC) / HAMMER_REBOUND_SEC;
  const reboundCurve = Math.sin((r * Math.PI) / 2) + Math.sin(r * Math.PI) * 0.08;
  return HAMMER_IDLE_ANGLE_RAD * Math.min(1.08, reboundCurve);
}

/**
 * Converts BPM (100 BPM = 1.6667 beats/sec) into normalized radial wave contraction speed.
 * Each full wave cycle spans 2 beats so the contracting halo feels readable and weighty at 100 BPM.
 */
export function getBpmWaveSpeed(bpm: number = FORGE_BPM): number {
  return bpm / 60 / 2; // 0.8333 cycles per second (1.2s per full contraction, 0.6s per beat)
}

export interface JudgmentResult {
  grade: JudgmentGrade;
  labelVn: string;
  multiplier: number;
  delta: number;
  isEarly: boolean;
}

/**
 * Evaluates wave progress (0 = outer spawn, 1 = anvil center)
 * against TARGET_RIM_PROGRESS (0.78 = golden anvil rim).
 */
export function judgeRhythmWave(progress: number): JudgmentResult {
  const clamped = Math.max(0, Math.min(1, progress));
  const diff = clamped - TARGET_RIM_PROGRESS;
  const absDiff = Math.abs(diff);

  if (absDiff <= PERFECT_TOLERANCE) {
    return {
      grade: 'PERFECT',
      labelVn: 'HOÀNG KIM',
      multiplier: 3.5,
      delta: diff,
      isEarly: diff < 0,
    };
  }

  if (absDiff <= GREAT_TOLERANCE) {
    return {
      grade: 'GREAT',
      labelVn: 'CHUẨN XÁC',
      multiplier: 1.5,
      delta: diff,
      isEarly: diff < 0,
    };
  }

  return {
    grade: 'MISS',
    labelVn: 'TRƯỢT NHỊP',
    multiplier: 0,
    delta: diff,
    isEarly: diff < 0,
  };
}

// ============================================================================
// BALANCE OVERHAUL: DE-INFLATION RPG BASELINE & COMMUNITY RAID MODEL
// ============================================================================
export const BOSS_FLOOR_1_MAX_HP = 1_500_000_000; // 1.5 Tỷ HP (Vòm Trời Thiết Vân - Tầng 1 · World Raid Edition)
export const BOSS_FLOOR_NAME = 'Vòm Trời Thiết Vân · Tầng 1';

export const RESONANCE_MAX_STRIKES = 50; // Tích 50 nhát -> Vỡ giáp 30s
export const SHIELD_BREAK_DURATION_SEC = 30; // 30s phá giáp

export const MIN_ANVIL_HEAT = 100; // 100°C base
export const MAX_ANVIL_HEAT = 1000; // 1000°C max
export const HEAT_DECAY_PER_SEC = 5; // -5°C per second idle decay

export interface AtmosphericSealLayer {
  id: number;
  name: string;
  shortName: string;
  minHpRatio: number; // e.g. 0.75
  maxHpRatio: number; // 1.0
  damageReductionPct: number; // 80 -> damage taken = 20%
  description: string;
}

export const ATMOSPHERIC_SEAL_LAYERS: AtmosphericSealLayer[] = [
  {
    id: 1,
    name: 'LỚP 1: THIẾT BÌ',
    shortName: 'Thiết Bì',
    minHpRatio: 0.75,
    maxHpRatio: 1.0,
    damageReductionPct: 80,
    description: 'Vỏ sắt nguội dày đặc phong tỏa · Giảm 80% DMG',
  },
  {
    id: 2,
    name: 'LỚP 2: CƯƠNG CỐT',
    shortName: 'Cương Cốt',
    minHpRatio: 0.5,
    maxHpRatio: 0.75,
    damageReductionPct: 60,
    description: 'Khung thiên cương cứng rắn · Giảm 60% DMG',
  },
  {
    id: 3,
    name: 'LỚP 3: LÔI HỎA TÂM',
    shortName: 'Lôi Hỏa Tâm',
    minHpRatio: 0.25,
    maxHpRatio: 0.5,
    damageReductionPct: 40,
    description: 'Lõi bão lôi hỏa bùng phát · Giảm 40% DMG',
  },
  {
    id: 4,
    name: 'LỚP 4: NGHỊCH CẢNH',
    shortName: 'Nghịch Cảnh',
    minHpRatio: 0.0,
    maxHpRatio: 0.25,
    damageReductionPct: 0,
    description: 'Vòm trời sụp đổ · Giáp 0% · Cuồng Bạo',
  },
];

export function getAtmosphericSealLayer(
  currentHp: number,
  maxHp: number = BOSS_FLOOR_1_MAX_HP
): AtmosphericSealLayer {
  const ratio = Math.max(0, Math.min(1, currentHp / Math.max(1, maxHp)));
  for (const layer of ATMOSPHERIC_SEAL_LAYERS) {
    if (ratio > layer.minHpRatio || (layer.minHpRatio === 0 && ratio >= 0)) {
      return layer;
    }
  }
  return ATMOSPHERIC_SEAL_LAYERS[ATMOSPHERIC_SEAL_LAYERS.length - 1];
}

export interface ContributionTier {
  id: string;
  title: string;
  damageRequired: number;
  rewardLinhThach: number;
  rewardTinhHoa: number;
  perkDescription: string;
  badge: string;
}

export const CONTRIBUTION_TIERS: ContributionTier[] = [
  {
    id: 'tier_1',
    title: 'Thợ Rèn Tập Sự',
    damageRequired: 1_000,
    rewardLinhThach: 100,
    rewardTinhHoa: 1,
    perkDescription: 'Nhận 100 Linh Thạch & 1 Tinh Hoa Thần Hồn',
    badge: '🥉',
  },
  {
    id: 'tier_2',
    title: 'Búa Sắt Rực Lửa',
    damageRequired: 10_000,
    rewardLinhThach: 500,
    rewardTinhHoa: 3,
    perkDescription: 'Tăng vĩnh viễn +5% tốc độ tích Overdrive',
    badge: '🥈',
  },
  {
    id: 'tier_3',
    title: 'Rương Tinh Thể Thiên Cẩm',
    damageRequired: 100_000,
    rewardLinhThach: 2_500,
    rewardTinhHoa: 8,
    perkDescription: 'Mở khóa nhánh kỹ năng Thần Hồn bậc 2',
    badge: '🥇',
  },
  {
    id: 'tier_4',
    title: 'Tông Sư Phá Thiên',
    damageRequired: 1_000_000,
    rewardLinhThach: 10_000,
    rewardTinhHoa: 20,
    perkDescription: 'Danh hiệu Tông Sư · Tăng vĩnh viễn +20% sát thương',
    badge: '👑',
  },
];

/**
 * Calculates base hammer damage based on Forge Level L:
 * L=1: 1 DMG
 * L=5: 4 DMG
 * L=10: 12 DMG
 * L=20: 35 DMG
 * L=25: 50 DMG
 */
export function calculateForgeDamage(level: number): number {
  if (level <= 1) return 1;
  if (level <= 5) return Math.round(1 + (level - 1) * 0.75); // Lv1=1, Lv5=4
  if (level <= 10) return Math.round(4 + (level - 5) * 1.6); // Lv10=12
  if (level <= 20) return Math.round(12 + (level - 10) * 2.3); // Lv20=35
  if (level <= 25) return Math.round(35 + (level - 20) * 3.0); // Lv25=50
  return Math.round(50 + (level - 25) * 4.4); // Beyond Lv25
}

/**
 * Calculates upgrade cost according to: Cost(L) = round(10 * L^1.35)
 * L=1: 10 LT
 * L=2: 25 LT
 * L=5: 88 LT
 * L=10: 224 LT
 * L=20: 568 LT
 */
export function getForgeUpgradeCost(level: number, baseMultiplier: number = 1.0): number {
  const safeL = Math.max(1, level);
  return Math.max(10, Math.round(10 * Math.pow(safeL, 1.35) * baseMultiplier));
}

// ============================================================================
// ARPG LOOT SYSTEM: 6-SLOT ARSENAL, PREFIXES, SUFFIXES & PROCEDURAL DROPS
// ============================================================================
export type EquipmentSlotKey = 'hammer' | 'anvil' | 'bellows' | 'gauntlets' | 'apron' | 'relic';

export type ItemTier = 'tier_e' | 'tier_d' | 'tier_c' | 'tier_b' | 'tier_a' | 'tier_s';
export type ItemRarity = 'common' | 'uncommon' | 'rare' | 'epic' | 'legendary' | 'mythic' | ItemTier;

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
  magicFindPct: number;
}

export const SLOT_INFO: Record<EquipmentSlotKey, { name: string; icon: string; statLabel: string; statUnit: string }> = {
  hammer: { name: 'Thần Chùy', icon: 'Hammer', statLabel: 'Sát Thương Cơ Bản', statUnit: 'DMG' },
  anvil: { name: 'Thần Đe', icon: 'Shield', statLabel: 'Vùng Hoàng Kim', statUnit: 'ms' },
  bellows: { name: 'Hỏa Lò', icon: 'Flame', statLabel: 'Tích Nhiệt Đe', statUnit: '°C/hit' },
  gauntlets: { name: 'Bao Tay Rèn', icon: 'Zap', statLabel: 'Tỷ Lệ Bạo Kích', statUnit: '%' },
  apron: { name: 'Tạp Dề Thiết Hộ', icon: 'Layers', statLabel: 'Linh Thạch Treo Máy', statUnit: 'LT/phút' },
  relic: { name: 'Định Thiên Pháp Bảo', icon: 'Sparkles', statLabel: 'Sát Thương Toàn Thể', statUnit: '%' },
};

interface BaseItemDef {
  name: string;
  baseValue: number;
  lore: string;
  minRarity: ItemRarity;
}

const BASE_ITEM_POOL: Record<EquipmentSlotKey, BaseItemDef[]> = {
  hammer: [
    { name: 'Búa Sắt Thiên Thai', baseValue: 2, lore: 'Búa sắt thô sơ từ thuở đầu khai lò phá trời.', minRarity: 'common' },
    { name: 'Búa Tinh Thiết', baseValue: 3, lore: 'Rèn từ tinh thiết luyện kỹ lưỡng qua trăm lần nung.', minRarity: 'uncommon' },
    { name: 'Búa Thiên Cương', baseValue: 5, lore: 'Đúc từ hợp kim thiên thạch, chùy nặng ngàn cân.', minRarity: 'rare' },
    { name: 'Chùy Hắc Diệm', baseValue: 10, lore: 'Lửa đen Cửu U cháy mãi trên đầu búa.', minRarity: 'epic' },
    { name: 'Thần Chùy Lôi Đình', baseValue: 18, lore: 'Mỗi nhát giáng xuống triệu hồi thiên lôi xé toạc màn đêm.', minRarity: 'legendary' },
    { name: 'Khai Thiên Thần Chùy', baseValue: 32, lore: 'Bảo vật thời Nữ Oa, từng đập vỡ xiềng xích cổ thần.', minRarity: 'mythic' },
  ],
  anvil: [
    { name: 'Đe Thép Cổ Vân', baseValue: 6, lore: 'Mặt đe tôi qua sương mây ngàn năm.', minRarity: 'common' },
    { name: 'Đe Tinh Cương', baseValue: 9, lore: 'Đe tinh luyện tăng độ đanh và nhạy bén khi nện búa.', minRarity: 'uncommon' },
    { name: 'Đe Trọng Lực', baseValue: 12, lore: 'Hút linh khí đất mẹ, giữ phôi thép vững như thái sơn.', minRarity: 'rare' },
    { name: 'Đe Huyền Thiết', baseValue: 18, lore: 'Rung động cộng hưởng vang dội khắp đại công trường.', minRarity: 'epic' },
    { name: 'Thần Đe Cửu Trọng', baseValue: 26, lore: 'Âm vang như chuông đồng thức tỉnh vạn linh.', minRarity: 'legendary' },
    { name: 'Thái Hư Bất Diệt Đe', baseValue: 36, lore: 'Vĩnh viễn không sứt mẻ trước mọi cuồng phong vũ bão.', minRarity: 'mythic' },
  ],
  bellows: [
    { name: 'Ống Bễ Da Hổ Lôi', baseValue: 3, lore: 'May từ da hổ sấm, mỗi nhịp thổi bùng ngọn lửa đỏ.', minRarity: 'common' },
    { name: 'Ống Bễ Da Hổ Tinh', baseValue: 4, lore: 'Ống bễ cải tiến đẩy luồng phong hỏa đều đặn vào lòng lò.', minRarity: 'uncommon' },
    { name: 'Ống Bễ Hỏa Phụng', baseValue: 6, lore: 'Lông vũ hỏa phụng giữ nhiệt lò không bao giờ tắt.', minRarity: 'rare' },
    { name: 'Ống Bễ Hỗn Độn', baseValue: 10, lore: 'Hút gió tám phương thổi vào tâm đe.', minRarity: 'epic' },
    { name: 'Cửu Thiên Liệt Hỏa Bễ', baseValue: 15, lore: 'Biến mặt đe thành dung nham cuồn cuộn.', minRarity: 'legendary' },
    { name: 'Thần Phong Hỏa Lò', baseValue: 22, lore: 'Gió thần khai thiên lập địa hun đúc vạn khí.', minRarity: 'mythic' },
  ],
  gauntlets: [
    { name: 'Bao Tay Da Thô', baseValue: 5, lore: 'Che chắn lòng bàn tay khỏi tàn tro rực lửa.', minRarity: 'common' },
    { name: 'Bao Tay Tinh Bì', baseValue: 7, lore: 'Gia cố khớp ngón tay linh hoạt hơn khi chuyển thế.', minRarity: 'uncommon' },
    { name: 'Bao Tay Thiết Giáp', baseValue: 9, lore: 'Lót vảy sắt dẻo dai, giữ chặt cán búa không trượt.', minRarity: 'rare' },
    { name: 'Bao Tay Vảy Rồng', baseValue: 14, lore: 'Vuốt rồng uốn lượn, tăng sức bộc phát trong gang tấc.', minRarity: 'epic' },
    { name: 'Lôi Thần Thiết Chưởng', baseValue: 20, lore: 'Tia chớp xanh neon nhảy múa trên từng đầu ngón tay.', minRarity: 'legendary' },
    { name: 'Chưởng Thiên Thần Giáp', baseValue: 28, lore: 'Cầm nắm càn khôn, nhát búa nào cũng như sấm rền.', minRarity: 'mythic' },
  ],
  apron: [
    { name: 'Tạp Dề Bì Hộ', baseValue: 15, lore: 'Tạp dề da dày dặn chống tia lửa bén.', minRarity: 'common' },
    { name: 'Tạp Dề Tinh Thiết', baseValue: 25, lore: 'Lót giáp sắt gia công bảo hộ thợ rèn kiên cố.', minRarity: 'uncommon' },
    { name: 'Tạp Dề Bách Luyện', baseValue: 35, lore: 'Lớp giáp gai hấp thu phản chấn từ vòm trời.', minRarity: 'rare' },
    { name: 'Tạp Dề Long Lân', baseValue: 65, lore: 'Linh khí tự tuần hoàn sinh sôi tài nguyên ngay khi nghỉ tay.', minRarity: 'epic' },
    { name: 'Huyền Minh Thiết Hộ', baseValue: 100, lore: 'Băng hỏa bất xâm, bảo bọc linh hồn thợ rèn.', minRarity: 'legendary' },
    { name: 'Thiên Cương Bất Hoại Y', baseValue: 160, lore: 'Giáp trụ bất diệt trước uy áp của Cổ Thần Cửu U.', minRarity: 'mythic' },
  ],
  relic: [
    { name: 'Thạch Bàn Đông Sơn', baseValue: 6, lore: 'Khắc họa cổ văn người Việt cổ hướng về trời cao.', minRarity: 'common' },
    { name: 'Thạch Phiến Lạc Việt', baseValue: 10, lore: 'Mảnh đá hoa văn hộ mệnh tăng cường linh cảm.', minRarity: 'uncommon' },
    { name: 'Ấn Lạc Thần', baseValue: 14, lore: 'Hào quang bảo hộ gia tăng sĩ khí toàn công trường.', minRarity: 'rare' },
    { name: 'Kính Cửu U', baseValue: 22, lore: 'Phản chiếu điểm yếu nhất trên giáp Thiên Ma.', minRarity: 'epic' },
    { name: 'Bát Quái Định Thiên Bàn', baseValue: 32, lore: 'Xoay chuyển càn khôn, hội tụ sức mạnh vạn dân.', minRarity: 'legendary' },
    { name: 'Khai Thiên Ngọc Tỷ', baseValue: 48, lore: 'Thần vật lập lại trật tự cõi hồng hoang.', minRarity: 'mythic' },
  ],
};

interface AffixDef {
  name: string;
  statKey: ItemAffix['statKey'];
  labelTemplate: (val: number) => string;
  minVal: number;
  maxVal: number;
  weight: number;
}

const PREFIX_POOL: AffixDef[] = [
  { name: 'Sắc Bén', statKey: 'flatDamage', minVal: 1, maxVal: 5, weight: 10, labelTemplate: (v) => `+${v} Sát thương cơ bản` },
  { name: 'Cuồng Nộ', statKey: 'damageMultiplier', minVal: 0.05, maxVal: 0.25, weight: 8, labelTemplate: (v) => `+${Math.round(v * 100)}% Tổng sát thương` },
  { name: 'Lôi Điện', statKey: 'critChancePct', minVal: 3, maxVal: 10, weight: 8, labelTemplate: (v) => `+${v}% Tỷ lệ Bạo Kích` },
  { name: 'Xích Diễm', statKey: 'heatGainPerHit', minVal: 2, maxVal: 7, weight: 8, labelTemplate: (v) => `+${v} °C/hit Hỏa Hầu` },
  { name: 'Trầm Trọng', statKey: 'resonanceBonus', minVal: 1, maxVal: 2, weight: 7, labelTemplate: (v) => `+${v} Điểm Phá Giáp / nhát` },
  { name: 'Huyền Ảo', statKey: 'perfectWindowMs', minVal: 5, maxVal: 18, weight: 8, labelTemplate: (v) => `+${v} ms Cửa sổ Hoàng Kim` },
  { name: 'Kim Cang', statKey: 'heatDecayReductionPct', minVal: 10, maxVal: 30, weight: 7, labelTemplate: (v) => `Giảm ${v}% tốc độ nguội đe` },
  { name: 'Hoàng Kim', statKey: 'linhThachPerHit', minVal: 1, maxVal: 3, weight: 9, labelTemplate: (v) => `+${v} Linh Thạch mỗi nhát` },
  { name: 'Thiên Mệnh', statKey: 'damageMultiplier', minVal: 0.2, maxVal: 0.45, weight: 3, labelTemplate: (v) => `+${Math.round(v * 100)}% Công phá Thiên Mệnh` },
];

const SUFFIX_POOL: AffixDef[] = [
  { name: 'chi Bạo Kích', statKey: 'critChancePct', minVal: 4, maxVal: 12, weight: 10, labelTemplate: (v) => `+${v}% Tỷ lệ Bạo Kích` },
  { name: 'chi Hỏa Hầu', statKey: 'heatDecayReductionPct', minVal: 15, maxVal: 35, weight: 8, labelTemplate: (v) => `Giảm ${v}% nguội đe rèn` },
  { name: 'chi Phá Giáp', statKey: 'resonanceBonus', minVal: 1, maxVal: 3, weight: 8, labelTemplate: (v) => `+${v} Điểm Phá Giáp` },
  { name: 'chi Phong Nhịp', statKey: 'perfectWindowMs', minVal: 8, maxVal: 22, weight: 8, labelTemplate: (v) => `+${v} ms Dung sai nhịp gõ` },
  { name: 'chi Tài Phú', statKey: 'linhThachPerHit', minVal: 2, maxVal: 5, weight: 9, labelTemplate: (v) => `+${v} Linh Thạch rơi` },
  { name: 'chi Thần Hồn', statKey: 'essenceDropChancePct', minVal: 5, maxVal: 15, weight: 6, labelTemplate: (v) => `+${v}% Tỷ lệ nhặt Tinh Hoa` },
  { name: 'chi Cực Nhịp', statKey: 'synergyChargeBonusPct', minVal: 10, maxVal: 30, weight: 7, labelTemplate: (v) => `+${v}% Tốc độ nạp Cực Nhịp` },
  { name: 'chi Hư Không', statKey: 'damageMultiplier', minVal: 0.1, maxVal: 0.35, weight: 5, labelTemplate: (v) => `+${Math.round(v * 100)}% Sát thương Hư Không` },
];

function pickRandomWeighted<T extends { weight: number }>(items: T[]): T {
  const total = items.reduce((sum, item) => sum + item.weight, 0);
  let random = Math.random() * total;
  for (const item of items) {
    if (random < item.weight) return item;
    random -= item.weight;
  }
  return items[0];
}

export function generateProceduralItem(options?: {
  slotKey?: EquipmentSlotKey;
  minRarity?: ItemRarity;
  itemLevel?: number;
}): EquipmentItem {
  const slots: EquipmentSlotKey[] = ['hammer', 'anvil', 'bellows', 'gauntlets', 'apron', 'relic'];
  const slotKey = options?.slotKey || slots[Math.floor(Math.random() * slots.length)];
  const rarity = options?.minRarity || 'common';
  const itemLevel = options?.itemLevel || 1;

  // Pick suitable base item
  const basePool = BASE_ITEM_POOL[slotKey];
  const eligibleBases = basePool.filter((b) => {
    const rarityOrder: ItemRarity[] = ['common', 'rare', 'epic', 'legendary', 'mythic'];
    return rarityOrder.indexOf(b.minRarity) <= rarityOrder.indexOf(rarity);
  });
  const baseDef = eligibleBases[eligibleBases.length - 1] || basePool[0];

  // Number of prefixes & suffixes based on rarity
  let prefixCount = 0;
  let suffixCount = 0;

  switch (rarity) {
    case 'mythic':
      prefixCount = 2;
      suffixCount = 2;
      break;
    case 'legendary':
      prefixCount = 2;
      suffixCount = 2;
      break;
    case 'epic':
      prefixCount = Math.random() < 0.5 ? 2 : 1;
      suffixCount = 3 - prefixCount;
      break;
    case 'rare':
      prefixCount = 1;
      suffixCount = 1;
      break;
    default: // common
      if (Math.random() < 0.5) prefixCount = 1;
      else suffixCount = 1;
      break;
  }

  const prefixes: ItemAffix[] = [];
  const suffixes: ItemAffix[] = [];
  const usedPrefixes = new Set<string>();
  const usedSuffixes = new Set<string>();

  // Roll prefixes
  for (let i = 0; i < prefixCount; i++) {
    const available = PREFIX_POOL.filter((p) => !usedPrefixes.has(p.name));
    if (available.length === 0) break;
    const def = pickRandomWeighted(available);
    usedPrefixes.add(def.name);

    // Roll stat value based on rarity
    const rarityMult =
      rarity === 'mythic' ? 1.5 : rarity === 'legendary' ? 1.25 : rarity === 'epic' ? 1.1 : 1.0;
    const rawVal = def.minVal + Math.random() * (def.maxVal - def.minVal);
    const finalVal =
      def.statKey === 'damageMultiplier'
        ? Number((rawVal * rarityMult).toFixed(2))
        : Math.round(rawVal * rarityMult);

    prefixes.push({
      id: `p_${Date.now()}_${i}_${Math.random().toString(36).substring(2, 5)}`,
      type: 'prefix',
      name: def.name,
      label: def.labelTemplate(finalVal),
      statKey: def.statKey,
      value: finalVal,
    });
  }

  // Roll suffixes
  for (let i = 0; i < suffixCount; i++) {
    const available = SUFFIX_POOL.filter((s) => !usedSuffixes.has(s.name));
    if (available.length === 0) break;
    const def = pickRandomWeighted(available);
    usedSuffixes.add(def.name);

    const rarityMult =
      rarity === 'mythic' ? 1.5 : rarity === 'legendary' ? 1.25 : rarity === 'epic' ? 1.1 : 1.0;
    const rawVal = def.minVal + Math.random() * (def.maxVal - def.minVal);
    const finalVal =
      def.statKey === 'damageMultiplier'
        ? Number((rawVal * rarityMult).toFixed(2))
        : Math.round(rawVal * rarityMult);

    suffixes.push({
      id: `s_${Date.now()}_${i}_${Math.random().toString(36).substring(2, 5)}`,
      type: 'suffix',
      name: def.name,
      label: def.labelTemplate(finalVal),
      statKey: def.statKey,
      value: finalVal,
    });
  }

  // If mythic, add unique divine blessing
  if (rarity === 'mythic') {
    suffixes.push({
      id: `divine_${Date.now()}`,
      type: 'suffix',
      name: 'chi Nữ Oa Chúc Phúc',
      label: '+35% Sát thương Khai Thiên & +10% Bạo Kích',
      statKey: 'damageMultiplier',
      value: 0.35,
    });
  }

  // Build full procedurally generated name
  const prefixStr = prefixes.map((p) => p.name).join(' ');
  const suffixStr = suffixes.map((s) => s.name).join(' ');
  const fullItemName = [prefixStr, baseDef.name, suffixStr].filter(Boolean).join(' ');

  const slotMeta = SLOT_INFO[slotKey];

  const ret: EquipmentItem = {
    id: `item_${Date.now()}_${Math.random().toString(36).substring(2, 8)}`,
    slotKey,
    slotName: slotMeta.name,
    baseName: baseDef.name,
    name: fullItemName,
    rarity,
    itemLevel,
    baseStatLabel: slotMeta.statLabel,
    baseStatValue: baseDef.baseValue,
    baseStatUnit: slotMeta.statUnit,
    prefixes,
    suffixes,
    loreDescription: baseDef.lore,
    droppedAt: Date.now(),
    setId: (['set_thunder', 'set_fire', 'set_gravity', 'set_mystic'] as EquipmentSetId[])[Math.floor(Math.random() * 4)],
  };
  if (ret.setId) {
    ret.setName = EQUIPMENT_SETS[ret.setId].name;
  }
  return ret;
}

// ============================================================================
// MMORPG DROP SYSTEM: 6-TIER (E -> S) MATRICES, PITY COUNTERS & RAID CLEAR CHESTS
// ============================================================================
export interface FloorTierWeights {
  tierE: number;
  tierD: number;
  tierC: number;
  tierB: number;
  tierA: number;
  tierS: number;
}

export const FLOOR_TIER_DROP_WEIGHTS: Record<number, FloorTierWeights> = {
  1: { tierE: 62.0, tierD: 30.0, tierC: 7.20, tierB: 0.78, tierA: 0.02, tierS: 0.00 },
  2: { tierE: 48.0, tierD: 36.0, tierC: 13.5, tierB: 2.40, tierA: 0.10, tierS: 0.00 },
  3: { tierE: 35.0, tierD: 38.0, tierC: 21.0, tierB: 5.65, tierA: 0.34, tierS: 0.01 },
  4: { tierE: 24.0, tierD: 36.0, tierC: 28.5, tierB: 10.6, tierA: 0.87, tierS: 0.03 },
  5: { tierE: 15.0, tierD: 31.0, tierC: 34.0, tierB: 17.8, tierA: 2.12, tierS: 0.08 },
  6: { tierE: 8.0,  tierD: 25.0, tierC: 38.0, tierB: 24.5, tierA: 4.30, tierS: 0.20 },
  7: { tierE: 4.0,  tierD: 18.0, tierC: 39.0, tierB: 31.0, tierA: 7.55, tierS: 0.45 },
  8: { tierE: 1.5,  tierD: 11.5, tierC: 36.0, tierB: 37.5, tierA: 12.5, tierS: 1.00 },
  9: { tierE: 0.0,  tierD: 6.0,  tierC: 30.0, tierB: 43.0, tierA: 19.0, tierS: 2.00 },
};

export function pickTierFromWeights(weights: FloorTierWeights): ItemRarity {
  const roll = Math.random() * 100;
  let cum = 0;
  cum += weights.tierS;
  if (roll < cum) return 'mythic'; // Tier S
  cum += weights.tierA;
  if (roll < cum) return 'legendary'; // Tier A
  cum += weights.tierB;
  if (roll < cum) return 'epic'; // Tier B
  cum += weights.tierC;
  if (roll < cum) return 'rare'; // Tier C
  cum += weights.tierD;
  if (roll < cum) return 'uncommon'; // Tier D
  return 'common'; // Tier E
}

export interface RollLootDropOptions {
  grade: JudgmentGrade;
  isOverdrive?: boolean;
  isShieldBreak?: boolean;
  magicFindPct?: number;
  vaultFloorId?: number;
  anvilPityCount?: number;
}

export interface RollLootDropResult {
  item: EquipmentItem | null;
  newPityCount: number;
  isPityTriggered: boolean;
}

export function rollLootDrop(options: RollLootDropOptions): RollLootDropResult {
  const {
    grade,
    isOverdrive = false,
    isShieldBreak = false,
    magicFindPct = 0,
    vaultFloorId = 1,
    anvilPityCount = 0,
  } = options;

  if (grade === 'MISS') {
    return { item: null, newPityCount: anvilPityCount, isPityTriggered: false };
  }

  // Base Trigger Chances (Section 5.2):
  // Normal (GREAT): 0.40%, Perfect: 1.20%, Overdrive: 2.50%, Shield Break: 100%
  let triggerChance = 0.004;
  if (grade === 'PERFECT') triggerChance = 0.012;
  if (isOverdrive) triggerChance = Math.max(triggerChance, 0.025);
  if (isShieldBreak) triggerChance = 1.0;

  // Apply Magic Find from SPI (Soft capped at +50%)
  const mfMult = 1 + Math.min(50, Math.max(0, magicFindPct)) / 100;
  triggerChance = Math.min(1.0, triggerChance * mfMult);

  if (Math.random() > triggerChance) {
    return { item: null, newPityCount: anvilPityCount, isPityTriggered: false };
  }

  // A drop triggered! Now check Pity:
  let updatedPity = anvilPityCount + 1;
  let rolledRarity: ItemRarity = 'common';
  let isPityTriggered = false;

  if (updatedPity >= 200) {
    // 200 drops pity: Guaranteed Tier A (legendary)
    rolledRarity = 'legendary';
    updatedPity = 0;
    isPityTriggered = true;
  } else if (updatedPity >= 50 && Math.random() < 0.5) {
    // 50 drops pity: Guaranteed Tier B (epic)
    rolledRarity = 'epic';
    isPityTriggered = true;
  } else {
    const weights = FLOOR_TIER_DROP_WEIGHTS[vaultFloorId] || FLOOR_TIER_DROP_WEIGHTS[1];
    rolledRarity = pickTierFromWeights(weights);
  }

  // If Tier B, A, or S drops naturally, reset pity counter
  if (rolledRarity === 'mythic' || rolledRarity === 'legendary' || rolledRarity === 'epic') {
    updatedPity = 0;
  }

  const item = generateProceduralItem({ minRarity: rolledRarity, itemLevel: vaultFloorId });
  return { item, newPityCount: updatedPity, isPityTriggered };
}

// ============================================================================
// KÊNH DROP 2: RƯƠNG CHIẾN LỢI PHẨM THẾ GIỚI KHI PHÁ VÒM (WORLD RAID CLEAR CHESTS)
// ============================================================================
export type RaidChestRank = 'C' | 'B' | 'A' | 'S' | 'MVP';

export interface RaidChestReward {
  rank: RaidChestRank;
  rankTitle: string;
  items: EquipmentItem[];
  ironDustReward: number;
  celestialStarReward: number;
  raidPityGranted: number;
  guaranteedTierSTriggered: boolean;
}

export function openWorldRaidClearChest(options: {
  rank: RaidChestRank;
  vaultFloorId: number;
  raidPityCount: number;
  playerStance?: StanceKey;
}): RaidChestReward {
  const { rank, vaultFloorId, raidPityCount, playerStance = 'Q' } = options;

  let itemCount = 2;
  let rankTitle = 'Rương Đồng Tâm (Hạng C)';
  let raidPityGranted = 1;
  let ironDustReward = 50;
  let celestialStarReward = 0;

  if (rank === 'B') {
    itemCount = 3;
    rankTitle = 'Rương Tinh Anh (Hạng B)';
    ironDustReward = 150;
  } else if (rank === 'A') {
    itemCount = 4;
    rankTitle = 'Rương Hộ Pháp (Hạng A)';
    ironDustReward = 300;
  } else if (rank === 'S') {
    itemCount = 5;
    rankTitle = 'Rương Tông Sư (Hạng S)';
    raidPityGranted = 3;
    ironDustReward = 600;
    celestialStarReward = 1;
  } else if (rank === 'MVP') {
    itemCount = 6;
    rankTitle = 'Rương Thái Thượng (MVP)';
    raidPityGranted = 3;
    ironDustReward = 1200;
    celestialStarReward = 2;
  }

  const items: EquipmentItem[] = [];
  const totalPity = raidPityCount + raidPityGranted;
  let guaranteedTierSTriggered = false;

  // Check 50 Raid Seals Pity -> 100% Tier S Smart Loot
  if (totalPity >= 50) {
    guaranteedTierSTriggered = true;
    const smartSetId: EquipmentSetId =
      playerStance === 'W'
        ? 'set_fire'
        : playerStance === 'E'
        ? 'set_gravity'
        : playerStance === 'R'
        ? 'set_mystic'
        : 'set_thunder';

    const tierSItem = generateProceduralItem({
      minRarity: 'mythic',
      itemLevel: Math.max(vaultFloorId, 5),
    });
    tierSItem.setId = smartSetId;
    tierSItem.setName = EQUIPMENT_SETS[smartSetId].name;
    items.push(tierSItem);
  }

  const remaining = itemCount - items.length;
  for (let i = 0; i < remaining; i++) {
    let rarity: ItemRarity = 'rare';
    const roll = Math.random() * 100;
    if (rank === 'MVP' && i === 0) {
      rarity = roll < 18 ? 'mythic' : 'legendary';
    } else if (rank === 'S' && i === 0 && vaultFloorId >= 5) {
      rarity = roll < 10 ? 'mythic' : 'legendary';
    } else if (rank === 'A' && i === 0) {
      rarity = roll < 4 ? 'mythic' : roll < 45 ? 'legendary' : 'epic';
    } else {
      const weights = FLOOR_TIER_DROP_WEIGHTS[vaultFloorId] || FLOOR_TIER_DROP_WEIGHTS[1];
      rarity = pickTierFromWeights(weights);
    }
    items.push(generateProceduralItem({ minRarity: rarity, itemLevel: vaultFloorId }));
  }

  return {
    rank,
    rankTitle,
    items,
    ironDustReward,
    celestialStarReward,
    raidPityGranted,
    guaranteedTierSTriggered,
  };
}

export function ascendEquipmentTier(item: EquipmentItem): EquipmentItem | null {
  const meta = getItemRarityMeta(item.rarity);
  if (meta.tier !== 'A') return null;

  const newBaseVal = Math.round(item.baseStatValue * (5.5 / 3.8));
  return {
    ...item,
    id: `ascended_${Date.now()}_${item.id}`,
    rarity: 'mythic',
    name: item.name.replace('Địa Linh Kim', 'Thiên Đạo Thần Khí'),
    baseStatValue: newBaseVal,
    itemLevel: item.itemLevel + 5,
  };
}

export function getMaxInventorySlots(forgerRankTier: number): number {
  return Math.min(64, Math.max(24, 20 + forgerRankTier * 4));
}


export function getSalvageYield(item: EquipmentItem): {
  linhThach: number;
  tinhHoa: number;
  ironDust: number;
  celestialStar: number;
} {
  const meta = getItemRarityMeta(item.rarity);
  switch (meta.tier) {
    case 'S':
      return { linhThach: 0, tinhHoa: 20, ironDust: 1000, celestialStar: 1 };
    case 'A':
      return { linhThach: 0, tinhHoa: 5, ironDust: 350, celestialStar: 0 };
    case 'B':
      return { linhThach: 0, tinhHoa: 1, ironDust: 120, celestialStar: 0 };
    case 'C':
      return { linhThach: 100, tinhHoa: 0, ironDust: 45, celestialStar: 0 };
    case 'D':
      return { linhThach: 30, tinhHoa: 0, ironDust: 15, celestialStar: 0 };
    default:
      return { linhThach: 10, tinhHoa: 0, ironDust: 5, celestialStar: 0 };
  }
}

export function getItemRarityMeta(rarity: ItemRarity) {
  switch (rarity) {
    case 'tier_s':
    case 'mythic':
      return {
        tier: 'S' as const,
        label: 'Tier S · Thiên Đạo Thần Khí',
        shortLabel: 'Tier S',
        subName: 'Thiên Đạo Thần Khí',
        textColor: 'text-red-400',
        borderColor: 'border-red-500/90',
        bgColor: 'bg-red-500/15',
        badgeBg: 'bg-red-500/25 text-red-300 border-red-500/50',
        glow: 'shadow-red-500/40',
        hex: '#EF4444',
        statMultiplier: 5.5,
        maxSockets: 4,
        maxAffixes: 4,
      };
    case 'tier_a':
    case 'legendary':
      return {
        tier: 'A' as const,
        label: 'Tier A · Địa Linh Kim',
        shortLabel: 'Tier A',
        subName: 'Địa Linh Kim',
        textColor: 'text-amber-400',
        borderColor: 'border-amber-400/90',
        bgColor: 'bg-amber-500/15',
        badgeBg: 'bg-amber-500/25 text-amber-300 border-amber-500/50',
        glow: 'shadow-amber-500/40',
        hex: '#F59E0B',
        statMultiplier: 3.8,
        maxSockets: 3,
        maxAffixes: 4,
      };
    case 'tier_b':
    case 'epic':
      return {
        tier: 'B' as const,
        label: 'Tier B · Huyền Thiết',
        shortLabel: 'Tier B',
        subName: 'Huyền Thiết',
        textColor: 'text-purple-400',
        borderColor: 'border-purple-400/90',
        bgColor: 'bg-purple-500/15',
        badgeBg: 'bg-purple-500/25 text-purple-300 border-purple-500/50',
        glow: 'shadow-purple-500/40',
        hex: '#A855F7',
        statMultiplier: 2.6,
        maxSockets: 2,
        maxAffixes: 3,
      };
    case 'tier_c':
    case 'rare':
      return {
        tier: 'C' as const,
        label: 'Tier C · Cổ Đồng',
        shortLabel: 'Tier C',
        subName: 'Cổ Đồng',
        textColor: 'text-blue-400',
        borderColor: 'border-blue-400/90',
        bgColor: 'bg-blue-500/15',
        badgeBg: 'bg-blue-500/25 text-blue-300 border-blue-500/50',
        glow: 'shadow-blue-500/40',
        hex: '#3B82F6',
        statMultiplier: 1.85,
        maxSockets: 2,
        maxAffixes: 2,
      };
    case 'tier_d':
    case 'uncommon':
      return {
        tier: 'D' as const,
        label: 'Tier D · Tinh Thiết',
        shortLabel: 'Tier D',
        subName: 'Tinh Thiết',
        textColor: 'text-emerald-400',
        borderColor: 'border-emerald-500/90',
        bgColor: 'bg-emerald-500/15',
        badgeBg: 'bg-emerald-500/25 text-emerald-300 border-emerald-500/50',
        glow: 'shadow-emerald-500/40',
        hex: '#10B981',
        statMultiplier: 1.35,
        maxSockets: 1,
        maxAffixes: 1,
      };
    default:
      return {
        tier: 'E' as const,
        label: 'Tier E · Phàm Thiết',
        shortLabel: 'Tier E',
        subName: 'Phàm Thiết',
        textColor: 'text-slate-300',
        borderColor: 'border-slate-700/80',
        bgColor: 'bg-slate-800/40',
        badgeBg: 'bg-slate-800/60 text-slate-300 border-slate-700/50',
        glow: 'shadow-slate-700/20',
        hex: '#94A3B8',
        statMultiplier: 1.0,
        maxSockets: 0,
        maxAffixes: 0,
      };
  }
}

export const INITIAL_EQUIPPED_SLOTS: Record<EquipmentSlotKey, EquipmentItem> = {
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
    magicFindPct: Math.min(50, Math.round(rawSPI * 0.4)),
  };
}

export function computeRaidContributionScore(
  damage: number,
  armorBreakPoints: number,
  heatPumped: number,
  anvilRepaired: number
): number {
  return Math.round(
    damage * 1.0 +
    armorBreakPoints * 25_000 +
    heatPumped * 15_000 +
    anvilRepaired * 2.0
  );
}

export interface StrikeInput {
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
  serverFurnaceHeat?: number;
  vaultMeltingThreshold?: number;
  isFrozenSky?: boolean;
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
  armorBreakGain: number;
  serverHeatGain: number;
  anvilRepairGain: number;
  freezeRegenSec: number;
  anvilDamage: number;
  raidContributionGain: number;
  isFrozenSky?: boolean;
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
      armorBreakGain: 0,
      serverHeatGain: -50,
      anvilRepairGain: 0,
      freezeRegenSec: 0,
      anvilDamage: 5,
      raidContributionGain: 0,
      isGlancingHit: false,
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

  // 9. World Raid Edition (v3.1) Calculations
  const isFrozenSky = input.isFrozenSky ?? (
    input.serverFurnaceHeat !== undefined && input.vaultMeltingThreshold !== undefined
      ? input.serverFurnaceHeat < input.vaultMeltingThreshold
      : false
  );

  // A. Phá Giáp (Armor Break Points)
  let baseBreakGain = input.stance === 'E'
    ? (isGolden ? 8 : 4) + Math.round(pen * 0.15)
    : (isGolden ? 2 : 1) + Math.round(pen * 0.05);
  if ((arsenal?.setCounts.set_gravity ?? 0) >= 2) {
    baseBreakGain += 2;
  }
  if (isFrozenSky) {
    baseBreakGain = Math.max(1, Math.round(baseBreakGain * 0.6));
  }
  const armorBreakGain = baseBreakGain;

  // B. Đại Hỏa Hẩu Server (Heat Pumped)
  let baseServerHeat = input.stance === 'W'
    ? (isGolden ? 25 : 12) + Math.round(intStat * 0.25)
    : (isGolden ? 6 : 2);
  if ((arsenal?.setCounts.set_fire ?? 0) >= 6 && input.stance === 'W') {
    baseServerHeat *= 2.0;
  }
  const serverHeatGain = Math.round(baseServerHeat);

  // C. Độ Bền Đại Đe Server (Anvil Repair)
  let baseAnvilRepair = input.stance === 'R'
    ? (isGolden ? 20 : 8) + Math.round((arsenal?.coreStats.spi ?? 10) * 0.2)
    : 0;
  if ((arsenal?.setCounts.set_mystic ?? 0) >= 4 && isGolden && input.stance === 'R') {
    baseAnvilRepair += 15;
  }
  const anvilRepairGain = Math.round(baseAnvilRepair);

  // D. Đóng Băng Tự Hồi Giáp (Set Thái Sơn 6/6)
  const freezeRegenSec = (input.stance === 'E' && (arsenal?.setCounts.set_gravity ?? 0) >= 6 && isGolden) ? 0.5 : 0;

  // E. Anvil Damage from Glancing hit
  const anvilDamage = isGlancingHit ? 3 : 0;

  // F. Raid Contribution Score (RCS)
  const raidContributionGain = computeRaidContributionScore(
    finalDamage,
    armorBreakGain,
    serverHeatGain,
    anvilRepairGain
  );

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
    armorBreakGain,
    serverHeatGain,
    anvilRepairGain,
    freezeRegenSec,
    anvilDamage,
    raidContributionGain,
    isFrozenSky,
  };
}

export interface ForgeUpgrade {
  id: string;
  name: string;
  subtitle: string;
  level: number;
  maxLevel: number;
  baseCost: number;
  costScale: number;
  powerPerLevel: number; // Base flat addition or level scaler
}

export const INITIAL_UPGRADES: ForgeUpgrade[] = [
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

export function calculateBasePower(upgrades: ForgeUpgrade[]): number {
  const hammer = upgrades.find((u) => u.id === 'celestial_hammer_core');
  const hammerLevel = hammer ? hammer.level : 1;
  const baseDmg = calculateForgeDamage(hammerLevel);

  const oil = upgrades.find((u) => u.id === 'thunder_quench_oil');
  const oilBonus = oil ? oil.level * 1 : 0;

  return Math.max(1, baseDmg + oilBonus);
}

// Backward-compatibility wrapper
export function calculateBasePowerBillions(upgrades: ForgeUpgrade[]): number {
  return calculateBasePower(upgrades);
}

export interface SpiritNode {
  id: string;
  name: string;
  constellation: string;
  description: string;
  costTinhHoa: number;
  bonusMult: number; // additive to spiritBonusMult, e.g. 0.25 = +25%
  x: number; // SVG 0..100
  y: number; // SVG 0..100
  requires?: string;
  tier?: number; // Tier 1 (available) or Tier 2 (requires 100k milestone)
  unlocked: boolean;
}

export const INITIAL_SPIRIT_NODES: SpiritNode[] = [
  {
    id: 'node_origin',
    name: 'Thái Sơ Hỏa Chủng',
    constellation: 'Tâm Tinh · Khởi Nguyên',
    description: 'Khơi nguồn Thần Hỏa cổ đại, tăng +20% tổng sát thương rèn đập.',
    costTinhHoa: 0,
    bonusMult: 0.2,
    x: 50,
    y: 82,
    tier: 1,
    unlocked: true,
  },
  {
    id: 'node_thunder_eye',
    name: 'Lôi Nhãn Tinh Quân',
    constellation: 'Tả Tinh · Lôi Điện',
    description: 'Mở rộng cảm ứng nhịp điệu, tăng +30% công lực Lôi Điện.',
    costTinhHoa: 2,
    bonusMult: 0.3,
    x: 24,
    y: 58,
    tier: 1,
    requires: 'node_origin',
    unlocked: false,
  },
  {
    id: 'node_crimson_furnace',
    name: 'Xích Đế Lò Luyện',
    constellation: 'Hữu Tinh · Thiên Hỏa',
    description: 'Nhiệt độ lò rèn vượt ngưỡng, tăng +35% sát thương lên Boss.',
    costTinhHoa: 3,
    bonusMult: 0.35,
    x: 76,
    y: 58,
    tier: 1,
    requires: 'node_origin',
    unlocked: false,
  },
  {
    id: 'node_shatter_star',
    name: 'Phá Quân Tinh Hồn',
    constellation: 'Trung Tinh · Phá Giáp',
    description: 'Cộng hưởng trọng lực, tăng +45% tổng sát thương và phá giáp.',
    costTinhHoa: 5,
    bonusMult: 0.45,
    x: 50,
    y: 38,
    tier: 2,
    requires: 'node_origin',
    unlocked: false,
  },
  {
    id: 'node_sky_breaker',
    name: 'Cửu Trọng Phá Thiên',
    constellation: 'Đỉnh Tinh · Chí Tôn',
    description: 'Đỉnh cao thần kỹ Vạn Dân Hợp Lực, tăng +80% công lực toàn diện.',
    costTinhHoa: 10,
    bonusMult: 0.8,
    x: 50,
    y: 14,
    tier: 2,
    requires: 'node_shatter_star',
    unlocked: false,
  },
];

export function canUnlockSpiritNode(
  nodeId: string,
  nodes: SpiritNode[],
  currentTinhHoa: number,
  tier2Unlocked: boolean = true
): boolean {
  const target = nodes.find((n) => n.id === nodeId);
  if (!target || target.unlocked) return false;
  if (target.tier === 2 && !tier2Unlocked) return false;
  if (currentTinhHoa < target.costTinhHoa) return false;
  if (target.requires) {
    const parent = nodes.find((n) => n.id === target.requires);
    if (!parent || !parent.unlocked) return false;
  }
  return true;
}

export function calculateSpiritMultiplier(nodes: SpiritNode[]): number {
  const bonus = nodes.reduce((acc, n) => (n.unlocked ? acc + n.bonusMult : acc), 1.0);
  return Number(bonus.toFixed(2));
}

// ============================================================================
// PHASE 2: ĐẲNG CẤP THỢ RÈN (FORGER RANKS) & KỸ PHÁP TỨ THẾ (STANCE SKILL TREES)
// ============================================================================
export interface ForgerRank {
  id: string;
  tier: number;
  title: string;
  badge: string;
  damageRequired: number;
  bonusDesc: string;
  damageMultiplier: number;
  essenceBonusPct: number;
  synergyRateBonusPct: number;
}

export const FORGER_RANKS: ForgerRank[] = [
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

export function getForgerRank(totalDamage: number): ForgerRank {
  for (let i = FORGER_RANKS.length - 1; i >= 0; i--) {
    if (totalDamage >= FORGER_RANKS[i].damageRequired) {
      return FORGER_RANKS[i];
    }
  }
  return FORGER_RANKS[0];
}

export interface StanceSkillNode {
  id: string;
  stance: StanceKey; // 'Q' | 'W' | 'E' | 'R'
  tier: number; // 1 to 5
  name: string;
  description: string;
  costTinhHoa: number;
  bonusType:
    | 'resonanceSpeed'
    | 'perfectWindow'
    | 'plasmaLightning'
    | 'burnDoT'
    | 'furnaceHeat'
    | 'fireBurst'
    | 'heavyShatter'
    | 'executeCrit'
    | 'oreWealth'
    | 'missForgive'
    | 'masterPerk';
  bonusValue: number;
  unlocked: boolean;
  requires?: string;
}

export const INITIAL_STANCE_SKILLS: StanceSkillNode[] = [
  // ===================== [Q] LÔI ĐỈNH (TỐC ĐỘ & NHỊP ĐIỆU) =====================
  {
    id: 'q_tier_1',
    stance: 'Q',
    tier: 1,
    name: 'Dẫn Lôi',
    description: 'Tăng +15% điểm Phá Giáp & +10% tốc độ nạp Cực Nhịp khi dùng thế Lôi Đỉnh.',
    costTinhHoa: 1,
    bonusType: 'resonanceSpeed',
    bonusValue: 0.15,
    unlocked: false,
  },
  {
    id: 'q_tier_2',
    stance: 'Q',
    tier: 2,
    name: 'Lôi Tốc Kích',
    description: 'Mở rộng cửa sổ nhịp Hoàng Kim thêm +15 ms khi ở thế Lôi Đỉnh.',
    costTinhHoa: 2,
    bonusType: 'perfectWindow',
    bonusValue: 15,
    requires: 'q_tier_1',
    unlocked: false,
  },
  {
    id: 'q_tier_3',
    stance: 'Q',
    tier: 3,
    name: 'Sét Truyền Thần',
    description: 'Gõ Perfect phóng tia sét lan sang các thợ rèn lân cận, buff +10% sát thương đồng minh.',
    costTinhHoa: 3,
    bonusType: 'plasmaLightning',
    bonusValue: 0.1,
    requires: 'q_tier_2',
    unlocked: false,
  },
  {
    id: 'q_tier_4',
    stance: 'Q',
    tier: 4,
    name: 'Bão Plasma Cuồng Kích',
    description: 'Trong trạng thái Overdrive, Thế Lôi Đỉnh gây thêm +50% Sát Thương sấm sét.',
    costTinhHoa: 5,
    bonusType: 'plasmaLightning',
    bonusValue: 0.5,
    requires: 'q_tier_3',
    unlocked: false,
  },
  {
    id: 'q_tier_5',
    stance: 'Q',
    tier: 5,
    name: 'Thiên Lôi Giáng Thế (Master Perk)',
    description: 'Đạt chuỗi 15 Hoàng Kim: Tự động giáng sấm sét tối thượng bỏ qua 100% giáp Boss (-500 DMG thuần)!',
    costTinhHoa: 10,
    bonusType: 'masterPerk',
    bonusValue: 500,
    requires: 'q_tier_4',
    unlocked: false,
  },

  // ===================== [W] VIÊM DƯƠNG (DoT & GIỮ LỬA) =====================
  {
    id: 'w_tier_1',
    stance: 'W',
    tier: 1,
    name: 'Tro Tàn',
    description: 'Mỗi nhát đập tích lũy tầng cháy trên Vòm Trời (tối đa 50 tầng), thiêu đốt HP Boss mỗi giây.',
    costTinhHoa: 1,
    bonusType: 'burnDoT',
    bonusValue: 1,
    unlocked: false,
  },
  {
    id: 'w_tier_2',
    stance: 'W',
    tier: 2,
    name: 'Hỏa Lò Khởi Sắc',
    description: 'Tăng +5°C Hỏa Hầu mỗi nhát đập và giảm 30% tốc độ nguội đe rèn tự nhiên.',
    costTinhHoa: 2,
    bonusType: 'furnaceHeat',
    bonusValue: 5,
    requires: 'w_tier_1',
    unlocked: false,
  },
  {
    id: 'w_tier_3',
    stance: 'W',
    tier: 3,
    name: 'Viêm Nhiệt Cuồng Chùy',
    description: 'Khi Hỏa Hầu trên 600°C, sát thương thế Viêm Dương tăng thêm +35%.',
    costTinhHoa: 3,
    bonusType: 'furnaceHeat',
    bonusValue: 0.35,
    requires: 'w_tier_2',
    unlocked: false,
  },
  {
    id: 'w_tier_4',
    stance: 'W',
    tier: 4,
    name: 'Hỏa Diệm Bùng Phát',
    description: 'Nhát gõ Hoàng Kim tích gấp đôi (+2 tầng cháy), giới hạn nâng lên tối đa 80 tầng cháy.',
    costTinhHoa: 5,
    bonusType: 'burnDoT',
    bonusValue: 2,
    requires: 'w_tier_3',
    unlocked: false,
  },
  {
    id: 'w_tier_5',
    stance: 'W',
    tier: 5,
    name: 'Hỏa Ngục Đồng Quy (Master Perk)',
    description: 'Kích nổ toàn bộ tầng cháy khi Phá Giáp (Shield Break), gây x3.0 sát thương tích lũy thiêu đốt!',
    costTinhHoa: 10,
    bonusType: 'fireBurst',
    bonusValue: 3.0,
    requires: 'w_tier_4',
    unlocked: false,
  },

  // ===================== [E] TRỌNG LỰC (BẠO KÍCH & CHÙY NẶNG) =====================
  {
    id: 'e_tier_1',
    stance: 'E',
    tier: 1,
    name: 'Chùy Ngàn Cân',
    description: 'Tăng sát thương thế Trọng Lực lên x1.5, mỗi nhát tích +2 điểm Phá Giáp.',
    costTinhHoa: 1,
    bonusType: 'heavyShatter',
    bonusValue: 2,
    unlocked: false,
  },
  {
    id: 'e_tier_2',
    stance: 'E',
    tier: 2,
    name: 'Địa Chấn Hư Không',
    description: 'Nhát gõ Chuẩn Xác/Hoàng Kim tạo chấn động cực mạnh, giảm 15% số nhát cần để Phá Giáp.',
    costTinhHoa: 2,
    bonusType: 'heavyShatter',
    bonusValue: 0.15,
    requires: 'e_tier_1',
    unlocked: false,
  },
  {
    id: 'e_tier_3',
    stance: 'E',
    tier: 3,
    name: 'Trọng Áp Phá Giáp',
    description: 'Tăng +25% Tỷ Lệ Bạo Kích (Crit) khi đang vận dụng thế Trọng Lực.',
    costTinhHoa: 3,
    bonusType: 'executeCrit',
    bonusValue: 0.25,
    requires: 'e_tier_2',
    unlocked: false,
  },
  {
    id: 'e_tier_4',
    stance: 'E',
    tier: 4,
    name: 'Nặng Tựa Thái Sơn',
    description: 'Đòn đánh Bạo Kích ở thế Trọng Lực gây x2.0 sát thương (thay vì x1.5 thông thường).',
    costTinhHoa: 5,
    bonusType: 'executeCrit',
    bonusValue: 2.0,
    requires: 'e_tier_3',
    unlocked: false,
  },
  {
    id: 'e_tier_5',
    stance: 'E',
    tier: 5,
    name: 'Hư Không Đoạt Mệnh (Master Perk)',
    description: 'Khi Boss còn dưới 30% máu lớp phong ấn: Tăng 30% tỷ lệ đòn đánh trảm sát nhân x5.0 sát thương!',
    costTinhHoa: 10,
    bonusType: 'masterPerk',
    bonusValue: 5.0,
    requires: 'e_tier_4',
    unlocked: false,
  },

  // ===================== [R] HUYỀN ÂM (CỘNG HƯỞNG & TRỢ LỰC) =====================
  {
    id: 'r_tier_1',
    stance: 'R',
    tier: 1,
    name: 'Hòa Âm',
    description: 'Tăng +25% Linh Thạch rơi mỗi nhát búa và tăng +20% Linh Thạch AFK treo máy.',
    costTinhHoa: 1,
    bonusType: 'oreWealth',
    bonusValue: 0.25,
    unlocked: false,
  },
  {
    id: 'r_tier_2',
    stance: 'R',
    tier: 2,
    name: 'Ngọc Bích Hộ Thể',
    description: 'Giảm 50% hình phạt khi bấm trượt nhịp (Miss), tự động bảo toàn 1 tầng Overdrive.',
    costTinhHoa: 2,
    bonusType: 'missForgive',
    bonusValue: 0.5,
    requires: 'r_tier_1',
    unlocked: false,
  },
  {
    id: 'r_tier_3',
    stance: 'R',
    tier: 3,
    name: 'Tiếng Vang Vạn Dân',
    description: 'Mỗi nhát gõ hoàn hảo tăng +0.3% tiến độ nạp Cực Nhịp Toàn Cầu.',
    costTinhHoa: 3,
    bonusType: 'oreWealth',
    bonusValue: 0.3,
    requires: 'r_tier_2',
    unlocked: false,
  },
  {
    id: 'r_tier_4',
    stance: 'R',
    tier: 4,
    name: 'Tinh Hoa Tụ Đỉnh',
    description: 'Tăng gấp đôi (+100%) tỷ lệ nhặt Tinh Hoa Thần Hồn từ nhát búa Hoàng Kim.',
    costTinhHoa: 5,
    bonusType: 'oreWealth',
    bonusValue: 1.0,
    requires: 'r_tier_3',
    unlocked: false,
  },
  {
    id: 'r_tier_5',
    stance: 'R',
    tier: 5,
    name: 'Khúc Khải Hoàn (Master Perk)',
    description: 'Kéo dài thời gian Đại Cộng Hưởng thêm 15 giây và ban phát hào quang x1.5 sát thương toàn đội!',
    costTinhHoa: 10,
    bonusType: 'masterPerk',
    bonusValue: 1.5,
    requires: 'r_tier_4',
    unlocked: false,
  },
];

export function canUnlockStanceSkill(
  nodeId: string,
  skills: StanceSkillNode[],
  currentTinhHoa: number,
  forgerRankTier: number = 1
): boolean {
  const target = skills.find((s) => s.id === nodeId);
  if (!target || target.unlocked) return false;
  if (currentTinhHoa < target.costTinhHoa) return false;
  if (target.tier >= 4 && forgerRankTier < 3) return false;
  if (target.requires) {
    const parent = skills.find((s) => s.id === target.requires);
    if (!parent || !parent.unlocked) return false;
  }
  return true;
}

export function calculateStanceSkillBonuses(
  skills: StanceSkillNode[],
  activeStance: StanceKey
): Record<string, number> {
  const bonuses: Record<string, number> = {
    damageMult: 1.0,
    resonanceAdd: 0,
    perfectWindowMs: 0,
    critChanceAdd: 0,
    critMultOverride: 0,
    heatGainAdd: 0,
    linhThachMult: 1.0,
    essenceDropMult: 1.0,
    hasMasterPerk: 0,
  };

  const unlockedSkills = skills.filter((s) => s.unlocked && s.stance === activeStance);
  for (const s of unlockedSkills) {
    switch (s.bonusType) {
      case 'resonanceSpeed':
        bonuses.resonanceAdd += s.bonusValue;
        break;
      case 'perfectWindow':
        bonuses.perfectWindowMs += s.bonusValue;
        break;
      case 'plasmaLightning':
        bonuses.damageMult += s.bonusValue;
        break;
      case 'furnaceHeat':
        if (s.bonusValue >= 1) bonuses.heatGainAdd += s.bonusValue;
        else bonuses.damageMult += s.bonusValue;
        break;
      case 'heavyShatter':
        bonuses.resonanceAdd += s.bonusValue;
        break;
      case 'executeCrit':
        if (s.bonusValue < 1) bonuses.critChanceAdd += s.bonusValue * 100;
        else bonuses.critMultOverride = s.bonusValue;
        break;
      case 'oreWealth':
        bonuses.linhThachMult += s.bonusValue;
        if (s.id === 'r_tier_4') bonuses.essenceDropMult += 1.0;
        break;
      case 'masterPerk':
        bonuses.hasMasterPerk = s.bonusValue;
        break;
    }
  }

  return bonuses;
}

// ============================================================================
// PHASE 3: CỬU TRỌNG THIÊN (THE 9 CELESTIAL VAULTS)
// ============================================================================
export interface CelestialVault {
  id: number;
  name: string;
  title: string;
  bossName: string;
  bossTitle: string;
  maxHp: number; // Integer RPG HP
  damageReductionPct: number;
  recommendedPlayers: string;
  armorBreakMaxPoints: number;
  armorRegenPerSec: number;
  serverChillPerSec: number;
  meltingThreshold: number;
  wipeMechanicName: string;
  wipeMechanicDesc: string;
  skyTheme: {
    bgGradient: string;
    crackColor: string;
    crackGlow: string;
    lightningHex: string;
    particleHex: string;
  };
  loreSummary: string;
  unlockedByDefault?: boolean;
}

export const CELESTIAL_VAULTS: CelestialVault[] = [
  {
    id: 1,
    name: 'Thiết Vân Vòm',
    title: 'Tầng 1 · Giáp Sắt Mây Đen',
    bossName: 'Hắc Diệm Thao Thiết',
    bossTitle: 'Cổ Thần Cửu U · Thôn Phệ Vạn Vật',
    maxHp: 1_500_000_000,
    damageReductionPct: 80,
    recommendedPlayers: '10 – 15 người (Raid Nhập Môn)',
    armorBreakMaxPoints: 500,
    armorRegenPerSec: 15,
    serverChillPerSec: -60,
    meltingThreshold: 1500,
    wipeMechanicName: 'Mây Đen Thôn Phệ',
    wipeMechanicDesc: 'Mỗi 45 giây hút 30% Linh Thạch rớt ra nếu không có ít nhất 3 người hệ [R] gõ Hoàng Kim liên tiếp.',
    skyTheme: {
      bgGradient: 'from-slate-950 via-[#0a0f1d] to-[#121927]',
      crackColor: '#FF9E00',
      crackGlow: '#FF4D00',
      lightningHex: '#00F0FF',
      particleHex: '#FF9E00',
    },
    loreSummary: 'Mái vòm bằng kim loại rỉ sét và mây đen kịt bọc kín thung lũng Thiên Thai.',
    unlockedByDefault: true,
  },
  {
    id: 2,
    name: 'Cổ Đồng Thiên',
    title: 'Tầng 2 · Đồng Rỉ Đông Sơn',
    bossName: 'Trấn Thiên Lạc Thần',
    bossTitle: 'Hộ Giới Thần Tướng · Trấn Áp Cổ Cương',
    maxHp: 4_500_000_000,
    damageReductionPct: 82,
    recommendedPlayers: '15 – 25 người (Raid Sơ Cấp)',
    armorBreakMaxPoints: 1000,
    armorRegenPerSec: 30,
    serverChillPerSec: -100,
    meltingThreshold: 2200,
    wipeMechanicName: 'Đồng Rỉ Hóa Thạch',
    wipeMechanicDesc: 'Cứ 10 nhát gõ cùng 1 Thế Búa làm kẹt đe cá nhân; buộc đội hình phải đảo Thế hoặc nhận buff giải rỉ từ đồng đội.',
    skyTheme: {
      bgGradient: 'from-[#1a120b] via-[#24170d] to-[#3a2310]',
      crackColor: '#F59E0B',
      crackGlow: '#D97706',
      lightningHex: '#FBBF24',
      particleHex: '#F59E0B',
    },
    loreSummary: 'Mái vòm đồng cổ chạm khắc hoa văn Đông Sơn ngàn năm, rỉ sét bốc khói độc thiêu đốt nhân gian.',
  },
  {
    id: 3,
    name: 'Lôi Tiêu Điện',
    title: 'Tầng 3 · Bão Plasma Tím',
    bossName: 'Ứng Lôi Chân Quân',
    bossTitle: 'Thiên Cấm Lôi Thần · Chưởng Quản Tử Lôi',
    maxHp: 12_000_000_000,
    damageReductionPct: 85,
    recommendedPlayers: '25 – 35 người (Raid Trung Cấp)',
    armorBreakMaxPoints: 1800,
    armorRegenPerSec: 55,
    serverChillPerSec: -160,
    meltingThreshold: 3000,
    wipeMechanicName: 'Bão Plasma Tím',
    wipeMechanicDesc: 'Đánh sét ngẫu nhiên vào 10 thợ rèn DPS cao nhất; nhóm [Q] Lôi Đỉnh phải gõ Perfect để thu lôi hộ đồng đội.',
    skyTheme: {
      bgGradient: 'from-[#140b24] via-[#1f1038] to-[#2c134d]',
      crackColor: '#C084FC',
      crackGlow: '#9333EA',
      lightningHex: '#E879F9',
      particleHex: '#A855F7',
    },
    loreSummary: 'Biển mây tím phóng ra các luồng sét plasma hàng triệu vôn ngăn cản bước chân thợ rèn.',
  },
  {
    id: 4,
    name: 'Hàn Băng Thần',
    title: 'Tầng 4 · Kính Băng Cực Độ',
    bossName: 'Huyền Minh Băng Hoàng',
    bossTitle: 'Tuyết Vực Thần Tước · Đóng Băng Hư Không',
    maxHp: 30_000_000_000,
    damageReductionPct: 88,
    recommendedPlayers: '35 – 50 người (Raid Trung Cấp)',
    armorBreakMaxPoints: 2800,
    armorRegenPerSec: 85,
    serverChillPerSec: -320,
    meltingThreshold: 4200,
    wipeMechanicName: 'Kính Băng Cực Độ',
    wipeMechanicDesc: 'Đóng băng Đại Hỏa Hẩu cực nhanh; cần ít nhất 12–15 Thợ Rèn [W] Viêm Dương quạt lửa liên tục mới giữ được lò.',
    skyTheme: {
      bgGradient: 'from-[#081826] via-[#0d273d] to-[#123654]',
      crackColor: '#38BDF8',
      crackGlow: '#0284C7',
      lightningHex: '#7DD3FC',
      particleHex: '#38BDF8',
    },
    loreSummary: 'Mặt gương băng vĩnh cửu đông cứng linh khí và phản hồi sát thương ngược về trần thế.',
  },
  {
    id: 5,
    name: 'Xích Diễm Giới',
    title: 'Tầng 5 · Nham Thạch Núi Lửa',
    bossName: 'Chúc Dung Ma Thần',
    bossTitle: 'Hỏa Cực Chi Chủ · Phần Diệt Cửu Châu',
    maxHp: 75_000_000_000,
    damageReductionPct: 90,
    recommendedPlayers: '45 – 60 người (Raid Cao Cấp)',
    armorBreakMaxPoints: 4200,
    armorRegenPerSec: 120,
    serverChillPerSec: 250,
    meltingThreshold: 8500,
    wipeMechanicName: 'Nham Thạch Núi Lửa',
    wipeMechanicDesc: 'Tự động bơm nhiệt làm nổ Đại Hỏa Hẩu; cần ít nhất 12 Thợ Rèn [R] Huyền Âm xả nhiệt điều hòa lò cho cả server.',
    skyTheme: {
      bgGradient: 'from-[#260b08] via-[#3d120d] to-[#541812]',
      crackColor: '#EF4444',
      crackGlow: '#DC2626',
      lightningHex: '#F87171',
      particleHex: '#EF4444',
    },
    loreSummary: 'Bầu trời dung nham đỏ quạch, lửa thiêng liên tục dội xuống đe rèn của nhân loại.',
  },
  {
    id: 6,
    name: 'Huyền Thủy Hải',
    title: 'Tầng 6 · Biển Trời Nghịch',
    bossName: 'Côn Bằng Hóa Minh',
    bossTitle: 'Cự Thú Thâm Uyên · Thôn Thiên Nạp Địa',
    maxHp: 180_000_000_000,
    damageReductionPct: 92,
    recommendedPlayers: '60 – 75 người (Raid Cao Cấp)',
    armorBreakMaxPoints: 6000,
    armorRegenPerSec: 165,
    serverChillPerSec: -450,
    meltingThreshold: 5500,
    wipeMechanicName: 'Sóng Thần Nghịch Lưu',
    wipeMechanicDesc: 'Cuốn trôi 50% thanh Overdrive của toàn server mỗi 30 giây nếu nhóm [E] Trọng Lực không dựng Tường Chấn Động.',
    skyTheme: {
      bgGradient: 'from-[#06181f] via-[#0b2834] to-[#103b4d]',
      crackColor: '#06B6D4',
      crackGlow: '#0891B2',
      lightningHex: '#22D3EE',
      particleHex: '#06B6D4',
    },
    loreSummary: 'Đại dương nghịch chuyển treo ngược trên bầu trời, áp suất khủng khiếp bóp nát vạn vật.',
  },
  {
    id: 7,
    name: 'Bát Quái Phong',
    title: 'Tầng 7 · Trận Đồ Phong Cấm',
    bossName: 'Vô Cực Cơ Quan Tôn',
    bossTitle: 'Thái Cổ Khôi Lỗi · Trận Nhãn Vạn Cổ',
    maxHp: 420_000_000_000,
    damageReductionPct: 94,
    recommendedPlayers: '75 – 90 người (Raid Tinh Anh)',
    armorBreakMaxPoints: 8500,
    armorRegenPerSec: 220,
    serverChillPerSec: -600,
    meltingThreshold: 6500,
    wipeMechanicName: 'Bát Quái Phong Cấm',
    wipeMechanicDesc: 'Boss khóa ngẫu nhiên 1 Thế Búa toàn server mỗi 40 giây và yêu cầu 3 Thế Búa còn lại gõ đồng bộ theo tỷ lệ 1:1:1.',
    skyTheme: {
      bgGradient: 'from-[#181a0b] via-[#262912] to-[#363a18]',
      crackColor: '#84CC16',
      crackGlow: '#65A30D',
      lightningHex: '#A3E635',
      particleHex: '#84CC16',
    },
    loreSummary: 'Vòng quay bánh răng cơ quan khổng lồ che lấp nhật nguyệt, vận hành theo Bát Quái trận đồ.',
  },
  {
    id: 8,
    name: 'Hư Không Đoạn',
    title: 'Tầng 8 · Hố Đen Vũ Trụ',
    bossName: 'Thôn Thiên Ma Thú',
    bossTitle: 'Dị Thứ Nguyên Thần · Thôn Hấp Tinh Tú',
    maxHp: 950_000_000_000,
    damageReductionPct: 95,
    recommendedPlayers: '90 – 110 người (Raid Đại Chiến)',
    armorBreakMaxPoints: 12000,
    armorRegenPerSec: 280,
    serverChillPerSec: -750,
    meltingThreshold: 7500,
    wipeMechanicName: 'Hố Đen Thôn Phệ',
    wipeMechanicDesc: 'Hút máu từ mọi nhát gõ trượt (mỗi nhát Miss của bất kỳ ai làm Boss hồi +0.05% HP); đòi hỏi cả trăm người giữ DEX chuẩn.',
    skyTheme: {
      bgGradient: 'from-[#090614] via-[#120d26] to-[#1c133b]',
      crackColor: '#818CF8',
      crackGlow: '#4F46E5',
      lightningHex: '#A5B4FC',
      particleHex: '#818CF8',
    },
    loreSummary: 'Vết nứt không gian vũ trụ hút cạn mọi tia sáng, thời gian và không gian bị bẻ cong.',
  },
  {
    id: 9,
    name: 'Hỗn Độn Thiên',
    title: 'Tầng 9 · Con Mắt Thiên Đạo',
    bossName: 'Cửu U Tối Cao Chi Nhân',
    bossTitle: 'Nguồn Cội Hắc Ám · Chúa Tể Cửu U',
    maxHp: 2_500_000_000_000,
    damageReductionPct: 96,
    recommendedPlayers: '100 – 150+ người (Vạn Dân Quyết Chiến)',
    armorBreakMaxPoints: 18000,
    armorRegenPerSec: 380,
    serverChillPerSec: -950,
    meltingThreshold: 8800,
    wipeMechanicName: 'Con Mắt Thiên Đạo (Enrage 60 phút)',
    wipeMechanicDesc: 'Yêu cầu kích hoạt liên hoàn Vạn Dân Tam Điểm Lôi Hỏa từ ít nhất 100 người chơi chia đều 4 Phường Rèn để xuyên thủng Hỗn Độn.',
    skyTheme: {
      bgGradient: 'from-[#1f0510] via-[#33081a] to-[#470a25]',
      crackColor: '#F43F5E',
      crackGlow: '#E11D48',
      lightningHex: '#FB7185',
      particleHex: '#F43F5E',
    },
    loreSummary: 'Đỉnh cao của Cửu Trọng Thiên Cấm. Con mắt thần thức tối cao giáng sự diệt vong xuống trần gian.',
  },
];

export function getCelestialVault(id: number): CelestialVault {
  return CELESTIAL_VAULTS.find((v) => v.id === id) || CELESTIAL_VAULTS[0];
}

// ============================================================================
// PHASE 3: HỆ THỐNG PHƯỜNG RÈN (BLACKSMITH GUILDS) & ĐẠI HỎA LÒ BANG HỘI
// ============================================================================
export interface BlacksmithGuild {
  id: string;
  name: string;
  motto: string;
  icon: string;
  color: string;
  preferredStance: StanceKey;
  description: string;
  hearthLevel: number;
  hearthExp: number;
  hearthExpToNext: number;
  auraPerk: string;
  memberCount: number;
}

export const BLACKSMITH_GUILDS: BlacksmithGuild[] = [
  {
    id: 'guild_thien_thai',
    name: 'Thiên Thai Phường',
    motto: 'Khai Lò Phá Khởi · Lôi Đình Trảm Thiên',
    icon: '⚡',
    color: '#00F0FF',
    preferredStance: 'Q',
    description: 'Nơi phát tích nhát búa đầu tiên của nhân loại trên đỉnh Thiên Thai. Chuyên tinh thế Lôi Đỉnh.',
    hearthLevel: 1,
    hearthExp: 0,
    hearthExpToNext: 1000,
    auraPerk: '+10% tốc độ tích Overdrive & +15% tỷ lệ Sét Lan đồng minh',
    memberCount: 142,
  },
  {
    id: 'guild_phan_thien',
    name: 'Phần Thiên Các',
    motto: 'Hỏa Diệm Bất Diệt · Luyện Khí Thành Thần',
    icon: '🔥',
    color: '#FF4D00',
    preferredStance: 'W',
    description: 'Tập hợp những thợ rèn cuồng nhiệt giữ ngọn lửa lò không bao giờ tắt. Chuyên tinh thế Viêm Dương.',
    hearthLevel: 1,
    hearthExp: 0,
    hearthExpToNext: 1000,
    auraPerk: '+15% Sát thương thiêu đốt DoT & duy trì Hỏa Hầu >600°C',
    memberCount: 118,
  },
  {
    id: 'guild_van_kiem',
    name: 'Vạn Kiếm Sơn',
    motto: 'Nặng Tựa Thái Sơn · Nhất Kích Vỡ Vòm',
    icon: '🏔️',
    color: '#A855F7',
    preferredStance: 'E',
    description: 'Ẩn cư tại dãy Vạn Kiếm hiểm trở, tôn sùng lực nện ngàn cân. Chuyên tinh thế Trọng Lực.',
    hearthLevel: 1,
    hearthExp: 0,
    hearthExpToNext: 1000,
    auraPerk: '+15% Sát thương Bạo Kích & giảm 20% nhát gõ cần để Phá Giáp',
    memberCount: 96,
  },
  {
    id: 'guild_doan_hon',
    name: 'Đoạn Hồn Cốc',
    motto: 'Khúc Hát Khải Hoàn · Đồng Tâm Hiệp Lực',
    icon: '🎶',
    color: '#10B981',
    preferredStance: 'R',
    description: 'Thung lũng âm vang tiếng đe rèn đồng điệu vạn dặm. Chuyên tinh thế Huyền Âm.',
    hearthLevel: 1,
    hearthExp: 0,
    hearthExpToNext: 1000,
    auraPerk: '+20% sản lượng Linh Thạch & tăng gấp đôi thời gian Đại Cộng Hưởng',
    memberCount: 164,
  },
];

export function getGuild(id: string): BlacksmithGuild {
  return BLACKSMITH_GUILDS.find((g) => g.id === id) || BLACKSMITH_GUILDS[0];
}

// ============================================================================
// PHASE 3: NGHI THỨC TÔI LỬA NGUYÊN TỐ (ELEMENTAL TEMPERING / FORGE QUENCHING)
// ============================================================================
export interface QuenchOption {
  type: QuenchType;
  name: string;
  icon: string;
  color: string;
  costLinhThach: number;
  costTinhHoa: number;
  bonusTitle: string;
  bonusDesc: string;
}

export const QUENCH_OPTIONS: QuenchOption[] = [
  {
    type: 'ice',
    name: 'Tôi Nước Suối Băng',
    icon: '❄️',
    color: '#38BDF8',
    costLinhThach: 150,
    costTinhHoa: 1,
    bonusTitle: 'Hút Tinh Thể & Tài Phú',
    bonusDesc: '+15% Tỷ lệ Tinh Hoa & +25 Linh Thạch AFK/phút',
  },
  {
    type: 'magma',
    name: 'Tôi Dung Nham Núi Lửa',
    icon: '🌋',
    color: '#F97316',
    costLinhThach: 150,
    costTinhHoa: 1,
    bonusTitle: 'Hỏa Diệm Thiêu Đốt',
    bonusDesc: '+8 Sát thương thiêu đốt DoT cố định mỗi đòn nện búa',
  },
  {
    type: 'thunder',
    name: 'Tôi Máu Lôi Thần',
    icon: '⚡',
    color: '#A855F7',
    costLinhThach: 150,
    costTinhHoa: 1,
    bonusTitle: 'Lôi Điện Bạo Liệt',
    bonusDesc: '+12% Tỷ lệ Bạo Kích (Crit) & nổ sét diện rộng',
  },
];

export function formatInteger(n: number): string {
  return Math.max(0, Math.round(n)).toLocaleString('en-US');
}

export function formatHP(n: number): string {
  return formatInteger(n);
}

// Backward-compatibility wrapper
export function formatBillionsHP(n: number): string {
  return formatInteger(n);
}

export function formatCountdown(totalSeconds: number): string {
  const clamped = Math.max(0, Math.floor(totalSeconds));
  const mins = Math.floor(clamped / 60);
  const secs = clamped % 60;
  return `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
}

// ============================================================================
// 3,000-PARTICLE GPU / FLOAT32ARRAY SPARK SYSTEM (VẠN DÂN GHOST SPARKS & SELF STRIKES)
// ============================================================================
export const FORGE_SPARK_BUFFER_SIZE = 3000;
export const SPARK_GRAVITY = 9.8;

export type SparkOriginType = 'SELF' | 'PEER';
export type PeerStrikeQuality = JudgmentGrade | 'NORMAL';

export interface ForgeSparkBuffer {
  capacity: number;
  cursor: number;
  totalSpawned: number;
  positions: Float32Array; // vec3 (x0, y0, z0) on anvil surface
  velocities: Float32Array; // vec3 (vx, vy, vz) initial launch velocity
  colors: Float32Array; // vec3 (r, g, b)
  timings: Float32Array; // vec3 (spawnTime, duration, pointSize)
  alphas: Float32Array; // float baseAlpha
}

/**
 * Allocates a fixed-size 3,000-particle Float32Array buffer for THREE.Points GPU rendering.
 */
export function createForgeSparkBuffer(
  capacity: number = FORGE_SPARK_BUFFER_SIZE
): ForgeSparkBuffer {
  const positions = new Float32Array(capacity * 3);
  const velocities = new Float32Array(capacity * 3);
  const colors = new Float32Array(capacity * 3);
  const timings = new Float32Array(capacity * 3);
  const alphas = new Float32Array(capacity);

  // Initialize timings with negative spawnTime (-100s) so unspawned slots are expired/invisible
  for (let i = 0; i < capacity; i++) {
    const i3 = i * 3;
    timings[i3] = -100;
    timings[i3 + 1] = 1.0;
    timings[i3 + 2] = 0.0;
    alphas[i] = 0.0;
  }

  return {
    capacity,
    cursor: 0,
    totalSpawned: 0,
    positions,
    velocities,
    colors,
    timings,
    alphas,
  };
}

export interface SpawnSparkBurstParams {
  origin: SparkOriginType;
  quality: PeerStrikeQuality;
  currentTime: number;
  customCount?: number;
}

export interface SpawnSparkBurstResult {
  startIndex: number;
  count: number;
  isSelf: boolean;
  avgPointSize: number;
  avgAlpha: number;
}

/**
 * Writes a burst of sparks into the 3,000-particle Float32Array ring buffer:
 * - SELF strike: Large, dazzling golden sparks (#FFD23F / #FFF4B8), high alpha (0.92..1.0), large size (17..26)
 * - PEER strike (onPeerStrike Ghost Sparks): Smaller translucent white/pale-cyan sparks (#E2F2FF / #7DD3FC), subtle alpha (0.30..0.46), smaller size (6.5..11.0)
 */
export function spawnForgeSparkBurst(
  buffer: ForgeSparkBuffer,
  params: SpawnSparkBurstParams
): SpawnSparkBurstResult {
  const isSelf = params.origin === 'SELF';
  const defaultCount = isSelf
    ? params.quality === 'PERFECT'
      ? 140
      : params.quality === 'GREAT'
      ? 85
      : 32
    : params.quality === 'PERFECT'
    ? 44
    : params.quality === 'GREAT'
    ? 28
    : 18;

  const count = Math.min(buffer.capacity, params.customCount ?? defaultCount);
  const startIndex = buffer.cursor;

  let sizeSum = 0;
  let alphaSum = 0;

  for (let i = 0; i < count; i++) {
    const idx = (startIndex + i) % buffer.capacity;
    const i3 = idx * 3;

    // Spawn on the top face of the Anvil (y ~ 0.36..0.40)
    const spreadX = isSelf ? 0.85 : 1.55;
    const spreadZ = isSelf ? 0.52 : 0.92;
    buffer.positions[i3] = (Math.random() - 0.5) * spreadX;
    buffer.positions[i3 + 1] = 0.37 + Math.random() * 0.05;
    buffer.positions[i3 + 2] = (Math.random() - 0.5) * spreadZ;

    // Launch upward from the anvil face with random angle and high upward velocity before gravity pulls them down
    const theta = Math.random() * Math.PI * 2;
    const radialSpeed = isSelf
      ? (params.quality === 'PERFECT' ? 2.6 : 1.8) + Math.random() * 3.8
      : 1.4 + Math.random() * 2.8;
    const upwardSpeed = isSelf
      ? (params.quality === 'PERFECT' ? 5.2 : 4.0) + Math.random() * 4.2
      : (params.quality === 'PERFECT' ? 3.8 : 2.8) + Math.random() * 3.0;

    buffer.velocities[i3] = Math.cos(theta) * radialSpeed;
    buffer.velocities[i3 + 1] = upwardSpeed;
    buffer.velocities[i3 + 2] = Math.sin(theta) * radialSpeed;

    if (isSelf) {
      // Self Strike: Dazzling Golden & White-Gold Sparks (#FFD23F -> #FFF6C2)
      const goldMix = Math.random();
      buffer.colors[i3] = 1.0; // R
      buffer.colors[i3 + 1] = 0.84 + goldMix * 0.14; // G
      buffer.colors[i3 + 2] = 0.22 + goldMix * 0.45; // B
    } else {
      // Peer Strike (Ghost Sparks): Translucent White (#E8F4FF) or Pale Cyan (#7DD3FC)
      const cyanMix = Math.random();
      buffer.colors[i3] = 0.56 + cyanMix * 0.42; // R
      buffer.colors[i3 + 1] = 0.88 + cyanMix * 0.11; // G
      buffer.colors[i3 + 2] = 1.0; // B
    }

    const duration = isSelf
      ? 0.85 + Math.random() * 0.65
      : 0.75 + Math.random() * 0.55;
    const pointSize = isSelf
      ? (params.quality === 'PERFECT' ? 22.0 : 18.0) + Math.random() * 8.0
      : (params.quality === 'PERFECT' ? 9.0 : 7.0) + Math.random() * 3.5;
    const baseAlpha = isSelf
      ? 0.95 + Math.random() * 0.05
      : 0.35 + Math.random() * 0.16;

    // Slight initial flight stagger (0.01s..0.18s) so the burst forms a full 3D fountain immediately on impact
    const initialLeadSec = (i / Math.max(1, count)) * (isSelf ? 0.18 : 0.22);
    buffer.timings[i3] = params.currentTime - initialLeadSec;
    buffer.timings[i3 + 1] = duration;
    buffer.timings[i3 + 2] = pointSize;
    buffer.alphas[idx] = baseAlpha;

    sizeSum += pointSize;
    alphaSum += baseAlpha;
  }

  buffer.cursor = (startIndex + count) % buffer.capacity;
  buffer.totalSpawned += count;

  return {
    startIndex,
    count,
    isSelf,
    avgPointSize: count > 0 ? sizeSum / count : 0,
    avgAlpha: count > 0 ? alphaSum / count : 0,
  };
}

/**
 * Pure ballistic trajectory calculator matching the GPU Vertex Shader:
 * p(dt) = p0 + v0 * dt + 0.5 * (0, -gravity, 0) * dt^2
 */
export function computeSparkBallisticPosition(
  x0: number,
  y0: number,
  z0: number,
  vx: number,
  vy: number,
  vz: number,
  dt: number,
  gravity: number = SPARK_GRAVITY
): [number, number, number] {
  const clampedDt = Math.max(0, dt);
  return [
    x0 + vx * clampedDt,
    y0 + vy * clampedDt - 0.5 * gravity * clampedDt * clampedDt,
    z0 + vz * clampedDt,
  ];
}

// ============================================================================
// VÒM TRỜI NỨT VỠ (SHATTERABLE SKY DOME) & 1,500 VORONOI FRAGMENTS SYSTEM
// ============================================================================
export const SKY_SHATTER_FRAGMENT_COUNT = 1500;
export const SKY_SHATTER_DURATION_SEC = 2.4;

/**
 * Calculates uCrackProgress (0.0 to 1.0) from current Boss HP and Max HP:
 * - 0.0: Intact dark metallic clouds
 * - > 0.3: Golden-orange Voronoi cracks spreading from zenith
 * - > 0.8: Maximum magma/lightning fissures + vertex displacement tremor
 * - 1.0 (HP = 0): Triggers 1,500-fragment InstancedMesh sky shatter
 */
export function computeCrackProgress(
  bossHpBillions: number,
  bossMaxHpBillions: number
): number {
  if (bossMaxHpBillions <= 0) return 1.0;
  const ratio = 1.0 - bossHpBillions / bossMaxHpBillions;
  return Math.max(0.0, Math.min(1.0, Number(ratio.toFixed(4))));
}

export interface SkyShatterState {
  count: number;
  origins: Float32Array; // 1500 * 3 (x, y, z on hemisphere)
  velocities: Float32Array; // 1500 * 3 (vx, vy, vz blasting outward & behind camera)
  rotations: Float32Array; // 1500 * 3 (rx, ry, rz initial Euler)
  angularVelocities: Float32Array; // 1500 * 3 (wx, wy, wz tumbling)
  initialScales: Float32Array; // 1500 (base shard size)
}

/**
 * Generates 1,500 Voronoi-like triangular shard states distributed across the inverted hemisphere dome,
 * configured to blast outward and toward/behind the camera (+Z) when triggerSkyShatter() is invoked.
 */
export function createSkyShatterFragments(
  count: number = SKY_SHATTER_FRAGMENT_COUNT,
  domeRadius: number = 6.5
): SkyShatterState {
  const origins = new Float32Array(count * 3);
  const velocities = new Float32Array(count * 3);
  const rotations = new Float32Array(count * 3);
  const angularVelocities = new Float32Array(count * 3);
  const initialScales = new Float32Array(count);

  const goldenRatio = (1 + Math.sqrt(5)) / 2;

  for (let i = 0; i < count; i++) {
    const i3 = i * 3;
    // Fibonacci disk/dome distribution across the full camera sky frustum behind the anvil
    const u = (i + 0.5) / count;
    const r = Math.sqrt(u);
    const phi = (2 * Math.PI * i) / goldenRatio;

    const nx = r * Math.cos(phi);
    const ny = r * Math.sin(phi);
    const nz = -Math.sqrt(Math.max(0.05, 1.0 - r * r * 0.75));

    origins[i3] = nx * domeRadius * 0.95;
    origins[i3 + 1] = 0.25 + ny * (domeRadius * 0.52);
    origins[i3 + 2] = nz * 4.5 - 1.5;

    // Explosive velocity blasting radially outward and rushing toward/behind the camera (+Z)
    const speed = 4.0 + (i % 17) * 0.42;
    velocities[i3] = nx * speed * 1.25;
    velocities[i3 + 1] = ny * speed * 0.95 + 0.6;
    velocities[i3 + 2] = 5.8 + (i % 13) * 0.65; // Rush toward and behind camera (+Z)

    rotations[i3] = (i * 1.3) % (Math.PI * 2);
    rotations[i3 + 1] = (i * 2.1) % (Math.PI * 2);
    rotations[i3 + 2] = (i * 0.7) % (Math.PI * 2);

    angularVelocities[i3] = ((i % 7) - 3) * 2.8;
    angularVelocities[i3 + 1] = ((i % 9) - 4) * 2.5;
    angularVelocities[i3 + 2] = ((i % 5) - 2) * 3.2;

    initialScales[i] = 0.26 + (i % 9) * 0.042;
  }

  return {
    count,
    origins,
    velocities,
    rotations,
    angularVelocities,
    initialScales,
  };
}

export interface SkyShardTransform {
  x: number;
  y: number;
  z: number;
  rx: number;
  ry: number;
  rz: number;
  scale: number;
}

/**
 * Computes the position, rotation, and scale-to-0 of a single sky fragment at time elapsedSec.
 */
export function evaluateSkyShardTransform(
  state: SkyShatterState,
  index: number,
  elapsedSec: number,
  durationSec: number = SKY_SHATTER_DURATION_SEC
): SkyShardTransform {
  const i3 = index * 3;
  const clampedElapsed = Math.max(0, elapsedSec);
  const progress = Math.min(1.0, clampedElapsed / Math.max(0.05, durationSec));

  // Scale shrinks smoothly down to 0 as fragments fly past the camera
  const scaleFactor = Math.max(0, 1.0 - progress * progress);
  const scale = state.initialScales[index] * scaleFactor;

  return {
    x: state.origins[i3] + state.velocities[i3] * clampedElapsed,
    y:
      state.origins[i3 + 1] +
      state.velocities[i3 + 1] * clampedElapsed -
      0.5 * 3.2 * clampedElapsed * clampedElapsed,
    z: state.origins[i3 + 2] + state.velocities[i3 + 2] * clampedElapsed,
    rx: state.rotations[i3] + state.angularVelocities[i3] * clampedElapsed,
    ry: state.rotations[i3 + 1] + state.angularVelocities[i3 + 1] * clampedElapsed,
    rz: state.rotations[i3 + 2] + state.angularVelocities[i3 + 2] * clampedElapsed,
    scale,
  };
}

// ============================================================================
// MÁI VÒM THIÊN GIỚI NỨT VỠ (THE CELESTIAL SHATTERABLE SKY DOME)
// - uCrack increments by +0.05 per strike (0.0 -> 1.0)
// - 0.1s cyan lightning pillar ascent + radial shockwave
// - Grand Shatter Event at uCrack >= 1.0: 2,500 3D fragments + swirling nebula galaxy
// ============================================================================
export const CRACK_INCREMENT_PER_STRIKE = 0.05;
export const LIGHTNING_PILLAR_ASCENT_SEC = 0.1;
export const GRAND_SHATTER_SHARD_COUNT = 420;
export const FALLING_DEBRIS_BUFFER_SIZE = 280;

export interface VaultStrikeAdvanceResult {
  previousCrack: number;
  nextCrack: number;
  triggeredGrandShatter: boolean;
  strikeCount: number;
}

/**
 * Advances uCrack by +0.05 on each strike and flags when The Grand Shatter Event (uCrack >= 1.0) triggers.
 */
export function advanceVaultCrack(
  currentCrack: number,
  increment: number = CRACK_INCREMENT_PER_STRIKE
): VaultStrikeAdvanceResult {
  const clampedPrev = Math.max(0.0, Math.min(1.0, currentCrack));
  const rawNext = Number((clampedPrev + increment).toFixed(4));
  const nextCrack = Math.max(0.0, Math.min(1.0, rawNext));
  const triggeredGrandShatter = clampedPrev < 1.0 && nextCrack >= 1.0;

  return {
    previousCrack: clampedPrev,
    nextCrack,
    triggeredGrandShatter,
    strikeCount: Math.round(nextCrack / CRACK_INCREMENT_PER_STRIKE),
  };
}

// ============================================================================
// BÚA THẦN HƯ ẢNH (PHANTOM ASTRAL HAMMER) & VÒNG TRẬN PHÁP CỔ TỰ (RUNIC ASTROLABE)
// ============================================================================
export const PHANTOM_HAMMER_DOWNSTROKE_SEC = 0.085;
export const PHANTOM_HAMMER_REBOUND_SEC = 0.34;
export const PHANTOM_HAMMER_TOTAL_SEC =
  PHANTOM_HAMMER_DOWNSTROKE_SEC + PHANTOM_HAMMER_REBOUND_SEC;

export const ASTROLABE_RING_BASE_SPEEDS: readonly [number, number, number] = [
  0.42, // Inner Gold Solar Ring (CW)
  -0.68, // Middle Cyan Lightning Ring (CCW)
  0.31, // Outer Dual Celestial Ring (CW)
];

export type PhantomHammerPhase = 'IDLE' | 'DESCENDING' | 'IMPACT' | 'REBOUND_DISSOLVE';

export interface PhantomHammerFrameState {
  active: boolean;
  phase: PhantomHammerPhase;
  swingAngleRad: number; // 1.15 rad raised -> 0.0 rad impact on anvil -> 0.48 rad rebound
  heightOffset: number; // +2.2m above anvil -> 0.0m impact -> +0.75m dissolve
  scale: number;
  opacity: number;
  fresnelBoost: number;
  hasTriggeredLightning: boolean;
}

/**
 * Evaluates the Colossal Phantom Astral Hammer (Búa Thần Hư Ảnh) at `elapsedStrikeSec`:
 * - 0 <= t < 0.085s: Slams down from the heavens onto the anvil face BEFORE the lightning pillar shoots up.
 * - t >= 0.085s: Impact occurs on the anvil face, triggering the upward cyan lightning pillar, then rebounds & dissolves.
 */
export function evaluatePhantomHammerStrike(elapsedStrikeSec: number): PhantomHammerFrameState {
  if (elapsedStrikeSec < 0 || elapsedStrikeSec >= PHANTOM_HAMMER_TOTAL_SEC) {
    return {
      active: false,
      phase: 'IDLE',
      swingAngleRad: 1.15,
      heightOffset: 2.2,
      scale: 0.85,
      opacity: 0.0,
      fresnelBoost: 1.0,
      hasTriggeredLightning: false,
    };
  }

  if (elapsedStrikeSec < PHANTOM_HAMMER_DOWNSTROKE_SEC) {
    const t = Math.max(0, Math.min(1, elapsedStrikeSec / PHANTOM_HAMMER_DOWNSTROKE_SEC));
    // Accelerated power slam curve (cubic ease-in)
    const slamEase = t * t * (3.0 - 2.0 * t);
    const fastDrop = Math.pow(t, 1.65);

    return {
      active: true,
      phase: 'DESCENDING',
      swingAngleRad: 1.18 * (1.0 - fastDrop),
      heightOffset: 2.15 * (1.0 - fastDrop),
      scale: 0.92 + 0.16 * slamEase,
      opacity: Math.min(1.0, 0.35 + t * 0.95),
      fresnelBoost: 1.4 + t * 1.8,
      hasTriggeredLightning: false,
    };
  }

  const reboundElapsed = elapsedStrikeSec - PHANTOM_HAMMER_DOWNSTROKE_SEC;
  const r = Math.max(0, Math.min(1, reboundElapsed / PHANTOM_HAMMER_REBOUND_SEC));
  const easeOut = 1.0 - Math.pow(1.0 - r, 2.2);
  const fadeOut = Math.pow(1.0 - r, 1.55);

  return {
    active: true,
    phase: r < 0.16 ? 'IMPACT' : 'REBOUND_DISSOLVE',
    swingAngleRad: 0.46 * easeOut,
    heightOffset: 0.72 * easeOut,
    scale: 1.08 - 0.12 * easeOut,
    opacity: Number(fadeOut.toFixed(4)),
    fresnelBoost: 3.2 * fadeOut + 0.8,
    hasTriggeredLightning: true,
  };
}

export interface AstrolabeRingsState {
  anglesRad: [number, number, number]; // Counter-rotating [CW, CCW, CW]
  emissiveIntensity: number;
  speedMultiplier: number;
}

/**
 * Computes counter-rotating angles and emissive intensity for the 3-Ring Runic Astrolabe
 * surrounding the Anvil Pedestal, scaling with uCrack (0.0 -> 1.0) and strikeFlash.
 */
export function evaluateAstrolabeRings(
  elapsedSec: number,
  uCrack: number,
  strikeFlash: number = 0
): AstrolabeRingsState {
  const clampedCrack = Math.max(0.0, Math.min(1.0, uCrack));
  const clampedFlash = Math.max(0.0, strikeFlash);
  const speedMultiplier = Number((1.0 + clampedCrack * 2.4 + clampedFlash * 1.8).toFixed(4));
  const effectiveTime = Math.max(0, elapsedSec) * (1.0 + clampedCrack * 1.15);

  const anglesRad: [number, number, number] = [
    Number((effectiveTime * ASTROLABE_RING_BASE_SPEEDS[0]).toFixed(4)),
    Number((effectiveTime * ASTROLABE_RING_BASE_SPEEDS[1]).toFixed(4)),
    Number((effectiveTime * ASTROLABE_RING_BASE_SPEEDS[2]).toFixed(4)),
  ];

  const emissiveIntensity = Number(
    (0.85 + Math.pow(clampedCrack, 0.85) * 2.35 + clampedFlash * 1.9).toFixed(4)
  );

  return {
    anglesRad,
    emissiveIntensity,
    speedMultiplier,
  };
}

// ============================================================================
// SÉT PHÂN NHÁNH 3D THỰC THỤ (5 PROCEDURAL 3D JAGGED LIGHTNING ARCHETYPES)
// - Midpoint Displacement / Fractal 3D Lightning
// - 5 distinct visual forms sharing the Cyan (#00F0FF) & Imperial Gold (#FFD23F / #FF9E00) palette
// - Each strike randomly picks one of the 5 archetypes and generates ascending trunks +
//   mid-air fractal forks + Vault Creeper bolts crawling across the Sky Dome Voronoi cracks
// ============================================================================
export type LightningArchetypeId =
  | 'FRACTAL_CROWN'
  | 'TWIN_DRAGON_HELIX'
  | 'CELESTIAL_CAGE'
  | 'CHAIN_TEMPEST'
  | 'SPEAR_OF_JUDGMENT';

export interface LightningArchetypeMeta {
  id: LightningArchetypeId;
  nameVn: string;
  subtitleVn: string;
  trunkCount: number;
  forkCount: number;
  creeperCount: number;
  jitterAmplitude: number;
  goldRatio: number; // 0..1 mix of gold vs cyan bolts
}

export const LIGHTNING_ARCHETYPES: readonly LightningArchetypeMeta[] = [
  {
    id: 'FRACTAL_CROWN',
    nameVn: 'Thiên Lôi Phân Nhánh',
    subtitleVn: 'Trụ sét chính kết hợp 7 nhánh sét phân cực & rễ sét bò lan vòm trời',
    trunkCount: 2,
    forkCount: 6,
    creeperCount: 7,
    jitterAmplitude: 0.78,
    goldRatio: 0.3,
  },
  {
    id: 'TWIN_DRAGON_HELIX',
    nameVn: 'Song Long Lôi Xoắn',
    subtitleVn: 'Hai luồng thần lôi Lam – Kim xoắn kép cùng tia sét bắc cầu',
    trunkCount: 2,
    forkCount: 6,
    creeperCount: 6,
    jitterAmplitude: 0.52,
    goldRatio: 0.5,
  },
  {
    id: 'CELESTIAL_CAGE',
    nameVn: 'Bát Hoang Lôi Ngục',
    subtitleVn: '6 cột lôi điện uốn vòm từ trận pháp hội tụ lên đỉnh Thiên Môn',
    trunkCount: 6,
    forkCount: 4,
    creeperCount: 8,
    jitterAmplitude: 0.68,
    goldRatio: 0.38,
  },
  {
    id: 'CHAIN_TEMPEST',
    nameVn: 'Liên Hoàn Lôi Vũ',
    subtitleVn: '5 luồng sét gấp khúc chữ Z phóng đa điểm nảy qua không trung',
    trunkCount: 5,
    forkCount: 5,
    creeperCount: 7,
    jitterAmplitude: 1.05,
    goldRatio: 0.35,
  },
  {
    id: 'SPEAR_OF_JUDGMENT',
    nameVn: 'Thiên Phạt Lôi Thương',
    subtitleVn: 'Đại thương lôi điện hội tụ, nổ tung thành hoa sét 8 cánh trên vòm đá',
    trunkCount: 4,
    forkCount: 5,
    creeperCount: 8,
    jitterAmplitude: 0.42,
    goldRatio: 0.45,
  },
];

export type Vec3Tuple = [number, number, number];

export type LightningBoltTier = 'TRUNK' | 'FORK' | 'VAULT_CREEPER';

export interface ProceduralLightningBolt3D {
  tier: LightningBoltTier;
  points: Vec3Tuple[];
  widthStart: number;
  widthEnd: number;
  colorMix: number; // 0.0 = Pure Cyan (#00F0FF), 1.0 = Imperial Fire Gold (#FFD23F / #FF9E00)
  progressStart: number; // 0..1 normalized timing along the 0.1s strike
  progressEnd: number;
}

export interface ProceduralLightningBurst3D {
  archetype: LightningArchetypeMeta;
  bolts: ProceduralLightningBolt3D[];
  trunkBoltCount: number;
  forkBoltCount: number;
  creeperBoltCount: number;
}

function seededRand(seedObj: { s: number }): number {
  seedObj.s = (seedObj.s * 1664525 + 1013904223) >>> 0;
  return (seedObj.s & 0xfffffff) / 0x10000000;
}

/**
 * Picks a random LightningArchetypeMeta, avoiding repeating `previousId` consecutively.
 */
export function selectRandomLightningArchetype(
  previousId?: LightningArchetypeId | null,
  randomVal: number = Math.random()
): LightningArchetypeMeta {
  const candidates = previousId
    ? LIGHTNING_ARCHETYPES.filter((a) => a.id !== previousId)
    : LIGHTNING_ARCHETYPES;
  const idx = Math.min(
    candidates.length - 1,
    Math.max(0, Math.floor(randomVal * candidates.length))
  );
  return candidates[idx];
}

/**
 * Generates a 3D jagged polyline between `start` and `end` using recursive Midpoint Displacement
 * (subdivisions = 3 -> 9 points; subdivisions = 4 -> 17 points) with optional arch/helix offset.
 */
export function midpointDisplacement3D(
  start: Vec3Tuple,
  end: Vec3Tuple,
  subdivisions: number,
  jitterAmp: number,
  seedObj: { s: number }
): Vec3Tuple[] {
  let pts: Vec3Tuple[] = [start, end];
  let amp = jitterAmp;

  for (let step = 0; step < subdivisions; step++) {
    const nextPts: Vec3Tuple[] = [pts[0]];
    for (let i = 0; i < pts.length - 1; i++) {
      const a = pts[i];
      const b = pts[i + 1];
      const mx = (a[0] + b[0]) * 0.5 + (seededRand(seedObj) - 0.5) * 2.0 * amp;
      const my = (a[1] + b[1]) * 0.5 + (seededRand(seedObj) - 0.5) * 1.1 * amp;
      const mz = (a[2] + b[2]) * 0.5 + (seededRand(seedObj) - 0.5) * 1.6 * amp;
      nextPts.push([mx, my, mz], b);
    }
    pts = nextPts;
    amp *= 0.54;
  }

  return pts;
}

/**
 * Generates a complete 3D jagged lightning burst for any of the 5 archetypes:
 * 1. Ascending Trunks (Anvil -> Sky Vault Zenith)
 * 2. Mid-Air Fractal Forks (5-8 jagged branches splitting off into the sky)
 * 3. Vault Creeper Bolts (6-8 jagged arcs crawling across the curved Sky Dome Voronoi cracks)
 */
export function generateProcedural3DLightning(
  archetypeId: LightningArchetypeId,
  anvilPos: Vec3Tuple = [0, -2.02, 0.65],
  zenithPos: Vec3Tuple = [0, 5.4, -3.8],
  uCrack: number = 0.5,
  seed: number = Math.floor(Math.random() * 999999) + 1
): ProceduralLightningBurst3D {
  const archetype =
    LIGHTNING_ARCHETYPES.find((a) => a.id === archetypeId) ?? LIGHTNING_ARCHETYPES[0];
  const seedObj = { s: (seed ^ 0x9e3779b9) >>> 0 };
  const bolts: ProceduralLightningBolt3D[] = [];

  const dx = zenithPos[0] - anvilPos[0];
  const dy = zenithPos[1] - anvilPos[1];
  const dz = zenithPos[2] - anvilPos[2];

  // 1. ASCENDING TRUNKS (Shaped according to the specific Archetype)
  const mainTrunkPaths: Vec3Tuple[][] = [];

  for (let t = 0; t < archetype.trunkCount; t++) {
    const isGold = t % 2 === 1 || seededRand(seedObj) < archetype.goldRatio;
    const colorMix = isGold ? 0.88 : 0.05;

    if (archetype.id === 'TWIN_DRAGON_HELIX') {
      // Double Helix: Two dragon bolts coiling 2.5 turns around the central axis + midpoint jitter
      const segs = 18;
      const phaseOffset = t * Math.PI;
      const pts: Vec3Tuple[] = [];
      for (let s = 0; s <= segs; s++) {
        const u = s / segs;
        const envelope = Math.sin(u * Math.PI); // 0 at ends, 1 in middle
        const coilRadius = (0.55 + uCrack * 0.35) * envelope;
        const angle = u * Math.PI * 5.0 + phaseOffset;
        const jx = (seededRand(seedObj) - 0.5) * 0.28 * envelope;
        const jy = (seededRand(seedObj) - 0.5) * 0.18 * envelope;
        const jz = (seededRand(seedObj) - 0.5) * 0.28 * envelope;
        pts.push([
          anvilPos[0] + dx * u + Math.cos(angle) * coilRadius + jx,
          anvilPos[1] + dy * u + jy,
          anvilPos[2] + dz * u + Math.sin(angle) * coilRadius + jz,
        ]);
      }
      mainTrunkPaths.push(pts);
      bolts.push({
        tier: 'TRUNK',
        points: pts,
        widthStart: 0.24,
        widthEnd: 0.14,
        colorMix,
        progressStart: 0.0,
        progressEnd: 0.65,
      });
    } else if (archetype.id === 'CELESTIAL_CAGE') {
      // 6 wide arched cage pillars erupting from the Astrolabe perimeter around the anvil and converging at Zenith
      const cageAngle = (t / archetype.trunkCount) * Math.PI * 2 + (seededRand(seedObj) - 0.5) * 0.25;
      const baseStart: Vec3Tuple = [
        anvilPos[0] + Math.cos(cageAngle) * 1.45,
        anvilPos[1] + 0.05,
        anvilPos[2] + Math.sin(cageAngle) * 0.85,
      ];
      const rawPts = midpointDisplacement3D(baseStart, zenithPos, 4, archetype.jitterAmplitude, seedObj);
      // Bow the midpoints outward to form a grand arched thunder cage
      const bowedPts: Vec3Tuple[] = rawPts.map((pt, idx) => {
        const u = idx / (rawPts.length - 1);
        const arch = Math.sin(u * Math.PI) * (1.85 + uCrack * 0.65);
        return [
          pt[0] + Math.cos(cageAngle) * arch,
          pt[1] + Math.sin(u * Math.PI) * 0.45,
          pt[2] + Math.sin(cageAngle) * arch * 0.55,
        ];
      });
      mainTrunkPaths.push(bowedPts);
      bolts.push({
        tier: 'TRUNK',
        points: bowedPts,
        widthStart: 0.19,
        widthEnd: 0.12,
        colorMix,
        progressStart: 0.0,
        progressEnd: 0.68,
      });
    } else if (archetype.id === 'CHAIN_TEMPEST') {
      // Multi-Node Zigzag Ricochet bolts bouncing across mid-air relay nodes to a cluster around Zenith
      const targetSpread = 0.35 + (t === 0 ? 0 : 1.35);
      const targetAngle = (t / archetype.trunkCount) * Math.PI * 2 + seededRand(seedObj) * 0.5;
      const endPt: Vec3Tuple = [
        zenithPos[0] + Math.cos(targetAngle) * targetSpread,
        zenithPos[1] + Math.sin(targetAngle) * targetSpread * 0.45,
        zenithPos[2] - Math.abs(Math.sin(targetAngle)) * 0.5,
      ];
      const pts = midpointDisplacement3D(anvilPos, endPt, 4, archetype.jitterAmplitude, seedObj);
      mainTrunkPaths.push(pts);
      bolts.push({
        tier: 'TRUNK',
        points: pts,
        widthStart: 0.21,
        widthEnd: 0.12,
        colorMix,
        progressStart: 0.0,
        progressEnd: 0.64,
      });
    } else if (archetype.id === 'SPEAR_OF_JUDGMENT') {
      // Tightly braided high-density thunder spear converging on Zenith
      const startOffsetAngle = (t / archetype.trunkCount) * Math.PI * 2;
      const startPt: Vec3Tuple = [
        anvilPos[0] + Math.cos(startOffsetAngle) * 0.38,
        anvilPos[1],
        anvilPos[2] + Math.sin(startOffsetAngle) * 0.38,
      ];
      const pts = midpointDisplacement3D(startPt, zenithPos, 4, archetype.jitterAmplitude, seedObj);
      mainTrunkPaths.push(pts);
      bolts.push({
        tier: 'TRUNK',
        points: pts,
        widthStart: 0.26,
        widthEnd: 0.18,
        colorMix,
        progressStart: 0.0,
        progressEnd: 0.6,
      });
    } else {
      // FRACTAL_CROWN: Classic jagged central fractal bolt
      const pts = midpointDisplacement3D(
        anvilPos,
        zenithPos,
        4,
        archetype.jitterAmplitude * (t === 0 ? 0.85 : 1.15),
        seedObj
      );
      mainTrunkPaths.push(pts);
      bolts.push({
        tier: 'TRUNK',
        points: pts,
        widthStart: t === 0 ? 0.26 : 0.17,
        widthEnd: t === 0 ? 0.15 : 0.1,
        colorMix,
        progressStart: 0.0,
        progressEnd: 0.62,
      });
    }
  }

  // 2. MID-AIR FRACTAL FORKS (5–8 jagged branches splitting outward from the trunks)
  for (let f = 0; f < archetype.forkCount; f++) {
    const parentTrunk = mainTrunkPaths[f % mainTrunkPaths.length];
    const branchIdx = Math.max(
      2,
      Math.min(parentTrunk.length - 3, Math.floor((0.25 + (f / archetype.forkCount) * 0.55) * parentTrunk.length))
    );
    const forkOrigin = parentTrunk[branchIdx];
    const sideSign = f % 2 === 0 ? 1 : -1;
    const reachX = sideSign * (1.35 + seededRand(seedObj) * 2.4);
    const reachY = 1.1 + seededRand(seedObj) * 1.9;
    const reachZ = -0.6 - seededRand(seedObj) * 1.6;

    const forkEnd: Vec3Tuple = [
      forkOrigin[0] + reachX,
      forkOrigin[1] + reachY,
      forkOrigin[2] + reachZ,
    ];
    const forkPts = midpointDisplacement3D(forkOrigin, forkEnd, 3, 0.52, seedObj);
    const isGold = seededRand(seedObj) < archetype.goldRatio;

    bolts.push({
      tier: 'FORK',
      points: forkPts,
      widthStart: 0.14,
      widthEnd: 0.035,
      colorMix: isGold ? 0.92 : 0.1,
      progressStart: 0.18 + (f / archetype.forkCount) * 0.25,
      progressEnd: 0.78,
    });
  }

  // 3. VAULT CREEPER BOLTS (6–8 jagged Voronoi lightning tendrils crawling across the Sky Dome upon impact)
  const creeperSpread = 3.2 + uCrack * 3.6;
  for (let c = 0; c < archetype.creeperCount; c++) {
    const baseAngle =
      (c / archetype.creeperCount) * Math.PI * 2 + (seededRand(seedObj) - 0.5) * 0.35;
    const dist = creeperSpread * (0.72 + seededRand(seedObj) * 0.45);

    // Follow the concave inner curvature of the Sky Dome around zenithPos = (0, 5.4, -3.8)
    const cx = zenithPos[0] + Math.cos(baseAngle) * dist * 1.25;
    const cy = zenithPos[1] + Math.sin(baseAngle) * dist * 0.65 - (dist * dist) * 0.045;
    const cz = zenithPos[2] - Math.sin(baseAngle) * dist * 0.35 - (dist * dist) * 0.035;

    const creeperPts = midpointDisplacement3D(
      zenithPos,
      [cx, cy, cz],
      4,
      0.62 + uCrack * 0.35,
      seedObj
    );
    const isGold = c % 2 === 1 || seededRand(seedObj) < archetype.goldRatio;

    bolts.push({
      tier: 'VAULT_CREEPER',
      points: creeperPts,
      widthStart: 0.16,
      widthEnd: 0.03,
      colorMix: isGold ? 0.95 : 0.08,
      progressStart: 0.52,
      progressEnd: 1.0,
    });
  }

  return {
    archetype,
    bolts,
    trunkBoltCount: archetype.trunkCount,
    forkBoltCount: archetype.forkCount,
    creeperBoltCount: archetype.creeperCount,
  };
}

// ============================================================================
// 11. CINEMATIC POST-PROCESSING: SCREEN-SPACE SHOCKWAVE & CHROMATIC ABERRATION
// ============================================================================

export const POST_FX_SHOCKWAVE_DURATION_SEC = 0.56;

export interface CinematicPostFxState {
  active: boolean;
  /** Normalized progress (0..1) of the post-processing impact wave */
  progress: number;
  /** Expanding radial UV radius (0..1.25) from the Anvil impact center */
  anvilShockRadius: number;
  /** UV refraction warp intensity for the Anvil shockwave ring */
  anvilShockStrength: number;
  /** Expanding radial UV radius (0..1.05) from the Sky Vault Zenith impact center */
  zenithShockRadius: number;
  /** UV refraction warp intensity for the Zenith shockwave ring */
  zenithShockStrength: number;
  /** Radial RGB channel split offset intensity (Chromatic Aberration) */
  chromaticAberration: number;
  /** Brief screen-space radial compression pulse right at hammer contact */
  impactZoomPulse: number;
  /** Luminous cyan-gold prismatic air-compression crest brightness */
  crestGlowIntensity: number;
}

/**
 * Evaluates the screen-space refractive shockwave distortion and radial RGB
 * chromatic aberration triggered at the exact moment the Phantom Hammer strikes the Anvil.
 */
export function evaluateCinematicPostFx(
  impactElapsedSec: number,
  uCrack: number,
  isShattered = false
): CinematicPostFxState {
  const clampedCrack = Math.max(0, Math.min(1, uCrack));
  const baseCa = isShattered ? 0.0042 : 0.0012 + clampedCrack * 0.0026;

  if (impactElapsedSec < 0 || impactElapsedSec > POST_FX_SHOCKWAVE_DURATION_SEC) {
    return {
      active: false,
      progress: 0,
      anvilShockRadius: 0,
      anvilShockStrength: 0,
      zenithShockRadius: 0,
      zenithShockStrength: 0,
      chromaticAberration: Number(baseCa.toFixed(5)),
      impactZoomPulse: 0,
      crestGlowIntensity: 0,
    };
  }

  const progress = Math.max(0, Math.min(1, impactElapsedSec / POST_FX_SHOCKWAVE_DURATION_SEC));
  const crackBoost = 1.0 + clampedCrack * 0.55;
  const shatterBoost = isShattered ? 1.4 : 1.0;

  // 1. Primary Anvil Screen-Space Shockwave (expands immediately at t = 0.0s from Anvil face)
  const anvilEase = 1.0 - Math.pow(1.0 - progress, 2.35);
  const anvilShockRadius = 0.04 + anvilEase * 1.18;
  const anvilRampIn = Math.sin(Math.min(1.0, progress / 0.14) * (Math.PI * 0.5));
  const anvilEnvelope = anvilRampIn * Math.pow(1.0 - progress, 1.45);
  const anvilShockStrength = 0.068 * anvilEnvelope * crackBoost * shatterBoost;

  // 2. Secondary Sky Vault Zenith Screen-Space Shockwave (triggered ~0.075s later when lightning hits zenith)
  const zenithDelay = 0.075;
  const zenithProg =
    impactElapsedSec > zenithDelay
      ? Math.max(
          0,
          Math.min(
            1,
            (impactElapsedSec - zenithDelay) / (POST_FX_SHOCKWAVE_DURATION_SEC - zenithDelay)
          )
        )
      : 0;
  const zenithEase = 1.0 - Math.pow(1.0 - zenithProg, 2.15);
  const zenithShockRadius = zenithProg > 0 ? 0.05 + zenithEase * 0.98 : 0;
  const zenithRampIn =
    zenithProg > 0 ? Math.sin(Math.min(1.0, zenithProg / 0.16) * (Math.PI * 0.5)) : 0;
  const zenithEnvelope = zenithRampIn * Math.pow(1.0 - zenithProg, 1.5);
  const zenithShockStrength = 0.052 * zenithEnvelope * crackBoost * shatterBoost;

  // 3. Radial Chromatic Aberration (R/G/B split peaking on hammer impact and decaying smoothly)
  const caDecay = Math.pow(1.0 - progress, 1.65);
  const caSpike = Math.exp(-impactElapsedSec * 14.0) * 0.012;
  const chromaticAberration =
    baseCa + (0.022 * caDecay + caSpike) * crackBoost * (isShattered ? 1.35 : 1.0);

  // 4. Radial Impact Micro-Zoom Pulse & Prismatic Air-Compression Crest
  const impactZoomPulse =
    Math.sin(Math.min(1.0, progress / 0.28) * Math.PI) *
    Math.pow(1.0 - progress, 1.8) *
    0.026 *
    crackBoost;
  const crestGlowIntensity = Math.pow(1.0 - progress, 1.35) * (0.88 + clampedCrack * 0.52);

  return {
    active: true,
    progress: Number(progress.toFixed(4)),
    anvilShockRadius: Number(anvilShockRadius.toFixed(4)),
    anvilShockStrength: Number(anvilShockStrength.toFixed(5)),
    zenithShockRadius: Number(zenithShockRadius.toFixed(4)),
    zenithShockStrength: Number(zenithShockStrength.toFixed(5)),
    chromaticAberration: Number(chromaticAberration.toFixed(5)),
    impactZoomPulse: Number(impactZoomPulse.toFixed(5)),
    crestGlowIntensity: Number(crestGlowIntensity.toFixed(4)),
  };
}

// ============================================================================
// 12. PANORAMIC 2D CANVAS: "PHÁ TRỜI: ĐẠI CÔNG TRƯỜNG VẠN DÂN"
// ============================================================================

export const PANORAMA_SKY_RATIO = 0.65;
export const PANORAMA_GROUND_RATIO = 0.35;
export const HERO_STRIKE_DOWNSTROKE_SEC = 0.1;
export const HERO_STRIKE_TOTAL_SEC = 0.32;
export const SCREEN_SHAKE_DURATION_SEC = 0.15;
export const PANORAMA_BOSS_MAX_HP = 10000;

export type HeroStanceKey = 'Q' | 'W' | 'E' | 'R';

export interface HeroStancePalette {
  key: HeroStanceKey;
  id: 'THUNDER' | 'FIRE' | 'GRAVITY' | 'MYSTIC';
  nameVn: string;
  subtitleVn: string;
  rimHex: string;
  glowRgba: string;
  coreHex: string;
  sparkHex: string;
}

export const HERO_STANCE_PALETTES: Record<HeroStanceKey, HeroStancePalette> = {
  Q: {
    key: 'Q',
    id: 'THUNDER',
    nameVn: 'Lôi Đỉnh',
    subtitleVn: 'Xanh Lôi Điện · Tốc Kích Vòm Trời',
    rimHex: '#00F0FF',
    glowRgba: 'rgba(0, 240, 255, 0.55)',
    coreHex: '#E6FEFF',
    sparkHex: '#FFD166',
  },
  W: {
    key: 'W',
    id: 'FIRE',
    nameVn: 'Viêm Dương',
    subtitleVn: 'Đỏ Viêm Dương · Thiêu Đốt Thiên Thạch',
    rimHex: '#FF471A',
    glowRgba: 'rgba(255, 71, 26, 0.58)',
    coreHex: '#FFF0D4',
    sparkHex: '#FFB703',
  },
  E: {
    key: 'E',
    id: 'GRAVITY',
    nameVn: 'Trọng Lực',
    subtitleVn: 'Tím Trọng Lực · Chấn Động Không Gian',
    rimHex: '#B85CFF',
    glowRgba: 'rgba(184, 92, 255, 0.56)',
    coreHex: '#F5E8FF',
    sparkHex: '#E0AAFF',
  },
  R: {
    key: 'R',
    id: 'MYSTIC',
    nameVn: 'Huyền Âm',
    subtitleVn: 'Ngọc Bích Huyền Âm · Cộng Hưởng Vạn Dân',
    rimHex: '#10E8A5',
    glowRgba: 'rgba(16, 232, 165, 0.55)',
    coreHex: '#E2FFF5',
    sparkHex: '#80FFDB',
  },
};

export interface PeerBlacksmithActor {
  id: string;
  label: string;
  /** Normalized X across the panoramic basalt plateau (0.05..0.95), avoiding 0.43..0.57 center hero stage */
  xNorm: number;
  /** Normalized Y on the bottom 35% plateau (0.68..0.89) */
  yNorm: number;
  /** Terrace row depth (0 = back upper quartz step, 1 = mid step, 2 = foreground flank) */
  terraceRow: 0 | 1 | 2;
  /** Visual scale factor based on terrace depth */
  scale: number;
  /** Facing direction (1 = toward center-right, -1 = toward center-left) */
  facing: 1 | -1;
  /** Autonomous strike cycle period in seconds */
  strikePeriodSec: number;
  /** Phase offset in seconds so peers strike in lively staggered waves */
  strikeOffsetSec: number;
  /** Lightning tint for peer co-op network */
  beamColorHex: string;
}

const PEER_BADGE_NUMBERS = [
  4120, 8901, 2049, 7734, 1508, 6392, 9410, 3185, 5602, 8219,
  1074, 4826, 7190, 3942, 6015, 9284, 2761, 5340, 8647, 1933,
  7451, 3098, 6812, 4509,
];

/**
 * Generates 12 to 24 online peer blacksmiths positioned along the stepped
 * basalt and quartz terraces behind and flanking the Main Hero.
 */
export function createPeerBlacksmithTroupe(count = 18): PeerBlacksmithActor[] {
  const clampedCount = Math.max(12, Math.min(24, Math.floor(count)));
  const peers: PeerBlacksmithActor[] = [];

  for (let i = 0; i < clampedCount; i++) {
    const isLeftWing = i % 2 === 0;
    const wingIndex = Math.floor(i / 2);
    const wingsPerSide = Math.ceil(clampedCount / 2);
    const terraceRow = (i % 3) as 0 | 1 | 2;

    // Spread evenly across left wing (0.06 .. 0.39) and right wing (0.61 .. 0.94)
    const t = wingsPerSide > 1 ? wingIndex / (wingsPerSide - 1) : 0.5;
    const xNorm = isLeftWing
      ? 0.06 + t * 0.33 + (terraceRow - 1) * 0.012
      : 0.61 + t * 0.33 - (terraceRow - 1) * 0.012;

    // Stepped quartz terraces within the bottom 35% (yNorm from 0.685 to 0.855)
    const rowBaseY = terraceRow === 0 ? 0.695 : terraceRow === 1 ? 0.76 : 0.83;
    const yJitter = ((i * 37) % 9 - 4) * 0.0035;
    const yNorm = Number((rowBaseY + yJitter).toFixed(4));

    const scale = terraceRow === 0 ? 0.48 : terraceRow === 1 ? 0.6 : 0.72;
    const badgeNum = PEER_BADGE_NUMBERS[i % PEER_BADGE_NUMBERS.length];

    peers.push({
      id: `peer-${badgeNum}`,
      label: `Thợ Rèn #${badgeNum}`,
      xNorm: Number(xNorm.toFixed(4)),
      yNorm,
      terraceRow,
      scale,
      facing: isLeftWing ? 1 : -1,
      strikePeriodSec: Number((1.45 + ((i * 29) % 13) * 0.11).toFixed(2)),
      strikeOffsetSec: Number((((i * 43) % 17) * 0.14).toFixed(2)),
      beamColorHex: i % 3 === 0 ? '#7CE8FF' : i % 3 === 1 ? '#C4F5FF' : '#99D6FF',
    });
  }

  // Sort back-to-front by yNorm for painter's algorithm rendering
  return peers.sort((a, b) => a.yNorm - b.yNorm);
}

export interface Point2D {
  x: number;
  y: number;
}

export interface Procedural2DLightningBolt {
  mainPoints: Point2D[];
  branches: Point2D[][];
  isHero: boolean;
}

/**
 * Generates a realistic 2D jagged lightning bolt between (x1, y1) on the anvil
 * and (x2, y2) on the Sky Vault using midpoint displacement and fractal branching.
 */
export function generate2DLightningBolt(
  x1: number,
  y1: number,
  x2: number,
  y2: number,
  isHero: boolean,
  seed = Math.random() * 10000
): Procedural2DLightningBolt {
  let s = Math.floor(seed) || 1337;
  const nextRand = () => {
    s = (s * 1664525 + 1013904223) % 4294967296;
    return s / 4294967296;
  };

  const subdivide = (
    ax: number,
    ay: number,
    bx: number,
    by: number,
    depth: number,
    displace: number
  ): Point2D[] => {
    if (depth <= 0) {
      return [
        { x: ax, y: ay },
        { x: bx, y: by },
      ];
    }
    const mx = (ax + bx) * 0.5;
    const my = (ay + by) * 0.5;
    const dx = bx - ax;
    const dy = by - ay;
    const len = Math.hypot(dx, dy) || 1;
    // Perpendicular normal in 2D
    const nx = -dy / len;
    const ny = dx / len;
    const offset = (nextRand() - 0.5) * 2 * displace;
    const px = mx + nx * offset;
    const py = my + ny * offset * 0.35;

    const left = subdivide(ax, ay, px, py, depth - 1, displace * 0.54);
    const right = subdivide(px, py, bx, by, depth - 1, displace * 0.54);
    return [...left.slice(0, -1), ...right];
  };

  const totalDist = Math.hypot(x2 - x1, y2 - y1);
  const trunkDepth = isHero ? 5 : 4;
  const trunkJitter = totalDist * (isHero ? 0.16 : 0.11);
  const mainPoints = subdivide(x1, y1, x2, y2, trunkDepth, trunkJitter);

  const branches: Point2D[][] = [];
  const branchCount = isHero ? 5 : 2;

  for (let b = 0; b < branchCount; b++) {
    if (!mainPoints || mainPoints.length < 2) continue;
    const safeIdx = Math.max(
      0,
      Math.min(
        mainPoints.length - 1,
        Math.floor(mainPoints.length * (0.2 + (b / branchCount) * 0.62))
      )
    );
    const startPt = mainPoints[safeIdx];
    if (!startPt || typeof startPt.x !== 'number' || typeof startPt.y !== 'number') continue;
    const side = (b % 2 === 0 ? 1 : -1) * (nextRand() > 0.2 ? 1 : -1);
    const branchSpanX = side * totalDist * (isHero ? 0.14 + nextRand() * 0.14 : 0.08 + nextRand() * 0.08);
    const branchSpanY = -totalDist * (0.12 + nextRand() * 0.16);
    const endX = startPt.x + branchSpanX;
    const endY = Math.max(24, startPt.y + branchSpanY);

    branches.push(
      subdivide(startPt.x, startPt.y, endX, endY, isHero ? 3 : 2, totalDist * 0.055)
    );
  }

  return {
    mainPoints,
    branches,
    isHero,
  };
}

export interface Hero2DStrikePose {
  phase: 'IDLE' | 'DOWNSTROKE' | 'IMPACT' | 'RECOVERY';
  /** Hammer angle in radians: negative = raised behind head, +1.15 = slammed onto anvil */
  hammerAngleRad: number;
  /** Vertical torso breathing / slam offset in pixels */
  torsoOffsetY: number;
  /** Squash & stretch X/Y factors */
  scaleX: number;
  scaleY: number;
  /** Rim-light intensity multiplier */
  rimIntensity: number;
}

/**
 * Evaluates the Main Hero's 2D silhouette animation pose:
 * - Idle state: gentle breathing bob
 * - Strike state: 0.1s explosive downstroke onto the anvil followed by 0.22s rebound
 */
export function evaluateHero2DStrikePose(
  strikeElapsedSec: number,
  idleTimeSec: number
): Hero2DStrikePose {
  if (strikeElapsedSec < 0 || strikeElapsedSec > HERO_STRIKE_TOTAL_SEC) {
    const breath = Math.sin(idleTimeSec * 2.8);
    return {
      phase: 'IDLE',
      hammerAngleRad: -0.78 + breath * 0.06,
      torsoOffsetY: breath * 2.5,
      scaleX: 1.0 - breath * 0.015,
      scaleY: 1.0 + breath * 0.018,
      rimIntensity: 1.0 + Math.sin(idleTimeSec * 4.2) * 0.12,
    };
  }

  if (strikeElapsedSec <= HERO_STRIKE_DOWNSTROKE_SEC) {
    const p = Math.max(0, Math.min(1, strikeElapsedSec / HERO_STRIKE_DOWNSTROKE_SEC));
    // Fast windup snap in first 20%, then explosive slam down to anvil (+1.15 rad) by p = 0.9..1.0
    const downP = Math.min(1, Math.max(0, (p - 0.2) / 0.72));
    const slamCurve = p < 0.2 ? -1.35 - (p / 0.2) * 0.35 : -1.7 + Math.pow(downP, 1.55) * 2.85;
    return {
      phase: p >= 0.82 ? 'IMPACT' : 'DOWNSTROKE',
      hammerAngleRad: Number(slamCurve.toFixed(4)),
      torsoOffsetY: p < 0.2 ? -5 * (p / 0.2) : 9 * downP,
      scaleX: p >= 0.82 ? 1.14 : 0.92,
      scaleY: p >= 0.82 ? 0.88 : 1.09,
      rimIntensity: 2.2,
    };
  }

  const recProg =
    (strikeElapsedSec - HERO_STRIKE_DOWNSTROKE_SEC) /
    (HERO_STRIKE_TOTAL_SEC - HERO_STRIKE_DOWNSTROKE_SEC);
  const easeOut = 1 - Math.pow(1 - Math.min(1, recProg), 2.2);
  const angle = 1.15 * (1 - easeOut) + -0.78 * easeOut;

  return {
    phase: recProg < 0.18 ? 'IMPACT' : 'RECOVERY',
    hammerAngleRad: Number(angle.toFixed(4)),
    torsoOffsetY: 9 * (1 - easeOut),
    scaleX: 1.0 + 0.12 * (1 - easeOut),
    scaleY: 1.0 - 0.1 * (1 - easeOut),
    rimIntensity: 2.2 - easeOut * 1.1,
  };
}

export interface PanoramaBossDamageResult {
  nextHp: number;
  damageDealt: number;
  crackProgress: number;
  isDefeated: boolean;
}

export function applyPanoramaSkyStrikeDamage(
  currentHp: number,
  maxHp: number,
  isHero: boolean,
  rhythmMultiplier = 3.5
): PanoramaBossDamageResult {
  const safeMax = Math.max(1, maxHp);
  const baseDmg = isHero ? 140 : 12;
  const damageDealt = Math.round(baseDmg * (isHero ? rhythmMultiplier : 1.0));
  const nextHp = Math.max(0, currentHp - damageDealt);
  const crackProgress = Number(Math.max(0, Math.min(1, 1 - nextHp / safeMax)).toFixed(4));

  return {
    nextHp,
    damageDealt,
    crackProgress,
    isDefeated: nextHp <= 0,
  };
}

export interface SkyCrackBranch {
  points: Point2D[]; // Normalized coordinates (x: 0..1, y: 0..0.62)
  threshold: number; // Crack progress (0..1) at which this branch ignites
  weight: number;
}

/**
 * Pre-generates the deterministic tectonic fissure tree across the top 65% Sky Vault
 * so cracks spread organically from the Zenith as Boss HP drops from 100% to 0%.
 */
export function createSkyVaultCrackTree(): SkyCrackBranch[] {
  const branches: SkyCrackBranch[] = [];
  let seed = 90210;
  const rand = () => {
    seed = (seed * 1664525 + 1013904223) % 4294967296;
    return seed / 4294967296;
  };

  const subdivideCrack = (
    ax: number,
    ay: number,
    bx: number,
    by: number,
    depth: number,
    disp: number
  ): Point2D[] => {
    if (depth <= 0) {
      return [
        { x: ax, y: ay },
        { x: bx, y: by },
      ];
    }
    const mx = (ax + bx) * 0.5;
    const my = (ay + by) * 0.5;
    const dx = bx - ax;
    const dy = by - ay;
    const len = Math.hypot(dx, dy) || 1;
    const nx = -dy / len;
    const ny = dx / len;
    const off = (rand() - 0.5) * 2 * disp;
    const px = Math.max(0.03, Math.min(0.97, mx + nx * off));
    const py = Math.max(0.03, Math.min(0.61, my + ny * off));
    const left = subdivideCrack(ax, ay, px, py, depth - 1, disp * 0.55);
    const right = subdivideCrack(px, py, bx, by, depth - 1, disp * 0.55);
    return [...left.slice(0, -1), ...right];
  };

  const zenithX = 0.5;
  const zenithY = 0.14;
  const primaryRayCount = 14;

  for (let i = 0; i < primaryRayCount; i++) {
    const baseAngle = -Math.PI * 0.06 + (i / (primaryRayCount - 1)) * (Math.PI * 1.12);
    const maxLen = 0.25 + (i % 3) * 0.11 + rand() * 0.08;
    const endX = Math.max(0.05, Math.min(0.95, zenithX + Math.cos(baseAngle) * maxLen * 1.38));
    const endY = Math.max(0.04, Math.min(0.59, zenithY + Math.sin(baseAngle) * maxLen * 0.88));

    const pts = subdivideCrack(zenithX, zenithY, endX, endY, 4, 0.042);

    branches.push({
      points: pts,
      threshold: (i % 4) * 0.05,
      weight: 2.8,
    });

    // Spawn jagged secondary sub-fissure forks along the main crack
    const forkIndices = [5, 10, 13];
    for (const fIdx of forkIndices) {
      if (fIdx >= pts.length) continue;
      const origin = pts[fIdx];
      const forkSign = (i + fIdx) % 2 === 0 ? 1 : -1;
      const forkAngle = baseAngle + forkSign * (0.52 + rand() * 0.42);
      const forkLen = 0.09 + rand() * 0.08;
      const fx = Math.max(0.03, Math.min(0.97, origin.x + Math.cos(forkAngle) * forkLen * 1.25));
      const fy = Math.max(0.03, Math.min(0.61, origin.y + Math.sin(forkAngle) * forkLen));
      const forkPts = subdivideCrack(origin.x, origin.y, fx, fy, 3, 0.022);
      branches.push({
        points: forkPts,
        threshold: Math.min(0.9, (fIdx / pts.length) * 0.65 + (i % 3) * 0.08),
        weight: 1.45,
      });
    }
  }

  return branches;
}
