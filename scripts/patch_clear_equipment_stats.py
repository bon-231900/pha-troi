# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# 1. Update rules.ts
with open('frontend/src/game/rules.ts', 'r', encoding='utf-8') as f:
    rules = f.read()

# Update SLOT_INFO
old_slot_info = """export const SLOT_INFO: Record<EquipmentSlotKey, { name: string; icon: string; statLabel: string; statUnit: string }> = {
  hammer: { name: 'Thần Chùy', icon: 'Hammer', statLabel: 'Sát Thương Cơ Bản', statUnit: 'DMG' },
  anvil: { name: 'Thần Đe', icon: 'Shield', statLabel: 'Tỷ Lệ Bạo Kích', statUnit: '%' },
  bellows: { name: 'Hỏa Lò', icon: 'Flame', statLabel: 'Tích Nhiệt Đe', statUnit: '°C/hit' },
  gauntlets: { name: 'Bao Tay Rèn', icon: 'Zap', statLabel: 'Tỷ Lệ Bạo Kích', statUnit: '%' },
  apron: { name: 'Tạp Dề Thiết Hộ', icon: 'Layers', statLabel: 'Linh Thạch Treo Máy', statUnit: 'LT/phút' },
  relic: { name: 'Định Thiên Pháp Bảo', icon: 'Sparkles', statLabel: 'Sát Thương Toàn Thể', statUnit: '%' },
};"""

new_slot_info = """export const SLOT_INFO: Record<EquipmentSlotKey, { name: string; icon: string; statLabel: string; statUnit: string }> = {
  hammer: { name: 'Thần Chùy', icon: 'Hammer', statLabel: 'Sát Thương Cơ Bản', statUnit: 'Sát Thương' },
  anvil: { name: 'Thần Đe', icon: 'Shield', statLabel: 'Tỷ Lệ Bạo Kích', statUnit: '% Bạo Kích' },
  bellows: { name: 'Hỏa Lò', icon: 'Flame', statLabel: 'Bơm Nhiệt Lò Rèn', statUnit: '°C Lửa / nhát' },
  gauntlets: { name: 'Bao Tay Rèn', icon: 'Zap', statLabel: 'Tỷ Lệ Bạo Kích', statUnit: '% Bạo Kích' },
  apron: { name: 'Tạp Dề Thiết Hộ', icon: 'Layers', statLabel: 'Thu Thập Tự Động', statUnit: 'Linh Thạch / phút' },
  relic: { name: 'Định Thiên Pháp Bảo', icon: 'Sparkles', statLabel: 'Khuếch Đại Uy Lực', statUnit: '% Tổng Sát Thương' },
};

/**
 * Format any equipment item's base stat into crystal clear, human-readable Vietnamese.
 */
export function formatItemDisplayStat(item?: EquipmentItem | null, slotKey?: EquipmentSlotKey): {
  statLabel: string;
  displayValue: string;
  unit: string;
  explanation: string;
} {
  const key = (item?.slotKey || slotKey || 'hammer') as EquipmentSlotKey;
  const val = item?.baseStatValue ?? 1;

  switch (key) {
    case 'hammer':
      return {
        statLabel: 'Sát Thương Cơ Bản',
        displayValue: `+${val} Sát Thương`,
        unit: 'Sát Thương',
        explanation: 'Tăng lực đập trực tiếp vào Mái Vòm Thiên Giới',
      };
    case 'anvil':
      return {
        statLabel: 'Tỷ Lệ Bạo Kích',
        displayValue: `+${val}% Bạo Kích`,
        unit: '% Bạo Kích',
        explanation: 'Tăng cơ hội giáng đòn chí mạng nhân đôi sát thương',
      };
    case 'bellows':
      return {
        statLabel: 'Bơm Nhiệt Lò Rèn',
        displayValue: `+${val}°C Lửa / nhát`,
        unit: '°C Lửa / nhát',
        explanation: 'Tăng nhiệt độ Lò Rèn mỗi khi đập búa để nung chảy vòm trời',
      };
    case 'gauntlets':
      return {
        statLabel: 'Tỷ Lệ Bạo Kích',
        displayValue: `+${val}% Bạo Kích`,
        unit: '% Bạo Kích',
        explanation: 'Gia tăng cơ hội xuất hiện đòn đánh Bạo Kích',
      };
    case 'apron':
      return {
        statLabel: 'Thu Thập Tự Động',
        displayValue: `+${val} Linh Thạch / phút`,
        unit: 'Linh Thạch / phút',
        explanation: 'Tự động tích lũy Linh Thạch ngay cả khi rảnh tay hoặc AFK',
      };
    case 'relic':
      return {
        statLabel: 'Khuếch Đại Uy Lực',
        displayValue: `+${val}% Tổng Sát Thương`,
        unit: '% Tổng Sát Thương',
        explanation: 'Tăng % toàn bộ sát thương của tất cả các chiêu thức',
      };
    default:
      return {
        statLabel: item?.baseStatLabel || 'Chỉ Số',
        displayValue: `+${val} ${item?.baseStatUnit || ''}`.trim(),
        unit: item?.baseStatUnit || '',
        explanation: '',
      };
  }
}"""

