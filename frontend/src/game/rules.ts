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
