import test from 'node:test';
import assert from 'node:assert/strict';
import {
  getItemRarityMeta,
  getSalvageYield,
  FLOOR_TIER_DROP_WEIGHTS,
  rollLootDrop,
  openWorldRaidClearChest,
  ascendEquipmentTier,
  getMaxInventorySlots,
  generateProceduralItem,
  computeRaidContributionScore,
  CELESTIAL_VAULTS,
  judgeRhythmWave,
  calculateStrikeOutcome,
  TARGET_RIM_PROGRESS,
  OVERDRIVE_MAX,
  getUpgradeCost,
  calculateBasePower,
  INITIAL_UPGRADES,
  INITIAL_SPIRIT_NODES,
  canUnlockSpiritNode,
  calculateSpiritMultiplier,
  formatCountdown,
  FORGE_BPM,
  getBpmWaveSpeed,
  computeHammerStrikeAngle,
  HAMMER_IDLE_ANGLE_RAD,
  HAMMER_DOWNSTROKE_SEC,
  HAMMER_STANCES,
  FORGE_SPARK_BUFFER_SIZE,
  createForgeSparkBuffer,
  spawnForgeSparkBurst,
  computeSparkBallisticPosition,
  SKY_SHATTER_FRAGMENT_COUNT,
  SKY_SHATTER_DURATION_SEC,
  computeCrackProgress,
  createSkyShatterFragments,
  evaluateSkyShardTransform,
  CRACK_INCREMENT_PER_STRIKE,
  LIGHTNING_PILLAR_ASCENT_SEC,
  GRAND_SHATTER_SHARD_COUNT,
  advanceVaultCrack,
} from './rules';

test('judgeRhythmWave returns PERFECT (x3.5) inside the golden anvil rim tolerance', () => {
  const exact = judgeRhythmWave(TARGET_RIM_PROGRESS);
  assert.equal(exact.grade, 'PERFECT');
  assert.equal(exact.multiplier, 3.5);
  assert.equal(exact.labelVn, 'HOÀNG KIM');

  const slightEarly = judgeRhythmWave(TARGET_RIM_PROGRESS - 0.05);
  assert.equal(slightEarly.grade, 'PERFECT');
});

test('judgeRhythmWave returns GREAT (x1.5) in warm zone and MISS (x0) outside', () => {
  const warm = judgeRhythmWave(TARGET_RIM_PROGRESS - 0.12);
  assert.equal(warm.grade, 'GREAT');
  assert.equal(warm.multiplier, 1.5);
  assert.equal(warm.labelVn, 'CHUẨN XÁC');

  const missFar = judgeRhythmWave(0.2);
  assert.equal(missFar.grade, 'MISS');
  assert.equal(missFar.multiplier, 0);
});

test('calculateStrikeOutcome triggers Overdrive at 8/8 and scales x3.5 on Perfect', () => {
  const outcome = calculateStrikeOutcome({
    grade: 'PERFECT',
    stance: 'W',
    basePower: 10,
    combo: 7,
    overdriveCharge: 7,
    overdriveActive: false,
    bossShieldPct: 50,
    spiritBonusMult: 1.2,
    globalBurstActive: false,
  });

  assert.equal(outcome.nextCombo, 8);
  assert.equal(outcome.nextOverdriveCharge, OVERDRIVE_MAX);
  assert.equal(outcome.triggeredOverdrive, true);
  assert.ok(outcome.damage > 0);
  assert.ok(outcome.linhThachEarned > 0);
  assert.ok(outcome.tinhHoaEarned >= 0);
});

test('calculateStrikeOutcome resets combo to 0 on MISS', () => {
  const missOutcome = calculateStrikeOutcome({
    grade: 'MISS',
    stance: 'Q',
    basePower: 10,
    combo: 14,
    overdriveCharge: 5,
    overdriveActive: false,
    bossShieldPct: 50,
    spiritBonusMult: 1.2,
    globalBurstActive: false,
  });

  assert.equal(missOutcome.nextCombo, 0);
  assert.equal(missOutcome.damage, 0);
  assert.equal(missOutcome.nextOverdriveCharge, 3);
  assert.equal(missOutcome.anvilDamage, 5);
});

