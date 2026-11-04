import React from 'react';
import {
  PlayerClassMeta,
  getOverdriveTier,
  OVERDRIVE_MAX,
  OVERDRIVE_TOTAL_CAP,
} from '../game/rules';
import { Zap, Flame, Mountain, Music, Sparkles, Shield, Clock, AlertCircle } from 'lucide-react';

interface ClassSkillBarProps {
  playerClass: PlayerClassMeta;
  overdriveCharge: number;
  overdriveActive: boolean;
  overdriveTimeLeft: number;
  totalForgeLevel: number;
  cooldowns: {
    W: number; // seconds left
    E: number;
    R: number;
  };
  onCastSkill: (slotKey: 'W' | 'E' | 'R') => void;
  onOpenClassSelect?: () => void;
  hudVisible?: boolean;
}

export const ClassSkillBar: React.FC<ClassSkillBarProps> = ({
  playerClass,
  overdriveCharge,
  overdriveActive,
  overdriveTimeLeft,
  totalForgeLevel,
  cooldowns,
  onCastSkill,
  onOpenClassSelect,
  hudVisible = true,
}) => {
  const tierInfo = getOverdriveTier(overdriveCharge);

  const isSkillUnlocked = (unlockLevel: number) => {
    return totalForgeLevel >= unlockLevel;
  };

  const canCastW = isSkillUnlocked(playerClass.skills.W.unlockLevel) && cooldowns.W <= 0;
  const canCastE = isSkillUnlocked(playerClass.skills.E.unlockLevel) && overdriveCharge >= 8 && cooldowns.E <= 0;
  const canCastR = isSkillUnlocked(playerClass.skills.R.unlockLevel) && overdriveCharge >= 16 && cooldowns.R <= 0;

  return (
    <div
      className={`fixed bottom-3 left-3 sm:left-5 z-20 flex flex-col gap-1.5 pointer-events-auto max-w-[320px] sm:max-w-[400px] transition-all duration-300 ${
        hudVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-6 pointer-events-none'
      }`}
    >
      {/* Sect Identity Banner Pill */}
      <div className="flex items-center justify-between px-2.5 py-1 rounded-xl bg-slate-950/85 border border-slate-800/90 backdrop-blur-md text-[10px] font-tech text-slate-300">
        <div className="flex items-center gap-1.5">
          <span className="text-sm">{playerClass.icon}</span>
          <span className="font-bold text-amber-300">{playerClass.name}</span>
          <span className="text-slate-500">·</span>
          <span className="text-slate-400 truncate max-w-[140px] sm:max-w-[180px]">
            {playerClass.sectTitle.split('·')[0]}
          </span>
        </div>

        {onOpenClassSelect && (
          <button
            type="button"
            onClick={onOpenClassSelect}
            className="text-[9px] text-cyan-400 hover:text-cyan-300 hover:underline cursor-pointer ml-2 whitespace-nowrap"
            title="Đổi hệ phái hoặc khởi tạo lại căn cơ"
          >
            Đổi Phái
          </button>
        )}
      </div>

      {/* 4 Class Skills Row: [Q] [W] [E] [R] */}
      <div
        role="group"
        aria-label="Bộ 4 Kỹ Năng Q W E R"
        className="grid grid-cols-4 gap-1 sm:gap-1.5 p-1 rounded-2xl bg-slate-950/90 border border-slate-800/90 backdrop-blur-md shadow-xl"
      >
        {/* SKILL [Q]: Core Rhythm Stance (Always active) */}
        <div
          className="relative p-1.5 sm:p-2 rounded-xl bg-slate-900/90 border border-amber-400/80 shadow-md flex flex-col items-center justify-between text-center select-none"
          title={`[Q] ${playerClass.skills.Q.name}: ${playerClass.skills.Q.description}`}
        >
          <div className="w-full flex items-center justify-between text-[9px] font-tech text-amber-300">
            <span className="font-bold bg-amber-400/20 px-1 rounded">Q</span>
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
          </div>

          <div className="my-0.5 text-base sm:text-lg">
            {playerClass.skills.Q.icon}
          </div>

          <div className="w-full">
            <div className="text-[10px] sm:text-[11px] font-tech font-bold text-slate-100 truncate">
              {playerClass.skills.Q.name.split(' ')[0]}
            </div>
            <div className="text-[8px] text-emerald-400 font-tech uppercase truncate">
              Gõ Đe
            </div>
          </div>
        </div>

        {/* SKILL [W]: Tactical Utility (Cooldown) */}
        {(() => {
          const sk = playerClass.skills.W;
          const unlocked = isSkillUnlocked(sk.unlockLevel);
          const onCd = cooldowns.W > 0;

          return (
            <button
              type="button"
              disabled={!canCastW}
              onClick={() => onCastSkill('W')}
              className={`relative p-1.5 sm:p-2 rounded-xl border flex flex-col items-center justify-between text-center transition-all select-none overflow-hidden ${
                !unlocked
                  ? 'bg-slate-950/40 border-slate-800/60 opacity-60 cursor-not-allowed'
                  : onCd
                  ? 'bg-slate-900/40 border-slate-700 cursor-not-allowed'
                  : 'bg-slate-900/90 hover:bg-slate-800 border-cyan-500/70 hover:border-cyan-400 cursor-pointer shadow-md shadow-cyan-500/20 active:scale-95'
              }`}
              title={`[W] ${sk.name} (Lv.${sk.unlockLevel}): ${sk.description}`}
            >
              {/* Cooldown overlay */}
              {onCd && (
                <div className="absolute inset-0 bg-slate-950/80 backdrop-blur-[1px] flex items-center justify-center z-10">
                  <span className="text-xs font-mono font-bold text-amber-300">
                    {cooldowns.W.toFixed(0)}s
                  </span>
                </div>
              )}

              <div className="w-full flex items-center justify-between text-[9px] font-tech text-cyan-300">
                <span className="font-bold bg-cyan-500/20 px-1 rounded">W</span>
                <span className="text-[8px] text-slate-400">{unlocked ? 'CD 10s' : `Lv.${sk.unlockLevel}`}</span>
              </div>

              <div className="my-0.5 text-base sm:text-lg">
                {sk.icon}
              </div>

              <div className="w-full">
                <div className="text-[10px] sm:text-[11px] font-tech font-bold text-slate-100 truncate">
                  {sk.name.split(' ')[0]}
                </div>
                <div className={`text-[8px] font-tech uppercase truncate ${canCastW ? 'text-cyan-300 font-bold' : 'text-slate-500'}`}>
                  {unlocked ? (onCd ? 'Hồi chiêu' : 'Kích hoạt') : 'Khóa'}
                </div>
              </div>
            </button>
          );
        })()}

        {/* SKILL [E]: Overdrive Consumer (Requires 8 OD) */}
        {(() => {
          const sk = playerClass.skills.E;
          const unlocked = isSkillUnlocked(sk.unlockLevel);
          const hasOd = overdriveCharge >= 8;
          const onCd = cooldowns.E > 0;

          return (
            <button
              type="button"
              disabled={!canCastE}
              onClick={() => onCastSkill('E')}
              className={`relative p-1.5 sm:p-2 rounded-xl border flex flex-col items-center justify-between text-center transition-all select-none overflow-hidden ${
                !unlocked
                  ? 'bg-slate-950/40 border-slate-800/60 opacity-60 cursor-not-allowed'
                  : canCastE
                  ? 'bg-gradient-to-b from-purple-950/90 to-slate-900 border-purple-400 ring-2 ring-purple-400/40 shadow-lg shadow-purple-500/30 cursor-pointer active:scale-95 animate-pulse'
                  : 'bg-slate-900/60 border-slate-700 cursor-not-allowed opacity-80'
              }`}
              title={`[E] ${sk.name} (Tốn 8 OD · Lv.${sk.unlockLevel}): ${sk.description}`}
            >
              {onCd && (
                <div className="absolute inset-0 bg-slate-950/80 backdrop-blur-[1px] flex items-center justify-center z-10">
                  <span className="text-xs font-mono font-bold text-purple-300">
                    {cooldowns.E.toFixed(0)}s
                  </span>
                </div>
              )}

              <div className="w-full flex items-center justify-between text-[9px] font-tech text-purple-300">
                <span className="font-bold bg-purple-500/20 px-1 rounded">E</span>
                <span className="text-[8px] text-amber-300 font-bold">8 OD</span>
              </div>

              <div className="my-0.5 text-base sm:text-lg">
                {sk.icon}
              </div>

              <div className="w-full">
                <div className="text-[10px] sm:text-[11px] font-tech font-bold text-slate-100 truncate">
                  {sk.name.split(' ')[0]}
                </div>
                <div className={`text-[8px] font-tech uppercase truncate font-bold ${canCastE ? 'text-purple-300' : 'text-slate-500'}`}>
                  {unlocked ? (canCastE ? 'SẴN SÀNG!' : 'Cần 8 OD') : 'Khóa'}
                </div>
              </div>
            </button>
          );
        })()}

        {/* SKILL [R]: Class Ultimate (Requires Overdrive Tier 3 / 16+ OD) */}
        {(() => {
          const sk = playerClass.skills.R;
          const unlocked = isSkillUnlocked(sk.unlockLevel);
          const hasOd = overdriveCharge >= 16;
          const onCd = cooldowns.R > 0;

          return (
            <button
              type="button"
              disabled={!canCastR}
              onClick={() => onCastSkill('R')}
              className={`relative p-1.5 sm:p-2 rounded-xl border flex flex-col items-center justify-between text-center transition-all select-none overflow-hidden ${
                !unlocked
                  ? 'bg-slate-950/40 border-slate-800/60 opacity-60 cursor-not-allowed'
                  : canCastR
                  ? 'bg-gradient-to-b from-red-950/90 to-slate-900 border-red-500 ring-2 ring-red-500/50 shadow-xl shadow-red-500/40 cursor-pointer active:scale-95 animate-bounce'
                  : 'bg-slate-900/60 border-slate-700 cursor-not-allowed opacity-80'
              }`}
              title={`[R] ${sk.name} (Đại Chiêu Tầng 3 · Lv.${sk.unlockLevel}): ${sk.description}`}
            >
              {onCd && (
                <div className="absolute inset-0 bg-slate-950/80 backdrop-blur-[1px] flex items-center justify-center z-10">
                  <span className="text-xs font-mono font-bold text-red-300">
                    {cooldowns.R.toFixed(0)}s
                  </span>
                </div>
              )}

              <div className="w-full flex items-center justify-between text-[9px] font-tech text-red-300">
                <span className="font-bold bg-red-500/20 px-1 rounded">R</span>
                <span className="text-[8px] text-red-400 font-bold">TẦNG 3</span>
              </div>

              <div className="my-0.5 text-base sm:text-lg">
                {sk.icon}
              </div>

              <div className="w-full">
                <div className="text-[10px] sm:text-[11px] font-tech font-bold text-slate-100 truncate">
                  {sk.name.split(' ')[0]}
                </div>
                <div className={`text-[8px] font-tech uppercase truncate font-bold ${canCastR ? 'text-red-300 animate-pulse' : 'text-slate-500'}`}>
                  {unlocked ? (canCastR ? 'ĐẠI CHIÊU!' : 'Cần Tầng 3') : 'Khóa'}
                </div>
              </div>
            </button>
          );
        })()}
      </div>

      {/* 3-Tier Overcharge Gauge (Tầng 1 Vàng -> Tầng 2 Tím -> Tầng 3 Đỏ) */}
      <div
        className="rounded-2xl px-3 py-2 border backdrop-blur-md transition-all duration-300 shadow-lg"
        style={{
          borderColor: tierInfo.borderColor,
          boxShadow: `0 0 15px ${tierInfo.glowColor}`,
          backgroundColor: 'rgba(5, 7, 15, 0.9)',
        }}
      >
        <div className="flex items-center justify-between text-[10px] sm:text-[11px] font-tech mb-1.5">
          <span className="font-bold flex items-center gap-1.5" style={{ color: tierInfo.color }}>
            <Sparkles className="w-3.5 h-3.5" />
            <span>{tierInfo.label}</span>
          </span>

          <span className="font-bold font-mono text-slate-200">
            {overdriveCharge.toFixed(1)} / {OVERDRIVE_TOTAL_CAP}
            <span className="text-slate-400 text-[9px] ml-1">
              ({tierInfo.tierCharge.toFixed(1)}/8 T{tierInfo.tier})
            </span>
          </span>
        </div>

        {/* 8-Segment Bar Colored Dynamically */}
        <div className="grid grid-cols-8 gap-1">
          {Array.from({ length: OVERDRIVE_MAX }).map((_, idx) => {
            const filled = tierInfo.tierCharge >= idx + 1;
            const half = !filled && tierInfo.tierCharge >= idx + 0.5;

            return (
              <div
                key={idx}
                className="h-2 rounded-sm transition-all duration-200 relative overflow-hidden bg-slate-900 border border-slate-800"
              >
                {filled && (
                  <div
                    className="w-full h-full shadow-sm"
                    style={{
                      backgroundColor: tierInfo.color,
                      boxShadow: `0 0 6px ${tierInfo.glowColor}`,
                    }}
                  />
                )}
                {half && (
                  <div
                    className="w-1/2 h-full"
                    style={{
                      backgroundColor: tierInfo.color,
                    }}
                  />
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
