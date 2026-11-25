import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import {
  getItemRarityMeta,
  getSalvageYield,
  rollLootDrop,
  openWorldRaidClearChest,
  ascendEquipmentTier,
  getMaxInventorySlots,
  generateProceduralItem,
  computeRaidContributionScore,
  CELESTIAL_VAULTS,
  BOSS_FLOOR_1_MAX_HP,
  getAtmosphericSealLayer,
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
  OVERDRIVE_TOTAL_CAP,
  getOverdriveTier,
  getPlayerClass,
  INITIAL_EQUIPPED_SLOTS,
  ensureAllEquippedSlots,
  calculateArsenalBonuses,
  type PlayerClassId,
  type EquipmentItem,
} from './rules';
import {
  SKILL_ART_MAP,
  getSkillArt,
  UI_FRAME_ASSETS,
  type SkillSlotKey,
} from './skillArtAssets';

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
  const wOutcome = calculateStrikeOutcome({
    grade: 'PERFECT',
    stance: 'W',
    basePower: 10,
    combo: 7,
    overdriveCharge: 7.2,
    overdriveActive: false,
    bossShieldPct: 50,
    spiritBonusMult: 1.2,
    globalBurstActive: false,
  });

  assert.equal(wOutcome.nextCombo, 8);
  assert.equal(wOutcome.nextOverdriveCharge, OVERDRIVE_MAX);
  assert.equal(wOutcome.triggeredOverdrive, true);
  assert.ok(wOutcome.damage > 0);
  assert.ok(wOutcome.linhThachEarned > 0);
  assert.ok(wOutcome.tinhHoaEarned >= 0);

  const qOutcome = calculateStrikeOutcome({
    grade: 'PERFECT',
    stance: 'Q',
    basePower: 10,
    combo: 7,
    overdriveCharge: 7,
    overdriveActive: false,
    bossShieldPct: 50,
    spiritBonusMult: 1.2,
    globalBurstActive: false,
  });

  assert.equal(qOutcome.nextCombo, 8);
  assert.equal(qOutcome.nextOverdriveCharge, 8.2);
  assert.equal(qOutcome.triggeredOverdrive, true);
  assert.ok(qOutcome.damage > 0);
  assert.ok(qOutcome.linhThachEarned > 0);

  const wBelowOutcome = calculateStrikeOutcome({
    grade: 'PERFECT',
    stance: 'W',
    basePower: 10,
    combo: 7,
    overdriveCharge: 5,
    overdriveActive: false,
    bossShieldPct: 50,
    spiritBonusMult: 1.2,
    globalBurstActive: false,
  });

  assert.equal(wBelowOutcome.nextOverdriveCharge, 5.8);
  assert.equal(wBelowOutcome.triggeredOverdrive, false);
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

test('v3.3 Single-Class commitment and 3-Tier Overcharge Gauge work deterministically', () => {
  // 1. Verify 4 classes exist with dedicated 4 skills each
  const classIds = ['thunder', 'fire', 'gravity', 'mystic'] as const;
  assert.equal(classIds.length, 4);

  classIds.forEach((cId) => {
    const cls = getPlayerClass(cId);
    assert.equal(cls.id, cId);
    assert.ok(cls.name.length > 0);
    assert.ok(cls.skills.Q.slot === 'Q');
    assert.ok(cls.skills.W.slot === 'W');
    assert.ok(cls.skills.E.slot === 'E');
    assert.ok(cls.skills.R.slot === 'R');
    assert.equal(cls.skills.Q.unlockLevel, 1);
    assert.equal(cls.skills.W.unlockLevel, 20);
    assert.equal(cls.skills.E.unlockLevel, 40);
    assert.equal(cls.skills.R.unlockLevel, 80);
    assert.ok(cls.subClasses.a.name.length > 0);
    assert.ok(cls.subClasses.b.name.length > 0);
  });

  // 2. Verify 3-Tier Overcharge Gauge transitions
  assert.equal(OVERDRIVE_TOTAL_CAP, 24);

  // Tier 1: 0 - 8
  const tier1 = getOverdriveTier(5);
  assert.equal(tier1.tier, 1);
  assert.equal(tier1.tierCharge, 5);
  assert.equal(tier1.isEmpoweredE, false);
  assert.equal(tier1.canUseR, false);

  // Tier 2: 8 - 16
  const tier2 = getOverdriveTier(12);
  assert.equal(tier2.tier, 2);
  assert.equal(tier2.tierCharge, 4);
  assert.equal(tier2.isEmpoweredE, true);
  assert.equal(tier2.canUseR, false);

  // Tier 3: 16 - 24
  const tier3 = getOverdriveTier(24);
  assert.equal(tier3.tier, 3);
  assert.equal(tier3.tierCharge, 8);
  assert.equal(tier3.isEmpoweredE, true);
  assert.equal(tier3.canUseR, true);
});

