import React, { useState } from 'react';
import { Send, Swords, ScrollText, MessageSquare, Award, CheckCircle } from 'lucide-react';
import { HAMMER_STANCES, StanceKey, CONTRIBUTION_TIERS, ContributionTier } from '../game/rules';

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
  playerTotalDamage: number; // Integer DMG (e.g. 4,210)
  playerTotalDamageBillions?: number; // legacy fallback
  perfectCount: number;
  maxCombo: number;
  serverDps?: number; // Integer DMG/s (e.g. 2,000)
  serverDpsBillions?: number; // legacy fallback
  claimedMilestones?: string[];
  onClaimMilestone?: (tierId: string) => void;
  combatLogs: CombatLogEntry[];
  chatMessages: ChatMessage[];
  onSendChat: (msg: string) => void;
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
}) => {
  const [inputText, setInputText] = useState('');
  const stanceInfo = HAMMER_STANCES[activeStance];

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
    <aside
      aria-label="Thế Trận, Cống Hiến và Truyền Âm"
      className="hidden lg:flex lg:w-[320px] xl:w-[360px] flex-col gap-3 p-4 bg-[#111625]/70 border-r border-slate-800/90 shrink-0 overflow-y-auto"
    >
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
      <div className="bg-[#080A10] border border-slate-800/90 rounded-xl p-3.5 flex flex-col flex-1 min-h-[180px]">
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center gap-2">
            <MessageSquare className="w-4 h-4 text-emerald-400" />
            <h3 className="font-display font-bold text-sm text-slate-100 tracking-wide">
              Truyền Âm Vạn Dân
            </h3>
          </div>
          <span className="text-[11px] font-tech text-slate-400">Kênh Toàn Server</span>
        </div>

        <div className="flex-1 overflow-y-auto space-y-2 pr-1 font-tech text-xs mb-2">
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
    </aside>
  );
};