import React from 'react';
import { AtmosphericSealLayer, getAtmosphericSealLayer, formatInteger } from '../game/rules';
import { GoogleUserProfile } from '../game/googleAuth';
import { PlayerClassMeta } from '../game/rules';
import { HEADER_FRAME_ASSETS, HEADER_ICON_ASSETS } from '../game/headerArtAssets';

export interface TopBossHeaderProps {
  bossName?: string;
  bossRealm?: string;
  bossHp: number; // Integer HP (e.g. 1,500,000,000)
  bossMaxHp: number;
  bossTrailHp: number;
  bossShieldPct: number;
  globalCountdownSec: number;
  globalSynergyPct: number;
  globalBurstActive: boolean;
  activeForgersCount: number;
  isCloudflareServerOnline?: boolean;
  isOffline?: boolean;
  realOnlinePeersCount?: number;
  anvilHeat?: number; // 100 - 1000°C (local)
  resonanceStrikes?: number; // legacy fallback
  isShieldBroken?: boolean;
  shieldBreakTimeLeft?: number;
  currentSealLayer?: AtmosphericSealLayer;
  // v3.1 World Raid additions
  serverFurnaceHeat?: number; // 0 - 10,000°C
  vaultMeltingThreshold?: number; // e.g. 1,500 - 8,800°C
  serverChillRate?: number; // e.g. -60°C/s
  serverAnvilHp?: number; // 0 - 10,000 HP
  serverAnvilMaxHp?: number; // 10,000 HP
  activeArmorBreakPoints?: number; // 0 - armorBreakMaxPoints
  armorBreakMaxPoints?: number; // e.g. 500
  armorRegenRate?: number; // e.g. 15/s
  isArmorRegenFrozen?: boolean;
  raidContributionScore?: number;
  phaseCheckActive?: boolean;
  phaseCheckTimeLeft?: number;
  muted: boolean;
  onToggleMute: () => void;
  onPause: () => void;
  onTriggerGlobalBurst: () => void;
  leftPanelOpen?: boolean;
  onToggleLeftPanel?: () => void;
  rightPanelOpen?: boolean;
  onToggleRightPanel?: () => void;
  googleProfile?: GoogleUserProfile | null;
  onGoogleLogin?: () => void;
  onGoogleLogout?: () => void;
  playerClass?: PlayerClassMeta;
  onSwitchCharacter?: () => void;
}

