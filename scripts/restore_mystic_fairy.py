# -*- coding: utf-8 -*-

# 1. Update rules.ts
with open('frontend/src/game/rules.ts', 'r', encoding='utf-8') as f:
    text = f.read()

# Make skin_mystic_fairy isAvailable: true
text = text.replace(
    """    bonusStatText: 'Tạo Hóa Vạn Vật · Hiệu Ứng Bích Lạc Tiên Quang rực rỡ',
    isAvailable: false,""",
    """    bonusStatText: 'Tạo Hóa Vạn Vật · Hiệu Ứng Bích Lạc Tiên Quang rực rỡ',
    isAvailable: true,"""
)

# Set default skin for mystic to skin_mystic_fairy
text = text.replace(
    """export const SECT_DEFAULT_SKIN: Record<PlayerClassId, string> = {
  thunder: 'skin_default',
  fire: 'skin_flame_lord',
  gravity: 'skin_default',
  mystic: 'skin_default',
};""",
    """export const SECT_DEFAULT_SKIN: Record<PlayerClassId, string> = {
  thunder: 'skin_default',
  fire: 'skin_flame_lord',
  gravity: 'skin_default',
  mystic: 'skin_mystic_fairy',
};"""
)

with open('frontend/src/game/rules.ts', 'w', encoding='utf-8') as f:
    f.write(text)
print("Updated rules.ts with skin_mystic_fairy available and default for mystic.")

# 2. Update CharacterCreationModal.tsx grid to grid-cols-3
with open('frontend/src/components/CharacterCreationModal.tsx', 'r', encoding='utf-8') as f:
    ccm = f.read()

ccm = ccm.replace(
    '<div className="grid grid-cols-2 gap-2.5 max-w-sm mx-auto w-full">',
    '<div className="grid grid-cols-3 gap-2 max-w-lg mx-auto w-full">'
)

with open('frontend/src/components/CharacterCreationModal.tsx', 'w', encoding='utf-8') as f:
    f.write(ccm)
print("Updated CharacterCreationModal.tsx grid.")

# 3. Update StatusModal.tsx grid to grid-cols-3
with open('frontend/src/components/StatusModal.tsx', 'r', encoding='utf-8') as f:
    sm = f.read()

sm = sm.replace(
    '<div className="grid grid-cols-2 gap-2.5 max-w-sm mx-auto w-full">',
    '<div className="grid grid-cols-3 gap-2 max-w-lg mx-auto w-full">'
)

with open('frontend/src/components/StatusModal.tsx', 'w', encoding='utf-8') as f:
    f.write(sm)
print("Updated StatusModal.tsx grid.")

# 4. Update TitlePages.tsx grid to grid-cols-3
with open('frontend/src/components/TitlePages.tsx', 'r', encoding='utf-8') as f:
    tp = f.read()

tp = tp.replace(
    '<div className="grid grid-cols-1 sm:grid-cols-2 gap-4 max-w-xl mx-auto">',
    '<div className="grid grid-cols-1 sm:grid-cols-3 gap-3 max-w-3xl mx-auto">'
)

with open('frontend/src/components/TitlePages.tsx', 'w', encoding='utf-8') as f:
    f.write(tp)
print("Updated TitlePages.tsx grid.")
