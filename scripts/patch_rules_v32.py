# -*- coding: utf-8 -*-
"""
Script to apply Balance Patch v3.2 MMORPG World Raid & Loot Table specifications to frontend/src/game/rules.ts
"""
import sys

def main():
    with open('frontend/src/game/rules.ts', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update ItemRarity & ItemTier definition
    old_rarity_def = "export type ItemRarity = 'common' | 'rare' | 'epic' | 'legendary' | 'mythic';"
    new_rarity_def = """export type ItemTier = 'tier_e' | 'tier_d' | 'tier_c' | 'tier_b' | 'tier_a' | 'tier_s';
export type ItemRarity = 'common' | 'uncommon' | 'rare' | 'epic' | 'legendary' | 'mythic' | ItemTier;"""

    if old_rarity_def in content:
        content = content.replace(old_rarity_def, new_rarity_def, 1)
        print("Updated ItemRarity definition.")
    else:
        print("[Notice] ItemRarity already updated or not found.")

    # 2. Add BASE_ITEM_POOL with 'uncommon' entries
    old_hammer_base = """  hammer: [
    { name: 'Búa Sắt Thiên Thai', baseValue: 2, lore: 'Búa sắt thô sơ từ thuở đầu khai lò phá trời.', minRarity: 'common' },
    { name: 'Búa Thiên Cương', baseValue: 5, lore: 'Đúc từ hợp kim thiên thạch, chùy nặng ngàn cân.', minRarity: 'rare' },"""
    new_hammer_base = """  hammer: [
    { name: 'Búa Sắt Thiên Thai', baseValue: 2, lore: 'Búa sắt thô sơ từ thuở đầu khai lò phá trời.', minRarity: 'common' },
    { name: 'Búa Tinh Thiết', baseValue: 3, lore: 'Rèn từ tinh thiết luyện kỹ lưỡng qua trăm lần nung.', minRarity: 'uncommon' },
    { name: 'Búa Thiên Cương', baseValue: 5, lore: 'Đúc từ hợp kim thiên thạch, chùy nặng ngàn cân.', minRarity: 'rare' },"""

    old_anvil_base = """  anvil: [
    { name: 'Đe Thép Cổ Vân', baseValue: 6, lore: 'Mặt đe tôi qua sương mây ngàn năm.', minRarity: 'common' },
    { name: 'Đe Trọng Lực', baseValue: 12, lore: 'Hút linh khí đất mẹ, giữ phôi thép vững như thái sơn.', minRarity: 'rare' },"""
    new_anvil_base = """  anvil: [
    { name: 'Đe Thép Cổ Vân', baseValue: 6, lore: 'Mặt đe tôi qua sương mây ngàn năm.', minRarity: 'common' },
    { name: 'Đe Tinh Cương', baseValue: 9, lore: 'Đe tinh luyện tăng độ đanh và nhạy bén khi nện búa.', minRarity: 'uncommon' },
    { name: 'Đe Trọng Lực', baseValue: 12, lore: 'Hút linh khí đất mẹ, giữ phôi thép vững như thái sơn.', minRarity: 'rare' },"""

    old_bellows_base = """  bellows: [
    { name: 'Ống Bễ Da Hổ Lôi', baseValue: 3, lore: 'May từ da hổ sấm, mỗi nhịp thổi bùng ngọn lửa đỏ.', minRarity: 'common' },
    { name: 'Ống Bễ Hỏa Phụng', baseValue: 6, lore: 'Lông vũ hỏa phụng giữ nhiệt lò không bao giờ tắt.', minRarity: 'rare' },"""
    new_bellows_base = """  bellows: [
    { name: 'Ống Bễ Da Hổ Lôi', baseValue: 3, lore: 'May từ da hổ sấm, mỗi nhịp thổi bùng ngọn lửa đỏ.', minRarity: 'common' },
    { name: 'Ống Bễ Da Hổ Tinh', baseValue: 4, lore: 'Ống bễ cải tiến đẩy luồng phong hỏa đều đặn vào lòng lò.', minRarity: 'uncommon' },
    { name: 'Ống Bễ Hỏa Phụng', baseValue: 6, lore: 'Lông vũ hỏa phụng giữ nhiệt lò không bao giờ tắt.', minRarity: 'rare' },"""

    old_gauntlets_base = """  gauntlets: [
    { name: 'Bao Tay Da Thô', baseValue: 5, lore: 'Che chắn lòng bàn tay khỏi tàn tro rực lửa.', minRarity: 'common' },
    { name: 'Bao Tay Thiết Giáp', baseValue: 9, lore: 'Lót vảy sắt dẻo dai, giữ chặt cán búa không trượt.', minRarity: 'rare' },"""
    new_gauntlets_base = """  gauntlets: [
    { name: 'Bao Tay Da Thô', baseValue: 5, lore: 'Che chắn lòng bàn tay khỏi tàn tro rực lửa.', minRarity: 'common' },
    { name: 'Bao Tay Tinh Bì', baseValue: 7, lore: 'Gia cố khớp ngón tay linh hoạt hơn khi chuyển thế.', minRarity: 'uncommon' },
    { name: 'Bao Tay Thiết Giáp', baseValue: 9, lore: 'Lót vảy sắt dẻo dai, giữ chặt cán búa không trượt.', minRarity: 'rare' },"""

    old_apron_base = """  apron: [
    { name: 'Tạp Dề Bì Hộ', baseValue: 15, lore: 'Tạp dề da dày dặn chống tia lửa bén.', minRarity: 'common' },
    { name: 'Tạp Dề Bách Luyện', baseValue: 35, lore: 'Lớp giáp gai hấp thu phản chấn từ vòm trời.', minRarity: 'rare' },"""
    new_apron_base = """  apron: [
    { name: 'Tạp Dề Bì Hộ', baseValue: 15, lore: 'Tạp dề da dày dặn chống tia lửa bén.', minRarity: 'common' },
    { name: 'Tạp Dề Tinh Thiết', baseValue: 25, lore: 'Lót giáp sắt gia công bảo hộ thợ rèn kiên cố.', minRarity: 'uncommon' },
    { name: 'Tạp Dề Bách Luyện', baseValue: 35, lore: 'Lớp giáp gai hấp thu phản chấn từ vòm trời.', minRarity: 'rare' },"""

    old_relic_base = """  relic: [
    { name: 'Thạch Bàn Đông Sơn', baseValue: 6, lore: 'Khắc họa cổ văn người Việt cổ hướng về trời cao.', minRarity: 'common' },
    { name: 'Ấn Lạc Thần', baseValue: 14, lore: 'Hào quang bảo hộ gia tăng sĩ khí toàn công trường.', minRarity: 'rare' },"""
    new_relic_base = """  relic: [
    { name: 'Thạch Bàn Đông Sơn', baseValue: 6, lore: 'Khắc họa cổ văn người Việt cổ hướng về trời cao.', minRarity: 'common' },
    { name: 'Thạch Phiến Lạc Việt', baseValue: 10, lore: 'Mảnh đá hoa văn hộ mệnh tăng cường linh cảm.', minRarity: 'uncommon' },
    { name: 'Ấn Lạc Thần', baseValue: 14, lore: 'Hào quang bảo hộ gia tăng sĩ khí toàn công trường.', minRarity: 'rare' },"""

    for o, n in [
        (old_hammer_base, new_hammer_base),
        (old_anvil_base, new_anvil_base),
        (old_bellows_base, new_bellows_base),
        (old_gauntlets_base, new_gauntlets_base),
        (old_apron_base, new_apron_base),
        (old_relic_base, new_relic_base)
    ]:
        if o in content:
            content = content.replace(o, n, 1)

    print("Updated base item pool.")

    # 3. Update getItemRarityMeta
    old_rarity_meta = """export function getItemRarityMeta(rarity: ItemRarity) {
  switch (rarity) {
    case 'mythic':
      return {
        label: 'Khai Thiên',
        textColor: 'text-orange-400',
        borderColor: 'border-orange-500/80',
        bgColor: 'bg-orange-500/15',
        badgeBg: 'bg-orange-500/20 text-orange-300 border-orange-500/40',
        glow: 'shadow-orange-500/30',
        hex: '#F97316',
      };
    case 'legendary':
      return {
        label: 'Hoàng Kim',
        textColor: 'text-amber-400',
        borderColor: 'border-amber-400/80',
        bgColor: 'bg-amber-500/15',
        badgeBg: 'bg-amber-500/20 text-amber-300 border-amber-500/40',
        glow: 'shadow-amber-500/30',
        hex: '#F59E0B',
      };
    case 'epic':
      return {
        label: 'U Minh',
        textColor: 'text-purple-400',
        borderColor: 'border-purple-400/80',
        bgColor: 'bg-purple-500/15',
        badgeBg: 'bg-purple-500/20 text-purple-300 border-purple-500/40',
        glow: 'shadow-purple-500/30',
        hex: '#A855F7',
      };
    case 'rare':
      return {
        label: 'Cổ Thiết',
        textColor: 'text-cyan-400',
        borderColor: 'border-cyan-400/80',
        bgColor: 'bg-cyan-500/15',
        badgeBg: 'bg-cyan-500/20 text-cyan-300 border-cyan-500/40',
        glow: 'shadow-cyan-500/30',
        hex: '#06B6D4',
      };
    default:
      return {
        label: 'Phàm Thiết',
        textColor: 'text-slate-200',
        borderColor: 'border-slate-700/80',
        bgColor: 'bg-slate-800/40',
        badgeBg: 'bg-slate-800/60 text-slate-300 border-slate-700/50',
        glow: 'shadow-slate-700/20',
        hex: '#94A3B8',
      };
  }
}"""

    new_rarity_meta = """export function getItemRarityMeta(rarity: ItemRarity) {
  switch (rarity) {
    case 'tier_s':
    case 'mythic':
      return {
        tier: 'S' as const,
        label: 'Tier S · Thiên Đạo Thần Khí',
        shortLabel: 'Tier S',
        subName: 'Thiên Đạo Thần Khí',
        textColor: 'text-red-400',
        borderColor: 'border-red-500/90',
        bgColor: 'bg-red-500/15',
        badgeBg: 'bg-red-500/25 text-red-300 border-red-500/50',
        glow: 'shadow-red-500/40',
        hex: '#EF4444',
        statMultiplier: 5.5,
        maxSockets: 4,
        maxAffixes: 4,
      };
    case 'tier_a':
    case 'legendary':
      return {
        tier: 'A' as const,
        label: 'Tier A · Địa Linh Kim',
        shortLabel: 'Tier A',
        subName: 'Địa Linh Kim',
        textColor: 'text-amber-400',
        borderColor: 'border-amber-400/90',
        bgColor: 'bg-amber-500/15',
        badgeBg: 'bg-amber-500/25 text-amber-300 border-amber-500/50',
        glow: 'shadow-amber-500/40',
        hex: '#F59E0B',
        statMultiplier: 3.8,
        maxSockets: 3,
        maxAffixes: 4,
      };
    case 'tier_b':
    case 'epic':
      return {
        tier: 'B' as const,
        label: 'Tier B · Huyền Thiết',
        shortLabel: 'Tier B',
        subName: 'Huyền Thiết',
        textColor: 'text-purple-400',
        borderColor: 'border-purple-400/90',
        bgColor: 'bg-purple-500/15',
        badgeBg: 'bg-purple-500/25 text-purple-300 border-purple-500/50',
        glow: 'shadow-purple-500/40',
        hex: '#A855F7',
        statMultiplier: 2.6,
        maxSockets: 2,
        maxAffixes: 3,
      };
    case 'tier_c':
    case 'rare':
      return {
        tier: 'C' as const,
        label: 'Tier C · Cổ Đồng',
        shortLabel: 'Tier C',
        subName: 'Cổ Đồng',
        textColor: 'text-blue-400',
        borderColor: 'border-blue-400/90',
        bgColor: 'bg-blue-500/15',
        badgeBg: 'bg-blue-500/25 text-blue-300 border-blue-500/50',
        glow: 'shadow-blue-500/40',
        hex: '#3B82F6',
        statMultiplier: 1.85,
        maxSockets: 2,
        maxAffixes: 2,
      };
    case 'tier_d':
    case 'uncommon':
      return {
        tier: 'D' as const,
        label: 'Tier D · Tinh Thiết',
        shortLabel: 'Tier D',
        subName: 'Tinh Thiết',
        textColor: 'text-emerald-400',
        borderColor: 'border-emerald-500/90',
        bgColor: 'bg-emerald-500/15',
        badgeBg: 'bg-emerald-500/25 text-emerald-300 border-emerald-500/50',
        glow: 'shadow-emerald-500/40',
        hex: '#10B981',
        statMultiplier: 1.35,
        maxSockets: 1,
        maxAffixes: 1,
      };
    default:
      return {
        tier: 'E' as const,
        label: 'Tier E · Phàm Thiết',
        shortLabel: 'Tier E',
        subName: 'Phàm Thiết',
        textColor: 'text-slate-300',
        borderColor: 'border-slate-700/80',
        bgColor: 'bg-slate-800/40',
        badgeBg: 'bg-slate-800/60 text-slate-300 border-slate-700/50',
        glow: 'shadow-slate-700/20',
        hex: '#94A3B8',
        statMultiplier: 1.0,
        maxSockets: 0,
        maxAffixes: 0,
      };
  }
}"""

    if old_rarity_meta in content:
        content = content.replace(old_rarity_meta, new_rarity_meta, 1)
        print("Updated getItemRarityMeta.")

    # 4. Update getSalvageYield
    old_salvage = """export function getSalvageYield(item: EquipmentItem): { linhThach: number; tinhHoa: number } {
  switch (item.rarity) {
    case 'mythic':
      return { linhThach: 1200, tinhHoa: 8 };
    case 'legendary':
      return { linhThach: 400, tinhHoa: 3 };
    case 'epic':
      return { linhThach: 120, tinhHoa: 1 };
    case 'rare':
      return { linhThach: 45, tinhHoa: 0 };
    default:
      return { linhThach: 15, tinhHoa: 0 };
  }
}"""

    new_salvage = """export function getSalvageYield(item: EquipmentItem): {
  linhThach: number;
  tinhHoa: number;
  ironDust: number;
  celestialStar: number;
} {
  const meta = getItemRarityMeta(item.rarity);
  switch (meta.tier) {
    case 'S':
      return { linhThach: 0, tinhHoa: 20, ironDust: 1000, celestialStar: 1 };
    case 'A':
      return { linhThach: 0, tinhHoa: 5, ironDust: 350, celestialStar: 0 };
    case 'B':
      return { linhThach: 0, tinhHoa: 1, ironDust: 120, celestialStar: 0 };
    case 'C':
      return { linhThach: 100, tinhHoa: 0, ironDust: 45, celestialStar: 0 };
    case 'D':
      return { linhThach: 30, tinhHoa: 0, ironDust: 15, celestialStar: 0 };
    default:
      return { linhThach: 10, tinhHoa: 0, ironDust: 5, celestialStar: 0 };
  }
}"""

    if old_salvage in content:
        content = content.replace(old_salvage, new_salvage, 1)
        print("Updated getSalvageYield.")

    # 5. Add Floor Tier Weights & Drop Engine & World Raid Clear Chest
    drop_tables_block = """// ============================================================================
// MMORPG DROP SYSTEM: 6-TIER (E -> S) MATRICES, PITY COUNTERS & RAID CLEAR CHESTS
// ============================================================================
export interface FloorTierWeights {
  tierE: number;
  tierD: number;
  tierC: number;
  tierB: number;
  tierA: number;
  tierS: number;
}

export const FLOOR_TIER_DROP_WEIGHTS: Record<number, FloorTierWeights> = {
  1: { tierE: 62.0, tierD: 30.0, tierC: 7.20, tierB: 0.78, tierA: 0.02, tierS: 0.00 },
  2: { tierE: 48.0, tierD: 36.0, tierC: 13.5, tierB: 2.40, tierA: 0.10, tierS: 0.00 },
  3: { tierE: 35.0, tierD: 38.0, tierC: 21.0, tierB: 5.65, tierA: 0.34, tierS: 0.01 },
  4: { tierE: 24.0, tierD: 36.0, tierC: 28.5, tierB: 10.6, tierA: 0.87, tierS: 0.03 },
  5: { tierE: 15.0, tierD: 31.0, tierC: 34.0, tierB: 17.8, tierA: 2.12, tierS: 0.08 },
  6: { tierE: 8.0,  tierD: 25.0, tierC: 38.0, tierB: 24.5, tierA: 4.30, tierS: 0.20 },
  7: { tierE: 4.0,  tierD: 18.0, tierC: 39.0, tierB: 31.0, tierA: 7.55, tierS: 0.45 },
  8: { tierE: 1.5,  tierD: 11.5, tierC: 36.0, tierB: 37.5, tierA: 12.5, tierS: 1.00 },
  9: { tierE: 0.0,  tierD: 6.0,  tierC: 30.0, tierB: 43.0, tierA: 19.0, tierS: 2.00 },
};

export function pickTierFromWeights(weights: FloorTierWeights): ItemRarity {
  const roll = Math.random() * 100;
  let cum = 0;
  cum += weights.tierS;
  if (roll < cum) return 'mythic'; // Tier S
  cum += weights.tierA;
  if (roll < cum) return 'legendary'; // Tier A
  cum += weights.tierB;
  if (roll < cum) return 'epic'; // Tier B
  cum += weights.tierC;
  if (roll < cum) return 'rare'; // Tier C
  cum += weights.tierD;
  if (roll < cum) return 'uncommon'; // Tier D
  return 'common'; // Tier E
}

export interface RollLootDropOptions {
  grade: JudgmentGrade;
  isOverdrive?: boolean;
  isShieldBreak?: boolean;
  magicFindPct?: number;
  vaultFloorId?: number;
  anvilPityCount?: number;
}

export interface RollLootDropResult {
  item: EquipmentItem | null;
  newPityCount: number;
  isPityTriggered: boolean;
}

export function rollLootDrop(options: RollLootDropOptions): RollLootDropResult {
  const {
    grade,
    isOverdrive = false,
    isShieldBreak = false,
    magicFindPct = 0,
    vaultFloorId = 1,
    anvilPityCount = 0,
  } = options;

  if (grade === 'MISS') {
    return { item: null, newPityCount: anvilPityCount, isPityTriggered: false };
  }

  // Base Trigger Chances (Section 5.2):
  // Normal (GREAT): 0.40%, Perfect: 1.20%, Overdrive: 2.50%, Shield Break: 100%
  let triggerChance = 0.004;
  if (grade === 'PERFECT') triggerChance = 0.012;
  if (isOverdrive) triggerChance = Math.max(triggerChance, 0.025);
  if (isShieldBreak) triggerChance = 1.0;

  // Apply Magic Find from SPI (Soft capped at +50%)
  const mfMult = 1 + Math.min(50, Math.max(0, magicFindPct)) / 100;
  triggerChance = Math.min(1.0, triggerChance * mfMult);

  if (Math.random() > triggerChance) {
    return { item: null, newPityCount: anvilPityCount, isPityTriggered: false };
  }

  // A drop triggered! Now check Pity:
  let updatedPity = anvilPityCount + 1;
  let rolledRarity: ItemRarity = 'common';
  let isPityTriggered = false;

  if (updatedPity >= 200) {
    // 200 drops pity: Guaranteed Tier A (legendary)
    rolledRarity = 'legendary';
    updatedPity = 0;
    isPityTriggered = true;
  } else if (updatedPity >= 50 && Math.random() < 0.5) {
    // 50 drops pity: Guaranteed Tier B (epic)
    rolledRarity = 'epic';
    isPityTriggered = true;
  } else {
    const weights = FLOOR_TIER_DROP_WEIGHTS[vaultFloorId] || FLOOR_TIER_DROP_WEIGHTS[1];
    rolledRarity = pickTierFromWeights(weights);
  }

  // If Tier B, A, or S drops naturally, reset pity counter
  if (rolledRarity === 'mythic' || rolledRarity === 'legendary' || rolledRarity === 'epic') {
    updatedPity = 0;
  }

  const item = generateProceduralItem({ minRarity: rolledRarity, itemLevel: vaultFloorId });
  return { item, newPityCount: updatedPity, isPityTriggered };
}

// ============================================================================
// KÊNH DROP 2: RƯƠNG CHIẾN LỢI PHẨM THẾ GIỚI KHI PHÁ VÒM (WORLD RAID CLEAR CHESTS)
// ============================================================================
export type RaidChestRank = 'C' | 'B' | 'A' | 'S' | 'MVP';

export interface RaidChestReward {
  rank: RaidChestRank;
  rankTitle: string;
  items: EquipmentItem[];
  ironDustReward: number;
  celestialStarReward: number;
  raidPityGranted: number;
  guaranteedTierSTriggered: boolean;
}

export function openWorldRaidClearChest(options: {
  rank: RaidChestRank;
  vaultFloorId: number;
  raidPityCount: number;
  playerStance?: StanceKey;
}): RaidChestReward {
  const { rank, vaultFloorId, raidPityCount, playerStance = 'Q' } = options;

  let itemCount = 2;
  let rankTitle = 'Rương Đồng Tâm (Hạng C)';
  let raidPityGranted = 1;
  let ironDustReward = 50;
  let celestialStarReward = 0;

  if (rank === 'B') {
    itemCount = 3;
    rankTitle = 'Rương Tinh Anh (Hạng B)';
    ironDustReward = 150;
  } else if (rank === 'A') {
    itemCount = 4;
    rankTitle = 'Rương Hộ Pháp (Hạng A)';
    ironDustReward = 300;
  } else if (rank === 'S') {
    itemCount = 5;
    rankTitle = 'Rương Tông Sư (Hạng S)';
    raidPityGranted = 3;
    ironDustReward = 600;
    celestialStarReward = 1;
  } else if (rank === 'MVP') {
    itemCount = 6;
    rankTitle = 'Rương Thái Thượng (MVP)';
    raidPityGranted = 3;
    ironDustReward = 1200;
    celestialStarReward = 2;
  }

  const items: EquipmentItem[] = [];
  const totalPity = raidPityCount + raidPityGranted;
  let guaranteedTierSTriggered = false;

  // Check 50 Raid Seals Pity -> 100% Tier S Smart Loot
  if (totalPity >= 50) {
    guaranteedTierSTriggered = true;
    const smartSetId: EquipmentSetId =
      playerStance === 'W'
        ? 'set_fire'
        : playerStance === 'E'
        ? 'set_gravity'
        : playerStance === 'R'
        ? 'set_mystic'
        : 'set_thunder';

    const tierSItem = generateProceduralItem({
      minRarity: 'mythic',
      itemLevel: Math.max(vaultFloorId, 5),
    });
    tierSItem.setId = smartSetId;
    tierSItem.setName = EQUIPMENT_SETS[smartSetId].name;
    items.push(tierSItem);
  }

  const remaining = itemCount - items.length;
  for (let i = 0; i < remaining; i++) {
    let rarity: ItemRarity = 'rare';
    const roll = Math.random() * 100;
    if (rank === 'MVP' && i === 0) {
      rarity = roll < 18 ? 'mythic' : 'legendary';
    } else if (rank === 'S' && i === 0 && vaultFloorId >= 5) {
      rarity = roll < 10 ? 'mythic' : 'legendary';
    } else if (rank === 'A' && i === 0) {
      rarity = roll < 4 ? 'mythic' : roll < 45 ? 'legendary' : 'epic';
    } else {
      const weights = FLOOR_TIER_DROP_WEIGHTS[vaultFloorId] || FLOOR_TIER_DROP_WEIGHTS[1];
      rarity = pickTierFromWeights(weights);
    }
    items.push(generateProceduralItem({ minRarity: rarity, itemLevel: vaultFloorId }));
  }

  return {
    rank,
    rankTitle,
    items,
    ironDustReward,
    celestialStarReward,
    raidPityGranted,
    guaranteedTierSTriggered,
  };
}

export function ascendEquipmentTier(item: EquipmentItem): EquipmentItem | null {
  const meta = getItemRarityMeta(item.rarity);
  if (meta.tier !== 'A') return null;

  const newBaseVal = Math.round(item.baseStatValue * (5.5 / 3.8));
  return {
    ...item,
    id: `ascended_${Date.now()}_${item.id}`,
    rarity: 'mythic',
    name: item.name.replace('Địa Linh Kim', 'Thiên Đạo Thần Khí'),
    baseStatValue: newBaseVal,
    itemLevel: item.itemLevel + 5,
  };
}

export function getMaxInventorySlots(forgerRankTier: number): number {
  return Math.min(64, Math.max(24, 20 + forgerRankTier * 4));
}
"""

    # Replace old rollLootDrop with drop_tables_block
    old_roll_loot = """export function rollLootDrop(
  grade: JudgmentGrade,
  isOverdrive: boolean = false,
  isShieldBreak: boolean = false
): EquipmentItem | null {
  if (grade === 'MISS') return null;

  // Drop chances
  let dropChance = 0.035; // 3.5% on great
  if (grade === 'PERFECT') dropChance = 0.12; // 12% on perfect
  if (isOverdrive) dropChance = Math.max(dropChance, 0.22); // 22% on overdrive
  if (isShieldBreak) dropChance = 1.0; // 100% on shield break

  if (Math.random() > dropChance) return null;

  // Roll rarity
  const roll = Math.random();
  let rarity: ItemRarity = 'common';

  if (isShieldBreak) {
    if (roll < 0.08) rarity = 'mythic';
    else if (roll < 0.35) rarity = 'legendary';
    else if (roll < 0.80) rarity = 'epic';
    else rarity = 'rare';
  } else if (grade === 'PERFECT' || isOverdrive) {
    if (roll < 0.01) rarity = 'mythic';
    else if (roll < 0.06) rarity = 'legendary';
    else if (roll < 0.24) rarity = 'epic';
    else if (roll < 0.60) rarity = 'rare';
    else rarity = 'common';
  } else {
    if (roll < 0.03) rarity = 'epic';
    else if (roll < 0.25) rarity = 'rare';
    else rarity = 'common';
  }

  return generateProceduralItem({ minRarity: rarity });
}"""

    if old_roll_loot in content:
        content = content.replace(old_roll_loot, drop_tables_block, 1)
        print("Updated rollLootDrop with MMORPG v3.2 drop tables & pity.")
    else:
        print("[Notice] rollLootDrop not matched exactly, checking with normalized...")
        old_norm = "\n".join([line.rstrip() for line in old_roll_loot.splitlines()])
        content_norm = "\n".join([line.rstrip() for line in content.splitlines()])
        if old_norm in content_norm:
            content = content_norm.replace(old_norm, drop_tables_block, 1)
            print("Updated rollLootDrop with normalized lines.")

    # 6. Add magicFindPct to ArsenalBonuses interface and calculation
    if "magicFindPct: number;" not in content:
        content = content.replace(
            "  critRateEffective: number;\n  piercePct: number;",
            "  critRateEffective: number;\n  piercePct: number;\n  magicFindPct: number;"
        )
        content = content.replace(
            "    critRateEffective,\n    piercePct,\n  };",
            "    critRateEffective,\n    piercePct,\n    magicFindPct: Math.min(50, Math.round(rawSPI * 0.4)),\n  };"
        )
        print("Added magicFindPct to ArsenalBonuses.")

    with open('frontend/src/game/rules.ts', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patch rules.ts complete!")

if __name__ == '__main__':
    main()
