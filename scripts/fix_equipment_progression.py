# -*- coding: utf-8 -*-
"""
Script to fix the equipment progression pipeline so that:
1. All 6 slots are guaranteed to be populated (auto-healing empty/null slots with INITIAL_EQUIPPED_SLOTS).
2. The Selected Relic Forge Station (Tôi Luyện & Khảm Phù Thạch) ALWAYS displays with full upgrade controls.
3. The player can immediately temper, ascend, and socket gems.
"""
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# -------------------------------------------------------------------------
# 1. Update frontend/src/game/rules.ts with ensureAllEquippedSlots
# -------------------------------------------------------------------------
RULES_FILE = r'frontend\src\game\rules.ts'
with open(RULES_FILE, 'r', encoding='utf-8') as f:
    rules_code = f.read()

ensure_func = """export function ensureAllEquippedSlots(
  rawEquipped?: Record<string, any> | null
): Record<EquipmentSlotKey, EquipmentItem> {
  const result: Record<EquipmentSlotKey, EquipmentItem> = { ...INITIAL_EQUIPPED_SLOTS };
  if (rawEquipped && typeof rawEquipped === 'object') {
    for (const key of Object.keys(INITIAL_EQUIPPED_SLOTS) as EquipmentSlotKey[]) {
      const item = rawEquipped[key];
      if (item && typeof item === 'object' && item.id) {
        result[key] = {
          ...INITIAL_EQUIPPED_SLOTS[key],
          ...item,
          level: typeof item.level === 'number' && item.level >= 1 ? item.level : 1,
          unlockedSockets: typeof item.unlockedSockets === 'number' ? item.unlockedSockets : getUnlockedSockets(item.rarity || 'common'),
          sockets: Array.isArray(item.sockets) ? item.sockets : [],
        };
      }
    }
  }
  return result;
}

export function calculateArsenalBonuses("""

if "export function ensureAllEquippedSlots" not in rules_code:
    rules_code = rules_code.replace("export function calculateArsenalBonuses(", ensure_func)
    with open(RULES_FILE, 'w', encoding='utf-8') as f:
        f.write(rules_code)
    print("[+] Added ensureAllEquippedSlots to rules.ts")
else:
    print("[i] ensureAllEquippedSlots already in rules.ts")

# -------------------------------------------------------------------------
# 2. Update frontend/src/game/characterSlots.ts to use ensureAllEquippedSlots
# -------------------------------------------------------------------------
SLOTS_FILE = r'frontend\src\game\characterSlots.ts'
with open(SLOTS_FILE, 'r', encoding='utf-8') as f:
    slots_code = f.read()

if "ensureAllEquippedSlots" not in slots_code:
    slots_code = slots_code.replace(
        "INITIAL_EQUIPPED_SLOTS,\n",
        "INITIAL_EQUIPPED_SLOTS,\n  ensureAllEquippedSlots,\n"
    )
    slots_code = slots_code.replace(
        "equippedItems: parsed.equippedItems && typeof parsed.equippedItems === 'object' ? parsed.equippedItems : INITIAL_EQUIPPED_SLOTS,",
        "equippedItems: ensureAllEquippedSlots(parsed.equippedItems),"
    )
    slots_code = slots_code.replace(
        "slot.progress.equippedItems = INITIAL_EQUIPPED_SLOTS;",
        "slot.progress.equippedItems = ensureAllEquippedSlots(slot.progress.equippedItems);"
    )
    with open(SLOTS_FILE, 'w', encoding='utf-8') as f:
        f.write(slots_code)
    print("[+] Updated characterSlots.ts with ensureAllEquippedSlots")

# -------------------------------------------------------------------------
# 3. Update frontend/src/App.tsx to ensure equippedItems is always healed
# -------------------------------------------------------------------------
APP_FILE = r'frontend\src\App.tsx'
with open(APP_FILE, 'r', encoding='utf-8') as f:
    app_code = f.read()

if "ensureAllEquippedSlots" not in app_code:
    app_code = app_code.replace(
        "INITIAL_EQUIPPED_SLOTS,\n",
        "INITIAL_EQUIPPED_SLOTS,\n  ensureAllEquippedSlots,\n"
    )

