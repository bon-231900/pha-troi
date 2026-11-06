import React, { useState } from 'react';
import { soundEngine } from '../game/audio';
import { Play } from 'lucide-react';
import { GoogleUserProfile } from '../game/googleAuth';
import { TitlePagesOverlay, TitleNavTab } from './TitlePages';

interface TitleScreenModalProps {
  onStart: () => void;
  googleProfile?: GoogleUserProfile | null;
  onGoogleLogin?: () => void;
}

export const TitleScreenModal: React.FC<TitleScreenModalProps> = ({
  onStart,
  googleProfile = null,
  onGoogleLogin,
}) => {
  const [isStarting, setIsStarting] = useState(false);
  const [activeTab, setActiveTab] = useState<TitleNavTab>('home');

  const handleTabClick = (tab: TitleNavTab) => {
    setActiveTab(tab);
    soundEngine.unlockAudio();
    soundEngine.playAnvilStrike('GREAT', 'Q', false);
  };

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
        <button
          type="button"
          onClick={() => handleTabClick('home')}
          className="flex items-center gap-2 cursor-pointer bg-transparent border-none text-left p-0 transition-transform active:scale-95"
        >
          <div className="w-8 h-8 rounded-full border border-amber-400/50 flex items-center justify-center bg-slate-950/50 backdrop-blur-md shadow-[0_0_12px_rgba(255,180,0,0.3)]">
            <span className="text-amber-300 font-display font-bold text-xs">破</span>
          </div>
          <span className="font-display font-bold text-sm tracking-wider text-amber-200/90">PHÁ TRỜI</span>
        </button>

        {/* Center Nav items (Responsive for Mobile & Desktop) */}
        <nav className="flex items-center gap-3 sm:gap-6 md:gap-8 text-xs font-tech tracking-[0.18em] uppercase overflow-x-auto py-1 px-1 no-scrollbar">
          {[
            { tab: 'home' as TitleNavTab, label: 'TRANG CHỦ', href: './index.html' },
            { tab: 'world' as TitleNavTab, label: 'THẾ GIỚI', href: './the-gioi.html' },
            { tab: 'character' as TitleNavTab, label: 'NHÂN VẬT', href: './nhan-vat.html' },
            { tab: 'features' as TitleNavTab, label: 'TÍNH NĂNG', href: './tinh-nang.html' },
            { tab: 'news' as TitleNavTab, label: 'TIN TỨC', href: './tin-tuc.html' },
          ].map((item) => (
            <a
              key={item.tab}
              href={item.href}
              className={`transition-all pb-1 cursor-pointer whitespace-nowrap bg-transparent ${
                activeTab === item.tab
                  ? 'text-amber-300 font-bold border-b-2 border-amber-400 drop-shadow-[0_0_8px_rgba(251,191,36,0.6)]'
                  : 'text-slate-300/80 hover:text-amber-200 font-medium border-b-2 border-transparent hover:border-amber-400/30'
              }`}
            >
              {item.label}
            </a>
          ))}
        </nav>

        {/* Top-right Status */}
        <div className="flex items-center gap-2 text-xs font-tech text-amber-300/80 tracking-wider">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
          <span>MÁY CHỦ TOÀN CẦU ON</span>
        </div>
      </div>

      {/* 3. Main Hero Typography Block */}
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

        {/* Action Buttons: 1 là Google, 2 là Chế Độ Khách */}
        <div className="mt-5 flex flex-col sm:flex-row items-stretch sm:items-center gap-3 w-full sm:w-auto">
          {/* LỰA CHỌN 1: ĐĂNG NHẬP GOOGLE (HOẶC VÀO GAME NẾU ĐÃ CÓ ACC) */}
          {googleProfile ? (
            <button
              type="button"
              data-start="true"
              onClick={handleStart}
              disabled={isStarting}
              className="group flex items-center justify-center gap-3 px-7 py-3 rounded-full bg-gradient-to-r from-emerald-950/80 via-slate-900/90 to-emerald-950/80 hover:from-emerald-900/90 hover:to-slate-800 border border-emerald-400/70 hover:border-emerald-300 text-emerald-200 text-xs sm:text-sm font-tech font-bold tracking-[0.15em] uppercase backdrop-blur-md shadow-[0_4px_25px_rgba(16,185,129,0.35)] transition-all cursor-pointer active:scale-95"
            >
              {googleProfile.avatar ? (
                <img src={googleProfile.avatar} alt="Avatar" className="w-6 h-6 rounded-full border border-emerald-400" />
              ) : (
                <div className="w-6 h-6 rounded-full bg-emerald-500 text-slate-950 flex items-center justify-center font-bold text-xs">
                  {googleProfile.name.charAt(0)}
                </div>
              )}
              <span>NHẬP TRẬN · {googleProfile.name.toUpperCase()}</span>
            </button>
          ) : (
            <button
              type="button"
              onClick={() => {
                onGoogleLogin?.();
              }}
              disabled={isStarting}
              className="group flex items-center justify-center gap-3 px-7 py-3 rounded-full bg-slate-900/85 hover:bg-slate-900 border border-amber-400/70 hover:border-amber-300 text-slate-100 hover:text-amber-200 text-xs sm:text-sm font-tech font-bold tracking-[0.15em] uppercase backdrop-blur-md shadow-[0_4px_25px_rgba(255,190,40,0.25)] transition-all cursor-pointer active:scale-95"
              title="Đăng nhập Google để lưu trữ túi đồ và búa rèn vĩnh viễn trên mây"
            >
              <div className="w-6 h-6 rounded-full bg-white flex items-center justify-center p-1 shadow-sm">
                <svg className="w-full h-full" viewBox="0 0 24 24">
                  <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" />
                  <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" />
                  <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z" />
                  <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z" />
                </svg>
              </div>
              <span>ĐĂNG NHẬP GOOGLE</span>
            </button>
          )}

          {/* LỰA CHỌN 2: CHƠI CHẾ ĐỘ KHÁCH (GUEST) */}
          <button
            type="button"
            data-start="true"
            onClick={handleStart}
            disabled={isStarting}
            className="group flex items-center justify-center gap-2 px-6 py-2.5 rounded-full bg-slate-950/60 hover:bg-slate-900/80 border border-slate-700/60 hover:border-slate-500 text-slate-300 hover:text-white text-xs font-tech font-semibold tracking-wider transition-all cursor-pointer active:scale-95"
            title="Chơi ngay không cần đăng nhập (Tiến độ chỉ lưu trên trình duyệt này)"
          >
            <Play className="w-3 h-3 fill-current text-slate-400 group-hover:text-amber-300 transition-colors" />
            <span>CHƠI CHẾ ĐỘ KHÁCH →</span>
          </button>
        </div>
      </div>

      {/* 4. Vertical Poetic Calligraphy Text on the Right Edge */}
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

      {/* 5. Bottom Status, Controls & Legal Links */}
      <div className="w-full max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between text-[11px] sm:text-xs text-slate-400/70 font-tech tracking-wider z-10 pt-3 border-t border-slate-800/40 gap-2">
        <div>Space / Chạm: Đập Đe Canh Nhịp • Q W E R: 4 Thế Búa</div>
        <div className="flex items-center gap-3 text-slate-500">
          <a href="./privacy.html" target="_blank" rel="noopener noreferrer" className="hover:text-amber-400 transition underline">
            Chính Sách Bảo Mật
          </a>
          <span>·</span>
          <a href="./terms.html" target="_blank" rel="noopener noreferrer" className="hover:text-amber-400 transition underline">
            Điều Khoản
          </a>
          <span>·</span>
          <span className="font-mono text-amber-400/60">v3.2 Cloud Edition</span>
        </div>
      </div>

      {/* 6. Rich Informational Pages Overlay (Thế Giới, Nhân Vật, Tính Năng, Tin Tức) */}
      <TitlePagesOverlay
        activeTab={activeTab}
        onSelectTab={handleTabClick}
        onStartGame={handleStart}
      />
    </div>
  );
};
