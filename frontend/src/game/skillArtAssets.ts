// ==============================================================================
// DỰ ÁN WEBGAME "PHÁ TRỜI" - THE CELESTIAL FORGE (phatroi.com)
// HỆ THỐNG ASSET ART CHO KỸ NĂNG & THANH ĐO SIÊU TẢI (OVERDRIVE HUD)
// ==============================================================================

import type { PlayerClassId } from './rules';

export type SkillSlotKey = 'Q' | 'W' | 'E' | 'R';

export interface SkillArtConfig {
  icon: string;
  glowColor: string;
  borderColor: string;
}

const SKILL_ART_BASE_PATH = './assets/art/ui/skills';

const SKILL_SLOTS: readonly SkillSlotKey[] = ['Q', 'W', 'E', 'R'];

const SLOT_GLOW_ALPHA: Record<SkillSlotKey, number> = {
  Q: 0.8,
  W: 0.7,
  E: 0.85,
  R: 0.95,
};

function hexToRgba(hex: string, alpha: number): string {
  const normalized = hex.replace('#', '');
  const r = parseInt(normalized.slice(0, 2), 16);
  const g = parseInt(normalized.slice(2, 4), 16);
  const b = parseInt(normalized.slice(4, 6), 16);
  return `rgba(${r}, ${g}, ${b}, ${alpha})`;
}

/** Build the Q/W/E/R skill art configs for one class from its asset prefix and border palette. */
function buildClassSkillSet(
  assetPrefix: 'thunder' | 'flame' | 'mountain' | 'music',
  borderColors: Record<SkillSlotKey, string>,
): Record<SkillSlotKey, SkillArtConfig> {
  const entries = SKILL_SLOTS.map((slot) => {
    const borderColor = borderColors[slot];
    return [
      slot,
      {
        icon: `${SKILL_ART_BASE_PATH}/skill_${assetPrefix}_${slot.toLowerCase()}.webp`,
        glowColor: hexToRgba(borderColor, SLOT_GLOW_ALPHA[slot]),
        borderColor,
      },
    ] as const;
  });
  return Object.fromEntries(entries) as Record<SkillSlotKey, SkillArtConfig>;
}

export const SKILL_ART_MAP: Record<PlayerClassId, Record<SkillSlotKey, SkillArtConfig>> = {
  thunder: buildClassSkillSet('thunder', {
    Q: '#06B6D4',
    W: '#0EA5E9',
    E: '#3B82F6',
    R: '#6366F1',
  }),
  fire: buildClassSkillSet('flame', {
    Q: '#F97316',
    W: '#EF4444',
    E: '#F59E0B',
    R: '#DC2626',
  }),
  gravity: buildClassSkillSet('mountain', {
    Q: '#10B981',
    W: '#F59E0B',
    E: '#D97706',
    R: '#B45309',
  }),
  mystic: buildClassSkillSet('music', {
    Q: '#A855F7',
    W: '#D946EF',
    E: '#C026D3',
    R: '#9333EA',
  }),
};

// Preserve compatibility with pre-v3.3 asset/sect identifiers.
const LEGACY_CLASS_ALIASES: Record<string, PlayerClassId> = {
  flame: 'fire',
  mountain: 'gravity',
  music: 'mystic',
};

export const UI_FRAME_ASSETS = {
  idle: `${SKILL_ART_BASE_PATH}/frame_skill_idle.webp`,
  ready: `${SKILL_ART_BASE_PATH}/frame_skill_ready.webp`,
  locked: `${SKILL_ART_BASE_PATH}/frame_skill_locked.webp`,
  gauge: `${SKILL_ART_BASE_PATH}/gauge_overdrive_frame.webp`,
  gemActive: `${SKILL_ART_BASE_PATH}/gem_overdrive_active.webp`,
  gemDormant: `${SKILL_ART_BASE_PATH}/gem_overdrive_dormant.webp`,
  plaqueFlame: `${SKILL_ART_BASE_PATH}/plaque_sect_flame.webp`,
};

/** Resolve skill art config for a canonical class ID or legacy alias, defaulting to thunder. */
export function getSkillArt(classId: string, slotKey: SkillSlotKey): SkillArtConfig {
  const canonicalId = Object.prototype.hasOwnProperty.call(LEGACY_CLASS_ALIASES, classId)
    ? LEGACY_CLASS_ALIASES[classId]
    : classId;
  const sect = Object.prototype.hasOwnProperty.call(SKILL_ART_MAP, canonicalId)
    ? SKILL_ART_MAP[canonicalId as PlayerClassId]
    : SKILL_ART_MAP.thunder;
  return sect[slotKey];
}
