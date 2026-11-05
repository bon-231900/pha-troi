import React, { useEffect, useRef, useState, useCallback, useImperativeHandle, forwardRef } from 'react';
import { PlayerClassId, PLAYER_CLASSES, StanceKey, SECT_DEFAULT_SKIN, CHARACTER_SKINS } from '../game/rules';
import { soundEngine } from '../game/audio';

export interface InteractiveAltarPreviewRef {
  triggerStrike: () => void;
}

interface InteractiveAltarPreviewProps {
  selectedClassId: PlayerClassId;
  characterName: string;
  skinId?: string;
  onStrikeStatsUpdate?: (stats: { totalStrikes: number; perfectStrikes: number; lastRating: string }) => void;
}

interface FloatingText {
  id: number;
  text: string;
  x: number;
  y: number;
  vy: number;
  alpha: number;
  color: string;
  glowColor: string;
  scale: number;
}

interface Particle {
  x: number;
  y: number;
  vx: number;
  vy: number;
  alpha: number;
  life: number;
  maxLife: number;
  color: string;
  size: number;
}

interface LightningBolt {
  segments: { x: number; y: number }[];
  alpha: number;
  color: string;
  lineWidth: number;
}

interface Shockwave {
  x: number;
  y: number;
  r: number;
  maxR: number;
  alpha: number;
  color: string;
}

const SECT_PALETTES: Record<PlayerClassId, {
  glow: string;
  light: string;
  deep: string;
  spark: string;
  rune: string;
  nameVn: string;
  strikeTitle: string;
}> = {
  thunder: {
    glow: '#00F0FF',
    light: '#38BDF8',
    deep: 'rgba(0, 240, 255, 0.12)',
    spark: '#E0F2FE',
    rune: 'rgba(0, 240, 255, 0.65)',
    nameVn: 'Lôi Đỉnh',
    strikeTitle: 'THIÊN LÔI BẠO KÍCH',
  },
  fire: {
    glow: '#FF5500',
    light: '#FB923C',
    deep: 'rgba(255, 85, 0, 0.12)',
    spark: '#FED7AA',
    rune: 'rgba(255, 85, 0, 0.65)',
    nameVn: 'Viêm Dương',
    strikeTitle: 'HỎA PHẦN THIÊN ĐỊA',
  },
  gravity: {
    glow: '#A855F7',
    light: '#C084FC',
    deep: 'rgba(168, 85, 247, 0.12)',
    spark: '#F3E8FF',
    rune: 'rgba(168, 85, 247, 0.65)',
    nameVn: 'Trọng Lực',
    strikeTitle: 'TỬ TINH CHẤN ĐỊA',
  },
  mystic: {
    glow: '#10B981',
    light: '#34D399',
    deep: 'rgba(16, 185, 129, 0.12)',
    spark: '#D1FAE5',
    rune: 'rgba(16, 185, 129, 0.65)',
    nameVn: 'Huyền Âm',
    strikeTitle: 'HUYỀN ÂM CỘNG HƯỞNG',
  },
};