export const TopBossHeader: React.FC<TopBossHeaderProps> = ({
  bossName = 'Vòm Trời Thiết Vân · Tầng 1',
  bossHp,
  bossMaxHp,
  bossTrailHp,
  bossShieldPct,
  globalCountdownSec,
  globalSynergyPct,
  globalBurstActive,
  activeForgersCount,
  isCloudflareServerOnline = false,
  isOffline = false,
  realOnlinePeersCount = 0,
  anvilHeat = 100,
  resonanceStrikes = 0,
  isShieldBroken = false,
  shieldBreakTimeLeft = 0,
  currentSealLayer,
  serverFurnaceHeat = 1500,
  vaultMeltingThreshold = 1500,
  serverChillRate = -60,
  serverAnvilHp = 10000,
  serverAnvilMaxHp = 10000,
  activeArmorBreakPoints = 0,
  armorBreakMaxPoints = 500,
  armorRegenRate = 15,
  isArmorRegenFrozen = false,
  raidContributionScore = 0,
  phaseCheckActive = false,
  phaseCheckTimeLeft = 30,
  muted,
  onToggleMute,
  onPause,
  onTriggerGlobalBurst,
  leftPanelOpen = false,
  onToggleLeftPanel,
  rightPanelOpen = false,
  onToggleRightPanel,
  googleProfile = null,
  onGoogleLogin,
  onGoogleLogout,
  playerClass,
  onSwitchCharacter,
}) => {
  const safeMax = Math.max(1, bossMaxHp);
  const safeHp = Math.max(0, Math.min(safeMax, bossHp));
  const hpPct = Math.max(0, Math.min(100, (safeHp / safeMax) * 100));
  const trailPct = Math.max(hpPct, Math.min(100, (bossTrailHp / safeMax) * 100));
  const crackPct = Math.max(0, Math.min(100, 100 - hpPct));

  const seal = currentSealLayer || getAtmosphericSealLayer(safeHp, safeMax);

  return (
    <header
      aria-label="Trạng thái Vòm Trời Thiên Cấm"
      className="pointer-events-none fixed top-1 sm:top-2.5 inset-x-0 z-20 px-2 sm:px-5 pt-safe flex flex-col items-center select-none"
    >
      {/* ------------------------------------------------------------- */}
      {/* MOBILE COMPACT HEADER (< 768px): Zero-Overflow, 1-Hand Friendly */}
      {/* ------------------------------------------------------------- */}
      <div className="flex md:hidden flex-col gap-1 w-full pointer-events-auto bg-[#070A14]/95 border border-amber-500/40 px-2.5 py-1.5 rounded-2xl shadow-2xl backdrop-blur-md">
        {/* Row 1: Actions Left + Boss HP Center + Actions Right */}
        <div className="flex items-center justify-between gap-2">
          {/* Left Actions: Thế Trận + Đổi Tu Sĩ */}
          <div className="flex items-center gap-1 shrink-0">
            {onToggleLeftPanel && (
              <button
                type="button"
                onClick={onToggleLeftPanel}
                className={`p-1.5 rounded-lg border text-xs font-tech font-bold cursor-pointer transition-all ${
                  leftPanelOpen
                    ? 'bg-amber-400 text-slate-950 border-amber-300'
                    : 'bg-slate-900/90 border-amber-500/30 text-amber-300'
                }`}
                title="Bật/Tắt Thế Trận & Cống Hiến"
              >
                <img
                  src={HEADER_ICON_ASSETS.battleArray}
                  alt="Thế Trận"
                  className="w-4 h-4 object-contain filter drop-shadow-[0_0_4px_#06B6D4]"
                />
              </button>
            )}

            {playerClass && onSwitchCharacter && (
              <button
                type="button"
                onClick={onSwitchCharacter}
                className={`flex items-center gap-1 px-1.5 py-1 rounded-lg text-[10px] font-tech font-bold border cursor-pointer active:scale-95 ${playerClass.badgeBg}`}
                title="Đổi Tu Sĩ (3 Slots)"
              >
                <span>{playerClass.icon}</span>
                <span className="truncate max-w-[60px]">{playerClass.name}</span>
              </button>
            )}
          </div>

          {/* Center: Boss Title & HP % */}
          <div className="flex-1 min-w-0 flex flex-col items-center justify-center">
            <div className="flex items-center gap-1 text-[10px] font-display font-bold text-amber-200 truncate max-w-full justify-center">
              <span className="w-1.5 h-1.5 rounded-full bg-red-500 animate-pulse shrink-0 shadow-[0_0_4px_#EF4444]" />
              <span className="truncate">{bossName}</span>
            </div>
            <div className="text-[10px] font-tech font-bold text-red-400 tabular-nums">
              {hpPct.toFixed(1)}% <span className="text-slate-400 font-normal">({safeHp >= 1e9 ? `${(safeHp / 1e9).toFixed(2)}B` : `${(safeHp / 1e6).toFixed(1)}M`} HP)</span>
            </div>
          </div>

          {/* Right Actions: Mute + Lò Rèn */}
          <div className="flex items-center gap-1 shrink-0">
            <button
              type="button"
              onClick={onToggleMute}
              className="p-1 rounded-lg bg-slate-900/90 border border-slate-800 text-slate-300 cursor-pointer"
              title={muted ? 'Bật âm thanh' : 'Tắt âm thanh'}
            >
              <img
                src={muted ? HEADER_ICON_ASSETS.soundOff : HEADER_ICON_ASSETS.soundOn}
                alt="Sound"
                className="w-4 h-4 object-contain"
              />
            </button>

            {onToggleRightPanel && (
              <button
                type="button"
                onClick={onToggleRightPanel}
                className={`flex items-center gap-1 px-2 py-1 rounded-lg border text-xs font-tech font-bold cursor-pointer transition-all shadow-md ${
                  rightPanelOpen
                    ? 'bg-amber-400 text-slate-950 border-amber-300'
                    : 'bg-amber-500/20 border-amber-500/60 text-amber-300'
                }`}
                title="Lò Rèn, Vũ Khí & Thần Hồn"
              >
                <img
                  src={HEADER_ICON_ASSETS.forgeHammer}
                  alt="Lò Rèn"
                  className="w-3.5 h-3.5 object-contain filter drop-shadow-[0_0_4px_#F59E0B]"
                />
                <span className="text-[10px] font-bold">Lò Rèn</span>
              </button>
            )}
          </div>
        </div>

        {/* Row 2: Sleek Dragon Jade HP Track */}
        <div className="relative h-3 w-full flex items-center justify-center my-0.5">
          <img
            src={HEADER_FRAME_ASSETS.hpWell}
            alt="HP Well"
            className="absolute inset-0 w-full h-full object-fill pointer-events-none z-10 drop-shadow-[0_0_4px_rgba(16,185,129,0.3)]"
          />
          <div className="relative w-[94%] h-1.5 rounded-full overflow-hidden bg-black/85">
            <div
              className="absolute inset-y-0 left-0 bg-amber-300/40 transition-all duration-300"
              style={{ width: `${trailPct}%` }}
            />
            <div
              className="absolute inset-y-0 left-0 bg-gradient-to-r from-red-600 via-orange-500 to-amber-400 transition-all duration-150"
              style={{ width: `${hpPct}%` }}
            />
          </div>
        </div>

        {/* Row 3: World Raid Mini Ticker */}
        <div className="flex items-center justify-between text-[9px] font-tech text-slate-400 pt-0.5 tabular-nums">
          <span className="flex items-center gap-1">
            <img src={HEADER_ICON_ASSETS.armorBreak} alt="Giáp" className="w-3 h-3 object-contain shrink-0" />
            {isShieldBroken ? (
              <b className="text-cyan-300">VỠ GIÁP ({shieldBreakTimeLeft.toFixed(0)}s)</b>
            ) : (
              <span>Giáp: <b className="text-purple-300">{activeArmorBreakPoints}</b>/{armorBreakMaxPoints}</span>
            )}
          </span>
          <span className="flex items-center gap-1">
            <img src={HEADER_ICON_ASSETS.furnaceHeat} alt="Lò" className="w-3 h-3 object-contain shrink-0" />
            Lò: <b className="text-amber-300">{serverFurnaceHeat}°C</b>
          </span>
          <span className="flex items-center gap-1">
            <img src={HEADER_ICON_ASSETS.greatAnvil} alt="Đe" className="w-3 h-3 object-contain shrink-0" />
            Đe: <b className="text-emerald-300">{serverAnvilHp}</b>/10k
          </span>
          <span className="flex items-center gap-1 text-amber-300 font-bold">
            <img src={HEADER_ICON_ASSETS.rcsMedal} alt="RCS" className="w-3 h-3 object-contain shrink-0" />
            {formatInteger(raidContributionScore)}
          </span>
        </div>
      </div>

      {/* ------------------------------------------------------------- */}
      {/* DESKTOP FULL HEADER (>= 768px): 3 Independent Floating Capsules */}
      {/* ------------------------------------------------------------- */}
      <div className="hidden md:flex items-center justify-between gap-3 w-full">
        {/* 1. Left Floating Capsule: Toggle Thế Trận & Online Counter */}
        <div className="pointer-events-auto flex items-center gap-2">
          {onToggleLeftPanel && (
            <button
              type="button"
              onClick={onToggleLeftPanel}
              className="relative flex items-center gap-1.5 px-3.5 py-2 rounded-xl select-none cursor-pointer group transition-all hover:brightness-125 active:scale-95 shadow-md overflow-hidden text-xs font-tech font-bold"
              title="Bật/Tắt Thế Trận & Cống Hiến [Phím [ ]"
            >
              <img
                src={leftPanelOpen ? HEADER_FRAME_ASSETS.tokenActive : HEADER_FRAME_ASSETS.tokenIdle}
                alt="Frame"
                className="absolute inset-0 w-full h-full object-fill pointer-events-none drop-shadow"
              />
              <img
                src={HEADER_ICON_ASSETS.battleArray}
                alt="Thế Trận"
                className="relative z-10 w-4 h-4 object-contain filter drop-shadow-[0_0_6px_#06B6D4] group-hover:scale-110 transition-transform"
              />
              <span className="relative z-10 text-amber-200 tracking-wider hidden sm:inline drop-shadow">
                Thế Trận
              </span>
            </button>
          )}

          <div className="hidden md:flex items-center gap-2 bg-[#070B16]/90 backdrop-blur-md border border-slate-800/90 px-3 py-1.5 rounded-xl font-tech text-xs text-slate-300 shadow-md">
            <img
              src={HEADER_ICON_ASSETS.cloudServer}
              alt="Server Seal"
              className="w-4 h-4 object-contain filter drop-shadow"
            />
            <span
              className={`w-2 h-2 rounded-full ${
                isOffline ? 'bg-amber-400' : 'bg-emerald-400 animate-pulse shadow-[0_0_6px_#34D399]'
              }`}
            />
            <span className="font-bold text-amber-300">
              {activeForgersCount.toLocaleString('en-US')}
            </span>
            <span className="text-slate-400 text-[11px]">
              {isCloudflareServerOnline && (
                <span className="text-emerald-400 font-bold bg-emerald-950/80 border border-emerald-500/40 px-1 py-0.5 rounded text-[10px] tracking-wide mr-1" title="Đã kết nối Serverless Cloudflare Edge API">
                  SERVER
                </span>
              )}
              {realOnlinePeersCount > 0 ? (
                <span className="text-cyan-400 font-bold">({realOnlinePeersCount + 1} Đồng Môn P2P)</span>
              ) : isOffline ? (
                'Độc Hành'
              ) : (
                'Vạn Dân'
              )}
            </span>
          </div>
        </div>

        {/* 2. Center Capsule: VÒM TRỜI THIẾT VÂN & WORLD RAID METERS */}
        <div
          aria-label="Thanh máu Vòm Trời & Trạng Thái World Raid"
          className="pointer-events-auto flex-1 max-w-md sm:max-w-xl md:max-w-2xl mx-auto px-4 py-2 rounded-2xl bg-[#060914]/92 border border-amber-500/40 shadow-[0_8px_30px_rgba(0,0,0,0.9)] backdrop-blur-md relative overflow-hidden"
        >
          <div className="absolute inset-0 bg-gradient-to-b from-amber-500/10 via-transparent to-black/40 pointer-events-none" />

          {/* Boss Title & HP Stats */}
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
          </div>

          {/* Ornate Dragon Jade HP Trough with Animated Ghost Bar */}
          <div className="relative z-10 h-4.5 sm:h-5 w-full flex items-center justify-center my-0.5">
            <img
              src={HEADER_FRAME_ASSETS.hpWell}
              alt="Dragon Jade Well"
              className="absolute inset-0 w-full h-full object-fill pointer-events-none z-10 drop-shadow-[0_0_6px_rgba(16,185,129,0.35)]"
            />
            <div className="relative w-[94%] h-2 sm:h-2.5 rounded-full overflow-hidden bg-black/85">
              <div
                className="absolute inset-y-0 left-0 bg-amber-300/45 transition-all duration-300"
                style={{ width: `${trailPct}%` }}
              />
              <div
                className="absolute inset-y-0 left-0 bg-gradient-to-r from-red-600 via-orange-500 to-amber-400 transition-all duration-150 shadow-[0_0_8px_#F59E0B]"
                style={{ width: `${hpPct}%` }}
              />
            </div>
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
              <span className="truncate">
                Lò: <b className="text-amber-300">{serverFurnaceHeat.toLocaleString('en-US')}°C</b>
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
              </div>

              {globalSynergyPct >= 100 || globalBurstActive ? (
                <button
                  type="button"
                  onClick={onTriggerGlobalBurst}
                  className="relative flex items-center gap-1 px-2 py-0.5 rounded bg-gradient-to-r from-amber-500 to-red-600 border border-amber-300 text-white font-bold text-[8px] sm:text-[9px] cursor-pointer animate-pulse shrink-0 shadow-[0_0_10px_#F59E0B]"
                >
                  <img src={HEADER_ICON_ASSETS.burstBadge} alt="Burst" className="w-3 h-3 object-contain" />
                  <span>{globalBurstActive ? 'BÙNG NỔ!' : 'KÍCH HOẠT'}</span>
                </button>
              ) : null}
            </div>
          </div>

          {/* Phase Check Alert (Tứ Trụ Khai Thiên) */}
          {phaseCheckActive && (
            <div className="relative z-10 mt-1.5 py-0.5 px-2 rounded-lg bg-red-950/80 border border-amber-500/60 flex items-center justify-center gap-1.5 text-amber-300 text-[9px] sm:text-[10px] font-tech font-bold animate-pulse shadow-md">
              <img src={HEADER_ICON_ASSETS.burstBadge} alt="Alert" className="w-3.5 h-3.5 object-contain shrink-0" />
              <span>[TỨ TRỤ KHAI THIÊN] Thiên Đạo Phán Quyết ({phaseCheckTimeLeft}s) — Hợp Lực 4 Phường Rèn!</span>
            </div>
          )}
        </div>

        {/* 3. Right Floating Capsule: Utilities + Toggle Lò Rèn */}
        <div className="pointer-events-auto flex items-center gap-2">
          {/* Player Class / Sect Commitment Badge -> Clickable to Switch Characters (3 Slots) */}
          {playerClass && (
            <button
              type="button"
              onClick={onSwitchCharacter}
              className="relative flex items-center gap-1.5 px-3 py-1.5 rounded-xl select-none cursor-pointer group transition-all hover:brightness-125 active:scale-95 shadow-md overflow-hidden text-xs font-tech font-bold"
              title="Bấm để Đổi Tu Sĩ / Quản lý 3 Slot & Trải nghiệm Bệ Đá Bát Quái Nện Thử Búa"
            >
              <img
                src={HEADER_FRAME_ASSETS.tokenIdle}
                alt="Frame"
                className="absolute inset-0 w-full h-full object-fill pointer-events-none drop-shadow"
              />
              <span className="relative z-10 text-sm filter drop-shadow">{playerClass.icon}</span>
              <span className="relative z-10 font-bold text-amber-200 drop-shadow">{playerClass.name}</span>
              <span className="relative z-10 text-[10px] text-amber-400 border-l border-amber-500/40 pl-1.5 font-bold">
                ĐỔI TU SĨ ▾
              </span>
            </button>
          )}

          {/* Google Cloud Save Button or User Profile */}
          {googleProfile ? (
            <div className="flex items-center gap-1.5 bg-[#070B16]/90 backdrop-blur-md border border-emerald-500/40 px-2.5 py-1.5 rounded-xl text-xs font-tech text-slate-200 shadow-md">
              {googleProfile.avatar ? (
                <img src={googleProfile.avatar} alt="Avatar" className="w-5 h-5 rounded-full border border-emerald-400/50" />
              ) : (
                <span className="w-5 h-5 rounded-full bg-emerald-700 text-white flex items-center justify-center text-[10px] font-bold">
                  {googleProfile.name.charAt(0)}
                </span>
              )}
              <span className="hidden sm:inline font-bold text-emerald-300 max-w-[80px] truncate" title={googleProfile.email}>
                {googleProfile.name}
              </span>
              <span className="flex items-center gap-1 text-[10px] text-emerald-400 bg-emerald-950/80 px-1 py-0.5 rounded border border-emerald-500/30" title="Tiến độ đã tự động lưu lên Cloudflare D1">
                <img src={HEADER_ICON_ASSETS.cloudServer} alt="Cloud" className="w-3 h-3 object-contain" />
                Đã Lưu
              </span>
              {onGoogleLogout && (
                <button
                  type="button"
                  onClick={onGoogleLogout}
                  className="text-slate-400 hover:text-red-400 text-xs ml-0.5 transition cursor-pointer"
                  title="Đăng xuất tài khoản Google"
                >
                  ✕
                </button>
              )}
            </div>
          ) : onGoogleLogin ? (
            <button
              type="button"
              onClick={onGoogleLogin}
              className="flex items-center gap-1.5 bg-gradient-to-r from-[#0d1527] to-[#121c35] hover:from-slate-800 hover:to-slate-700 border border-cyan-500/40 hover:border-cyan-400/70 px-2.5 py-1.5 rounded-xl text-xs font-tech font-bold text-cyan-300 shadow-md transition-all cursor-pointer group"
              title="Đăng nhập Google để lưu trữ túi đồ và búa rèn vĩnh viễn trên mây"
            >
              <svg className="w-3.5 h-3.5" viewBox="0 0 24 24">
                <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" />
                <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" />
                <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z" />
                <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z" />
              </svg>
              <span className="hidden sm:inline group-hover:text-cyan-200">Đăng Nhập</span>
            </button>
          ) : null}

          {/* Sound Mute & Pause Utility Cluster */}
          <div className="flex items-center gap-0.5 sm:gap-1 bg-[#070B16]/90 backdrop-blur-md border border-slate-800/90 p-1 rounded-xl shadow-md">
            <button
              type="button"
              tabIndex={-1}
              aria-label={muted ? 'Bật âm thanh [M]' : 'Tắt âm thanh [M]'}
              onClick={(e) => {
                e.currentTarget.blur();
                onToggleMute();
              }}
              className="w-7 h-7 sm:w-8 sm:h-8 rounded-lg hover:bg-amber-500/10 flex items-center justify-center transition-all cursor-pointer group"
            >
              <img
                src={muted ? HEADER_ICON_ASSETS.soundOff : HEADER_ICON_ASSETS.soundOn}
                alt={muted ? 'Muted' : 'Sound On'}
                className="w-4 h-4 object-contain filter drop-shadow group-hover:scale-110 transition-transform"
              />
            </button>

            <button
              type="button"
              tabIndex={-1}
              aria-label="Tạm dừng lò rèn [P]"
              onClick={(e) => {
                e.currentTarget.blur();
                onPause();
              }}
              className="w-7 h-7 sm:w-8 sm:h-8 rounded-lg hover:bg-amber-500/10 flex items-center justify-center transition-all cursor-pointer group"
            >
              <img
                src={HEADER_ICON_ASSETS.pauseTalisman}
                alt="Pause"
                className="w-4 h-4 object-contain filter drop-shadow-[0_0_4px_#F59E0B] group-hover:scale-110 transition-transform"
              />
            </button>
          </div>

          {/* Lò Rèn Toggle Button */}
          {onToggleRightPanel && (
            <button
              type="button"
              onClick={onToggleRightPanel}
              className="relative flex items-center gap-1.5 px-3.5 py-2 rounded-xl select-none cursor-pointer group transition-all hover:brightness-125 active:scale-95 shadow-md overflow-hidden text-xs font-tech font-bold"
              title="Bật/Tắt Lò Rèn & Thần Hồn [Phím ] ]"
            >
              <img
                src={rightPanelOpen ? HEADER_FRAME_ASSETS.tokenActive : HEADER_FRAME_ASSETS.tokenIdle}
                alt="Frame"
                className="absolute inset-0 w-full h-full object-fill pointer-events-none drop-shadow"
              />
              <img
                src={HEADER_ICON_ASSETS.forgeHammer}
                alt="Lò Rèn"
                className="relative z-10 w-4 h-4 object-contain filter drop-shadow-[0_0_6px_#F59E0B] group-hover:scale-110 transition-transform"
              />
              <span className="relative z-10 text-amber-200 tracking-wider hidden sm:inline drop-shadow">
                Lò Rèn
              </span>
            </button>
          )}
        </div>
      </div>
    </header>
  );
};
