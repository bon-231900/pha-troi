import React from 'react';
import { Volume2, VolumeX, Pause, RotateCcw, Shield, Hammer, Flame } from 'lucide-react';
import { formatCountdown, AtmosphericSealLayer, getAtmosphericSealLayer } from '../game/rules';

export interface TopBossHeaderProps {
  bossName?: string;
  bossRealm?: string;
  bossHp: number; // Integer HP (e.g. 500,000,000)
  bossMaxHp: number;
  bossTrailHp: number;
  bossShieldPct: number;
  globalCountdownSec: number;
  globalSynergyPct: number;
  globalBurstActive: boolean;
  activeForgersCount: number;
  isOffline?: boolean;
  anvilHeat?: number; // 100 - 1000°C
  resonanceStrikes?: number; // 0 - 50
  isShieldBroken?: boolean;
  shieldBreakTimeLeft?: number;
  currentSealLayer?: AtmosphericSealLayer;
  muted: boolean;
  onToggleMute: () => void;
  onPause: () => void;
  onRestart: () => void;
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
  anvilHeat = 100,
  resonanceStrikes = 0,
  isShieldBroken = false,
  shieldBreakTimeLeft = 0,
  currentSealLayer,
  muted,
  onToggleMute,
  onPause,
  onRestart,
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
  const heatBonusPct = Math.min(45, Math.floor((Math.max(100, anvilHeat) - 100) / 100) * 5);

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
            {isOffline ? 'Độc Hành' : 'Vạn Dân'}
          </span>
        </div>
      </div>

      {/* 2. Center Capsule: VÒM TRỜI THIẾT VÂN (Ultra-Compact Floating Bar - Zero Sky Obstruction) */}
      <div
        aria-label="Thanh máu Vòm Trời Thiết Vân"
        className="pointer-events-auto flex-1 max-w-sm sm:max-w-lg mx-auto bg-[#070A14]/90 border border-amber-500/40 px-3 py-1.5 rounded-xl shadow-[0_8px_25px_rgba(0,0,0,0.8)] backdrop-blur-md"
      >
        <div className="flex items-center justify-between gap-2 mb-1">
          <div className="flex items-center gap-1.5 min-w-0">
            <span className="w-2 h-2 rounded-full bg-red-500 animate-pulse shrink-0" />
            <span className="font-display text-[11px] sm:text-xs font-bold tracking-wider text-amber-300 uppercase truncate">
              {bossName}
            </span>
            <span className="hidden sm:inline px-1.5 py-0.2 rounded bg-amber-500/20 border border-amber-500/40 text-[9px] font-tech text-amber-300">
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

        {/* Micro Sub-indicators: Heat, Resonance & Synergy in 1 compact row */}
        <div className="flex items-center justify-between text-[9px] sm:text-[10px] font-tech text-slate-400 mt-1 tabular-nums gap-1">
          {/* Anvil Heat indicator */}
          <div className="flex items-center gap-1 text-amber-300">
            <Flame className="w-3 h-3 text-orange-400" />
            <span>Hỏa Hầu: {anvilHeat}°C</span>
            {heatBonusPct > 0 && (
              <span className="text-emerald-400 font-bold">(+{heatBonusPct}%)</span>
            )}
          </div>

          {/* Phá Giáp Resonance indicator */}
          <div className="flex items-center gap-1">
            {isShieldBroken ? (
              <span className="text-cyan-300 font-bold animate-pulse">
                VỠ GIÁP ({shieldBreakTimeLeft.toFixed(0)}s) x1.5 DMG!
              </span>
            ) : (
              <span className="text-slate-400">
                Phá Giáp: <span className="text-amber-300 font-bold">{resonanceStrikes}</span>/50
              </span>
            )}
          </div>

          {/* Cực nhịp / Global Burst */}
          <div className="flex items-center gap-1">
            <span>Cực nhịp: {formatCountdown(globalCountdownSec)}</span>
            {globalSynergyPct >= 100 || globalBurstActive ? (
              <button
                type="button"
                onClick={onTriggerGlobalBurst}
                className="px-1.5 py-0.2 rounded bg-amber-400 text-slate-950 font-bold text-[9px] cursor-pointer animate-pulse"
              >
                {globalBurstActive ? 'BÙNG NỔ!' : 'KÍCH HOẠT'}
              </button>
            ) : (
              <span className="text-amber-400/80">({globalSynergyPct.toFixed(0)}%)</span>
            )}
          </div>
        </div>
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

          <button
            type="button"
            tabIndex={-1}
            aria-label="Rèn lại từ đầu [R]"
            onClick={(e) => {
              e.currentTarget.blur();
              onRestart();
            }}
            className="w-7 h-7 sm:w-8 sm:h-8 rounded-lg hover:bg-slate-800 flex items-center justify-center text-slate-300 hover:text-amber-300 transition-colors cursor-pointer"
          >
            <RotateCcw className="w-3.5 h-3.5" />
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