old_app_init = """  // ARPG Equipment & Backpack State (Procedural Drops & Affixes)
  const [equippedItems, setEquippedItems] = useState<Record<EquipmentSlotKey, EquipmentItem | null>>(() => {
    try {
      const s = getInitialSaveString();
      if (s) {
        const parsed = JSON.parse(s);
        if (parsed.equippedItems && typeof parsed.equippedItems === 'object') {
          return parsed.equippedItems;
        }
      }
    } catch {}
    return INITIAL_EQUIPPED_SLOTS;
  });"""

new_app_init = """  // ARPG Equipment & Backpack State (Procedural Drops & Affixes)
  const [equippedItems, setEquippedItems] = useState<Record<EquipmentSlotKey, EquipmentItem>>(() => {
    try {
      const s = getInitialSaveString();
      if (s) {
        const parsed = JSON.parse(s);
        return ensureAllEquippedSlots(parsed?.equippedItems);
      }
    } catch {}
    return ensureAllEquippedSlots(null);
  });"""

if old_app_init in app_code:
    app_code = app_code.replace(old_app_init, new_app_init)
    print("[+] Healed App.tsx useState initialization for equippedItems")

# Also heal slot switching in App.tsx line 1157
app_code = app_code.replace(
    "setEquippedItems(prog.equippedItems && typeof prog.equippedItems === 'object' ? prog.equippedItems : INITIAL_EQUIPPED_SLOTS);",
    "setEquippedItems(ensureAllEquippedSlots(prog.equippedItems));"
)

with open(APP_FILE, 'w', encoding='utf-8') as f:
    f.write(app_code)
print("[+] App.tsx updated successfully!")

# -------------------------------------------------------------------------
# 4. Update frontend/src/components/RightProgressionPanel.tsx
# -------------------------------------------------------------------------
PANEL_FILE = r'frontend\src\components\RightProgressionPanel.tsx'
with open(PANEL_FILE, 'r', encoding='utf-8') as f:
    panel_code = f.read()

# Add INITIAL_EQUIPPED_SLOTS import
if "INITIAL_EQUIPPED_SLOTS" not in panel_code:
    panel_code = panel_code.replace(
        "getUnlockedSockets,\n",
        "getUnlockedSockets,\n  INITIAL_EQUIPPED_SLOTS,\n"
    )

# In the 6 items map:
old_card_item = "const item = equippedItems[slotKey];"
new_card_item = "const item = equippedItems[slotKey] || INITIAL_EQUIPPED_SLOTS[slotKey];"
if old_card_item in panel_code:
    panel_code = panel_code.replace(old_card_item, new_card_item)
    print("[+] Card loop item fallback to INITIAL_EQUIPPED_SLOTS")

# In the selected weapon station:
old_selected_station = """            {/* 3. BÀN RÈN & NÂNG CẤP KHÍ GIỚI ĐƯỢC CHỌN (SELECTED WEAPON STATION) */}
            {(() => {
              const item = equippedItems[selectedSlotKey];
              if (!item) return null;"""

new_selected_station = """            {/* 3. BÀN RÈN & NÂNG CẤP KHÍ GIỚI ĐƯỢC CHỌN (SELECTED WEAPON STATION) */}
            {(() => {
              const item = equippedItems[selectedSlotKey] || INITIAL_EQUIPPED_SLOTS[selectedSlotKey];"""

if old_selected_station in panel_code:
    panel_code = panel_code.replace(old_selected_station, new_selected_station)
    print("[+] Selected weapon station now guaranteed to render")

# In rune pouch socket check:
old_pouch_selected = "const currentSelected = equippedItems[selectedSlotKey];"
new_pouch_selected = "const currentSelected = equippedItems[selectedSlotKey] || INITIAL_EQUIPPED_SLOTS[selectedSlotKey];"
if old_pouch_selected in panel_code:
    panel_code = panel_code.replace(old_pouch_selected, new_pouch_selected)
    print("[+] Rune pouch socket check now guaranteed to have selected weapon")

with open(PANEL_FILE, 'w', encoding='utf-8') as f:
    f.write(panel_code)

print("[SUCCESS] All equipment progression pipeline fixes applied successfully!")
