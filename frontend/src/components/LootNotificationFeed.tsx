import React, { useEffect, useState } from 'react';
import {
  EquipmentItem,
  EquipmentSlotKey,
  getItemRarityMeta,
  RuneGem,
} from '../game/rules';
import { X, ChevronRight, Gem, Sparkles } from 'lucide-react';

export interface LootToastItem {
  id: string;
  type: 'drop' | 'salvage' | 'full' | 'gem' | 'tinhHoa';
  item?: EquipmentItem;
  gem?: RuneGem;
  dustAmount?: number;
  tinhHoaAmount?: number;
  salvageYield?: { ironDust: number; linhThach: number; tinhHoa?: number };
  timestamp: number;
}

interface LootNotificationFeedProps {
  notifications: LootToastItem[];
  onDismiss: (id: string) => void;
  onOpenInventory: () => void;
}

const ITEM_ART_URLS: Record<EquipmentSlotKey, string> = {
  hammer: '/assets/art/items/item_hammer.webp',
  anvil: '/assets/art/items/item_anvil.webp',
  bellows: '/assets/art/items/item_bellows.webp',
  gauntlets: '/assets/art/items/item_gauntlets.webp',
  apron: '/assets/art/items/item_apron.webp',
  relic: '/assets/art/items/item_relic.webp',
};

export const LootNotificationFeed: React.FC<LootNotificationFeedProps> = ({
  notifications,
  onDismiss,
  onOpenInventory,
}) => {
  return (
    <div
      className="fixed bottom-24 right-3 sm:right-6 z-40 flex flex-col-reverse gap-2.5 pointer-events-none max-w-[320px] sm:max-w-[360px] w-full select-none"
      aria-live="polite"
    >
      {notifications.map((toast) => (
        <LootToastCard
          key={toast.id}
          toast={toast}
          onDismiss={() => onDismiss(toast.id)}
          onOpenInventory={onOpenInventory}
        />
      ))}
    </div>
  );
};

