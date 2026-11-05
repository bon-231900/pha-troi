import React from 'react';
import { PlayerClassMeta } from '../game/rules';
import { HEADER_ICON_ASSETS, HEADER_FRAME_ASSETS } from '../game/headerArtAssets';

interface StatusModalProps {
  mode: 'paused' | 'gameover';
  playerTotalDamage?: number;
  playerTotalDamageBillions?: number; // legacy fallback
  maxCombo: number;
  perfectCount: number;
  onResume: () => void;
  onRestart: () => void;
  onReturnTitle: () => void;
  onSwitchCharacter?: () => void;
  muted?: boolean;
  onToggleMute?: () => void;
  playerClass?: PlayerClassMeta;
  activeCharacterName?: string;
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
  onSwitchCharacter,
  muted = false,
  onToggleMute,
  playerClass,
  activeCharacterName,
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
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/85 backdrop-blur-md animate-in fade-in duration-200"
    >
      <div className="relative w-full max-w-lg rounded-2xl bg-[#090D1A]/95 border border-amber-500/50 p-6 sm:p-7 text-center shadow-[0_10px_50px_rgba(0,0,0,0.9)] overflow-hidden">
        {/* Ornate Top Border Flare */}
        <div className="absolute top-0 inset-x-0 h-1 bg-gradient-to-r from-transparent via-amber-400 to-transparent shadow-[0_0_12px_#F59E0B]" />
        
        {/* Header Badge */}
        <div className="flex items-center justify-center gap-1.5 text-xs font-tech tracking-[0.2em] text-cyan-300 uppercase mb-1">
          <img
            src={HEADER_ICON_ASSETS.pauseTalisman}
            alt="Talisman"
            className="w-4 h-4 object-contain filter drop-shadow-[0_0_4px_#06B6D4]"
          />
          <span>{mode === 'paused' ? 'Định Thân Phù · Trận Pháp Tạm Ngưng' : 'Thiên Ma Bại Trận · Cửu Trọng Khai Mở'}</span>
        </div>

        <h2 className="font-display text-2xl sm:text-3xl font-extrabold text-amber-300 mb-2 drop-shadow-[0_2px_10px_rgba(245,158,11,0.3)]">
          {mode === 'paused' ? 'LÒ RÈN TẠM DỪNG' : 'ĐẠI THẮNG PHÁ TRỜI'}
        </h2>

        {/* Current Active Character Capsule (If paused) */}
        {mode === 'paused' && (playerClass || activeCharacterName) && (
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-slate-900/90 border border-amber-500/30 text-xs font-tech text-slate-300 mb-3 shadow-inner">
            <span className="text-amber-400">Tu Sĩ Hiện Tại:</span>
            {playerClass && <span className="text-base">{playerClass.icon}</span>}
            <span className="font-bold text-amber-200">
              {activeCharacterName || 'Đệ Tử'}
            </span>
            {playerClass && (
              <span className="text-[11px] text-cyan-300 bg-cyan-950/70 border border-cyan-500/30 px-1.5 py-0.2 rounded">
                {playerClass.name}
              </span>
            )}
          </div>
        )}

        {/* 3 Tabular Combat Stat Tiles */}
        <div className="grid grid-cols-3 gap-2.5 my-4 font-tech">
          <div className="p-3 rounded-xl bg-[#060810]/90 border border-slate-800/90 shadow-md">
            <div className="text-[11px] text-slate-400">Tổng Công Phá</div>
            <div className="text-sm sm:text-base font-bold text-amber-300 tabular-nums">
              {currentDamage.toLocaleString('en-US')}
            </div>
          </div>
          <div className="p-3 rounded-xl bg-[#060810]/90 border border-slate-800/90 shadow-md">
            <div className="text-[11px] text-slate-400">Đỉnh Combo</div>
            <div className="text-sm sm:text-base font-bold text-cyan-300 tabular-nums">{maxCombo}</div>
          </div>
          <div className="p-3 rounded-xl bg-[#060810]/90 border border-slate-800/90 shadow-md">
            <div className="text-[11px] text-slate-400">Nhịp Hoàng Kim</div>
            <div className="text-sm sm:text-base font-bold text-red-400 tabular-nums">{perfectCount}</div>
          </div>
        </div>

