# -*- coding: utf-8 -*-
with open(r'frontend\src\components\RightProgressionPanel.tsx', 'r', encoding='utf-8') as f:
    c = f.read()

target = """            {/* 1. Ngũ Đại Thuộc Tính Rèn (MMORPG Stats Card) */}
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
            </div>"""

replacement = """            {/* 1. Ngũ Đại Thuộc Tính Rèn (Trận Đồ Bản Mệnh Thần Lực) */}
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

if target in c:
    c = c.replace(target, replacement)
    with open(r'frontend\src\components\RightProgressionPanel.tsx', 'w', encoding='utf-8') as f:
        f.write(c)
    print("SUCCESS: Stat Nexus Replaced!")
else:
    print("FAILED: Target not found")
