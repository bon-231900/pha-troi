# -*- coding: utf-8 -*-
"""
Script to apply Balance Patch v3.0 UI enhancements to RightProgressionPanel.tsx
"""
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

with open(r'd:\tieu-thuyet\frontend\src\components\RightProgressionPanel.tsx', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Imports
c = c.replace(
    "  calculateArsenalBonuses,\n",
    "  calculateArsenalBonuses,\n  checkForgeEquilibrium,\n  EQUIPMENT_SETS,\n"
)

# 2. Pass upgrades to calculateArsenalBonuses
c = c.replace(
    "const arsenalBonuses = calculateArsenalBonuses(equippedItems);",
    "const arsenalBonuses = calculateArsenalBonuses(equippedItems, upgrades);"
)

# 3. Replace the small stats header with the full Ngũ Đại Thuộc Tính Rèn & 4 Sets block
old_stats_header = """            {/* Overview Stats Bar */}
            <div className="p-3 rounded-xl bg-[#080A10] border border-slate-800 flex items-center justify-between">
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

new_stats_header = """            {/* 1. NGŨ ĐẠI THUỘC TÍNH RÈN (5 CORE STATS) */}
            <div className="p-3 rounded-xl bg-[#080A10] border border-slate-800">
              <div className="flex items-center justify-between mb-2">
                <span className="text-[11px] font-tech font-bold text-amber-300">NGŨ ĐẠI THUỘC TÍNH RÈN</span>
                <span className="text-[10px] text-slate-400 font-mono">Chuẩn MMORPG v3.0</span>
              </div>
              <div className="grid grid-cols-5 gap-1.5 text-center font-tech">
                <div className="p-1.5 rounded-lg bg-slate-900/80 border border-slate-800">
                  <div className="text-[9px] text-slate-400">STR · Chùy</div>
                  <div className="text-xs font-bold text-amber-300">{arsenalBonuses.coreStats.str}</div>
                </div>
                <div className="p-1.5 rounded-lg bg-slate-900/80 border border-slate-800">
                  <div className="text-[9px] text-slate-400">DEX · Chuẩn</div>
                  <div className="text-xs font-bold text-cyan-300">{arsenalBonuses.coreStats.dex}</div>
                </div>
                <div className="p-1.5 rounded-lg bg-slate-900/80 border border-slate-800">
                  <div className="text-[9px] text-slate-400">INT · Nhiệt</div>
                  <div className="text-xs font-bold text-red-400">{arsenalBonuses.coreStats.int}</div>
                </div>
                <div className="p-1.5 rounded-lg bg-slate-900/80 border border-slate-800">
                  <div className="text-[9px] text-slate-400">PEN · Phá</div>
                  <div className="text-xs font-bold text-purple-400">{arsenalBonuses.coreStats.pen}</div>
                </div>
                <div className="p-1.5 rounded-lg bg-slate-900/80 border border-slate-800">
                  <div className="text-[9px] text-slate-400">SPI · Hưởng</div>
                  <div className="text-xs font-bold text-emerald-400">{arsenalBonuses.coreStats.spi}</div>
                </div>
              </div>

              {/* Stat breakdown badges */}
              <div className="mt-2 flex flex-wrap gap-2 text-[10px] font-tech text-slate-300 pt-2 border-t border-slate-800/60">
                <span className="px-1.5 py-0.5 rounded bg-cyan-950/60 text-cyan-300 border border-cyan-800/40">
                  Crit: {arsenalBonuses.critRateEffective}% {arsenalBonuses.critRateEffective >= 55 && '(Soft Cap)'}
                </span>
                <span className="px-1.5 py-0.5 rounded bg-purple-950/60 text-purple-300 border border-purple-800/40">
                  Xuyên Giáp: {Math.round(arsenalBonuses.piercePct * 100)}%
                </span>
                <span className="px-1.5 py-0.5 rounded bg-amber-950/60 text-amber-300 border border-amber-800/40">
                  Hoàng Kim: +{arsenalBonuses.perfectWindowMs}ms
                </span>
              </div>

              {/* Glancing Hit Warning */}
              {arsenalBonuses.glancingHitPenalty && (
                <div className="mt-2 p-2 rounded-lg bg-red-950/40 border border-red-500/40 text-[11px] text-red-300 flex items-start gap-1.5">
                  <span className="text-xs">⚠️</span>
                  <div>
                    <span className="font-bold">Cảnh Báo Dội Búa!</span> Lực Chùy ({arsenalBonuses.coreStats.str}) vượt quá 2.5x Nhiệt Lò ({arsenalBonuses.coreStats.int}). Đe nguội giảm 35% sát thương cuối! Hãy nâng cấp Ống Bễ (INT)!
                  </div>
                </div>
              )}
            </div>

            {/* 2. BỘ TRANG BỊ KHÍ GIỚI (SET BONUSES 2/4/6) */}
            <div className="p-3 rounded-xl bg-[#080A10] border border-slate-800">
              <div className="text-[11px] font-tech font-bold text-amber-300 mb-2">
                BỘ TRANG BỊ KHÍ GIỚI (SET BONUSES)
              </div>
              <div className="grid grid-cols-2 gap-2 text-[10px] font-tech mb-2">
                {Object.values(EQUIPMENT_SETS).map((s) => {
                  const cnt = arsenalBonuses.setCounts[s.id] || 0;
                  return (
                    <div
                      key={s.id}
                      className={`p-2 rounded-lg border ${
                        cnt >= 2
                          ? 'bg-slate-900 border-amber-400/40 text-amber-200'
                          : 'bg-slate-950/60 border-slate-800/60 text-slate-500'
                      }`}
                    >
                      <div className="flex items-center justify-between font-bold">
                        <span>{s.name}</span>
                        <span className={cnt >= 2 ? 'text-amber-400' : 'text-slate-600'}>
                          {cnt}/6 Món
                        </span>
                      </div>
                    </div>
                  );
                })}
              </div>

              {/* Active Set Perks List */}
              {arsenalBonuses.activeSetPerks.length > 0 ? (
                <div className="space-y-1">
                  {arsenalBonuses.activeSetPerks.map((perk, idx) => (
                    <div key={idx} className="text-[10px] text-emerald-300 flex items-center gap-1.5">
                      <span className="text-xs">✦</span>
                      <span>{perk}</span>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-[10px] text-slate-500 italic">
                  Chưa kích hoạt bộ nào (Cần ít nhất 2 món cùng bộ để mở hiệu ứng)
                </div>
              )}
            </div>"""

c = c.replace(old_stats_header, new_stats_header)

# 4. In Upgrades tab: add checkForgeEquilibrium constraint
old_upg_map = """            {upgrades.map((up) => {
              const cost = getUpgradeCost(up);
              const canAfford = linhThach >= cost && up.level < up.maxLevel;"""

new_upg_map = """            {upgrades.map((up) => {
              const cost = getUpgradeCost(up);
              const eqCheck = checkForgeEquilibrium(upgrades, up.id);
              const isEqLocked = !eqCheck.allowed;
              const canAfford = linhThach >= cost && up.level < up.maxLevel && !isEqLocked;"""

c = c.replace(old_upg_map, new_upg_map)

# Add equilibrium warning text inside the upgrade card
old_cost_row = """                  <div className="flex items-center justify-between pt-2 border-t border-slate-800/80">
                    <div className="text-xs font-tech text-slate-300">
                      Chi phí:{' '}
                      <span className="text-cyan-300 font-bold">
                        {cost.toLocaleString('en-US')} LT
                      </span>
                    </div>"""

new_cost_row = """                  {isEqLocked && (
                    <div className="text-[10px] text-red-400 font-tech mb-2 px-2 py-1 rounded bg-red-950/30 border border-red-500/30">
                      🔒 Lệch Cấp Lò Rèn (>15 cấp so với Cấp {eqCheck.minLevel}). Hãy nâng cấp các hạng mục khác!
                    </div>
                  )}

                  <div className="flex items-center justify-between pt-2 border-t border-slate-800/80">
                    <div className="text-xs font-tech text-slate-300">
                      Chi phí:{' '}
                      <span className="text-cyan-300 font-bold">
                        {cost.toLocaleString('en-US')} LT
                      </span>
                    </div>"""

c = c.replace(old_cost_row, new_cost_row)

with open(r'd:\tieu-thuyet\frontend\src\components\RightProgressionPanel.tsx', 'w', encoding='utf-8') as f:
    f.write(c)

print("RightProgressionPanel.tsx đã được nâng cấp UI Ngũ Đại Thuộc Tính & Set Bonuses!")