test('skillArtAssets maps all 4 PlayerClassId keys to distinct Q/W/E/R icon paths without falling back to flame', () => {
  const expectedPrefixes: Record<PlayerClassId, string> = {
    thunder: 'skill_thunder_',
    fire: 'skill_flame_',
    gravity: 'skill_mountain_',
    mystic: 'skill_music_',
  };
  const slots: readonly SkillSlotKey[] = ['Q', 'W', 'E', 'R'];

  assert.deepEqual(
    Object.keys(SKILL_ART_MAP).sort(),
    (['fire', 'gravity', 'mystic', 'thunder'] as const).slice().sort()
  );

  const collectedIcons = new Set<string>();

  for (const [classId, expectedPrefix] of Object.entries(expectedPrefixes) as Array<[PlayerClassId, string]>) {
    assert.ok(Object.prototype.hasOwnProperty.call(SKILL_ART_MAP, classId));

    for (const slot of slots) {
      const mapEntry = SKILL_ART_MAP[classId][slot];
      const resolved = getSkillArt(classId, slot);
      const expectedIcon = `./assets/art/ui/skills/${expectedPrefix}${slot.toLowerCase()}.webp`;

      assert.equal(mapEntry.icon, expectedIcon);
      assert.deepEqual(resolved, mapEntry);
      assert.ok(mapEntry.borderColor.startsWith('#'));
      assert.ok(mapEntry.glowColor.startsWith('rgba('));

      if (classId !== 'fire') {
        assert.equal(mapEntry.icon.includes('skill_flame_'), false);
      }
      collectedIcons.add(mapEntry.icon);
    }
  }

  assert.equal(collectedIcons.size, 16);
});

test('getSkillArt resolves legacy class aliases and falls back to thunder for unknown classes', () => {
  const slots: readonly SkillSlotKey[] = ['Q', 'W', 'E', 'R'];
  const legacyPairs: Array<[string, PlayerClassId]> = [
    ['flame', 'fire'],
    ['mountain', 'gravity'],
    ['music', 'mystic'],
  ];

  for (const slot of slots) {
    for (const [alias, canonical] of legacyPairs) {
      assert.deepEqual(getSkillArt(alias, slot), SKILL_ART_MAP[canonical][slot]);
    }

    assert.deepEqual(getSkillArt('unknown_class', slot), SKILL_ART_MAP.thunder[slot]);
    assert.deepEqual(getSkillArt('', slot), SKILL_ART_MAP.thunder[slot]);
  }
});

test('SKILL_ART_MAP and UI_FRAME_ASSETS reference existing non-empty files under frontend/public/assets', () => {
  const testDir = path.dirname(fileURLToPath(import.meta.url));
  const publicDir = path.resolve(testDir, '../../public');
  const slots: readonly SkillSlotKey[] = ['Q', 'W', 'E', 'R'];
  const classIds: readonly PlayerClassId[] = ['thunder', 'fire', 'gravity', 'mystic'];

  const assetPaths: string[] = [];
  for (const classId of classIds) {
    for (const slot of slots) {
      assetPaths.push(SKILL_ART_MAP[classId][slot].icon);
    }
  }
  assetPaths.push(...Object.values(UI_FRAME_ASSETS));

  assert.equal(assetPaths.length, 23);

  for (const assetPath of assetPaths) {
    assert.ok(assetPath.startsWith('./assets/'), `Expected ./assets/ prefix for ${assetPath}`);
    const fileOnDisk = path.resolve(publicDir, assetPath.slice(2));
    assert.equal(fs.existsSync(fileOnDisk), true, `Missing asset file: ${fileOnDisk}`);
    const stat = fs.statSync(fileOnDisk);
    assert.equal(stat.isFile(), true, `Expected regular file: ${fileOnDisk}`);
    assert.ok(stat.size > 0, `Expected non-empty file: ${fileOnDisk}`);
  }
});