// Procedural Tiên Hiệp Daoist Plaque Renderer
function drawDaoistPlaque(
  ctx: CanvasRenderingContext2D,
  x: number,
  y: number,
  title: string,
  classId: PlayerClassId
) {
  ctx.save();
  ctx.translate(x, y);

  const pal = SECT_PALETTES[classId];

  // Font typography
  ctx.font = '700 14px "Lora", serif';
  const tw = ctx.measureText(title).width;

  const padX = 18;
  const bw = Math.max(140, tw + padX * 2);
  const bh = 24;
  const halfW = bw * 0.5;
  const halfH = bh * 0.5;

  // 1. Shadow
  ctx.save();
  ctx.fillStyle = 'rgba(0, 0, 0, 0.85)';
  ctx.filter = 'blur(6px)';
  ctx.beginPath();
  ctx.roundRect(-halfW - 4, -halfH - 2, bw + 8, bh + 6, 6);
  ctx.fill();
  ctx.restore();

  // 2. Swallowtail Body
  const chamfer = 6;
  const wingNotch = 5;

  ctx.save();
  const bodyGrad = ctx.createLinearGradient(0, -halfH, 0, halfH);
  bodyGrad.addColorStop(0, '#161B2E');
  bodyGrad.addColorStop(1, '#0B0F1C');
  ctx.fillStyle = bodyGrad;

  ctx.beginPath();
  ctx.moveTo(-halfW + chamfer, -halfH);
  ctx.lineTo(halfW - chamfer, -halfH);
  ctx.lineTo(halfW, -halfH + chamfer);
  ctx.lineTo(halfW + wingNotch, 0); // Right swallowtail wing
  ctx.lineTo(halfW, halfH - chamfer);
  ctx.lineTo(halfW - chamfer, halfH);
  ctx.lineTo(-halfW + chamfer, halfH);
  ctx.lineTo(-halfW, halfH - chamfer);
  ctx.lineTo(-halfW - wingNotch, 0); // Left swallowtail wing
  ctx.lineTo(-halfW, -halfH + chamfer);
  ctx.closePath();
  ctx.fill();

  // Gold/Sect rim
  ctx.strokeStyle = pal.glow;
  ctx.lineWidth = 1.3;
  ctx.shadowColor = pal.glow;
  ctx.shadowBlur = 8;
  ctx.stroke();
  ctx.restore();

  // 3. Inner Filigree
  ctx.save();
  ctx.strokeStyle = '#FDE68A';
  ctx.lineWidth = 0.8;
  ctx.globalAlpha = 0.45;
  const inPad = 2.5;
  ctx.beginPath();
  ctx.moveTo(-halfW + chamfer + inPad, -halfH + inPad);
  ctx.lineTo(halfW - chamfer - inPad, -halfH + inPad);
  ctx.lineTo(halfW - inPad, -halfH + chamfer + inPad);
  ctx.lineTo(halfW + wingNotch - inPad, 0);
  ctx.lineTo(halfW - inPad, halfH - chamfer - inPad);
  ctx.lineTo(halfW - chamfer - inPad, halfH - inPad);
  ctx.lineTo(-halfW + chamfer + inPad, halfH - inPad);
  ctx.lineTo(-halfW + inPad, halfH - chamfer - inPad);
  ctx.lineTo(-halfW - wingNotch + inPad, 0);
  ctx.lineTo(-halfW + inPad, -halfH + chamfer + inPad);
  ctx.closePath();
  ctx.stroke();
  ctx.restore();

  // 4. Inset Gems on wings
  ctx.save();
  ctx.fillStyle = pal.glow;
  ctx.shadowColor = pal.glow;
  ctx.shadowBlur = 5;
  ctx.beginPath();
  ctx.arc(-halfW - 1, 0, 2, 0, Math.PI * 2);
  ctx.arc(halfW + 1, 0, 2, 0, Math.PI * 2);
  ctx.fill();
  ctx.restore();

  // 5. Text with Handwriting Calligraphy
  ctx.save();
  ctx.font = '700 14px "Lora", serif';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillStyle = 'rgba(0, 0, 0, 0.9)';
  ctx.fillText(title, 0, 1); // Drop shadow
  ctx.fillStyle = '#FEF08A';
  ctx.fillText(title, 0, 0);
  ctx.restore();

  ctx.restore();
}

