import React, { useState } from 'react';
import {
  PlayerClassId,
  PLAYER_CLASSES,
  PlayerClassMeta,
} from '../game/rules';
import { soundEngine } from '../game/audio';
import { Sparkles, Dices, Shield, Zap, Flame, Mountain, Music, ArrowRight, Check } from 'lucide-react';

interface CharacterCreationModalProps {
  currentClassId?: PlayerClassId | null;
  currentName?: string;
  isInitialCreation?: boolean;
  onConfirm: (classId: PlayerClassId, characterName: string) => void;
  onCancel?: () => void;
}

const RANDOM_NAMES = [
  'Tiêu Dao Thần Chùy',
  'Vạn Cổ Thiết Hồn',
  'Lôi Đình Tinh Anh',
  'Phần Thiên Hỏa Tượng',
  'Thái Sơn Hộ Pháp',
  'Bích Ngọc Nhạc Sư',
  'Cửu U Kiếm Tượng',
  'Xích Hỏa Ma Tôn',
  'Thiên Lôi Thần Tướng',
  'Đoạn Hồn Tiên Đồng',
  'Huyền Âm Bất Diệt',
  'Cương Mãnh Đại Sư',
];

export const CharacterCreationModal: React.FC<CharacterCreationModalProps> = ({
  currentClassId = null,
  currentName = '',
  isInitialCreation = false,
  onConfirm,
  onCancel,
}) => {
  const [selectedClassId, setSelectedClassId] = useState<PlayerClassId>(currentClassId || 'thunder');
  const [characterName, setCharacterName] = useState<string>(() => {
    if (currentName && currentName.trim().length > 0) return currentName;
    return `Thợ Rèn #${Math.floor(Math.random() * 8999 + 1000)}`;
  });
  const [isSubmitting, setIsSubmitting] = useState(false);

  const selectedClass = PLAYER_CLASSES[selectedClassId];

  const handleRandomizeName = () => {
    const random = RANDOM_NAMES[Math.floor(Math.random() * RANDOM_NAMES.length)];
    setCharacterName(random);
    soundEngine.playAnvilStrike('GREAT', 'Q', false);
  };

  const handleSelectClass = (cId: PlayerClassId) => {
    setSelectedClassId(cId);
    const cls = PLAYER_CLASSES[cId];
    soundEngine.playStanceSwitch(cls.stanceKey);
  };

  const handleCommit = () => {
    if (isSubmitting) return;
    setIsSubmitting(true);
    soundEngine.unlockAudio();
    soundEngine.playGlobalBurstFanfare();
    setTimeout(() => {
      onConfirm(selectedClassId, characterName.trim() || 'Thợ Rèn Vô Danh');
    }, 400);
  };

  const getClassIcon = (cId: PlayerClassId) => {
    switch (cId) {
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

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-6 bg-slate-950/90 backdrop-blur-xl select-none overflow-y-auto">
      <div className="relative w-full max-w-4xl bg-[#070A14] border border-amber-500/40 rounded-2xl shadow-2xl p-4 sm:p-7 flex flex-col gap-4 text-slate-100 max-h-[92vh] overflow-y-auto">
        {/* Glow ambient background accents */}
        <div
          className="absolute -top-24 -left-24 w-72 h-72 rounded-full opacity-20 filter blur-3xl pointer-events-none"
          style={{ backgroundColor: selectedClass.color }}
        />
        <div
          className="absolute -bottom-24 -right-24 w-72 h-72 rounded-full opacity-15 filter blur-3xl pointer-events-none"
          style={{ backgroundColor: selectedClass.color }}
        />

        {/* Modal Header */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between border-b border-slate-800 pb-3 gap-2">
          <div>
            <div className="flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-amber-400 animate-pulse" />
              <h2 className="text-lg sm:text-xl font-bold font-display tracking-wider text-amber-300">
                KHỞI NGUYÊN CĂN CƠ · BÁI SƯ NHẬP PHÁI
              </h2>
            </div>
            <p className="text-xs text-slate-400 font-tech mt-0.5">
              Quy tắc Độc Nhất Căn Cơ: Mỗi thợ rèn chỉ chọn 1 Hệ Phái duy nhất xuyên suốt hành trình Phá Mái Vòm Trời.
            </p>
          </div>

          {!isInitialCreation && onCancel && (
            <button
              type="button"
              onClick={onCancel}
              className="text-xs text-slate-400 hover:text-slate-100 px-3 py-1 rounded bg-slate-900 border border-slate-800 cursor-pointer self-start sm:self-auto"
            >
              ✕ Đóng
            </button>
          )}
        </div>

        {/* Character Name Input Row */}
        <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800 flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-2.5">
          <div className="text-xs font-tech font-semibold text-slate-300 whitespace-nowrap">
            ĐẠO HIỆU THỢ RÈN:
          </div>
          <div className="flex items-center gap-2 flex-1 max-w-md">
            <input
              type="text"
              maxLength={24}
              value={characterName}
              onChange={(e) => setCharacterName(e.target.value)}
              placeholder="Nhập tên nhân vật..."
              className="flex-1 bg-slate-950 border border-slate-700 focus:border-amber-400 px-3 py-1.5 rounded-lg text-sm font-tech text-amber-200 outline-none transition-colors"
            />
            <button
              type="button"
              onClick={handleRandomizeName}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-amber-300 border border-slate-700 text-xs font-tech cursor-pointer transition-colors"
              title="Ngẫu nhiên tên thợ rèn hào hiệp"
            >
              <Dices className="w-3.5 h-3.5" />
              <span>Ngẫu Nhiên</span>
            </button>
          </div>
        </div>

        {/* 4 Class Cards Grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-2.5">
          {(Object.keys(PLAYER_CLASSES) as PlayerClassId[]).map((cId) => {
            const cls = PLAYER_CLASSES[cId];
            const isSelected = selectedClassId === cId;
            return (
              <button
                key={cId}
                type="button"
                onClick={() => handleSelectClass(cId)}
                className={`p-3 rounded-xl border text-left transition-all cursor-pointer flex flex-col justify-between min-h-[110px] relative overflow-hidden ${
                  isSelected
                    ? 'bg-slate-900/90 border-amber-400 ring-2 ring-amber-400/40 shadow-lg scale-[1.02]'
                    : 'bg-slate-950/60 border-slate-800/90 hover:border-slate-700 hover:bg-slate-900/50'
                }`}
              >
                {/* Selected check badge */}
                {isSelected && (
                  <div className="absolute top-2 right-2 w-4 h-4 rounded-full bg-amber-400 text-slate-950 flex items-center justify-center text-[10px] font-bold">
                    <Check className="w-3 h-3 stroke-[3]" />
                  </div>
                )}

                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <div className="w-7 h-7 rounded-lg flex items-center justify-center bg-slate-950/80 border border-slate-800">
                      {getClassIcon(cId)}
                    </div>
                    <div>
                      <h3 className={`text-xs sm:text-sm font-bold font-tech ${cls.textColor}`}>
                        {cls.name}
                      </h3>
                      <div className="text-[10px] text-slate-400 font-tech truncate">
                        Phím [{cls.stanceKey}]
                      </div>
                    </div>
                  </div>
                  <div className="text-[10px] text-slate-300 font-tech font-semibold">
                    {cls.sectTitle.split('·')[0].trim()}
                  </div>
                </div>

                <div className="text-[9px] text-slate-400 font-tech mt-2 pt-1 border-t border-slate-800/70 truncate">
                  {cls.primaryStats.join(' · ')}
                </div>
              </button>
            );
          })}
        </div>

        {/* Selected Class Deep-Dive Showcase */}
        <div className="p-4 rounded-2xl bg-gradient-to-b from-[#0B0F1E] to-[#070912] border border-slate-800 flex flex-col gap-3">
          {/* Header of Class */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800 pb-2.5">
            <div>
              <div className="flex items-center gap-2">
                <span className={`text-xs px-2 py-0.5 rounded border font-tech font-bold ${selectedClass.badgeBg}`}>
                  {selectedClass.sectTitle}
                </span>
                <span className="text-xs text-slate-400 font-tech">Vũ khí: {selectedClass.weaponName}</span>
              </div>
              <p className="text-xs text-amber-200/90 italic font-tech mt-1">
                "{selectedClass.motto}"
              </p>
            </div>

            <div className="text-left sm:text-right font-tech text-xs">
              <span className="text-slate-400">Vai trò Raid: </span>
              <span className="text-cyan-300 font-bold">{selectedClass.roleSummary}</span>
            </div>
          </div>

          {/* 4 Skills [Q] [W] [E] [R] Evolution Grid */}
          <div>
            <div className="text-[11px] font-tech font-bold text-amber-300 uppercase tracking-wider mb-2 flex items-center gap-1.5">
              <Sparkles className="w-3.5 h-3.5 text-amber-400" />
              <span>BỘ 4 KỸ NĂNG TIẾN HÓA CỦA {selectedClass.name.toUpperCase()} (Q - W - E - R):</span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs font-tech">
              {(['Q', 'W', 'E', 'R'] as const).map((slotKey) => {
                const sk = selectedClass.skills[slotKey];
                return (
                  <div
                    key={slotKey}
                    className="p-2.5 rounded-xl bg-slate-950/70 border border-slate-800/80 flex items-start gap-2.5"
                  >
                    <div className="w-8 h-8 rounded-lg bg-slate-900 border border-slate-700 flex flex-col items-center justify-center shrink-0">
                      <span className="text-xs font-bold text-amber-300">[{slotKey}]</span>
                      <span className="text-[8px] text-slate-400">{sk.unlockLevel === 1 ? 'Lv.1' : `Lv.${sk.unlockLevel}`}</span>
                    </div>

                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between gap-1 mb-0.5">
                        <span className="font-bold text-slate-200 truncate">
                          {sk.name}
                        </span>
                        <span className="text-[10px] text-cyan-300 shrink-0">
                          {sk.cooldownSec > 0 ? `CD ${sk.cooldownSec}s` : sk.overdriveCost > 0 ? `Tốn ${sk.overdriveCost} OD` : 'Nội tại'}
                        </span>
                      </div>
                      <div className="text-[10px] text-amber-400/90 font-medium mb-1">
                        {sk.typeTitle}
                      </div>
                      <p className="text-[11px] text-slate-400 leading-relaxed">
                        {sk.description}
                      </p>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Sub-Classes Future Specialization */}
          <div className="pt-2 border-t border-slate-800 flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-2 text-xs font-tech">
            <div className="text-slate-400">
              <span className="text-slate-300 font-bold">2 Nhánh Chuyển Chức (Lv.120): </span>
              <span className="text-purple-300">① {selectedClass.subClasses.a.name} ({selectedClass.subClasses.a.focus})</span>
              <span> · </span>
              <span className="text-emerald-300">② {selectedClass.subClasses.b.name} ({selectedClass.subClasses.b.focus})</span>
            </div>
          </div>
        </div>

        {/* CTA Confirmation Button */}
        <div className="pt-2 flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3">
          <div className="text-xs text-slate-400 font-tech">
            Sau khi bái sư, 4 phím Q W E R sẽ trở thành bộ chiêu thức tiến hóa của {selectedClass.name}.
          </div>

          <button
            type="button"
            disabled={isSubmitting}
            onClick={handleCommit}
            className="group flex items-center justify-center gap-3 px-8 py-3.5 rounded-full bg-gradient-to-r from-amber-500 via-amber-400 to-yellow-500 hover:from-amber-400 hover:to-yellow-400 text-slate-950 font-tech font-bold text-sm tracking-[0.15em] uppercase shadow-lg shadow-amber-500/25 transition-all cursor-pointer active:scale-95"
          >
            <span>BÁI SƯ NHẬP PHÁI — BƯỚC VÀO THIÊN TRẬN</span>
            <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
          </button>
        </div>
      </div>
    </div>
  );
};
