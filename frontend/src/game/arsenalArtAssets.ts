// ==============================================================================
// DỰ ÁN WEBGAME "PHÁ TRỜI" - THE CELESTIAL FORGE (phatroi.com)
// HỆ THỐNG ASSET ART CHO LÒ RÈN, BẢN MỆNH THẦN KHÍ & PHÙ THẠCH (ARSENAL)
// ==============================================================================

import { EquipmentSlotKey, RuneType } from './rules';

/**
 * 6 Lục Đại Bản Mệnh Thần Khí (Vĩnh Cửu)
 */
export const RELIC_ART_ASSETS: Record<EquipmentSlotKey, { primary: string; fallback: string; title: string }> = {
  hammer: {
    primary: './assets/art/items/item_hammer_celestial.webp',
    fallback: './assets/art/items/item_hammer.webp',
    title: 'Khai Thiên Thần Chùy',
  },
  anvil: {
    primary: './assets/art/items/item_anvil_primordial.webp',
    fallback: './assets/art/items/item_anvil.webp',
    title: 'Vạn Cổ Thần Đe',
  },
  bellows: {
    primary: './assets/art/items/item_bellows_samadhi.webp',
    fallback: './assets/art/items/item_bellows.webp',
    title: 'Tam Muội Hỏa Lò',
  },
  gauntlets: {
    primary: './assets/art/items/item_gauntlets_dragonscale.webp',
    fallback: './assets/art/items/item_gauntlets.webp',
    title: 'Long Lân Rèn Thủ',
  },
  apron: {
    primary: './assets/art/items/item_apron_celestial_mail.webp',
    fallback: './assets/art/items/item_apron.webp',
    title: 'Tinh Thần Thiết Hộ',
  },
  relic: {
    primary: './assets/art/items/item_relic_bagua_core.webp',
    fallback: './assets/art/items/item_relic.webp',
    title: 'Định Thiên Linh Bảo',
  },
};

/**
 * Ngũ Đại Phù Thạch Thượng Cổ (5 Elemental Rune Gems)
 */
export const RUNE_ART_BY_TYPE: Record<RuneType, { url: string; elementVfxColor: string; name: string }> = {
  thunder: {
    url: './assets/art/runes/gem_rune_thunder.webp',
    elementVfxColor: '#00F0FF',
    name: 'Lôi Quang Phù Thạch',
  },
  fire: {
    url: './assets/art/runes/gem_rune_fire.webp',
    elementVfxColor: '#FB923C',
    name: 'Địa Hỏa Tinh Thạch',
  },
  gravity: {
    url: './assets/art/runes/gem_rune_gravity.webp',
    elementVfxColor: '#C084FC',
    name: 'Thái Sơn Trọng Thạch',
  },
  mystic: {
    url: './assets/art/runes/gem_rune_mystic.webp',
    elementVfxColor: '#34D399',
    name: 'Huyền Âm Bích Ngọc',
  },
  fortune: {
    url: './assets/art/runes/gem_rune_fortune.webp',
    elementVfxColor: '#F59E0B',
    name: 'Thiên Mệnh Thần Tinh',
  },
};

/**
 * Ngũ Đại Thuộc Tính Rèn (5 Stat Sigils/Emblems)
 */
export const STAT_SIGIL_ASSETS: Record<'str' | 'dex' | 'int' | 'pen' | 'spi', { url: string; label: string; color: string; desc: string }> = {
  str: {
    url: './assets/art/sigils/sigil_stat_str.webp',
    label: 'Sức Mạnh',
    color: '#F87171',
    desc: 'Tăng sát thương vật lý gõ búa cơ bản',
  },
  dex: {
    url: './assets/art/sigils/sigil_stat_agi.webp',
    label: 'Khéo Léo',
    color: '#34D399',
    desc: 'Mở rộng cửa sổ Hoàng Kim & Tốc độ ra đòn',
  },
  int: {
    url: './assets/art/sigils/sigil_stat_int.webp',
    label: 'Trí Tuệ',
    color: '#60A5FA',
    desc: 'Tăng sát thương kỹ pháp Q/W/E/R & Hiệu lực nguyên tố',
  },
  pen: {
    url: './assets/art/sigils/sigil_stat_pen.webp',
    label: 'Xuyên Giáp',
    color: '#FBBF24',
    desc: 'Bào mòn khiên Vòm Trời nhanh gấp bội',
  },
  spi: {
    url: './assets/art/sigils/sigil_stat_spr.webp',
    label: 'Tâm Thần',
    color: '#C084FC',
    desc: 'Kéo dài thời gian Bạo Phát Overdrive & Tỉ lệ rớt ngọc',
  },
};

export function getRelicArt(slotKey: EquipmentSlotKey): { primary: string; fallback: string; title: string } {
  return RELIC_ART_ASSETS[slotKey] || {
    primary: './assets/art/items/item_hammer.webp',
    fallback: './assets/art/items/item_hammer.webp',
    title: 'Thần Khí',
  };
}

export function getRuneArt(type: RuneType): string {
  return RUNE_ART_BY_TYPE[type]?.url || './assets/art/runes/gem_rune_thunder.webp';
}

