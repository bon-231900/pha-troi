# -*- coding: utf-8 -*-
"""
Script to apply the comprehensive Arsenal & Rune UI Revamp to RightProgressionPanel.tsx
"""
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

FILE_PATH = r'frontend\src\components\RightProgressionPanel.tsx'

with open(FILE_PATH, 'r', encoding='utf-8') as f:
    c = f.read()

# -------------------------------------------------------------------------
# 1. ADD ARSENAL ART IMPORTS
# -------------------------------------------------------------------------
import_target = "const ITEM_ART_URLS: Record<EquipmentSlotKey, string> = {"
if "arsenalArtAssets" not in c:
    c = c.replace(
        import_target,
        """import {
  RELIC_ART_ASSETS,
  RUNE_ART_BY_TYPE,
  STAT_SIGIL_ASSETS,
  getRelicArt,
  getRuneArt,
} from '../game/arsenalArtAssets';

const ITEM_ART_URLS: Record<EquipmentSlotKey, string> = {"""
    )

# Update ITEM_ART_URLS to the new high-res assets
c = c.replace("'/assets/art/items/item_hammer.webp'", "'/assets/art/items/item_hammer_celestial.webp'")
c = c.replace("'/assets/art/items/item_anvil.webp'", "'/assets/art/items/item_anvil_primordial.webp'")
c = c.replace("'/assets/art/items/item_bellows.webp'", "'/assets/art/items/item_bellows_samadhi.webp'")
c = c.replace("'/assets/art/items/item_gauntlets.webp'", "'/assets/art/items/item_gauntlets_dragonscale.webp'")
c = c.replace("'/assets/art/items/item_apron.webp'", "'/assets/art/items/item_apron_celestial_mail.webp'")
c = c.replace("'/assets/art/items/item_relic.webp'", "'/assets/art/items/item_relic_bagua_core.webp'")

# -------------------------------------------------------------------------
# 2. UPGRADE NAVIGATION TABS & RESOURCE BAR
# -------------------------------------------------------------------------
old_tabs_and_bar = """      {/* 4 Segmented Control Tabs */}
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
      </div>"""

