import React, { useEffect, useRef } from 'react';
import {
  FORGE_BPM,
  HAMMER_STANCES,
  JudgmentGrade,
  OVERDRIVE_MAX,
  StanceKey,
} from '../game/rules';
import { Flame, Sparkles, Zap, Shield, ChevronUp } from 'lucide-react';
import { CelestialAnvil3D, CelestialAnvil3DHandle } from './CelestialAnvil3D';

export interface FloatingFeedback {
  id: number;
  grade: JudgmentGrade;
  labelVn: string;
  multiplier: number;
  damageBillions: number;
  stance: StanceKey;
  overdrive: boolean;
}

interface RadialForgeCenterProps {
  waveProgressRef: React.MutableRefObject<number>;
  activeStance: StanceKey;
  combo: number;
  overdriveCharge: number;
  overdriveActive: boolean;
  overdriveTimeLeft: number;
  globalBurstActive: boolean;
  lastFeedback: FloatingFeedback | null;
  shakeClass: string;
  linhThach: number;
  tinhHoa: number;
  basePowerBillions: number;
  onStrike: () => void;
  onSelectStance: (stance: StanceKey) => void;
  onOpenMobileDrawer: () => void;
}

interface PoolParticle {
  active: boolean;
  x: number;
  y: number;
  vx: number;
  vy: number;
  size: number;
  alpha: number;
  life: number;
  maxLife: number;
  color: string;
}

const POOL_SIZE = 120;

