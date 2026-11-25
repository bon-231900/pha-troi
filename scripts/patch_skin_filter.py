# -*- coding: utf-8 -*-
import sys

with open('frontend/src/game/rules.ts', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Add isAvailable to CharacterSkinMeta
target_meta = """  spritesheetPath: string;
  cardPath: string;
  bonusStatText: string;
}"""

repl_meta = """  spritesheetPath: string;
  cardPath: string;
  bonusStatText: string;
  isAvailable?: boolean;
}"""

if target_meta in text:
    text = text.replace(target_meta, repl_meta, 1)
    print("Patched CharacterSkinMeta interface.")

# 2. Add isAvailable to each skin
replacements = [
    ("bonusStatText: 'Khởi Nguyên Chi Lực · Tốc Độ Đúc +0%',", "bonusStatText: 'Khởi Nguyên Chi Lực · Tốc Độ Đúc +0%',\n    isAvailable: true,"),
    ("bonusStatText: 'Lôi Điện Cuộn Trào · Hiệu ứng Lôi Quang hào nhoáng',", "bonusStatText: 'Lôi Điện Cuộn Trào · Hiệu ứng Lôi Quang hào nhoáng',\n    isAvailable: false,"),
    ("bonusStatText: 'Lôi Thần Giáng Thế · Hiệu ứng Lôi Quang Thần Thoại rực rỡ',", "bonusStatText: 'Lôi Thần Giáng Thế · Hiệu ứng Lôi Quang Thần Thoại rực rỡ',\n    isAvailable: false,"),
    ("bonusStatText: 'Nhiệt Lửa Luyện Kim · Hỏa Hẩu rực lửa lò rèn',", "bonusStatText: 'Nhiệt Lửa Luyện Kim · Hỏa Hẩu rực lửa lò rèn',\n    isAvailable: false,"),
    ("bonusStatText: 'Nghiệp Hỏa Thiêu Thiên · Hiệu ứng Hỏa Quang Ma Tổ rực rỡ',", "bonusStatText: 'Nghiệp Hỏa Thiêu Thiên · Hiệu ứng Hỏa Quang Ma Tổ rực rỡ',\n    isAvailable: true,"),
    ("bonusStatText: 'Bàn Thạch Hộ Thể · Hào quang Trọng Lực tím hoàng kim',", "bonusStatText: 'Bàn Thạch Hộ Thể · Hào quang Trọng Lực tím hoàng kim',\n    isAvailable: false,"),
    ("bonusStatText: 'Linh Khí Phục Hồi · Hào quang Bích Ngọc thoát tục',", "bonusStatText: 'Linh Khí Phục Hồi · Hào quang Bích Ngọc thoát tục',\n    isAvailable: false,"),
    ("bonusStatText: 'Tạo Hóa Vạn Vật · Hiệu Ứng Bích Lạc Tiên Quang rực rỡ',", "bonusStatText: 'Tạo Hóa Vạn Vật · Hiệu Ứng Bích Lạc Tiên Quang rực rỡ',\n    isAvailable: false,"),
]

for old, new in replacements:
    if old in text:
        text = text.replace(old, new, 1)

target_defaults = """export const SECT_DEFAULT_SKIN: Record<PlayerClassId, string> = {
  thunder: 'skin_thunder_robe',
  fire: 'skin_flame_robe',
  gravity: 'skin_mountain_robe',
  mystic: 'skin_mystic_robe',
};

export function getSkinOrDefault(skinId?: string | null, classId?: PlayerClassId): CharacterSkinMeta {
  if (skinId && CHARACTER_SKINS[skinId]) {
    return CHARACTER_SKINS[skinId];
  }
  if (classId && SECT_DEFAULT_SKIN[classId]) {
    return CHARACTER_SKINS[SECT_DEFAULT_SKIN[classId]];
  }
  return CHARACTER_SKINS.skin_default;
}"""

repl_defaults = """export const AVAILABLE_CHARACTER_SKINS: CharacterSkinMeta[] = Object.values(CHARACTER_SKINS).filter(
  (sk) => sk.isAvailable !== false
);

export const SECT_DEFAULT_SKIN: Record<PlayerClassId, string> = {
  thunder: 'skin_default',
  fire: 'skin_flame_lord',
  gravity: 'skin_default',
  mystic: 'skin_default',
};

export function getSkinOrDefault(skinId?: string | null, classId?: PlayerClassId): CharacterSkinMeta {
  if (skinId && CHARACTER_SKINS[skinId] && CHARACTER_SKINS[skinId].isAvailable !== false) {
    return CHARACTER_SKINS[skinId];
  }
  if (classId && SECT_DEFAULT_SKIN[classId] && CHARACTER_SKINS[SECT_DEFAULT_SKIN[classId]]?.isAvailable !== false) {
    return CHARACTER_SKINS[SECT_DEFAULT_SKIN[classId]];
  }
  return CHARACTER_SKINS.skin_default;
}"""

if target_defaults in text:
    text = text.replace(target_defaults, repl_defaults, 1)
    print("Patched SECT_DEFAULT_SKIN & getSkinOrDefault.")
else:
    print("Warning: target_defaults not found!")

with open('frontend/src/game/rules.ts', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated rules.ts successfully!")
