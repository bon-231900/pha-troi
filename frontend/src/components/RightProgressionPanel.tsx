import React, { useState, useMemo } from 'react';
import {
  ForgeUpgrade,
  SpiritNode,
  EquipmentItem,
  EquipmentSlotKey,
  ItemRarity,
  SLOT_INFO,
  MAX_INVENTORY_SLOTS,
  getUpgradeCost,
  canUnlockSpiritNode,
  calculateSpiritMultiplier,
  calculateForgeDamage,
  getItemRarityMeta,
  getSalvageYield,
  calculateArsenalBonuses,
  checkForgeEquilibrium,
  EQUIPMENT_SETS,
  ForgerRank,
  FORGER_RANKS,
  getForgerRank,
  StanceSkillNode,
  canUnlockStanceSkill,
  StanceKey,
  HAMMER_STANCES,
  formatInteger,
  QuenchType,
  QUENCH_OPTIONS,
  getMaxInventorySlots,
  ascendEquipmentTier,
  PlayerClassMeta,
  RuneGem,
  RuneType,
  RuneTier,
  getTemperCost,
  getAscensionCost,
  getUnlockedSockets,
} from '../game/rules';

const ITEM_ART_URLS: Record<EquipmentSlotKey, string> = {
  hammer: '/assets/art/items/item_hammer.webp',
  anvil: '/assets/art/items/item_anvil.webp',
  bellows: '/assets/art/items/item_bellows.webp',
  gauntlets: '/assets/art/items/item_gauntlets.webp',
  apron: '/assets/art/items/item_apron.webp',
  relic: '/assets/art/items/item_relic.webp',
};
import {
  Hammer,
  Sparkles,
  Trophy,
  X,
  Check,
  Lock,
  Shield,
  Flame,
  Zap,
  Layers,
  Trash2,
  PackageOpen,
  ArrowRightLeft,
  Info,
  Gem,
  ChevronRight,
  Plus,
} from 'lucide-react';

export interface LeaderboardEntry {
  id: string;
  name: string;
  sect: string;
  damage: number; // Integer DMG
  damageBillions?: number; // legacy fallback
  isPlayer?: boolean;
}

interface RightProgressionPanelProps {
  equippedItems: Record<EquipmentSlotKey, EquipmentItem | null>;
  inventory: EquipmentItem[];
  upgrades: ForgeUpgrade[];
  spiritNodes?: SpiritNode[];
  stanceSkills: StanceSkillNode[];
  forgerRank: ForgerRank;
  playerTotalDamage: number;
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
  playerClass?: PlayerClassMeta;
  runePouch?: RuneGem[];
  onTemperEquipment?: (slotKey: EquipmentSlotKey) => void;
  onAscendEquipment?: (slotKey: EquipmentSlotKey) => void;
  onSocketGem?: (slotKey: EquipmentSlotKey, socketIndex: number, gemId: string) => void;
  onUnsocketGem?: (slotKey: EquipmentSlotKey, socketIndex: number) => void;
}

