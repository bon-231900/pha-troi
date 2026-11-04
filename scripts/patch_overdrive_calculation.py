# -*- coding: utf-8 -*-
with open('frontend/src/game/rules.ts', 'r', encoding='utf-8') as f:
    code = f.read()

target = """  // 2. Overdrive Charging
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
  const overdriveMult = isOverdriveNow ? 2.0 : 1.0;"""

replacement = """  // 2. 3-Tier Overdrive Charging (Up to 24 points: Tier 1: 8, Tier 2: 16, Tier 3: 24)
  const baseChargeGain = isGolden ? (input.stance === 'Q' ? 1.5 : 1.0) : 0.5;
  let nextOverdriveCharge = Math.min(OVERDRIVE_TOTAL_CAP, input.overdriveCharge + baseChargeGain);
  let triggeredOverdrive = false;

  if (nextOverdriveCharge >= 8 && input.overdriveCharge < 8) {
    triggeredOverdrive = true;
  }

  const tier = getOverdriveTier(nextOverdriveCharge);
  const overdriveMult = tier.tier === 3 ? 2.5 : tier.tier === 2 ? 1.8 : (nextOverdriveCharge >= 8 || input.overdriveActive ? 1.35 : 1.0);"""

if target in code:
    code = code.replace(target, replacement, 1)
    with open('frontend/src/game/rules.ts', 'w', encoding='utf-8') as f:
        f.write(code)
    print("Updated 3-Tier Overdrive calculation in rules.ts!")
else:
    print("Warning: target not found in rules.ts")
