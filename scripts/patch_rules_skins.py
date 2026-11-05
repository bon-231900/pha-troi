# -*- coding: utf-8 -*-
with open('frontend/src/game/rules.ts', 'r', encoding='utf-8') as f:
    content = f.read()

target = "export function getPlayerClass(id: PlayerClassId): PlayerClassMeta {\n  return PLAYER_CLASSES[id] || PLAYER_CLASSES.thunder;\n}"

if target not in content:
    # try CRLF
    target = "export function getPlayerClass(id: PlayerClassId): PlayerClassMeta {\r\n  return PLAYER_CLASSES[id] || PLAYER_CLASSES.thunder;\r\n}"

replacement = target + """

// ---------------------------------------------------------------------------
// HỆ THỐNG Y PHỤC MÔN PHÁI & TRANG PHỤC THỢ RÈN (CHARACTER SECT SKINS & OUTFITS)
// ---------------------------------------------------------------------------

export interface CharacterSkinMeta {
  id: string;
  name: string;
  sectId: PlayerClassId | 'neutral';
  sectTitle: string;
  description: string;
  rarity: 'phàm' | 'linh' | 'huyền' | 'thiên' | 'thần_thoại';
  rarityColor: string;
  rarityBadgeBg: string;
  rarityBorder: string;
  icon: string;
  paletteColor: string;
  spritesheetPath: string;
  cardPath: string;
  bonusStatText: string;
}

export const CHARACTER_SKINS: Record<string, CharacterSkinMeta> = {
  skin_default: {
    id: 'skin_default',
    name: 'Phàm Nhân Thiết Tượng',
    sectId: 'neutral',
    sectTitle: 'Khởi Nguyên Thiết Bào',
    description: 'Y phục thợ rèn sơ cấp mộc mạc làm từ vải thô gia cường da thú, bền bỉ trước tàn lửa lò rèn.',
    rarity: 'phàm',
    rarityColor: '#94A3B8',
    rarityBadgeBg: 'bg-slate-500/20 text-slate-300 border-slate-500/40',
    rarityBorder: 'border-slate-600',
    icon: '🥋',
    paletteColor: '#94A3B8',
    spritesheetPath: 'assets/art/skins/skin_default/spritesheet_strip.webp',
    cardPath: 'assets/art/skins/skin_default/card.webp',
    bonusStatText: 'Tự Nhiên Vô Tà · Tốc Độ Đúc +0%',
  },
  skin_thunder_robe: {
    id: 'skin_thunder_robe',
    name: 'Cửu Tiêu Lôi Bào',
    sectId: 'thunder',
    sectTitle: 'Thiên Thai Phường · Đạo Bào Kiếm Tiên',
    description: 'Đạo bào lam bạch dệt bằng sợi tơ Lôi Tinh, cổ áo thêu hoa văn Lôi Vân, vung búa tỏa ngàn tia lôi quang.',
    rarity: 'linh',
    rarityColor: '#00F0FF',
    rarityBadgeBg: 'bg-cyan-500/20 text-cyan-300 border-cyan-500/40',
    rarityBorder: 'border-cyan-500',
    icon: '⚡',
    paletteColor: '#00F0FF',
    spritesheetPath: 'assets/art/skins/skin_thunder_robe/spritesheet_strip.webp',
    cardPath: 'assets/art/skins/skin_thunder_robe/card.webp',
    bonusStatText: 'Lôi Điện Cuộn Trào · Hiệu ứng Lôi Quang hào nhoáng',
  },
  skin_flame_robe: {
    id: 'skin_flame_robe',
    name: 'Hắc Diệm Minh Bào',
    sectId: 'fire',
    sectTitle: 'Phần Thiên Các · Ma Quân Hỏa Bào',
    description: 'Chiến bào hắc diệm đen thẫm viền lửa đỏ son, vai giáp rực lửa không bao giờ tắt, thiêu đốt vạn vật.',
    rarity: 'linh',
    rarityColor: '#FF4D00',
    rarityBadgeBg: 'bg-red-500/20 text-red-300 border-red-500/40',
    rarityBorder: 'border-red-500',
    icon: '🔥',
    paletteColor: '#FF4D00',
    spritesheetPath: 'assets/art/skins/skin_flame_robe/spritesheet_strip.webp',
    cardPath: 'assets/art/skins/skin_flame_robe/card.webp',
    bonusStatText: 'Nhiệt Lửa Luyện Kim · Hỏa Hẩu rực lửa lò rèn',
  },
  skin_mountain_robe: {
    id: 'skin_mountain_robe',
    name: 'Bất Chu Nham Giáp',
    sectId: 'gravity',
    sectTitle: 'Bất Chu Sơn · Thạch Nham Chiến Giáp',
    description: 'Trọng giáp thạch nham đúc từ đá núi Bất Chu, vai giáp khắc cổ phù hộ thể, kiên cố bất động trước thiên tai.',
    rarity: 'linh',
    rarityColor: '#A855F7',
    rarityBadgeBg: 'bg-purple-500/20 text-purple-300 border-purple-500/40',
    rarityBorder: 'border-purple-500',
    icon: '🏔️',
    paletteColor: '#A855F7',
    spritesheetPath: 'assets/art/skins/skin_mountain_robe/spritesheet_strip.webp',
    cardPath: 'assets/art/skins/skin_mountain_robe/card.webp',
    bonusStatText: 'Bàn Thạch Hộ Thể · Hào quang Trọng Lực tím hoàng kim',
  },
  skin_mystic_robe: {
    id: 'skin_mystic_robe',
    name: 'Thanh Mộc Tiên Y',
    sectId: 'mystic',
    sectTitle: 'Thái Ất Tông · Bích Ngọc Đan Bào',
    description: 'Đạo bào ngọc bích dệt từ tơ mộc linh ngàn năm, dải lụa tiên nhân lục ngọc thanh nhã, tỏa ngát hương đan dược.',
    rarity: 'linh',
    rarityColor: '#10B981',
    rarityBadgeBg: 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40',
    rarityBorder: 'border-emerald-500',
    icon: '🎵',
    paletteColor: '#10B981',
    spritesheetPath: 'assets/art/skins/skin_mystic_robe/spritesheet_strip.webp',
    cardPath: 'assets/art/skins/skin_mystic_robe/card.webp',
    bonusStatText: 'Linh Khí Phục Hồi · Hào quang Bích Ngọc thoát tục',
  },
};

export const SECT_DEFAULT_SKIN: Record<PlayerClassId, string> = {
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
}
"""

if target in content:
    content = content.replace(target, replacement, 1)
    with open('frontend/src/game/rules.ts', 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS: rules.ts patched with skin system!")
else:
    print("ERROR: target not found in rules.ts!")
