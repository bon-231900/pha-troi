# -*- coding: utf-8 -*-
with open('frontend/src/game/rules.test.ts', 'r', encoding='utf-8') as f:
    test_code = f.read()

old_import = """  advanceVaultCrack,
} from './rules';"""

new_import = """  advanceVaultCrack,
  OVERDRIVE_TOTAL_CAP,
  getOverdriveTier,
  PLAYER_CLASSES,
  getPlayerClass,
} from './rules';"""

test_code = test_code.replace(old_import, new_import, 1)

new_test = """
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
"""

test_code += new_test

with open('frontend/src/game/rules.test.ts', 'w', encoding='utf-8') as f:
    f.write(test_code)

print("Added v3.3 tests!")
