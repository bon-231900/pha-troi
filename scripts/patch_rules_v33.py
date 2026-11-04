# -*- coding: utf-8 -*-
import sys

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

with open('frontend/src/game/rules.ts', 'r', encoding='utf-8') as f:
    code = f.read()

target = """export const OVERDRIVE_MAX = 8;"""

replacement = """export const OVERDRIVE_MAX = 8;
export const OVERDRIVE_TOTAL_CAP = 24; // 3 Tiers: 8 points each (Tier 1 Gold, Tier 2 Purple, Tier 3 Red)

export interface OverdriveTierInfo {
  tier: 1 | 2 | 3;
  tierCharge: number; // 0..8 in current tier
  tierMax: number;
  label: string;
  color: string;
  borderColor: string;
  glowColor: string;
  isEmpoweredE: boolean;
  canUseR: boolean;
}

export function getOverdriveTier(charge: number): OverdriveTierInfo {
  const clamped = Math.max(0, Math.min(OVERDRIVE_TOTAL_CAP, charge));
  if (clamped >= 16) {
    return {
      tier: 3,
      tierCharge: Math.min(8, clamped - 16),
      tierMax: 8,
      label: 'TẦNG 3: CỰC CẢNH (HỒNG HOANG)',
      color: '#EF4444',
      borderColor: '#DC2626',
      glowColor: 'rgba(239, 68, 68, 0.6)',
      isEmpoweredE: true,
      canUseR: true,
    };
  }
  if (clamped >= 8) {
    return {
      tier: 2,
      tierCharge: Math.min(8, clamped - 8),
      tierMax: 8,
      label: 'TẦNG 2: SIÊU TẢI (HUYỀN THIÊN)',
      color: '#A855F7',
      borderColor: '#9333EA',
      glowColor: 'rgba(168, 85, 247, 0.5)',
      isEmpoweredE: true,
      canUseR: false,
    };
  }
  return {
    tier: 1,
    tierCharge: Math.min(8, clamped),
    tierMax: 8,
    label: 'TẦNG 1: KHỞI NGUYÊN (HOÀNG KIM)',
    color: '#F59E0B',
    borderColor: '#D97706',
    glowColor: 'rgba(245, 158, 11, 0.4)',
    isEmpoweredE: false,
    canUseR: false,
  };
}

// ============================================================================
// BALANCE PATCH v3.3: SINGLE-CLASS COMMITMENT & 4-SKILL KITS
// ============================================================================

export type PlayerClassId = 'thunder' | 'fire' | 'gravity' | 'mystic';

export interface ClassSkillMeta {
  slot: 'Q' | 'W' | 'E' | 'R';
  id: string;
  name: string;
  typeTitle: string; // 'Thức Căn Bản' | 'Thức Điều Hòa' | 'Thức Bạo Phát' | 'Thức Chân Truyền'
  unlockLevel: number; // 1, 20, 40, 80
  description: string;
  cooldownSec: number;
  overdriveCost: number; // 0, 8, 16
  icon: string;
}

export interface PlayerClassMeta {
  id: PlayerClassId;
  name: string;
  sectTitle: string;
  guildId: string;
  stanceKey: StanceKey;
  icon: string;
  color: string;
  badgeBg: string;
  textColor: string;
  borderColor: string;
  weaponName: string;
  primaryStats: string[];
  motto: string;
  roleSummary: string;
  skills: {
    Q: ClassSkillMeta;
    W: ClassSkillMeta;
    E: ClassSkillMeta;
    R: ClassSkillMeta;
  };
  subClasses: {
    a: { name: string; focus: string; desc: string };
    b: { name: string; focus: string; desc: string };
  };
}

export const PLAYER_CLASSES: Record<PlayerClassId, PlayerClassMeta> = {
  thunder: {
    id: 'thunder',
    name: 'Hệ Lôi Đỉnh',
    sectTitle: 'Thiên Thai Phường · Lôi Thần Chùy',
    guildId: 'guild_thien_thai',
    stanceKey: 'Q',
    icon: '⚡',
    color: '#00F0FF',
    badgeBg: 'bg-cyan-500/20 text-cyan-300 border-cyan-500/40',
    textColor: 'text-cyan-400',
    borderColor: 'border-cyan-500',
    weaponName: 'Lôi Thần Chùy',
    primaryStats: ['DEX (Chuẩn Xác)', 'SPI (Cộng Hưởng)'],
    motto: 'Khai Lò Phá Khởi · Lôi Đình Trảm Thiên',
    roleSummary: 'Sát Thương Chủ Lực Khi Vỡ Giáp · Tốc Kích & Sét Lan',
    skills: {
      Q: {
        slot: 'Q',
        id: 'thunder_q',
        name: 'Lôi Đỉnh Chùy',
        typeTitle: 'Thức Căn Bản',
        unlockLevel: 1,
        description: 'Mỗi nhát Hoàng Kim tăng +10 ms cửa sổ nhịp, nạp 1.5 ô Overdrive và phóng tia sét phụ giáng 45% DMG.',
        cooldownSec: 0,
        overdriveCost: 0,
        icon: '⚡',
      },
      W: {
        slot: 'W',
        id: 'thunder_w',
        name: 'Lôi Quang Bộ',
        typeTitle: 'Thức Điều Hòa',
        unlockLevel: 20,
        description: 'Bảo toàn chuỗi Combo trong 3 nhát gõ tiếp theo nếu gõ trượt và chuyển 20% DEX thành Xuyên Giáp PEN.',
        cooldownSec: 10,
        overdriveCost: 0,
        icon: '💨',
      },
      E: {
        slot: 'E',
        id: 'thunder_e',
        name: 'Bão Plasma Cuồng Kích',
        typeTitle: 'Thức Bạo Phát',
        unlockLevel: 40,
        description: 'Phóng 8 luồng sét liên hoàn vào Mái Vòm, mỗi luồng tăng +12% Crit DMG theo chuỗi combo hiện tại.',
        cooldownSec: 5,
        overdriveCost: 8,
        icon: '🌩️',
      },
      R: {
        slot: 'R',
        id: 'thunder_r',
        name: 'Thiên Lôi Giáng Thế',
        typeTitle: 'Thức Chân Truyền',
        unlockLevel: 80,
        description: 'Triệu hồi cột sét khổng lồ nối 15 đồng minh trên server, nhân tổng sát thương cả nhóm thêm x2.2 trong 10 giây.',
        cooldownSec: 30,
        overdriveCost: 16,
        icon: '👑',
      },
    },
    subClasses: {
      a: {
        name: 'Tật Lôi Kiếm Tượng',
        focus: 'DEX + STR',
        desc: 'Chuyên gia tốc độ cao; mỗi nhát gõ ở Overdrive Tầng 3 tính bằng 3 lần nhảy sát thương độc lập.',
      },
      b: {
        name: 'Thiên Lôi Pháp Sư',
        focus: 'SPI + DEX',
        desc: 'Mạng lưới sét không giảm uy lực khi nảy qua 10 đồng minh và nạp hộ Overdrive cho cả tổ đội.',
      },
    },
  },
  fire: {
    id: 'fire',
    name: 'Hệ Viêm Dương',
    sectTitle: 'Phần Thiên Các · Xích Hỏa Lô',
    guildId: 'guild_phan_thien',
    stanceKey: 'W',
    icon: '🔥',
    color: '#FF4D00',
    badgeBg: 'bg-red-500/20 text-red-300 border-red-500/40',
    textColor: 'text-red-400',
    borderColor: 'border-red-500',
    weaponName: 'Xích Hỏa Lô',
    primaryStats: ['INT (Nhiệt Lực)', 'PEN (Phá Phách)'],
    motto: 'Hỏa Diệm Bất Diệt · Luyện Khí Thành Thần',
    roleSummary: 'Duy Trì Nhiệt Lò Server & Đốt Máu % Boss',
    skills: {
      Q: {
        slot: 'Q',
        id: 'fire_q',
        name: 'Viêm Dương Chùy',
        typeTitle: 'Thức Căn Bản',
        unlockLevel: 1,
        description: 'Mỗi nhát gõ tăng +6°C Hỏa Hẩu và khắc 1 tầng Tro Tàn (tối đa 50 tầng) đốt máu Boss liên tục theo chỉ số INT.',
        cooldownSec: 0,
        overdriveCost: 0,
        icon: '🔥',
      },
      W: {
        slot: 'W',
        id: 'fire_w',
        name: 'Thuật Khống Hỏa',
        typeTitle: 'Thức Điều Hòa',
        unlockLevel: 20,
        description: 'Chuyển hóa nhiệt dư thừa (>850°C) thành Lửa Xanh Tinh Luyện, ngăn quá nhiệt và bơm +50°C/hit vào Đại Hỏa Hẩu Server.',
        cooldownSec: 8,
        overdriveCost: 0,
        icon: '🛡️',
      },
      E: {
        slot: 'E',
        id: 'fire_e',
        name: 'Hỏa Diệm Bùng Phát',
        typeTitle: 'Thức Bạo Phát',
        unlockLevel: 40,
        description: 'Kích nổ lập tức 50% số tầng Tro Tàn thành sát thương chuẩn và làm mềm vỏ Mái Vòm (-20% Giáp Boss trong 8 giây).',
        cooldownSec: 5,
        overdriveCost: 8,
        icon: '💥',
      },
      R: {
        slot: 'R',
        id: 'fire_r',
        name: 'Hỏa Ngục Đồng Quy',
        typeTitle: 'Thức Chân Truyền',
        unlockLevel: 80,
        description: 'Biến mặt đe thành mặt trời rực cháy trong 12 giây, khóa cứng thanh Đại Hỏa Hẩu Server không bị tụt nhiệt.',
        cooldownSec: 30,
        overdriveCost: 16,
        icon: '☀️',
      },
    },
    subClasses: {
      a: {
        name: 'Phần Viêm Độc Tôn',
        focus: 'INT + DEX',
        desc: 'Cho phép các tầng Tro Tàn nhận 100% Tỷ lệ Bạo Kích và Crit DMG từ chỉ số DEX.',
      },
      b: {
        name: 'Dung Lô Đại Sư',
        focus: 'INT + PEN',
        desc: 'Mỗi 100°C đóng góp vào Đại Hỏa Hẩu Server giúp tăng +5% Xuyên Giáp PEN cho toàn bộ người chơi.',
      },
    },
  },
  gravity: {
    id: 'gravity',
    name: 'Hệ Trọng Lực',
    sectTitle: 'Vạn Kiếm Sơn · Trọng Cương Chùy',
    guildId: 'guild_van_kiem',
    stanceKey: 'E',
    icon: '🏔️',
    color: '#A855F7',
    badgeBg: 'bg-purple-500/20 text-purple-300 border-purple-500/40',
    textColor: 'text-purple-400',
    borderColor: 'border-purple-500',
    weaponName: 'Trọng Cương Chùy',
    primaryStats: ['STR (Lực Chùy)', 'PEN (Phá Phách)'],
    motto: 'Nặng Tựa Thái Sơn · Nhất Kích Vỡ Vòm',
    roleSummary: 'Phá Khiên Bầu Trời & Chống Cơ Chế Hồi Giáp',
    skills: {
      Q: {
        slot: 'Q',
        id: 'gravity_q',
        name: 'Trọng Lực Chùy',
        typeTitle: 'Thức Căn Bản',
        unlockLevel: 1,
        description: 'Sát thương cơ bản x1.5 và +3 Điểm Phá Giáp/hit, đòn đánh nặng ngàn cân công phá lớp giáp Mái Vòm.',
        cooldownSec: 0,
        overdriveCost: 0,
        icon: '🔨',
      },
      W: {
        slot: 'W',
        id: 'gravity_w',
        name: 'Thái Sơn Áp Đỉnh',
        typeTitle: 'Thức Điều Hòa',
        unlockLevel: 20,
        description: 'Cường hóa búa bằng toàn bộ STR + PEN, chặn đứng 100% tốc độ Tự Hồi Giáp của Bầu Trời trong 4 giây.',
        cooldownSec: 12,
        overdriveCost: 0,
        icon: '⛰️',
      },
      E: {
        slot: 'E',
        id: 'gravity_e',
        name: 'Địa Chấn Hư Không',
        typeTitle: 'Thức Bạo Phát',
        unlockLevel: 40,
        description: 'Đập nứt không gian gây sát thương bằng 450% (STR + PEN) và trừ thẳng một lượng lớn điểm Phá Giáp của Mái Vòm.',
        cooldownSec: 5,
        overdriveCost: 8,
        icon: '🌌',
      },
      R: {
        slot: 'R',
        id: 'gravity_r',
        name: 'Hư Không Đoạt Mệnh',
        typeTitle: 'Thức Chân Truyền',
        unlockLevel: 80,
        description: 'Giáng đại chùy phán quyết; nếu Boss Vỡ Giáp hoặc dưới 30% HP, gây bạo kích tuyệt đối (x5.0 DMG) và đập tan Thiên Thạch Hộ Vòm.',
        cooldownSec: 30,
        overdriveCost: 16,
        icon: '⚡',
      },
    },
    subClasses: {
      a: {
        name: 'Thái Sơn Thần Chùy',
        focus: 'PEN + STR',
        desc: 'Tăng gấp đôi lượng Điểm Phá Giáp/hit và cho phép đòn đánh xuyên qua trạng thái Giáp Hóa Cứng của Boss Tầng 7–9.',
      },
      b: {
        name: 'Bất Động Minh Vương',
        focus: 'STR + SPI',
        desc: 'Hấp thụ 50% chấn động Thiên Kiếp thay cho Đại Đe Server và phản lại thành sát thương chuẩn lên Bầu Trời.',
      },
    },
  },
  mystic: {
    id: 'mystic',
    name: 'Hệ Huyền Âm',
    sectTitle: 'Đoạn Hồn Cốc · Bích Ngọc Đỉnh',
    guildId: 'guild_doan_hon',
    stanceKey: 'R',
    icon: '🎶',
    color: '#10B981',
    badgeBg: 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40',
    textColor: 'text-emerald-400',
    borderColor: 'border-emerald-500',
    weaponName: 'Bích Ngọc Đỉnh',
    primaryStats: ['SPI (Cộng Hưởng)', 'INT (Nhiệt Lực)'],
    motto: 'Khúc Hát Khải Hoàn · Đồng Tâm Hiệp Lực',
    roleSummary: 'Bảo Vệ Đại Đe Thần, Kéo Dài Vỡ Giáp & Buff Toàn Raid',
    skills: {
      Q: {
        slot: 'Q',
        id: 'mystic_q',
        name: 'Huyền Âm Chùy',
        typeTitle: 'Thức Căn Bản',
        unlockLevel: 1,
        description: 'Mỗi nhát gõ Hoàng Kim phát sóng âm tăng +25% Linh Thạch và hồi phục +10 Độ Bền Đại Đe Server.',
        cooldownSec: 0,
        overdriveCost: 0,
        icon: '🎶',
      },
      W: {
        slot: 'W',
        id: 'mystic_w',
        name: 'Ngọc Bích Hộ Thể',
        typeTitle: 'Thức Điều Hòa',
        unlockLevel: 20,
        description: 'Tạo lớp màng âm thanh cho bản thân và 5 đồng minh gần nhất, miễn nhiễm 1 lần phạt Miss / Dội Búa và hồi +100 Độ Bền Đại Đe.',
        cooldownSec: 10,
        overdriveCost: 0,
        icon: '🛡️',
      },
      E: {
        slot: 'E',
        id: 'mystic_e',
        name: 'Tiếng Vang Vạn Dân',
        typeTitle: 'Thức Bạo Phát',
        unlockLevel: 40,
        description: 'Truyền năng lượng SPI cho toàn kênh, giúp tất cả người chơi đang online nhận ngay +2 ô Overdrive và +15% Crit Rate trong 8 giây.',
        cooldownSec: 5,
        overdriveCost: 8,
        icon: '📢',
      },
      R: {
        slot: 'R',
        id: 'mystic_r',
        name: 'Khúc Khải Hoàn Bất Diệt',
        typeTitle: 'Thức Chân Truyền',
        unlockLevel: 80,
        description: 'Cố định trạng thái Vỡ Giáp của Bầu Trời thêm 8 giây và tăng +50% Tỷ lệ rơi đồ hiếm (Magic Find) cho toàn Raid trong 15 giây.',
        cooldownSec: 30,
        overdriveCost: 16,
        icon: '✨',
      },
    },
    subClasses: {
      a: {
        name: 'Thiên Âm Hộ Pháp',
        focus: 'SPI + INT',
        desc: 'Tăng gấp đôi lượng Hồi Phục Độ Bền Đại Đe, tự động thanh tẩy hiệu ứng đóng băng/quá nhiệt cho 15 thợ rèn lân cận.',
      },
      b: {
        name: 'Khải Hoàn Nhạc Sư',
        focus: 'SPI + DEX',
        desc: 'Kéo dài thời gian Boss Vỡ Giáp tối đa và tăng trực tiếp +25% Crit DMG cùng +30% Tỷ lệ rớt Tinh Hoa TH cho cả đội.',
      },
    },
  },
};

export function getPlayerClass(id: PlayerClassId): PlayerClassMeta {
  return PLAYER_CLASSES[id] || PLAYER_CLASSES.thunder;
}"""

if target in code:
    code = code.replace(target, replacement, 1)
    with open('frontend/src/game/rules.ts', 'w', encoding='utf-8') as f:
        f.write(code)
    print("Updated rules.ts with v3.3 single-class and 3-tier overdrive!")
else:
    print("Warning: target not found in rules.ts")