new_tabs_and_bar = """      {/* 4 Xianxia Daoist Token Tabs */}
      <div
        role="tablist"
        aria-label="Quản lý Vũ Khí, Rèn Đúc, Thần Hồn và Bảng Vàng"
        className="grid grid-cols-4 gap-1 p-1 bg-[#060810] border border-amber-500/30 rounded-xl mb-2.5 shrink-0 shadow-lg"
      >
        <button
          type="button"
          role="tab"
          aria-selected={activeTab === 'arsenal'}
          onClick={() => setActiveTab('arsenal')}
          className={`flex items-center justify-center gap-1.5 py-1.5 px-1 rounded-lg text-xs transition-all cursor-pointer whitespace-nowrap font-tech ${
            activeTab === 'arsenal'
              ? 'bg-gradient-to-b from-amber-400 via-amber-500 to-amber-600 text-slate-950 font-bold shadow-[0_0_12px_rgba(245,158,11,0.4)] border border-amber-300 ring-1 ring-amber-400/50'
              : 'text-slate-400 hover:text-amber-200 hover:bg-slate-900/60'
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
          className={`flex items-center justify-center gap-1.5 py-1.5 px-1 rounded-lg text-xs transition-all cursor-pointer whitespace-nowrap font-tech ${
            activeTab === 'upgrades'
              ? 'bg-gradient-to-b from-amber-400 via-amber-500 to-amber-600 text-slate-950 font-bold shadow-[0_0_12px_rgba(245,158,11,0.4)] border border-amber-300 ring-1 ring-amber-400/50'
              : 'text-slate-400 hover:text-amber-200 hover:bg-slate-900/60'
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
          className={`flex items-center justify-center gap-1.5 py-1.5 px-1 rounded-lg text-xs transition-all cursor-pointer whitespace-nowrap font-tech ${
            activeTab === 'spirit'
              ? 'bg-gradient-to-b from-cyan-400 via-cyan-500 to-cyan-600 text-slate-950 font-bold shadow-[0_0_12px_rgba(6,182,212,0.4)] border border-cyan-300 ring-1 ring-cyan-400/50'
              : 'text-slate-400 hover:text-cyan-200 hover:bg-slate-900/60'
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
          className={`flex items-center justify-center gap-1.5 py-1.5 px-1 rounded-lg text-xs transition-all cursor-pointer whitespace-nowrap font-tech ${
            activeTab === 'leaderboard'
              ? 'bg-gradient-to-b from-amber-400 via-amber-500 to-amber-600 text-slate-950 font-bold shadow-[0_0_12px_rgba(245,158,11,0.4)] border border-amber-300 ring-1 ring-amber-400/50'
              : 'text-slate-400 hover:text-amber-200 hover:bg-slate-900/60'
          }`}
          title="Bảng Vàng Vạn Dân"
        >
          <Trophy className="w-3.5 h-3.5" />
          <span className="truncate">Bảng Vàng</span>
        </button>
      </div>

      {/* Celestial Jade Resource Capsule */}
      <div className="flex items-center justify-between p-1.5 rounded-xl bg-[#070A14] border border-amber-500/20 mb-2.5 font-tech text-[10.5px] shrink-0 overflow-x-auto gap-1 shadow-inner">
        <div className="px-2 py-1 rounded-lg bg-cyan-950/40 border border-cyan-500/30 flex items-center gap-1 text-cyan-300 font-bold whitespace-nowrap shadow-sm">
          <span className="text-[10px] text-cyan-400">💎 LT:</span>
          <span>{linhThach.toLocaleString('en-US')}</span>
        </div>

        <div className="px-2 py-1 rounded-lg bg-amber-950/40 border border-amber-500/30 flex items-center gap-1 text-amber-300 font-bold whitespace-nowrap shadow-sm">
          <span className="text-[10px] text-amber-400">🔥 Tinh Hoa:</span>
          <span>{tinhHoa}</span>
        </div>

        <div className="px-2 py-1 rounded-lg bg-slate-900/80 border border-slate-700/60 flex items-center gap-1 text-slate-200 font-bold whitespace-nowrap shadow-sm">
          <span className="text-[10px] text-slate-400">⚙️ Bụi Thiết:</span>
          <span>{ironDust.toLocaleString('en-US')}</span>
        </div>

        {celestialStars > 0 && (
          <div className="px-2 py-1 rounded-lg bg-purple-950/60 border border-purple-500/40 flex items-center gap-1 text-purple-300 font-bold whitespace-nowrap shadow-sm">
            <span>✨ {celestialStars} T.Tinh</span>
          </div>
        )}
      </div>"""

if old_tabs_and_bar in c:
    c = c.replace(old_tabs_and_bar, new_tabs_and_bar)
    print("[+] Replaced Tabs & Resource Bar")
else:
    print("[-] Old tabs block not found directly, checking fallback...")

# -------------------------------------------------------------------------
# 3. UPGRADE NGŨ ĐẠI THUỘC TÍNH RÈN
# -------------------------------------------------------------------------
old_stat_nexus = """            {/* 1. Ngũ Đại Thuộc Tính Rèn (MMORPG Stats Card) */}
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
                      ⚠️ Dội Búa: STR > 2.5x INT (-30% DMG)
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
            </div>"""

