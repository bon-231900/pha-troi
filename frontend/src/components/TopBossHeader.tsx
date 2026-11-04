import React from 'react';
import { Volume2, VolumeX, Pause, Shield, Hammer, Flame, Award, AlertTriangle } from 'lucide-react';
import { formatCountdown, AtmosphericSealLayer, getAtmosphericSealLayer, formatInteger } from '../game/rules';

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
      className="pointer-events-none fixed top-2 sm:top-2.5 inset-x-0 z-20 px-2 sm:px-5 flex items-center justify-between gap-2 select-none"
    >
      {/* 1. Left Floating Capsule: Toggle Thế Trận & Online Counter */}
      <div className="pointer-events-auto flex items-center gap-1.5">
        {onToggleLeftPanel && (
          <button
            type="button"
            onClick={onToggleLeftPanel}
            className={`flex items-center gap-1.5 px-2.5 py-1.5 rounded-xl backdrop-blur-md border text-xs font-tech font-bold tracking-wider cursor-pointer transition-all shadow-md ${
              leftPanelOpen
                ? 'bg-amber-400 text-slate-950 border-amber-300 shadow-amber-500/25'
                : 'bg-[#070B16]/85 hover:bg-slate-900 border-amber-500/30 text-amber-300 hover:text-amber-200'
            }`}
            title="Bật/Tắt Thế Trận & Cống Hiến [Phím [ ]"
          >
            <Shield className="w-3.5 h-3.5 text-cyan-400" />
            <span className="hidden sm:inline">Thế Trận</span>
          </button>
        )}

        <div className="hidden md:flex items-center gap-2 bg-[#070B16]/85 backdrop-blur-md border border-slate-800/90 px-2.5 py-1.5 rounded-xl font-tech text-xs text-slate-300 shadow-md">
          <span
            className={`w-2 h-2 rounded-full ${
              isOffline ? 'bg-amber-400' : 'bg-emerald-400 animate-pulse'
            }`}
          />
          <span className="font-bold text-amber-300">
            {activeForgersCount.toLocaleString('en-US')}
          </span>
          <span className="text-slate-400 text-[11px]">
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
        className="pointer-events-auto flex-1 max-w-md sm:max-w-xl md:max-w-2xl mx-auto bg-[#070A14]/90 border border-amber-500/40 px-3.5 py-1.5 rounded-xl shadow-[0_8px_25px_rgba(0,0,0,0.8)] backdrop-blur-md"
      >
        <div className="flex items-center justify-between gap-2 mb-1">
          <div className="flex items-center gap-1.5 shrink-0">
            <span className="w-2 h-2 rounded-full bg-red-500 animate-pulse shrink-0" />
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

        {/* Sleek 5px HP Track with Delayed Ghost Bar */}
        <div className="relative h-2 w-full bg-[#0D1322] border border-amber-500/30 rounded-full overflow-hidden">
          <div
            className="absolute inset-y-0 left-0 bg-amber-300/50 transition-all duration-300"
            style={{ width: `${trailPct}%` }}
          />
          <div
            className="absolute inset-y-0 left-0 bg-gradient-to-r from-red-600 via-orange-500 to-amber-400 transition-all duration-150"
            style={{ width: `${hpPct}%` }}
          />
        </div>

        {/* World Raid v3.1 3-Meter HUD Row */}
        <div className="grid grid-cols-2 sm:grid-cols-4 items-center justify-between text-[9px] sm:text-[10px] font-tech text-slate-400 mt-1.5 gap-1.5 pt-1 border-t border-slate-800/80 tabular-nums">
          {/* Meter 1: Phá Giáp (Active Armor Break vs Regen) */}
          <div className="flex items-center gap-1 truncate" title="Thanh Phá Giáp Thiên Đạo: Bầu trời tự động hồi giáp mỗi giây!">
            <Shield className="w-3 h-3 text-purple-400 shrink-0" />
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

          {/* Meter 2: Đại Hỏa Hẩu Vạn Dân (Server Heat vs Celestial Chill) */}
          <div className="flex items-center gap-1 truncate" title="Đại Hỏa Hẩu Toàn Server: Cần vượt ngưỡng để vòm trời nung chảy!">
            <Flame className="w-3 h-3 text-orange-400 shrink-0" />
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

          {/* Meter 3: Độ Bền Đại Đe Thần (Great Server Anvil) */}
          <div className="flex items-center gap-1 truncate" title="Độ Bền Đại Đe Thần Server (10,000 HP). Vỡ đe = Toàn server thất bại (Wipe) và Boss hồi 15% HP!">
            <Hammer className={`w-3 h-3 shrink-0 ${serverAnvilHp < 2500 ? 'text-red-500 animate-pulse' : serverAnvilHp < 5000 ? 'text-amber-400' : 'text-emerald-400'}`} />
            <span className="truncate">
              Đe: <b className={`${serverAnvilHp < 2500 ? 'text-red-400 font-extrabold animate-pulse' : serverAnvilHp < 5000 ? 'text-amber-300' : 'text-emerald-300'}`}>{serverAnvilHp.toLocaleString('en-US')}</b>/10k
            </span>
          </div>

          {/* Meter 4: Raid Contribution Score (RCS) & Global Burst */}
          <div className="flex items-center justify-end gap-1.5 shrink-0">
            <div className="flex items-center gap-0.5 text-amber-300" title="Điểm Cống Hiến Raid (RCS): Tích lũy từ Sát thương, Phá giáp, Bơm nhiệt và Hàn đe!">
              <Award className="w-3 h-3 text-amber-400 shrink-0" />
              <span className="font-bold">{formatInteger(raidContributionScore)}</span>
              <span className="text-[8px] text-amber-400/80">RCS</span>
            </div>

            {globalSynergyPct >= 100 || globalBurstActive ? (
              <button
                type="button"
                onClick={onTriggerGlobalBurst}
                className="px-1.5 py-0.2 rounded bg-amber-400 text-slate-950 font-bold text-[8px] sm:text-[9px] cursor-pointer animate-pulse shrink-0"
              >
                {globalBurstActive ? 'BÙNG NỔ!' : 'KÍCH HOẠT'}
              </button>
            ) : null}
          </div>
        </div>

        {/* Phase Check Alert (Tứ Trụ Khai Thiên) */}
        {phaseCheckActive && (
          <div className="mt-1.5 py-0.5 px-2 rounded-lg bg-red-950/80 border border-amber-500/60 flex items-center justify-center gap-1.5 text-amber-300 text-[9px] sm:text-[10px] font-tech font-bold animate-pulse shadow-md">
            <AlertTriangle className="w-3 h-3 text-amber-400 shrink-0" />
            <span>[TỨ TRỤ KHAI THIÊN] Thiên Đạo Phán Quyết ({phaseCheckTimeLeft}s) — Hợp Lực 4 Phường Rèn!</span>
          </div>
        )}
      </div>

      {/* 3. Right Floating Capsule: Utilities + Toggle Lò Rèn */}
      <div className="pointer-events-auto flex items-center gap-1.5">
        <div className="flex items-center gap-0.5 sm:gap-1 bg-[#070B16]/85 backdrop-blur-md border border-slate-800/90 p-1 rounded-xl shadow-md">
          <button
            type="button"
            tabIndex={-1}
            aria-label={muted ? 'Bật âm thanh [M]' : 'Tắt âm thanh [M]'}
            onClick={(e) => {
              e.currentTarget.blur();
              onToggleMute();
            }}
            className="w-7 h-7 sm:w-8 sm:h-8 rounded-lg hover:bg-slate-800 flex items-center justify-center text-slate-300 hover:text-amber-300 transition-colors cursor-pointer"
          >
            {muted ? <VolumeX className="w-3.5 h-3.5" /> : <Volume2 className="w-3.5 h-3.5" />}
          </button>

          <button
            type="button"
            tabIndex={-1}
            aria-label="Tạm dừng lò rèn [P]"
            onClick={(e) => {
              e.currentTarget.blur();
              onPause();
            }}
            className="w-7 h-7 sm:w-8 sm:h-8 rounded-lg hover:bg-slate-800 flex items-center justify-center text-slate-300 hover:text-amber-300 transition-colors cursor-pointer"
          >
            <Pause className="w-3.5 h-3.5" />
          </button>
        </div>

        {onToggleRightPanel && (
          <button
            type="button"
            onClick={onToggleRightPanel}
            className={`flex items-center gap-1.5 px-2.5 py-1.5 rounded-xl backdrop-blur-md border text-xs font-tech font-bold tracking-wider cursor-pointer transition-all shadow-md ${
              rightPanelOpen
                ? 'bg-amber-400 text-slate-950 border-amber-300 shadow-amber-500/25'
                : 'bg-[#070B16]/85 hover:bg-slate-900 border-amber-500/30 text-amber-300 hover:text-amber-200'
            }`}
            title="Bật/Tắt Lò Rèn & Thần Hồn [Phím ] ]"
          >
            <Hammer className="w-3.5 h-3.5 text-amber-400" />
            <span className="hidden sm:inline">Lò Rèn</span>
          </button>
        )}
      </div>
    </header>
  );
};