if old_slot_info in rules:
    rules = rules.replace(old_slot_info, new_slot_info, 1)
    print("Updated SLOT_INFO and added formatItemDisplayStat in rules.ts.")
else:
    print("Warning: old_slot_info not found in rules.ts!")

# Update INITIAL_EQUIPPED_SLOTS in rules.ts
old_initial_slots = """export const INITIAL_EQUIPPED_SLOTS: Record<EquipmentSlotKey, EquipmentItem> = {
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
    name: 'Đe Thép Cổ Vân chi Bạo Kích',
    rarity: 'common',
    itemLevel: 1,
    baseStatLabel: 'Tỷ Lệ Bạo Kích',
    baseStatValue: 4,
    baseStatUnit: '%',
    prefixes: [],
    suffixes: [{ id: 's_init_1', type: 'suffix', name: 'chi Bạo Kích', label: '+3% Bạo Kích', statKey: 'critChancePct', value: 3 }],
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
};"""

new_initial_slots = """export const INITIAL_EQUIPPED_SLOTS: Record<EquipmentSlotKey, EquipmentItem> = {
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
    baseStatUnit: 'Sát Thương',
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
    name: 'Đe Thép Cổ Vân chi Bạo Kích',
    rarity: 'common',
    itemLevel: 1,
    baseStatLabel: 'Tỷ Lệ Bạo Kích',
    baseStatValue: 4,
    baseStatUnit: '% Bạo Kích',
    prefixes: [],
    suffixes: [{ id: 's_init_1', type: 'suffix', name: 'chi Bạo Kích', label: '+3% Bạo Kích', statKey: 'critChancePct', value: 3 }],
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
    baseStatLabel: 'Bơm Nhiệt Lò Rèn',
    baseStatValue: 3,
    baseStatUnit: '°C Lửa / nhát',
    prefixes: [{ id: 'p_init_2', type: 'prefix', name: 'Xích Diễm', label: '+2 °C Hỏa Hầu', statKey: 'heatGainPerHit', value: 2 }],
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
    baseStatUnit: '% Bạo Kích',
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
    baseStatLabel: 'Thu Thập Tự Động',
    baseStatValue: 15,
    baseStatUnit: 'Linh Thạch / phút',
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
    baseStatLabel: 'Khuếch Đại Uy Lực',
    baseStatValue: 5,
    baseStatUnit: '% Tổng Sát Thương',
    prefixes: [],
    suffixes: [],
    loreDescription: 'Mảnh thạch bàn khắc họa chim Lạc sải cánh, tượng trưng cho ý chí người thợ rèn Việt cổ.',
    setId: 'set_thunder',
    setName: 'Thiên Lôi Phá Khởi',
  },
};"""

if old_initial_slots in rules:
    rules = rules.replace(old_initial_slots, new_initial_slots, 1)
    print("Updated INITIAL_EQUIPPED_SLOTS with human-friendly units.")
else:
    print("Warning: old_initial_slots not found in rules.ts!")

# Update ensureAllEquippedSlots to auto-heal legacy saved units
old_ensure = """export function ensureAllEquippedSlots(
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
}"""

new_ensure = """export function ensureAllEquippedSlots(
  rawEquipped?: Record<string, any> | null
): Record<EquipmentSlotKey, EquipmentItem> {
  const result: Record<EquipmentSlotKey, EquipmentItem> = { ...INITIAL_EQUIPPED_SLOTS };
  if (rawEquipped && typeof rawEquipped === 'object') {
    for (const key of Object.keys(INITIAL_EQUIPPED_SLOTS) as EquipmentSlotKey[]) {
      const item = rawEquipped[key];
      if (item && typeof item === 'object' && item.id) {
        const defaultSlot = INITIAL_EQUIPPED_SLOTS[key];
        result[key] = {
          ...defaultSlot,
          ...item,
          baseStatLabel: defaultSlot.baseStatLabel,
          baseStatUnit: defaultSlot.baseStatUnit,
          level: typeof item.level === 'number' && item.level >= 1 ? item.level : 1,
          unlockedSockets: typeof item.unlockedSockets === 'number' ? item.unlockedSockets : getUnlockedSockets(item.rarity || 'common'),
          sockets: Array.isArray(item.sockets) ? item.sockets : [],
        };
      }
    }
  }
  return result;
}"""