new_stat_nexus = """            {/* 1. Ngũ Đại Thuộc Tính Rèn (Trận Đồ Bản Mệnh Thần Lực) */}
            <div className="p-3 rounded-xl bg-gradient-to-b from-[#0B0F1C] to-[#070912] border border-amber-500/40 shadow-xl flex flex-col gap-2.5 relative overflow-hidden">
              <div className="flex items-center justify-between relative z-10">
                <div className="flex items-center gap-2">
                  <div className="w-5 h-5 rounded bg-amber-500/20 border border-amber-500/40 flex items-center justify-center">
                    <Shield className="w-3.5 h-3.5 text-amber-400" />
                  </div>
                  <div>
                    <div className="text-[11px] font-tech font-bold text-amber-300 tracking-wider">
                      NGŨ ĐẠI THUỘC TÍNH RÈN
                    </div>
                    <div className="text-[9px] text-slate-400">
                      Trận đồ Thần Lực bản mệnh thợ rèn
                    </div>
                  </div>
                </div>
                <div className="px-2 py-0.5 rounded-full bg-cyan-950/60 border border-cyan-500/40 text-[10px] font-tech text-cyan-300 font-mono shadow-sm">
                  {arsenalBonuses.totalEquippedCount}/6 Món Thần Khí
                </div>
              </div>

              {/* 5 Core Attributes with Authentic Sigils */}
              <div className="grid grid-cols-5 gap-1.5 font-tech relative z-10">
                {(['str', 'dex', 'int', 'pen', 'spi'] as const).map((statKey) => {
                  const sigil = STAT_SIGIL_ASSETS[statKey];
                  const val = statKey === 'str'
                    ? arsenalBonuses.coreStats.str
                    : statKey === 'dex'
                    ? arsenalBonuses.coreStats.dex
                    : statKey === 'int'
                    ? arsenalBonuses.coreStats.int
                    : statKey === 'pen'
                    ? arsenalBonuses.coreStats.pen
                    : arsenalBonuses.coreStats.spi;

                  return (
                    <div
                      key={statKey}
                      title={`${sigil.label}: ${sigil.desc}`}
                      className="p-1.5 rounded-lg bg-[#0E1426]/90 border border-slate-800/80 hover:border-amber-500/50 flex flex-col items-center justify-center gap-1 transition-all group cursor-help shadow"
                    >
                      <img
                        src={sigil.url}
                        alt={sigil.label}
                        className="w-7 h-7 object-contain drop-shadow group-hover:scale-110 transition-transform"
                      />
                      <span className="text-[9px] text-slate-400 tracking-tight">{sigil.label}</span>
                      <span className="text-xs font-bold font-mono tracking-tight" style={{ color: sigil.color }}>
                        {val}
                      </span>
                    </div>
                  );
                })}
              </div>

              {/* Dynamic Equilibrium & Secondary stats */}
              <div className="p-2 rounded-lg bg-[#080B14] border border-slate-800/90 flex flex-col sm:flex-row sm:items-center justify-between gap-1.5 text-[10px] font-tech relative z-10">
                <div className="flex items-center gap-1.5">
                  {arsenalBonuses.glancingHitPenalty ? (
                    <span className="text-red-400 bg-red-950/80 px-2 py-0.5 rounded border border-red-500/50 flex items-center gap-1 font-bold">
                      ⚠️ Dội Búa (STR &gt; 2.5x INT)
                    </span>
                  ) : (
                    <span className="text-emerald-300 bg-emerald-950/80 px-2 py-0.5 rounded border border-emerald-500/50 flex items-center gap-1 font-bold">
                      ✓ Cân Bằng STR/INT: {(arsenalBonuses.coreStats.str / Math.max(1, arsenalBonuses.coreStats.int)).toFixed(1)}
                    </span>
                  )}
                </div>
                <div className="flex items-center gap-2 text-cyan-300 font-mono">
                  <span>Xuyên: +{arsenalBonuses.piercePct}%</span>
                  <span className="text-slate-600">·</span>
                  <span>MF: +{arsenalBonuses.magicFindPct}%</span>
                  <span className="text-slate-600">·</span>
                  <span>Crit: {arsenalBonuses.critRateEffective}%</span>
                </div>
              </div>
            </div>"""

if old_stat_nexus in c:
    c = c.replace(old_stat_nexus, new_stat_nexus)
    print("[+] Replaced Ngũ Đại Thuộc Tính Rèn")
else:
    print("[-] Old stat nexus not found directly")

# -------------------------------------------------------------------------
# 4. UPGRADE 6 RELICS CARDS & SOCKET PIPS
# -------------------------------------------------------------------------
old_relic_map = """                  (slotKey) => {
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
                  }"""

