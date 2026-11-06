import React, { useState } from 'react';
import { 
  Globe, Users, Zap, Flame, Mountain, Music, Shield, Sparkles, 
  Newspaper, CheckCircle2, ChevronRight, Award, FlameKindling, Swords
} from 'lucide-react';
import { PLAYER_CLASSES, PlayerClassId, CHARACTER_SKINS } from '../game/rules';

export type TitleNavTab = 'home' | 'world' | 'character' | 'features' | 'news';

interface TitlePageProps {
  activeTab: TitleNavTab;
  onSelectTab: (tab: TitleNavTab) => void;
  onStartGame: () => void;
}

export const TitlePagesOverlay: React.FC<TitlePageProps> = ({
  activeTab,
  onSelectTab,
  onStartGame,
}) => {
  const [selectedClassId, setSelectedClassId] = useState<PlayerClassId>('thunder');
  const [characterViewMode, setCharacterViewMode] = useState<'sects' | 'wardrobe'>('sects');
  const base = import.meta.env.BASE_URL || './';
  const cleanBase = base.endsWith('/') ? base : base + '/';

  if (activeTab === 'home') return null;

  return (
    <div className="fixed inset-0 z-40 bg-slate-950/85 backdrop-blur-2xl flex flex-col justify-between p-4 sm:p-8 md:p-12 text-slate-100 overflow-y-auto animate-in fade-in duration-300">
      {/* 1. Header Toolbar with Tab Indicator, Nav Switcher & Close Button */}
      <div className="w-full max-w-6xl mx-auto flex flex-col md:flex-row items-center justify-between border-b border-amber-500/20 pb-4 gap-3 shrink-0">
        <div className="flex items-center gap-3 w-full md:w-auto">
          <div className="w-9 h-9 rounded-xl border border-amber-400/40 bg-slate-900/90 flex items-center justify-center text-amber-300 font-bold text-sm shadow-[0_0_15px_rgba(251,191,36,0.2)] shrink-0">
            {activeTab === 'world' && <Globe className="w-5 h-5" />}
            {activeTab === 'character' && <Users className="w-5 h-5" />}
            {activeTab === 'features' && <Sparkles className="w-5 h-5" />}
            {activeTab === 'news' && <Newspaper className="w-5 h-5" />}
          </div>
          <div>
            <h2 className="text-xs sm:text-sm md:text-base font-bold font-tech text-amber-300 tracking-wider uppercase">
              {activeTab === 'world' && 'THẾ GIỚI · LỤC TRỌNG THIÊN & ĐÚC THẦN ĐÀI'}
              {activeTab === 'character' && 'NHÂN VẬT · TỨ ĐẠI MÔN PHÁI & TỦ ĐỒ TIÊN GIA'}
              {activeTab === 'features' && 'TÍNH NĂNG · GAMEPLAY HÀNH ĐỘNG RÈN BÚA & RAID THẾ GIỚI'}
              {activeTab === 'news' && 'TIN TỨC · BẢN CẬP NHẬT MÁY CHỦ PHÁ TRỜI'}
            </h2>
            <p className="text-[10px] sm:text-[11px] text-slate-400 font-tech">
              Hệ thống tra cứu thông tin chính thức của Webgame Phá Trời (phatroi.com)
            </p>
          </div>
        </div>

        {/* Center Nav tabs inside overlay */}
        <div className="flex items-center gap-1 sm:gap-2 text-[11px] sm:text-xs font-tech tracking-[0.12em] uppercase bg-slate-900/90 p-1.5 rounded-full border border-slate-800 overflow-x-auto max-w-full">
          {[
            { tab: 'home' as TitleNavTab, label: 'TRANG CHỦ' },
            { tab: 'world' as TitleNavTab, label: 'THẾ GIỚI' },
            { tab: 'character' as TitleNavTab, label: 'NHÂN VẬT' },
            { tab: 'features' as TitleNavTab, label: 'TÍNH NĂNG' },
            { tab: 'news' as TitleNavTab, label: 'TIN TỨC' },
          ].map((item) => (
            <button
              key={item.tab}
              type="button"
              onClick={() => onSelectTab(item.tab)}
              className={`px-2.5 sm:px-3 py-1 rounded-full transition-all cursor-pointer whitespace-nowrap ${
                activeTab === item.tab
                  ? 'bg-amber-500/25 text-amber-300 border border-amber-400/60 font-bold shadow-[0_0_12px_rgba(251,191,36,0.4)]'
                  : 'text-slate-400 hover:text-amber-200'
              }`}
            >
              {item.label}
            </button>
          ))}
        </div>

        {/* Quick Close / Return to Home */}
        <button
          type="button"
          onClick={() => onSelectTab('home')}
          className="px-4 py-1.5 rounded-full bg-slate-900/90 hover:bg-slate-800 border border-slate-700/80 hover:border-amber-400/60 text-xs font-tech text-slate-300 hover:text-amber-200 transition-all cursor-pointer flex items-center gap-1.5 shrink-0 self-end md:self-auto"
        >
          <span>✕ ĐÓNG</span>
        </button>
      </div>

      {/* 2. Main Page Content Body */}
      <div className="w-full max-w-6xl mx-auto my-6 flex-1">
        {/* ============================================================== */}
        {/* TAB 1: THẾ GIỚI (WORLD & LORE) */}
        {/* ============================================================== */}
        {activeTab === 'world' && (
          <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-300">
            {/* World Summary Banner */}
            <div className="relative rounded-2xl overflow-hidden border border-amber-500/30 bg-gradient-to-r from-slate-900/95 via-slate-900/70 to-slate-950/95 p-6 md:p-8 shadow-2xl">
              <div className="max-w-2xl">
                <span className="text-[11px] font-tech text-amber-400 font-bold uppercase tracking-widest px-2.5 py-1 rounded bg-amber-500/10 border border-amber-500/30">
                  CỔ THẦN BỐI CẢNH
                </span>
                <h3 className="text-xl md:text-2xl font-bold font-tech text-slate-100 mt-3 mb-2">
                  Đại Lò Rèn Vạn Cổ & Mái Vòm Thiên Đạo
                </h3>
                <p className="text-xs sm:text-sm text-slate-300 leading-relaxed font-light">
                  Từ thời Thái Cổ, bầu trời không phải là hư vô mà là một **Mái Vòm Phong Ấn** giam cầm linh khí của nhân gian. 
                  Trên đỉnh núi Bất Chu, vạn dân cùng tề tựu quanh **Vạn Cổ Đúc Thần Đài** — nơi chiếc Búa Khởi Nguyên giáng xuống đe thép, 
                  hội tụ sức mạnh của hàng ngàn thợ rèn online cùng lúc để làm nứt vỡ từng tầng trời, tái sinh thiên đạo.
                </p>
              </div>
            </div>

            {/* 6 Sky States / 6 Tầng Trời Phá Giới */}
            <div>
              <h4 className="text-xs font-tech font-bold text-amber-300 tracking-wider uppercase mb-3 flex items-center gap-2">
                <span>✧ LỤC TRỌNG THIÊN ĐẠO (6 TRẠNG THÁI VÒM TRỜI KHI THỢ RÈN GIÁNG BÚA)</span>
              </h4>
              <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-3">
                {[
                  { id: 1, name: 'Sơ Khởi', desc: 'Bầu trời nguyên vẹn, phong ấn kiên cố', pct: '100% HP', file: 'sky_state_1_pristine.webp' },
                  { id: 2, name: 'Rạn Nứt', desc: 'Những vết nứt lôi quang đầu tiên xuất hiện', pct: '80% HP', file: 'sky_state_2_incipient.webp' },
                  { id: 3, name: 'Lan Rộng', desc: 'Vết nứt không gian chằng chịt khắp vòm trời', pct: '60% HP', file: 'sky_state_3_spreading.webp' },
                  { id: 4, name: 'Tai Ương', desc: 'Bão từ và mảnh vụn thiên thạch trút xuống', pct: '40% HP', file: 'sky_state_4_severe.webp' },
                  { id: 5, name: 'Hỗn Mang', desc: 'Hư không rách toạc, vòm trời sắp sụp đổ', pct: '20% HP', file: 'sky_state_5_cataclysm.webp' },
                  { id: 6, name: 'Phá Trời', desc: 'Thiên đạo vỡ tan hoàn toàn, vạn dân đắc đạo', pct: '0% HP', file: 'sky_state_6_shattered.webp' },
                ].map((s) => (
                  <div key={s.id} className="rounded-xl border border-slate-800 bg-slate-900/60 p-2.5 flex flex-col gap-2 hover:border-amber-400/50 transition-all group">
                    <div className="aspect-[4/3] rounded-lg overflow-hidden bg-slate-950 relative border border-slate-800">
                      <img 
                        src={`${cleanBase}assets/art/sky_states/${s.file}`} 
                        alt={s.name} 
                        className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500" 
                      />
                      <span className="absolute bottom-1 right-1 px-1.5 py-0.5 rounded bg-black/80 text-[9px] font-mono font-bold text-amber-300">
                        {s.pct}
                      </span>
                    </div>
                    <div>
                      <h5 className="text-xs font-bold text-slate-200 font-tech">Tầng {s.id}: {s.name}</h5>
                      <p className="text-[10px] text-slate-400 font-light mt-0.5 leading-tight">{s.desc}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* 4 Sacred Blacksmith Guilds / Thánh Địa Rèn */}
            <div>
              <h4 className="text-xs font-tech font-bold text-amber-300 tracking-wider uppercase mb-3 flex items-center gap-2">
                <span>✧ TỨ ĐẠI THÁNH ĐỊA RÈN BÚA NHÂN GIAN</span>
              </h4>
              <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-3">
                {[
                  { name: 'Thiên Thai Phường', sect: 'Lôi Đình Tông', icon: '⚡', color: 'border-cyan-500/40 text-cyan-300', desc: 'Ngự trên đỉnh mây sấm sét, chuyên rèn Lôi Kiếm và búa sét tốc độ cao, đòn búa nhanh như ánh chớp.' },
                  { name: 'Phần Thiên Các', sect: 'Viêm Dương Phái', icon: '🔥', color: 'border-red-500/40 text-red-300', desc: 'Tọa lạc giữa biển nham thạch ma vực, kiểm soát Hỏa Hẩu cực hạn, nhát búa nung đỏ thiêu đốt vạn vật.' },
                  { name: 'Bất Chu Sơn', sect: 'Sơn Nhạc Tông', icon: '⛰️', color: 'border-purple-500/40 text-purple-300', desc: 'Dưới chân cột chống trời, đúc giáp đá Huyền Vũ ngàn cân, nhát búa mang uy lực trọng lực đè bẹp phòng ngự.' },
                  { name: 'Thái Ất Tông', sect: 'Huyền Âm Phái', icon: '🎵', color: 'border-emerald-500/40 text-emerald-300', desc: 'Ẩn mình trong rừng trúc bích ngọc, hòa âm tiếng búa như tiếng chuông khánh, hồi phục đe và ban phước cho toàn đội.' },
                ].map((g, i) => (
                  <div key={i} className={`rounded-xl border ${g.color} bg-slate-900/60 p-3.5 flex flex-col gap-2`}>
                    <div className="flex items-center gap-2">
                      <span className="text-2xl">{g.icon}</span>
                      <div>
                        <h5 className="text-xs font-bold font-tech text-slate-100">{g.name}</h5>
                        <span className="text-[10px] text-amber-400 font-tech">{g.sect}</span>
                      </div>
                    </div>
                    <p className="text-[11px] text-slate-400 leading-relaxed font-light">{g.desc}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* ============================================================== */}
        {/* TAB 2: NHÂN VẬT (CHARACTERS & WARDROBE) */}
        {/* ============================================================== */}
        {activeTab === 'character' && (
          <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-300">
            {/* View Mode Toggle */}
            <div className="flex items-center justify-between flex-wrap gap-2">
              <div className="flex items-center gap-2 bg-slate-900/90 border border-slate-800 rounded-xl p-1">
                <button
                  type="button"
                  onClick={() => setCharacterViewMode('sects')}
                  className={`px-3 py-1 rounded-lg text-xs font-tech font-bold transition-all cursor-pointer ${
                    characterViewMode === 'sects' ? 'bg-amber-400 text-slate-950 shadow' : 'text-slate-400 hover:text-slate-200'
                  }`}
                >
                  ⚔️ TỨ ĐẠI MÔN PHÁI (Q W E R)
                </button>
                <button
                  type="button"
                  onClick={() => setCharacterViewMode('wardrobe')}
                  className={`px-3 py-1 rounded-lg text-xs font-tech font-bold transition-all cursor-pointer ${
                    characterViewMode === 'wardrobe' ? 'bg-amber-400 text-slate-950 shadow' : 'text-slate-400 hover:text-slate-200'
                  }`}
                >
                  👘 TỦ ĐỒ TIÊN GIA (7 BỘ TRANG PHỤC)
                </button>
              </div>

              <span className="text-xs text-slate-400 font-tech">
                {characterViewMode === 'sects' ? 'Chọn môn phái để xem chiêu thức & phong cách' : 'Bao gồm các bộ Thần Thoại mới cập nhật'}
              </span>
            </div>

            {/* SUB-VIEW 1: TỨ ĐẠI MÔN PHÁI */}
            {characterViewMode === 'sects' && (
              <div className="space-y-4">
                {/* Sect Selector Tabs */}
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
                  {(Object.keys(PLAYER_CLASSES) as PlayerClassId[]).map((cId) => {
                    const cls = PLAYER_CLASSES[cId];
                    const isSelected = selectedClassId === cId;
                    return (
                      <button
                        key={cId}
                        type="button"
                        onClick={() => setSelectedClassId(cId)}
                        className={`p-2.5 rounded-xl border text-left cursor-pointer transition-all flex items-center gap-2.5 ${
                          isSelected
                            ? 'bg-slate-900/95 border-amber-400 shadow-lg scale-[1.02] ring-1 ring-amber-400/50'
                            : 'bg-slate-900/50 border-slate-800 hover:border-slate-700'
                        }`}
                      >
                        <span className="text-2xl">{cls.icon}</span>
                        <div className="min-w-0">
                          <h5 className="text-xs font-bold font-tech text-slate-200 truncate">{cls.name}</h5>
                          <span className="text-[10px] text-amber-400/90 font-tech block truncate">{cls.sectTitle.split('·')[0]}</span>
                        </div>
                      </button>
                    );
                  })}
                </div>

                {/* Selected Sect Full Detail Card */}
                {(() => {
                  const cls = PLAYER_CLASSES[selectedClassId];
                  return (
                    <div className="rounded-2xl border border-amber-500/30 bg-slate-900/80 p-5 md:p-6 space-y-4 shadow-xl">
                      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-3 border-b border-slate-800 pb-3">
                        <div className="flex items-center gap-3">
                          <div className="w-12 h-12 rounded-xl border border-amber-400/50 bg-slate-950 flex items-center justify-center text-3xl shadow">
                            {cls.icon}
                          </div>
                          <div>
                            <h3 className="text-base sm:text-lg font-bold font-tech text-amber-300">
                              {cls.name} · {cls.sectTitle}
                            </h3>
                            <p className="text-xs text-slate-300 italic font-light">"{cls.motto}"</p>
                          </div>
                        </div>

                        <div className="flex items-center gap-2">
                          <span className="px-2.5 py-1 rounded bg-slate-950 border border-slate-700 text-xs font-mono font-bold text-slate-300">
                            VŨ KHÍ: {cls.weaponName}
                          </span>
                        </div>
                      </div>

                      {/* 4 Skill Cards Q W E R */}
                      <div>
                        <h4 className="text-xs font-tech font-bold text-slate-400 uppercase tracking-wider mb-2">
                          BỘ 4 CHIÊU THỨC CHÂN TRUYỀN (HOTKEYS: Q, W, E, R)
                        </h4>
                        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-2.5 font-tech">
                          {(['Q', 'W', 'E', 'R'] as const).map((key) => {
                            const sk = cls.skills[key];
                            return (
                              <div key={key} className="rounded-xl border border-slate-800 bg-slate-950/70 p-3 flex flex-col justify-between gap-2">
                                <div className="flex items-center justify-between">
                                  <span className="w-6 h-6 rounded-lg bg-amber-500/20 border border-amber-500/40 text-amber-300 font-bold text-xs flex items-center justify-center">
                                    {key}
                                  </span>
                                  <span className="text-[10px] text-slate-400">{sk.typeTitle}</span>
                                </div>
                                <div>
                                  <h5 className="text-xs font-bold text-slate-100 flex items-center gap-1">
                                    <span>{sk.icon}</span>
                                    <span>{sk.name}</span>
                                  </h5>
                                  <p className="text-[10px] text-slate-400 mt-1 leading-relaxed font-light">{sk.description}</p>
                                </div>
                                <div className="text-[9px] text-amber-400/80 pt-1 border-t border-slate-800/60 flex justify-between">
                                  <span>Hồi chiêu: {sk.cooldownSec}s</span>
                                  <span>Hao Overdrive: {sk.overdriveCost}</span>
                                </div>
                              </div>
                            );
                          })}
                        </div>
                      </div>
                    </div>
                  );
                })()}
              </div>
            )}

            {/* SUB-VIEW 2: TỦ ĐỒ TIÊN GIA SHOWCASE */}
            {characterViewMode === 'wardrobe' && (
              <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-7 gap-3">
                {Object.values(CHARACTER_SKINS).map((sk) => (
                  <div key={sk.id} className="rounded-xl border border-slate-800 bg-slate-900/70 p-2 flex flex-col gap-2 hover:border-amber-400/60 transition-all group">
                    <div className="w-full aspect-[3/4] rounded-lg overflow-hidden bg-slate-950 relative border border-slate-800">
                      <img 
                        src={`${cleanBase}${sk.cardPath}`} 
                        alt={sk.name} 
                        className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300" 
                      />
                      <span className="absolute bottom-1 right-1 text-sm drop-shadow">{sk.icon}</span>
                      <span className={`absolute top-1 left-1 px-1.5 py-0.2 rounded text-[8px] font-bold uppercase ${sk.rarityBadgeBg}`}>
                        {sk.rarity.replace('_', ' ')}
                      </span>
                    </div>
                    <div className="min-w-0">
                      <h5 className="text-xs font-bold text-slate-200 font-tech truncate">{sk.name}</h5>
                      <span className="text-[10px] text-amber-400/90 font-tech block truncate">{sk.sectTitle}</span>
                      <p className="text-[9px] text-slate-400 font-light mt-1 line-clamp-2 leading-tight">
                        {sk.description}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* ============================================================== */}
        {/* TAB 3: TÍNH NĂNG (GAMEPLAY MECHANICS) */}
        {/* ============================================================== */}
        {activeTab === 'features' && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 animate-in fade-in slide-in-from-bottom-4 duration-300">
            {[
              {
                title: 'Búa Rèn Canh Nhịp (100 BPM Rhythm Forge)',
                icon: '⚡',
                badge: 'HÀNH ĐỘNG JUICY',
                desc: 'Vòng hào quang thu hẹp nhịp nhàng trên đe thép. Bấm phím Cách hoặc chạm màn hình đúng tâm vàng để kích hoạt đòn PERFECT: sát thương x3.5, nổ tung 3.000 hạt tia lửa sấm sét và rung chấn màn hình.',
              },
              {
                title: 'Hỏa Hẩu & Overdrive Tầng 3',
                icon: '🔥',
                badge: 'CHIẾN THUẬT QUẢN LÝ NHIỆT',
                desc: 'Mỗi cú gõ hoàn hảo tích nhiệt cho Lò Rèn Vạn Cổ. Khi đạt 8/8 ngọc Overdrive, thợ rèn kích hoạt trạng thái Bạo Phát: tăng tốc độ vung búa, mở khóa kỹ năng E/R và tăng mạnh tỷ lệ rớt bảo vật.',
              },
              {
                title: 'Hệ Thống Rơi Đồ MMORPG 6 Bậc (Tier E -> S)',
                icon: '🛡️',
                badge: 'TRANG BỊ & CHẾ TÁC',
                desc: 'Săn lùng trang bị Bậc E (Phàm Thiết) đến Bậc S (Thiên Đạo Thần Khí). Mỗi trang bị đi kèm chỉ số độc bản, kích hoạt bộ Set Perks môn phái, lò tôi luyện Quench (Băng, Hỏa, Lôi) và khảm nạp Ngọc Bát Quái.',
              },
              {
                title: 'Cơ Chế Bảo Hiểm Rơi Đồ (Pity System 200 Hits)',
                icon: '👑',
                badge: 'CÔNG BẰNG & MINH BẠCH',
                desc: 'Hệ thống tự động tích lũy điểm kiên trì. Nếu sau 200 nhát búa chưa rơi trang bị Bậc A+ (Legendary), hệ thống bảo hiểm sẽ kích hoạt 100% rớt Thần Khí tối thượng ngay tại nhát gõ tiếp theo.',
              },
              {
                title: 'Kênh Thế Giới Realtime (Multiplayer Amphitheater)',
                icon: '🌐',
                badge: 'HÀNG NGÀN NGƯỜI CÙNG LÚC',
                desc: 'Toàn bộ thợ rèn đang online đều hiển thị trực tiếp trên các tầng đài đá xung quanh bạn. Cùng chia sẻ hào quang buff, tích lũy điểm RCS (Raid Contribution Score) và cùng phá sụp Mái Vòm Thiên Đạo.',
              },
              {
                title: 'Lưu Trữ Đám Mây & 3 Slot Nhân Vật Độc Lập',
                icon: '☁️',
                badge: 'ĐA TÀI KHOẢN',
                desc: 'Đăng nhập Google chỉ với 1 chạm để sao lưu vĩnh viễn túi đồ và cấp bậc rèn. Quản lý 3 Slot nhân vật riêng biệt với 3 môn phái và phong cách chiến đấu hoàn toàn khác nhau.',
              },
            ].map((f, i) => (
              <div key={i} className="rounded-2xl border border-slate-800 bg-slate-900/70 p-5 flex flex-col gap-2.5 hover:border-amber-400/40 transition-all">
                <div className="flex items-center justify-between">
                  <span className="text-2xl">{f.icon}</span>
                  <span className="text-[10px] font-tech font-bold px-2 py-0.5 rounded bg-amber-500/10 border border-amber-500/30 text-amber-300">
                    {f.badge}
                  </span>
                </div>
                <h4 className="text-sm font-bold font-tech text-slate-100">{f.title}</h4>
                <p className="text-xs text-slate-300 leading-relaxed font-light">{f.desc}</p>
              </div>
            ))}
          </div>
        )}

        {/* ============================================================== */}
        {/* TAB 4: TIN TỨC (NEWS & PATCH NOTES) */}
        {/* ============================================================== */}
        {activeTab === 'news' && (
          <div className="space-y-4 max-w-4xl mx-auto animate-in fade-in slide-in-from-bottom-4 duration-300">
            {[
              {
                version: 'v3.4 · BẢN CẬP NHẬT Y PHỤC THẦN THOẠI & AUDIT TOÀN DIỆN',
                date: '06/11/2026',
                tag: 'MỚI NHẤT',
                tagColor: 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40',
                points: [
                  'Ra mắt 2 bộ Y Phục Thần Thoại đỉnh cao: [Thái Cổ Lôi Thần Giáp] & [Phần Thiên Ma Tổ] với chuyển động nện búa thực tế 6 khung hình.',
                  'Khắc phục triệt để lỗi cơ chế Bảo Hiểm Pity (Đảm bảo rớt trang bị Bậc S sau 200 nhát gõ).',
                  'Sửa toàn bộ lỗi bộ lọc Túi Phù Thạch (⚡ Lôi, 🔥 Hỏa, ⛰️ Sơn, 🎵 Âm, 🌟 Vận).',
                  'Khắc phục lỗi màn hình thử đồ và tối ưu hóa 100% TypeScript type safety.',
                ]
              },
              {
                version: 'v3.3 · ĐẠI CHIẾN TỨ ĐẠI MÔN PHÁI (Q W E R SYSTEM)',
                date: '05/11/2026',
                tag: 'TÍNH NĂNG LỚN',
                tagColor: 'bg-cyan-500/20 text-cyan-300 border-cyan-500/40',
                points: [
                  'Chính thức ra mắt Tứ Đại Môn Phái: Lôi Đình, Phần Thiên, Bất Chu Sơn, Thái Ất Tông.',
                  'Mỗi môn phái sở hữu 4 kỹ năng Q W E R độc bản với thời gian hồi chiêu và tiêu hao Overdrive riêng biệt.',
                  'Đồng bộ tư thế và hiệu ứng đòn đánh tới toàn bộ thợ rèn trong phòng chơi nhiều người.',
                ]
              },
              {
                version: 'v3.2 · HỆ THỐNG TRANG BỊ MMORPG & TỔ ĐỂ BÁT QUÁI',
                date: '04/11/2026',
                tag: 'HỆ THỐNG ĐÚC',
                tagColor: 'bg-amber-500/20 text-amber-300 border-amber-500/40',
                points: [
                  'Hệ thống trang bị 6 bậc từ Tier E đến Tier S Thần Khí.',
                  'Mở tính năng Tôi Luyện Quench (Băng, Hỏa, Lôi) và Khảm Nạp Phù Thạch.',
                  'Nâng cấp giao diện Mobile AAA: hỗ trợ Safe Area, Thumb Dock và phản hồi rung Haptics.',
                ]
              },
            ].map((n, i) => (
              <div key={i} className="rounded-2xl border border-slate-800 bg-slate-900/80 p-5 space-y-3">
                <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-1 border-b border-slate-800 pb-2.5">
                  <div className="flex items-center gap-2">
                    <span className={`text-[10px] font-tech font-bold px-2 py-0.5 rounded border ${n.tagColor}`}>
                      {n.tag}
                    </span>
                    <h4 className="text-xs sm:text-sm font-bold font-tech text-amber-300">{n.version}</h4>
                  </div>
                  <span className="text-[11px] font-mono text-slate-400">{n.date}</span>
                </div>
                <ul className="space-y-1.5 text-xs text-slate-300 font-light">
                  {n.points.map((pt, j) => (
                    <li key={j} className="flex items-start gap-2">
                      <span className="text-amber-400 text-xs mt-0.5">•</span>
                      <span>{pt}</span>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* 3. Bottom Action Bar with Enter Game Button */}
      <div className="w-full max-w-6xl mx-auto flex items-center justify-between border-t border-slate-800/80 pt-4 shrink-0 text-xs font-tech">
        <div className="text-slate-400">
          <span>Đang xem: </span>
          <b className="text-amber-300 uppercase">
            {activeTab === 'world' && 'Thế Giới'}
            {activeTab === 'character' && 'Nhân Vật & Ngoại Trang'}
            {activeTab === 'features' && 'Tính Năng Gameplay'}
            {activeTab === 'news' && 'Bản Cập Nhật'}
          </b>
        </div>

        <button
          type="button"
          onClick={onStartGame}
          className="px-6 py-2 rounded-full bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-slate-950 font-bold tracking-wider uppercase transition-all shadow-lg hover:shadow-amber-500/30 cursor-pointer active:scale-95 flex items-center gap-2"
        >
          <span>VÀO GAME NGAY</span>
          <ChevronRight className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
};
