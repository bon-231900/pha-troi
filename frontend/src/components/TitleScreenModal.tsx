import React, { useState } from 'react';
import { soundEngine } from '../game/audio';
import { Play } from 'lucide-react';

interface TitleScreenModalProps {
  onStart: () => void;
}

export const TitleScreenModal: React.FC<TitleScreenModalProps> = ({ onStart }) => {
  const [isStarting, setIsStarting] = useState(false);

  const handleStart = () => {
    if (isStarting) return;
    setIsStarting(true);
    soundEngine.unlockAudio();
    soundEngine.playAnvilStrike('PERFECT', 'Q', false);
    setTimeout(() => {
      onStart();
    }, 450);
  };

  const base = import.meta.env.BASE_URL || './';
  const cleanBase = base.endsWith('/') ? base : base + '/';
  const splashBgSrc = `${cleanBase}assets/art/celestial_splash_bg.webp`;
  const logoSrc = `${cleanBase}assets/art/pha_troi_calligraphy_logo.webp`;

  return (
    <div
      className={`fixed inset-0 z-50 flex flex-col justify-between p-6 sm:p-10 md:p-14 select-none overflow-hidden transition-opacity duration-500 ${
        isStarting ? 'opacity-0 scale-105 pointer-events-none' : 'opacity-100 scale-100'
      }`}
    >
      {/* 1. Full-bleed 2K Native Crisp Celestial Splash Art (2560x1428) */}
      <div className="absolute inset-0 -z-10 overflow-hidden bg-slate-950">
        <img
          src={splashBgSrc}
          alt="Toàn Dân Phá Trời - The Celestial Forge"
          className="w-full h-full object-cover object-center transform scale-100 filter drop-shadow-2xl"
          loading="eager"
          decoding="async"
        />
        {/* Subtle cinematic vignette gradients preserving art vibrancy */}
        <div className="absolute inset-0 bg-gradient-to-r from-slate-950/85 via-slate-950/35 to-transparent pointer-events-none" />
        <div className="absolute inset-0 bg-gradient-to-t from-slate-950/90 via-transparent to-slate-950/50 pointer-events-none" />
      </div>

      {/* 2. Top Navigation Bar (matching reference layout) */}
      <div className="w-full flex items-center justify-between max-w-7xl mx-auto z-10">
        {/* Top-left small brand insignia */}
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-full border border-amber-400/50 flex items-center justify-center bg-slate-950/50 backdrop-blur-md shadow-[0_0_12px_rgba(255,180,0,0.3)]">
            <span className="text-amber-300 font-display font-bold text-xs">破</span>
          </div>
          <span className="font-display font-bold text-sm tracking-wider text-amber-200/90">PHÁ TRỜI</span>
        </div>

        {/* Center Nav items */}
        <div className="hidden md:flex items-center gap-8 text-xs font-tech tracking-[0.2em] text-slate-300 uppercase">
          <span className="text-amber-300 font-semibold cursor-pointer">TRANG CHỦ</span>
          <span className="hover:text-amber-200 transition-colors cursor-pointer">THẾ GIỚI</span>
          <span className="hover:text-amber-200 transition-colors cursor-pointer">NHÂN VẬT</span>
          <span className="hover:text-amber-200 transition-colors cursor-pointer">TÍNH NĂNG</span>
          <span className="hover:text-amber-200 transition-colors cursor-pointer">TIN TỨC</span>
        </div>

        {/* Top-right CTA */}
        <button
          type="button"
          onClick={handleStart}
          className="px-4 py-1.5 rounded-full bg-gradient-to-r from-amber-400/20 via-amber-300/30 to-amber-500/20 hover:from-amber-400/35 hover:to-amber-500/35 border border-amber-400/60 text-amber-200 text-xs font-tech font-bold tracking-wider backdrop-blur-md shadow-md transition-all cursor-pointer"
        >
          VÀO GAME →
        </button>
      </div>

      {/* 3. Main Hero Typography Block (Positioned on the Left / Mid-Left like the reference) */}
      <div className="my-auto max-w-2xl z-10 flex flex-col items-start text-left pl-2 sm:pl-6 md:pl-12">
        {/* The Original Calligraphy Brush Title "Phá Trời" */}
        <div className="relative mb-2">
          <img
            src={logoSrc}
            alt="Phá Trời - The Celestial Forge"
            className="w-[280px] sm:w-[360px] md:w-[440px] max-w-full object-contain drop-shadow-[0_4px_25px_rgba(255,200,80,0.45)] select-none pointer-events-none"
          />
        </div>

        {/* Ornamental Divider: — ✧ — Vạn Cổ Đúc Thần Đài — ✧ — */}
        <div className="flex items-center gap-3 my-2 text-amber-200/90 text-sm sm:text-base tracking-widest">
          <span className="w-10 sm:w-16 h-[1px] bg-gradient-to-r from-transparent to-amber-400/70" />
          <span className="text-amber-300 text-xs">✧</span>
          <span className="italic font-medium drop-shadow-sm" style={{ fontFamily: "'Be Vietnam Pro', sans-serif" }}>
            Vạn Cổ Đúc Thần Đài
          </span>
          <span className="text-amber-300 text-xs">✧</span>
          <span className="w-10 sm:w-16 h-[1px] bg-gradient-to-l from-transparent to-amber-400/70" />
        </div>

        {/* Poetic Subtitle Paragraph */}
        <div
          className="text-slate-200/85 text-xs sm:text-sm md:text-[15px] font-light leading-relaxed my-3 max-w-md drop-shadow"
          style={{ fontFamily: "'Be Vietnam Pro', sans-serif" }}
        >
          <p>Một thế giới nơi tiên đạo giao hòa với hiện thực,</p>
          <p>và con người viết tiếp huyền thoại của chính mình.</p>
        </div>

        {/* Pill Glassmorphic Action Button (Styled identical to the reference "XEM TRAILER" button) */}
        <div className="mt-4 flex items-center gap-4">
          <button
            type="button"
            data-start="true"
            onClick={handleStart}
            disabled={isStarting}
            className="group flex items-center gap-3 px-6 py-2.5 sm:px-8 sm:py-3 rounded-full bg-slate-900/65 hover:bg-slate-900/85 border border-amber-500/40 hover:border-amber-400 text-slate-100 hover:text-amber-200 text-xs sm:text-sm font-tech font-bold tracking-[0.2em] uppercase backdrop-blur-md shadow-[0_4px_20px_rgba(0,0,0,0.5)] transition-all cursor-pointer active:scale-95"
          >
            <div className="w-6 h-6 sm:w-7 sm:h-7 rounded-full bg-amber-400/25 group-hover:bg-amber-400 group-hover:text-slate-950 text-amber-300 flex items-center justify-center transition-colors">
              <Play className="w-3 h-3 sm:w-3.5 sm:h-3.5 fill-current ml-0.5" />
            </div>
            <span>NHẬP TRẬN ĐÚC BINH</span>
          </button>
        </div>
      </div>

      {/* 4. Vertical Poetic Calligraphy Text on the Right Edge (From Reference Image) */}
      <div className="hidden lg:flex fixed right-10 top-1/2 -translate-y-1/2 flex-col items-center gap-3 z-10 pointer-events-none select-none">
        <span className="text-amber-400/60 text-xs">✧</span>
        <div
          className="flex flex-col items-center text-xs tracking-[0.6em] text-slate-300/80 uppercase [writing-mode:vertical-rl]"
          style={{ fontFamily: "'Be Vietnam Pro', sans-serif" }}
        >
          <span>TU ĐẠO GIỮA NHÂN GIAN</span>
        </div>
        <span className="text-amber-400/60 text-xs">✧</span>
      </div>

      {/* 5. Bottom Status / Hints */}
      <div className="w-full max-w-7xl mx-auto flex items-center justify-between text-[11px] sm:text-xs text-slate-400/70 font-tech tracking-wider z-10 pt-2 border-t border-slate-800/40">
        <div>Space / Chạm: Đập Đe Canh Nhịp • Q W E R: 4 Thế Búa</div>
        <div className="font-mono text-amber-400/60">v2.4 · Phá Trời Khai Thiên</div>
      </div>
    </div>
  );
};
