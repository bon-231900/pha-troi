import React, { useState } from 'react';
import { Hammer, Flame, Zap, Shield, Gift, ChevronDown, ChevronUp, X, Sparkles, ArrowRight } from 'lucide-react';

export interface BeginnerTutorialGuideProps {
  currentStep: number; // 1 to 4
  strikesCount: number; // 0 to 3
  heatStrikesCount: number; // 0 to 5
  hasUsedSkill: boolean;
  rightPanelOpen: boolean;
  playerClassName: string;
  onClaimReward: () => void;
  onSkipTutorial: () => void;
  onOpenForgePanel: () => void;
}

export const BeginnerTutorialGuide: React.FC<BeginnerTutorialGuideProps> = ({
  currentStep,
  strikesCount,
  heatStrikesCount,
  hasUsedSkill,
  rightPanelOpen,
  playerClassName,
  onClaimReward,
  onSkipTutorial,
  onOpenForgePanel,
}) => {
  const [minimized, setMinimized] = useState<boolean>(false);
  const [showSkipConfirm, setShowSkipConfirm] = useState<boolean>(false);

  // Completed steps calculation
  const isStep1Done = strikesCount >= 3 || currentStep > 1;
  const isStep2Done = heatStrikesCount >= 5 || currentStep > 2;
  const isStep3Done = hasUsedSkill || currentStep > 3;
  const isStep4Done = rightPanelOpen || currentStep > 4;

  const currentDisplayStep = Math.min(4, Math.max(1, currentStep));

  return (
    <aside
      aria-label="Chỉ dẫn tân thủ nhập môn"
      className="fixed top-[64px] sm:top-[74px] right-2 sm:right-4 z-35 max-w-[calc(100vw-16px)] sm:max-w-[390px] w-full select-none pointer-events-auto transition-all duration-300"
    >
      {/* Mini Bar when Minimized */}
      {minimized ? (
        <div
          onClick={() => setMinimized(false)}
          className="flex items-center justify-between px-3.5 py-2 rounded-xl bg-[#090D1A]/95 border border-amber-500/60 shadow-[0_4px_20px_rgba(245,158,11,0.25)] backdrop-blur-md cursor-pointer hover:border-amber-400 group transition-all"
        >
          <div className="flex items-center gap-2">
            <span className="flex h-2.5 w-2.5 relative">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-amber-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-amber-500"></span>
            </span>
            <span className="text-xs font-tech font-bold text-amber-300 tracking-wider">
              📜 CHỈ DẪN TÂN THỦ · BƯỚC {currentDisplayStep}/4
            </span>
          </div>
          <div className="flex items-center gap-1.5">
            <button
              type="button"
              className="text-amber-400 hover:text-amber-200 p-0.5 rounded transition"
              title="Mở rộng hướng dẫn"
            >
              <ChevronDown className="w-4 h-4" />
            </button>
            <button
              type="button"
              onClick={(e) => {
                e.stopPropagation();
                setShowSkipConfirm(true);
              }}
              className="text-slate-400 hover:text-rose-400 p-0.5 rounded transition"
              title="Đóng hướng dẫn"
            >
              <X className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      ) : (
        /* Full Scroll Guide Container */
        <div className="relative rounded-2xl bg-gradient-to-b from-[#0c1222]/98 via-[#090e1c]/98 to-[#060812]/98 border-2 border-amber-500/70 shadow-[0_8px_32px_rgba(0,0,0,0.8),0_0_20px_rgba(245,158,11,0.2)] backdrop-blur-xl overflow-hidden p-3.5 sm:p-4 text-slate-100 font-tech">
          {/* Top Decorative Ambient Glow */}
          <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-amber-500 via-orange-400 to-amber-500" />

          {/* Header */}
          <div className="flex items-center justify-between pb-2.5 mb-2.5 border-b border-amber-500/20">
            <div className="flex items-center gap-2">
              <div className="w-7 h-7 rounded-lg bg-amber-500/20 border border-amber-400/50 flex items-center justify-center text-amber-300 shadow-[0_0_10px_rgba(245,158,11,0.3)]">
                <Sparkles className="w-4 h-4" />
              </div>
              <div>
                <div className="text-[10px] text-amber-400 font-bold uppercase tracking-widest flex items-center gap-1">
                  <span>Tiên Lò Truyền Âm</span>
                  <span className="text-slate-500">•</span>
                  <span className="text-cyan-400">{playerClassName}</span>
                </div>
                <h4 className="text-xs sm:text-sm font-bold text-amber-200 tracking-wide">
                  Thiên Khởi · Nhập Môn Thần Đúc
                </h4>
              </div>
            </div>

            <div className="flex items-center gap-1">
              <button
                type="button"
                onClick={() => setMinimized(true)}
                className="p-1 rounded-lg hover:bg-slate-800/60 text-slate-400 hover:text-slate-200 transition cursor-pointer"
                title="Thu gọn"
              >
                <ChevronUp className="w-4 h-4" />
              </button>
              <button
                type="button"
                onClick={() => setShowSkipConfirm(true)}
                className="px-2 py-0.5 rounded-md hover:bg-rose-950/40 border border-transparent hover:border-rose-500/40 text-[10px] text-slate-400 hover:text-rose-300 transition cursor-pointer"
                title="Bỏ qua hướng dẫn"
              >
                Bỏ qua
              </button>
              <button
                type="button"
                onClick={() => setShowSkipConfirm(true)}
                className="p-1 rounded-lg hover:bg-rose-950/60 text-slate-400 hover:text-rose-300 transition cursor-pointer ml-0.5"
                title="Đóng vĩnh viễn"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          </div>

          {/* Skip Confirmation Overlay */}
          {showSkipConfirm && (
            <div className="absolute inset-0 z-20 bg-black/90 backdrop-blur-sm p-4 flex flex-col justify-center items-center text-center rounded-2xl border border-rose-500/50">
              <h5 className="text-sm font-bold text-amber-300 mb-1">Đạo hữu muốn bỏ qua hướng dẫn?</h5>
              <p className="text-xs text-slate-300 mb-4 leading-relaxed">
                Đừng lo! Bạn vẫn sẽ nhận được trọn vẹn <span className="text-amber-400 font-bold">+500 Linh Thạch</span> và <span className="text-cyan-400 font-bold">+50 Bụi Thiết</span> nhập môn.
              </p>
              <div className="flex items-center gap-2">
                <button
                  type="button"
                  onClick={() => setShowSkipConfirm(false)}
                  className="px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-bold text-slate-200 cursor-pointer"
                >
                  Quay lại làm tiếp
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setShowSkipConfirm(false);
                    onSkipTutorial();
                  }}
                  className="px-3.5 py-1.5 rounded-xl bg-gradient-to-r from-amber-600 to-amber-500 hover:from-amber-500 hover:to-amber-400 text-xs font-bold text-slate-950 shadow-md cursor-pointer"
                >
                  Bỏ qua & Nhận quà 🎁
                </button>
              </div>
            </div>
          )}

          {/* Stepper Progress Indicator (4 Steps) */}
          <div className="grid grid-cols-4 gap-1.5 mb-3.5">
            {[
              { num: 1, label: 'Đập Búa', done: isStep1Done },
              { num: 2, label: 'Thổi Lửa', done: isStep2Done },
              { num: 3, label: 'Tuyệt Kỹ', done: isStep3Done },
              { num: 4, label: 'Lò Rèn', done: isStep4Done },
            ].map((s) => {
              const isCurrent = currentDisplayStep === s.num;
              return (
                <div key={s.num} className="flex flex-col items-center">
                  <div
                    className={`w-full h-1.5 rounded-full mb-1 transition-all ${
                      s.done
                        ? 'bg-emerald-500 shadow-[0_0_8px_#10B981]'
                        : isCurrent
                        ? 'bg-amber-400 animate-pulse shadow-[0_0_8px_#F59E0B]'
                        : 'bg-slate-800'
                    }`}
                  />
                  <span
                    className={`text-[9px] font-bold truncate ${
                      s.done ? 'text-emerald-400' : isCurrent ? 'text-amber-300 font-extrabold' : 'text-slate-600'
                    }`}
                  >
                    {s.num}. {s.label}
                  </span>
                </div>
              );
            })}
          </div>

          {/* Current Step Body */}
          <div className="space-y-3">
            {/* STEP 1: Hammer Strike */}
            {currentDisplayStep === 1 && (
              <div className="p-3 rounded-xl bg-amber-950/20 border border-amber-500/40 relative overflow-hidden">
                <div className="flex items-start gap-2.5">
                  <div className="w-8 h-8 rounded-lg bg-amber-500/20 border border-amber-400/60 flex items-center justify-center text-amber-300 shrink-0 mt-0.5">
                    <Hammer className="w-4 h-4 animate-bounce" />
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-xs font-bold text-amber-300">Bước 1: Khởi Lực Đập Búa</span>
                      <span className="text-xs font-bold text-amber-400 tabular-nums">
                        {Math.min(3, strikesCount)} / 3 nhát
                      </span>
                    </div>
                    <p className="text-[11px] text-slate-300 leading-relaxed mb-2">
                      Nhấp chuột trực tiếp vào <span className="text-amber-300 font-bold">Bàn Đe</span> giữa màn hình (hoặc bấm <span className="text-amber-300 font-bold">[SPACE]</span> / nút <span className="text-amber-300 font-bold">[GÕ BÚA]</span>) để ra đòn!
                    </p>
                    {/* Progress Bar */}
                    <div className="w-full bg-slate-900 rounded-full h-2 border border-slate-800 overflow-hidden">
                      <div
                        className="bg-gradient-to-r from-amber-500 to-amber-300 h-full transition-all duration-300"
                        style={{ width: `${Math.min(100, (strikesCount / 3) * 100)}%` }}
                      />
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* STEP 2: Heat Up Furnace */}
            {currentDisplayStep === 2 && (
              <div className="p-3 rounded-xl bg-orange-950/25 border border-orange-500/50 relative overflow-hidden">
                <div className="flex items-start gap-2.5">
                  <div className="w-8 h-8 rounded-lg bg-orange-500/20 border border-orange-400/60 flex items-center justify-center text-orange-400 shrink-0 mt-0.5">
                    <Flame className="w-4 h-4 animate-pulse text-orange-400" />
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-xs font-bold text-orange-300">Bước 2: Thổi Bùng Hỏa Lò</span>
                      <span className="text-xs font-bold text-orange-400 tabular-nums">
                        {Math.min(5, heatStrikesCount)} / 5 nhát liên kích
                      </span>
                    </div>
                    <p className="text-[11px] text-slate-300 leading-relaxed mb-2">
                      Gõ liên tục để thổi bùng nhiệt lò! Khi đạt <span className="text-orange-400 font-bold">🔥 Nung</span>, giáp boss sẽ bị nung chảy và nhận gấp đôi sát thương.
                    </p>
                    {/* Progress Bar */}
                    <div className="w-full bg-slate-900 rounded-full h-2 border border-slate-800 overflow-hidden">
                      <div
                        className="bg-gradient-to-r from-red-500 via-orange-500 to-amber-400 h-full transition-all duration-300"
                        style={{ width: `${Math.min(100, (heatStrikesCount / 5) * 100)}%` }}
                      />
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* STEP 3: Cast Class Skill */}
            {currentDisplayStep === 3 && (
              <div className="p-3 rounded-xl bg-cyan-950/25 border border-cyan-500/50 relative overflow-hidden">
                <div className="flex items-start gap-2.5">
                  <div className="w-8 h-8 rounded-lg bg-cyan-500/20 border border-cyan-400/60 flex items-center justify-center text-cyan-300 shrink-0 mt-0.5">
                    <Zap className="w-4 h-4 animate-bounce text-cyan-400" />
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-xs font-bold text-cyan-300">Bước 3: Thức Tỉnh Tuyệt Kỹ</span>
                      <span className="text-[10px] px-1.5 py-0.5 rounded bg-cyan-900/60 border border-cyan-500/50 text-cyan-300 font-bold">
                        ĐÃ NẠP SẴN NỘ
                      </span>
                    </div>
                    <p className="text-[11px] text-slate-300 leading-relaxed mb-2">
                      Năng lượng Thần Lực (Overdrive) đã sẵn sàng! Bấm phím <span className="text-cyan-300 font-bold">[W]</span> hoặc click vào biểu tượng kỹ năng góc dưới trái để giải phóng uy lực!
                    </p>
                    <div className="flex items-center gap-1.5 text-[10px] text-emerald-400 font-bold">
                      <span className="inline-block w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
                      <span>Nhấp vào icon kỹ năng hoặc bấm phím W ngay!</span>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* STEP 4: Open Forge & Claim Welcome Gift */}
            {currentDisplayStep === 4 && (
              <div className="p-3 rounded-xl bg-emerald-950/25 border border-emerald-500/50 relative overflow-hidden">
                <div className="flex items-start gap-2.5 mb-2.5">
                  <div className="w-8 h-8 rounded-lg bg-emerald-500/20 border border-emerald-400/60 flex items-center justify-center text-emerald-300 shrink-0 mt-0.5">
                    <Shield className="w-4 h-4 text-emerald-400" />
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-xs font-bold text-emerald-300">Bước 4: Khám Phá Lò Rèn</span>
                      <span className="text-[10px] text-amber-400 font-bold">BƯỚC CUỐI</span>
                    </div>
                    <p className="text-[11px] text-slate-300 leading-relaxed">
                      Bấm nút <span className="text-amber-300 font-bold">[LÒ RÈN]</span> góc trên bên phải (hoặc phím <span className="text-amber-300 font-bold">[ ] ]</span>) để diện kiến Lục Đại Thần Khí!
                    </p>
                  </div>
                </div>

                {!rightPanelOpen ? (
                  <button
                    type="button"
                    onClick={onOpenForgePanel}
                    className="w-full py-2 px-3 rounded-xl bg-gradient-to-r from-amber-600 via-amber-500 to-yellow-500 hover:from-amber-500 hover:to-yellow-400 text-slate-950 font-bold text-xs shadow-[0_0_15px_rgba(245,158,11,0.4)] flex items-center justify-center gap-1.5 cursor-pointer active:scale-95 transition-all"
                  >
                    <span>MỞ BẢNG LÒ RÈN NGAY</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </button>
                ) : (
                  <div className="pt-2 border-t border-emerald-500/30 text-center">
                    <div className="text-[11px] text-amber-300 font-bold mb-2 flex items-center justify-center gap-1">
                      <Sparkles className="w-3.5 h-3.5 text-amber-400 animate-spin" />
                      <span>Chúc mừng đạo hữu nhập môn thành công!</span>
                    </div>
                    {/* Welcome Gift Box */}
                    <button
                      type="button"
                      onClick={onClaimReward}
                      className="w-full py-2.5 px-4 rounded-xl bg-gradient-to-r from-yellow-500 via-amber-400 to-orange-500 hover:brightness-110 text-slate-950 font-bold text-xs sm:text-sm shadow-[0_0_20px_rgba(251,191,36,0.6)] flex items-center justify-center gap-2 cursor-pointer active:scale-95 transition-all animate-pulse"
                    >
                      <Gift className="w-4 h-4 text-slate-950" />
                      <span>NHẬN QUÀ TÂN THỦ (+500 LT & +50 BỤI THIẾT)</span>
                    </button>
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Reward Preview Footer */}
          <div className="mt-3 pt-2.5 border-t border-slate-800 flex items-center justify-between text-[10px] text-slate-400">
            <span className="flex items-center gap-1 text-slate-400">
              <Gift className="w-3 h-3 text-amber-400" />
              <span>Phần thưởng hoàn thành:</span>
            </span>
            <div className="flex items-center gap-2 font-bold">
              <span className="text-amber-300">+500 Linh Thạch</span>
              <span className="text-slate-600">•</span>
              <span className="text-cyan-300">+50 Bụi Thiết</span>
            </div>
          </div>
        </div>
      )}
    </aside>
  );
};
