with open('frontend/src/components/TopBossHeader.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

old_hp_target = """          {/* Boss Title & HP Stats */}
          <div className="relative z-10 flex items-center justify-between gap-2 mb-1">
            <div className="flex items-center gap-1.5 shrink-0">
              <span className="w-2 h-2 rounded-full bg-red-500 animate-pulse shrink-0 shadow-[0_0_6px_#EF4444]" />
              <span className="font-display text-[11px] sm:text-xs font-bold tracking-wider text-amber-300 uppercase whitespace-nowrap">
                {bossName}
              </span>
              <span className="hidden sm:inline px-1.5 py-0.2 rounded bg-amber-500/20 border border-amber-500/40 text-[9px] font-tech text-amber-300 whitespace-nowrap">
                {seal.shortName} (-{seal.damageReductionPct}%)
              </span>
            </div>

            <div className="font-tech text-[10px] sm:text-xs font-bold tabular-nums text-slate-200 whitespace-nowrap shrink-0">
              <span className="text-red-400 font-extrabold">{safeHp.toLocaleString('en-US')}</span>
              <span className="text-slate-400 font-normal"> / {safeMax.toLocaleString('en-US')} HP</span>
              <span className="ml-1 text-orange-400 font-semibold">(Nứt {crackPct.toFixed(1)}%)</span>
            </div>
          </div>"""

new_hp_target = """          {/* Boss Title & HP Stats */}
          <div className="relative z-10 flex items-center justify-between gap-1.5 mb-1 min-w-0">
            <div className="flex items-center gap-1 sm:gap-1.5 min-w-0">
              <span className="w-2 h-2 rounded-full bg-red-500 animate-pulse shrink-0 shadow-[0_0_6px_#EF4444]" />
              <span className="font-display text-[11px] sm:text-xs font-bold tracking-wider text-amber-300 uppercase truncate">
                {bossName}
              </span>
              <span className="hidden lg:inline px-1.5 py-0.2 rounded bg-amber-500/20 border border-amber-500/40 text-[9px] font-tech text-amber-300 whitespace-nowrap shrink-0">
                {seal.shortName} (-{seal.damageReductionPct}%)
              </span>
            </div>

            <div className="font-tech text-[10px] sm:text-xs font-bold tabular-nums text-slate-200 whitespace-nowrap shrink-0 pl-1.5">
              <span className="text-red-400 font-extrabold">{safeHp.toLocaleString('en-US')}</span>
              <span className="text-slate-400 font-normal"> / {safeMax.toLocaleString('en-US')} HP</span>
              <span className="ml-1 text-orange-400 font-semibold hidden md:inline">(Nứt {crackPct.toFixed(1)}%)</span>
            </div>
          </div>"""

old_furnace_target = """              <span className="truncate">
                Lò: <b className="text-amber-300">{serverFurnaceHeat.toLocaleString('en-US')}°C</b>
              </span>"""

new_furnace_target = """              <span className="whitespace-nowrap">
                Lò: <b className="text-amber-300">{serverFurnaceHeat >= 10000 ? '10k' : serverFurnaceHeat}°C</b>
              </span>"""

assert old_hp_target in code, "old_hp_target not found in TopBossHeader.tsx"
assert old_furnace_target in code, "old_furnace_target not found in TopBossHeader.tsx"

code = code.replace(old_hp_target, new_hp_target, 1)
code = code.replace(old_furnace_target, new_furnace_target, 1)

with open('frontend/src/components/TopBossHeader.tsx', 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated TopBossHeader.tsx successfully!")
