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

export interface StrikeInput {
  grade: JudgmentGrade;
  stance: StanceKey;
  basePowerBillions: number; // e.g. 0.45B
  combo: number;
  overdriveCharge: number; // 0 to 8
  overdriveActive: boolean;
  bossShieldPct: number; // 0 to 100
  spiritBonusMult: number; // >= 1.0
  globalBurstActive: boolean;
}

export interface StrikeOutcome {
  damageBillions: number;
  displayMultiplier: number;
  nextCombo: number;
  nextOverdriveCharge: number;
  triggeredOverdrive: boolean;
  shieldDepletion: number;
  synergyGain: number;
  linhThachEarned: number;
  tinhHoaEarned: number;
}

export function calculateStrikeOutcome(input: StrikeInput): StrikeOutcome {
  const stanceCfg = HAMMER_STANCES[input.stance];

  if (input.grade === 'MISS') {
    return {
      damageBillions: 0,
      displayMultiplier: 0,
      nextCombo: 0,
      nextOverdriveCharge: Math.max(0, input.overdriveCharge - 1),
      triggeredOverdrive: false,
      shieldDepletion: 0,
      synergyGain: 0,
      linhThachEarned: 0,
      tinhHoaEarned: 0,
    };
  }

  const gradeMult = input.grade === 'PERFECT' ? 3.5 : 1.5;
  const nextCombo = input.combo + 1;
  const comboScaling = 1 + Math.min(nextCombo, 100) * 0.015;

  const chargeGain = input.grade === 'PERFECT' ? 1 : 0.5;
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
  const globalBurstMult = input.globalBurstActive ? 2.5 : 1.0;

  // When Boss Energy Shield is intact (> 0%), damage is mitigated by 35%, when broken (0%), damage gets 1.5x vulnerability bonus
  const shieldStateMult = input.bossShieldPct > 0 ? 0.65 : 1.5;

  const rawDamage =
    input.basePowerBillions *
    gradeMult *
    stanceCfg.damageMult *
    comboScaling *
    overdriveMult *
    globalBurstMult *
    shieldStateMult *
    input.spiritBonusMult;

  const damageBillions = Number(rawDamage.toFixed(4));

  const baseShieldDepletion = input.grade === 'PERFECT' ? 3.2 : 1.2;
  const shieldDepletion = Number(
    (baseShieldDepletion * stanceCfg.shieldMult * (isOverdriveNow ? 1.5 : 1.0)).toFixed(2)
  );

  const baseSynergy = input.grade === 'PERFECT' ? 2.4 : 0.9;
  const synergyGain = Number((baseSynergy * stanceCfg.synergyMult).toFixed(2));

  const baseLinhThach = input.grade === 'PERFECT' ? 45 : 18;
  const linhThachEarned = Math.round(
    baseLinhThach * stanceCfg.resourceMult * comboScaling * (isOverdriveNow ? 1.5 : 1.0)
  );

  const tinhHoaEarned =
    input.grade === 'PERFECT'
      ? Math.max(1, Math.round(2 * stanceCfg.resourceMult * (isOverdriveNow ? 2 : 1)))
      : 0;

  return {
    damageBillions,
    displayMultiplier: Number((gradeMult * (isOverdriveNow ? 2 : 1)).toFixed(1)),
    nextCombo,
    nextOverdriveCharge,
    triggeredOverdrive,
    shieldDepletion,
    synergyGain,
    linhThachEarned,
    tinhHoaEarned,
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
  powerPerLevel: number; // in Billions HP per strike
}

export const INITIAL_UPGRADES: ForgeUpgrade[] = [
  {
    id: 'celestial_hammer_core',
    name: 'Lõi Búa Thiên Thạch',
    subtitle: '+0.18B Sát thương cơ bản mỗi cấp',
    level: 1,
    maxLevel: 50,
    baseCost: 80,
    costScale: 1.35,
    powerPerLevel: 0.18,
  },
  {
    id: 'thunder_quench_oil',
    name: 'Dầu Tôi Lôi Đình',
    subtitle: '+0.32B Công lực khi đập trúng nhịp',
    level: 1,
    maxLevel: 40,
    baseCost: 160,
    costScale: 1.42,
    powerPerLevel: 0.32,
  },
  {
    id: 'nine_heavens_bellows',
    name: 'Ống Bễ Cửu Trọng Thiên',
    subtitle: '+0.65B Sức công phá lò rèn thần hỏa',
    level: 0,
    maxLevel: 30,
    baseCost: 350,
    costScale: 1.5,
    powerPerLevel: 0.65,
  },
  {
    id: 'ancient_anvil_rune',
    name: 'Cổ Văn Mặt Đe',
    subtitle: '+1.20B Cộng hưởng sát thương vạn dân',
    level: 0,
    maxLevel: 25,
    baseCost: 800,
    costScale: 1.58,
    powerPerLevel: 1.2,
  },
];

export function getUpgradeCost(upgrade: ForgeUpgrade): number {
  return Math.round(upgrade.baseCost * Math.pow(upgrade.costScale, upgrade.level));
}

export function calculateBasePowerBillions(upgrades: ForgeUpgrade[]): number {
  const base = 0.35;
  const bonus = upgrades.reduce((sum, u) => sum + u.level * u.powerPerLevel, 0);
  return Number((base + bonus).toFixed(3));
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
    unlocked: true,
  },
  {
    id: 'node_thunder_eye',
    name: 'Lôi Nhãn Tinh Quân',
    constellation: 'Tả Tinh · Lôi Điện',
    description: 'Mở rộng cảm ứng nhịp điệu, tăng +30% công lực Lôi Điện.',
    costTinhHoa: 4,
    bonusMult: 0.3,
    x: 24,
    y: 58,
    requires: 'node_origin',
    unlocked: false,
  },
  {
    id: 'node_crimson_furnace',
    name: 'Xích Đế Lò Luyện',
    constellation: 'Hữu Tinh · Thiên Hỏa',
    description: 'Nhiệt độ lò rèn vượt ngưỡng, tăng +35% sát thương lên Boss.',
    costTinhHoa: 4,
    bonusMult: 0.35,
    x: 76,
    y: 58,
    requires: 'node_origin',
    unlocked: false,
  },
  {
    id: 'node_shatter_star',
    name: 'Phá Quân Tinh Hồn',
    constellation: 'Trung Tinh · Phá Giáp',
    description: 'Cộng hưởng trọng lực, tăng +45% tổng sát thương và xuyên giáp.',
    costTinhHoa: 8,
    bonusMult: 0.45,
    x: 50,
    y: 38,
    requires: 'node_origin',
    unlocked: false,
  },
  {
    id: 'node_sky_breaker',
    name: 'Cửu Trọng Phá Thiên',
    constellation: 'Đỉnh Tinh · Chí Tôn',
    description: 'Đỉnh cao thần kỹ Vạn Dân Hợp Lực, nhân thêm +80% công lực toàn diện.',
    costTinhHoa: 15,
    bonusMult: 0.8,
    x: 50,
    y: 14,
    requires: 'node_shatter_star',
    unlocked: false,
  },
];

export function canUnlockSpiritNode(
  nodeId: string,
  nodes: SpiritNode[],
  currentTinhHoa: number
): boolean {
  const target = nodes.find((n) => n.id === nodeId);
  if (!target || target.unlocked) return false;
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

export function formatBillionsHP(billions: number): string {
  return `${Math.max(0, billions).toFixed(2)}B`;
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

