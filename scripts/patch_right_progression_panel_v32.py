# -*- coding: utf-8 -*-
"""
Script to apply v3.2 MMORPG UI upgrades to frontend/src/components/RightProgressionPanel.tsx
"""
import sys

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def main():
    with open('frontend/src/components/RightProgressionPanel.tsx', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update imports
    old_imports = """  formatInteger,
  QuenchType,
  QUENCH_OPTIONS,
} from '../game/rules';"""

    new_imports = """  formatInteger,
  QuenchType,
  QUENCH_OPTIONS,
  getMaxInventorySlots,
  ascendEquipmentTier,
} from '../game/rules';"""

    if old_imports in content:
        content = content.replace(old_imports, new_imports, 1)
        print("Updated imports.")

    # 2. Update RightProgressionPanelProps interface
    old_props_iface = """  playerTotalDamage: number;
  burnStacks?: number;
  linhThach: number;
  tinhHoa: number;
  tier2Unlocked?: boolean;
  leaderboard: LeaderboardEntry[];
  mobileDrawerOpen: boolean;
  onCloseMobileDrawer: () => void;
  onBuyUpgrade: (upgradeId: string) => void;
  onUnlockSpiritNode?: (nodeId: string) => void;
  onUnlockStanceSkill: (skillId: string) => void;
  onEquipItem: (item: EquipmentItem) => void;
  onUnequipItem: (slotKey: EquipmentSlotKey) => void;
  onSalvageItem: (item: EquipmentItem) => void;
  onQuickSalvage: (rarities: ItemRarity[]) => void;
  onQuenchItem?: (itemId: string, quenchType: QuenchType) => void;
}"""

    new_props_iface = """  playerTotalDamage: number;
  burnStacks?: number;
  linhThach: number;
  tinhHoa: number;
  ironDust?: number;
  celestialStars?: number;
  anvilPityCount?: number;
  raidPityCount?: number;
  tier2Unlocked?: boolean;
  leaderboard: LeaderboardEntry[];
  mobileDrawerOpen: boolean;
  onCloseMobileDrawer: () => void;
  onBuyUpgrade: (upgradeId: string) => void;
  onUnlockSpiritNode?: (nodeId: string) => void;
  onUnlockStanceSkill: (skillId: string) => void;
  onEquipItem: (item: EquipmentItem) => void;
  onUnequipItem: (slotKey: EquipmentSlotKey) => void;
  onSalvageItem: (item: EquipmentItem) => void;
  onQuickSalvage: (rarities: ItemRarity[]) => void;
  onQuenchItem?: (itemId: string, quenchType: QuenchType) => void;
  onAscendItem?: (item: EquipmentItem) => void;
  autoSalvageTiers?: { tierE: boolean; tierD: boolean; tierC: boolean };
  onToggleAutoSalvage?: (tierKey: 'tierE' | 'tierD' | 'tierC') => void;
}"""

    if old_props_iface in content:
        content = content.replace(old_props_iface, new_props_iface, 1)
        print("Updated RightProgressionPanelProps interface.")

    # 3. Update component parameter destructuring
    old_destruct = """  playerTotalDamage,
  burnStacks = 0,
  linhThach,
  tinhHoa,
  tier2Unlocked = false,
  leaderboard,
  mobileDrawerOpen,
  onCloseMobileDrawer,
  onBuyUpgrade,
  onUnlockSpiritNode,
  onUnlockStanceSkill,
  onEquipItem,
  onUnequipItem,
  onSalvageItem,
  onQuickSalvage,
  onQuenchItem,
}) => {"""

    new_destruct = """  playerTotalDamage,
  burnStacks = 0,
  linhThach,
  tinhHoa,
  ironDust = 0,
  celestialStars = 0,
  anvilPityCount = 0,
  raidPityCount = 0,
  tier2Unlocked = false,
  leaderboard,
  mobileDrawerOpen,
  onCloseMobileDrawer,
  onBuyUpgrade,
  onUnlockSpiritNode,
  onUnlockStanceSkill,
  onEquipItem,
  onUnequipItem,
  onSalvageItem,
  onQuickSalvage,
  onQuenchItem,
  onAscendItem,
  autoSalvageTiers = { tierE: false, tierD: false, tierC: false },
  onToggleAutoSalvage,
}) => {"""

    if old_destruct in content:
        content = content.replace(old_destruct, new_destruct, 1)
        print("Updated component destructuring.")

    # 4. Update Resource Bar Summary
    old_res_bar = """      {/* Resource Bar Summary */}
      <div className="flex items-center justify-between px-3 py-1.5 rounded-lg bg-[#080A10] border border-slate-800/80 mb-2.5 font-tech text-xs shrink-0">
        <div>
          <span className="text-slate-400">Linh Thạch: </span>
          <span className="text-cyan-300 font-bold">{linhThach.toLocaleString('en-US')}</span>
        </div>
        <span>·</span>
        <div>
          <span className="text-slate-400">Tinh Hoa: </span>
          <span className="text-amber-300 font-bold">{tinhHoa}</span>
        </div>
        <span>·</span>
        <div>
          <span className="text-slate-400">Thần Hồn: </span>
          <span className="text-emerald-300 font-bold">x{spiritTotalMult.toFixed(2)}</span>
        </div>
      </div>"""

    new_res_bar = """      {/* Resource Bar Summary */}
      <div className="flex items-center justify-between px-2.5 py-1.5 rounded-lg bg-[#080A10] border border-slate-800/80 mb-2.5 font-tech text-[11px] shrink-0 overflow-x-auto gap-1.5">
        <div className="whitespace-nowrap">
          <span className="text-slate-400">LT: </span>
          <span className="text-cyan-300 font-bold">{linhThach.toLocaleString('en-US')}</span>
        </div>
        <span>·</span>
        <div className="whitespace-nowrap">
          <span className="text-slate-400">Tinh Hoa: </span>
          <span className="text-amber-300 font-bold">{tinhHoa}</span>
        </div>
        <span>·</span>
        <div className="whitespace-nowrap">
          <span className="text-slate-400">Bụi Thiết: </span>
          <span className="text-slate-200 font-bold">{ironDust.toLocaleString('en-US')}</span>
        </div>
        {celestialStars > 0 && (
          <>
            <span>·</span>
            <div className="whitespace-nowrap">
              <span className="text-purple-400 font-bold">✨ {celestialStars} Thiên Tinh</span>
            </div>
          </>
        )}
      </div>"""

    if old_res_bar in content:
        content = content.replace(old_res_bar, new_res_bar, 1)
        print("Updated Resource Bar Summary.")

    # 5. Update Equipped Stats Card with Ngũ Đại Thuộc Tính Rèn
    old_stats_card = """            {/* Top Equipped Stats Card */}
            <div className="p-2.5 rounded-xl bg-[#080A10] border border-amber-500/30 flex items-center justify-between">
              <div>
                <div className="text-[10px] text-slate-400 font-tech">Sức Mạnh Bộ Trang Bị Đang Mặc</div>
                <div className="text-xs font-bold text-amber-300">
                  {arsenalBonuses.totalEquippedCount}/6 Món · +{arsenalBonuses.flatDamage} DMG Cơ Bản
                </div>
              </div>
              <div className="flex items-center gap-1.5 text-[10px] font-tech text-cyan-300 bg-[#111625] px-2 py-1 rounded-lg border border-slate-800">
                <span>x{arsenalBonuses.damageMultiplier} Sát Thương</span>
                <span>·</span>
                <span>+{arsenalBonuses.critChancePct}% Crit</span>
              </div>
            </div>"""

    new_stats_card = """            {/* Ngũ Đại Thuộc Tính Rèn (Stat Triad & Synergy MMORPG Card) */}
            <div className="p-2.5 rounded-xl bg-[#080A10] border border-amber-500/30 flex flex-col gap-2">
              <div className="flex items-center justify-between">
                <span className="text-[11px] font-tech font-bold text-amber-300">
                  NGŨ ĐẠI THUỘC TÍNH RÈN (MMORPG STATS)
                </span>
                <span className="text-[10px] font-tech text-slate-400">
                  {arsenalBonuses.totalEquippedCount}/6 Món Trang Bị
                </span>
              </div>

              {/* 5 Core Attributes Pills */}
              <div className="grid grid-cols-5 gap-1 text-center font-tech">
                <div className="p-1 rounded bg-slate-900/80 border border-red-500/30">
                  <div className="text-[8px] text-red-400 font-bold">STR</div>
                  <div className="text-xs font-bold text-red-300">{arsenalBonuses.coreStats.str}</div>
                  <div className="text-[7px] text-slate-400 truncate">Lực Chùy</div>
                </div>
                <div className="p-1 rounded bg-slate-900/80 border border-yellow-500/30">
                  <div className="text-[8px] text-yellow-400 font-bold">DEX</div>
                  <div className="text-xs font-bold text-yellow-300">{arsenalBonuses.coreStats.dex}</div>
                  <div className="text-[7px] text-slate-400 truncate">Chuẩn Xác</div>
                </div>
                <div className="p-1 rounded bg-slate-900/80 border border-orange-500/30">
                  <div className="text-[8px] text-orange-400 font-bold">INT</div>
                  <div className="text-xs font-bold text-orange-300">{arsenalBonuses.coreStats.int}</div>
                  <div className="text-[7px] text-slate-400 truncate">Nhiệt Lực</div>
                </div>
                <div className="p-1 rounded bg-slate-900/80 border border-purple-500/30">
                  <div className="text-[8px] text-purple-400 font-bold">PEN</div>
                  <div className="text-xs font-bold text-purple-300">{arsenalBonuses.coreStats.pen}</div>
                  <div className="text-[7px] text-slate-400 truncate">Phá Phách</div>
                </div>
                <div className="p-1 rounded bg-slate-900/80 border border-emerald-500/30">
                  <div className="text-[8px] text-emerald-400 font-bold">SPI</div>
                  <div className="text-xs font-bold text-emerald-300">{arsenalBonuses.coreStats.spi}</div>
                  <div className="text-[7px] text-slate-400 truncate">Cộng Hưởng</div>
                </div>
              </div>

              {/* Stat Synergy Indicators */}
              <div className="flex items-center justify-between text-[10px] font-tech text-slate-300 pt-1 border-t border-slate-800/80">
                <div className="flex items-center gap-1">
                  {arsenalBonuses.glancingHitPenalty ? (
                    <span className="text-red-400 font-bold bg-red-950/60 px-1.5 py-0.5 rounded border border-red-500/40 animate-pulse">
                      ⚠️ DỘI BÚA (STR &gt; 2.5 INT: -35% DMG)
                    </span>
                  ) : (
                    <span className="text-emerald-400 bg-emerald-950/60 px-1.5 py-0.5 rounded border border-emerald-500/40">
                      ✓ Cân Bằng STR/INT: {(arsenalBonuses.coreStats.str / Math.max(1, arsenalBonuses.coreStats.int)).toFixed(1)}
                    </span>
                  )}
                </div>
                <div className="flex items-center gap-2 text-cyan-300">
                  <span>Xuyên Giáp: +{arsenalBonuses.piercePct}%</span>
                  <span>·</span>
                  <span>MF: +{arsenalBonuses.magicFindPct}%</span>
                  <span>·</span>
                  <span>Crit: {arsenalBonuses.critRateEffective}%</span>
                </div>
              </div>
            </div>"""

    if old_stats_card in content:
        content = content.replace(old_stats_card, new_stats_card, 1)
        print("Updated Stats Card with Ngũ Đại Thuộc Tính Rèn.")

    # 6. Update Bag capacity calculation and quick salvage counts
    old_bag_calc = """  // Quick salvage counts
  const commonInBag = inventory.filter((it) => it.rarity === 'common').length;
  const rareInBag = inventory.filter((it) => it.rarity === 'rare').length;"""

    new_bag_calc = """  // Inventory capacity & salvage counts
  const maxInventorySlots = getMaxInventorySlots(forgerRank.tier);
  const tierECount = inventory.filter((it) => it.rarity === 'common').length;
  const tierDCount = inventory.filter((it) => it.rarity === 'uncommon').length;
  const tierCCount = inventory.filter((it) => it.rarity === 'rare').length;"""

    if old_bag_calc in content:
        content = content.replace(old_bag_calc, new_bag_calc, 1)
        print("Updated bag counts.")

    # 7. Update Inventory Grid & Pity Bar
    old_bag_section = """            {/* Backpack / Inventory */}
            <div>
              <div className="text-[11px] font-tech text-slate-300 mb-1.5 flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <span className="font-bold text-cyan-300">TÚI ĐỒ (RƯƠNG VŨ KHÍ)</span>
                  <span className="text-[10px] font-mono text-slate-400">
                    [{inventory.length}/{MAX_INVENTORY_SLOTS}]
                  </span>
                </div>

                {/* Quick Salvage Actions */}
                <div className="flex items-center gap-1">
                  {commonInBag > 0 && (
                    <button
                      type="button"
                      onClick={() => onQuickSalvage(['common'])}
                      className="px-2 py-0.5 rounded bg-slate-800 hover:bg-slate-700 border border-slate-700 text-slate-300 text-[10px] font-tech cursor-pointer transition-colors"
                      title="Phân giải toàn bộ trang bị Phàm Thiết (Trắng) trong túi"
                    >
                      Tách Trắng ({commonInBag})
                    </button>
                  )}
                  {(commonInBag > 0 || rareInBag > 0) && (
                    <button
                      type="button"
                      onClick={() => onQuickSalvage(['common', 'rare'])}
                      className="px-2 py-0.5 rounded bg-cyan-950/60 hover:bg-cyan-900/80 border border-cyan-500/40 text-cyan-300 text-[10px] font-tech cursor-pointer transition-colors"
                      title="Phân giải nhanh toàn bộ đồ Trắng & Cổ Thiết (Xanh) trong túi"
                    >
                      Tách Trắng/Xanh ({commonInBag + rareInBag})
                    </button>
                  )}
                </div>
              </div>

              {/* 24-Slot Bag Grid */}
              <div className="grid grid-cols-6 gap-1.5 p-2 rounded-xl bg-[#070912] border border-slate-800/90">
                {Array.from({ length: MAX_INVENTORY_SLOTS }).map((_, idx) => {"""

    new_bag_section = """            {/* Backpack / Inventory */}
            <div>
              <div className="text-[11px] font-tech text-slate-300 mb-1.5 flex flex-col sm:flex-row sm:items-center justify-between gap-1">
                <div className="flex items-center gap-2">
                  <span className="font-bold text-cyan-300">TÚI ĐỒ (RƯƠNG VŨ KHÍ)</span>
                  <span className="text-[10px] font-mono text-slate-400">
                    [{inventory.length}/{maxInventorySlots}]
                  </span>
                </div>

                {/* Quick Salvage Actions */}
                <div className="flex items-center gap-1 flex-wrap">
                  {tierECount > 0 && (
                    <button
                      type="button"
                      onClick={() => onQuickSalvage(['common'])}
                      className="px-1.5 py-0.5 rounded bg-slate-800 hover:bg-slate-700 border border-slate-700 text-slate-300 text-[9px] font-tech cursor-pointer transition-colors"
                      title="Phân giải toàn bộ Tier E (Phàm Thiết)"
                    >
                      Tách Tier E ({tierECount})
                    </button>
                  )}
                  {tierDCount > 0 && (
                    <button
                      type="button"
                      onClick={() => onQuickSalvage(['uncommon'])}
                      className="px-1.5 py-0.5 rounded bg-emerald-950/60 hover:bg-emerald-900/80 border border-emerald-500/40 text-emerald-300 text-[9px] font-tech cursor-pointer transition-colors"
                      title="Phân giải toàn bộ Tier D (Tinh Thiết)"
                    >
                      Tách Tier D ({tierDCount})
                    </button>
                  )}
                  {tierCCount > 0 && (
                    <button
                      type="button"
                      onClick={() => onQuickSalvage(['rare'])}
                      className="px-1.5 py-0.5 rounded bg-blue-950/60 hover:bg-blue-900/80 border border-blue-500/40 text-blue-300 text-[9px] font-tech cursor-pointer transition-colors"
                      title="Phân giải toàn bộ Tier C (Cổ Đồng)"
                    >
                      Tách Tier C ({tierCCount})
                    </button>
                  )}
                </div>
              </div>

              {/* Auto Salvage Filter Toggles */}
              <div className="flex items-center justify-between p-1.5 rounded-lg bg-slate-950/80 border border-slate-800/80 mb-1.5 text-[9px] font-tech text-slate-400">
                <span className="font-bold text-slate-300">Tự động nung chảy:</span>
                <div className="flex items-center gap-2">
                  <label className="flex items-center gap-1 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={autoSalvageTiers.tierE}
                      onChange={() => onToggleAutoSalvage?.('tierE')}
                      className="rounded accent-amber-400"
                    />
                    <span className="text-slate-300">Tier E</span>
                  </label>
                  <label className="flex items-center gap-1 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={autoSalvageTiers.tierD}
                      onChange={() => onToggleAutoSalvage?.('tierD')}
                      className="rounded accent-emerald-400"
                    />
                    <span className="text-emerald-300">Tier D</span>
                  </label>
                  <label className="flex items-center gap-1 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={autoSalvageTiers.tierC}
                      onChange={() => onToggleAutoSalvage?.('tierC')}
                      className="rounded accent-blue-400"
                    />
                    <span className="text-blue-300">Tier C</span>
                  </label>
                </div>
              </div>

              {/* Pity Counter Bar */}
              <div className="flex items-center justify-between p-1.5 rounded-lg bg-amber-950/20 border border-amber-500/30 mb-1.5 text-[9px] font-tech">
                <span className="text-amber-300">
                  🎯 Luyện Khí Pity: <b>{anvilPityCount}/200</b> <span className="text-slate-400">(Tier A)</span>
                </span>
                <span className="text-orange-300">
                  👑 Ấn Ký Hồng Hoang: <b>{raidPityCount}/50</b> <span className="text-slate-400">(Tier S)</span>
                </span>
              </div>

              {/* Dynamic Capacity Bag Grid (Up to 64 slots) */}
              <div className="grid grid-cols-6 sm:grid-cols-8 gap-1.5 p-2 rounded-xl bg-[#070912] border border-slate-800/90 max-h-52 overflow-y-auto">
                {Array.from({ length: maxInventorySlots }).map((_, idx) => {"""

    if old_bag_section in content:
        content = content.replace(old_bag_section, new_bag_section, 1)
        print("Updated Bag Section with Pity Bar & Auto-Salvage.")

    # 8. Add Tier A -> S Ascension button in Item Details
    old_item_actions = """                  <button
                    type="button"
                    onClick={() => onSalvageItem(activeSelected)}
                    className="flex-1 py-1.5 px-3 rounded-lg bg-red-950/40 hover:bg-red-900/60 border border-red-500/40 text-red-300 text-xs font-tech font-bold cursor-pointer transition-colors flex items-center justify-center gap-1"
                  >
                    <Trash2 className="w-3.5 h-3.5" />
                    Tách ({getSalvageYield(activeSelected).linhThach} LT)
                  </button>
                </div>"""

    new_item_actions = """                  <button
                    type="button"
                    onClick={() => onSalvageItem(activeSelected)}
                    className="flex-1 py-1.5 px-3 rounded-lg bg-red-950/40 hover:bg-red-900/60 border border-red-500/40 text-red-300 text-xs font-tech font-bold cursor-pointer transition-colors flex items-center justify-center gap-1"
                  >
                    <Trash2 className="w-3.5 h-3.5" />
                    Tách ({getSalvageYield(activeSelected).ironDust} Bụi)
                  </button>
                </div>

                {/* Thăng Bậc Thần Khí (Tier A -> Tier S Ascension) */}
                {getItemRarityMeta(activeSelected.rarity).tier === 'A' && (
                  <div className="pt-2 border-t border-slate-800 flex items-center justify-between gap-2">
                    <div>
                      <div className="text-[10px] font-tech font-bold text-amber-300 flex items-center gap-1">
                        <Sparkles className="w-3 h-3 text-amber-400" />
                        THĂNG BẬC THẦN KHÍ (TIER A → S):
                      </div>
                      <div className="text-[9px] text-slate-400">
                        Chi phí: 1,000 Bụi Thiết · 10 Tinh Hoa · 1 Thiên Tinh
                      </div>
                    </div>
                    <button
                      type="button"
                      disabled={ironDust < 1000 || tinhHoa < 10 || celestialStars < 1}
                      onClick={() => onAscendItem?.(activeSelected)}
                      className={`px-2.5 py-1.5 rounded-lg text-xs font-tech font-bold transition-all shadow-md ${
                        ironDust >= 1000 && tinhHoa >= 10 && celestialStars >= 1
                          ? 'bg-gradient-to-r from-red-600 to-amber-500 text-white cursor-pointer active:scale-95 shadow-red-500/25'
                          : 'bg-slate-800 text-slate-500 cursor-not-allowed opacity-60'
                      }`}
                      title="Nâng phẩm chất từ Tier A lên Tier S (Thiên Đạo Thần Khí)!"
                    >
                      THĂNG BẬC TIER S
                    </button>
                  </div>
                )}"""

    if old_item_actions in content:
        content = content.replace(old_item_actions, new_item_actions, 1)
        print("Updated Item Actions with Ascension.")

    with open('frontend/src/components/RightProgressionPanel.tsx', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patch RightProgressionPanel.tsx complete!")

if __name__ == '__main__':
    main()
