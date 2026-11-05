import React, { useState, useEffect } from 'react';
import { CharacterProfile, MAX_CHARACTER_SLOTS } from '../game/characterSlots';
import { PLAYER_CLASSES, PlayerClassId, CHARACTER_SKINS, getSkinOrDefault } from '../game/rules';
import { soundEngine } from '../game/audio';
import {
  Zap,
  Flame,
  Mountain,
  Music,
  Plus,
  Play,
  Trash2,
  ArrowLeft,
  Shield,
  Sparkles,
  AlertTriangle,
} from 'lucide-react';

interface CharacterSelectionModalProps {
  slots: (CharacterProfile | null)[];
  activeSlotId: 1 | 2 | 3;
  onSelectSlot: (slotId: 1 | 2 | 3) => void;
  onCreateNewInSlot: (slotId: 1 | 2 | 3) => void;
  onDeleteSlot: (slotId: 1 | 2 | 3) => void;
  onBackToTitle: () => void;
}

export const CharacterSelectionModal: React.FC<CharacterSelectionModalProps> = ({
  slots,
  activeSlotId,
  onSelectSlot,
  onCreateNewInSlot,
  onDeleteSlot,
  onBackToTitle,
}) => {
  const [selectedSlotIndex, setSelectedSlotIndex] = useState<number>(activeSlotId - 1);
  const [deleteConfirmSlot, setDeleteConfirmSlot] = useState<number | null>(null);

  const getClassMeta = (classId: PlayerClassId) => {
    return PLAYER_CLASSES[classId] || PLAYER_CLASSES.thunder;
  };

  const getClassIcon = (classId: PlayerClassId) => {
    switch (classId) {
      case 'thunder':
        return <Zap className="w-5 h-5 text-cyan-400" />;
      case 'fire':
        return <Flame className="w-5 h-5 text-orange-400" />;
      case 'gravity':
        return <Mountain className="w-5 h-5 text-purple-400" />;
      case 'mystic':
        return <Music className="w-5 h-5 text-emerald-400" />;
    }
  };

  const handleSelectSlot = (idx: number) => {
    setSelectedSlotIndex(idx);
    const profile = slots[idx];
    if (profile) {
      const cls = getClassMeta(profile.classId);
      soundEngine.playStanceSwitch(cls.stanceKey);
    } else {
      soundEngine.playAnvilStrike('GREAT', 'Q', false);
    }
  };

  const handleEnterGame = (slotId: 1 | 2 | 3) => {
    soundEngine.unlockAudio();
    soundEngine.playAnvilStrike('PERFECT', 'Q', false);
    onSelectSlot(slotId);
  };

  const formatDamage = (dmg: number) => {
    if (dmg >= 1_000_000_000) return `${(dmg / 1_000_000_000).toFixed(2)}B`;
    if (dmg >= 1_000_000) return `${(dmg / 1_000_000).toFixed(1)}M`;
    if (dmg >= 1_000) return `${(dmg / 1_000).toFixed(0)}k`;
    return `${dmg}`;
  };

  const formatTimeAgo = (ts: number) => {
    const diffMs = Date.now() - ts;
    const mins = Math.floor(diffMs / 60000);
    if (mins < 1) return 'Vừa mới đây';
    if (mins < 60) return `${mins} phút trước`;
    const hours = Math.floor(mins / 60);
    if (hours < 24) return `${hours} giờ trước`;
    const days = Math.floor(hours / 24);
    return `${days} ngày trước`;
  };

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      const isInput =
        e.target instanceof HTMLInputElement ||
        e.target instanceof HTMLTextAreaElement ||
        (e.target instanceof HTMLElement && e.target.isContentEditable);
      if (isInput) return;

      const isSpace =
        e.code === 'Space' ||
        e.key === ' ' ||
        e.key === 'Spacebar' ||
        e.keyCode === 32 ||
        e.which === 32;
      const isEnter = e.code === 'Enter' || e.key === 'Enter';

      if (isSpace || isEnter) {
        e.preventDefault();
        e.stopPropagation();
        const slotNumber = (selectedSlotIndex + 1) as 1 | 2 | 3;
        const profile = slots[selectedSlotIndex];
        if (profile) {
          handleEnterGame(slotNumber);
        } else {
          onCreateNewInSlot(slotNumber);
        }
      }
    };

    window.addEventListener('keydown', handleKeyDown, true);
    return () => window.removeEventListener('keydown', handleKeyDown, true);
  }, [selectedSlotIndex, slots, onCreateNewInSlot]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-6 bg-slate-950/92 backdrop-blur-2xl select-none overflow-y-auto">
      {/* Background ambient accents */}
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-cyan-500/10 rounded-full filter blur-3xl pointer-events-none" />
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-amber-500/10 rounded-full filter blur-3xl pointer-events-none" />

      <div className="relative w-full max-w-5xl bg-[#060914] border border-amber-500/35 rounded-3xl shadow-2xl p-5 sm:p-8 flex flex-col gap-6 text-slate-100 max-h-[95vh] overflow-y-auto">
        {/* Header */}
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between border-b border-slate-800/80 pb-4 gap-3">
          <div className="flex items-center gap-3">
            <button
              type="button"
              onClick={onBackToTitle}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-900/80 hover:bg-slate-800 border border-slate-700 text-xs font-tech text-slate-300 hover:text-amber-300 transition-colors cursor-pointer"
            >
              <ArrowLeft className="w-3.5 h-3.5" />
              <span>Màn Hình Chính</span>
            </button>
            <div className="h-4 w-[1px] bg-slate-800" />
            <div>
              <div className="flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-amber-400 animate-pulse" />
                <h1 className="text-base sm:text-lg font-bold font-display tracking-wider text-amber-200">
                  HỒ SƠ TU SĨ · TAM ĐẠI ĐẠO CƠ
                </h1>
              </div>
              <p className="text-xs text-slate-400 font-tech">
                Chọn đệ tử nhập trận hoặc khởi tạo đạo cơ mới (Tối đa 3 nhân vật riêng biệt).
              </p>
            </div>
          </div>

          <div className="text-xs font-tech text-slate-400 flex items-center gap-2">
            <span className="text-amber-400/80">Quy tắc Độc Nhất:</span>
            <span>Mỗi slot lưu giữ trọn vẹn môn phái & bảo vật độc lập</span>
          </div>
        </div>

        {/* 3 Character Slots Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {slots.map((profile, idx) => {
            const slotNumber = (idx + 1) as 1 | 2 | 3;
            const isSelected = selectedSlotIndex === idx;

            if (profile) {
              const cls = getClassMeta(profile.classId);
              return (
                <div
                  key={idx}
                  onClick={() => handleSelectSlot(idx)}
                  className={`group relative rounded-2xl border transition-all duration-200 flex flex-col justify-between p-5 cursor-pointer overflow-hidden ${
                    isSelected
                      ? 'bg-gradient-to-b from-[#0D162B] to-[#070B16] border-amber-400/90 ring-2 ring-amber-400/30 shadow-xl shadow-amber-500/10'
                      : 'bg-slate-950/60 border-slate-800/90 hover:border-slate-700 hover:bg-slate-900/50'
                  }`}
                >
                  {/* Subtle Top Gradient Line */}
                  <div
                    className="absolute top-0 left-0 right-0 h-1 transition-opacity"
                    style={{ backgroundColor: cls.color }}
                  />

                  {/* Slot Top Meta */}
                  <div>
                    <div className="flex items-center justify-between mb-3">
                      <span className="text-[11px] font-tech font-bold px-2 py-0.5 rounded bg-slate-900 border border-slate-800 text-slate-300">
                        SLOT #{slotNumber}
                      </span>
                      <div className="flex items-center gap-1.5">
                        <span className={`text-[11px] font-tech font-semibold px-2 py-0.5 rounded border ${cls.badgeBg}`}>
                          {cls.name}
                        </span>
                        <div className="w-6 h-6 rounded-md bg-slate-900/80 border border-slate-800 flex items-center justify-center">
                          {getClassIcon(profile.classId)}
                        </div>
                      </div>
                    </div>

                    {/* Character Name & Outfit Avatar Thumbnail */}
                    <div className="flex items-center gap-3 mb-2.5">
                      {(() => {
                        const skin = getSkinOrDefault(profile.equippedSkinId, profile.classId);
                        return (
                          <>
                            <div className="w-12 h-16 rounded-xl overflow-hidden bg-slate-900 border border-slate-700/80 shrink-0 relative shadow">
                              <img
                                src={`$${import.meta.env.BASE_URL || './'}${skin.cardPath}`}
                                alt={skin.name}
                                className="w-full h-full object-cover"
                              />
                              <span className="absolute bottom-0.5 right-1 text-[10px]">{skin.icon}</span>
                            </div>
                            <div className="min-w-0 flex-1">
                              <h2
                                className="text-base sm:text-lg font-bold text-amber-200 drop-shadow truncate"
                                style={{ fontFamily: "'Lora', Georgia, serif" }}
                              >
                                {profile.characterName}
                              </h2>
                              <div className="text-[11px] text-amber-400 font-tech font-semibold truncate">
                                {skin.name}
                              </div>
                              <div className="text-[10px] text-slate-400 font-tech truncate">
                                {cls.sectTitle.split('·')[0].trim()}
                              </div>
                            </div>
                          </>
                        );
                      })()}
                    </div>

                    {/* Progress Metrics */}
                    <div className="space-y-1.5 py-3 border-y border-slate-800/80 text-xs font-tech">
                      <div className="flex justify-between items-center text-slate-300">
                        <span className="text-slate-400">Cấp Độ:</span>
                        <span className="font-bold text-amber-300">Lv. {profile.level}</span>
                      </div>
                      <div className="flex justify-between items-center text-slate-300">
                        <span className="text-slate-400">Vòm Trời:</span>
                        <span className="text-slate-200">Tầng {profile.progress.currentVaultId || 1}</span>
                      </div>
                      <div className="flex justify-between items-center text-slate-300">
                        <span className="text-slate-400">Tổng Sát Thương:</span>
                        <span className="font-mono text-cyan-300">{formatDamage(profile.progress.playerTotalDamage || 0)}</span>
                      </div>
                      <div className="flex justify-between items-center text-slate-300">
                        <span className="text-slate-400">Linh Thạch:</span>
                        <span className="font-mono text-amber-400">{(profile.progress.linhThach || 0).toLocaleString()} 💎</span>
                      </div>
                    </div>

                    <div className="text-[10px] text-slate-500 font-tech mt-2">
                      Lần cuối: {formatTimeAgo(profile.lastPlayedAt)}
                    </div>
                  </div>

                  {/* Actions Bar */}
                  <div className="mt-4 pt-3 border-t border-slate-800/60 flex items-center gap-2">
                    <button
                      type="button"
                      onClick={(e) => {
                        e.stopPropagation();
                        handleEnterGame(slotNumber);
                      }}
                      className="flex-1 flex items-center justify-center gap-2 py-2.5 px-4 rounded-xl bg-gradient-to-r from-amber-500 to-yellow-500 hover:from-amber-400 hover:to-yellow-400 text-slate-950 text-xs font-tech font-bold uppercase tracking-wider shadow-md hover:shadow-amber-500/20 transition-all cursor-pointer active:scale-95"
                    >
                      <Play className="w-3.5 h-3.5 fill-current" />
                      <span>XUẤT TRẬN</span>
                    </button>

                    <button
                      type="button"
                      onClick={(e) => {
                        e.stopPropagation();
                        setDeleteConfirmSlot(slotNumber);
                      }}
                      className="p-2.5 rounded-xl bg-slate-900 hover:bg-red-950/50 text-slate-400 hover:text-red-400 border border-slate-800 hover:border-red-800/60 text-xs cursor-pointer transition-colors"
                      title="Giải thể đạo cơ (Xóa nhân vật)"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              );
            }

            // Empty Slot
            return (
              <div
                key={idx}
                onClick={() => handleSelectSlot(idx)}
                className={`group relative rounded-2xl border-2 border-dashed transition-all duration-200 flex flex-col items-center justify-center p-8 min-h-[310px] text-center cursor-pointer ${
                  isSelected
                    ? 'bg-slate-900/40 border-amber-400/80 ring-2 ring-amber-400/20'
                    : 'bg-slate-950/40 border-slate-800/80 hover:border-slate-700 hover:bg-slate-900/30'
                }`}
              >
                <div className="text-[11px] font-tech font-bold px-2 py-0.5 rounded bg-slate-900 border border-slate-800 text-slate-400 mb-4">
                  SLOT #{slotNumber} · TRỐNG
                </div>

                <div className="w-14 h-14 rounded-2xl bg-slate-900/80 border border-slate-800 flex items-center justify-center text-slate-500 group-hover:text-amber-400 group-hover:border-amber-400/60 transition-colors mb-3">
                  <Plus className="w-7 h-7" />
                </div>

                <h3 className="text-sm font-bold font-tech text-slate-300 group-hover:text-amber-300 transition-colors mb-1">
                  ĐẠO CƠ TRỐNG
                </h3>
                <p className="text-xs text-slate-500 font-tech max-w-[200px] mb-5">
                  Chưa bái sư nhập phái. Tạo đệ tử mới để trải nghiệm môn phái khác.
                </p>

                <button
                  type="button"
                  onClick={(e) => {
                    e.stopPropagation();
                    onCreateNewInSlot(slotNumber);
                  }}
                  className="flex items-center gap-2 py-2 px-4 rounded-xl bg-slate-800 hover:bg-amber-500 text-slate-200 hover:text-slate-950 text-xs font-tech font-bold tracking-wider transition-all cursor-pointer"
                >
                  <Sparkles className="w-3.5 h-3.5" />
                  <span>KHỞI TẠO TU SĨ MỚI</span>
                </button>
              </div>
            );
          })}
        </div>

        {/* Footer info banner */}
        <div className="p-3 rounded-xl bg-slate-900/50 border border-slate-800/60 flex flex-col sm:flex-row items-center justify-between text-xs font-tech text-slate-400 gap-2">
          <div className="flex items-center gap-2">
            <Shield className="w-4 h-4 text-emerald-400 shrink-0" />
            <span>Tự động đồng bộ và bảo lưu vĩnh viễn trên trình duyệt này.</span>
          </div>
          <div className="text-slate-500 text-[11px]">
            Bấm [XUẤT TRẬN] để bắt đầu hành trình phá vỡ Mái Vòm Thiên Cấm.
          </div>
        </div>
      </div>

      {/* Delete Confirmation Modal */}
      {deleteConfirmSlot !== null && (
        <div className="fixed inset-0 z-60 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm">
          <div className="w-full max-w-md bg-slate-950 border border-red-500/50 rounded-2xl p-6 text-slate-100 shadow-2xl flex flex-col gap-4">
            <div className="flex items-center gap-3 text-red-400">
              <AlertTriangle className="w-6 h-6" />
              <h3 className="text-base font-bold font-tech">XÁC NHẬN GIẢI THỂ ĐẠO CƠ</h3>
            </div>

            <p className="text-xs text-slate-300 leading-relaxed font-tech">
              Bạn có chắc chắn muốn giải thể vĩnh viễn đệ tử tại <strong className="text-amber-300">SLOT #{deleteConfirmSlot}</strong>? Toàn bộ cấp độ, trang bị và linh thạch của slot này sẽ bị tiêu biến và không thể khôi phục.
            </p>

            <div className="flex items-center justify-end gap-3 pt-2">
              <button
                type="button"
                onClick={() => setDeleteConfirmSlot(null)}
                className="px-4 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-tech cursor-pointer"
              >
                Hủy Bỏ
              </button>
              <button
                type="button"
                onClick={() => {
                  onDeleteSlot(deleteConfirmSlot as 1 | 2 | 3);
                  setDeleteConfirmSlot(null);
                }}
                className="px-4 py-2 rounded-lg bg-red-600 hover:bg-red-500 text-white font-bold text-xs font-tech cursor-pointer"
              >
                Đồng Ý Xóa
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