new_relic_map = """                  (slotKey) => {
                    const item = equippedItems[slotKey];
                    const slotMeta = SLOT_INFO[slotKey];
                    const isSelected = selectedSlotKey === slotKey;
                    const rMeta = item ? getItemRarityMeta(item.rarity) : null;
                    const itemLvl = item?.level || 1;
                    const unlockedSockets = item?.unlockedSockets ?? (item ? getUnlockedSockets(item.rarity) : 0);
                    const sockets = item?.sockets || [];
                    const relicCfg = getRelicArt(slotKey);

                    return (
                      <button
                        key={slotKey}
                        type="button"
                        onClick={() => setSelectedSlotKey(slotKey)}
                        className={`p-2.5 rounded-xl border text-left transition-all cursor-pointer flex flex-col justify-between min-h-[105px] group relative overflow-hidden ${
                          isSelected
                            ? 'bg-gradient-to-b from-[#12182B] to-[#0A0E1A] border-amber-400 ring-2 ring-amber-400/50 shadow-xl shadow-amber-500/20'
                            : 'bg-[#080B14] border-slate-800 hover:border-amber-500/40 hover:bg-[#0D1222]'
                        }`}
                      >
                        <div>
                          <div className="flex items-center justify-between mb-1.5">
                            <span className="text-[9px] font-tech uppercase text-amber-400/90 font-bold tracking-wider">
                              {slotMeta.name}
                            </span>
                            {item && (
                              <span className={`text-[8px] px-1.5 py-0.2 rounded font-tech font-bold uppercase ${rMeta?.badgeBg}`}>
                                Tier {rMeta?.tier}
                              </span>
                            )}
                          </div>

                          <div className="flex items-center gap-2">
                            <div className={`w-11 h-11 rounded-xl bg-black/90 border flex items-center justify-center shrink-0 overflow-hidden shadow-inner relative transition-transform group-hover:scale-105 ${
                              isSelected ? 'border-amber-400/80 shadow-[0_0_10px_rgba(245,158,11,0.3)]' : 'border-slate-800'
                            }`}>
                              <img
                                src={relicCfg.primary}
                                alt={slotMeta.name}
                                onError={(e) => {
                                  (e.target as HTMLImageElement).src = relicCfg.fallback;
                                }}
                                className="w-9 h-9 object-contain drop-shadow"
                              />
                            </div>
                            <div className="min-w-0 flex-1">
                              <div className={`font-bold text-[11px] line-clamp-2 leading-snug min-h-[26px] ${rMeta?.textColor || 'text-slate-200'}`}>
                                {item ? item.name : relicCfg.title}
                              </div>
                              <div className="text-[9.5px] font-tech text-cyan-300 font-mono mt-0.5">
                                +{item?.baseStatValue || 1} {item?.baseStatUnit || 'DMG'}
                              </div>
                            </div>
                          </div>
                        </div>

                        {/* Level & Socket Pips with Real Gems */}
                        <div className="mt-2 pt-1 border-t border-slate-800/80 flex items-center justify-between text-[9px] font-tech">
                          <span className="text-amber-300 font-mono font-bold flex items-center gap-1">
                            Lv.{itemLvl}<span className="text-slate-500">/20</span>
                          </span>
                          {/* Socket Pips */}
                          <div className="flex items-center gap-1">
                            {Array.from({ length: 4 }).map((_, sIdx) => {
                              const isUnlocked = sIdx < unlockedSockets;
                              const gem = isUnlocked ? sockets[sIdx] : null;

                              if (!isUnlocked) {
                                return (
                                  <span
                                    key={sIdx}
                                    className="w-3 h-3 rounded-full bg-slate-950 border border-slate-800/80 text-[7px] text-slate-700 flex items-center justify-center"
                                    title="Lỗ khảm bị khóa"
                                  >
                                    🔒
                                  </span>
                                );
                              }
                              if (gem) {
                                const runeUrl = getRuneArt(gem.type);
                                return (
                                  <div
                                    key={sIdx}
                                    className="w-3.5 h-3.5 rounded-full border flex items-center justify-center overflow-hidden shadow-sm animate-pulse"
                                    style={{ borderColor: gem.color }}
                                    title={`Đã khảm: ${gem.name} (+${gem.value} ${gem.statLabel})`}
                                  >
                                    <img
                                      src={runeUrl}
                                      alt={gem.name}
                                      className="w-full h-full object-cover"
                                    />
                                  </div>
                                );
                              }
                              return (
                                <span
                                  key={sIdx}
                                  className="w-3 h-3 rounded-full border border-dashed border-cyan-400/80 bg-cyan-950/40 text-[7px] text-cyan-300 flex items-center justify-center"
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
                  }"""