const LootToastCard: React.FC<{
  toast: LootToastItem;
  onDismiss: () => void;
  onOpenInventory: () => void;
}> = ({ toast, onDismiss, onOpenInventory }) => {
  const [progress, setProgress] = useState(100);
  const DURATION_MS = 4600;

  useEffect(() => {
    const startTime = performance.now();
    const timer = setInterval(() => {
      const elapsed = performance.now() - startTime;
      const remaining = Math.max(0, 100 - (elapsed / DURATION_MS) * 100);
      setProgress(remaining);
      if (remaining <= 0) {
        clearInterval(timer);
        onDismiss();
      }
    }, 50);

    return () => clearInterval(timer);
  }, [onDismiss]);

  const { item, type, gem, salvageYield } = toast;

  // Handle Rune Gem toast
  if (type === 'gem' && gem) {
    return (
      <div
        onClick={onOpenInventory}
        className="pointer-events-auto relative overflow-hidden rounded-2xl bg-gradient-to-r from-slate-950/98 via-[#0A1020]/95 to-slate-950/98 border border-cyan-500/50 backdrop-blur-xl shadow-2xl transition-all duration-300 hover:scale-[1.02] cursor-pointer group animate-in slide-in-from-right-8 duration-300 shadow-cyan-950/50"
      >
        <div className="absolute top-0 left-0 w-3 h-3 border-t-2 border-l-2 border-cyan-400 pointer-events-none" />
        <div className="absolute top-0 right-0 w-3 h-3 border-t-2 border-r-2 border-cyan-400 pointer-events-none" />
        <div className="absolute bottom-0 left-0 w-3 h-3 border-b-2 border-l-2 border-cyan-400 pointer-events-none" />
        <div className="absolute bottom-0 right-0 w-3 h-3 border-b-2 border-r-2 border-cyan-400 pointer-events-none" />

        <div
          className="absolute -top-12 -right-12 w-28 h-28 rounded-full blur-2xl opacity-30 pointer-events-none"
          style={{ backgroundColor: gem.color }}
        />

        <div className="p-2.5 sm:p-3 flex items-start gap-3">
          <div
            className="relative w-12 h-12 rounded-xl flex items-center justify-center border shrink-0 bg-slate-950/90 overflow-hidden shadow-inner"
            style={{ borderColor: gem.color, boxShadow: `0 0 14px ${gem.color}55` }}
          >
            <Gem className="w-6 h-6 animate-pulse" style={{ color: gem.color }} />
            <span className="absolute -bottom-0.5 -right-0.5 text-[8.5px] font-mono font-black px-1 rounded bg-black/95 border border-slate-700 text-cyan-200">
              {gem.tier.substring(0, 1).toUpperCase()}
            </span>
          </div>

          <div className="flex-1 min-w-0 pr-5">
            <div className="flex items-center gap-1.5 mb-0.5">
              <span
                className="text-[10px] font-tech font-bold uppercase tracking-wider px-1.5 py-0.5 rounded bg-cyan-950/90 border border-cyan-500/50 text-cyan-300"
              >
                💎 PHÙ THẠCH HIẾM
              </span>
              <span className="text-[10px] text-slate-400 font-tech uppercase">
                {gem.type}
              </span>
            </div>

            <h4
              className="text-xs sm:text-[13px] font-bold truncate tracking-wide text-cyan-200"
              title={gem.name}
            >
              {gem.name}
            </h4>

            <div className="flex items-center justify-between mt-0.5">
              <span className="text-[11px] text-slate-300 font-tech truncate">
                +{gem.value} {gem.statLabel}
              </span>
              <span className="text-[10px] text-amber-400 group-hover:translate-x-0.5 transition-transform flex items-center font-tech ml-2 shrink-0 font-bold">
                Mở Túi Khảm <ChevronRight className="w-3 h-3" />
              </span>
            </div>
          </div>

          <button
            type="button"
            onClick={(e) => {
              e.stopPropagation();
              onDismiss();
            }}
            className="absolute top-2 right-2 p-1 text-slate-500 hover:text-slate-200 rounded-lg hover:bg-slate-800/80 transition-colors"
            aria-label="Đóng"
          >
            <X className="w-3.5 h-3.5" />
          </button>
        </div>

        <div className="h-0.5 w-full bg-slate-800/80">
          <div
            className="h-full transition-all ease-linear"
            style={{
              width: `${progress}%`,
              backgroundColor: gem.color,
              boxShadow: `0 0 6px ${gem.color}`,
            }}
          />
        </div>
      </div>
    );
  }

  // Handle Tinh Hoa toast
  if (type === 'tinhHoa') {
    return (
      <div
        className="pointer-events-auto relative overflow-hidden rounded-2xl bg-gradient-to-r from-slate-950/98 via-[#150A20]/95 to-slate-950/98 border border-purple-500/50 backdrop-blur-xl shadow-2xl p-2.5 sm:p-3 flex items-center gap-3 animate-in slide-in-from-right-8 duration-300"
      >
        <div className="w-10 h-10 rounded-xl bg-purple-950/80 border border-purple-500/60 flex items-center justify-center shrink-0">
          <Sparkles className="w-5 h-5 text-purple-300 animate-spin" style={{ animationDuration: '6s' }} />
        </div>
        <div className="flex-1 min-w-0 pr-4">
          <span className="text-[10px] font-tech font-bold uppercase tracking-wider px-1.5 py-0.5 rounded bg-purple-950 border border-purple-500 text-purple-300">
            ✨ CỰC PHẨM
          </span>
          <div className="text-xs font-bold text-purple-200 mt-0.5">
            Thu Được +{toast.tinhHoaAmount || 1} Tinh Hoa Thần Hồn!
          </div>
        </div>
        <button
          type="button"
          onClick={onDismiss}
          className="text-slate-500 hover:text-slate-200 p-1"
        >
          <X className="w-3.5 h-3.5" />
        </button>
      </div>
    );
  }

  // Handle Equipment/Full toast fallback
  const meta = item ? getItemRarityMeta(item.rarity) : getItemRarityMeta('common');
  const itemArtSrc = item ? (ITEM_ART_URLS[item.slotKey] || '/assets/art/items/item_relic.webp') : '/assets/art/items/item_hammer.webp';
  const isLegendaryOrMythic = meta.tier === 'S' || meta.tier === 'A';

  return (
    <div
      onClick={onOpenInventory}
      className={`pointer-events-auto relative overflow-hidden rounded-2xl bg-gradient-to-r from-slate-950/98 via-[#0B0F19]/95 to-slate-950/98 border backdrop-blur-xl shadow-2xl transition-all duration-300 hover:scale-[1.02] cursor-pointer group animate-in slide-in-from-right-8 duration-300 ${
        isLegendaryOrMythic
          ? `${meta.borderColor} ${meta.glow} ring-1 ring-amber-400/40`
          : `${meta.borderColor} shadow-black/80`
      }`}
    >
      <div className="absolute top-0 left-0 w-3 h-3 border-t-2 border-l-2 border-amber-400/40 pointer-events-none" />
      <div className="absolute top-0 right-0 w-3 h-3 border-t-2 border-r-2 border-amber-400/40 pointer-events-none" />
      <div className="absolute bottom-0 left-0 w-3 h-3 border-b-2 border-l-2 border-amber-400/40 pointer-events-none" />
      <div className="absolute bottom-0 right-0 w-3 h-3 border-b-2 border-r-2 border-amber-400/40 pointer-events-none" />

      <div
        className="absolute -top-12 -right-12 w-28 h-28 rounded-full blur-2xl opacity-25 pointer-events-none"
        style={{ backgroundColor: meta.hex }}
      />

      <div className="p-2.5 sm:p-3 flex items-start gap-3">
        <div
          className={`relative w-12 h-12 rounded-xl flex items-center justify-center border shrink-0 bg-slate-950/90 overflow-hidden shadow-inner ${meta.borderColor}`}
          style={{
            boxShadow: `0 0 12px ${meta.hex}33`,
          }}
        >
          <img
            src={itemArtSrc}
            alt={item?.name || 'Vũ Khí'}
            className="w-11 h-11 object-contain drop-shadow-[0_2px_8px_rgba(0,0,0,0.85)] transition-transform group-hover:scale-110 duration-300"
            loading="lazy"
          />
          <span
            className="absolute -bottom-0.5 -right-0.5 text-[9px] font-mono font-black px-1.5 py-0.2 rounded bg-black/95 border border-slate-700 text-slate-100 shadow-sm"
          >
            {meta.tier}
          </span>
        </div>

        <div className="flex-1 min-w-0 pr-5">
          <div className="flex items-center gap-1.5 mb-0.5">
            <span
              className={`text-[10px] font-tech font-bold uppercase tracking-wider px-1.5 py-0.5 rounded ${meta.badgeBg}`}
            >
              {type === 'salvage' ? '⚡ TỰ NUNG' : type === 'full' ? '⚠️ RƯƠNG ĐẦY' : `TIER ${meta.tier}`}
            </span>
            <span className="text-[10px] text-slate-400 font-tech">
              {item?.slotName || 'Khí Giới'}
            </span>
          </div>

          <h4
            className={`text-xs sm:text-[13px] font-bold truncate tracking-wide ${meta.textColor}`}
            title={item?.name}
          >
            {item?.name}
          </h4>

          {type === 'salvage' && salvageYield ? (
            <p className="text-[11px] text-cyan-300 font-tech flex items-center gap-1.5 mt-0.5">
              <span>+{salvageYield.ironDust} Bụi Thiết</span>
              <span>•</span>
              <span>+{salvageYield.linhThach} LT</span>
              {salvageYield.tinhHoa && salvageYield.tinhHoa > 0 ? (
                <>
                  <span>•</span>
                  <span className="text-amber-300">+{salvageYield.tinhHoa} TH</span>
                </>
              ) : null}
            </p>
          ) : type === 'full' ? (
            <div className="flex items-center justify-between mt-0.5">
              <span className="text-[11px] text-amber-300 font-tech">
                Rương đã đầy! Mở túi phân giải.
              </span>
              <span className="text-[10px] text-amber-400 group-hover:translate-x-0.5 transition-transform flex items-center font-tech ml-1 shrink-0 font-bold">
                Mở Túi <ChevronRight className="w-3 h-3" />
              </span>
            </div>
          ) : (
            <div className="flex items-center justify-between mt-0.5">
              <span className="text-[11px] text-slate-300 font-tech truncate">
                +{item?.baseStatValue} {item?.baseStatUnit}
              </span>
              <span className="text-[10px] text-amber-400 group-hover:translate-x-0.5 transition-transform flex items-center font-tech ml-2 shrink-0">
                Túi đồ <ChevronRight className="w-3 h-3" />
              </span>
            </div>
          )}
        </div>

        <button
          type="button"
          onClick={(e) => {
            e.stopPropagation();
            onDismiss();
          }}
          className="absolute top-2 right-2 p-1 text-slate-500 hover:text-slate-200 rounded-lg hover:bg-slate-800/80 transition-colors"
          aria-label="Đóng"
        >
          <X className="w-3.5 h-3.5" />
        </button>
      </div>

      <div className="h-0.5 w-full bg-slate-800/80">
        <div
          className="h-full transition-all ease-linear"
          style={{
            width: `${progress}%`,
            backgroundColor: meta.hex,
            boxShadow: `0 0 6px ${meta.hex}`,
          }}
        />
      </div>
    </div>
  );
};
