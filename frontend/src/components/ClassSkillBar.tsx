import React from 'react';
import {
  PlayerClassMeta,
  getOverdriveTier,
  OVERDRIVE_MAX,
  OVERDRIVE_TOTAL_CAP,
} from '../game/rules';
import { Sparkles, Lock } from 'lucide-react';
import { hapticEngine } from '../game/haptics';
import { getSkillArt, UI_FRAME_ASSETS } from '../game/skillArtAssets';

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
  onHeroStrike?: () => void;
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
  onHeroStrike,
  hudVisible = true,
}) => {
  const tierInfo = getOverdriveTier(overdriveCharge);

  const isSkillUnlocked = (unlockLevel: number) => {
    return totalForgeLevel >= unlockLevel;
  };

  const canCastW = isSkillUnlocked(playerClass.skills.W.unlockLevel) && cooldowns.W <= 0;
  const canCastE = isSkillUnlocked(playerClass.skills.E.unlockLevel) && overdriveCharge >= 8 && cooldowns.E <= 0;
  const canCastR = isSkillUnlocked(playerClass.skills.R.unlockLevel) && overdriveCharge >= 16 && cooldowns.R <= 0;

  const artQ = getSkillArt(playerClass.id, 'Q');
  const artW = getSkillArt(playerClass.id, 'W');
  const artE = getSkillArt(playerClass.id, 'E');
  const artR = getSkillArt(playerClass.id, 'R');

  return (
    <div
      className={`fixed bottom-2 inset-x-2 sm:inset-x-auto sm:left-5 sm:bottom-3 z-20 flex flex-col gap-1.5 pointer-events-auto sm:max-w-[420px] pb-safe transition-all duration-300 ${
        hudVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-6 pointer-events-none'
      }`}
    >
      {/* 1. SECT IDENTITY TALISMAN PLAQUE (Asset Art Plaque) */}
      <div className="relative flex items-center justify-between px-3 py-1.5 rounded-xl bg-gradient-to-r from-red-950/90 via-slate-950/90 to-amber-950/80 border border-amber-500/40 backdrop-blur-md text-[10px] font-tech text-slate-200 shadow-lg overflow-hidden">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-amber-500/10 via-transparent to-transparent pointer-events-none" />
        <div className="relative flex items-center gap-2">
          <div className="w-5 h-5 rounded-full overflow-hidden border border-amber-400/60 flex items-center justify-center bg-black/60 shadow-sm">
            <img
              src={artQ.icon}
              alt={playerClass.name}
              className="w-4 h-4 object-contain"
            />
          </div>
          <span className="font-bold text-amber-300 tracking-wide font-cinzel text-xs">
            {playerClass.name}
          </span>
          <span className="text-amber-500/60">✦</span>
          <span className="text-slate-300 font-serif truncate max-w-[150px] sm:max-w-[200px]">
            {playerClass.sectTitle.split('·')[0]}
          </span>
        </div>

        <div className="relative text-[9px] text-amber-400 font-mono font-bold bg-black/40 px-1.5 py-0.5 rounded border border-amber-500/30">
          Lv.{totalForgeLevel}
        </div>
      </div>

      {/* 2. 4 CLASS SKILLS ROW: [Q] [W] [E] [R] WITH MODULAR ASSET FRAMES */}
      <div
        role="group"
        aria-label="Bộ 4 Kỹ Năng Q W E R"
        className="grid grid-cols-4 gap-1.5 p-1.5 rounded-2xl bg-black/85 border border-amber-900/40 backdrop-blur-md shadow-2xl"
      >
        {/* SKILL [Q]: Core Strike Stance */}
        <button
          type="button"
          onClick={() => {
            hapticEngine.playStrike();
            onHeroStrike?.();
          }}
          className="relative p-1 rounded-xl flex flex-col items-center justify-between text-center select-none cursor-pointer transition-all hover:brightness-125 active:scale-95 group overflow-hidden"
          title={`[Q] ${playerClass.skills.Q.name}: Bấm hoặc nhấn SPACE để gõ đe`}
        >
          {/* Frame Asset Background */}
          <img
            src={UI_FRAME_ASSETS.ready}
            alt="Ready Frame"
            className="absolute inset-0 w-full h-full object-fill pointer-events-none drop-shadow-[0_0_8px_rgba(245,158,11,0.5)]"
          />

          {/* Keybind Tag */}
          <div className="relative z-10 w-full flex items-center justify-between text-[8px] font-tech text-amber-200 px-1 pt-0.5">
            <span className="font-bold bg-black/70 px-1 py-0.5 rounded border border-amber-400/50">
              Q / SPACE
            </span>
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse shadow-[0_0_4px_#34D399]" />
          </div>

          {/* Real Skill Art Icon */}
          <div className="relative z-10 my-0.5 w-10 h-10 sm:w-11 sm:h-11 flex items-center justify-center">
            <img
              src={artQ.icon}
              alt={playerClass.skills.Q.name}
              className="w-full h-full object-contain filter drop-shadow-[0_0_6px_rgba(249,115,22,0.8)] group-hover:scale-105 transition-transform"
            />
          </div>

          {/* Skill Title & Action Text */}
          <div className="relative z-10 w-full pb-0.5">
            <div className="text-[10px] font-tech font-bold text-slate-100 truncate drop-shadow">
              {playerClass.skills.Q.name.split(' ')[0]}
            </div>
            <div className="text-[8px] text-amber-300 font-tech uppercase truncate font-bold drop-shadow">
              GÕ ĐE ⚡
            </div>
          </div>
        </button>

        {/* SKILL [W]: Tactical Utility */}
        {(() => {
          const sk = playerClass.skills.W;
          const unlocked = isSkillUnlocked(sk.unlockLevel);
          const onCd = cooldowns.W > 0;
          const frameBg = !unlocked
            ? UI_FRAME_ASSETS.locked
            : canCastW
            ? UI_FRAME_ASSETS.ready
            : UI_FRAME_ASSETS.idle;

          return (
            <button
              type="button"
              disabled={!canCastW}
              onClick={() => onCastSkill('W')}
              className={`relative p-1 rounded-xl flex flex-col items-center justify-between text-center select-none transition-all overflow-hidden group ${
                !unlocked
                  ? 'cursor-not-allowed opacity-75'
                  : onCd
                  ? 'cursor-not-allowed brightness-90'
                  : 'cursor-pointer hover:brightness-125 active:scale-95'
              }`}
              title={`[W] ${sk.name} (Lv.${sk.unlockLevel}): ${sk.description}`}
            >
              {/* Frame Asset Background */}
              <img
                src={frameBg}
                alt="Frame"
                className="absolute inset-0 w-full h-full object-fill pointer-events-none"
              />

              {/* Cooldown Overlay */}
              {onCd && (
                <div className="absolute inset-0 bg-black/85 backdrop-blur-[1px] flex flex-col items-center justify-center z-20">
                  <span className="text-xs font-mono font-bold text-amber-300 drop-shadow">
                    {cooldowns.W.toFixed(0)}s
                  </span>
                  <span className="text-[8px] text-slate-400 font-tech">HỒI CHIÊU</span>
                </div>
              )}

              {/* Keybind Tag */}
              <div className="relative z-10 w-full flex items-center justify-between text-[8px] font-tech text-cyan-200 px-1 pt-0.5">
                <span className="font-bold bg-black/70 px-1 py-0.5 rounded border border-cyan-400/50">
                  W
                </span>
                <span className="text-[8px] text-slate-300 font-mono">
                  {unlocked ? (onCd ? `${cooldowns.W.toFixed(0)}s` : '10s') : `Lv.${sk.unlockLevel}`}
                </span>
              </div>

              {/* Real Skill Art Icon */}
              <div className="relative z-10 my-0.5 w-10 h-10 sm:w-11 sm:h-11 flex items-center justify-center">
                <img
                  src={artW.icon}
                  alt={sk.name}
                  className={`w-full h-full object-contain filter drop-shadow-[0_0_6px_rgba(6,182,212,0.7)] group-hover:scale-105 transition-transform ${
                    !unlocked ? 'grayscale opacity-40' : ''
                  }`}
                />
              </div>

              {/* Skill Title & Action Text */}
              <div className="relative z-10 w-full pb-0.5">
                <div className="text-[10px] font-tech font-bold text-slate-100 truncate drop-shadow">
                  {sk.name.split(' ')[0]}
                </div>
                <div
                  className={`text-[8px] font-tech uppercase truncate font-bold drop-shadow ${
                    !unlocked ? 'text-slate-500' : canCastW ? 'text-cyan-300 animate-pulse' : 'text-slate-400'
                  }`}
                >
                  {unlocked ? (canCastW ? 'KÍCH HOẠT' : 'HỒI CHIÊU') : 'KHÓA'}
                </div>
              </div>
            </button>
          );
        })()}

        {/* SKILL [E]: Overdrive Burst (Requires 8 OD) */}
        {(() => {
          const sk = playerClass.skills.E;
          const unlocked = isSkillUnlocked(sk.unlockLevel);
          const onCd = cooldowns.E > 0;
          const frameBg = !unlocked
            ? UI_FRAME_ASSETS.locked
            : canCastE
            ? UI_FRAME_ASSETS.ready
            : UI_FRAME_ASSETS.idle;

          return (
            <button
              type="button"
              disabled={!canCastE}
              onClick={() => onCastSkill('E')}
              className={`relative p-1 rounded-xl flex flex-col items-center justify-between text-center select-none transition-all overflow-hidden group ${
                !unlocked
                  ? 'cursor-not-allowed opacity-75'
                  : onCd
                  ? 'cursor-not-allowed brightness-90'
                  : canCastE
                  ? 'cursor-pointer hover:brightness-125 active:scale-95 drop-shadow-[0_0_12px_rgba(245,158,11,0.6)]'
                  : 'cursor-not-allowed opacity-85'
              }`}
              title={`[E] ${sk.name} (Tốn 8 OD · Lv.${sk.unlockLevel}): ${sk.description}`}
            >
              {/* Frame Asset Background */}
              <img
                src={frameBg}
                alt="Frame"
                className="absolute inset-0 w-full h-full object-fill pointer-events-none"
              />

              {/* Cooldown Overlay */}
              {onCd && (
                <div className="absolute inset-0 bg-black/85 backdrop-blur-[1px] flex flex-col items-center justify-center z-20">
                  <span className="text-xs font-mono font-bold text-purple-300 drop-shadow">
                    {cooldowns.E.toFixed(0)}s
                  </span>
                  <span className="text-[8px] text-slate-400 font-tech">HỒI CHIÊU</span>
                </div>
              )}

              {/* Keybind Tag */}
              <div className="relative z-10 w-full flex items-center justify-between text-[8px] font-tech text-purple-200 px-1 pt-0.5">
                <span className="font-bold bg-black/70 px-1 py-0.5 rounded border border-purple-400/50">
                  E
                </span>
                <span className="text-[8px] text-amber-300 font-bold font-mono">
                  8 OD
                </span>
              </div>

              {/* Real Skill Art Icon */}
              <div className="relative z-10 my-0.5 w-10 h-10 sm:w-11 sm:h-11 flex items-center justify-center">
                <img
                  src={artE.icon}
                  alt={sk.name}
                  className={`w-full h-full object-contain filter drop-shadow-[0_0_6px_rgba(245,158,11,0.8)] group-hover:scale-105 transition-transform ${
                    !unlocked ? 'grayscale opacity-40' : canCastE ? 'scale-105 animate-pulse' : ''
                  }`}
                />
              </div>

              {/* Skill Title & Action Text */}
              <div className="relative z-10 w-full pb-0.5">
                <div className="text-[10px] font-tech font-bold text-slate-100 truncate drop-shadow">
                  {sk.name.split(' ')[0]}
                </div>
                <div
                  className={`text-[8px] font-tech uppercase truncate font-bold drop-shadow ${
                    !unlocked ? 'text-slate-500' : canCastE ? 'text-amber-300 animate-pulse' : 'text-slate-400'
                  }`}
                >
                  {unlocked ? (canCastE ? 'SẴN SÀNG!' : 'CẦN 8 OD') : 'KHÓA'}
                </div>
              </div>
            </button>
          );
        })()}

        {/* SKILL [R]: Class Ultimate (Requires Overdrive Tier 3 / 16+ OD) */}
        {(() => {
          const sk = playerClass.skills.R;
          const unlocked = isSkillUnlocked(sk.unlockLevel);
          const onCd = cooldowns.R > 0;
          const frameBg = !unlocked
            ? UI_FRAME_ASSETS.locked
            : canCastR
            ? UI_FRAME_ASSETS.ready
            : UI_FRAME_ASSETS.idle;

          return (
            <button
              type="button"
              disabled={!canCastR}
              onClick={() => onCastSkill('R')}
              className={`relative p-1 rounded-xl flex flex-col items-center justify-between text-center select-none transition-all overflow-hidden group ${
                !unlocked
                  ? 'cursor-not-allowed opacity-75'
                  : onCd
                  ? 'cursor-not-allowed brightness-90'
                  : canCastR
                  ? 'cursor-pointer hover:brightness-125 active:scale-95 drop-shadow-[0_0_16px_rgba(239,68,68,0.8)] animate-pulse'
                  : 'cursor-not-allowed opacity-85'
              }`}
              title={`[R] ${sk.name} (Đại Chiêu Tầng 3 · Lv.${sk.unlockLevel}): ${sk.description}`}
            >
              {/* Frame Asset Background */}
              <img
                src={frameBg}
                alt="Frame"
                className="absolute inset-0 w-full h-full object-fill pointer-events-none"
              />

              {/* Cooldown Overlay */}
              {onCd && (
                <div className="absolute inset-0 bg-black/85 backdrop-blur-[1px] flex flex-col items-center justify-center z-20">
                  <span className="text-xs font-mono font-bold text-red-300 drop-shadow">
                    {cooldowns.R.toFixed(0)}s
                  </span>
                  <span className="text-[8px] text-slate-400 font-tech">HỒI CHIÊU</span>
                </div>
              )}

              {/* Keybind Tag */}
              <div className="relative z-10 w-full flex items-center justify-between text-[8px] font-tech text-red-200 px-1 pt-0.5">
                <span className="font-bold bg-black/70 px-1 py-0.5 rounded border border-red-500/50">
                  R
                </span>
                <span className="text-[8px] text-red-400 font-bold font-mono">
                  TẦNG 3
                </span>
              </div>

              {/* Real Skill Art Icon */}
              <div className="relative z-10 my-0.5 w-10 h-10 sm:w-11 sm:h-11 flex items-center justify-center">
                <img
                  src={artR.icon}
                  alt={sk.name}
                  className={`w-full h-full object-contain filter drop-shadow-[0_0_8px_rgba(239,68,68,0.9)] group-hover:scale-105 transition-transform ${
                    !unlocked ? 'grayscale opacity-40' : canCastR ? 'scale-110' : ''
                  }`}
                />
              </div>

              {/* Skill Title & Action Text */}
              <div className="relative z-10 w-full pb-0.5">
                <div className="text-[10px] font-tech font-bold text-slate-100 truncate drop-shadow">
                  {sk.name.split(' ')[0]}
                </div>
                <div
                  className={`text-[8px] font-tech uppercase truncate font-bold drop-shadow ${
                    !unlocked ? 'text-slate-500' : canCastR ? 'text-red-400 animate-bounce' : 'text-slate-400'
                  }`}
                >
                  {unlocked ? (canCastR ? 'ĐẠI CHIÊU!' : 'CẦN TẦNG 3') : 'KHÓA'}
                </div>
              </div>
            </button>
          );
        })()}
      </div>

      {/* 3. 3-TIER OVERDRIVE DRAGON GAUGE WITH CELESTIAL RUNE GEMS */}
      <div
        className="rounded-2xl px-3 py-2 border backdrop-blur-md transition-all duration-300 shadow-xl relative overflow-hidden"
        style={{
          borderColor: tierInfo.borderColor,
          boxShadow: `0 0 18px ${tierInfo.glowColor}`,
          backgroundColor: 'rgba(5, 7, 15, 0.92)',
        }}
      >
        <div className="flex items-center justify-between text-[10px] sm:text-[11px] font-tech mb-1.5">
          <span className="font-bold flex items-center gap-1.5" style={{ color: tierInfo.color }}>
            <Sparkles className="w-3.5 h-3.5" />
            <span className="tracking-wide">{tierInfo.label}</span>
          </span>

          <span className="font-bold font-mono text-slate-200">
            {overdriveCharge.toFixed(1)} / {OVERDRIVE_TOTAL_CAP}
            <span className="text-slate-400 text-[9px] ml-1">
              ({tierInfo.tierCharge.toFixed(1)}/8 T{tierInfo.tier})
            </span>
          </span>
        </div>

        {/* 8-Segment Gem Sockets using Authentic Xianxia Rune Crystals */}
        <div className="grid grid-cols-8 gap-1.5 items-center justify-items-center py-0.5">
          {Array.from({ length: OVERDRIVE_MAX }).map((_, idx) => {
            const filled = tierInfo.tierCharge >= idx + 1;
            const half = !filled && tierInfo.tierCharge >= idx + 0.5;

            return (
              <div
                key={idx}
                className="relative w-7 h-7 sm:w-8 sm:h-8 flex items-center justify-center transition-all duration-200"
              >
                {filled ? (
                  <img
                    src={UI_FRAME_ASSETS.gemActive}
                    alt="Active Gem"
                    className="w-full h-full object-contain filter drop-shadow-[0_0_8px_#A855F7] animate-pulse"
                  />
                ) : half ? (
                  <div className="relative w-full h-full flex items-center justify-center">
                    <img
                      src={UI_FRAME_ASSETS.gemActive}
                      alt="Half Gem"
                      className="w-full h-full object-contain opacity-70 filter drop-shadow-[0_0_4px_#A855F7]"
                    />
                  </div>
                ) : (
                  <img
                    src={UI_FRAME_ASSETS.gemDormant}
                    alt="Dormant Gem"
                    className="w-5 h-5 object-contain opacity-35 grayscale"
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
