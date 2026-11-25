import React, { useState } from 'react';
import { Hammer, Flame, Zap, Shield, Sparkles, X, BookOpen, Layers, HeartHandshake } from 'lucide-react';

export interface ForgeGuideHelpModalProps {
  isOpen: boolean;
  onClose: () => void;
  playerClassName?: string;
}

export const ForgeGuideHelpModal: React.FC<ForgeGuideHelpModalProps> = ({
  isOpen,
  onClose,
  playerClassName = 'Thần Đúc Giả',
}) => {
  const [activeTab, setActiveTab] = useState<'basics' | 'furnace' | 'skills' | 'forge' | 'raid'>('basics');

  if (!isOpen) return null;

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-label="Cẩm nang bí kíp rèn đúc"
      className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-4 bg-black/80 backdrop-blur-md select-none pointer-events-auto"
      onClick={onClose}
    >
      <div
        className="relative w-full max-w-2xl bg-gradient-to-b from-[#0c1222] via-[#090e1c] to-[#060812] border-2 border-amber-500/60 rounded-2xl shadow-[0_10px_40px_rgba(0,0,0,0.9),0_0_25px_rgba(245,158,11,0.25)] overflow-hidden flex flex-col max-h-[90vh] text-slate-100 font-tech"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Top Decorative Amber Line */}
        <div className="h-1.5 bg-gradient-to-r from-amber-500 via-orange-400 to-amber-500 w-full" />

        {/* Modal Header */}
        <div className="flex items-center justify-between px-5 py-4 border-b border-amber-500/20 bg-slate-900/40">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-amber-500/20 border border-amber-400/50 flex items-center justify-center text-amber-300 shadow-[0_0_12px_rgba(245,158,11,0.3)]">
              <BookOpen className="w-5 h-5" />
            </div>
            <div>
              <div className="text-[10px] text-amber-400 font-bold uppercase tracking-widest flex items-center gap-1.5">
                <span>Cẩm Nang Bí Kíp</span>
                <span className="text-slate-500">•</span>
                <span className="text-cyan-400">{playerClassName}</span>
              </div>
              <h3 className="text-base sm:text-lg font-bold text-amber-200">
                Thiên Cổ Bí Truyền · Hướng Dẫn Quy Tắc Rèn
              </h3>
            </div>
          </div>
          <button
            type="button"
            onClick={onClose}
            className="w-9 h-9 rounded-full bg-slate-800/80 hover:bg-rose-950 border border-slate-700 hover:border-rose-500/50 flex items-center justify-center text-slate-300 hover:text-rose-300 transition cursor-pointer"
            title="Đóng [ESC]"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Navigation Tabs */}
        <div className="flex items-center gap-1 px-4 py-2 bg-[#080c16] border-b border-slate-800 overflow-x-auto scrollbar-none">
          {[
            { id: 'basics', label: '1. Đập Búa & Combo', icon: Hammer },
            { id: 'furnace', label: '2. Hỏa Lò & Giáp Nung', icon: Flame },
            { id: 'skills', label: '3. Nộ Khí & Chiêu Thức', icon: Zap },
            { id: 'forge', label: '4. Lục Đại Thần Khí', icon: Shield },
            { id: 'raid', label: '5. Độ Bền Đe Server', icon: HeartHandshake },
          ].map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                type="button"
                onClick={() => setActiveTab(tab.id as any)}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-bold transition-all whitespace-nowrap cursor-pointer ${
                  isActive
                    ? 'bg-amber-500/20 border border-amber-400/70 text-amber-300 shadow-[0_0_10px_rgba(245,158,11,0.2)]'
                    : 'bg-slate-900/40 border border-transparent text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
                }`}
              >
                <Icon className={`w-3.5 h-3.5 ${isActive ? 'text-amber-400' : 'text-slate-500'}`} />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </div>

        {/* Tab Content Body */}
        <div className="p-5 overflow-y-auto space-y-4 flex-1">
          {/* TAB 1: BASICS */}
          {activeTab === 'basics' && (
            <div className="space-y-4">
              <div className="p-4 rounded-xl bg-amber-950/20 border border-amber-500/30 flex items-start gap-3">
                <Hammer className="w-6 h-6 text-amber-400 shrink-0 mt-0.5" />
                <div>
                  <h4 className="text-sm font-bold text-amber-300 mb-1">Cách Thao Tác Gõ Búa</h4>
                  <p className="text-xs text-slate-300 leading-relaxed">
                    Bạn có thể gõ búa bằng cách <strong className="text-amber-200">nhấp chuột vào Bàn Đe</strong> ở giữa màn hình, bấm <strong className="text-amber-200">Phím Cách [SPACE]</strong> trên bàn phím, hoặc bấm nút <strong className="text-amber-200">[GÕ BÚA]</strong> trên điện thoại.
                  </p>
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800">
                  <div className="text-xs font-bold text-cyan-300 mb-1 flex items-center gap-1.5">
                    <Sparkles className="w-4 h-4 text-cyan-400" />
                    <span>Đòn Đánh Hoàng Kim (Perfect Strike)</span>
                  </div>
                  <p className="text-xs text-slate-400 leading-relaxed">
                    Gõ búa với nhịp điệu chính xác sẽ kích hoạt đòn đánh Hoàng Kim, nhân đôi sát thương và nạp thanh Thần Lực nhanh gấp đôi.
                  </p>
                </div>

                <div className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800">
                  <div className="text-xs font-bold text-orange-300 mb-1 flex items-center gap-1.5">
                    <Layers className="w-4 h-4 text-orange-400" />
                    <span>Chuỗi Combo Liên Hoàn</span>
                  </div>
                  <p className="text-xs text-slate-400 leading-relaxed">
                    Duy trì nhịp gõ đều đặn sẽ tích lũy chuỗi Combo. Cứ mỗi mốc combo cao sẽ kích hoạt buff sát thương lan tỏa cho toàn xưởng rèn.
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* TAB 2: FURNACE */}
          {activeTab === 'furnace' && (
            <div className="space-y-4">
              <div className="p-4 rounded-xl bg-orange-950/25 border border-orange-500/40 flex items-start gap-3">
                <Flame className="w-6 h-6 text-orange-400 shrink-0 mt-0.5" />
                <div>
                  <h4 className="text-sm font-bold text-orange-300 mb-1">Cơ Chế Hỏa Lò & Trạng Thái Nung Chảy</h4>
                  <p className="text-xs text-slate-300 leading-relaxed">
                    Boss Thiết Vân Vòm có lớp giáp sắt cực kỳ kiên cố (giảm tới 80% sát thương thường). Để phá vỡ giáp này, người chơi phải <strong className="text-orange-200">gõ búa liên tục để tăng nhiệt độ Hỏa Lò</strong>.
                  </p>
                </div>
              </div>

              <div className="space-y-2.5 text-xs text-slate-300 bg-slate-900/50 p-4 rounded-xl border border-slate-800">
                <div className="flex items-center gap-2">
                  <span className="w-2.5 h-2.5 rounded-full bg-cyan-400"></span>
                  <span><strong>Lò Nguội (&lt; ngưỡng nung):</strong> Boss giữ nguyên lớp Thiết Bì cứng rắn (-80% sát thương).</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="w-2.5 h-2.5 rounded-full bg-orange-400"></span>
                  <span><strong>Lò Nung (🔥 Nung):</strong> Giáp sắt bị nung chảy mềm rụm, sát thương tăng gấp đôi!</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="w-2.5 h-2.5 rounded-full bg-red-500 animate-pulse"></span>
                  <span><strong>Lò Quá Nhiệt (&gt; 6,000°C):</strong> Sát thương bạo kích tối đa, đòn đánh bùng nổ vệt lửa!</span>
                </div>
                <div className="pt-2 border-t border-slate-800 text-[11px] text-amber-400">
                  💡 <em>Lưu ý: Nếu người chơi ngừng gõ hoặc AFK, Hỏa Lò sẽ hạ nhiệt tự nhiên dần về mức bình thường. Hãy chăm chỉ giữ lửa!</em>
                </div>
              </div>
            </div>
          )}

          {/* TAB 3: SKILLS */}
          {activeTab === 'skills' && (
            <div className="space-y-4">
              <div className="p-4 rounded-xl bg-cyan-950/25 border border-cyan-500/40 flex items-start gap-3">
                <Zap className="w-6 h-6 text-cyan-400 shrink-0 mt-0.5" />
                <div>
                  <h4 className="text-sm font-bold text-cyan-300 mb-1">Thanh Thần Lực (Overdrive) & Bộ Kỹ Năng Q W E R</h4>
                  <p className="text-xs text-slate-300 leading-relaxed">
                    Mỗi lần gõ búa sẽ nạp đầy dần thanh Nộ (tối đa 3 điểm OD). Khi đủ nộ khí, bạn có thể giải phóng tuyệt kỹ môn phái bằng các phím <strong className="text-cyan-300">[W]</strong>, <strong className="text-cyan-300">[E]</strong>, <strong className="text-cyan-300">[R]</strong>.
                  </p>
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                <div className="p-3 rounded-xl bg-slate-900/60 border border-cyan-500/30">
                  <div className="text-xs font-bold text-cyan-300 mb-1">⚡ Phái Lôi (Sấm Sét)</div>
                  <p className="text-[11px] text-slate-400 leading-relaxed">
                    Tập trung vào Bạo Kích sấm sét, phóng lôi đình rực trời, gây sốc sát thương cực đại lên Thiết Vòm.
                  </p>
                </div>
                <div className="p-3 rounded-xl bg-slate-900/60 border border-orange-500/30">
                  <div className="text-xs font-bold text-orange-300 mb-1">🔥 Phái Hỏa (Hỏa Diệm)</div>
                  <p className="text-[11px] text-slate-400 leading-relaxed">
                    Bơm nhiệt độ lò lên mốc Quá Nhiệt (+2,000°C), thiêu đốt liên tục và khóa nhiệt độ không bị nguội trong 15 giây!
                  </p>
                </div>
                <div className="p-3 rounded-xl bg-slate-900/60 border border-emerald-500/30">
                  <div className="text-xs font-bold text-emerald-300 mb-1">🎵 Thể Đạo / Sóng Âm</div>
                  <p className="text-[11px] text-slate-400 leading-relaxed">
                    Sử dụng sóng âm tiên thiên, tạo ngọc bích hộ thể và sửa chữa Độ Bền Đe cho toàn bộ người chơi trong server.
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* TAB 4: FORGE */}
          {activeTab === 'forge' && (
            <div className="space-y-4">
              <div className="p-4 rounded-xl bg-emerald-950/25 border border-emerald-500/40 flex items-start gap-3">
                <Shield className="w-6 h-6 text-emerald-400 shrink-0 mt-0.5" />
                <div>
                  <h4 className="text-sm font-bold text-emerald-300 mb-1">Lục Đại Bản Mệnh Thần Khí</h4>
                  <p className="text-xs text-slate-300 leading-relaxed">
                    Mở bảng <strong className="text-amber-300">[LÒ RÈN]</strong> (phím <strong className="text-amber-300">[ ] ]</strong>) để xem và Tôi Luyện 6 món trang bị vĩnh cửu.
                  </p>
                </div>
              </div>

              <div className="grid grid-cols-2 sm:grid-cols-3 gap-2.5 text-xs">
                <div className="p-2.5 rounded-lg bg-slate-900/60 border border-slate-800">
                  <div className="font-bold text-amber-300">🔨 Thần Chùy</div>
                  <div className="text-[11px] text-slate-400">Tăng Sát Thương gõ búa</div>
                </div>
                <div className="p-2.5 rounded-lg bg-slate-900/60 border border-slate-800">
                  <div className="font-bold text-amber-300">⚒️ Thần Đe</div>
                  <div className="text-[11px] text-slate-400">Tăng Tỷ Lệ Bạo Kích</div>
                </div>
                <div className="p-2.5 rounded-lg bg-slate-900/60 border border-slate-800">
                  <div className="font-bold text-amber-300">🔥 Hỏa Lò</div>
                  <div className="text-[11px] text-slate-400">Tăng Lửa nung mỗi nhát</div>
                </div>
                <div className="p-2.5 rounded-lg bg-slate-900/60 border border-slate-800">
                  <div className="font-bold text-amber-300">🧤 Bao Tay Rèn</div>
                  <div className="text-[11px] text-slate-400">Tăng Bạo Kích & Tốc độ</div>
                </div>
                <div className="p-2.5 rounded-lg bg-slate-900/60 border border-slate-800">
                  <div className="font-bold text-amber-300">🛡️ Tạp Dề Thiết Hộ</div>
                  <div className="text-[11px] text-slate-400">Tăng Linh Thạch / phút</div>
                </div>
                <div className="p-2.5 rounded-lg bg-slate-900/60 border border-slate-800">
                  <div className="font-bold text-amber-300">🔮 Định Thiên Pháp Bảo</div>
                  <div className="text-[11px] text-slate-400">Tăng Tổng Sát Thương</div>
                </div>
              </div>
            </div>
          )}

          {/* TAB 5: RAID ANVIL */}
          {activeTab === 'raid' && (
            <div className="space-y-4">
              <div className="p-4 rounded-xl bg-purple-950/25 border border-purple-500/40 flex items-start gap-3">
                <HeartHandshake className="w-6 h-6 text-purple-400 shrink-0 mt-0.5" />
                <div>
                  <h4 className="text-sm font-bold text-purple-300 mb-1">Bảo Vệ Độ Bền Đe Toàn Dân</h4>
                  <p className="text-xs text-slate-300 leading-relaxed">
                    Bàn đe rèn là pháp trận kết nối toàn bộ người chơi trực tuyến. Boss Thiết Vân Vòm theo chu kỳ sẽ giáng sét bão tố làm sụt giảm Độ Bền Đe.
                  </p>
                </div>
              </div>

              <div className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800 text-xs text-slate-300 space-y-2">
                <p>
                  🛡️ Khi Độ Bền Đe xuống thấp (&lt; 20%), toàn bộ xưởng rèn sẽ rơi vào trạng thái báo động đỏ.
                </p>
                <p>
                  ✨ Các thợ rèn gõ đòn Perfect hoặc dùng chiêu thức hộ thể sẽ tự động bơm máu sửa chữa lại Đe Thần.
                </p>
              </div>
            </div>
          )}
        </div>

        {/* Modal Footer */}
        <div className="px-5 py-3 border-t border-slate-800 bg-slate-900/60 flex items-center justify-between">
          <div className="text-[11px] text-slate-400">
            Mẹo: Bấm <strong className="text-amber-300">[?]</strong> trên thanh tiêu đề để mở lại cẩm nang này bất kỳ lúc nào.
          </div>
          <button
            type="button"
            onClick={onClose}
            className="px-4 py-2 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold text-xs cursor-pointer shadow-md transition-all active:scale-95"
          >
            Đã Hiểu
          </button>
        </div>
      </div>
    </div>
  );
};