test('CELESTIAL_VAULTS floors 2..9 scale 30% HP threshold above BOSS_FLOOR_1_MAX_HP * 0.3 and preserve getAtmosphericSealLayer ratios', () => {
  assert.equal(CELESTIAL_VAULTS.length, 9);
  assert.equal(CELESTIAL_VAULTS[0].id, 1);
  assert.equal(CELESTIAL_VAULTS[0].maxHp, BOSS_FLOOR_1_MAX_HP);
  assert.equal(CELESTIAL_VAULTS[0].maxHp * 0.3, BOSS_FLOOR_1_MAX_HP * 0.3);

  let previousMaxHp = 0;
  for (const vault of CELESTIAL_VAULTS) {
    assert.ok(vault.maxHp > previousMaxHp, `Expected Floor ${vault.id} maxHp to increase strictly`);
    previousMaxHp = vault.maxHp;

    const thirtyPctHp = vault.maxHp * 0.3;
    if (vault.id >= 2) {
      assert.ok(vault.maxHp > BOSS_FLOOR_1_MAX_HP);
      assert.ok(
        thirtyPctHp > BOSS_FLOOR_1_MAX_HP * 0.3,
        `Floor ${vault.id} 30% HP (${thirtyPctHp}) should exceed Floor 1 30% HP (${BOSS_FLOOR_1_MAX_HP * 0.3})`
      );
      if (vault.id >= 3) {
        assert.ok(thirtyPctHp > BOSS_FLOOR_1_MAX_HP);
      }

      // Calling without vault.maxHp falls back to BOSS_FLOOR_1_MAX_HP and misclassifies 30% HP as Layer 1.
      const fallbackDefaultSeal = getAtmosphericSealLayer(thirtyPctHp);
      assert.equal(fallbackDefaultSeal.id, 1);
    }

    // Passing vault.maxHp preserves exact 4-layer seal percentages across every floor 1..9.
    assert.equal(getAtmosphericSealLayer(vault.maxHp, vault.maxHp).id, 1);
    assert.equal(getAtmosphericSealLayer(vault.maxHp * 0.8, vault.maxHp).damageReductionPct, 80);

    assert.equal(getAtmosphericSealLayer(vault.maxHp * 0.75, vault.maxHp).id, 2);
    assert.equal(getAtmosphericSealLayer(vault.maxHp * 0.6, vault.maxHp).damageReductionPct, 60);

    assert.equal(getAtmosphericSealLayer(vault.maxHp * 0.5, vault.maxHp).id, 3);
    const layerAt30Pct = getAtmosphericSealLayer(thirtyPctHp, vault.maxHp);
    assert.equal(layerAt30Pct.id, 3);
    assert.equal(layerAt30Pct.damageReductionPct, 40);

    assert.equal(getAtmosphericSealLayer(vault.maxHp * 0.25, vault.maxHp).id, 4);
    assert.equal(getAtmosphericSealLayer(vault.maxHp * 0.1, vault.maxHp).damageReductionPct, 0);
    assert.equal(getAtmosphericSealLayer(0, vault.maxHp).id, 4);
  }
});