        {/* Action Controls Section */}
        <div className="flex flex-col gap-2.5 mt-5">
          {mode === 'paused' ? (
            <>
              {/* 1. Primary Action: Tiếp Tục Rèn Đúc */}
              <button
                type="button"
                onClick={onResume}
                className="w-full flex items-center justify-center gap-2 px-6 py-3 rounded-xl bg-gradient-to-r from-amber-500 via-amber-400 to-amber-500 hover:from-amber-400 hover:to-amber-300 text-slate-950 font-tech font-extrabold text-sm tracking-wider shadow-[0_0_20px_rgba(245,158,11,0.4)] cursor-pointer transition-all hover:scale-[1.01] active:scale-[0.98]"
              >
                <img
                  src={HEADER_ICON_ASSETS.forgeHammer}
                  alt="Resume"
                  className="w-4 h-4 object-contain filter drop-shadow"
                />
                <span>TIẾP TỤC RÈN ĐÚC</span>
                <span className="text-[10px] bg-slate-950/30 text-slate-950 px-1.5 py-0.5 rounded font-mono font-bold ml-1">
                  ESC / SPACE
                </span>
              </button>

              {/* 2. Secondary Row: Đổi Tu Sĩ & Bật/Tắt Âm Thanh */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                {/* Đổi Nhân Vật (Đổi Tu Sĩ) */}
                {onSwitchCharacter && (
                  <button
                    type="button"
                    onClick={onSwitchCharacter}
                    className="flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-[#0F1424] hover:bg-[#161F38] text-amber-200 border border-amber-500/40 hover:border-amber-400 font-tech font-bold text-xs shadow-md cursor-pointer transition-all active:scale-[0.98] group"
                    title="Mở bảng Tam Đại Đạo Cơ để chọn hoặc tạo đệ tử khác"
                  >
                    <span className="text-sm group-hover:scale-110 transition-transform">
                      {playerClass?.icon || '🥋'}
                    </span>
                    <span>ĐỔI TU SĨ (3 SLOTS)</span>
                  </button>
                )}

                {/* Bật / Tắt Âm Thanh */}
                {onToggleMute && (
                  <button
                    type="button"
                    onClick={onToggleMute}
                    className={`flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl border font-tech font-bold text-xs shadow-md cursor-pointer transition-all active:scale-[0.98] ${
                      muted
                        ? 'bg-rose-950/40 border-rose-500/50 text-rose-300 hover:bg-rose-900/50'
                        : 'bg-emerald-950/40 border-emerald-500/50 text-emerald-300 hover:bg-emerald-900/50'
                    }`}
                    title="Bật/Tắt hiệu ứng âm thanh và nhạc nền [Phím M]"
                  >
                    <img
                      src={muted ? HEADER_ICON_ASSETS.soundOff : HEADER_ICON_ASSETS.soundOn}
                      alt={muted ? 'Muted' : 'Sound On'}
                      className="w-4 h-4 object-contain filter drop-shadow"
                    />
                    <span>{muted ? 'ÂM THANH: ĐÃ TẮT' : 'ÂM THANH: ĐANG BẬT'}</span>
                    <span className="text-[10px] opacity-75 font-mono font-normal">
                      [M]
                    </span>
                  </button>
                )}
              </div>

              {/* 2B. Tủ Đồ Tiên Gia: 5 Bộ Y Phục Môn Phái */}
              {onEquipSkin && (
                <div className="p-3 rounded-2xl bg-slate-900/70 border border-slate-800 flex flex-col gap-2">
                  <div className="flex items-center justify-between text-xs font-tech">
                    <span className="text-amber-300 font-bold uppercase tracking-wider flex items-center gap-1.5">
                      <Sparkles className="w-3.5 h-3.5 text-amber-400" />
                      <span>TỦ ĐỒ TIÊN GIA (CHỌN TRANG PHỤC):</span>
                    </span>
                    <span className="text-[11px] text-slate-400">
                      Đang mặc: <b className="text-amber-300">{CHARACTER_SKINS[equippedSkinId || 'skin_default']?.name}</b>
                    </span>
                  </div>

                  <div className="grid grid-cols-5 gap-1.5">
                    {Object.values(CHARACTER_SKINS).map((sk) => {
                      const isEquipped = (equippedSkinId || 'skin_default') === sk.id;
                      return (
                        <button
                          key={sk.id}
                          type="button"
                          onClick={() => onEquipSkin(sk.id)}
                          className={`relative rounded-xl border p-1 text-center cursor-pointer transition-all flex flex-col items-center gap-1 group ${
                            isEquipped
                              ? 'bg-slate-800/95 border-amber-400 ring-2 ring-amber-400/50 shadow-lg scale-105 z-10'
                              : 'bg-slate-950/70 border-slate-800 hover:border-slate-700 hover:bg-slate-900/60'
                          }`}
                          title={`${sk.name} · ${sk.sectTitle}\n${sk.description}`}
                        >
                          {isEquipped && (
                            <div className="absolute -top-1.5 -right-1 px-1 py-0.2 rounded-full bg-emerald-500 text-slate-950 text-[7px] font-bold z-20 shadow">
                              ĐANG MẶC
                            </div>
                          )}
                          <div className="w-full aspect-[3/4] rounded-lg overflow-hidden bg-slate-900/90 relative border border-slate-700/50">
                            <img
                              src={`$${import.meta.env.BASE_URL || './'}${sk.cardPath}`}
                              alt={sk.name}
                              className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
                            />
                            <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent pointer-events-none" />
                            <span className="absolute bottom-0.5 right-1 text-[11px]">{sk.icon}</span>
                          </div>
                          <span className={`text-[9px] font-tech font-bold leading-tight truncate w-full ${
                            isEquipped ? 'text-amber-300' : 'text-slate-300'
                          }`}>
                            {sk.name.replace('Phàm Nhân ', '').replace('Cửu Tiêu ', '').replace('Hắc Diệm ', '').replace('Bất Chu ', '').replace('Thanh Mộc ', '')}
                          </span>
                        </button>
                      );
                    })}
                  </div>
                </div>
              )}

              {/* 3. Restart and Title Actions */}
              <div className="grid grid-cols-2 gap-2.5 pt-1 border-t border-slate-800/80">
                <button
                  type="button"
                  onClick={onRestart}
                  className="px-4 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-300 hover:text-white border border-slate-800 hover:border-slate-700 font-tech font-semibold text-xs cursor-pointer transition-colors"
                >
                  RÈN LẠI TỪ ĐẦU
                </button>
                <button
                  type="button"
                  onClick={onReturnTitle}
                  className="px-4 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-400 hover:text-rose-300 border border-slate-800 hover:border-rose-900/40 font-tech font-semibold text-xs cursor-pointer transition-colors"
                >
                  VỀ TRANG CHỦ
                </button>
              </div>

              {/* 4. Version Badge & Force Clear Cache / Reload Helper */}
              <div className="pt-1 flex items-center justify-between text-[10px] font-tech text-slate-400 px-1">
                <span>Bản game: <b className="text-amber-400">v4.2 (Vạn Cổ Đúc Thần Đài)</b></span>
                <button
                  type="button"
                  onClick={() => {
                    localStorage.removeItem('pha_troi_cache_buster');
                    window.location.reload();
                  }}
                  className="text-cyan-400 hover:text-cyan-300 underline cursor-pointer flex items-center gap-1 font-bold"
                  title="Xóa cache trình duyệt và tải ngay phiên bản mới nhất"
                >
                  <span>Làm mới & Xóa Cache ⟳</span>
                </button>
              </div>
            </>
          ) : (
            <>
              <button
                type="button"
                onClick={onRestart}
                className="w-full px-5 py-3 rounded-xl bg-amber-400 hover:bg-amber-300 text-slate-950 font-tech font-bold text-sm shadow-md cursor-pointer transition-colors"
              >
                TIẾN VÀO TẦNG TIẾP THEO
              </button>
              <button
                type="button"
                onClick={onReturnTitle}
                className="w-full px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 font-tech font-semibold text-sm cursor-pointer transition-colors"
              >
                VỀ TRANG CHỦ
              </button>
            </>
          )}
        </div>

        {/* Footer Hotkey Guidance Note */}
        <div className="mt-4 pt-3 border-t border-slate-800/60 text-[10px] font-tech text-slate-500 flex items-center justify-center gap-2">
          <span><kbd className="px-1 py-0.5 rounded bg-slate-800 border border-slate-700 text-amber-300">ESC</kbd> Đóng / Mở</span>
          <span>•</span>
          <span><kbd className="px-1 py-0.5 rounded bg-slate-800 border border-slate-700 text-cyan-300">M</kbd> Bật/Tắt Âm</span>
          <span>•</span>
          <span><kbd className="px-1 py-0.5 rounded bg-slate-800 border border-slate-700 text-slate-300">SPACE</kbd> Nện Búa</span>
        </div>
      </div>
    </div>
  );
};
