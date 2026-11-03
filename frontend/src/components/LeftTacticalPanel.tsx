import React, { useState } from 'react';
import {
  Send,
  Swords,
  ScrollText,
  MessageSquare,
  Award,
  CheckCircle,
  Flame,
  Layers,
  Sparkles,
  Users,
  Compass,
  Zap,
} from 'lucide-react';
import {
  HAMMER_STANCES,
  StanceKey,
  CONTRIBUTION_TIERS,
  ContributionTier,
  formatInteger,
  CELESTIAL_VAULTS,
  getCelestialVault,
  CelestialVault,
  BLACKSMITH_GUILDS,
  getGuild,
  BlacksmithGuild,
} from '../game/rules';

export interface CombatLogEntry {
  id: number;
  timestamp: string;
  text: string;
  tone: 'gold' | 'cyan' | 'red' | 'neutral';
}

export interface ChatMessage {
  id: number;
  sender: string;
  realm: string;
  content: string;
  isPlayer?: boolean;
}

interface LeftTacticalPanelProps {
  activeStance: StanceKey;
  playerTotalDamage: number;
  playerTotalDamageBillions?: number;
  perfectCount: number;
  maxCombo: number;
  serverDps?: number;
  serverDpsBillions?: number;
  claimedMilestones?: string[];
  onClaimMilestone?: (tierId: string) => void;
  combatLogs: CombatLogEntry[];
  chatMessages: ChatMessage[];
  onSendChat: (msg: string) => void;
  // Phase 3 additions:
  currentVaultId?: number;
  onSelectVault?: (vaultId: number) => void;
  userGuildId?: string;
  onSelectGuild?: (guildId: string) => void;
  guildHearths?: Record<string, { level: number; exp: number }>;
  onDonateHearth?: (guildId: string, amount: number) => void;
  linhThach?: number;
}