if old_ensure in rules:
    rules = rules.replace(old_ensure, new_ensure, 1)
    print("Updated ensureAllEquippedSlots to auto-heal legacy saved units.")
else:
    print("Warning: old_ensure not found in rules.ts!")

with open('frontend/src/game/rules.ts', 'w', encoding='utf-8') as f:
    f.write(rules)

# 2. Update RightProgressionPanel.tsx
with open('frontend/src/components/RightProgressionPanel.tsx', 'r', encoding='utf-8') as f:
    rpp = f.read()

# Add formatItemDisplayStat import
old_rpp_import = "import { EquipmentItem, EquipmentSlotKey, ItemRarity, INITIAL_EQUIPPED_SLOTS, getItemRarityMeta, getUnlockedSockets, SLOT_INFO, QUENCH_OPTIONS, StanceKey, PlayerClassMeta, RuneGem, RuneType, getRuneArt, RARITY_SOCKET_COLORS, RARITY_SOCKET_GLOW } from '../game/rules';"
new_rpp_import = "import { EquipmentItem, EquipmentSlotKey, ItemRarity, INITIAL_EQUIPPED_SLOTS, getItemRarityMeta, getUnlockedSockets, SLOT_INFO, QUENCH_OPTIONS, StanceKey, PlayerClassMeta, RuneGem, RuneType, getRuneArt, RARITY_SOCKET_COLORS, RARITY_SOCKET_GLOW, formatItemDisplayStat } from '../game/rules';"

if old_rpp_import in rpp:
    rpp = rpp.replace(old_rpp_import, new_rpp_import, 1)
    print("Imported formatItemDisplayStat in RightProgressionPanel.tsx.")
else:
    print("Warning: old_rpp_import not found!")

# Replace card stat display
old_card_stat = """                              <div className="text-[9.5px] font-tech text-cyan-300 font-mono mt-0.5">
                                +{item?.baseStatValue || 1} {item?.baseStatUnit || 'DMG'}
                              </div>"""

new_card_stat = """                              <div className="text-[10px] font-tech text-cyan-300 font-bold mt-1 tracking-tight truncate">
                                {formatItemDisplayStat(item, slotKey).displayValue}
                              </div>"""

if old_card_stat in rpp:
    rpp = rpp.replace(old_card_stat, new_card_stat, 1)
    print("Updated card stat display in RightProgressionPanel.tsx.")
else:
    print("Warning: old_card_stat not found!")

# Replace card title tooltip for full clarity
old_button_title = 'onClick={() => setSelectedSlotKey(slotKey)}'
new_button_title = """onClick={() => setSelectedSlotKey(slotKey)}
                        title={`${item ? item.name : relicCfg.title} · ${formatItemDisplayStat(item, slotKey).statLabel}: ${formatItemDisplayStat(item, slotKey).displayValue} (${formatItemDisplayStat(item, slotKey).explanation})`}"""

if old_button_title in rpp:
    rpp = rpp.replace(old_button_title, new_button_title, 1)
    print("Added explanatory title tooltip to equipment cards.")
else:
    print("Warning: old_button_title not found!")

# Replace selected weapon station stat header
old_sel_stat = """                        <div className="text-[11px] font-tech text-cyan-300 font-mono mt-0.5">
                          {item.baseStatLabel}: +{item.baseStatValue} {item.baseStatUnit}
                        </div>"""

new_sel_stat = """                        <div className="text-[11px] font-tech text-cyan-300 font-bold mt-0.5">
                          {formatItemDisplayStat(item, selectedSlotKey).statLabel}: <span className="text-amber-300 font-mono">{formatItemDisplayStat(item, selectedSlotKey).displayValue}</span>
                        </div>
                        <div className="text-[9.5px] text-slate-400 font-sans mt-0.5">
                          ℹ️ {formatItemDisplayStat(item, selectedSlotKey).explanation}
                        </div>"""

if old_sel_stat in rpp:
    rpp = rpp.replace(old_sel_stat, new_sel_stat, 1)
    print("Updated selected weapon station stat header.")
else:
    print("Warning: old_sel_stat not found!")

# Replace tempering cost display
old_temper_stat = """                          <span className="text-emerald-400 font-bold">
                            +{statGain} {item.baseStatUnit}
                          </span>"""

new_temper_stat = """                          <span className="text-emerald-400 font-bold">
                            +{statGain} {formatItemDisplayStat(item, selectedSlotKey).unit}
                          </span>"""

if old_temper_stat in rpp:
    rpp = rpp.replace(old_temper_stat, new_temper_stat, 1)
    print("Updated tempering stat gain unit.")
else:
    print("Warning: old_temper_stat not found!")

with open('frontend/src/components/RightProgressionPanel.tsx', 'w', encoding='utf-8') as f:
    f.write(rpp)

print("Patch script finished successfully!")