export const RadialForgeCenter: React.FC<RadialForgeCenterProps> = ({
  waveProgressRef,
  activeStance,
  combo,
  overdriveCharge,
  overdriveActive,
  overdriveTimeLeft,
  globalBurstActive,
  lastFeedback,
  shakeClass,
  linhThach,
  tinhHoa,
  basePowerBillions,
  onStrike,
  onSelectStance,
  onOpenMobileDrawer,
}) => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const particlePoolRef = useRef<PoolParticle[]>([]);
  const anvil3DRef = useRef<CelestialAnvil3DHandle | null>(null);

  // Ambient 2D perimeter ghost sparks canvas (Bão Lửa Vạn Dân outer frame)
  useEffect(() => {
    const pool: PoolParticle[] = Array.from({ length: POOL_SIZE }, () => ({
      active: false,
      x: 0,
      y: 0,
      vx: 0,
      vy: 0,
      size: 2,
      alpha: 0,
      life: 0,
      maxLife: 1,
      color: '#FFD23F',
    }));
    particlePoolRef.current = pool;

    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const updateSize = () => {
      if (!canvas.parentElement) return;
      const rect = canvas.parentElement.getBoundingClientRect();
      canvas.width = Math.max(300, Math.floor(rect.width));
      canvas.height = Math.max(300, Math.floor(rect.height));
    };
    updateSize();

    const ro = new ResizeObserver(updateSize);
    if (canvas.parentElement) {
      ro.observe(canvas.parentElement);
    }

    let lastTime = performance.now();
    let rafId = 0;

    const spawnGhostSpark = (w: number, h: number) => {
      for (let i = 0; i < pool.length; i++) {
        const p = pool[i];
        if (!p.active) {
          const cx = w / 2;
          const cy = h / 2;
          const angle = Math.random() * Math.PI * 2;
          const spawnRadius = Math.max(w, h) * 0.54;
          const startX = cx + Math.cos(angle) * spawnRadius;
          const startY = cy + Math.sin(angle) * spawnRadius;
          const speed = 110 + Math.random() * 130;
          p.active = true;
          p.x = startX;
          p.y = startY;
          p.vx = ((cx - startX) / spawnRadius) * speed;
          p.vy = ((cy - startY) / spawnRadius) * speed;
          p.size = 1.5 + Math.random() * 2.0;
          p.life = 0;
          p.maxLife = spawnRadius / speed;
          p.alpha = 0.4 + Math.random() * 0.35;
          const rand = Math.random();
          p.color = rand > 0.6 ? '#FFD23F' : rand > 0.25 ? '#00F0FF' : '#FF3B30';
          break;
        }
      }
    };

    const tick = (now: number) => {
      const dt = Math.min((now - lastTime) / 1000, 0.05);
      lastTime = now;

      const w = canvas.width;
      const h = canvas.height;
      ctx.clearRect(0, 0, w, h);

      spawnGhostSpark(w, h);

      for (let i = 0; i < pool.length; i++) {
        const p = pool[i];
        if (!p.active) continue;
        p.life += dt;
        if (p.life >= p.maxLife) {
          p.active = false;
          continue;
        }
        p.x += p.vx * dt;
        p.y += p.vy * dt;

        const lifeRatio = 1 - p.life / p.maxLife;
        ctx.save();
        ctx.globalAlpha = p.alpha * lifeRatio;
        ctx.strokeStyle = p.color;
        ctx.lineWidth = p.size;
        ctx.beginPath();
        ctx.moveTo(p.x, p.y);
        ctx.lineTo(p.x - p.vx * 0.025, p.y - p.vy * 0.025);
        ctx.stroke();
        ctx.restore();
      }

      rafId = requestAnimationFrame(tick);
    };

    rafId = requestAnimationFrame(tick);
    return () => {
      cancelAnimationFrame(rafId);
      ro.disconnect();
    };
  }, []);

  const stanceKeys: StanceKey[] = ['Q', 'W', 'E', 'R'];

  return (
    <main
      aria-label="Lò Rèn Trung Tâm 3D và Vòng Tròn Nhịp Điệu"
      className={`relative flex-1 flex flex-col items-center justify-between p-3 md:p-4 overflow-hidden select-none bg-[#080A10] ${shakeClass}`}
    >
      {/* Background Particle Ghost Sparks Canvas (Bão Lửa Vạn Dân) */}
      <canvas
        ref={canvasRef}
        data-testid="ghost-sparks-canvas"
        className="absolute inset-0 w-full h-full pointer-events-none z-0"
      />

      {/* Top Center HUD Strip: Player Currency, Base Forge Power, BPM & Combo Counter */}
      <div className="relative z-10 w-full flex flex-wrap items-center justify-between gap-2 px-3 py-1.5 bg-[#111625] border border-slate-800/90 rounded-xl">
        <div className="flex items-center gap-3 font-tech text-xs md:text-sm">
          <div>
            <span className="text-slate-400">Công Lực: </span>
            <span className="text-amber-300 font-bold">{basePowerBillions.toFixed(2)}B</span>
          </div>
          <span className="text-slate-600">·</span>
          <div>
            <span className="text-slate-400">Linh Thạch: </span>
            <span className="text-cyan-300 font-bold">{linhThach.toLocaleString('en-US')}</span>
          </div>
          <span className="text-slate-600">·</span>
          <div>
            <span className="text-slate-400">Tinh Hoa: </span>
            <span className="text-amber-400 font-bold">{tinhHoa}</span>
          </div>
        </div>

        <div className="flex items-center gap-3 font-tech">
          <span className="text-xs text-cyan-300">Nhịp Lò: {FORGE_BPM} BPM</span>
          <span className="text-slate-600">·</span>
          <span className="text-base md:text-lg font-extrabold text-amber-300">
            {combo} COMBO
          </span>
        </div>
      </div>

      {/* Central Three.js 3D Mythic Anvil + Custom GLSL Shader Radial Rhythm Ring */}
      <div className="relative z-10 my-auto flex flex-col items-center justify-center w-full max-w-[500px]">
        {/* Floating Judgment & Damage Callout */}
        <div className="h-11 flex flex-col items-center justify-center pointer-events-none mb-1">
          {lastFeedback ? (
            <div
              key={lastFeedback.id}
              className="flex flex-col items-center transition-transform duration-150 scale-105"
            >
              <div
                className={`font-display font-extrabold text-sm md:text-base tracking-wider ${
                  lastFeedback.grade === 'PERFECT'
                    ? 'text-amber-300'
                    : lastFeedback.grade === 'GREAT'
                    ? 'text-cyan-300'
                    : 'text-slate-400'
                }`}
              >
                {lastFeedback.labelVn}{' '}
                {lastFeedback.multiplier > 0 ? `· x${lastFeedback.multiplier.toFixed(1)}` : ''}
              </div>
              {lastFeedback.damageBillions > 0 && (
                <div className="font-tech text-xs md:text-sm font-bold text-red-400">
                  -{lastFeedback.damageBillions.toFixed(3)}B HP
                </div>
              )}
            </div>
          ) : (
            <div className="text-xs font-tech text-slate-400 text-center">
              Canh vòng hào quang 3D chạm <span className="text-amber-300 font-semibold">Gờ Vàng Đe</span> ({FORGE_BPM} BPM) · Nhấn{' '}
              <span className="text-cyan-300 font-semibold">Space / Chạm Đe</span>
            </div>
          )}
        </div>

        {/* Three.js 3D Celestial Anvil + Divine Hammer + 3,000-Spark GPU Particle System */}
        <CelestialAnvil3D
          ref={anvil3DRef}
          waveProgressRef={waveProgressRef}
          currentStance={HAMMER_STANCES[activeStance].stanceId}
          activeStance={activeStance}
          overdriveActive={overdriveActive}
          globalBurstActive={globalBurstActive}
          lastStrikeId={lastFeedback?.id ?? 0}
          lastStrikeGrade={lastFeedback?.grade ?? 'PERFECT'}
          onStrike={onStrike}
        />

        {/* 4 HAMMER STANCES ARC (Q - W - E - R / THUNDER - FIRE - GRAVITY - MYSTIC) AROUND THE 3D ANVIL */}
        <div
          role="group"
          aria-label="4 Thế Búa Q W E R"
          className="w-full grid grid-cols-4 gap-2 mt-2"
        >
          {stanceKeys.map((k, idx) => {
            const st = HAMMER_STANCES[k];
            const isSelected = activeStance === k;
            const arcOffset = idx === 0 || idx === 3 ? '-translate-y-1.5' : 'translate-y-0';

            return (
              <button
                key={k}
                type="button"
                onClick={() => onSelectStance(k)}
                className={`relative flex flex-col items-center p-2 rounded-xl border transition-all cursor-pointer ${arcOffset} ${
                  isSelected
                    ? 'bg-[#111625] border-amber-400 shadow-md shadow-amber-500/20 scale-[1.03]'
                    : 'bg-[#080A10] border-slate-800 hover:border-slate-700 text-slate-400'
                }`}
              >
                <div className="flex items-center gap-1.5 mb-0.5">
                  <span
                    className="w-5 h-5 rounded text-xs font-tech font-bold flex items-center justify-center text-slate-950"
                    style={{ backgroundColor: st.color }}
                  >
                    {k}
                  </span>
                  {k === 'Q' && <Zap className="w-3.5 h-3.5 text-cyan-400" />}
                  {k === 'W' && <Flame className="w-3.5 h-3.5 text-red-400" />}
                  {k === 'E' && <Shield className="w-3.5 h-3.5 text-purple-400" />}
                  {k === 'R' && <Sparkles className="w-3.5 h-3.5 text-emerald-400" />}
                </div>
                <div className="text-[11px] font-semibold text-slate-100 whitespace-nowrap truncate max-w-full">
                  {st.name}
                </div>
                <div className="hidden sm:block text-[10px] font-tech text-slate-400 whitespace-nowrap truncate max-w-full">
                  {st.stanceId}
                </div>
              </button>
            );
          })}
        </div>
      </div>

      {/* Bottom Overdrive 8/8 Bar + Mobile One-Thumb Action Strip */}
      <div className="relative z-10 w-full max-w-[500px] flex flex-col gap-2 mt-2">
        <div
          className={`w-full rounded-xl px-3 py-2 border transition-colors ${
            overdriveActive
              ? 'bg-cyan-500/15 border-cyan-400'
              : 'bg-[#111625] border-slate-800'
          }`}
        >
          <div className="flex items-center justify-between text-xs font-tech mb-1.5">
            <span className={overdriveActive ? 'text-cyan-300 font-bold' : 'text-slate-300'}>
              {overdriveActive
                ? `LÔI ĐÌNH QUÁ TẢI · BÃO TỐ (${overdriveTimeLeft.toFixed(1)}s)`
                : 'Thanh Overdrive · Tích Đủ 8/8 Chuỗi'}
            </span>
            <span className="font-bold text-amber-300">
              {overdriveActive ? 'SÁT THƯƠNG x2.0' : `${overdriveCharge.toFixed(1)} / ${OVERDRIVE_MAX}`}
            </span>
          </div>

          <div className="grid grid-cols-8 gap-1.5">
            {Array.from({ length: OVERDRIVE_MAX }).map((_, idx) => {
              const filled = overdriveActive || overdriveCharge >= idx + 1;
              const half = !filled && overdriveCharge >= idx + 0.5;
              return (
                <div
                  key={idx}
                  className={`h-2.5 rounded-sm transition-all ${
                    overdriveActive
                      ? 'bg-cyan-400 shadow-sm shadow-cyan-400/60'
                      : filled
                      ? 'bg-amber-400'
                      : half
                      ? 'bg-amber-400/50'
                      : 'bg-slate-800'
                  }`}
                />
              );
            })}
          </div>
        </div>

        {/* Mobile One-Thumb Forging Pad & Bottom Sheet Drawer Trigger (Visible on <lg viewports) */}
        <div className="flex lg:hidden items-center gap-2 w-full">
          <button
            type="button"
            onClick={onStrike}
            className="flex-1 py-3.5 px-3 rounded-xl bg-amber-400 active:bg-amber-300 text-slate-950 font-display font-bold text-xs sm:text-sm tracking-wider shadow-lg shadow-amber-500/20 cursor-pointer whitespace-nowrap truncate"
          >
            GIÁNG BÚA ({activeStance})
          </button>
          <button
            type="button"
            onClick={onOpenMobileDrawer}
            className="py-3.5 px-3 rounded-xl bg-[#111625] border border-slate-700 text-amber-300 font-tech text-xs font-semibold flex items-center gap-1 cursor-pointer whitespace-nowrap shrink-0"
          >
            <ChevronUp className="w-4 h-4" />
            <span>Nâng Cấp & Thần Hồn</span>
          </button>
        </div>
      </div>
    </main>
  );
};