export const LeftTacticalPanel: React.FC<LeftTacticalPanelProps> = ({
  activeStance,
  playerTotalDamage,
  playerTotalDamageBillions,
  perfectCount,
  maxCombo,
  serverDps = 2000,
  serverDpsBillions,
  claimedMilestones = [],
  onClaimMilestone,
  combatLogs,
  chatMessages,
  onSendChat,
  currentVaultId = 1,
  onSelectVault,
  userGuildId = 'guild_thien_thai',
  onSelectGuild,
  guildHearths = {},
  onDonateHearth,
  linhThach = 0,
}) => {
  const [activeTab, setActiveTab] = useState<'tactical' | 'guild' | 'vaults'>('tactical');
  const [inputText, setInputText] = useState('');
  const stanceInfo = HAMMER_STANCES[activeStance];

  // Resolve current guild & vault
  const currentGuild = getGuild(userGuildId);
  const currentVault = getCelestialVault(currentVaultId);
  const hearthState = guildHearths[userGuildId] || { level: 1, exp: 0 };
  const expNeeded = hearthState.level * 1000;
  const hearthProgressPct = Math.min(100, Math.max(0, (hearthState.exp / expNeeded) * 100));

  // Resolve total damage integer
  const currentDamage = Math.round(
    typeof playerTotalDamage === 'number'
      ? playerTotalDamage
      : (playerTotalDamageBillions || 0) * 1e9
  );

  // Next milestone calculation
  const nextTier =
    CONTRIBUTION_TIERS.find((t) => currentDamage < t.damageRequired) ||
    CONTRIBUTION_TIERS[CONTRIBUTION_TIERS.length - 1];
  const prevReq =
    CONTRIBUTION_TIERS.slice()
      .reverse()
      .find((t) => currentDamage >= t.damageRequired)?.damageRequired || 0;
  const progressPct = Math.min(
    100,
    Math.max(
      0,
      ((currentDamage - prevReq) / Math.max(1, nextTier.damageRequired - prevReq)) * 100
    )
  );

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const trimmed = inputText.trim();
    if (!trimmed) return;
    onSendChat(trimmed);
    setInputText('');
  };

  return (
    <div
      aria-label="Thế Trận, Phường Rèn và Cửu Trọng Thiên"
      className="flex flex-col gap-3 p-3 sm:p-4 bg-[#111625]/70 h-full overflow-y-auto"
    >
      {/* 3 Segmented Control Tabs */}
      <div
        role="tablist"
        aria-label="Chuyển đổi danh mục Thế Trận"
        className="grid grid-cols-3 gap-1 p-1 bg-[#080A10] border border-slate-800 rounded-xl shrink-0"
      >
        <button
          type="button"
          role="tab"
          aria-selected={activeTab === 'tactical'}
          onClick={() => setActiveTab('tactical')}
          className={`flex items-center justify-center gap-1 py-1.5 px-1 rounded-lg text-xs font-medium transition-colors cursor-pointer whitespace-nowrap ${
            activeTab === 'tactical'
              ? 'bg-amber-400 text-slate-950 font-bold'
              : 'text-slate-300 hover:text-white'
          }`}
          title="Thế Trận & Cống Hiến"
        >
          <Swords className="w-3.5 h-3.5" />
          <span className="truncate">Thế Trận</span>
        </button>

        <button
          type="button"
          role="tab"
          aria-selected={activeTab === 'guild'}
          onClick={() => setActiveTab('guild')}
          className={`flex items-center justify-center gap-1 py-1.5 px-1 rounded-lg text-xs font-medium transition-colors cursor-pointer whitespace-nowrap ${
            activeTab === 'guild'
              ? 'bg-orange-500 text-slate-950 font-bold'
              : 'text-slate-300 hover:text-white'
          }`}
          title="Phường Rèn & Đại Hỏa Lò"
        >
          <Flame className="w-3.5 h-3.5" />
          <span className="truncate">Phường Rèn</span>
        </button>

        <button
          type="button"
          role="tab"
          aria-selected={activeTab === 'vaults'}
          onClick={() => setActiveTab('vaults')}
          className={`flex items-center justify-center gap-1 py-1.5 px-1 rounded-lg text-xs font-medium transition-colors cursor-pointer whitespace-nowrap ${
            activeTab === 'vaults'
              ? 'bg-cyan-400 text-slate-950 font-bold'
              : 'text-slate-300 hover:text-white'
          }`}
          title="Bản Đồ 9 Tầng Trời (Cửu Trọng Thiên)"
        >
          <Layers className="w-3.5 h-3.5" />
          <span className="truncate">Cửu Thiên</span>
        </button>
      </div>

      {/* ================================================================= */}
      {/* TAB 1: THẾ TRẬN & CỐNG HIẾN & CHAT (TACTICAL) */}
      {/* ================================================================= */}
      {activeTab === 'tactical' && (
        <div className="space-y-3">
          {/* 1. Thế Trận Vạn Dân (Tactical Formation & Player Telemetry) */}
          <div className="bg-[#080A10] border border-slate-800/90 rounded-xl p-3.5">
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center gap-2">
                <Swords className="w-4 h-4 text-amber-400" />
                <h3 className="font-display font-bold text-sm text-slate-100 tracking-wide">
                  Thế Trận Vạn Dân
                </h3>
              </div>
              <span className="text-xs font-tech text-cyan-300">
                DPS Server: {serverDps.toLocaleString('en-US')} DMG/s
              </span>
            </div>

            <div className="p-2.5 rounded-lg bg-[#111625] border border-slate-800/80 mb-2.5">
              <div className="text-[11px] text-slate-400 mb-0.5">Thế Búa Đang Vận Dụng</div>
              <div className="flex items-center justify-between">
                <span className="font-semibold text-sm text-amber-300">
                  [{stanceInfo.key}] {stanceInfo.name}
                </span>
                <span className="text-xs font-tech text-slate-300">{stanceInfo.title}</span>
              </div>
              <div className="text-xs text-slate-400 mt-1">{stanceInfo.role}</div>
            </div>

            <div className="grid grid-cols-3 gap-2 font-tech text-center">
              <div className="p-2 rounded-lg bg-[#111625]/80 border border-slate-800/60">
                <div className="text-[10px] text-slate-400">Tổng Công Phá</div>
                <div className="text-xs sm:text-sm font-bold text-amber-300">
                  {currentDamage.toLocaleString('en-US')}
                </div>
              </div>
              <div className="p-2 rounded-lg bg-[#111625]/80 border border-slate-800/60">
                <div className="text-[10px] text-slate-400">Nhịp Hoàng Kim</div>
                <div className="text-xs sm:text-sm font-bold text-cyan-300">{perfectCount}</div>
              </div>
              <div className="p-2 rounded-lg bg-[#111625]/80 border border-slate-800/60">
                <div className="text-[10px] text-slate-400">Đỉnh Combo</div>
                <div className="text-xs sm:text-sm font-bold text-red-400">{maxCombo}</div>
              </div>
            </div>
          </div>

          {/* 2. Cột Mốc Cống Hiến Cá Nhân (Personal Contribution Tiers) */}
          <div className="bg-[#080A10] border border-amber-500/30 rounded-xl p-3.5">
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center gap-1.5 text-amber-300 font-display font-bold text-sm">
                <Award className="w-4 h-4 text-amber-400" />
                <span>Cống Hiến Cá Nhân</span>
              </div>
              <span className="text-[11px] font-tech text-cyan-300">
                {nextTier.badge} {nextTier.title}
              </span>
            </div>

            {/* Progress bar towards next milestone */}
            <div className="mb-2">
              <div className="flex items-center justify-between text-[11px] font-tech text-slate-300 mb-1">
                <span>Đã góp vào Vòm Trời:</span>
                <span className="font-bold text-amber-300">
                  {currentDamage.toLocaleString('en-US')} / {nextTier.damageRequired.toLocaleString('en-US')} DMG
                </span>
              </div>
              <div className="h-2 w-full bg-slate-900 rounded-full overflow-hidden border border-slate-800">
                <div
                  className="h-full bg-gradient-to-r from-amber-500 to-orange-400 transition-all duration-300"
                  style={{ width: `${progressPct}%` }}
                />
              </div>
            </div>

            {/* Milestones list */}
            <div className="space-y-1.5 mt-2.5">
              {CONTRIBUTION_TIERS.map((tier) => {
                const reached = currentDamage >= tier.damageRequired;
                const claimed = claimedMilestones.includes(tier.id);
                return (
                  <div
                    key={tier.id}
                    className={`p-2 rounded-lg border flex items-center justify-between text-xs transition-colors ${
                      reached
                        ? 'bg-amber-500/10 border-amber-500/40 text-slate-100'
                        : 'bg-[#111625]/60 border-slate-800/80 text-slate-400'
                    }`}
                  >
                    <div className="min-w-0 pr-2">
                      <div className="flex items-center gap-1 font-semibold text-amber-200">
                        <span>{tier.badge}</span>
                        <span className="truncate">{tier.title}</span>
                        <span className="text-[10px] text-slate-400 font-tech">
                          ({tier.damageRequired.toLocaleString('en-US')} DMG)
                        </span>
                      </div>
                      <div className="text-[10px] text-slate-400 truncate">{tier.perkDescription}</div>
                    </div>

                    <div className="shrink-0">
                      {claimed ? (
                        <span className="flex items-center gap-0.5 text-[10px] font-tech text-emerald-400">
                          <CheckCircle className="w-3 h-3" /> Đã nhận
                        </span>
                      ) : reached ? (
                        <button
                          type="button"
                          onClick={() => onClaimMilestone?.(tier.id)}
                          className="px-2 py-1 rounded bg-amber-400 hover:bg-amber-300 text-slate-950 font-tech font-bold text-[10px] shadow cursor-pointer transition-all active:scale-95 animate-pulse"
                        >
                          NHẬN QUÀ
                        </button>
                      ) : (
                        <span className="text-[10px] font-tech text-slate-500">Chưa đạt</span>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* 3. Boss Combat Log (Nhật Ký Lò Rèn & Chiến Sự) */}
          <div className="bg-[#080A10] border border-slate-800/90 rounded-xl p-3.5 flex flex-col min-h-[160px] max-h-[190px]">
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center gap-2">
                <ScrollText className="w-4 h-4 text-cyan-400" />
                <h3 className="font-display font-bold text-sm text-slate-100 tracking-wide">
                  Nhật Ký Chiến Trường
                </h3>
              </div>
              <span className="text-[11px] font-tech text-slate-400">Thời gian thực</span>
            </div>

            <div className="flex-1 overflow-y-auto space-y-1.5 pr-1 font-tech text-xs">
              {combatLogs.map((entry) => (
                <div key={entry.id} className="leading-snug flex items-start gap-1.5">
                  <span className="text-slate-500 shrink-0">[{entry.timestamp}]</span>
                  <span
                    className={
                      entry.tone === 'gold'
                        ? 'text-amber-300'
                        : entry.tone === 'cyan'
                        ? 'text-cyan-300'
                        : entry.tone === 'red'
                        ? 'text-red-400'
                        : 'text-slate-300'
                    }
                  >
                    {entry.text}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* 4. Truyền Âm Vạn Dân (Live Multiplayer Chat) */}
          <div className="bg-[#080A10] border border-slate-800/90 rounded-xl p-3.5 flex flex-col min-h-[180px]">
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center gap-2">
                <MessageSquare className="w-4 h-4 text-emerald-400" />
                <h3 className="font-display font-bold text-sm text-slate-100 tracking-wide">
                  Truyền Âm Vạn Dân
                </h3>
              </div>
              <span className="text-[11px] font-tech text-slate-400">Kênh Toàn Server</span>
            </div>

            <div className="flex-1 overflow-y-auto space-y-2 pr-1 font-tech text-xs mb-2 max-h-[140px]">
              {chatMessages.map((msg) => (
                <div
                  key={msg.id}
                  className={`p-2 rounded-lg ${
                    msg.isPlayer
                      ? 'bg-amber-500/10 border border-amber-500/30'
                      : 'bg-[#111625] border border-slate-800/60'
                  }`}
                >
                  <div className="flex items-center justify-between mb-0.5">
                    <span
                      className={`font-semibold ${msg.isPlayer ? 'text-amber-300' : 'text-cyan-300'}`}
                    >
                      {msg.sender}
                    </span>
                    <span className="text-[10px] text-slate-400">{msg.realm}</span>
                  </div>
                  <div className="text-slate-200 leading-relaxed">{msg.content}</div>
                </div>
              ))}
            </div>

            <form onSubmit={handleSubmit} className="flex gap-2 shrink-0">
              <input
                type="text"
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                placeholder="Truyền âm tới toàn thể thợ rèn..."
                maxLength={140}
                className="flex-1 bg-[#111625] border border-slate-800 rounded-lg px-2.5 py-1.5 text-xs text-slate-100 placeholder-slate-500 focus:outline-none focus:border-amber-400/80 font-tech"
              />
              <button
                type="submit"
                className="px-3 py-1.5 rounded-lg bg-amber-400 hover:bg-amber-300 text-slate-950 font-tech font-bold text-xs flex items-center gap-1 cursor-pointer transition-colors"
              >
                <Send className="w-3 h-3" />
                <span>Gửi</span>
              </button>
            </form>
          </div>
        </div>
      )}

      {/* ================================================================= */}
      {/* TAB 2: PHƯỜNG RÈN & ĐẠI HỎA LÒ BANG HỘI (GUILD SYSTEM) */}
      {/* ================================================================= */}
      {activeTab === 'guild' && (
        <div className="space-y-3">
          {/* Current Guild Banner */}
          <div className="p-3.5 rounded-xl bg-gradient-to-br from-[#120d1c] to-[#1c1228] border border-orange-500/30 shadow-lg space-y-2">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <span className="text-2xl">{currentGuild.icon}</span>
                <div>
                  <h4 className="font-tech font-bold text-sm text-orange-300">
                    {currentGuild.name}
                  </h4>
                  <p className="text-[10px] text-slate-400 italic">"{currentGuild.motto}"</p>
                </div>
              </div>
              <span className="text-[10px] font-tech px-2 py-0.5 rounded bg-orange-500/20 text-orange-300 font-bold border border-orange-500/40">
                {currentGuild.memberCount} Thành Viên
              </span>
            </div>

            {/* Guild Aura Perk */}
            <div className="p-2 rounded-lg bg-black/40 border border-orange-500/20 text-xs font-tech text-orange-200">
              ⚡ <b>Hào Quang Phường Rèn:</b> {currentGuild.auraPerk}
            </div>

            {/* Great Hearth Level & Contribution */}
            <div className="pt-2 border-t border-slate-800 space-y-1.5">
              <div className="flex items-center justify-between text-xs font-tech">
                <span className="text-slate-300 font-semibold flex items-center gap-1">
                  <Flame className="w-3.5 h-3.5 text-orange-400" />
                  Đại Hỏa Lò Phường: Cấp {hearthState.level}/10
                </span>
                <span className="text-amber-300 font-bold">
                  {hearthState.exp} / {expNeeded} LT ({hearthProgressPct.toFixed(0)}%)
                </span>
              </div>
              <div className="h-2 w-full bg-slate-900 rounded-full overflow-hidden border border-slate-800">
                <div
                  className="h-full bg-gradient-to-r from-orange-500 to-amber-400 transition-all duration-300 shadow-sm shadow-orange-500/50"
                  style={{ width: `${hearthProgressPct}%` }}
                />
              </div>

              {/* Donate Buttons */}
              <div className="flex items-center justify-between pt-1 gap-2">
                <div className="text-[10px] font-tech text-slate-400">
                  Linh Thạch có: <b className="text-cyan-300">{linhThach.toLocaleString('en-US')}</b>
                </div>
                <div className="flex gap-1.5">
                  <button
                    type="button"
                    disabled={linhThach < 50}
                    onClick={() => onDonateHearth?.(userGuildId, 50)}
                    className={`px-2 py-1 rounded-lg text-[10px] font-tech font-bold transition-all ${
                      linhThach >= 50
                        ? 'bg-orange-500 hover:bg-orange-400 text-slate-950 cursor-pointer shadow-sm active:scale-95'
                        : 'bg-slate-800 text-slate-500 cursor-not-allowed'
                    }`}
                  >
                    Góp +50 LT
                  </button>
                  <button
                    type="button"
                    disabled={linhThach < 200}
                    onClick={() => onDonateHearth?.(userGuildId, 200)}
                    className={`px-2 py-1 rounded-lg text-[10px] font-tech font-bold transition-all ${
                      linhThach >= 200
                        ? 'bg-amber-400 hover:bg-amber-300 text-slate-950 cursor-pointer shadow-sm active:scale-95'
                        : 'bg-slate-800 text-slate-500 cursor-not-allowed'
                    }`}
                  >
                    Góp +200 LT
                  </button>
                </div>
              </div>
            </div>
          </div>

          {/* Vũ Điệu Khai Thiên: Tam Điểm Lôi Hỏa Card */}
          <div className="p-3 rounded-xl bg-[#080A10] border border-cyan-500/30 space-y-1.5">
            <div className="flex items-center gap-1.5 text-cyan-300 font-tech font-bold text-xs">
              <Zap className="w-4 h-4 text-cyan-400 animate-pulse" />
              <span>VŨ ĐIỆU KHAI THIÊN: TAM ĐIỂM LÔI HỎA</span>
            </div>
            <p className="text-[11px] text-slate-300 leading-relaxed font-sans">
              Khi bạn duy trì chuỗi <b>Perfect Combo ≥ 6</b> trong thế búa Phường Rèn, 3 luồng năng lượng từ đồng môn sẽ cùng hợp nhất giáng <b>Tam Điểm Lôi Hỏa (-1,500 DMG)</b> xuyên thủng lớp mây đen!
            </p>
          </div>

          {/* 4 Blacksmith Guilds List */}
          <div className="space-y-2">
            <div className="text-xs font-tech text-slate-400 font-semibold px-1">
              4 ĐẠI PHƯỜNG RÈN BÁ CHỦ:
            </div>

            {BLACKSMITH_GUILDS.map((g) => {
              const isSelected = g.id === userGuildId;
              return (
                <div
                  key={g.id}
                  className={`p-3 rounded-xl border transition-all ${
                    isSelected
                      ? 'bg-orange-950/20 border-orange-500/60 ring-1 ring-orange-500/40'
                      : 'bg-[#080A10] border-slate-800 hover:border-slate-700'
                  }`}
                >
                  <div className="flex items-start justify-between gap-2 mb-1.5">
                    <div className="flex items-center gap-2">
                      <span className="text-xl">{g.icon}</span>
                      <div>
                        <div className="flex items-center gap-1.5">
                          <h5 className="font-tech font-bold text-xs text-slate-100">{g.name}</h5>
                          <span className="text-[9px] font-tech px-1 rounded bg-slate-800 text-slate-300">
                            Thế [{g.preferredStance}]
                          </span>
                        </div>
                        <p className="text-[10px] text-slate-400 italic">"{g.motto}"</p>
                      </div>
                    </div>

                    <span className="text-[10px] font-tech text-slate-400 whitespace-nowrap">
                      {g.memberCount} Thợ
                    </span>
                  </div>

                  <p className="text-[11px] text-slate-300 mb-2 font-tech">
                    ⚡ {g.auraPerk}
                  </p>

                  <div className="flex justify-end pt-2 border-t border-slate-800/80">
                    {isSelected ? (
                      <span className="text-xs font-tech font-bold text-orange-400 flex items-center gap-1">
                        <CheckCircle className="w-3.5 h-3.5" /> ĐANG THAM GIA
                      </span>
                    ) : (
                      <button
                        type="button"
                        onClick={() => onSelectGuild?.(g.id)}
                        className="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-orange-500 text-slate-300 hover:text-slate-950 font-tech font-bold text-xs transition-colors cursor-pointer"
                      >
                        Gia Nhập Phường
                      </button>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* ================================================================= */}
      {/* TAB 3: CỬU TRỌNG THIÊN (THE 9 CELESTIAL VAULTS MAP) */}
      {/* ================================================================= */}
      {activeTab === 'vaults' && (
        <div className="space-y-3">
          {/* Active Vault Card Header */}
          <div className="p-3.5 rounded-xl bg-gradient-to-br from-[#0c1424] to-[#121c32] border border-cyan-500/40 shadow-xl space-y-1.5">
            <div className="flex items-center justify-between">
              <span className="text-[10px] font-tech px-2 py-0.5 rounded bg-cyan-500/20 text-cyan-300 font-bold border border-cyan-500/30">
                ĐANG CÔNG PHÁ: TẦNG {currentVault.id}/9
              </span>
              <span className="text-xs font-tech text-amber-300 font-bold">
                {formatInteger(currentVault.maxHp)} HP
              </span>
            </div>
            <h4 className="font-tech font-bold text-sm text-cyan-300">
              {currentVault.name} · {currentVault.title}
            </h4>
            <div className="text-xs font-tech text-slate-200">
              Trùm: <b className="text-amber-300">{currentVault.bossName}</b> ({currentVault.bossTitle})
            </div>
            <p className="text-[11px] text-slate-400 italic font-sans leading-relaxed pt-1 border-t border-slate-800">
              "{currentVault.loreSummary}"
            </p>
          </div>

          <div className="text-xs font-tech text-slate-400 font-semibold px-1">
            BẢN ĐỒ CỬU TRỌNG THIÊN CẤM:
          </div>

          {/* 9 Vaults List */}
          <div className="space-y-2">
            {CELESTIAL_VAULTS.map((vault) => {
              const isCurrent = vault.id === currentVaultId;

              return (
                <div
                  key={vault.id}
                  className={`p-3 rounded-xl border transition-all ${
                    isCurrent
                      ? 'bg-cyan-950/25 border-cyan-500/60 ring-1 ring-cyan-500/40'
                      : 'bg-[#080A10] border-slate-800 hover:border-slate-700'
                  }`}
                >
                  <div className="flex items-start justify-between gap-2 mb-1">
                    <div>
                      <div className="flex items-center gap-1.5">
                        <span className="text-[10px] font-tech px-1.5 py-0.5 rounded bg-slate-800 text-slate-300 font-bold">
                          TẦNG {vault.id}
                        </span>
                        <h5 className="font-tech font-bold text-xs text-slate-100">
                          {vault.name}
                        </h5>
                      </div>
                      <p className="text-[10px] text-cyan-300 font-tech mt-0.5">{vault.title}</p>
                    </div>

                    <div className="text-right shrink-0">
                      <div className="text-xs font-tech font-bold text-amber-300">
                        {formatInteger(vault.maxHp)} HP
                      </div>
                      <div className="text-[9px] font-tech text-rose-400">
                        Giáp: -{vault.damageReductionPct}% DMG
                      </div>
                    </div>
                  </div>

                  <div className="text-[11px] font-tech text-slate-300 mb-2">
                    Boss: <b className="text-amber-200">{vault.bossName}</b>
                    <span className="text-slate-400 text-[10px] block truncate">{vault.bossTitle}</span>
                  </div>

                  <p className="text-[10px] text-slate-400 italic mb-2 line-clamp-2">
                    {vault.loreSummary}
                  </p>

                  <div className="flex justify-end pt-2 border-t border-slate-800/80">
                    {isCurrent ? (
                      <span className="text-xs font-tech font-bold text-cyan-300 flex items-center gap-1">
                        <CheckCircle className="w-3.5 h-3.5 text-cyan-400" /> ĐANG CÔNG PHÁ
                      </span>
                    ) : (
                      <button
                        type="button"
                        onClick={() => onSelectVault?.(vault.id)}
                        className="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-cyan-400 text-slate-300 hover:text-slate-950 font-tech font-bold text-xs transition-colors cursor-pointer"
                      >
                        Chuyển Sang Tầng Này
                      </button>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
};
