import React, { useState } from 'react';
import { Send, Swords, ScrollText, MessageSquare } from 'lucide-react';
import { HAMMER_STANCES, StanceKey } from '../game/rules';

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
  playerTotalDamageBillions: number;
  perfectCount: number;
  maxCombo: number;
  serverDpsBillions: number;
  combatLogs: CombatLogEntry[];
  chatMessages: ChatMessage[];
  onSendChat: (msg: string) => void;
}

export const LeftTacticalPanel: React.FC<LeftTacticalPanelProps> = ({
  activeStance,
  playerTotalDamageBillions,
  perfectCount,
  maxCombo,
  serverDpsBillions,
  combatLogs,
  chatMessages,
  onSendChat,
}) => {
  const [inputText, setInputText] = useState('');
  const stanceInfo = HAMMER_STANCES[activeStance];

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const trimmed = inputText.trim();
    if (!trimmed) return;
    onSendChat(trimmed);
    setInputText('');
  };

  return (
    <aside
      aria-label="Thế Trận, Nhật Ký Chiến Trường và Truyền Âm"
      className="hidden lg:flex lg:w-[320px] xl:w-[350px] flex-col gap-3 p-4 bg-[#111625]/70 border-r border-slate-800/90 shrink-0 overflow-y-auto"
    >
      {/* 1. Thế Trận Vạn Dân (Tactical Formation & Player Telemetry) */}
      <div className="bg-[#080A10] border border-slate-800/90 rounded-xl p-3.5">
        <div className="flex items-center justify-between mb-2.5">
          <div className="flex items-center gap-2">
            <Swords className="w-4 h-4 text-amber-400" />
            <h3 className="font-display font-bold text-sm text-slate-100 tracking-wide">
              Thế Trận Vạn Dân
            </h3>
          </div>
          <span className="text-xs font-tech text-cyan-300">
            DPS Server: {serverDpsBillions.toFixed(2)}B/s
          </span>
        </div>

        <div className="p-2.5 rounded-lg bg-[#111625] border border-slate-800/80 mb-3">
          <div className="text-xs text-slate-400 mb-0.5">Thế Búa Đang Vận Dụng</div>
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
            <div className="text-[11px] text-slate-400">Tổng Công Phá</div>
            <div className="text-sm font-bold text-amber-300">
              {playerTotalDamageBillions.toFixed(2)}B
            </div>
          </div>
          <div className="p-2 rounded-lg bg-[#111625]/80 border border-slate-800/60">
            <div className="text-[11px] text-slate-400">Nhịp Hoàng Kim</div>
            <div className="text-sm font-bold text-cyan-300">{perfectCount}</div>
          </div>
          <div className="p-2 rounded-lg bg-[#111625]/80 border border-slate-800/60">
            <div className="text-[11px] text-slate-400">Đỉnh Combo</div>
            <div className="text-sm font-bold text-red-400">{maxCombo}</div>
          </div>
        </div>
      </div>

      {/* 2. Boss Combat Log (Nhật Ký Lò Rèn & Chiến Sự) */}
      <div className="bg-[#080A10] border border-slate-800/90 rounded-xl p-3.5 flex flex-col min-h-[175px] max-h-[210px]">
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

      {/* 3. Mini-Chat Vạn Dân (Interactive Server Coordination Chat) */}
      <div className="flex-1 bg-[#080A10] border border-slate-800/90 rounded-xl p-3.5 flex flex-col min-h-[220px]">
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center gap-2">
            <MessageSquare className="w-4 h-4 text-amber-400" />
            <h3 className="font-display font-bold text-sm text-slate-100 tracking-wide">
              Truyền Âm Vạn Dân
            </h3>
          </div>
          <span className="text-[11px] font-tech text-slate-400">Kênh Cửu Trọng</span>
        </div>

        {/* Chat Feed */}
        <div className="flex-1 overflow-y-auto space-y-2 pr-1 mb-2.5 text-xs">
          {chatMessages.map((msg) => (
            <div key={msg.id} className="leading-relaxed">
              <span
                className={`font-semibold ${
                  msg.isPlayer ? 'text-amber-300' : 'text-cyan-300'
                }`}
              >
                {msg.sender}
              </span>
              <span className="text-slate-500 mx-1">·</span>
              <span className="text-[11px] font-tech text-slate-400">{msg.realm}: </span>
              <span className="text-slate-200">{msg.content}</span>
            </div>
          ))}
        </div>

        {/* Quick Tactical Callout Buttons */}
        <div className="flex items-center gap-1.5 mb-2 overflow-x-auto pb-0.5">
          <button
            type="button"
            onClick={() => onSendChat('Anh em đổi Phá Giáp Chùy [E] đập vỡ khiên Boss!')}
            className="px-2 py-1 rounded bg-[#111625] hover:bg-slate-800 border border-slate-800 text-[11px] text-slate-300 whitespace-nowrap shrink-0 cursor-pointer"
          >
            Hô hào Phá Giáp [E]
          </button>
          <button
            type="button"
            onClick={() => onSendChat('Giữ nhịp Hoàng Kim tích 8/8 Overdrive nào!')}
            className="px-2 py-1 rounded bg-[#111625] hover:bg-slate-800 border border-slate-800 text-[11px] text-slate-300 whitespace-nowrap shrink-0 cursor-pointer"
          >
            Giữ chuỗi 8/8
          </button>
        </div>

        {/* Chat Input Form */}
        <form onSubmit={handleSubmit} className="flex items-center gap-1.5">
          <label htmlFor="chat-input" className="sr-only">
            Nhập truyền âm vạn dân
          </label>
          <input
            id="chat-input"
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Truyền âm hiệu lệnh..."
            className="flex-1 bg-[#111625] border border-slate-800 rounded-lg px-2.5 py-1.5 text-xs text-slate-100 placeholder:text-slate-500 focus:outline-none focus:border-amber-400"
          />
          <button
            type="submit"
            aria-label="Gửi truyền âm"
            className="p-2 rounded-lg bg-amber-400 hover:bg-amber-300 text-slate-950 transition-colors cursor-pointer shrink-0"
          >
            <Send className="w-3.5 h-3.5" />
          </button>
        </form>
      </div>
    </aside>
  );
};
