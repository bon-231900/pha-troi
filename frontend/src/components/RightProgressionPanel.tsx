import React, { useState } from 'react';
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
} from '../game/rules';
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
  spiritNodes: SpiritNode[];
  linhThach: number;
  tinhHoa: number;
  tier2Unlocked?: boolean;
  leaderboard: LeaderboardEntry[];
  mobileDrawerOpen: boolean;
  onCloseMobileDrawer: () => void;
  onBuyUpgrade: (upgradeId: string) => void;
  onUnlockSpiritNode: (nodeId: string) => void;
  onEquipItem: (item: EquipmentItem) => void;
  onUnequipItem: (slotKey: EquipmentSlotKey) => void;
  onSalvageItem: (item: EquipmentItem) => void;
  onQuickSalvage: (rarities: ItemRarity[]) => void;
}

export const RightProgressionPanel: React.FC<RightProgressionPanelProps> = ({
  equippedItems,
  inventory,
  upgrades,
  spiritNodes,
  linhThach,
  tinhHoa,
  tier2Unlocked = false,
  leaderboard,
  mobileDrawerOpen,
  onCloseMobileDrawer,
  onBuyUpgrade,
  onUnlockSpiritNode,
  onEquipItem,
  onUnequipItem,
  onSalvageItem,
  onQuickSalvage,
}) => {
  const [activeTab, setActiveTab] = useState<'arsenal' | 'upgrades' | 'spirit' | 'leaderboard'>('arsenal');
  const [selectedItem, setSelectedItem] = useState<EquipmentItem | null>(() => {
    return equippedItems.hammer || inventory[0] || null;
  });
  const [selectedNodeId, setSelectedNodeId] = useState<string>('node_thunder_eye');

  const selectedNode =
    spiritNodes.find((n) => n.id === selectedNodeId) || spiritNodes[0];
  const spiritTotalMult = calculateSpiritMultiplier(spiritNodes);

  const arsenalBonuses = calculateArsenalBonuses(equippedItems);

  // Helper: check if item is currently equipped
  const isEquipped = (item: EquipmentItem | null): boolean => {
    if (!item) return false;
    return equippedItems[item.slotKey]?.id === item.id;
  };

  // Quick salvage counts
  const commonInBag = inventory.filter((it) => it.rarity === 'common').length;
  const rareInBag = inventory.filter((it) => it.rarity === 'rare').length;

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
          title="Chòm Sao Thần Hồn"
        >
          <Sparkles className="w-3.5 h-3.5" />
          <span className="truncate">Thần Hồn</span>
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
      </div>

      {/* Tab Body */}
      <div className="flex-1 overflow-y-auto pr-0.5 space-y-2.5">
        {/* ================================================================= */}
        {/* TAB 1: ARSENAL & BACKPACK (ARPG LOOT & AFFIX SYSTEM) */}
        {/* ================================================================= */}
        {activeTab === 'arsenal' && (
          <div className="flex flex-col gap-2.5">
            {/* Top Equipped Stats Card */}
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
            </div>

            {/* 6 Equipped Slots Grid */}
            <div>
              <div className="text-[11px] font-tech text-slate-300 mb-1.5 flex items-center justify-between">
                <span className="font-bold text-amber-300">6 VỊ TRÍ KHÍ GIỚI ĐANG MANG</span>
                <span className="text-[10px] text-slate-400">Click để kiểm tra & tháo đồ</span>
              </div>

              <div className="grid grid-cols-2 gap-2">
                {(['hammer', 'anvil', 'bellows', 'gauntlets', 'apron', 'relic'] as EquipmentSlotKey[]).map(
                  (slotKey) => {
                    const item = equippedItems[slotKey];
                    const slotMeta = SLOT_INFO[slotKey];
                    const isSelected = selectedItem?.id === item?.id;
                    const rMeta = item ? getItemRarityMeta(item.rarity) : null;

                    return (
                      <button
                        key={slotKey}
                        type="button"
                        onClick={() => {
                          if (item) setSelectedItem(item);
                        }}
                        className={`p-2 rounded-xl border text-left transition-all cursor-pointer flex flex-col justify-between min-h-[82px] ${
                          isSelected
                            ? 'bg-slate-900/90 border-amber-400 ring-1 ring-amber-400/50 shadow-md'
                            : item
                            ? 'bg-[#080A10] border-slate-800 hover:border-slate-700'
                            : 'bg-[#06080F]/60 border-dashed border-slate-800 opacity-60'
                        }`}
                      >
                        <div>
                          <div className="flex items-center justify-between mb-0.5">
                            <span className="text-[9px] font-tech uppercase text-slate-400">
                              {slotMeta.name}
                            </span>
                            {item && (
                              <span
                                className={`text-[8px] px-1 rounded font-tech ${
                                  rMeta?.badgeBg
                                }`}
                              >
                                {rMeta?.label}
                              </span>
                            )}
                          </div>

                          <div
                            className={`font-semibold text-[11px] truncate ${
                              rMeta ? rMeta.textColor : 'text-slate-500'
                            }`}
                          >
                            {item ? item.name : 'Chưa Trang Bị'}
                          </div>
                        </div>

                        {item ? (
                          <div className="mt-1 pt-1 border-t border-slate-800/80 flex items-center justify-between text-[9px] font-tech">
                            <span className="text-cyan-300">
                              +{item.baseStatValue} {item.baseStatUnit}
                            </span>
                            <span className="text-slate-400">
                              {item.prefixes.length + item.suffixes.length} Dòng Affix
                            </span>
                          </div>
                        ) : (
                          <div className="text-[9px] text-slate-500 italic">Đập đe để nhặt đồ</div>
                        )}
                      </button>
                    );
                  }
                )}
              </div>
            </div>

            {/* Backpack / Inventory Section with Quick Salvage */}
            <div className="pt-2 border-t border-slate-800">
              <div className="flex items-center justify-between mb-1.5">
                <div className="flex items-center gap-1.5 text-xs font-tech">
                  <PackageOpen className="w-3.5 h-3.5 text-cyan-400" />
                  <span className="font-bold text-slate-200">TÚI ĐỒ (RƯƠNG VŨ KHÍ)</span>
                  <span className="text-[10px] text-slate-400">
                    ({inventory.length}/{MAX_INVENTORY_SLOTS})
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
                {Array.from({ length: MAX_INVENTORY_SLOTS }).map((_, idx) => {
                  const bagItem = inventory[idx] || null;
                  const isSelected = selectedItem?.id === bagItem?.id;
                  const rMeta = bagItem ? getItemRarityMeta(bagItem.rarity) : null;

                  return (
                    <button
                      key={bagItem ? bagItem.id : `empty_${idx}`}
                      type="button"
                      disabled={!bagItem}
                      onClick={() => {
                        if (bagItem) setSelectedItem(bagItem);
                      }}
                      className={`relative aspect-square rounded-lg border flex flex-col items-center justify-center transition-all ${
                        bagItem
                          ? `cursor-pointer ${
                              isSelected
                                ? 'border-amber-400 ring-2 ring-amber-400/40 bg-slate-800 shadow-md scale-105'
                                : `${rMeta?.borderColor} ${rMeta?.bgColor} hover:brightness-125`
                            }`
                          : 'border-dashed border-slate-800/60 bg-slate-950/40 cursor-default'
                      }`}
                      title={bagItem ? `${bagItem.name} (${rMeta?.label})` : 'Ô trống'}
                    >
                      {bagItem ? (
                        <>
                          <div className={`text-[10px] font-tech font-bold ${rMeta?.textColor}`}>
                            {bagItem.slotName.substring(0, 2)}
                          </div>
                          <div className="text-[8px] font-tech text-slate-400">
                            +{bagItem.baseStatValue}
                          </div>
                          {bagItem.rarity !== 'common' && (
                            <span
                              className={`absolute top-0.5 right-0.5 w-1.5 h-1.5 rounded-full ${
                                bagItem.rarity === 'mythic'
                                  ? 'bg-orange-400 animate-ping'
                                  : bagItem.rarity === 'legendary'
                                  ? 'bg-amber-400'
                                  : bagItem.rarity === 'epic'
                                  ? 'bg-purple-400'
                                  : 'bg-cyan-400'
                              }`}
                            />
                          )}
                        </>
                      ) : (
                        <span className="text-[10px] text-slate-700">·</span>
                      )}
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Selected Item Inspector & Comparison Card */}
            {selectedItem && (
              <div className="p-3.5 rounded-xl bg-[#080A10] border border-slate-800 space-y-2.5">
                {/* Header */}
                <div className="flex items-start justify-between gap-2">
                  <div>
                    <div className="flex items-center gap-1.5">
                      <span className="text-[10px] font-tech text-cyan-400 uppercase">
                        [{selectedItem.slotName}]
                      </span>
                      <span
                        className={`text-[9px] px-1.5 py-0.2 rounded border font-tech ${
                          getItemRarityMeta(selectedItem.rarity).badgeBg
                        }`}
                      >
                        {getItemRarityMeta(selectedItem.rarity).label}
                      </span>
                      {isEquipped(selectedItem) && (
                        <span className="text-[9px] px-1.5 py-0.2 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 font-tech">
                          ĐANG TRANG BỊ
                        </span>
                      )}
                    </div>
                    <h4
                      className={`font-semibold text-sm ${
                        getItemRarityMeta(selectedItem.rarity).textColor
                      }`}
                    >
                      {selectedItem.name}
                    </h4>
                  </div>

                  <span className="text-xs font-tech font-bold text-slate-400 whitespace-nowrap">
                    Lv.{selectedItem.itemLevel}
                  </span>
                </div>

                {/* Lore quote */}
                <p className="text-[11px] text-slate-400 italic leading-relaxed border-l-2 border-slate-700 pl-2">
                  "{selectedItem.loreDescription}"
                </p>

                {/* Base Stat */}
                <div className="p-2 rounded-lg bg-[#111625] border border-slate-800 text-xs font-tech flex items-center justify-between">
                  <span className="text-slate-400">{selectedItem.baseStatLabel}:</span>
                  <span className="text-cyan-300 font-bold">
                    +{selectedItem.baseStatValue} {selectedItem.baseStatUnit}
                  </span>
                </div>

                {/* Prefixes (Tiền Tố) */}
                {selectedItem.prefixes.length > 0 && (
                  <div className="space-y-1">
                    <div className="text-[10px] font-tech text-amber-300 uppercase tracking-wider">
                      ⚡ Tiền Tố (Prefix):
                    </div>
                    {selectedItem.prefixes.map((pref) => (
                      <div
                        key={pref.id}
                        className="px-2 py-1 rounded-lg bg-amber-500/10 border border-amber-500/20 text-[11px] font-tech text-amber-200 flex items-center justify-between"
                      >
                        <span className="font-bold">[{pref.name}]</span>
                        <span>{pref.label}</span>
                      </div>
                    ))}
                  </div>
                )}

                {/* Suffixes (Hậu Tố) */}
                {selectedItem.suffixes.length > 0 && (
                  <div className="space-y-1">
                    <div className="text-[10px] font-tech text-purple-300 uppercase tracking-wider">
                      🔮 Hậu Tố (Suffix / Affix):
                    </div>
                    {selectedItem.suffixes.map((suf) => (
                      <div
                        key={suf.id}
                        className="px-2 py-1 rounded-lg bg-purple-500/10 border border-purple-500/20 text-[11px] font-tech text-purple-200 flex items-center justify-between"
                      >
                        <span className="font-bold">[{suf.name}]</span>
                        <span>{suf.label}</span>
                      </div>
                    ))}
                  </div>
                )}

                {/* Comparison with currently equipped slot (if inspecting a bag item) */}
                {!isEquipped(selectedItem) && (() => {
                  const currentEq = equippedItems[selectedItem.slotKey];
                  const diff = currentEq
                    ? selectedItem.baseStatValue - currentEq.baseStatValue
                    : selectedItem.baseStatValue;

                  return (
                    <div className="p-2 rounded-lg bg-[#0E1322] border border-slate-800 text-[11px] font-tech flex items-center justify-between">
                      <div className="flex items-center gap-1.5 text-slate-400">
                        <ArrowRightLeft className="w-3.5 h-3.5 text-cyan-400" />
                        <span>So với đồ đang mặc ({currentEq ? currentEq.name : 'Trống'}):</span>
                      </div>
                      <span
                        className={`font-bold ${
                          diff > 0
                            ? 'text-emerald-400'
                            : diff < 0
                            ? 'text-red-400'
                            : 'text-slate-400'
                        }`}
                      >
                        {diff > 0 ? `+${diff}` : `${diff}`} {selectedItem.baseStatUnit}
                      </span>
                    </div>
                  );
                })()}

                {/* Action Buttons: Equip or Salvage */}
                <div className="pt-2 border-t border-slate-800 flex items-center gap-2">
                  {!isEquipped(selectedItem) ? (
                    <>
                      <button
                        type="button"
                        onClick={() => onEquipItem(selectedItem)}
                        className="flex-1 py-2 px-3 rounded-xl bg-amber-400 hover:bg-amber-300 text-slate-950 font-tech font-bold text-xs tracking-wider cursor-pointer shadow-md shadow-amber-500/20 active:scale-95 transition-all text-center"
                      >
                        TRANG BỊ NGAY
                      </button>

                      {(() => {
                        const salvage = getSalvageYield(selectedItem);
                        return (
                          <button
                            type="button"
                            onClick={() => onSalvageItem(selectedItem)}
                            className="py-2 px-3 rounded-xl bg-red-950/40 hover:bg-red-900/60 border border-red-500/40 text-red-300 font-tech font-bold text-xs flex items-center gap-1 cursor-pointer transition-colors"
                            title={`Tách thành +${salvage.linhThach} LT${
                              salvage.tinhHoa > 0 ? `, +${salvage.tinhHoa} TH` : ''
                            }`}
                          >
                            <Trash2 className="w-3.5 h-3.5" />
                            <span>Tách (+{salvage.linhThach} LT)</span>
                          </button>
                        );
                      })()}
                    </>
                  ) : (
                    <button
                      type="button"
                      onClick={() => onUnequipItem(selectedItem.slotKey)}
                      className="w-full py-2 px-3 rounded-xl bg-slate-800 hover:bg-slate-700 border border-slate-700 text-slate-300 font-tech font-bold text-xs cursor-pointer transition-colors text-center"
                    >
                      THÁO RA TÚI ĐỒ
                    </button>
                  )}
                </div>
              </div>
            )}
          </div>
        )}

        {/* ================================================================= */}
        {/* TAB 2: FORGE UPGRADES */}
        {/* ================================================================= */}
        {activeTab === 'upgrades' && (
          <div className="space-y-2.5">
            {upgrades.map((up) => {
              const cost = getUpgradeCost(up);
              const canAfford = linhThach >= cost && up.level < up.maxLevel;

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
        {/* TAB 3: SPIRIT CONSTELLATION NODES */}
        {/* ================================================================= */}
        {activeTab === 'spirit' && (
          <div className="space-y-3">
            <div className="p-3 rounded-xl bg-[#080A10] border border-cyan-500/30 flex items-center justify-between">
              <div>
                <div className="text-[10px] text-slate-400 font-tech">Hào Quang Thần Hồn</div>
                <div className="text-sm font-bold text-cyan-300 font-tech">
                  x{spiritTotalMult.toFixed(2)} Sát Thương Toàn Bản Thân
                </div>
              </div>
              <div className="text-right">
                <div className="text-[10px] text-slate-400 font-tech">Tinh Hoa Đang Có</div>
                <div className="text-sm font-bold text-amber-400 font-tech">
                  {tinhHoa} TH
                </div>
              </div>
            </div>

            <div className="space-y-2">
              <div className="text-xs font-tech text-slate-400 font-semibold px-1">
                CHÒM SAO THẦN HỒN BẬC 1:
              </div>
              <div className="grid grid-cols-2 gap-2">
                {spiritNodes
                  .filter((n) => n.tier === 1)
                  .map((node) => {
                    const isSelected = selectedNode.id === node.id;
                    const canUnlock = canUnlockSpiritNode(
                      node.id,
                      spiritNodes,
                      tinhHoa,
                      tier2Unlocked
                    );

                    return (
                      <button
                        key={node.id}
                        type="button"
                        onClick={() => setSelectedNodeId(node.id)}
                        className={`p-2.5 rounded-xl border text-left transition-all cursor-pointer flex flex-col justify-between min-h-[92px] ${
                          node.unlocked
                            ? 'bg-cyan-950/20 border-cyan-500/40'
                            : canUnlock
                            ? 'bg-amber-950/20 border-amber-500/40 hover:border-amber-400'
                            : 'bg-slate-900/40 border-slate-800 opacity-60'
                        } ${isSelected ? 'ring-2 ring-cyan-400 shadow-lg shadow-cyan-500/20' : ''}`}
                      >
                        <div className="flex items-center justify-between mb-1">
                          <span className="text-[10px] font-tech text-slate-400">
                            Node #{node.id.split('_')[1]?.toUpperCase()}
                          </span>
                          {node.unlocked ? (
                            <Check className="w-3.5 h-3.5 text-emerald-400" />
                          ) : (
                            <Lock className="w-3.5 h-3.5 text-slate-500" />
                          )}
                        </div>

                        <div className="font-semibold text-xs text-slate-200 line-clamp-1">
                          {node.name}
                        </div>

                        <div className="text-[10px] font-tech text-cyan-400 mt-1">
                          +{Math.round(node.bonusMult * 100)}% Công Lực
                        </div>
                      </button>
                    );
                  })}
              </div>
            </div>

            {/* Selected Spirit Node Inspector Card */}
            {selectedNode && (
              <div className="p-3.5 rounded-xl bg-[#080A10] border border-cyan-500/40 space-y-2">
                <div className="flex items-center justify-between">
                  <h4 className="font-semibold text-sm text-cyan-300 font-tech">
                    {selectedNode.name}
                  </h4>
                  <span
                    className={`text-[10px] font-tech px-2 py-0.5 rounded ${
                      selectedNode.unlocked
                        ? 'bg-emerald-500/20 text-emerald-300'
                        : 'bg-slate-800 text-slate-400'
                    }`}
                  >
                    {selectedNode.unlocked ? 'ĐÃ KHAI MỞ' : 'CHƯA MỞ'}
                  </span>
                </div>

                <p className="text-xs text-slate-300 leading-relaxed">
                  {selectedNode.description}
                </p>

                <div className="flex items-center justify-between pt-2 border-t border-slate-800">
                  <span className="text-xs font-tech text-amber-300">
                    Chi phí: <b>{selectedNode.costTinhHoa} Tinh Hoa</b>
                  </span>

                  {!selectedNode.unlocked && (
                    <button
                      type="button"
                      disabled={!canUnlockSpiritNode(selectedNode.id, spiritNodes, tinhHoa, tier2Unlocked)}
                      onClick={() => onUnlockSpiritNode(selectedNode.id)}
                      className={`px-3 py-1.5 rounded-lg text-xs font-tech font-bold transition-all shadow-sm ${
                        canUnlockSpiritNode(selectedNode.id, spiritNodes, tinhHoa, tier2Unlocked)
                          ? 'bg-cyan-400 hover:bg-cyan-300 text-slate-950 cursor-pointer shadow-cyan-500/20'
                          : 'bg-slate-800 text-slate-500 cursor-not-allowed'
                      }`}
                    >
                      Khai Mở Node
                    </button>
                  )}
                </div>
              </div>
            )}
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