if old_relic_map in c:
    c = c.replace(old_relic_map, new_relic_map)
    print("[+] Replaced 6 Relics Matrix")
else:
    print("[-] Old relic map not found directly")

# -------------------------------------------------------------------------
# 5. UPGRADE SELECTED RELIC HERO & SOCKET PEDESTAL
# -------------------------------------------------------------------------
old_selected_hero = """                  {/* Item Header */}
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
                  </div>"""

new_selected_hero = """                  {/* Item Header */}
                  <div className="flex items-start justify-between gap-2">
                    <div className="flex items-center gap-3">
                      <div className="w-14 h-14 rounded-2xl bg-black/95 border-2 border-amber-500/60 flex items-center justify-center shrink-0 overflow-hidden shadow-xl shadow-amber-500/10 relative group">
                        <img
                          src={getRelicArt(selectedSlotKey).primary}
                          alt={slotMeta.name}
                          onError={(e) => {
                            (e.target as HTMLImageElement).src = getRelicArt(selectedSlotKey).fallback;
                          }}
                          className="w-11 h-11 object-contain drop-shadow group-hover:scale-110 transition-transform"
                        />
                      </div>
                      <div>
                        <div className="flex items-center gap-1.5">
                          <span className="text-[10px] font-tech text-amber-400 font-bold uppercase tracking-wider">
                            {slotMeta.name}
                          </span>
                          <span className={`text-[9px] px-1.5 py-0.2 rounded font-tech font-bold uppercase ${rMeta.badgeBg}`}>
                            Tier {rMeta.tier} · {rMeta.label}
                          </span>
                        </div>
                        <h4 className={`text-sm font-bold leading-tight ${rMeta.textColor}`}>
                          {item.name}
                        </h4>
                        <div className="text-[11px] font-tech text-cyan-300 font-mono mt-0.5">
                          {item.baseStatLabel}: +{item.baseStatValue} {item.baseStatUnit}
                        </div>
                      </div>
                    </div>
                  </div>"""

if old_selected_hero in c:
    c = c.replace(old_selected_hero, new_selected_hero)
    print("[+] Replaced Selected Item Hero Header")

# -------------------------------------------------------------------------
# 6. UPGRADE SOCKET MODULE IN SELECTED RELIC WITH REAL GEM VISUALS
# -------------------------------------------------------------------------
old_socket_card = """                        if (gem) {
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
                        }"""

new_socket_card = """                        if (gem) {
                          return (
                            <div
                              key={sIdx}
                              className="p-2 rounded-xl bg-[#070A14] border border-slate-700/80 flex items-center justify-between gap-2 shadow-inner"
                              style={{ borderLeftColor: gem.color, borderLeftWidth: '3px' }}
                            >
                              <div className="flex items-center gap-2 min-w-0 flex-1">
                                <div
                                  className="w-8 h-8 rounded-lg bg-black/90 border flex items-center justify-center shrink-0 overflow-hidden shadow-sm p-0.5"
                                  style={{ borderColor: `${gem.color}60` }}
                                >
                                  <img
                                    src={getRuneArt(gem.type)}
                                    alt={gem.name}
                                    className="w-full h-full object-contain"
                                  />
                                </div>
                                <div className="min-w-0 flex-1">
                                  <div className="flex items-center gap-1">
                                    <span className="text-[10px] font-bold text-slate-200 truncate">
                                      {gem.name}
                                    </span>
                                    <span className="text-[8px] font-tech px-1 rounded bg-slate-800 text-cyan-300 font-mono">
                                      +{gem.value} {gem.statLabel}
                                    </span>
                                  </div>
                                  <div className="text-[8.5px] text-slate-400 truncate mt-0.5">
                                    {gem.specialPerk}
                                  </div>
                                </div>
                              </div>
                              <button
                                type="button"
                                onClick={() => onUnsocketGem?.(selectedSlotKey, sIdx)}
                                className="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-red-950 hover:border-red-500/50 border border-slate-700 text-slate-300 hover:text-red-200 text-[9px] font-tech font-bold cursor-pointer shrink-0 transition-all active:scale-95"
                                title="Tháo ngọc về Túi Phù Thạch (Miễn phí)"
                              >
                                Tháo
                              </button>
                            </div>
                          );
                        }"""

