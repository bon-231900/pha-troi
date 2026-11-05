# -*- coding: utf-8 -*-
with open('frontend/src/components/TopBossHeader.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

old_block = '''        {/* 2. Center Capsule: VÒM TRỜI THIẾT VÂN & WORLD RAID METERS */}
        <div
          aria-label="Thanh máu Vòm Trời & Trạng Thái World Raid"
          className="pointer-events-auto flex-1 max-w-md sm:max-w-xl md:max-w-2xl mx-auto px-4 py-2 rounded-2xl bg-[#060914]/92 border border-amber-500/40 shadow-[0_8px_30px_rgba(0,0,0,0.9)] backdrop-blur-md relative overflow-hidden"
        >
          <div className="absolute inset-0 bg-gradient-to-b from-amber-500/10 via-transparent to-black/40 pointer-events-none" />

          {/* Boss Title & HP Stats */}
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
          </div>

          {/* Ornate Dragon Jade HP Trough with Animated Ghost Bar */}
          <div className="relative z-10 h-5 sm:h-6 w-full flex items-center justify-center my-0.5">
            {/* Active Trough Background & Bars */}
            <div className="absolute inset-x-[3%] top-[30%] bottom-[28%] rounded-sm overflow-hidden bg-black/90 shadow-inner">
              {/* Visual Ghost Trail Bar (Máu tuột vàng rực) */}
              <div
                className="absolute inset-y-0 left-0 bg-gradient-to-r from-amber-200 via-amber-300 to-amber-500 shadow-[0_0_12px_#F59E0B] transition-all duration-300"
                style={{ width: `${effectiveTrailPct}%` }}
              />
              {/* Active HP Bar with Combat Hit Flash */}
              <div
                className={`absolute inset-y-0 left-0 bg-gradient-to-r from-red-600 via-orange-500 to-amber-400 transition-all duration-100 ${
                  isHitFlashing ? 'brightness-150 shadow-[0_0_14px_#FFF]' : 'shadow-[0_0_8px_#F59E0B]'
                }`}
                style={{ width: `${hpPct}%` }}
              />
            </div>
            {/* Dragon Jade Well Bezel Frame */}
            <img
              src={HEADER_FRAME_ASSETS.hpWell}
              alt="Dragon Jade Well"
              className="absolute inset-0 w-full h-full object-fill pointer-events-none z-20 drop-shadow-[0_0_6px_rgba(16,185,129,0.35)]"
            />
          </div>

          {/* World Raid v3.1 4-Meter HUD Row */}
          <div className="relative z-10 grid grid-cols-2 sm:grid-cols-4 items-center justify-between text-[9px] sm:text-[10px] font-tech text-slate-300 mt-1.5 gap-2 pt-1 border-t border-slate-800/80 tabular-nums">
            {/* Meter 1: Phá Giáp */}
            <div className="flex items-center gap-1.5 truncate" title="Thanh Phá Giáp Thiên Đạo: Bầu trời tự động hồi giáp mỗi giây!">
              <img
                src={HEADER_ICON_ASSETS.armorBreak}
                alt="Phá Giáp"
                className="w-4 h-4 object-contain filter drop-shadow-[0_0_4px_#A855F7] shrink-0"
              />
              {isShieldBroken ? (
                <span className="text-cyan-300 font-bold animate-pulse truncate">
                  VỠ GIÁP ({shieldBreakTimeLeft.toFixed(0)}s)
                </span>
              ) : (
                <span className="truncate">
                  Giáp: <b className="text-purple-300">{activeArmorBreakPoints}</b>/{armorBreakMaxPoints}
                  {isArmorRegenFrozen ? (
                    <span className="text-emerald-400 font-bold ml-1 text-[8px] sm:text-[9px]">(Băng hồi)</span>
                  ) : (
                    <span className="text-rose-400 font-semibold ml-1 text-[8px] sm:text-[9px]">(-{armorRegenRate}/s)</span>
                  )}
                </span>
              )}
            </div>

            {/* Meter 2: Đại Hỏa Hẩu */}
            <div className="flex items-center gap-1.5 truncate" title="Đại Hỏa Hẩu Toàn Server: Cần vượt ngưỡng để vòm trời nung chảy!">
              <img
                src={HEADER_ICON_ASSETS.furnaceHeat}
                alt="Hỏa Hẩu"
                className="w-4 h-4 object-contain filter drop-shadow-[0_0_4px_#F97316] shrink-0"
              />
              <span className="whitespace-nowrap">
                Lò: <b className="text-amber-300">{serverFurnaceHeat >= 10000 ? '10k' : serverFurnaceHeat}°C</b>
              </span>
              {serverFurnaceHeat >= vaultMeltingThreshold ? (
                <span className="px-1 py-0.2 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-[8px] font-bold">
                  🔥 Nung
                </span>
              ) : (
                <span className="px-1 py-0.2 rounded bg-cyan-500/20 text-cyan-300 border border-cyan-500/30 text-[8px] font-semibold" title={`Cần đạt ${vaultMeltingThreshold}°C`}>
                  ❄️ Đông
                </span>
              )}
            </div>

            {/* Meter 3: Độ Bền Đại Đe */}
            <div className="flex items-center gap-1.5 truncate" title="Độ Bền Đại Đe Thần Server (10,000 HP). Vỡ đe = Toàn server thất bại (Wipe) và Boss hồi 15% HP!">
              <img
                src={HEADER_ICON_ASSETS.greatAnvil}
                alt="Đại Đe"
                className="w-4 h-4 object-contain filter drop-shadow-[0_0_4px_#10B981] shrink-0"
              />
              <span className="truncate">
                Đe: <b className={`${serverAnvilHp < 2500 ? 'text-red-400 font-extrabold animate-pulse' : serverAnvilHp < 5000 ? 'text-amber-300' : 'text-emerald-300'}`}>{serverAnvilHp.toLocaleString('en-US')}</b>/10k
              </span>
            </div>

            {/* Meter 4: RCS & Burst */}
            <div className="flex items-center justify-end gap-1.5 shrink-0">
              <div className="flex items-center gap-1 text-amber-300" title="Điểm Cống Hiến Raid (RCS): Tích lũy từ Sát thương, Phá giáp, Bơm nhiệt và Hàn đe!">
                <img
                  src={HEADER_ICON_ASSETS.rcsMedal}
                  alt="RCS"
                  className="w-4 h-4 object-contain filter drop-shadow-[0_0_4px_#F59E0B] shrink-0"
                />
                <span className="font-bold">{formatInteger(raidContributionScore)}</span>
                <span className="text-[8px] text-amber-400/80">RCS</span>
              </div>'''

new_block = '''        {/* 2. Center Capsule: VÒM TRỜI THIẾT VÂN & WORLD RAID METERS */}
        <div
          aria-label="Thanh máu Vòm Trời & Trạng Thái World Raid"
          className="pointer-events-auto flex-1 min-w-0 max-w-2xl lg:max-w-3xl mx-auto px-3 sm:px-4 py-1.5 sm:py-2 rounded-2xl bg-[#060914]/92 border border-amber-500/40 shadow-[0_8px_30px_rgba(0,0,0,0.9)] backdrop-blur-md relative overflow-hidden"
        >
          <div className="absolute inset-0 bg-gradient-to-b from-amber-500/10 via-transparent to-black/40 pointer-events-none" />

          {/* Boss Title & HP Stats */}
          <div className="relative z-10 flex items-center justify-between gap-1.5 mb-1 min-w-0">
            <div className="flex items-center gap-1 sm:gap-1.5 min-w-0 flex-1">
              <span className="w-2 h-2 rounded-full bg-red-500 animate-pulse shrink-0 shadow-[0_0_6px_#EF4444]" />
              <span className="font-display text-[11px] sm:text-xs font-bold tracking-wider text-amber-300 uppercase truncate" title={bossName}>
                {bossName}
              </span>
              <span className="hidden xl:inline px-1.5 py-0.2 rounded bg-amber-500/20 border border-amber-500/40 text-[9px] font-tech text-amber-300 whitespace-nowrap shrink-0">
                {seal.shortName} (-{seal.damageReductionPct}%)
              </span>
            </div>

            <div className="font-tech text-[10px] sm:text-xs font-bold tabular-nums text-slate-200 whitespace-nowrap shrink-0 pl-1.5 flex items-center gap-1">
              <span className="text-red-400 font-extrabold">{safeHp.toLocaleString('en-US')}</span>
              <span className="text-slate-400 font-normal"> / {safeMax.toLocaleString('en-US')} HP</span>
              <span className="text-orange-400 font-semibold hidden lg:inline ml-0.5">(Nứt {crackPct.toFixed(1)}%)</span>
            </div>
          </div>

          {/* Ornate Dragon Jade HP Trough with Animated Ghost Bar */}
          <div className="relative z-10 h-5 sm:h-6 w-full flex items-center justify-center my-0.5">
            {/* Active Trough Background & Bars */}
            <div className="absolute inset-x-[3%] top-[30%] bottom-[28%] rounded-sm overflow-hidden bg-black/90 shadow-inner">
              {/* Visual Ghost Trail Bar (Máu tuột vàng rực) */}
              <div
                className="absolute inset-y-0 left-0 bg-gradient-to-r from-amber-200 via-amber-300 to-amber-500 shadow-[0_0_12px_#F59E0B] transition-all duration-300"
                style={{ width: `${effectiveTrailPct}%` }}
              />
              {/* Active HP Bar with Combat Hit Flash */}
              <div
                className={`absolute inset-y-0 left-0 bg-gradient-to-r from-red-600 via-orange-500 to-amber-400 transition-all duration-100 ${
                  isHitFlashing ? 'brightness-150 shadow-[0_0_14px_#FFF]' : 'shadow-[0_0_8px_#F59E0B]'
                }`}
                style={{ width: `${hpPct}%` }}
              />
            </div>
            {/* Dragon Jade Well Bezel Frame */}
            <img
              src={HEADER_FRAME_ASSETS.hpWell}
              alt="Dragon Jade Well"
              className="absolute inset-0 w-full h-full object-fill pointer-events-none z-20 drop-shadow-[0_0_6px_rgba(16,185,129,0.35)]"
            />
          </div>

          {/* World Raid v3.1 4-Meter HUD Row */}
          <div className="relative z-10 flex items-center justify-between text-[9px] sm:text-[10px] font-tech text-slate-300 mt-1.5 gap-1.5 sm:gap-2 pt-1 border-t border-slate-800/80 tabular-nums overflow-hidden">
            {/* Meter 1: Phá Giáp */}
            <div className="flex items-center gap-1 shrink-0" title="Thanh Phá Giáp Thiên Đạo: Bầu trời tự động hồi giáp mỗi giây!">
              <img
                src={HEADER_ICON_ASSETS.armorBreak}
                alt="Phá Giáp"
                className="w-3.5 h-3.5 object-contain filter drop-shadow-[0_0_4px_#A855F7] shrink-0"
              />
              {isShieldBroken ? (
                <span className="text-cyan-300 font-bold animate-pulse whitespace-nowrap">
                  VỠ GIÁP ({shieldBreakTimeLeft.toFixed(0)}s)
                </span>
              ) : (
                <span className="whitespace-nowrap">
                  Giáp: <b className="text-purple-300">{activeArmorBreakPoints}</b>/{armorBreakMaxPoints}
                  {isArmorRegenFrozen ? (
                    <span className="text-emerald-400 font-bold ml-0.5 text-[8px] sm:text-[9px]">(Băng hồi)</span>
                  ) : (
                    <span className="text-rose-400 font-semibold ml-0.5 text-[8px] sm:text-[9px]">(-{armorRegenRate}/s)</span>
                  )}
                </span>
              )}
            </div>

            {/* Meter 2: Đại Hỏa Hẩu */}
            <div className="flex items-center gap-1 shrink-0" title="Đại Hỏa Hẩu Toàn Server: Cần vượt ngưỡng để vòm trời nung chảy!">
              <img
                src={HEADER_ICON_ASSETS.furnaceHeat}
                alt="Hỏa Hẩu"
                className="w-3.5 h-3.5 object-contain filter drop-shadow-[0_0_4px_#F97316] shrink-0"
              />
              <span className="whitespace-nowrap">
                Lò: <b className="text-amber-300">{serverFurnaceHeat.toLocaleString('en-US')}°C</b>
              </span>
              {serverFurnaceHeat >= vaultMeltingThreshold ? (
                <span className="px-1 py-0.2 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-[8px] font-bold shrink-0">
                  🔥 Nung
                </span>
              ) : (
                <span className="px-1 py-0.2 rounded bg-cyan-500/20 text-cyan-300 border border-cyan-500/30 text-[8px] font-semibold shrink-0" title={`Cần đạt ${vaultMeltingThreshold}°C`}>
                  ❄️ Đông
                </span>
              )}
            </div>

            {/* Meter 3: Độ Bền Đại Đe */}
            <div className="flex items-center gap-1 shrink-0" title="Độ Bền Đại Đe Thần Server (10,000 HP). Vỡ đe = Toàn server thất bại (Wipe) và Boss hồi 15% HP!">
              <img
                src={HEADER_ICON_ASSETS.greatAnvil}
                alt="Đại Đe"
                className="w-3.5 h-3.5 object-contain filter drop-shadow-[0_0_4px_#10B981] shrink-0"
              />
              <span className="whitespace-nowrap">
                Đe: <b className={`${serverAnvilHp < 2500 ? 'text-red-400 font-extrabold animate-pulse' : serverAnvilHp < 5000 ? 'text-amber-300' : 'text-emerald-300'}`}>{serverAnvilHp.toLocaleString('en-US')}</b>/10k
              </span>
            </div>

            {/* Meter 4: RCS & Burst */}
            <div className="flex items-center justify-end gap-1 shrink-0">
              <div className="flex items-center gap-1 text-amber-300 whitespace-nowrap" title="Điểm Cống Hiến Raid (RCS): Tích lũy từ Sát thương, Phá giáp, Bơm nhiệt và Hàn đe!">
                <img
                  src={HEADER_ICON_ASSETS.rcsMedal}
                  alt="RCS"
                  className="w-3.5 h-3.5 object-contain filter drop-shadow-[0_0_4px_#F59E0B] shrink-0"
                />
                <span className="font-bold">{formatInteger(raidContributionScore)}</span>
                <span className="text-[8px] text-amber-400/80">RCS</span>
              </div>'''

if old_block in content:
    content = content.replace(old_block, new_block, 1)
    with open('frontend/src/components/TopBossHeader.tsx', 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS: TopBossHeader patched!")
else:
    print("ERROR: old_block not found!")