test('ensureAllEquippedSlots safely restores partial/legacy equipped items and never throws in calculateArsenalBonuses', () => {
  const legacySave: Record<string, unknown> = {
    hammer: {
      id: 'legacy_hammer_1',
      slotKey: 'hammer',
      name: 'Cổ Chùy Truyền Thuyết',
      rarity: 'epic',
      baseStatValue: 25,
    },
    relic: {
      id: 'legacy_relic_1',
      slotKey: 'relic',
      name: 'Cổ Bảo Thái Cổ',
      rarity: 'legendary',
      baseStatValue: 18,
      setId: 'set_thunder',
    },
    // Invalid entry with empty id should fall back to INITIAL_EQUIPPED_SLOTS.apron
    apron: {
      id: '',
      name: 'Broken Apron',
    },
  };

  const restored = ensureAllEquippedSlots(legacySave);

  for (const slotKey of Object.keys(INITIAL_EQUIPPED_SLOTS) as Array<keyof typeof INITIAL_EQUIPPED_SLOTS>) {
    const item = restored[slotKey];
    assert.ok(item, `Expected slot ${slotKey} to be populated`);
    assert.equal(Array.isArray(item.prefixes), true, `Expected prefixes array on ${slotKey}`);
    assert.equal(Array.isArray(item.suffixes), true, `Expected suffixes array on ${slotKey}`);
  }

  for (const restoredKey of ['hammer', 'relic'] as const) {
    const item = restored[restoredKey];
    assert.equal(Array.isArray(item.sockets), true, `Expected sockets array on ${restoredKey}`);
    assert.equal(typeof item.level, 'number');
    assert.ok((item.level ?? 0) >= 1);
  }

  assert.equal(restored.hammer.id, 'legacy_hammer_1');
  assert.deepEqual(restored.hammer.prefixes, []);
  assert.deepEqual(restored.hammer.suffixes, []);
  assert.deepEqual(restored.hammer.sockets, []);
  assert.equal(restored.hammer.unlockedSockets, 3);
  assert.equal(restored.hammer.baseStatLabel, INITIAL_EQUIPPED_SLOTS.hammer.baseStatLabel);
  assert.equal(restored.hammer.baseStatUnit, INITIAL_EQUIPPED_SLOTS.hammer.baseStatUnit);

  assert.equal(restored.relic.id, 'legacy_relic_1');
  assert.deepEqual(restored.relic.prefixes, []);
  assert.deepEqual(restored.relic.suffixes, []);
  assert.deepEqual(restored.relic.sockets, []);
  assert.equal(restored.relic.unlockedSockets, 4);

  assert.equal(restored.apron.id, INITIAL_EQUIPPED_SLOTS.apron.id);

  assert.doesNotThrow(() => {
    const bonuses = calculateArsenalBonuses(restored);
    assert.equal(bonuses.totalEquippedCount, 6);
    assert.equal(bonuses.flatDamage, 25);
  });

  // Also ensure null/undefined input restores all starter slots cleanly
  const fromNull = ensureAllEquippedSlots(null);
  assert.equal(fromNull.hammer.id, INITIAL_EQUIPPED_SLOTS.hammer.id);
  assert.doesNotThrow(() => calculateArsenalBonuses(fromNull));
});

test('Thiên Lôi 2/6 set bonus adds +5% critChancePct alongside +12% synergyChargeBonusPct in calculateArsenalBonuses', () => {
  const hammerPiece: EquipmentItem = {
    id: 'test_thunder_hammer',
    slotKey: 'hammer',
    slotName: 'Thần Chùy',
    baseName: 'Lôi Chùy',
    name: 'Lôi Chùy',
    rarity: 'rare',
    itemLevel: 10,
    baseStatLabel: 'Sát Thương Cơ Bản',
    baseStatValue: 10,
    baseStatUnit: 'Sát Thương',
    prefixes: [],
    suffixes: [],
    sockets: [],
    loreDescription: 'Test hammer',
    setId: 'set_thunder',
    setName: 'Thiên Lôi Phá Khởi',
  };

  const relicNoSet: EquipmentItem = {
    id: 'test_neutral_relic',
    slotKey: 'relic',
    slotName: 'Định Thiên Pháp Bảo',
    baseName: 'Ngọc Bội',
    name: 'Ngọc Bội',
    rarity: 'rare',
    itemLevel: 10,
    baseStatLabel: 'Khuếch Đại Uy Lực',
    baseStatValue: 0,
    baseStatUnit: '% Tổng Sát Thương',
    prefixes: [],
    suffixes: [],
    sockets: [],
    loreDescription: 'Test relic without set',
  };

  const relicThunderSet: EquipmentItem = {
    ...relicNoSet,
    id: 'test_thunder_relic',
    setId: 'set_thunder',
    setName: 'Thiên Lôi Phá Khởi',
  };

  const onePiece = calculateArsenalBonuses([hammerPiece, relicNoSet]);
  assert.equal(onePiece.setCounts.set_thunder, 1);
  assert.equal(onePiece.critChancePct, 3);
  assert.equal(onePiece.synergyChargeBonusPct, 0);
  assert.equal(onePiece.activeSetPerks.some((p) => p.startsWith('Thiên Lôi 2/6')), false);

  const twoPieces = calculateArsenalBonuses([hammerPiece, relicThunderSet]);
  assert.equal(twoPieces.setCounts.set_thunder, 2);
  assert.equal(twoPieces.critChancePct - onePiece.critChancePct, 5);
  assert.equal(twoPieces.synergyChargeBonusPct - onePiece.synergyChargeBonusPct, 12);
  assert.equal(twoPieces.critChancePct, 8);
  assert.equal(twoPieces.synergyChargeBonusPct, 12);
  assert.equal(
    twoPieces.activeSetPerks.includes('Thiên Lôi 2/6: +12% Nạp Cực Nhịp (SPI) & +5% Tỷ Lệ Bạo Kích'),
    true
  );
});