export const RightProgressionPanel: React.FC<RightProgressionPanelProps> = ({
  equippedItems,
  inventory,
  upgrades,
  spiritNodes = [],
  stanceSkills,
  forgerRank,
  playerTotalDamage,
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
  playerClass,
  runePouch = [],
  onTemperEquipment,
  onAscendEquipment,
  onSocketGem,
  onUnsocketGem,
}) => {
  const [activeTab, setActiveTab] = useState<'arsenal' | 'upgrades' | 'spirit' | 'leaderboard'>('arsenal');
  const [selectedSlotKey, setSelectedSlotKey] = useState<EquipmentSlotKey>('hammer');
  const [gemPouchFilter, setGemPouchFilter] = useState<RuneType | 'all'>('all');
  const [selectedItem, setSelectedItem] = useState<EquipmentItem | null>(() => {
    return equippedItems.hammer || inventory[0] || null;
  });
  const [selectedStanceTree, setSelectedStanceTree] = useState<StanceKey>('Q');
  const [selectedSkillNodeId, setSelectedSkillNodeId] = useState<string>('q_tier_1');
  const [selectedNodeId, setSelectedNodeId] = useState<string>('node_thunder_eye');

  // Always resolve freshest reference from equippedItems or inventory
  const activeSelected = useMemo(() => {
    if (!selectedItem) return null;
    for (const k of Object.keys(equippedItems) as EquipmentSlotKey[]) {
      if (equippedItems[k]?.id === selectedItem.id) return equippedItems[k];
    }
    return inventory.find((it) => it.id === selectedItem.id) || selectedItem;
  }, [selectedItem, equippedItems, inventory]);

  const selectedNode =
    spiritNodes.find((n) => n.id === selectedNodeId) || spiritNodes[0];
  const spiritTotalMult = calculateSpiritMultiplier(spiritNodes);

  const arsenalBonuses = calculateArsenalBonuses(equippedItems, upgrades);

  // Helper: check if item is currently equipped
  const isEquipped = (item: EquipmentItem | null): boolean => {
    if (!item) return false;
    return equippedItems[item.slotKey]?.id === item.id;
  };

  // Inventory capacity & salvage counts
  const maxInventorySlots = getMaxInventorySlots(forgerRank.tier);
  const tierECount = inventory.filter((it) => it.rarity === 'common').length;
  const tierDCount = inventory.filter((it) => it.rarity === 'uncommon').length;
  const tierCCount = inventory.filter((it) => it.rarity === 'rare').length;

  const renderPanelContent = () => (
    <div className="flex flex-col h-full">
      {/* 4 Segmented Control Tabs */}
      <div
        role="tablist"
        aria-label="Quản lý Vũ Khí, Rèn Đúc, Thần Hồn và Bảng Vàng"
        className="grid grid-cols-4 gap-1 p-1 bg-[#080A10] border border-slate-800 rounded-xl mb-3 shrink-0"
      >
        <button
          type="button"
          role="tab"
          aria-selected={activeTab === 'arsenal'}
          onClick={() => setActiveTab('arsenal')}
          className={`flex items-center justify-center gap-1 py-1.5 px-1 rounded-lg text-xs font-medium transition-colors cursor-pointer whitespace-nowrap ${
            activeTab === 'arsenal'
              ? 'bg-amber-400 text-slate-950 font-bold'
              : 'text-slate-300 hover:text-white'
          }`}
          title="Trang Bị & Túi Đồ (Loot & Affix)"
        >
          <Shield className="w-3.5 h-3.5" />
          <span className="truncate">Vũ Khí</span>
        </button>

        <button
          type="button"
          role="tab"
          aria-selected={activeTab === 'upgrades'}
          onClick={() => setActiveTab('upgrades')}
          className={`flex items-center justify-center gap-1 py-1.5 px-1 rounded-lg text-xs font-medium transition-colors cursor-pointer whitespace-nowrap ${
            activeTab === 'upgrades'
              ? 'bg-amber-400 text-slate-950 font-bold'
              : 'text-slate-300 hover:text-white'
          }`}
          title="Nâng Cấp Lò Rèn"
        >
          <Hammer className="w-3.5 h-3.5" />
          <span className="truncate">Lò Rèn</span>
        </button>

        <button
          type="button"
          role="tab"
          aria-selected={activeTab === 'spirit'}
          onClick={() => setActiveTab('spirit')}
          className={`flex items-center justify-center gap-1 py-1.5 px-1 rounded-lg text-xs font-medium transition-colors cursor-pointer whitespace-nowrap ${
            activeTab === 'spirit'
              ? 'bg-cyan-400 text-slate-950 font-bold'
              : 'text-slate-300 hover:text-white'
          }`}
          title="Kỹ Pháp Tứ Thế & Đẳng Cấp Thợ Rèn"
        >
          <Sparkles className="w-3.5 h-3.5" />
          <span className="truncate">Kỹ Pháp</span>
        </button>

        <button
          type="button"
          role="tab"
          aria-selected={activeTab === 'leaderboard'}
          onClick={() => setActiveTab('leaderboard')}
          className={`flex items-center justify-center gap-1 py-1.5 px-1 rounded-lg text-xs font-medium transition-colors cursor-pointer whitespace-nowrap ${
            activeTab === 'leaderboard'
              ? 'bg-amber-400 text-slate-950 font-bold'
              : 'text-slate-300 hover:text-white'
          }`}
          title="Bảng Vàng Vạn Dân"
        >
          <Trophy className="w-3.5 h-3.5" />
          <span className="truncate">Bảng Vàng</span>
        </button>
      </div>

      {/* Resource Bar Summary */}
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
      </div>

      {/* Tab Body */}
      <div className="flex-1 overflow-y-auto pr-0.5 space-y-2.5">
        {/* ================================================================= */}
        {/* TAB 1: ARSENAL & BACKPACK (ARPG LOOT & AFFIX SYSTEM) */}
        {/* ================================================================= */}
        {activeTab === 'arsenal' && (
          <div className="flex flex-col gap-2.5">
            {/* 1. Ngũ Đại Thuộc Tính Rèn (MMORPG Stats Card) */}
            <div className="p-2.5 rounded-xl bg-[#080A10] border border-amber-500/30 flex flex-col gap-2 shadow-inner">
              <div className="flex items-center justify-between">
                <span className="text-[11px] font-tech font-bold text-amber-300 flex items-center gap-1.5">
                  <Shield className="w-3.5 h-3.5 text-amber-400" />
                  NGŨ ĐẠI THUỘC TÍNH RÈN (BẢN MỆNH THẦN LỰC)
                </span>
                <span className="text-[10px] font-tech text-cyan-300 font-mono">
                  {arsenalBonuses.totalEquippedCount}/6 Món Thần Khí
                </span>
              </div>

              {/* 5 Core Attributes */}
              <div className="grid grid-cols-5 gap-1 text-center font-tech">
                <div className="p-1 rounded bg-[#0E1322] border border-slate-800">
                  <div className="text-[9px] text-slate-400">Sức Mạnh</div>
                  <div className="text-xs font-bold text-red-400 font-mono">
                    {arsenalBonuses.coreStats.str}
                  </div>
                </div>
                <div className="p-1 rounded bg-[#0E1322] border border-slate-800">
                  <div className="text-[9px] text-slate-400">Khéo Léo</div>
                  <div className="text-xs font-bold text-emerald-400 font-mono">
                    {arsenalBonuses.coreStats.dex}
                  </div>
                </div>
                <div className="p-1 rounded bg-[#0E1322] border border-slate-800">
                  <div className="text-[9px] text-slate-400">Trí Tuệ</div>
                  <div className="text-xs font-bold text-blue-400 font-mono">
                    {arsenalBonuses.coreStats.int}
                  </div>
                </div>
                <div className="p-1 rounded bg-[#0E1322] border border-slate-800">
                  <div className="text-[9px] text-slate-400">Xuyên Giáp</div>
                  <div className="text-xs font-bold text-amber-400 font-mono">
                    {arsenalBonuses.coreStats.pen}
                  </div>
                </div>
                <div className="p-1 rounded bg-[#0E1322] border border-slate-800">
                  <div className="text-[9px] text-slate-400">Tâm Thần</div>
                  <div className="text-xs font-bold text-purple-400 font-mono">
                    {arsenalBonuses.coreStats.spi}
                  </div>
                </div>
              </div>

              {/* Equilibrium, Pierce, Magic Find, Crit */}
              <div className="flex items-center justify-between text-[10px] font-tech pt-1 border-t border-slate-800/80">
                <div className="flex items-center gap-1.5">
                  {arsenalBonuses.glancingHitPenalty ? (
                    <span className="text-red-400 bg-red-950/60 px-1.5 py-0.5 rounded border border-red-500/40">
                      ⚠️ Dội Búa: STR &gt; 2.5x INT (-30% DMG)
                    </span>
                  ) : (
                    <span className="text-emerald-400 bg-emerald-950/60 px-1.5 py-0.5 rounded border border-emerald-500/40">
                      ✓ Cân Bằng STR/INT: {(arsenalBonuses.coreStats.str / Math.max(1, arsenalBonuses.coreStats.int)).toFixed(1)}
                    </span>
                  )}
                </div>
                <div className="flex items-center gap-2 text-cyan-300">
                  <span>Xuyên: +{arsenalBonuses.piercePct}%</span>
                  <span>·</span>
                  <span>MF: +{arsenalBonuses.magicFindPct}%</span>
                  <span>·</span>
                  <span>Crit: {arsenalBonuses.critRateEffective}%</span>
                </div>
              </div>
            </div>

            {/* 2. LỤC ĐẠI BẢN MỆNH THẦN KHÍ (6 Fixed Equipment Slots) */}
            <div>
              <div className="text-[11px] font-tech text-slate-300 mb-1.5 flex items-center justify-between">
                <span className="font-bold text-amber-300 flex items-center gap-1">
                  <Flame className="w-3.5 h-3.5 text-orange-400" />
                  LỤC ĐẠI BẢN MỆNH THẦN KHÍ (VĨNH CỬU)
                </span>
                <span className="text-[9.5px] text-slate-400">Click chọn món để Tôi Luyện & Khảm Phù Thạch</span>
              </div>

              <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
                {(['hammer', 'anvil', 'bellows', 'gauntlets', 'apron', 'relic'] as EquipmentSlotKey[]).map(
                  (slotKey) => {
                    const item = equippedItems[slotKey];
                    const slotMeta = SLOT_INFO[slotKey];
                    const isSelected = selectedSlotKey === slotKey;
                    const rMeta = item ? getItemRarityMeta(item.rarity) : null;
                    const itemLvl = item?.level || 1;
                    const unlockedSockets = item?.unlockedSockets ?? (item ? getUnlockedSockets(item.rarity) : 0);
                    const sockets = item?.sockets || [];

                    return (
                      <button
                        key={slotKey}
                        type="button"
                        onClick={() => setSelectedSlotKey(slotKey)}
                        className={`p-2 rounded-xl border text-left transition-all cursor-pointer flex flex-col justify-between min-h-[92px] ${
                          isSelected
                            ? 'bg-slate-900/95 border-amber-400 ring-2 ring-amber-400/40 shadow-lg shadow-amber-500/10'
                            : 'bg-[#080A10] border-slate-800 hover:border-slate-700'
                        }`}
                      >
                        <div>
                          <div className="flex items-center justify-between mb-1">
                            <span className="text-[9px] font-tech uppercase text-slate-400 font-bold">
                              {slotMeta.name}
                            </span>
                            {item && (
                              <span className={`text-[8px] px-1 py-0.2 rounded font-tech ${rMeta?.badgeBg}`}>
                                Tier {rMeta?.tier}
                              </span>
                            )}
                          </div>

                          <div className="flex items-center gap-2">
                            <div className="w-10 h-10 rounded-lg bg-black/80 border border-slate-800 flex items-center justify-center shrink-0 overflow-hidden shadow-inner">
                              <img
                                src={ITEM_ART_URLS[slotKey]}
                                alt={slotMeta.name}
                                className="w-8 h-8 object-contain drop-shadow"
                              />
                            </div>
                            <div className="min-w-0 flex-1">
                              <div className={`font-semibold text-[11px] truncate ${rMeta?.textColor || 'text-slate-200'}`}>
                                {item ? item.name : slotMeta.name}
                              </div>
                              <div className="text-[9.5px] font-tech text-cyan-300 font-mono">
                                +{item?.baseStatValue || 1} {item?.baseStatUnit || 'DMG'}
                              </div>
                            </div>
                          </div>
                        </div>

                        {/* Level & Socket pips */}
                        <div className="mt-1.5 pt-1 border-t border-slate-800/80 flex items-center justify-between text-[9px] font-tech">
                          <span className="text-amber-300 font-mono font-bold">
                            Lv.{itemLvl}/20
                          </span>
                          {/* Socket Pips */}
                          <div className="flex items-center gap-0.5">
                            {Array.from({ length: 4 }).map((_, sIdx) => {
                              const isUnlocked = sIdx < unlockedSockets;
                              const gem = isUnlocked ? sockets[sIdx] : null;

                              if (!isUnlocked) {
                                return (
                                  <span key={sIdx} className="w-2 h-2 rounded-full bg-slate-950 border border-slate-800 text-[6px] text-slate-700 flex items-center justify-center" title="Lỗ khảm bị khóa">
                                    ·
                                  </span>
                                );
                              }
                              if (gem) {
                                return (
                                  <span
                                    key={sIdx}
                                    className="w-2.5 h-2.5 rounded-full flex items-center justify-center text-[7px] shadow-sm animate-pulse"
                                    style={{ backgroundColor: gem.color }}
                                    title={`Đã khảm: ${gem.name} (+${gem.value} ${gem.statLabel})`}
                                  >
                                    ★
                                  </span>
                                );
                              }
                              return (
                                <span
                                  key={sIdx}
                                  className="w-2.5 h-2.5 rounded-full border border-dashed border-cyan-400/80 bg-cyan-950/40 text-[7px] text-cyan-300 flex items-center justify-center"
                                  title="Lỗ khảm trống"
                                >
                                  ○
                                </span>
                              );
                            })}
                          </div>
                        </div>
                      </button>
                    );
                  }
                )}
              </div>
            </div>

            {/* 3. BÀN RÈN & NÂNG CẤP KHÍ GIỚI ĐƯỢC CHỌN (SELECTED WEAPON STATION) */}
            {(() => {
              const item = equippedItems[selectedSlotKey];
              if (!item) return null;

              const slotMeta = SLOT_INFO[selectedSlotKey];
              const rMeta = getItemRarityMeta(item.rarity);
              const itemLvl = item.level || 1;
              const unlockedSockets = item.unlockedSockets ?? getUnlockedSockets(item.rarity);
              const sockets = item.sockets || [];
              const temperCost = getTemperCost(item);
              const ascensionCost = getAscensionCost(item);

              const statGain =
                item.slotKey === 'apron'
                  ? 5
                  : item.slotKey === 'gauntlets'
                  ? 0.5
                  : (item.rarity === 'mythic' || item.rarity === 'legendary') && item.slotKey === 'hammer'
                  ? 2
                  : 1;

              const canAffordTemper =
                (ironDust || 0) >= temperCost.ironDust && linhThach >= temperCost.linhThach && itemLvl < 20;

              const canAffordAscension =
                ascensionCost &&
                (ironDust || 0) >= ascensionCost.ironDust &&
                tinhHoa >= ascensionCost.tinhHoa &&
                (celestialStars || 0) >= ascensionCost.celestialStars &&
                itemLvl >= 20;

              return (
                <div className="p-3 rounded-xl bg-[#090C15] border border-amber-500/40 space-y-3 shadow-xl">
                  {/* Item Header */}
                  <div className="flex items-start justify-between gap-2">
                    <div className="flex items-center gap-2.5">
                      <div className="w-12 h-12 rounded-xl bg-black/90 border border-amber-500/50 flex items-center justify-center shrink-0 overflow-hidden shadow-md">
                        <img
                          src={ITEM_ART_URLS[selectedSlotKey]}
                          alt={slotMeta.name}
                          className="w-10 h-10 object-contain drop-shadow"
                        />
                      </div>
                      <div>
                        <div className="flex items-center gap-1.5">
                          <span className="text-[10px] font-tech text-amber-400 font-bold uppercase tracking-wider">
                            {slotMeta.name}
                          </span>
                          <span className={`text-[9px] px-1.5 py-0.2 rounded font-tech ${rMeta.badgeBg}`}>
                            Tier {rMeta.tier} · {rMeta.label}
                          </span>
                        </div>
                        <h4 className={`text-sm font-bold truncate ${rMeta.textColor}`}>
                          {item.name}
                        </h4>
                        <div className="text-[11px] font-tech text-cyan-300 font-mono">
                          {item.baseStatLabel}: +{item.baseStatValue} {item.baseStatUnit}
                        </div>
                      </div>
                    </div>
                  </div>

                  {item.loreDescription && (
                    <p className="text-[10px] text-slate-400 italic bg-black/40 p-2 rounded-lg border border-slate-800/80">
                      "{item.loreDescription}"
                    </p>
                  )}

                  {/* MODULE A: TÔI LUYỆN THÉP (TEMPERING LV.1 -> 20) */}
                  <div className="p-2.5 rounded-xl bg-[#0E1322] border border-slate-800 space-y-2">
                    <div className="flex items-center justify-between text-xs font-tech">
                      <span className="flex items-center gap-1.5 font-bold text-slate-200">
                        <Hammer className="w-3.5 h-3.5 text-amber-400" />
                        TÔI LUYỆN CẤP ĐỘ KHÍ GIỚI:
                      </span>
                      <span className="text-amber-300 font-mono font-bold">
                        Cấp {itemLvl} / 20
                      </span>
                    </div>

                    {/* Level Progress Bar */}
                    <div className="w-full bg-slate-950 h-2 rounded-full overflow-hidden border border-slate-800">
                      <div
                        className="bg-gradient-to-r from-amber-500 via-orange-500 to-amber-300 h-full transition-all duration-300"
                        style={{ width: `${Math.min(100, (itemLvl / 20) * 100)}%` }}
                      />
                    </div>

                    {itemLvl < 20 ? (
                      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pt-1">
                        <div className="text-[10px] font-tech text-slate-400 flex items-center gap-2">
                          <span>Chi phí:</span>
                          <span className="text-cyan-300 font-mono font-bold">
                            {temperCost.ironDust} Bụi Thiết
                          </span>
                          <span>+</span>
                          <span className="text-amber-300 font-mono font-bold">
                            {temperCost.linhThach.toLocaleString()} LT
                          </span>
                          <span className="text-slate-500">|</span>
                          <span className="text-emerald-400 font-bold">
                            +{statGain} {item.baseStatUnit}
                          </span>
                        </div>

                        <button
                          type="button"
                          disabled={!canAffordTemper}
                          onClick={() => onTemperEquipment?.(selectedSlotKey)}
                          className={`py-1.5 px-3 rounded-lg font-tech font-bold text-xs tracking-wider transition-all flex items-center justify-center gap-1.5 ${
                            canAffordTemper
                              ? 'bg-amber-400 hover:bg-amber-300 text-slate-950 cursor-pointer shadow-md shadow-amber-500/20 active:scale-95'
                              : 'bg-slate-900 border border-slate-800 text-slate-500 cursor-not-allowed opacity-60'
                          }`}
                        >
                          <Hammer className="w-3.5 h-3.5" />
                          <span>TÔI LUYỆN CẤP {itemLvl + 1}</span>
                        </button>
                      </div>
                    ) : (
                      <div className="p-1.5 rounded-lg bg-amber-500/10 border border-amber-500/30 text-center text-[10.5px] font-tech text-amber-300 font-bold">
                        ⚡ ĐÃ ĐẠT CỰC HẠN CẤP 20/20 · SẴN SÀNG THỐI HỎA ĐỘT PHÁ BẬC!
                      </div>
                    )}
                  </div>

                  {/* MODULE B: THỐI HỎA ĐỘT PHÁ BẬC (MULTI-TIER ASCENSION) */}
                  {ascensionCost && (
                    <div className="p-2.5 rounded-xl bg-gradient-to-r from-purple-950/40 via-red-950/30 to-purple-950/40 border border-purple-500/40 space-y-2">
                      <div className="flex items-center justify-between text-xs font-tech">
                        <span className="flex items-center gap-1.5 font-bold text-purple-200">
                          <Sparkles className="w-3.5 h-3.5 text-purple-400 animate-spin" />
                          THỐI HỎA ĐỘT PHÁ PHẨM BẬC:
                        </span>
                        <span className="text-amber-300 font-bold font-mono">
                          Tiến Lên {ascensionCost.targetTierName}
                        </span>
                      </div>

                      <div className="text-[10px] font-tech text-slate-300 flex items-center gap-2 flex-wrap">
                        <span>Đột phá sẽ khai mở:</span>
                        <span className="text-cyan-300 font-bold bg-cyan-950/60 px-1.5 py-0.5 rounded border border-cyan-500/40">
                          +1 Lỗ Khảm Phù Thạch
                        </span>
                        <span>&amp;</span>
                        <span className="text-emerald-300 font-bold bg-emerald-950/60 px-1.5 py-0.5 rounded border border-emerald-500/40">
                          +60% Chỉ Số Cơ Bản
                        </span>
                      </div>

                      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pt-1 border-t border-purple-900/50">
                        <div className="text-[10px] font-tech text-slate-400 flex items-center gap-2 flex-wrap">
                          <span>Chi phí:</span>
                          <span className="text-cyan-300 font-mono font-bold">
                            {ascensionCost.ironDust.toLocaleString()} Bụi
                          </span>
                          <span>+</span>
                          <span className="text-amber-300 font-mono font-bold">
                            {ascensionCost.tinhHoa} Tinh Hoa
                          </span>
                          {ascensionCost.celestialStars > 0 && (
                            <>
                              <span>+</span>
                              <span className="text-purple-300 font-mono font-bold">
                                {ascensionCost.celestialStars} Thiên Tinh
                              </span>
                            </>
                          )}
                        </div>

                        <button
                          type="button"
                          disabled={!canAffordAscension}
                          onClick={() => onAscendEquipment?.(selectedSlotKey)}
                          className={`py-2 px-3 rounded-lg font-tech font-bold text-xs tracking-wider transition-all flex items-center justify-center gap-1.5 ${
                            canAffordAscension
                              ? 'bg-gradient-to-r from-red-600 via-purple-600 to-amber-500 hover:brightness-125 text-white shadow-lg shadow-purple-500/30 cursor-pointer active:scale-95 animate-pulse'
                              : 'bg-slate-900 border border-slate-800 text-slate-500 cursor-not-allowed opacity-60'
                          }`}
                        >
                          <Sparkles className="w-3.5 h-3.5 text-amber-300" />
                          <span>
                            {itemLvl < 20 ? 'CẦN ĐẠT CẤP 20 ĐỂ ĐỘT PHÁ' : '🔥 THỐI HỎA ĐỘT PHÁ BẬC'}
                          </span>
                        </button>
                      </div>
                    </div>
                  )}

                  {/* MODULE C: KHẢM NẠM PHÙ THẠCH (SOCKETS) */}
                  <div className="p-2.5 rounded-xl bg-[#0E1322] border border-cyan-500/30 space-y-2">
                    <div className="flex items-center justify-between text-xs font-tech">
                      <span className="flex items-center gap-1.5 font-bold text-cyan-300">
                        <Gem className="w-3.5 h-3.5 text-cyan-400" />
                        KHẢM NẠM PHÙ THẠCH THƯỢNG CỔ:
                      </span>
                      <span className="text-slate-400 font-mono text-[10px]">
                        {sockets.filter(Boolean).length}/{unlockedSockets} Lỗ Đang Khảm
                      </span>
                    </div>

                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-1.5">
                      {Array.from({ length: 4 }).map((_, sIdx) => {
                        const isUnlocked = sIdx < unlockedSockets;
                        const gem = isUnlocked ? sockets[sIdx] : null;

                        if (!isUnlocked) {
                          return (
                            <div
                              key={sIdx}
                              className="p-2 rounded-lg bg-black/40 border border-dashed border-slate-800/80 text-[10px] font-tech text-slate-600 flex items-center justify-between"
                            >
                              <div className="flex items-center gap-1.5">
                                <Lock className="w-3 h-3 text-slate-700" />
                                <span>Lỗ Khảm #{sIdx + 1} (Khóa)</span>
                              </div>
                              <span className="text-[8.5px] italic text-slate-600">Đột phá bậc để mở</span>
                            </div>
                          );
                        }

                        if (gem) {
                          return (
                            <div
                              key={sIdx}
                              className="p-2 rounded-lg bg-[#070912] border border-slate-700 flex items-center justify-between gap-1 shadow-inner"
                              style={{ borderLeftColor: gem.color, borderLeftWidth: '3px' }}
                            >
                              <div className="min-w-0 flex-1">
                                <div className="flex items-center gap-1">
                                  <span className="text-[10px] font-bold text-slate-200 truncate">
                                    {gem.name}
                                  </span>
                                  <span className="text-[8px] font-tech px-1 rounded bg-slate-800 text-cyan-300">
                                    +{gem.value} {gem.statLabel}
                                  </span>
                                </div>
                                <div className="text-[8.5px] text-slate-400 truncate mt-0.5">
                                  {gem.specialPerk}
                                </div>
                              </div>
                              <button
                                type="button"
                                onClick={() => onUnsocketGem?.(selectedSlotKey, sIdx)}
                                className="px-2 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white text-[9px] font-tech cursor-pointer shrink-0 transition-colors"
                                title="Tháo ngọc về Túi Phù Thạch (Miễn phí)"
                              >
                                Tháo
                              </button>
                            </div>
                          );
                        }

                        return (
                          <div
                            key={sIdx}
                            className="p-2 rounded-lg bg-cyan-950/20 border border-dashed border-cyan-500/40 text-[10px] font-tech text-cyan-300 flex items-center justify-between"
                          >
                            <div className="flex items-center gap-1.5">
                              <span className="w-2.5 h-2.5 rounded-full border border-dashed border-cyan-400 flex items-center justify-center text-[7px]">○</span>
                              <span>Lỗ Khảm #{sIdx + 1} (Trống)</span>
                            </div>
                            <span className="text-[9px] text-amber-300 italic">
                              Chọn ngọc bên dưới để khảm
                            </span>
                          </div>
                        );
                      })}
                    </div>
                  </div>

                  {/* MODULE D: TIỀN TỐ, HẬU TỐ & TÔI LỬA (AFFIXES & QUENCHING) */}
                  {(item.prefixes.length > 0 || item.suffixes.length > 0) && (
                    <div className="space-y-1 pt-1 border-t border-slate-800">
                      <div className="text-[10px] font-tech text-slate-400 uppercase tracking-wider">
                        Trận Đồ Cổ Thuật (Affix):
                      </div>
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-1 font-tech text-[10px]">
                        {item.prefixes.map((p) => (
                          <div key={p.id} className="p-1.5 rounded bg-amber-500/10 border border-amber-500/20 text-amber-200 flex items-center justify-between">
                            <span className="font-bold">[{p.name}]</span>
                            <span>{p.label}</span>
                          </div>
                        ))}
                        {item.suffixes.map((s) => (
                          <div key={s.id} className="p-1.5 rounded bg-purple-500/10 border border-purple-500/20 text-purple-200 flex items-center justify-between">
                            <span className="font-bold">[{s.name}]</span>
                            <span>{s.label}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Quenching / Elemental Seasoning */}
                  <div className="pt-2 border-t border-slate-800 space-y-1.5">
                    <div className="flex items-center justify-between text-[11px] font-tech text-amber-300">
                      <span className="flex items-center gap-1 font-bold">
                        <Flame className="w-3.5 h-3.5 text-orange-400" />
                        NGHI THỨC TÔI LỬA NGUYÊN TỐ:
                      </span>
                      {item.quench ? (
                        <span className="text-[10px] text-emerald-300 font-bold px-1.5 py-0.5 rounded bg-emerald-500/20 border border-emerald-500/40">
                          ✓ {QUENCH_OPTIONS.find((q) => q.type === item.quench)?.name.split(' ')[1] || 'ĐÃ TÔI LỬA'}
                        </span>
                      ) : (
                        <span className="text-[10px] text-slate-400 font-mono">150 LT + 1 TH</span>
                      )}
                    </div>

                    <div className="grid grid-cols-3 gap-1.5">
                      {QUENCH_OPTIONS.map((q) => {
                        const isApplied = item.quench === q.type;
                        const canAfford = linhThach >= q.costLinhThach && tinhHoa >= q.costTinhHoa;

                        return (
                          <button
                            key={q.type}
                            type="button"
                            disabled={isApplied || !canAfford}
                            onClick={() => onQuenchItem?.(item.id, q.type)}
                            className={`p-2 rounded-lg border text-center transition-all flex flex-col items-center justify-center gap-0.5 ${
                              isApplied
                                ? 'bg-emerald-950/40 border-emerald-500/60 text-emerald-300 ring-1 ring-emerald-500/30'
                                : canAfford
                                ? 'bg-slate-900/60 border-slate-700 hover:border-amber-400 cursor-pointer active:scale-95 text-slate-200'
                                : 'bg-slate-900/20 border-slate-800 text-slate-500 cursor-not-allowed opacity-60'
                            }`}
                            title={`${q.name}: ${q.bonusDesc}`}
                          >
                            <span className="text-base">{q.icon}</span>
                            <span className="text-[10px] font-tech font-bold truncate max-w-full">
                              {q.name.split(' ')[1]}
                            </span>
                            <span className="text-[9px] font-mono text-slate-400">
                              {isApplied ? 'Đang dùng' : '150 LT'}
                            </span>
                          </button>
                        );
                      })}
                    </div>
                  </div>
                </div>
              );
            })()}

            {/* 4. TÚI PHÙ THẠCH THƯỢNG CỔ (ANCIENT RUNE GEM POUCH) */}
            <div className="pt-2 border-t border-slate-800 space-y-2">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-1.5">
                <div className="flex items-center gap-1.5 text-xs font-tech">
                  <Gem className="w-3.5 h-3.5 text-cyan-400" />
                  <span className="font-bold text-slate-200">TÚI PHÙ THẠCH THƯỢNG CỔ</span>
                  <span className="text-[10px] text-amber-300 font-mono">
                    [{runePouch.length} Viên Ngọc]
                  </span>
                </div>

                {/* Filter Chips */}
                <div className="flex items-center gap-1 flex-wrap">
                  {(['all', 'lightning', 'fire', 'mountain', 'dark', 'fortune'] as const).map((elem) => {
                    const label =
                      elem === 'all'
                        ? `Tất cả (${runePouch.length})`
                        : elem === 'lightning'
                        ? `⚡ Lôi (${runePouch.filter((g) => g.type === 'lightning').length})`
                        : elem === 'fire'
                        ? `🔥 Hỏa (${runePouch.filter((g) => g.type === 'fire').length})`
                        : elem === 'mountain'
                        ? `⛰️ Sơn (${runePouch.filter((g) => g.type === 'mountain').length})`
                        : elem === 'dark'
                        ? `❄️ Âm (${runePouch.filter((g) => g.type === 'dark').length})`
                        : `🌟 Vận (${runePouch.filter((g) => g.type === 'fortune').length})`;

                    const isActive = gemPouchFilter === elem;

                    return (
                      <button
                        key={elem}
                        type="button"
                        onClick={() => setGemPouchFilter(elem)}
                        className={`px-1.5 py-0.5 rounded text-[9px] font-tech cursor-pointer transition-colors ${
                          isActive
                            ? 'bg-amber-400 text-slate-950 font-bold'
                            : 'bg-slate-800 text-slate-400 hover:text-slate-200'
                        }`}
                      >
                        {label}
                      </button>
                    );
                  })}
                </div>
              </div>

              {/* Gem Cards Grid */}
              {runePouch.length === 0 ? (
                <div className="p-4 rounded-xl bg-[#070912] border border-slate-800/80 text-center space-y-1">
                  <div className="text-xs font-tech text-slate-300 font-bold">
                    Túi Phù Thạch Hiện Đang Trống
                  </div>
                  <p className="text-[10px] text-slate-500 max-w-sm mx-auto">
                    Phù Thạch là kỳ trân dị bảo cực hiếm trong vũ trụ (rơi với tỉ lệ cực thấp khi nhát gõ Hoàng Kim hoặc phá vỡ Khiên Vòm Trời). Hãy kiên trì rèn đúc!
                  </p>
                </div>
              ) : (
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 max-h-72 overflow-y-auto p-1.5 rounded-xl bg-[#070912] border border-slate-800/90">
                  {runePouch
                    .filter((gem) => (gemPouchFilter === 'all' ? true : gem.type === gemPouchFilter))
                    .map((gem) => {
                      const currentSelected = equippedItems[selectedSlotKey];
                      const unlockedCount =
                        currentSelected?.unlockedSockets ?? (currentSelected ? getUnlockedSockets(currentSelected.rarity) : 0);
                      const sockets = currentSelected?.sockets || [];
                      const firstEmptyIndex = sockets.findIndex((s, idx) => idx < unlockedCount && s === null);
                      const canSocket = firstEmptyIndex !== -1 && currentSelected !== null;

                      return (
                        <div
                          key={gem.id}
                          className="p-2 rounded-lg bg-[#0C101D] border border-slate-800 flex flex-col justify-between gap-1.5 shadow"
                          style={{ borderTopColor: gem.color, borderTopWidth: '2px' }}
                        >
                          <div>
                            <div className="flex items-center justify-between gap-1">
                              <span className="font-bold text-[11px] text-slate-200 truncate">
                                {gem.name}
                              </span>
                              <span className="text-[8px] font-tech px-1 rounded uppercase font-bold" style={{ backgroundColor: `${gem.color}20`, color: gem.color }}>
                                {gem.tier}
                              </span>
                            </div>
                            <div className="text-[9.5px] font-tech text-cyan-300 font-mono mt-0.5">
                              +{gem.value} {gem.statLabel}
                            </div>
                            <div className="text-[8.5px] text-slate-400 mt-0.5 line-clamp-2">
                              {gem.specialPerk}
                            </div>
                          </div>

                          <div className="pt-1 border-t border-slate-800/80 flex items-center justify-between">
                            <span className="text-[8.5px] font-tech uppercase" style={{ color: gem.color }}>
                              Hệ {gem.type}
                            </span>
                            {canSocket ? (
                              <button
                                type="button"
                                onClick={() => onSocketGem?.(selectedSlotKey, firstEmptyIndex, gem.id)}
                                className="px-2 py-0.5 rounded bg-cyan-600 hover:bg-cyan-500 text-white font-tech font-bold text-[9px] cursor-pointer shadow transition-all active:scale-95"
                              >
                                Khảm Vào {SLOT_INFO[selectedSlotKey].name}
                              </button>
                            ) : (
                              <span className="text-[8.5px] font-tech text-slate-500 italic">
                                {currentSelected ? 'Hết lỗ trống' : 'Chưa chọn vũ khí'}
                              </span>
                            )}
                          </div>
                        </div>
                      );
                    })}
                </div>
              )}
            </div>
          </div>
        )}

        {/* ================================================================= */}
        {/* TAB 2: FORGE UPGRADES */}
        {/* ================================================================= */}
        {activeTab === 'upgrades' && (
          <div className="space-y-2.5">
            {upgrades.map((up) => {
              const cost = getUpgradeCost(up);
              const eqCheck = checkForgeEquilibrium(upgrades, up.id);
              const isEqLocked = !eqCheck.allowed;
              const canAfford = linhThach >= cost && up.level < up.maxLevel && !isEqLocked;

              let currentBonusText = '';
              if (up.id === 'celestial_hammer_core') {
                const cur = calculateForgeDamage(up.level);
                const nxt = calculateForgeDamage(up.level + 1);
                currentBonusText = `Sát thương: ${cur} DMG (Cấp tới: ${nxt} DMG)`;
              } else if (up.id === 'thunder_quench_oil') {
                currentBonusText = `Hiện tại: +${up.level} DMG thực tế`;
              } else if (up.id === 'bellows_inferno') {
                currentBonusText = `Hiện tại: +${up.level * 4}% tốc độ Hỏa Hầu`;
              } else if (up.id === 'cosmic_resonance_anvil') {
                currentBonusText = `Hiện tại: +${Math.floor(up.level / 2)} Linh Thạch & +${Math.floor(
                  up.level / 4
                )}% Phá Giáp`;
              }

              return (
                <div
                  key={up.id}
                  className="p-3 rounded-xl bg-[#080A10] border border-slate-800 hover:border-slate-700 transition-colors"
                >
                  <div className="flex items-start justify-between gap-2 mb-1.5">
                    <div>
                      <h4 className="font-semibold text-xs text-amber-300 font-tech">
                        {up.name}
                      </h4>
                      <p className="text-[11px] text-slate-400">{up.subtitle}</p>
                    </div>
                    <span className="text-[11px] font-tech text-cyan-400 font-bold whitespace-nowrap">
                      Cấp {up.level}/{up.maxLevel}
                    </span>
                  </div>

                  <div className="text-[10px] text-slate-400 mb-2 font-mono">
                    {currentBonusText}
                  </div>

                  {isEqLocked && (
                    <div className="text-[10px] text-red-400 font-tech mb-2 px-2 py-1 rounded bg-red-950/30 border border-red-500/30">
                      🔒 Lệch Cấp Lò Rèn (hơn 15 cấp so với Cấp {eqCheck.minLevel}). Hãy nâng cấp các hạng mục khác!
                    </div>
                  )}

                  <div className="flex items-center justify-between pt-2 border-t border-slate-800/80">
                    <div className="text-xs font-tech text-slate-300">
                      Chi phí:{' '}
                      <span className="text-cyan-300 font-bold">
                        {cost.toLocaleString('en-US')} LT
                      </span>
                    </div>

                    <button
                      type="button"
                      disabled={!canAfford}
                      onClick={() => onBuyUpgrade(up.id)}
                      className={`px-3 py-1.5 rounded-lg text-xs font-tech font-bold transition-all shadow-sm ${
                        canAfford
                          ? 'bg-amber-400 hover:bg-amber-300 text-slate-950 cursor-pointer shadow-amber-500/20 active:scale-95'
                          : 'bg-slate-800 text-slate-500 cursor-not-allowed'
                      }`}
                    >
                      {up.level >= up.maxLevel
                        ? 'ĐẠT TỐI ĐA'
                        : `Rèn Cấp · ${cost.toLocaleString('en-US')} LT`}
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        )}

        {/* ================================================================= */}
        {/* TAB 3: KỸ PHÁP TỨ THẾ & ĐẲNG CẤP THỢ RÈN */}
        {/* ================================================================= */}
        {activeTab === 'spirit' && (
          <div className="space-y-3">
            {/* 1. ĐẲNG CẤP THỢ RÈN (FORGER RANK) CARD */}
            {(() => {
              const currentRankIndex = FORGER_RANKS.findIndex((r) => r.id === forgerRank.id);
              const nextRank = FORGER_RANKS[currentRankIndex + 1] || null;
              const progressPct = nextRank
                ? Math.min(100, Math.max(0, (playerTotalDamage / nextRank.damageRequired) * 100))
                : 100;

              return (
                <div className="p-3 rounded-xl bg-gradient-to-br from-[#0c0f18] to-[#141a29] border border-amber-500/30 shadow-lg">
                  <div className="flex items-center justify-between gap-2 mb-1.5">
                    <div className="flex items-center gap-2">
                      <span className="text-xl">{forgerRank.badge}</span>
                      <div>
                        <div className="flex items-center gap-1.5">
                          <h4 className="font-tech font-bold text-sm text-amber-300">
                            {forgerRank.title}
                          </h4>
                          <span className="text-[10px] font-tech px-1.5 py-0.5 rounded bg-amber-400/20 text-amber-300 font-bold border border-amber-400/30">
                            BẬC {forgerRank.tier}/4
                          </span>
                        </div>
                        <p className="text-[10px] text-slate-400 font-tech">
                          Tổng cống hiến: <b className="text-slate-200">{formatInteger(playerTotalDamage)} DMG</b>
                        </p>
                      </div>
                    </div>

                    <div className="text-right">
                      <div className="text-[10px] font-tech text-slate-400">Tinh Hoa Thần Hồn</div>
                      <div className="text-sm font-bold text-amber-400 font-tech">
                        {tinhHoa} TH
                      </div>
                    </div>
                  </div>

                  {/* Progress bar to next rank */}
                  {nextRank ? (
                    <div className="space-y-1 mt-2 pt-2 border-t border-slate-800">
                      <div className="flex items-center justify-between text-[10px] font-tech">
                        <span className="text-slate-400">
                          Thăng bậc: <b className="text-cyan-300">{nextRank.title}</b>
                        </span>
                        <span className="text-amber-300 font-bold">
                          {formatInteger(playerTotalDamage)} / {formatInteger(nextRank.damageRequired)} DMG ({progressPct.toFixed(1)}%)
                        </span>
                      </div>
                      <div className="h-1.5 w-full bg-slate-900 rounded-full overflow-hidden border border-slate-800">
                        <div
                          className="h-full bg-gradient-to-r from-amber-500 to-amber-300 transition-all duration-300 shadow-sm shadow-amber-400/50"
                          style={{ width: `${progressPct}%` }}
                        />
                      </div>
                    </div>
                  ) : (
                    <div className="mt-2 pt-1.5 border-t border-slate-800 text-[10px] font-tech text-emerald-400 font-bold text-center">
                      👑 ĐÃ ĐẠT CẢNH GIỚI CAO NHẤT: TRẢM THIÊN THẦN TƯỢNG
                    </div>
                  )}

                  {/* Passive buffs banner */}
                  <div className="mt-2 px-2 py-1.5 rounded-lg bg-black/40 border border-slate-800/80 text-[11px] text-amber-200/90 font-tech">
                    ⚡ {forgerRank.bonusDesc}
                  </div>
                </div>
              );
            })()}

            {/* 2A. BẢN SẮC CĂN CƠ · HỆ PHÁI ĐÃ CHỌN CARD */}
            {playerClass && (
              <div
                className="p-3 rounded-xl border flex flex-col gap-2.5 transition-all shadow-lg"
                style={{
                  backgroundColor: `${playerClass.color}15`,
                  borderColor: `${playerClass.color}50`,
                }}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="text-xl">{playerClass.icon}</span>
                    <div>
                      <h4 className="text-xs font-bold font-tech text-amber-300">
                        {playerClass.name} · {playerClass.sectTitle}
                      </h4>
                      <div className="text-[10px] text-slate-400">
                        {playerClass.role} ({playerClass.guildTitle})
                      </div>
                    </div>
                  </div>
                  <span className="px-2 py-0.5 rounded text-[10px] font-tech font-bold bg-slate-900/90 border border-amber-500/30 text-amber-300/90 select-none">
                    Độc Nhất Căn Cơ
                  </span>
                </div>

                {/* 4 Class Skills Q W E R Mini Preview */}
                <div className="grid grid-cols-4 gap-1 font-tech">
                  {(['Q', 'W', 'E', 'R'] as const).map((slotKey) => {
                    const sk = playerClass.skills[slotKey];
                    return (
                      <div
                        key={slotKey}
                        className="p-1.5 rounded-lg bg-slate-950/80 border border-slate-800 flex flex-col items-center text-center gap-0.5"
                      >
                        <span
                          className="w-4 h-4 rounded text-[9px] font-bold flex items-center justify-center"
                          style={{ backgroundColor: playerClass.color, color: '#05070F' }}
                        >
                          {slotKey}
                        </span>
                        <span className="text-[9px] font-semibold text-slate-200 truncate w-full">
                          {sk.name}
                        </span>
                        <span className="text-[8px] text-cyan-400">
                          {slotKey === 'Q' ? 'Cấp 1' : slotKey === 'W' ? 'Cấp 40' : slotKey === 'E' ? 'Cấp 100' : 'Cấp 200'}
                        </span>
                      </div>
                    );
                  })}
                </div>

                {/* 2 Sub-Classes Preview */}
                <div className="text-[10px] font-tech text-slate-400 pt-1.5 border-t border-slate-800/80 flex items-center justify-between">
                  <span className="text-purple-300">① {playerClass.subClasses.a.name}</span>
                  <span>·</span>
                  <span className="text-emerald-300">② {playerClass.subClasses.b.name}</span>
                  <span className="text-[9px] text-slate-500">(Mở Cấp 120)</span>
                </div>
              </div>
            )}

            {/* 2. STANCE SELECTOR TABS (Q, W, E, R) */}
            <div>
              <div className="text-xs font-tech text-slate-400 font-semibold px-1 mb-1.5 flex items-center justify-between">
                <span>CÂY KỸ PHÁP TỨ THẾ:</span>
                <span className="text-[10px] text-slate-500 font-mono">Dùng Tinh Hoa để lĩnh hội</span>
              </div>

              <div className="grid grid-cols-4 gap-1 p-1 bg-[#080A10] border border-slate-800 rounded-xl">
                {(['Q', 'W', 'E', 'R'] as StanceKey[]).map((stKey) => {
                  const st = HAMMER_STANCES[stKey];
                  const isSelected = selectedStanceTree === stKey;
                  const unlockedCount = stanceSkills.filter((s) => s.stance === stKey && s.unlocked).length;

                  const borderClasses = {
                    Q: 'border-cyan-400 bg-cyan-950/50 text-cyan-300 shadow-cyan-500/20',
                    W: 'border-orange-500 bg-orange-950/50 text-orange-300 shadow-orange-500/20',
                    E: 'border-purple-500 bg-purple-950/50 text-purple-300 shadow-purple-500/20',
                    R: 'border-emerald-500 bg-emerald-950/50 text-emerald-300 shadow-emerald-500/20',
                  }[stKey];

                  return (
                    <button
                      key={stKey}
                      type="button"
                      onClick={() => {
                        setSelectedStanceTree(stKey);
                        const firstOfStance = stanceSkills.find((s) => s.stance === stKey);
                        if (firstOfStance) setSelectedSkillNodeId(firstOfStance.id);
                      }}
                      className={`p-2 rounded-lg border text-center transition-all cursor-pointer flex flex-col items-center justify-center gap-0.5 ${
                        isSelected
                          ? `border-2 ${borderClasses} shadow-md`
                          : 'border-slate-800 bg-slate-900/30 text-slate-400 hover:text-slate-200'
                      }`}
                    >
                      <span className="font-tech font-bold text-xs">[{stKey}]</span>
                      <span className="text-[10px] font-tech truncate max-w-full">{st.name}</span>
                      <span className="text-[9px] font-tech text-slate-400">{unlockedCount}/5</span>
                    </button>
                  );
                })}
              </div>
            </div>

            {/* 3. 5-TIER SKILL PROGRESSION NODES */}
            <div className="space-y-1.5">
              {stanceSkills
                .filter((s) => s.stance === selectedStanceTree)
                .map((node) => {
                  const isSelected = selectedSkillNodeId === node.id;
                  const canUnlock = canUnlockStanceSkill(node.id, stanceSkills, tinhHoa, forgerRank.tier);
                  const isMasterPerk = node.tier === 5;

                  return (
                    <button
                      key={node.id}
                      type="button"
                      onClick={() => setSelectedSkillNodeId(node.id)}
                      className={`w-full p-2.5 rounded-xl border text-left transition-all cursor-pointer flex items-center justify-between gap-2.5 ${
                        node.unlocked
                          ? 'bg-emerald-950/20 border-emerald-500/40 hover:border-emerald-400'
                          : canUnlock
                          ? 'bg-amber-950/25 border-amber-400/50 hover:border-amber-300 ring-1 ring-amber-400/30'
                          : 'bg-slate-900/30 border-slate-800 opacity-60'
                      } ${isSelected ? 'ring-2 ring-cyan-400 shadow-lg shadow-cyan-500/20' : ''} ${
                        isMasterPerk ? 'border-amber-400/60 bg-gradient-to-r from-amber-950/30 via-purple-950/30 to-slate-900/40' : ''
                      }`}
                    >
                      <div className="flex items-center gap-2.5 min-w-0">
                        <div
                          className={`w-7 h-7 rounded-lg flex items-center justify-center shrink-0 font-tech font-bold text-xs ${
                            node.unlocked
                              ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40'
                              : isMasterPerk
                              ? 'bg-amber-400/20 text-amber-300 border border-amber-400'
                              : 'bg-slate-800 text-slate-400 border border-slate-700'
                          }`}
                        >
                          {isMasterPerk ? '★' : `T${node.tier}`}
                        </div>

                        <div className="min-w-0">
                          <div className="flex items-center gap-1.5">
                            <span className="font-tech font-semibold text-xs text-slate-100 truncate">
                              {node.name}
                            </span>
                            {isMasterPerk && (
                              <span className="text-[9px] font-tech font-bold px-1 rounded bg-amber-400 text-slate-950 shrink-0">
                                MASTER
                              </span>
                            )}
                          </div>
                          <p className="text-[10px] text-slate-400 truncate max-w-[240px]">
                            {node.description}
                          </p>
                        </div>
                      </div>

                      <div className="flex items-center gap-2 shrink-0">
                        <span className="text-xs font-tech font-bold text-amber-300 whitespace-nowrap">
                          {node.costTinhHoa} TH
                        </span>
                        {node.unlocked ? (
                          <Check className="w-4 h-4 text-emerald-400 shrink-0" />
                        ) : canUnlock ? (
                          <Sparkles className="w-4 h-4 text-amber-400 shrink-0 animate-pulse" />
                        ) : (
                          <Lock className="w-4 h-4 text-slate-500 shrink-0" />
                        )}
                      </div>
                    </button>
                  );
                })}
            </div>

            {/* 4. SELECTED SKILL INSPECTOR & UNLOCK ACTION CARD */}
            {(() => {
              const selectedSkill =
                stanceSkills.find((s) => s.id === selectedSkillNodeId) ||
                stanceSkills.find((s) => s.stance === selectedStanceTree);
              if (!selectedSkill) return null;

              const canUnlock = canUnlockStanceSkill(
                selectedSkill.id,
                stanceSkills,
                tinhHoa,
                forgerRank.tier
              );
              const parentNode = selectedSkill.requires
                ? stanceSkills.find((s) => s.id === selectedSkill.requires)
                : null;
              const needsParent = parentNode && !parentNode.unlocked;
              const needsRank = selectedSkill.tier >= 4 && forgerRank.tier < 3;
              const notEnoughTH = tinhHoa < selectedSkill.costTinhHoa;

              return (
                <div className="p-3.5 rounded-xl bg-[#080A10] border border-cyan-500/40 space-y-2.5 shadow-xl">
                  <div className="flex items-start justify-between gap-2">
                    <div>
                      <div className="flex items-center gap-1.5">
                        <span className="text-[10px] font-tech px-1.5 py-0.5 rounded bg-slate-800 text-slate-300 font-bold">
                          TẦNG {selectedSkill.tier} · [{selectedSkill.stance}] {HAMMER_STANCES[selectedSkill.stance].name}
                        </span>
                        {selectedSkill.tier === 5 && (
                          <span className="text-[10px] font-tech px-1.5 py-0.5 rounded bg-amber-500/20 border border-amber-400/50 text-amber-300 font-bold">
                            MASTER PERK
                          </span>
                        )}
                      </div>
                      <h4 className="font-tech font-bold text-sm text-amber-300 mt-1">
                        {selectedSkill.name}
                      </h4>
                    </div>

                    <span
                      className={`text-[10px] font-tech px-2 py-0.5 rounded font-bold shrink-0 ${
                        selectedSkill.unlocked
                          ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40'
                          : 'bg-slate-800 text-slate-400'
                      }`}
                    >
                      {selectedSkill.unlocked ? '✓ ĐÃ LĨNH HỘI' : 'CHƯA MỞ'}
                    </span>
                  </div>

                  <p className="text-xs text-slate-300 leading-relaxed font-sans bg-black/30 p-2.5 rounded-lg border border-slate-800/80">
                    {selectedSkill.description}
                  </p>

                  {/* Requirements / Warnings */}
                  {!selectedSkill.unlocked && (
                    <div className="space-y-1 text-[11px] font-tech">
                      {needsParent && (
                        <div className="text-rose-400 flex items-center gap-1">
                          <span>⚠️ Yêu cầu hoàn thành trước:</span>
                          <b className="text-slate-200">{parentNode?.name}</b>
                        </div>
                      )}
                      {needsRank && (
                        <div className="text-amber-400 flex items-center gap-1">
                          <span>⚠️ Yêu cầu Đẳng cấp:</span>
                          <b className="text-amber-300">Cổ Đúc Sư (Bậc 3) trở lên</b>
                        </div>
                      )}
                      {notEnoughTH && (
                        <div className="text-slate-400">
                          Chi phí: <b className="text-amber-300">{selectedSkill.costTinhHoa} TH</b> (Bạn có {tinhHoa} TH)
                        </div>
                      )}
                    </div>
                  )}

                  {/* Action Button */}
                  <div className="pt-2 border-t border-slate-800">
                    {selectedSkill.unlocked ? (
                      <div className="w-full py-2 rounded-xl bg-emerald-950/30 border border-emerald-500/30 text-emerald-300 font-tech font-bold text-xs text-center">
                        ✓ KỸ PHÁP ĐÃ LĨNH HỘI & ĐANG KÍCH HOẠT VĨNH VIỄN
                      </div>
                    ) : (
                      <button
                        type="button"
                        disabled={!canUnlock}
                        onClick={() => onUnlockStanceSkill(selectedSkill.id)}
                        className={`w-full py-2.5 px-3 rounded-xl font-tech font-bold text-xs tracking-wider transition-all flex items-center justify-center gap-2 ${
                          canUnlock
                            ? 'bg-gradient-to-r from-amber-400 to-amber-300 hover:from-amber-300 hover:to-amber-200 text-slate-950 cursor-pointer shadow-lg shadow-amber-500/20 active:scale-95'
                            : 'bg-slate-800 text-slate-500 cursor-not-allowed border border-slate-700/50'
                        }`}
                      >
                        <Sparkles className="w-4 h-4" />
                        <span>KHAI MỞ KỸ PHÁP · {selectedSkill.costTinhHoa} TINH HOA THẦN HỒN</span>
                      </button>
                    )}
                  </div>
                </div>
              );
            })()}
          </div>
        )}

        {/* ================================================================= */}
        {/* TAB 4: LEADERBOARD */}
        {/* ================================================================= */}
        {activeTab === 'leaderboard' && (
          <div className="space-y-2">
            <div className="text-[11px] font-tech text-slate-400 px-1 mb-1">
              Bảng Vàng Vạn Dân · Cửu Trọng Thiên (Cập nhật thời gian thực):
            </div>

            {leaderboard.map((entry, index) => {
              const isTop3 = index < 3;
              const medalColors = ['text-amber-400', 'text-slate-300', 'text-amber-600'];
              const dmgValue =
                typeof entry.damage === 'number'
                  ? entry.damage
                  : (entry.damageBillions || 0) * 1_000_000;

              return (
                <div
                  key={entry.id}
                  className={`flex items-center justify-between p-2.5 rounded-xl border transition-all ${
                    entry.isPlayer
                      ? 'bg-amber-500/10 border-amber-400/50 ring-1 ring-amber-400/30'
                      : 'bg-[#080A10] border-slate-800'
                  }`}
                >
                  <div className="flex items-center gap-2.5">
                    <span
                      className={`font-tech text-xs font-bold w-5 text-center ${
                        isTop3 ? medalColors[index] : 'text-slate-500'
                      }`}
                    >
                      #{index + 1}
                    </span>

                    <div>
                      <div className="flex items-center gap-1.5">
                        <span
                          className={`font-semibold text-xs ${
                            entry.isPlayer ? 'text-amber-300' : 'text-slate-200'
                          }`}
                        >
                          {entry.name}
                        </span>
                        {entry.isPlayer && (
                          <span className="text-[9px] bg-amber-400 text-slate-950 font-bold px-1.5 py-0.2 rounded font-tech">
                            BẠN
                          </span>
                        )}
                      </div>
                      <span className="text-[10px] text-slate-400 font-tech">
                        {entry.sect}
                      </span>
                    </div>
                  </div>

                  <div className="text-right">
                    <div className="font-tech text-xs font-bold text-cyan-300">
                      {dmgValue.toLocaleString('en-US')} DMG
                    </div>
                    <span className="text-[9px] text-slate-400 font-tech">Tổng Công Lực</span>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );

  return (
    <aside
      aria-label="Vũ Khí, Nâng Cấp, Cây Thần Hồn và Bảng Vàng"
      className="h-full flex flex-col p-3 select-none"
    >
      {renderPanelContent()}
    </aside>
  );
};
export default RightProgressionPanel;
