// ==============================================================================
// DỰ ÁN WEBGAME "PHÁ TRỜI" - THE CELESTIAL FORGE (phatroi.com)
// HỆ THỐNG ASSET ART CHO KỸ NĂNG & THANH ĐO SIÊU TẢI (OVERDRIVE HUD)
// ==============================================================================

export interface SkillArtConfig {
  icon: string;
  glowColor: string;
  borderColor: string;
}

export const SKILL_ART_MAP: Record<string, Record<'Q' | 'W' | 'E' | 'R', SkillArtConfig>> = {
  flame: {
    Q: {
      icon: './assets/art/ui/skills/skill_flame_q.webp',
      glowColor: 'rgba(249, 115, 22, 0.8)',
      borderColor: '#F97316',
    },
    W: {
      icon: './assets/art/ui/skills/skill_flame_w.webp',
      glowColor: 'rgba(239, 68, 68, 0.7)',
      borderColor: '#EF4444',
    },
    E: {
      icon: './assets/art/ui/skills/skill_flame_e.webp',
      glowColor: 'rgba(245, 158, 11, 0.85)',
      borderColor: '#F59E0B',
    },
    R: {
      icon: './assets/art/ui/skills/skill_flame_r.webp',
      glowColor: 'rgba(220, 38, 38, 0.95)',
      borderColor: '#DC2626',
    },
  },
  thunder: {
    Q: {
      icon: './assets/art/ui/skills/skill_thunder_q.webp',
      glowColor: 'rgba(6, 182, 212, 0.8)',
      borderColor: '#06B6D4',
    },
    W: {
      icon: './assets/art/ui/skills/skill_thunder_w.webp',
      glowColor: 'rgba(14, 165, 233, 0.7)',
      borderColor: '#0EA5E9',
    },
    E: {
      icon: './assets/art/ui/skills/skill_thunder_e.webp',
      glowColor: 'rgba(59, 130, 246, 0.85)',
      borderColor: '#3B82F6',
    },
    R: {
      icon: './assets/art/ui/skills/skill_thunder_r.webp',
      glowColor: 'rgba(99, 102, 241, 0.95)',
      borderColor: '#6366F1',
    },
  },
  mountain: {
    Q: {
      icon: './assets/art/ui/skills/skill_mountain_q.webp',
      glowColor: 'rgba(16, 185, 129, 0.8)',
      borderColor: '#10B981',
    },
    W: {
      icon: './assets/art/ui/skills/skill_mountain_w.webp',
      glowColor: 'rgba(245, 158, 11, 0.7)',
      borderColor: '#F59E0B',
    },
    E: {
      icon: './assets/art/ui/skills/skill_mountain_e.webp',
      glowColor: 'rgba(217, 119, 6, 0.85)',
      borderColor: '#D97706',
    },
    R: {
      icon: './assets/art/ui/skills/skill_mountain_r.webp',
      glowColor: 'rgba(180, 83, 9, 0.95)',
      borderColor: '#B45309',
    },
  },
  music: {
    Q: {
      icon: './assets/art/ui/skills/skill_music_q.webp',
      glowColor: 'rgba(168, 85, 247, 0.8)',
      borderColor: '#A855F7',
    },
    W: {
      icon: './assets/art/ui/skills/skill_music_w.webp',
      glowColor: 'rgba(217, 70, 239, 0.7)',
      borderColor: '#D946EF',
    },
    E: {
      icon: './assets/art/ui/skills/skill_music_e.webp',
      glowColor: 'rgba(192, 38, 211, 0.85)',
      borderColor: '#C026D3',
    },
    R: {
      icon: './assets/art/ui/skills/skill_music_r.webp',
      glowColor: 'rgba(147, 51, 234, 0.95)',
      borderColor: '#9333EA',
    },
  },
};

export const UI_FRAME_ASSETS = {
  idle: './assets/art/ui/skills/frame_skill_idle.webp',
  ready: './assets/art/ui/skills/frame_skill_ready.webp',
  locked: './assets/art/ui/skills/frame_skill_locked.webp',
  gauge: './assets/art/ui/skills/gauge_overdrive_frame.webp',
  gemActive: './assets/art/ui/skills/gem_overdrive_active.webp',
  gemDormant: './assets/art/ui/skills/gem_overdrive_dormant.webp',
  plaqueFlame: './assets/art/ui/skills/plaque_sect_flame.webp',
};

export function getSkillArt(classId: string, slotKey: 'Q' | 'W' | 'E' | 'R'): SkillArtConfig {
  const sect = SKILL_ART_MAP[classId] || SKILL_ART_MAP.flame;
  return sect[slotKey];
}
