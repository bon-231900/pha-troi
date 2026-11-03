import React, { useEffect, useState } from 'react';

interface LoadingScreenProps {
  onLoaded?: () => void;
  minDurationMs?: number;
}

export const LoadingScreen: React.FC<LoadingScreenProps> = ({
  onLoaded,
  minDurationMs = 700,
}) => {
  const [progress, setProgress] = useState(15);
  const [fading, setFading] = useState(false);
  const [hidden, setHidden] = useState(false);

  useEffect(() => {
    const startTime = performance.now();

    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval);
          return 100;
        }
        return Math.min(100, prev + Math.floor(Math.random() * 25 + 15));
      });
    }, 90);

    const checkComplete = () => {
      const elapsed = performance.now() - startTime;
      const remaining = Math.max(0, minDurationMs - elapsed);

      setTimeout(() => {
        setProgress(100);
        setTimeout(() => {
          setFading(true);
          setTimeout(() => {
            setHidden(true);
            onLoaded?.();
          }, 350);
        }, 150);
      }, remaining);
    };

    checkComplete();

    return () => clearInterval(interval);
  }, [minDurationMs, onLoaded]);

  if (hidden) return null;

  return (
    <div
      className={`fixed inset-0 z-50 flex flex-col items-center justify-center bg-[#04060C] select-none transition-opacity duration-300 ${
        fading ? 'opacity-0 pointer-events-none' : 'opacity-100'
      }`}
    >
      {/* Background radial celestial glow */}
      <div
        className="absolute inset-0 pointer-events-none"
        style={{
          background:
            'radial-gradient(circle at 50% 50%, rgba(255, 158, 0, 0.12) 0%, rgba(4, 6, 12, 0.95) 60%, #04060C 100%)',
        }}
      />

      <div className="relative z-10 flex flex-col items-center max-w-sm w-full px-6 text-center">
        {/* Animated Forging Anvil Icon */}
        <div className="relative mb-6">
          <div className="w-20 h-20 rounded-2xl bg-slate-900 border border-amber-500/40 flex items-center justify-center text-3xl shadow-xl shadow-amber-500/20">
            <span className="animate-bounce">🔨</span>
          </div>
          <div className="absolute -inset-1 rounded-2xl bg-amber-500/20 blur-md -z-10 animate-pulse" />
        </div>

        {/* Title */}
        <div className="text-xs font-tech uppercase tracking-[0.3em] text-amber-400/80 mb-1">
          PHÁ TRỜI · THE CELESTIAL FORGE
        </div>
        <h2 className="text-xl sm:text-2xl font-bold font-display text-slate-100 tracking-wider mb-6">
          ĐANG KHAI MỞ CỬU TRỌNG THIÊN
        </h2>

        {/* Progress Bar */}
        <div className="w-full bg-slate-900/80 border border-slate-800 rounded-full h-2 mb-3 overflow-hidden p-0.5">
          <div
            className="h-full bg-gradient-to-r from-amber-500 via-amber-400 to-cyan-400 rounded-full transition-all duration-150 ease-out shadow-sm shadow-amber-400/50"
            style={{ width: `${progress}%` }}
          />
        </div>

        {/* Progress percent */}
        <div className="flex justify-between w-full text-xs font-tech text-slate-400 mb-6">
          <span>Chuẩn bị lò rèn...</span>
          <span className="text-amber-400 font-bold">{progress}%</span>
        </div>

        {/* Hint Tip */}
        <div className="text-[11px] text-slate-400/80 bg-slate-900/60 border border-slate-800/80 rounded-xl px-3 py-2 max-w-xs leading-relaxed">
          💡 Canh chuẩn nhịp <b>100 BPM</b> khi vòng sóng chạm <b>Gờ Vàng Đe</b> để giáng búa Hoàng Kim x3.5!
        </div>
      </div>
    </div>
  );
};
