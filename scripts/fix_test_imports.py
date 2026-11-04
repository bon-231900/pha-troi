# -*- coding: utf-8 -*-
with open('frontend/src/game/rules.test.ts', 'r', encoding='utf-8') as f:
    c = f.read()

# Remove the require block
c = c.replace("""  const {
    getItemRarityMeta,
    getSalvageYield,
    FLOOR_TIER_DROP_WEIGHTS,
    rollLootDrop,
    openWorldRaidClearChest,
    ascendEquipmentTier,
    getMaxInventorySlots,
    generateProceduralItem
  } = require('./rules');""", "// imports from rules.ts")

# Add imports to top
to_import = """import {
  getItemRarityMeta,
  getSalvageYield,
  FLOOR_TIER_DROP_WEIGHTS,
  rollLootDrop,
  openWorldRaidClearChest,
  ascendEquipmentTier,
  getMaxInventorySlots,
  generateProceduralItem,"""

c = c.replace("import {", to_import, 1)

with open('frontend/src/game/rules.test.ts', 'w', encoding='utf-8') as f:
    f.write(c)
print("Updated rules.test.ts imports successfully.")
