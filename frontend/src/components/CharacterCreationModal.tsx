import React, { useState, useRef } from 'react';
import {
  PlayerClassId,
  PLAYER_CLASSES,
  PlayerClassMeta,
  CHARACTER_SKINS,
  SECT_DEFAULT_SKIN,
  CharacterSkinMeta,
} from '../game/rules';
import { soundEngine } from '../game/audio';
import { Sparkles, Dices, Zap, Flame, Mountain, Music, ArrowRight, Check } from 'lucide-react';
import { InteractiveAltarPreview, InteractiveAltarPreviewRef } from './InteractiveAltarPreview';

interface CharacterCreationModalProps {
  currentClassId?: PlayerClassId | null;
  currentName?: string;
  currentSkinId?: string | null;
  isInitialCreation?: boolean;
  slotId?: 1 | 2 | 3;
  onConfirm: (classId: PlayerClassId, characterName: string, skinId?: string) => void;
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
  currentSkinId = null,
  isInitialCreation = false,
  slotId,
  onConfirm,
  onCancel,
}) => {
  const [selectedClassId, setSelectedClassId] = useState<PlayerClassId>(currentClassId || 'thunder');
  const [selectedSkinId, setSelectedSkinId] = useState<string>(() => {
    if (currentSkinId && CHARACTER_SKINS[currentSkinId]) return currentSkinId;
    return SECT_DEFAULT_SKIN[currentClassId || 'thunder'] || 'skin_thunder_robe';
  });
  const [characterName, setCharacterName] = useState<string>(() => {
    if (currentName && currentName.trim().length > 0) return currentName;
    return `Thợ Rèn #${Math.floor(Math.random() * 8999 + 1000)}`;
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const altarPreviewRef = useRef<InteractiveAltarPreviewRef>(null);

  const selectedClass = PLAYER_CLASSES[selectedClassId];

  const handleRandomizeName = () => {
    const random = RANDOM_NAMES[Math.floor(Math.random() * RANDOM_NAMES.length)];
    setCharacterName(random);
    soundEngine.playAnvilStrike('GREAT', 'Q', false);
  };

  const handleSelectClass = (cId: PlayerClassId) => {
    setSelectedClassId(cId);
    setSelectedSkinId(SECT_DEFAULT_SKIN[cId] || 'skin_default');
    const cls = PLAYER_CLASSES[cId];
    soundEngine.playStanceSwitch(cls.stanceKey);
  };

  const handleSelectSkin = (sId: string) => {
    setSelectedSkinId(sId);
    soundEngine.playAnvilStrike('GREAT', 'Q', false);
  };

  const handleCommit = () => {
    if (isSubmitting) return;
    setIsSubmitting(true);
    soundEngine.unlockAudio();
    soundEngine.playGlobalBurstFanfare();
    setTimeout(() => {
      onConfirm(selectedClassId, characterName.trim() || 'Thợ Rèn Vô Danh', selectedSkinId);
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
    <div className="fixed inset-0 z-50 flex items-center justify-center p-2 sm:p-4 bg-slate-950/92 backdrop-blur-2xl select-none overflow-y-auto">
      <div className="relative w-full max-w-6xl bg-[#060913] border border-amber-500/40 rounded-3xl shadow-2xl p-3.5 sm:p-5 lg:p-6 flex flex-col gap-3 text-slate-100 max-h-[96vh] overflow-y-auto">
        {/* Glow ambient background accents */}
        <div
          className="absolute -top-32 -left-32 w-96 h-96 rounded-full opacity-25 filter blur-3xl pointer-events-none transition-colors duration-500"
          style={{ backgroundColor: selectedClass.color }}
        />
        <div
          className="absolute -bottom-32 -right-32 w-96 h-96 rounded-full opacity-20 filter blur-3xl pointer-events-none transition-colors duration-500"
          style={{ backgroundColor: selectedClass.color }}
        />

        {/* Modal Header */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between border-b border-slate-800 pb-2.5 gap-2">
          <div>
            <div className="flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-amber-400 animate-pulse" />
              <h2 className="text-base sm:text-lg font-bold font-display tracking-wider text-amber-300">
                {slotId ? `SLOT #${slotId} · KHỞI NGUYÊN CĂN CƠ` : 'KHỞI NGUYÊN CĂN CƠ · BÁI SƯ NHẬP PHÁI'}
              </h2>
            </div>
            <p className="text-[11px] text-slate-400 font-tech mt-0.5">
              Quy tắc Độc Nhất Căn Cơ: Mỗi thợ rèn chọn 1 Hệ Phái duy nhất · Có thể gõ thử cảm nhận phách lực môn phái trước khi nhập môn.
            </p>
          </div>

          {onCancel && (
            <button
              type="button"
              onClick={onCancel}
              className="text-xs text-slate-400 hover:text-slate-100 px-3 py-1.5 rounded-xl bg-slate-900 border border-slate-800 hover:border-slate-700 cursor-pointer self-start sm:self-auto transition-colors"
            >
              ✕ Quay Lại
            </button>
          )}
        </div>

        {/* 2.5D SPLIT SCREEN: LEFT PREVIEW + RIGHT CONFIGURATION */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-4 items-stretch">
          {/* LEFT COLUMN: 2.5D INTERACTIVE ALTAR & PRE-TEST HAMMER */}
          <div className="lg:col-span-5 flex flex-col justify-between gap-2.5">
            <InteractiveAltarPreview
              ref={altarPreviewRef}
              selectedClassId={selectedClassId}
              characterName={characterName}
              skinId={selectedSkinId}
            />

            {/* Sect Outfits & Robe Selector */}
            <div className="p-3 rounded-2xl bg-slate-900/80 border border-slate-800 flex flex-col gap-2">
              <div className="flex items-center justify-between text-xs font-tech">
                <span className="text-amber-300 font-bold uppercase tracking-wider flex items-center gap-1.5">
                  <Sparkles className="w-3.5 h-3.5 text-amber-400" />
                  <span>Y PHỤC MÔN PHÁI (5 BỘ ĐỒ ĐỘC BẢN):</span>
                </span>
                <span className="text-[11px] text-slate-400">
                  Đang chọn: <b className="text-amber-300">{CHARACTER_SKINS[selectedSkinId]?.name || 'Phục Trang'}</b>
                </span>
              </div>

              {/* 5 Outfit Cards Row */}
              <div className="grid grid-cols-5 gap-1.5">
                {Object.values(CHARACTER_SKINS).map((sk) => {
                  const isSelected = selectedSkinId === sk.id;
                  const isSectMatch = sk.sectId === selectedClassId;
                  return (
                    <button
                      key={sk.id}
                      type="button"
                      onClick={() => handleSelectSkin(sk.id)}
                      className={`relative rounded-xl border p-1 text-center cursor-pointer transition-all flex flex-col items-center gap-1 group ${
                        isSelected
                          ? 'bg-slate-800/90 border-amber-400 ring-2 ring-amber-400/50 shadow-lg scale-105 z-10'
                          : 'bg-slate-950/70 border-slate-800 hover:border-slate-700 hover:bg-slate-900/60'
                      }`}
                      title={`${sk.name} · ${sk.sectTitle}\n${sk.description}`}
                    >
                      {/* Sect Recommended Tag */}
                      {isSectMatch && (
                        <div className="absolute -top-1.5 -right-1 px-1 py-0.2 rounded-full bg-amber-500 text-slate-950 text-[7px] font-bold z-20 shadow">
                          CHUẨN
                        </div>
                      )}

                      {/* Outfit Card Image */}
                      <div className="w-full aspect-[3/4] rounded-lg overflow-hidden bg-slate-900/90 relative border border-slate-700/50">
                        <img
                          src={`${import.meta.env.BASE_URL || './'}${sk.cardPath}`}
                          alt={sk.name}
                          className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
                        />
                        <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent pointer-events-none" />
                        <span className="absolute bottom-0.5 right-1 text-[11px]">{sk.icon}</span>
                      </div>

                      {/* Outfit Short Name */}
                      <span className={`text-[9px] font-tech font-bold leading-tight truncate w-full ${
                        isSelected ? 'text-amber-300' : 'text-slate-300'
                      }`}>
                        {sk.name.replace('Phàm Nhân ', '').replace('Cửu Tiêu ', '').replace('Hắc Diệm ', '').replace('Bất Chu ', '').replace('Thanh Mộc ', '')}
                      </span>
                    </button>
                  );
                })}
              </div>

              {/* Lore / Description Line */}
              <div className="text-[10px] font-tech text-slate-400 italic bg-slate-950/60 py-1 px-2 rounded-lg border border-slate-800/60 truncate">
                ✨ {CHARACTER_SKINS[selectedSkinId]?.description || ''}
              </div>
            </div>
          </div>

          {/* RIGHT COLUMN: SECT SELECTION, SKILLS, AND COMMIT */}
          <div className="lg:col-span-7 flex flex-col gap-2.5">
            {/* Character Name Input Row */}
            <div className="p-3 rounded-2xl bg-slate-900/70 border border-slate-800 flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-2.5">
              <div className="text-xs font-tech font-semibold text-slate-300 whitespace-nowrap">
                ĐẠO HIỆU THỢ RÈN:
              </div>
              <div className="flex items-center gap-2 flex-1">
                <input
                  type="text"
                  maxLength={24}
                  value={characterName}
                  onChange={(e) => setCharacterName(e.target.value)}
                  placeholder="Nhập tên nhân vật..."
                  className="flex-1 bg-slate-950 border border-slate-700 focus:border-amber-400 px-3 py-1.5 rounded-xl text-sm font-tech text-amber-200 outline-none transition-colors"
                />
                <button
                  type="button"
                  onClick={handleRandomizeName}
                  className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-amber-300 border border-slate-700 text-xs font-tech cursor-pointer transition-colors shrink-0"
                  title="Ngẫu nhiên tên thợ rèn hào hiệp"
                >
                  <Dices className="w-3.5 h-3.5" />
                  <span>Ngẫu Nhiên</span>
                </button>
              </div>
            </div>

            {/* 4 Class Cards Grid */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
              {(Object.keys(PLAYER_CLASSES) as PlayerClassId[]).map((cId) => {
                const cls = PLAYER_CLASSES[cId];
                const isSelected = selectedClassId === cId;
                return (
                  <button
                    key={cId}
                    type="button"
                    onClick={() => handleSelectClass(cId)}
                    className={`p-2.5 rounded-2xl border text-left transition-all cursor-pointer flex flex-col justify-between min-h-[100px] relative overflow-hidden ${
                      isSelected
                        ? 'bg-slate-900/95 border-amber-400 ring-2 ring-amber-400/40 shadow-lg scale-[1.02]'
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
                      <div className="flex items-center gap-1.5 mb-1">
                        <div className="w-6 h-6 rounded-lg flex items-center justify-center bg-slate-950/80 border border-slate-800 shrink-0">
                          {getClassIcon(cId)}
                        </div>
                        <div className="min-w-0">
                          <h3 className={`text-xs font-bold font-tech truncate ${cls.textColor}`}>
                            {cls.name}
                          </h3>
                        </div>
                      </div>
                      <div className="text-[10px] text-slate-300 font-tech font-semibold truncate">
                        {cls.sectTitle.split('·')[0].trim()}
                      </div>
                    </div>

                    <div className="text-[9px] text-slate-400 font-tech mt-1.5 pt-1 border-t border-slate-800/70 truncate">
                      {cls.primaryStats.join(' · ')}
                    </div>
                  </button>
                );
              })}
            </div>

            {/* Selected Class Deep-Dive Showcase */}
            <div className="p-3.5 rounded-2xl bg-gradient-to-b from-[#0B0F1E] to-[#070912] border border-slate-800 flex flex-col gap-2.5">
              {/* Header of Class */}
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-1.5 border-b border-slate-800/80 pb-2">
                <div>
                  <div className="flex items-center gap-2">
                    <span className={`text-[11px] px-2 py-0.5 rounded-lg border font-tech font-bold ${selectedClass.badgeBg}`}>
                      {selectedClass.sectTitle}
                    </span>
                    <span className="text-[11px] text-slate-400 font-tech">Vũ khí: {selectedClass.weaponName}</span>
                  </div>
                  <p className="text-[11px] text-amber-200/90 italic font-tech mt-1">
                    "{selectedClass.motto}"
                  </p>
                </div>

                <div className="text-left sm:text-right font-tech text-xs">
                  <span className="text-slate-400">Đặc tính: </span>
                  <span className="text-cyan-300 font-bold">{selectedClass.roleSummary}</span>
                </div>
              </div>

              {/* 4 Skills [Q] [W] [E] [R] Evolution Grid */}
              <div>
                <div className="text-[10px] font-tech font-bold text-amber-300 uppercase tracking-wider mb-1.5 flex items-center gap-1.5">
                  <Sparkles className="w-3 h-3 text-amber-400" />
                  <span>BỘ 4 KỸ NĂNG TIẾN HÓA CỦA {selectedClass.name.toUpperCase()} (Q - W - E - R):</span>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs font-tech">
                  {(['Q', 'W', 'E', 'R'] as const).map((slotKey) => {
                    const sk = selectedClass.skills[slotKey];
                    return (
                      <div
                        key={slotKey}
                        className="p-2 rounded-xl bg-slate-950/70 border border-slate-800/80 flex items-start gap-2"
                      >
                        <div className="w-7 h-7 rounded-lg bg-slate-900 border border-slate-700 flex flex-col items-center justify-center shrink-0">
                          <span className="text-xs font-bold text-amber-300">[{slotKey}]</span>
                          <span className="text-[7px] text-slate-400">{sk.unlockLevel === 1 ? 'Lv.1' : `Lv.${sk.unlockLevel}`}</span>
                        </div>

                        <div className="flex-1 min-w-0">
                          <div className="flex items-center justify-between gap-1 mb-0.5">
                            <span className="font-bold text-slate-200 text-xs truncate">
                              {sk.name}
                            </span>
                            <span className="text-[9px] text-cyan-300 shrink-0">
                              {sk.cooldownSec > 0 ? `CD ${sk.cooldownSec}s` : sk.overdriveCost > 0 ? `Tốn ${sk.overdriveCost} OD` : 'Nội tại'}
                            </span>
                          </div>
                          <div className="text-[9px] text-amber-400/90 font-medium mb-0.5">
                            {sk.typeTitle}
                          </div>
                          <p className="text-[10px] text-slate-400 leading-snug line-clamp-2">
                            {sk.description}
                          </p>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* Sub-Classes Future Specialization */}
              <div className="pt-1.5 border-t border-slate-800/80 flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-1 text-[11px] font-tech">
                <div className="text-slate-400">
                  <span className="text-slate-300 font-bold">2 Nhánh Chuyển Chức (Lv.120): </span>
                  <span className="text-purple-300">① {selectedClass.subClasses.a.name} ({selectedClass.subClasses.a.focus})</span>
                  <span> · </span>
                  <span className="text-emerald-300">② {selectedClass.subClasses.b.name} ({selectedClass.subClasses.b.focus})</span>
                </div>
              </div>
            </div>

            {/* CTA Confirmation Button */}
            <div className="pt-1 flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3">
              <div className="text-[11px] text-slate-400 font-tech">
                Sau khi bái sư, 4 phím Q W E R sẽ mở khóa bộ chiêu thức tiến hóa của {selectedClass.name}.
              </div>

              <button
                type="button"
                disabled={isSubmitting}
                onClick={handleCommit}
                className="group flex items-center justify-center gap-2.5 px-7 py-3 rounded-2xl bg-gradient-to-r from-amber-500 via-amber-400 to-yellow-500 hover:from-amber-400 hover:to-yellow-400 text-slate-950 font-tech font-bold text-xs sm:text-sm tracking-[0.12em] uppercase shadow-lg shadow-amber-500/25 transition-all cursor-pointer active:scale-95 shrink-0"
              >
                <span>BÁI SƯ NHẬP PHÁI — BƯỚC VÀO THIÊN TRẬN</span>
                <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
