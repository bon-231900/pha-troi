import React from 'react';

interface StatusModalProps {
  mode: 'paused' | 'gameover';
  playerTotalDamage?: number;
  playerTotalDamageBillions?: number; // legacy fallback
  maxCombo: number;
  perfectCount: number;
  onResume: () => void;
  onRestart: () => void;
  onReturnTitle: () => void;
}

export const StatusModal: React.FC<StatusModalProps> = ({
  mode,
  playerTotalDamage,
  playerTotalDamageBillions,
  maxCombo,
  perfectCount,
  onResume,
  onRestart,
  onReturnTitle,
}) => {
  const currentDamage = Math.round(
    typeof playerTotalDamage === 'number'
      ? playerTotalDamage
      : (playerTotalDamageBillions || 0) * 1e9
  );

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-label={mode === 'paused' ? 'Tạm Dừng Lò Rèn' : 'Đại Thắng Phá Trời'}
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80"
    >
      <div className="w-full max-w-md rounded-2xl bg-[#111625] border border-amber-400/50 p-6 text-center shadow-2xl">
        <div className="text-xs font-tech tracking-[0.2em] text-cyan-300 uppercase mb-1">
          {mode === 'paused' ? 'Tạm Ngưng Nhịp Búa' : 'Thiên Ma Bại Trận · Cửu Trọng Khai Mở'}
        </div>
        <h2 className="font-display text-2xl md:text-3xl font-extrabold text-amber-300 mb-4">
          {mode === 'paused' ? 'LÒ RÈN TẠM DỪNG' : 'ĐẠI THẮNG PHÁ TRỜI'}
        </h2>

        {/* 3 Tabular Stat Tiles */}
        <div className="grid grid-cols-3 gap-2.5 my-5 font-tech">
          <div className="p-3 rounded-xl bg-[#080A10] border border-slate-800">
            <div className="text-[11px] text-slate-400">Tổng Công Phá</div>
            <div className="text-base font-bold text-amber-300">
              {currentDamage.toLocaleString('en-US')}
            </div>
          </div>
          <div className="p-3 rounded-xl bg-[#080A10] border border-slate-800">
            <div className="text-[11px] text-slate-400">Đỉnh Combo</div>
            <div className="text-base font-bold text-cyan-300">{maxCombo}</div>
          </div>
          <div className="p-3 rounded-xl bg-[#080A10] border border-slate-800">
            <div className="text-[11px] text-slate-400">Nhịp Hoàng Kim</div>
            <div className="text-base font-bold text-red-400">{perfectCount}</div>
          </div>
        </div>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-2.5">
          {mode === 'paused' ? (
            <>
              <button
                type="button"
                onClick={onResume}
                className="w-full sm:w-auto px-5 py-2.5 rounded-xl bg-amber-400 hover:bg-amber-300 text-slate-950 font-tech font-bold text-sm shadow-md cursor-pointer transition-colors"
              >
                TIẾP TỤC RÈN ĐÚC
              </button>
              <button
                type="button"
                onClick={onRestart}
                className="w-full sm:w-auto px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 font-tech font-semibold text-sm cursor-pointer transition-colors"
              >
                RÈN LẠI TỪ ĐẦU
              </button>
            </>
          ) : (
            <>
              <button
                type="button"
                onClick={onRestart}
                className="w-full sm:w-auto px-5 py-2.5 rounded-xl bg-amber-400 hover:bg-amber-300 text-slate-950 font-tech font-bold text-sm shadow-md cursor-pointer transition-colors"
              >
                TIẾN VÀO TẦNG TIẾP THEO
              </button>
              <button
                type="button"
                onClick={onReturnTitle}
                className="w-full sm:w-auto px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 font-tech font-semibold text-sm cursor-pointer transition-colors"
              >
                VỀ TRANG CHỦ
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  );
};