if old_socket_card in c:
    c = c.replace(old_socket_card, new_socket_card)
    print("[+] Replaced Socket Pedestals with Real Gem Visuals")

# -------------------------------------------------------------------------
# 7. UPGRADE TÚI PHÙ THẠCH THƯỢNG CỔ WITH AUTHENTIC RUNE GEMS
# -------------------------------------------------------------------------
old_rune_card = """                        <div
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
                        </div>"""

new_rune_card = """                        <div
                          key={gem.id}
                          className="p-2.5 rounded-xl bg-gradient-to-b from-[#0E1324] to-[#080B14] border border-slate-800 hover:border-cyan-500/50 flex flex-col justify-between gap-2 shadow-lg transition-all"
                          style={{ borderTopColor: gem.color, borderTopWidth: '3px' }}
                        >
                          <div className="flex items-start gap-2.5">
                            <div
                              className="w-11 h-11 rounded-xl bg-black/90 border flex items-center justify-center shrink-0 overflow-hidden shadow-inner p-1 relative"
                              style={{ borderColor: `${gem.color}60` }}
                            >
                              <img
                                src={getRuneArt(gem.type)}
                                alt={gem.name}
                                className="w-full h-full object-contain drop-shadow hover:scale-110 transition-transform"
                              />
                            </div>
                            <div className="min-w-0 flex-1">
                              <div className="flex items-center justify-between gap-1">
                                <span className="font-bold text-[11px] text-slate-200 truncate">
                                  {gem.name}
                                </span>
                                <span
                                  className="text-[8px] font-tech px-1.5 py-0.2 rounded font-bold uppercase"
                                  style={{ backgroundColor: `${gem.color}25`, color: gem.color, border: `1px solid ${gem.color}40` }}
                                >
                                  {gem.tier}
                                </span>
                              </div>
                              <div className="text-[9.5px] font-tech text-cyan-300 font-mono mt-0.5">
                                +{gem.value} {gem.statLabel}
                              </div>
                              <div className="text-[8.5px] text-slate-400 mt-0.5 line-clamp-2 leading-tight">
                                {gem.specialPerk}
                              </div>
                            </div>
                          </div>

                          <div className="pt-1.5 border-t border-slate-800/80 flex items-center justify-between">
                            <span className="text-[8.5px] font-tech uppercase font-bold" style={{ color: gem.color }}>
                              Hệ {gem.type}
                            </span>
                            {canSocket ? (
                              <button
                                type="button"
                                onClick={() => onSocketGem?.(selectedSlotKey, firstEmptyIndex, gem.id)}
                                className="px-2.5 py-1 rounded-lg bg-gradient-to-r from-cyan-600 to-cyan-500 hover:from-cyan-500 hover:to-cyan-400 text-white font-tech font-bold text-[9.5px] cursor-pointer shadow-md shadow-cyan-500/20 transition-all active:scale-95"
                              >
                                Khảm Vào {SLOT_INFO[selectedSlotKey].name}
                              </button>
                            ) : (
                              <span className="text-[8.5px] font-tech text-slate-500 italic">
                                {currentSelected ? 'Hết lỗ trống' : 'Chưa chọn vũ khí'}
                              </span>
                            )}
                          </div>
                        </div>"""

if old_rune_card in c:
    c = c.replace(old_rune_card, new_rune_card)
    print("[+] Replaced Túi Phù Thạch Cards with 3D Gem Visuals")

with open(FILE_PATH, 'w', encoding='utf-8') as f:
    f.write(c)

print("[SUCCESS] RightProgressionPanel.tsx patched successfully!")