export const InteractiveAltarPreview = forwardRef<InteractiveAltarPreviewRef, InteractiveAltarPreviewProps>((
  { selectedClassId, characterName, onStrikeStatsUpdate },
  ref
) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);

  // Statistics
  const [totalStrikes, setTotalStrikes] = useState(0);
  const [perfectStrikes, setPerfectStrikes] = useState(0);
  const [lastRating, setLastRating] = useState<string>('');
  const [lastDamage, setLastDamage] = useState<number>(0);

  // Animation & game loop refs
  const strikeTimerRef = useRef<number>(-1);
  const screenShakeRef = useRef<number>(0);
  const particlesRef = useRef<Particle[]>([]);
  const floatingTextsRef = useRef<FloatingText[]>([]);
  const lightningBoltsRef = useRef<LightningBolt[]>([]);
  const shockwavesRef = useRef<Shockwave[]>([]);
  const nextTextIdRef = useRef<number>(1);

  // Asset image refs
  const altarImgRef = useRef<HTMLImageElement | null>(null);
  const heroSheetRef = useRef<HTMLImageElement | null>(null);
  const skinCacheRef = useRef<Map<string, HTMLImageElement>>(new Map());
  const assetsLoadedRef = useRef<boolean>(false);

  // Effective skin for this class
  const activeSkinId = skinId || SECT_DEFAULT_SKIN[selectedClassId] || 'skin_default';

  // Base platform asset loader
  useEffect(() => {
    let active = true;
    const base = import.meta.env.BASE_URL || '/';
    const cleanBase = base.endsWith('/') ? base : `${base}/`;

    const altarImg = new Image();
    altarImg.onload = () => {
      if (active) {
        altarImgRef.current = altarImg;
        assetsLoadedRef.current = true;
      }
    };
    altarImg.src = `${cleanBase}assets/art/altar_platform.webp`;
    if (altarImg.complete) {
      altarImgRef.current = altarImg;
      assetsLoadedRef.current = true;
    }

    return () => {
      active = false;
    };
  }, []);

  // Dynamic Skin Spritesheet Loader (instant cached switching)
  useEffect(() => {
    let active = true;
    const base = import.meta.env.BASE_URL || '/';
    const cleanBase = base.endsWith('/') ? base : `${base}/`;

    const cached = skinCacheRef.current.get(activeSkinId);
    if (cached && cached.complete) {
      heroSheetRef.current = cached;
      return;
    }

    const skinMeta = CHARACTER_SKINS[activeSkinId];
    const srcPath = skinMeta ? `${cleanBase}${skinMeta.spritesheetPath}` : `${cleanBase}assets/art/hero_spritesheet_strip.webp`;
    const skinImg = new Image();
    skinImg.onload = () => {
      if (active) {
        skinCacheRef.current.set(activeSkinId, skinImg);
        heroSheetRef.current = skinImg;
      }
    };
    skinImg.src = srcPath;
    if (skinImg.complete) {
      skinCacheRef.current.set(activeSkinId, skinImg);
      heroSheetRef.current = skinImg;
    }

    return () => {
      active = false;
    };
  }, [activeSkinId]);

  // Strike Action Function
  const executeStrike = useCallback(() => {
    soundEngine.unlockAudio();
    const cls = PLAYER_CLASSES[selectedClassId];
    const pal = SECT_PALETTES[selectedClassId];

    // Rhythm calculation: 100 BPM = 600ms period
    const now = performance.now();
    const beatPeriod = 600; // ms
    const phase = (now % beatPeriod) / beatPeriod;
    const sweetSpot = 0.78;
    const diff = Math.abs(phase - sweetSpot);

    let rating: 'PERFECT' | 'GREAT' | 'HIT' = 'HIT';
    let baseDamage = 350;
    let multiplier = 1.0;

    if (diff <= 0.10 || diff >= 0.90) {
      rating = 'PERFECT';
      multiplier = 2.8;
      baseDamage = 980;
    } else if (diff <= 0.22 || diff >= 0.78) {
      rating = 'GREAT';
      multiplier = 1.8;
      baseDamage = 620;
    } else {
      rating = 'HIT';
      multiplier = 1.1;
      baseDamage = 380;
    }

    const finalDamage = Math.floor(baseDamage * (0.95 + Math.random() * 0.12));

    // Sound feedback
    const stanceKey = cls.stanceKey as StanceKey;
    soundEngine.playAnvilStrike(rating, stanceKey, rating === 'PERFECT');

    // Trigger visual hero strike animation
    strikeTimerRef.current = 0; // Starts strike timer
    screenShakeRef.current = rating === 'PERFECT' ? 7 : rating === 'GREAT' ? 4 : 2;

    // Spawn Lightning Bolt
    const canvas = canvasRef.current;
    if (canvas) {
      const cw = canvas.width;
      const ch = canvas.height;
      const impactX = cw * 0.5 + 16;
      const impactY = ch * 0.70;

      // Celestial lightning bolt from sky to anvil
      const segments: { x: number; y: number }[] = [];
      const startX = impactX + (Math.random() - 0.5) * 80;
      const startY = 10;
      const segCount = 7;
      for (let s = 0; s <= segCount; s++) {
        const t = s / segCount;
        const curX = startX + (impactX - startX) * t + (s > 0 && s < segCount ? (Math.random() - 0.5) * 40 : 0);
        const curY = startY + (impactY - startY) * t;
        segments.push({ x: curX, y: curY });
      }

      lightningBoltsRef.current.push({
        segments,
        alpha: 1.0,
        color: pal.glow,
        lineWidth: rating === 'PERFECT' ? 4 : 2.5,
      });

      // Shockwave
      shockwavesRef.current.push({
        x: impactX,
        y: impactY,
        r: 8,
        maxR: rating === 'PERFECT' ? 95 : 65,
        alpha: 0.95,
        color: pal.glow,
      });

      // Sparks burst
      const sparkCount = rating === 'PERFECT' ? 24 : 14;
      for (let i = 0; i < sparkCount; i++) {
        const angle = Math.random() * Math.PI * 2;
        const speed = 2 + Math.random() * 5.5;
        particlesRef.current.push({
          x: impactX,
          y: impactY,
          vx: Math.cos(angle) * speed,
          vy: Math.sin(angle) * speed - 2.5,
          alpha: 1.0,
          life: 0,
          maxLife: 20 + Math.random() * 15,
          color: Math.random() > 0.4 ? pal.spark : pal.glow,
          size: 1.5 + Math.random() * 2.5,
        });
      }

      // Floating Combat Text
      const textLabel =
        rating === 'PERFECT'
          ? `★ ${pal.strikeTitle}! -${finalDamage.toLocaleString()}`
          : rating === 'GREAT'
          ? `★ CHÍNH XÁC! -${finalDamage.toLocaleString()}`
          : `ĐOẠN THIẾT -${finalDamage.toLocaleString()}`;

      floatingTextsRef.current.push({
        id: nextTextIdRef.current++,
        text: textLabel,
        x: impactX,
        y: impactY - 35,
        vy: -1.6,
        alpha: 1.0,
        color: rating === 'PERFECT' ? '#FDE047' : pal.glow,
        glowColor: pal.glow,
        scale: rating === 'PERFECT' ? 1.25 : 1.0,
      });
    }

    // Update state stats
    setTotalStrikes((prev) => {
      const nextTotal = prev + 1;
      const nextPerfect = rating === 'PERFECT' ? perfectStrikes + 1 : perfectStrikes;
      setPerfectStrikes(nextPerfect);
      setLastRating(rating);
      setLastDamage(finalDamage);

      if (onStrikeStatsUpdate) {
        onStrikeStatsUpdate({
          totalStrikes: nextTotal,
          perfectStrikes: nextPerfect,
          lastRating: rating,
        });
      }
      return nextTotal;
    });
  }, [selectedClassId, perfectStrikes, onStrikeStatsUpdate]);

  // Expose ref
  useImperativeHandle(ref, () => ({
    triggerStrike: executeStrike,
  }));

  // Keyboard Space listener (capture mode, supports all space variants)
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      const isSpace =
        e.code === 'Space' ||
        e.key === ' ' ||
        e.key === 'Spacebar' ||
        e.keyCode === 32 ||
        e.which === 32;

      if (!isSpace) return;

      const target = e.target as HTMLElement | null;
      if (target && (target.tagName === 'INPUT' || target.tagName === 'TEXTAREA')) {
        return; // Let typing spaces work in name input
      }

      e.preventDefault();
      e.stopPropagation();
      executeStrike();
    };

    window.addEventListener('keydown', handleKeyDown, true);
    return () => {
      window.removeEventListener('keydown', handleKeyDown, true);
    };
  }, [executeStrike]);

  // Main 60 FPS Render Loop
  useEffect(() => {
    const canvas = canvasRef.current;
    const container = containerRef.current;
    if (!canvas || !container) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let animId: number;
    let lastTime = performance.now();
    let baguaAngle = 0;

    // Ambient background motes
    const ambientMotes: { x: number; y: number; r: number; speed: number; alpha: number }[] = [];
    for (let i = 0; i < 28; i++) {
      ambientMotes.push({
        x: Math.random() * 400,
        y: Math.random() * 400,
        r: 0.8 + Math.random() * 1.8,
        speed: 0.2 + Math.random() * 0.5,
        alpha: 0.2 + Math.random() * 0.5,
      });
    }

    const resize = () => {
      const w = container.clientWidth || 360;
      const h = container.clientHeight || 420;
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      canvas.width = w * dpr;
      canvas.height = h * dpr;
      canvas.style.width = `${w}px`;
      canvas.style.height = `${h}px`;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    };

    resize();
    window.addEventListener('resize', resize);

    const render = (now: number) => {
      const dt = Math.min(0.1, (now - lastTime) / 1000);
      lastTime = now;

      const w = container.clientWidth || 360;
      const h = container.clientHeight || 420;

      // Update screen shake
      let offsetX = 0;
      let offsetY = 0;
      if (screenShakeRef.current > 0) {
        offsetX = (Math.random() - 0.5) * screenShakeRef.current * 2;
        offsetY = (Math.random() - 0.5) * screenShakeRef.current * 2;
        screenShakeRef.current = Math.max(0, screenShakeRef.current - dt * 25);
      }

      ctx.save();
      ctx.translate(offsetX, offsetY);

      // 1. Clear & Background Gradient
      ctx.clearRect(-10, -10, w + 20, h + 20);

      const pal = SECT_PALETTES[selectedClassId];
      const bgGrad = ctx.createRadialGradient(w * 0.5, h * 0.45, 20, w * 0.5, h * 0.5, w * 0.85);
      bgGrad.addColorStop(0, '#0F172A');
      bgGrad.addColorStop(0.55, '#070A14');
      bgGrad.addColorStop(1, '#020308');
      ctx.fillStyle = bgGrad;
      ctx.fillRect(0, 0, w, h);

      // Ambient Sect Glow Pool
      const sectGlowGrad = ctx.createRadialGradient(w * 0.5, h * 0.65, 10, w * 0.5, h * 0.65, w * 0.55);
      sectGlowGrad.addColorStop(0, pal.deep);
      sectGlowGrad.addColorStop(1, 'transparent');
      ctx.fillStyle = sectGlowGrad;
      ctx.fillRect(0, 0, w, h);

      // 2. Ambient Floating Motes
      ctx.save();
      ctx.fillStyle = pal.spark;
      for (const m of ambientMotes) {
        m.y -= m.speed;
        if (m.y < 0) {
          m.y = h;
          m.x = Math.random() * w;
        }
        ctx.globalAlpha = m.alpha * (0.6 + Math.sin(now * 0.003 + m.x) * 0.3);
        ctx.beginPath();
        ctx.arc(m.x, m.y, m.r, 0, Math.PI * 2);
        ctx.fill();
      }
      ctx.restore();

      // 3. Central Altar Platform (2.5D Bagua Altar)
      const altarCenterX = w * 0.5;
      const altarCenterY = h * 0.72;
      const altarW = Math.min(280, w * 0.82);

      if (altarImgRef.current && assetsLoadedRef.current) {
        const aImg = altarImgRef.current;
        const altarH = altarW * (aImg.height / aImg.width);
        const aX = altarCenterX - altarW * 0.5;
        const aY = altarCenterY - altarH * 0.35;

        // Ground shadow
        ctx.save();
        ctx.fillStyle = 'rgba(0, 0, 0, 0.85)';
        ctx.filter = 'blur(12px)';
        ctx.beginPath();
        ctx.ellipse(altarCenterX, altarCenterY + altarH * 0.32, altarW * 0.46, 16, 0, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();

        // Altar Image
        ctx.drawImage(aImg, aX, aY, altarW, altarH);
      }

      // 4. Rotating Bagua / Daoist Rune Array on Altar
      baguaAngle += dt * 0.45;
      ctx.save();
      ctx.translate(altarCenterX, altarCenterY);
      ctx.scale(1.0, 0.32); // 2.5D perspective flatten
      ctx.rotate(baguaAngle);

      ctx.strokeStyle = pal.rune;
      ctx.lineWidth = 1.4;
      ctx.shadowColor = pal.glow;
      ctx.shadowBlur = 10;
      ctx.globalAlpha = 0.65 + Math.sin(now * 0.003) * 0.2;

      // Outer rune circle
      const runeRadius = altarW * 0.36;
      ctx.beginPath();
      ctx.arc(0, 0, runeRadius, 0, Math.PI * 2);
      ctx.stroke();

      // Inner 8 Trigram spokes
      for (let i = 0; i < 8; i++) {
        const ang = (i * Math.PI) / 4;
        ctx.beginPath();
        ctx.moveTo(Math.cos(ang) * (runeRadius * 0.45), Math.sin(ang) * (runeRadius * 0.45));
        ctx.lineTo(Math.cos(ang) * (runeRadius * 0.95), Math.sin(ang) * (runeRadius * 0.95));
        ctx.stroke();
      }
      ctx.restore();

      // 5. Main Hero Sprite with Strike Animation
      const heroSheet = heroSheetRef.current;
      const FRAME_W = 360;
      const FRAME_H = 480;
      const renderScale = Math.min(0.48, (w / 380) * 0.46);
      const dw = FRAME_W * renderScale;
      const dh = FRAME_H * renderScale;
      const heroFootX = altarCenterX - 10;
      const heroFootY = altarCenterY - 4;
      const spriteLeft = heroFootX - dw * 0.46;
      const spriteTop = heroFootY - 440 * renderScale;

      // Hero Foot Shadow
      ctx.save();
      ctx.fillStyle = 'rgba(0, 0, 0, 0.75)';
      ctx.filter = 'blur(6px)';
      ctx.beginPath();
      ctx.ellipse(heroFootX - 12, heroFootY + 2, 22, 6, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.beginPath();
      ctx.ellipse(heroFootX + 24, heroFootY + 3, 26, 7, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();

      // Frame mapping for strike
      let heroFrameIdx = 0;
      const STRIKE_TOTAL_SEC = 0.42;
      if (strikeTimerRef.current >= 0) {
        strikeTimerRef.current += dt;
        const progress = Math.min(1.0, strikeTimerRef.current / STRIKE_TOTAL_SEC);
        if (progress < 0.18) heroFrameIdx = 1;
        else if (progress < 0.38) heroFrameIdx = 2;
        else if (progress < 0.62) heroFrameIdx = 3; // Impact
        else if (progress < 0.82) heroFrameIdx = 4;
        else heroFrameIdx = 5;

        if (strikeTimerRef.current >= STRIKE_TOTAL_SEC) {
          strikeTimerRef.current = -1; // Done strike
        }
      }

      if (heroSheet && assetsLoadedRef.current) {
        const sx = heroFrameIdx * FRAME_W;
        const sy = 0;

        ctx.save();
        if (heroFrameIdx === 3) {
          // Impact glow
          ctx.shadowColor = pal.glow;
          ctx.shadowBlur = 24;
        }
        ctx.drawImage(heroSheet, sx, sy, FRAME_W, FRAME_H, spriteLeft, spriteTop, dw, dh);
        ctx.restore();
      }

      // 6. Contracting 100 BPM Rhythm Ring on Anvil
      const anvilImpactX = spriteLeft + 213 * renderScale;
      const anvilImpactY = spriteTop + 342 * renderScale;

      const beatPeriod = 600; // 100 BPM = 600ms
      const rhythmPhase = (now % beatPeriod) / beatPeriod;
      const ringScale = 1.0 - rhythmPhase;
      const isSweetSpot = Math.abs(rhythmPhase - 0.78) <= 0.12;

      ctx.save();
      ctx.strokeStyle = isSweetSpot ? '#FFD166' : pal.glow;
      ctx.lineWidth = isSweetSpot ? 2.8 : 1.4;
      ctx.shadowColor = isSweetSpot ? '#FFD166' : pal.glow;
      ctx.shadowBlur = isSweetSpot ? 12 : 5;
      ctx.globalAlpha = 0.4 + rhythmPhase * 0.55;

      ctx.beginPath();
      ctx.ellipse(
        anvilImpactX,
        anvilImpactY,
        12 + ringScale * 38,
        5 + ringScale * 14,
        0,
        0,
        Math.PI * 2
      );
      ctx.stroke();

      // Static target ring on anvil
      ctx.strokeStyle = '#FFFFFF';
      ctx.lineWidth = 1.0;
      ctx.globalAlpha = 0.5;
      ctx.beginPath();
      ctx.ellipse(anvilImpactX, anvilImpactY, 13, 5.5, 0, 0, Math.PI * 2);
      ctx.stroke();
      ctx.restore();

      // 7. Shockwaves
      for (let i = shockwavesRef.current.length - 1; i >= 0; i--) {
        const sw = shockwavesRef.current[i];
        sw.r += dt * 140;
        sw.alpha -= dt * 2.2;
        if (sw.alpha <= 0 || sw.r >= sw.maxR) {
          shockwavesRef.current.splice(i, 1);
          continue;
        }
        ctx.save();
        ctx.strokeStyle = sw.color;
        ctx.lineWidth = 2.4 * sw.alpha;
        ctx.globalAlpha = Math.max(0, sw.alpha);
        ctx.shadowColor = sw.color;
        ctx.shadowBlur = 10;
        ctx.beginPath();
        ctx.ellipse(sw.x, sw.y, sw.r, sw.r * 0.35, 0, 0, Math.PI * 2);
        ctx.stroke();
        ctx.restore();
      }

      // 8. Lightning Bolts
      for (let i = lightningBoltsRef.current.length - 1; i >= 0; i--) {
        const bolt = lightningBoltsRef.current[i];
        bolt.alpha -= dt * 4.5;
        if (bolt.alpha <= 0) {
          lightningBoltsRef.current.splice(i, 1);
          continue;
        }
        ctx.save();
        ctx.strokeStyle = '#FFFFFF';
        ctx.lineWidth = bolt.lineWidth;
        ctx.shadowColor = bolt.color;
        ctx.shadowBlur = 18;
        ctx.globalAlpha = Math.max(0, bolt.alpha);

        ctx.beginPath();
        ctx.moveTo(bolt.segments[0].x, bolt.segments[0].y);
        for (let s = 1; s < bolt.segments.length; s++) {
          ctx.lineTo(bolt.segments[s].x, bolt.segments[s].y);
        }
        ctx.stroke();

        ctx.strokeStyle = bolt.color;
        ctx.lineWidth = bolt.lineWidth * 2.2;
        ctx.globalAlpha = Math.max(0, bolt.alpha * 0.45);
        ctx.stroke();
        ctx.restore();
      }

      // 9. Particle Sparks
      for (let i = particlesRef.current.length - 1; i >= 0; i--) {
        const p = particlesRef.current[i];
        p.x += p.vx;
        p.y += p.vy;
        p.vy += dt * 9.8; // gravity
        p.life++;
        p.alpha = 1 - p.life / p.maxLife;

        if (p.life >= p.maxLife || p.alpha <= 0) {
          particlesRef.current.splice(i, 1);
          continue;
        }

        ctx.save();
        ctx.fillStyle = p.color;
        ctx.shadowColor = p.color;
        ctx.shadowBlur = 6;
        ctx.globalAlpha = Math.max(0, p.alpha);
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
      }

      // 10. Overhead Tiên Hiệp Daoist Swallowtail Plaque
      const plaqueTitle = `${characterName.trim() || 'Vô Danh Tu Sĩ'} · [${pal.nameVn}]`;
      const plaqueY = spriteTop - 18;
      drawDaoistPlaque(ctx, altarCenterX, plaqueY, plaqueTitle, selectedClassId);

      // 11. Floating Combat Texts
      for (let i = floatingTextsRef.current.length - 1; i >= 0; i--) {
        const ft = floatingTextsRef.current[i];
        ft.y += ft.vy;
        ft.alpha -= dt * 0.9;

        if (ft.alpha <= 0) {
          floatingTextsRef.current.splice(i, 1);
          continue;
        }

        ctx.save();
        ctx.font = `800 ${14 * ft.scale}px "Playfair Display", serif`;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.globalAlpha = Math.max(0, ft.alpha);

        // Text stroke glow
        ctx.strokeStyle = 'rgba(0, 0, 0, 0.9)';
        ctx.lineWidth = 3.5;
        ctx.strokeText(ft.text, ft.x, ft.y);

        ctx.fillStyle = ft.color;
        ctx.shadowColor = ft.glowColor;
        ctx.shadowBlur = 12;
        ctx.fillText(ft.text, ft.x, ft.y);
        ctx.restore();
      }

      ctx.restore();
      animId = requestAnimationFrame(render);
    };

    animId = requestAnimationFrame(render);

    return () => {
      cancelAnimationFrame(animId);
      window.removeEventListener('resize', resize);
    };
  }, [selectedClassId, characterName]);

  const cls = PLAYER_CLASSES[selectedClassId];
  const pal = SECT_PALETTES[selectedClassId];

  return (
    <div className="flex flex-col w-full h-full relative select-none">
      {/* 2.5D Interactive Canvas Container */}
      <div
        ref={containerRef}
        onClick={executeStrike}
        className="relative w-full h-[280px] sm:h-[320px] lg:h-[360px] rounded-2xl overflow-hidden border border-amber-500/30 bg-[#050811] shadow-2xl cursor-pointer group"
      >
        <canvas ref={canvasRef} className="block w-full h-full" />

        {/* Top Header Badge */}
        <div className="absolute top-3 left-3 right-3 flex items-center justify-between pointer-events-none">
          <div className="flex items-center gap-2 px-2.5 py-1 rounded-lg bg-slate-950/80 border border-slate-800 backdrop-blur-sm">
            <span className="w-2 h-2 rounded-full animate-ping" style={{ backgroundColor: pal.glow }} />
            <span className="text-[11px] font-tech font-bold text-amber-200">
              BỆ ĐÁ BÁT QUÁI · NỆN THỬ CĂN CƠ
            </span>
          </div>

          <div className="text-[10px] font-tech text-slate-300 px-2 py-0.5 rounded bg-slate-900/80 border border-slate-800">
            NHỊP ĐE: 100 BPM
          </div>
        </div>

        {/* Center Prompt on Hover */}
        <div className="absolute bottom-3 left-3 right-3 flex items-center justify-between pointer-events-none">
          <div className="text-[11px] font-tech text-slate-400 bg-slate-950/80 px-2.5 py-1 rounded-lg border border-slate-800 backdrop-blur-sm">
            Chạm màn hình hoặc bấm <span className="text-amber-300 font-bold">[SPACE]</span> để gõ búa
          </div>

          {totalStrikes > 0 && (
            <div className="text-[11px] font-tech text-amber-300 bg-slate-950/80 px-2.5 py-1 rounded-lg border border-slate-800 backdrop-blur-sm flex items-center gap-2">
              <span>Đã thử: <strong>{totalStrikes}</strong> lần</span>
              <span className="text-emerald-400">({perfectStrikes} Hoàn Hảo)</span>
            </div>
          )}
        </div>
      </div>

      {/* Control Bar & Feedback below Canvas */}
      <div className="mt-3 flex flex-col sm:flex-row items-center justify-between gap-2.5 p-2.5 rounded-xl bg-slate-950/80 border border-slate-800">
        <button
          type="button"
          onClick={executeStrike}
          className="w-full sm:w-auto flex-1 flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl text-xs sm:text-sm font-tech font-bold tracking-wider uppercase transition-all cursor-pointer active:scale-95 shadow-lg"
          style={{
            backgroundColor: pal.glow,
            color: '#000000',
            boxShadow: `0 0 16px ${pal.glow}40`,
          }}
        >
          <span>⚡ NỆN THỬ BÚA [SPACE]</span>
        </button>

        <div className="text-[11px] font-tech text-slate-400 flex items-center gap-3">
          <span>Khí tức: <strong style={{ color: pal.glow }}>{cls.sectTitle.split('·')[0].trim()}</strong></span>
          <span>·</span>
          <span>Bạo phát: <strong className="text-amber-300">{cls.roleSummary.split('·')[0].trim()}</strong></span>
        </div>
      </div>
    </div>
  );
});

InteractiveAltarPreview.displayName = 'InteractiveAltarPreview';
