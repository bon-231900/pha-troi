import React from 'react';
import { Volume2, VolumeX, Pause, RotateCcw, Zap, ShieldAlert } from 'lucide-react';
import { formatBillionsHP, formatCountdown } from '../game/rules';

interface TopBossHeaderProps {
  bossName: string;
  bossRealm: string;
  bossHpBillions: number;
  bossMaxHpBillions: number;
  bossTrailHpBillions: number;
  bossShieldPct: number;
  globalCountdownSec: number;
  globalSynergyPct: number;
  globalBurstActive: boolean;
  activeForgersCount: number;
  isOffline?: boolean;
  muted: boolean;
  onToggleMute: () => void;
  onPause: () => void;
  onRestart: () => void;
  onTriggerGlobalBurst: () => void;
}

export const TopBossHeader: React.FC<TopBossHeaderProps> = ({
  bossName,
  bossRealm,
  bossHpBillions,
  bossMaxHpBillions,
  bossTrailHpBillions,
  bossShieldPct,
  globalCountdownSec,
  globalSynergyPct,
  globalBurstActive,
  activeForgersCount,
  isOffline = false,
  muted,
  onToggleMute,
  onPause,
  onRestart,
  onTriggerGlobalBurst,
}) => {
  const hpPct = Math.max(0, Math.min(100, (bossHpBillions / bossMaxHpBillions) * 100));
  const trailPct = Math.max(hpPct, Math.min(100, (bossTrailHpBillions / bossMaxHpBillions) * 100));
  const shieldBroken = bossShieldPct <= 0;

  return (
    <section
      aria-label="Trạng thái Trùm và Cực Nhịp Toàn Cầu"
      className="w-full bg-[#111625] border-b border-slate-800/90 px-3 py-2.5 md:px-6 md:py-3 shrink-0"
    >
      <div className="max-w-[1440px] mx-auto flex flex-col gap-2">
        {/* Top Row: Boss Identity + HP Readout + Utility Controls */}
        <div className="flex flex-wrap items-center justify-between gap-2">
          <div className="flex items-center gap-3 min-w-0">
            <div className="flex flex-col">
              <div className="flex items-center gap-2">
                <h2 className="font-display font-bold text-sm sm:text-base md:text-lg text-amber-300 tracking-wide truncate">
                  {bossName}
                </h2>
                <span className="hidden sm:inline text-xs text-slate-400">·</span>
                <span className="hidden sm:inline text-xs text-slate-300 font-tech">
                  {bossRealm}
                </span>
                <span
                  className={`px-1.5 py-0.5 rounded text-[10px] font-mono font-bold flex items-center gap-1 border ${
                    isOffline
                      ? 'bg-amber-500/15 text-amber-300 border-amber-500/30'
                      : 'bg-emerald-500/15 text-emerald-300 border-emerald-500/30'
                  }`}
                  title={isOffline ? 'Chế độ Ngoại Tuyến (Chơi Đơn / Tự động đồng bộ)' : 'Đã kết nối Phân Khu Vạn Dân'}
                >
                  <span
                    className={`w-1.5 h-1.5 rounded-full ${
                      isOffline ? 'bg-amber-400' : 'bg-emerald-400 animate-pulse'
                    }`}
                  />
                  {isOffline ? 'ĐỘC HÀNH' : 'VẠN DÂN'}
                </span>
              </div>
              <div className="text-[11px] text-slate-400 font-tech flex items-center gap-2">
                <span>{activeForgersCount.toLocaleString('en-US')} Thợ Rèn Hợp Lực</span>
                <span>·</span>
                <span className={shieldBroken ? 'text-cyan-300 font-semibold' : 'text-amber-300'}>
                  {shieldBroken
                    ? 'GIÁP VỠ · SÁT THƯƠNG x1.5'
                    : `Giáp Năng Lượng: ${bossShieldPct.toFixed(1)}%`}
                </span>
              </div>
            </div>
          </div>

          {/* Right: Colossal HP Numeric Telemetry + Utility Buttons */}
          <div className="flex items-center gap-3 ml-auto">
            <div className="text-right font-tech">
              <div className="text-sm sm:text-base md:text-xl font-bold text-slate-100 leading-none">
                <span className="text-red-400">{formatBillionsHP(bossHpBillions)}</span>
                <span className="text-slate-500 text-xs md:text-sm">
                  {' '}
                  / {formatBillionsHP(bossMaxHpBillions)} HP
                </span>
              </div>
              <div className="text-[11px] text-amber-300 font-semibold">
                {hpPct.toFixed(2)}% Sinh Mệnh Còn Lại
              </div>
            </div>

            {/* Utility Controls */}
            <div className="flex items-center gap-1.5">
              <button
                type="button"
                tabIndex={-1}
                aria-label={muted ? 'Bật âm thanh [M]' : 'Tắt âm thanh [M]'}
                onClick={(e) => {
                  e.currentTarget.blur();
                  onToggleMute();
                }}
                className="w-9 h-9 md:w-10 md:h-10 rounded-lg bg-[#080A10] border border-slate-800 hover:border-amber-400/60 flex items-center justify-center text-slate-300 hover:text-amber-300 transition-colors cursor-pointer"
              >
                {muted ? <VolumeX className="w-4 h-4" /> : <Volume2 className="w-4 h-4" />}
              </button>
              <button
                type="button"
                tabIndex={-1}
                aria-label="Tạm dừng [P]"
                onClick={(e) => {
                  e.currentTarget.blur();
                  onPause();
                }}
                className="w-9 h-9 md:w-10 md:h-10 rounded-lg bg-[#080A10] border border-slate-800 hover:border-amber-400/60 flex items-center justify-center text-slate-300 hover:text-amber-300 transition-colors cursor-pointer"
              >
                <Pause className="w-4 h-4" />
              </button>
              <button
                type="button"
                tabIndex={-1}
                aria-label="Rèn lại từ đầu [R]"
                onClick={(e) => {
                  e.currentTarget.blur();
                  onRestart();
                }}
                className="w-9 h-9 md:w-10 md:h-10 rounded-lg bg-[#080A10] border border-slate-800 hover:border-amber-400/60 flex items-center justify-center text-slate-300 hover:text-amber-300 transition-colors cursor-pointer"
              >
                <RotateCcw className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>

        {/* Colossal Dual-Layer Boss Health Bar & Energy Shield Resonance */}
        <div className="flex flex-col gap-1.5">
          {/* Primary Boss HP Bar with 10% segment dividers */}
          <div className="relative h-4 md:h-5 w-full rounded-md bg-[#080A10] border border-slate-800 overflow-hidden">
            {/* Delayed Damage Ghost Bar */}
            <div
              className="absolute inset-y-0 left-0 bg-amber-300/40 transition-all duration-300"
              style={{ width: `${trailPct}%` }}
            />
            {/* Active Crimson Thiên Hỏa HP Bar */}
            <div
              className="
                absolute inset-y-0 left-0 transition-all duration-100
                bg-gradient-to-r from-[#FF3B30] via-[#FF6B00] to-[#FFD23F]
              "
              style={{ width: `${hpPct}%` }}
            />
            {/* 10% Segment Notches */}
            <div className="absolute inset-0 grid grid-cols-10 pointer-events-none">
              {Array.from({ length: 9 }).map((_, idx) => (
                <div key={idx} className="border-r border-slate-950/60 h-full" />
              ))}
            </div>
          </div>

          {/* Energy Shield Resonance Bar + Global Beat Bar in one compact ergonomic strip */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-2 items-center">
            {/* Energy Shield Bar */}
            <div className="flex items-center gap-2.5 bg-[#080A10] border border-slate-800/80 rounded-lg px-3 py-1.5">
              <ShieldAlert className="w-4 h-4 text-cyan-400 shrink-0" />
              <div className="text-xs font-tech text-slate-300 whitespace-nowrap shrink-0">
                Giáp Năng Lượng
              </div>
              <div className="relative flex-1 h-2 bg-slate-900 rounded-full overflow-hidden">
                <div
                  className="absolute inset-y-0 left-0 bg-gradient-to-r from-[#0099FF] to-[#00F0FF] transition-all duration-150"
                  style={{ width: `${bossShieldPct}%` }}
                />
              </div>
              <div className="text-xs font-tech font-semibold text-cyan-300 whitespace-nowrap shrink-0">
                {shieldBroken ? 'PHÁ VỠ!' : `${bossShieldPct.toFixed(0)}%`}
              </div>
            </div>

            {/* Global Beat Bar (Thanh Cực Nhịp Toàn Cầu 3-min Countdown + Synergy) */}
            <div
              className={`flex items-center gap-2.5 rounded-lg px-3 py-1.5 border transition-colors ${
                globalBurstActive
                  ? 'bg-amber-500/15 border-amber-400 text-amber-200'
                  : 'bg-[#080A10] border-slate-800/80 text-slate-300'
              }`}
            >
              <Zap
                className={`w-4 h-4 shrink-0 ${
                  globalBurstActive ? 'text-amber-300' : 'text-amber-400'
                }`}
              />
              <div className="text-xs font-tech whitespace-nowrap shrink-0">
                Cực Nhịp Toàn Cầu ·{' '}
                <span className="text-amber-300 font-bold">
                  {formatCountdown(globalCountdownSec)}
                </span>
              </div>
              <div className="relative flex-1 h-2 bg-slate-900 rounded-full overflow-hidden">
                <div
                  className="absolute inset-y-0 left-0 bg-gradient-to-r from-[#FFA000] to-[#FFD23F] transition-all duration-150"
                  style={{ width: `${Math.min(100, globalSynergyPct)}%` }}
                />
              </div>
              <button
                type="button"
                onClick={onTriggerGlobalBurst}
                disabled={globalSynergyPct < 100 && !globalBurstActive}
                className={`px-2.5 py-0.5 rounded text-[11px] font-tech font-bold whitespace-nowrap shrink-0 transition-all ${
                  globalBurstActive
                    ? 'bg-amber-400 text-slate-950'
                    : globalSynergyPct >= 100
                    ? 'bg-amber-400 hover:bg-amber-300 text-slate-950 cursor-pointer shadow-sm shadow-amber-400/40'
                    : 'bg-slate-800 text-slate-400'
                }`}
              >
                {globalBurstActive
                  ? 'BÙNG NỔ x2.5!'
                  : globalSynergyPct >= 100
                  ? 'HỢP LỰC NGAY'
                  : `${globalSynergyPct.toFixed(0)}%`}
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};