test('upgrade cost, spirit constellation, and 0.08s Divine Hammer strike curve work deterministically', () => {
  const firstUpgrade = INITIAL_UPGRADES[0];
  const costLv1 = getUpgradeCost(firstUpgrade);
  assert.equal(costLv1, firstUpgrade.baseCost);
  const costLv2 = getUpgradeCost({ ...firstUpgrade, level: 2 });
  assert.ok(costLv2 > firstUpgrade.baseCost);

  const basePower = calculateBasePower(INITIAL_UPGRADES);
  assert.ok(basePower > 0.5);

  assert.equal(canUnlockSpiritNode('node_thunder_eye', INITIAL_SPIRIT_NODES, 10), true);
  assert.equal(canUnlockSpiritNode('node_sky_breaker', INITIAL_SPIRIT_NODES, 50), false);

  const mult = calculateSpiritMultiplier(INITIAL_SPIRIT_NODES);
  assert.equal(mult, 1.2);
  assert.equal(formatCountdown(180), '03:00');
  assert.equal(FORGE_BPM, 100);
  assert.ok(Math.abs(getBpmWaveSpeed(100) - 100 / 120) < 0.001);

  // Verify 4 stance skins mapping
  assert.equal(HAMMER_STANCES.Q.stanceId, 'THUNDER');
  assert.equal(HAMMER_STANCES.W.stanceId, 'FIRE');
  assert.equal(HAMMER_STANCES.E.stanceId, 'GRAVITY');
  assert.equal(HAMMER_STANCES.R.stanceId, 'MYSTIC');

  // Verify 45-degree idle angle and 0.08s perpendicular impact (0 rad)
  assert.ok(Math.abs(computeHammerStrikeAngle(-1, 0) - HAMMER_IDLE_ANGLE_RAD) < 0.0001);
  assert.ok(Math.abs(computeHammerStrikeAngle(HAMMER_DOWNSTROKE_SEC, 0) - 0) < 0.0001);
  assert.ok(Math.abs(computeHammerStrikeAngle(0.5, 0) - HAMMER_IDLE_ANGLE_RAD) < 0.0001);
});

test('3,000-particle Float32Array Spark Buffer differentiates Self Golden Sparks vs Peer Ghost Sparks and follows gravity', () => {
  const buf = createForgeSparkBuffer();
  assert.equal(buf.capacity, 3000);
  assert.equal(FORGE_SPARK_BUFFER_SIZE, 3000);
  assert.equal(buf.positions.length, 9000);
  assert.equal(buf.velocities.length, 9000);
  assert.equal(buf.colors.length, 9000);
  assert.equal(buf.timings.length, 9000);
  assert.equal(buf.alphas.length, 3000);

  const selfBurst = spawnForgeSparkBurst(buf, {
    origin: 'SELF',
    quality: 'PERFECT',
    currentTime: 2.5,
  });

  const peerBurst = spawnForgeSparkBurst(buf, {
    origin: 'PEER',
    quality: 'GREAT',
    currentTime: 2.6,
  });

  // Self sparks must be larger and brighter than Peer Ghost Sparks
  assert.ok(selfBurst.avgPointSize > peerBurst.avgPointSize * 1.8);
  assert.ok(selfBurst.avgAlpha > peerBurst.avgAlpha * 1.8);

  // Verify upward launch velocity vy > 0
  assert.ok(buf.velocities[1] > 2.5);

  // Verify ballistic arc: rises initially then falls under gravity
  const [, yPeak] = computeSparkBallisticPosition(0, 0.38, 0, 1.0, 4.9, 0, 0.5, 9.8);
  const [, yFall] = computeSparkBallisticPosition(0, 0.38, 0, 1.0, 4.9, 0, 1.2, 9.8);
  assert.ok(yPeak > 0.38);
  assert.ok(yFall < yPeak);
});

test('Shatterable Sky Dome uCrackProgress and 1,500 Voronoi fragments scale to 0 and blast past camera', () => {
  assert.equal(computeCrackProgress(1000, 1000), 0.0);
  assert.equal(computeCrackProgress(650, 1000), 0.35);
  assert.equal(computeCrackProgress(150, 1000), 0.85);
  assert.equal(computeCrackProgress(0, 1000), 1.0);

  const shatter = createSkyShatterFragments();
  assert.equal(shatter.count, 1500);
  assert.equal(SKY_SHATTER_FRAGMENT_COUNT, 1500);

  const t0 = evaluateSkyShardTransform(shatter, 0, 0);
  const tMid = evaluateSkyShardTransform(shatter, 0, 1.0);
  const tEnd = evaluateSkyShardTransform(shatter, 0, SKY_SHATTER_DURATION_SEC);

  // Fragments blast backward toward/past camera (+Z) and shrink scale down to 0
  assert.ok(tMid.z > t0.z);
  assert.ok(tMid.scale < t0.scale);
  assert.equal(tEnd.scale, 0);
});

