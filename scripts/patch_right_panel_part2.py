# -*- coding: utf-8 -*-
import sys
import re

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

with open('frontend/src/components/RightProgressionPanel.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

# Replace the inventory section
old_bag_pattern = """            {/* Backpack / Inventory Section with Quick Salvage */}
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
            </div>"""

new_bag_replacement = """            {/* Backpack / Inventory Section with Dynamic Capacity & Pity Counters */}
            <div className="pt-2 border-t border-slate-800 space-y-2">
              {/* Dual Pity Bar & Drop Luck Indicators */}
              <div className="p-2 rounded-xl bg-gradient-to-r from-slate-950 via-[#0B0F1C] to-slate-950 border border-slate-800 text-[10px] font-tech flex flex-col gap-1.5">
                <div className="flex items-center justify-between text-slate-300">
                  <span className="flex items-center gap-1 font-bold text-amber-300">
                    <Sparkles className="w-3 h-3 text-amber-400" />
                    BẢO HIỂM NỆN BÚA (ANVIL PITY):
                  </span>
                  <span className="text-cyan-300 font-mono">
                    {anvilPityCount}/200 {anvilPityCount >= 50 && anvilPityCount < 200 ? '(Đã bảo hiểm Tier B)' : anvilPityCount >= 200 ? '(Nổ Tier A!)' : `(Tier B: ${anvilPityCount}/50)`}
                  </span>
                </div>
                <div className="w-full bg-slate-900 h-1.5 rounded-full overflow-hidden border border-slate-800">
                  <div
                    className="bg-gradient-to-r from-cyan-500 via-purple-500 to-amber-400 h-full transition-all duration-300"
                    style={{ width: `${Math.min(100, (anvilPityCount / 200) * 100)}%` }}
                  />
                </div>

                <div className="flex items-center justify-between text-slate-400 pt-0.5">
                  <span className="flex items-center gap-1 font-bold text-red-300">
                    <Shield className="w-3 h-3 text-red-400" />
                    BẢO HIỂM RƯƠNG RAID (TIER S PITY):
                  </span>
                  <span className="text-red-300 font-mono">
                    {raidPityCount}/50 Ấn Ký {raidPityCount >= 50 ? '(Nổ Thần Khí Tier S!)' : ''}
                  </span>
                </div>
                <div className="w-full bg-slate-900 h-1 rounded-full overflow-hidden border border-slate-800">
                  <div
                    className="bg-gradient-to-r from-purple-500 to-red-500 h-full transition-all duration-300"
                    style={{ width: `${Math.min(100, (raidPityCount / 50) * 100)}%` }}
                  />
                </div>
              </div>

              {/* Inventory Header & Quick Salvage Actions */}
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-1.5">
                <div className="flex items-center gap-1.5 text-xs font-tech">
                  <PackageOpen className="w-3.5 h-3.5 text-cyan-400" />
                  <span className="font-bold text-slate-200">RƯƠNG KHÍ GIỚI</span>
                  <span className="text-[10px] text-amber-300 font-mono">
                    [{inventory.length}/{maxInventorySlots} Ô]
                  </span>
                </div>

                {/* Quick Salvage Actions */}
                <div className="flex items-center gap-1 flex-wrap">
                  {tierECount > 0 && (
                    <button
                      type="button"
                      onClick={() => onQuickSalvage(['common'])}
                      className="px-1.5 py-0.5 rounded bg-slate-800 hover:bg-slate-700 border border-slate-700 text-slate-300 text-[9px] font-tech cursor-pointer transition-colors"
                      title="Phân giải toàn bộ Tier E (Phàm Thiết) ra Bụi Thiết"
                    >
                      Tách Tier E ({tierECount})
                    </button>
                  )}
                  {tierDCount > 0 && (
                    <button
                      type="button"
                      onClick={() => onQuickSalvage(['uncommon'])}
                      className="px-1.5 py-0.5 rounded bg-emerald-950/60 hover:bg-emerald-900/80 border border-emerald-500/40 text-emerald-300 text-[9px] font-tech cursor-pointer transition-colors"
                      title="Phân giải toàn bộ Tier D (Tinh Thiết) ra Bụi Thiết"
                    >
                      Tách Tier D ({tierDCount})
                    </button>
                  )}
                  {tierCCount > 0 && (
                    <button
                      type="button"
                      onClick={() => onQuickSalvage(['rare'])}
                      className="px-1.5 py-0.5 rounded bg-blue-950/60 hover:bg-blue-900/80 border border-blue-500/40 text-blue-300 text-[9px] font-tech cursor-pointer transition-colors"
                      title="Phân giải toàn bộ Tier C (Cổ Đồng) ra Bụi Thiết"
                    >
                      Tách Tier C ({tierCCount})
                    </button>
                  )}
                </div>
              </div>

              {/* Auto-Salvage Checkbox Filters */}
              {onToggleAutoSalvage && (
                <div className="flex items-center gap-3 px-2 py-1 rounded-lg bg-slate-950/60 border border-slate-800/80 text-[10px] font-tech text-slate-400">
                  <span className="text-slate-300 font-semibold">Tự động nung:</span>
                  <label className="flex items-center gap-1 cursor-pointer hover:text-slate-200">
                    <input
                      type="checkbox"
                      checked={autoSalvageTiers.tierE}
                      onChange={() => onToggleAutoSalvage('tierE')}
                      className="accent-amber-400 w-3 h-3 rounded"
                    />
                    <span>Tier E</span>
                  </label>
                  <label className="flex items-center gap-1 cursor-pointer hover:text-slate-200">
                    <input
                      type="checkbox"
                      checked={autoSalvageTiers.tierD}
                      onChange={() => onToggleAutoSalvage('tierD')}
                      className="accent-emerald-400 w-3 h-3 rounded"
                    />
                    <span>Tier D</span>
                  </label>
                  <label className="flex items-center gap-1 cursor-pointer hover:text-slate-200">
                    <input
                      type="checkbox"
                      checked={autoSalvageTiers.tierC}
                      onChange={() => onToggleAutoSalvage('tierC')}
                      className="accent-blue-400 w-3 h-3 rounded"
                    />
                    <span>Tier C</span>
                  </label>
                </div>
              )}

              {/* Dynamic Bag Grid (Scales up to 64 slots based on Forger Rank) */}
              <div className="grid grid-cols-6 sm:grid-cols-8 gap-1.5 p-2 rounded-xl bg-[#070912] border border-slate-800/90 max-h-56 overflow-y-auto">
                {Array.from({ length: maxInventorySlots }).map((_, idx) => {
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
                      title={bagItem ? `${bagItem.name} [Tier ${rMeta?.tier} - ${rMeta?.label}]` : `Ô trống #${idx + 1}`}
                    >
                      {bagItem ? (
                        <>
                          <div className={`text-[9px] font-tech font-bold ${rMeta?.textColor}`}>
                            {bagItem.slotName.substring(0, 2)}
                          </div>
                          <div className="text-[7.5px] font-tech text-slate-400">
                            +{bagItem.baseStatValue}
                          </div>
                          {/* Tier Badge / Pip */}
                          <span
                            className={`absolute top-0.5 right-0.5 w-2 h-2 rounded-full text-[6px] font-bold flex items-center justify-center ${
                              bagItem.rarity === 'mythic'
                                ? 'bg-red-500 text-white animate-pulse'
                                : bagItem.rarity === 'legendary'
                                ? 'bg-amber-400 text-slate-950'
                                : bagItem.rarity === 'epic'
                                ? 'bg-purple-400 text-slate-950'
                                : bagItem.rarity === 'rare'
                                ? 'bg-blue-400 text-slate-950'
                                : bagItem.rarity === 'uncommon'
                                ? 'bg-emerald-400 text-slate-950'
                                : 'bg-slate-600 text-white'
                            }`}
                          >
                            {rMeta?.tier}
                          </span>
                        </>
                      ) : (
                        <span className="text-[10px] text-slate-700">·</span>
                      )}
                    </button>
                  );
                })}
              </div>
            </div>"""

if old_bag_pattern in code:
    code = code.replace(old_bag_pattern, new_bag_replacement, 1)
    print("Replaced inventory section with dynamic capacity & pity bars.")
else:
    print("Warning: old_bag_pattern not found!")

# Now add Ascension button in the item action buttons
old_salvage_action = """                      {(() => {
                        const salvage = getSalvageYield(activeSelected);
                        return (
                          <button
                            type="button"
                            onClick={() => onSalvageItem(activeSelected)}
                            className="py-2 px-3 rounded-xl bg-red-950/40 hover:bg-red-900/60 border border-red-500/40 text-red-300 font-tech font-bold text-xs flex items-center gap-1 cursor-pointer transition-colors"
                            title={`Tách thành +${salvage.linhThach} LT${
                              salvage.tinhHoa > 0 ? `, +${salvage.tinhHoa} TH` : ''
                            }`}
                          >
                            <Trash2 className="w-3.5 h-3.5" />
                            <span>Tách (+{salvage.linhThach} LT)</span>
                          </button>
                        );
                      })()}"""

new_salvage_action = """                      {(() => {
                        const salvage = getSalvageYield(activeSelected);
                        return (
                          <button
                            type="button"
                            onClick={() => onSalvageItem(activeSelected)}
                            className="py-2 px-3 rounded-xl bg-red-950/40 hover:bg-red-900/60 border border-red-500/40 text-red-300 font-tech font-bold text-xs flex items-center gap-1 cursor-pointer transition-colors"
                            title={`Tách: +${salvage.ironDust} Bụi Thiết, +${salvage.linhThach} LT${
                              salvage.tinhHoa > 0 ? `, +${salvage.tinhHoa} TH` : ''
                            }${salvage.celestialStar > 0 ? `, +${salvage.celestialStar} Thiên Tinh` : ''}`}
                          >
                            <Trash2 className="w-3.5 h-3.5" />
                            <span>Tách (+{salvage.ironDust} Bụi)</span>
                          </button>
                        );
                      })()}"""

if old_salvage_action in code:
    code = code.replace(old_salvage_action, new_salvage_action, 1)
    print("Updated salvage button with iron dust yield.")

# Add Tier A -> S Ascension button
old_action_block = """                {/* Action Buttons: Equip or Salvage */}"""
ascension_code = """                {/* Tier A -> Tier S Ascension (Thăng Bậc Thần Khí) */}
                {activeSelected.rarity === 'legendary' && onAscendItem && (
                  <div className="pt-2 border-t border-purple-900/50 flex flex-col gap-1.5">
                    <button
                      type="button"
                      onClick={() => onAscendItem(activeSelected)}
                      disabled={ironDust < 1000 || tinhHoa < 10 || celestialStars < 1}
                      className={`w-full py-2 px-3 rounded-xl font-tech font-bold text-xs tracking-wider transition-all flex items-center justify-center gap-1.5 ${
                        ironDust >= 1000 && tinhHoa >= 10 && celestialStars >= 1
                          ? 'bg-gradient-to-r from-red-600 via-purple-600 to-amber-500 hover:brightness-125 text-white shadow-lg shadow-purple-500/30 cursor-pointer active:scale-95'
                          : 'bg-slate-900 border border-slate-800 text-slate-500 cursor-not-allowed opacity-60'
                      }`}
                      title="Nâng cấp trang bị Tier A (Địa Linh Kim) lên Tier S (Thiên Đạo Thần Khí) giữ nguyên toàn bộ Affix"
                    >
                      <Sparkles className="w-3.5 h-3.5 text-amber-300 animate-spin" />
                      <span>THĂNG BẬC TIER S (1000 Bụi + 10 TH + 1 Thiên Tinh)</span>
                    </button>
                  </div>
                )}

                {/* Action Buttons: Equip or Salvage */}"""

if old_action_block in code and "THĂNG BẬC TIER S" not in code:
    code = code.replace(old_action_block, ascension_code, 1)
    print("Added Tier A -> S Ascension button.")

with open('frontend/src/components/RightProgressionPanel.tsx', 'w', encoding='utf-8') as f:
    f.write(code)

print("Saved RightProgressionPanel.tsx part 2 successfully!")
