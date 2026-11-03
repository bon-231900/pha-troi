import React from 'react';
import { soundEngine } from '../game/audio';

interface TitleScreenModalProps {
  onStart: () => void;
}

export const TitleScreenModal: React.FC<TitleScreenModalProps> = ({ onStart }) => {
  const handleStart = () => {
    soundEngine.unlockAudio();
    soundEngine.playAnvilStrike('PERFECT', 'Q', false);
    onStart();
  };
  return (
    <div
      className="fixed inset-0 z-50 flex flex-col items-center justify-between p-6 md:p-12 overflow-hidden bg-[#080A10]"
      style={{
        backgroundImage:
          'radial-gradient(circle at 50% 38%, rgba(255, 160, 0, 0.18) 0%, rgba(17, 22, 37, 0.98) 52%, #080A10 100%)',
      }}
    >
      {/* Top quiet realm inscription */}
      <div className="text-center tracking-[0.25em] text-xs md:text-sm text-amber-300/80 font-tech uppercase">
        Đại Công Trường Vạn Dân · Cửu Trọng Thiên Cẩm
      </div>

      {/* Centerpiece SVG Emblem + Title Lockup over calm negative space */}
      <div className="my-auto flex flex-col items-center max-w-2xl text-center">
        <div className="relative mb-6 flex items-center justify-center">
          <svg
            viewBox="0 0 220 180"
            className="w-44 h-36 md:w-56 md:h-44"
            aria-hidden="true"
          >
            <defs>
              <linearGradient id="crestGold" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="#FFD23F" />
                <stop offset="50%" stopColor="#FFA000" />
                <stop offset="100%" stopColor="#FF3B30" />
              </linearGradient>
              <linearGradient id="crestCyan" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" stopColor="#00F0FF" />
                <stop offset="100%" stopColor="#0099FF" />
              </linearGradient>
            </defs>

            {/* Outer Radial Rhythm Halo */}
            <circle
              cx="110"
              cy="95"
              r="74"
              fill="none"
              stroke="url(#crestGold)"
              strokeWidth="1.5"
              strokeDasharray="8 6"
              opacity="0.65"
            />
            <circle
              cx="110"
              cy="95"
              r="58"
              fill="none"
              stroke="url(#crestCyan)"
              strokeWidth="2"
              opacity="0.85"
            />

            {/* Isometric Mythic Anvil Silhouette */}
            <polygon
              points="55,95 165,95 148,115 72,115"
              fill="#111625"
              stroke="#FFD23F"
              strokeWidth="2.5"
            />
            <polygon
              points="78,115 142,115 130,142 90,142"
              fill="#080A10"
              stroke="#FFA000"
              strokeWidth="2"
            />
            <polygon
              points="64,142 156,142 166,156 54,156"
              fill="#1E293B"
              stroke="#FFD23F"
              strokeWidth="2"
            />

            {/* Celestial Thunder Bolt piercing the Anvil */}
            <polygon
              points="116,18 92,72 114,72 102,112 134,60 112,60"
              fill="url(#crestCyan)"
            />
            <circle cx="110" cy="95" r="5" fill="#FFD23F" />
          </svg>
        </div>

        <h1
          className="font-display text-4xl sm:text-5xl md:text-6xl font-extrabold tracking-wider text-amber-300 mb-3"
          style={{
            textShadow: '0 4px 24px rgba(255, 160, 0, 0.35)',
            textWrap: 'balance',
          }}
        >
          PHÁ TRỜI
        </h1>
        <p className="font-display text-sm sm:text-base md:text-lg tracking-[0.2em] text-cyan-300 uppercase mb-6">
          The Celestial Forge · Thiên Cổ Rực Lửa
        </p>

        <p className="text-slate-300 text-sm md:text-base max-w-lg mb-8 leading-relaxed">
          Hợp lực cùng vạn dân rèn thần binh giữa Cửu Trọng Thiên. Canh chuẩn vòng sóng hội tụ vào{' '}
          <span className="text-amber-300 font-semibold">Gờ Vàng Đe Thần</span> để giáng búa Hoàng Kim{' '}
          <span className="font-tech text-cyan-300 font-semibold">x3.5</span> và xuyên thủng giáp Thiên Ma.
        </p>

        <button
          type="button"
          data-start="true"
          onClick={handleStart}
          className="px-8 py-4 rounded-xl bg-amber-400 hover:bg-amber-300 active:scale-95 text-slate-950 font-display font-bold text-base md:text-lg tracking-wider transition-all cursor-pointer shadow-lg shadow-amber-500/25 whitespace-nowrap shrink-0"
        >
          KHAI LÒ PHÁ TRỜI
        </button>
      </div>

      {/* Bottom single-line flat control hint */}
      <div className="text-xs md:text-sm text-slate-400 font-tech tracking-wide text-center">
        Space / Chạm: Đập Đe Theo Nhịp · Q W E R: Đổi 4 Thế Búa · P: Tạm Dừng · M: Âm Thanh
      </div>
    </div>
  );
};