test('Celestial Vault uCrack increments by +0.05 per strike and triggers 420-shard high-shader Grand Shatter at 1.0', () => {
  assert.equal(CRACK_INCREMENT_PER_STRIKE, 0.05);
  assert.equal(LIGHTNING_PILLAR_ASCENT_SEC, 0.1);
  assert.equal(GRAND_SHATTER_SHARD_COUNT, 420);

  const s1 = advanceVaultCrack(0.0);
  assert.equal(s1.nextCrack, 0.05);
  assert.equal(s1.triggeredGrandShatter, false);

  const s20 = advanceVaultCrack(0.95);
  assert.equal(s20.nextCrack, 1.0);
  assert.equal(s20.triggeredGrandShatter, true);
  assert.equal(s20.strikeCount, 20);

  const shardSet = createSkyShatterFragments(GRAND_SHATTER_SHARD_COUNT);
  assert.equal(shardSet.count, 420);
});




test('v3.1 World Raid mechanics compute correct RCS and vault 9 tiers', () => {
  // imports at top
  assert.equal(CELESTIAL_VAULTS.length, 9);
  assert.equal(CELESTIAL_VAULTS[0].maxHp, 1_500_000_000);
  assert.equal(CELESTIAL_VAULTS[0].armorBreakMaxPoints, 500);
  assert.equal(CELESTIAL_VAULTS[0].armorRegenPerSec, 15);
  assert.equal(CELESTIAL_VAULTS[8].maxHp, 2_500_000_000_000);
  assert.equal(CELESTIAL_VAULTS[8].armorBreakMaxPoints, 18000);
  assert.equal(CELESTIAL_VAULTS[8].armorRegenPerSec, 380);

  // RCS formula: Damage*1.0 + BreakPoints*25,000 + HeatPumped*15,000 + AnvilRepaired*2.0
  const rcs = computeRaidContributionScore(100, 2, 5, 20);
  // 100 + 50,000 + 75,000 + 40 = 125,140
  assert.equal(rcs, 125140);
});

test('v3.2 MMORPG drop tables, 6 tiers (E -> S) and pity counter work deterministically', () => {
// imports from rules.ts

  // 1. Tiers verification
  const metaE = getItemRarityMeta('common');
  assert.equal(metaE.tier, 'E');
  assert.equal(metaE.label, 'Tier E · Phàm Thiết');

  const metaD = getItemRarityMeta('uncommon');
  assert.equal(metaD.tier, 'D');
  assert.equal(metaD.label, 'Tier D · Tinh Thiết');

  const metaS = getItemRarityMeta('mythic');
  assert.equal(metaS.tier, 'S');
  assert.equal(metaS.label, 'Tier S · Thiên Đạo Thần Khí');

  // 2. Salvage yields verification
  const salvageS = getSalvageYield({ rarity: 'mythic' });
  assert.equal(salvageS.ironDust, 1000);
  assert.equal(salvageS.celestialStar, 1);
  assert.equal(salvageS.tinhHoa, 20);

  const salvageE = getSalvageYield({ rarity: 'common' });
  assert.equal(salvageE.ironDust, 5);
  assert.equal(salvageE.linhThach, 10);

  // 3. Max inventory capacity expansion (24 -> 64)
  assert.equal(getMaxInventorySlots(1), 24);
  assert.equal(getMaxInventorySlots(5), 40);
  assert.equal(getMaxInventorySlots(10), 60);

  // 4. Pity counter: at 200 drops without Tier A+, guaranteed Tier A
  const pityResult = rollLootDrop({
    grade: 'PERFECT',
    isShieldBreak: true,
    anvilPityCount: 199,
    vaultFloorId: 1
  });
  assert.ok(pityResult.item !== null);
  assert.equal(pityResult.item.rarity, 'legendary');
  assert.equal(pityResult.newPityCount, 0);
  assert.equal(pityResult.isPityTriggered, true);

  // 5. World Raid Clear Chest
  const chestReward = openWorldRaidClearChest({
    rank: 'S',
    vaultFloorId: 3,
    raidPityCount: 10,
    playerStance: 'W'
  });
  assert.equal(chestReward.items.length, 5);
  assert.equal(chestReward.ironDustReward, 600);
  assert.equal(chestReward.raidPityGranted, 3);

  // 6. Tier A -> Tier S Ascension
  const itemA = generateProceduralItem({ minRarity: 'legendary' });
  const itemS = ascendEquipmentTier(itemA);
  assert.ok(itemS !== null);
  assert.equal(itemS.rarity, 'mythic');
  assert.ok(itemS.baseStatValue > itemA.baseStatValue);
});
