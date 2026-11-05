import React, {
  useEffect,
  useRef,
  useImperativeHandle,
  forwardRef,
  useCallback,
} from 'react';
import {
  PANORAMA_SKY_RATIO,
  HERO_STRIKE_TOTAL_SEC,
  SCREEN_SHAKE_DURATION_SEC,
  HERO_STANCE_PALETTES,
  type StanceKey,
  type Point2D,
} from '../game/rules';
import { hapticEngine } from '../game/haptics';

export interface RemotePeerStrikePayload {
  peerId: string;
  name: string;
  slotIndex: number;
  stance: StanceKey;
  damage: number;
  isGolden: boolean;
  isCrit?: boolean;
}

export interface RemotePeerInfo {
  peerId: string;
  name: string;
  guildId?: string;
  stance: StanceKey;
  slotIndex: number;
}

export interface CommunityPanoramicForgeCanvasHandle {
  triggerHeroStrike: (forceGolden?: boolean) => void;
  triggerPeerWave: () => void;
  triggerRemotePeerStrike: (payload: RemotePeerStrikePayload) => void;
  updateRemotePeers: (peers: RemotePeerInfo[]) => void;
  spawnCombatText: (
    text: string,
    subtext: string,
    color: string,
    glowColor: string,
    isGolden: boolean
  ) => void;
  reset: () => void;
}

export interface CommunityPanoramicForgeCanvasProps {
  bossHp: number;
  bossMaxHp: number;
  activeStance: StanceKey;
  gameState: 'title' | 'playing' | 'paused' | 'gameover';
  playerName?: string;
  onHeroStrikeAction?: (forceGolden: boolean) => void;
  onPeerAutonomousDamage?: (damageAmount: number) => void;
  className?: string;
}

interface ActiveLightningBolt2D {
  segments: Point2D[];
  alpha: number;
  decay: number;
  color: string;
  lineWidth: number;
}

interface SparkParticle2D {
  active: boolean;
  x: number;
  y: number;
  vx: number;
  vy: number;
  size: number;
  color: string;
  alpha: number;
  age: number;
  maxAge: number;
  isAsh: boolean;
}

interface FloatingCombatText2D {
  id: number;
  text: string;
  subtext: string;
  x: number;
  y: number;
  vy: number;
  color: string;
  glowColor: string;
  ageSec: number;
  durationSec: number;
  scale: number;
}

interface Shockwave2D {
  x: number;
  y: number;
  radius: number;
  maxRadius: number;
  alpha: number;
  color: string;
}

const MAX_SPARK_POOL = 360;

// Tiên Hiệp Daoist Plaque Color Palettes
const PLAQUE_PALETTES: Record<string, {
  gold: string;
  rim: string;
  glow: string;
  gem: string;
  text: string;
  bg1: string;
  bg2: string;
}> = {
  hero: {
    gold: '#FFD700',
    rim: '#F59E0B',
    glow: '#00F0FF',
    gem: '#00F0FF',
    text: '#FFFFFF',
    bg1: 'rgba(12, 18, 36, 0.96)',
    bg2: 'rgba(4, 7, 16, 0.98)',
  },
  thunder: {
    gold: '#7DD3FC',
    rim: '#00F0FF',
    glow: '#00F0FF',
    gem: '#38BDF8',
    text: '#E0F2FE',
    bg1: 'rgba(8, 18, 36, 0.95)',
    bg2: 'rgba(3, 8, 20, 0.98)',
  },
  fire: {
    gold: '#FDE68A',
    rim: '#FF7700',
    glow: '#FF5500',
    gem: '#FB923C',
    text: '#FED7AA',
    bg1: 'rgba(28, 12, 8, 0.95)',
    bg2: 'rgba(12, 4, 3, 0.98)',
  },
  mystic: {
    gold: '#A7F3D0',
    rim: '#10B981',
    glow: '#10B981',
    gem: '#34D399',
    text: '#D1FAE5',
    bg1: 'rgba(6, 26, 18, 0.95)',
    bg2: 'rgba(2, 12, 8, 0.98)',
  },
  gravity: {
    gold: '#E9D5FF',
    rim: '#A855F7',
    glow: '#C084FC',
    gem: '#C084FC',
    text: '#F3E8FF',
    bg1: 'rgba(20, 10, 32, 0.95)',
    bg2: 'rgba(8, 4, 16, 0.98)',
  },
};

const STANCE_TO_SECT: Record<string, string> = {
  Q: 'thunder',
  W: 'fire',
  E: 'gravity',
  R: 'mystic',
  thunder: 'thunder',
  fire: 'fire',
  gravity: 'gravity',
  mystic: 'mystic',
};

const SECT_COLORS: Record<string, { glow: string; light: string; spark: string }> = {
  thunder: { glow: '#00F0FF', light: '#38BDF8', spark: '#E0F2FE' },
  fire: { glow: '#FF5500', light: '#FB923C', spark: '#FED7AA' },
  gravity: { glow: '#A855F7', light: '#C084FC', spark: '#F3E8FF' },
  mystic: { glow: '#10B981', light: '#34D399', spark: '#D1FAE5' },
};

// Procedural Tiên Hiệp Daoist Plaque Renderer
function drawXianxiaPlaque(
  ctx: CanvasRenderingContext2D,
  x: number,
  y: number,
  text: string,
  stanceKey = 'thunder',
  isHero = false,
  isReal = true
) {
  if (!text || !text.trim()) return;

  ctx.save();
  ctx.translate(x, y);

  const sect = STANCE_TO_SECT[stanceKey] || 'thunder';
  const pal = isHero ? PLAQUE_PALETTES.hero : (PLAQUE_PALETTES[sect] || PLAQUE_PALETTES.thunder);

  ctx.font = isHero
    ? '700 15px "Charm", "Caveat", cursive'
    : '700 13.5px "Charm", "Caveat", cursive';
  const tw = ctx.measureText(text).width;

  // Harmonious compact width
  const padX = isHero ? 20 : 16;
  const bw = Math.max(isHero ? 150 : 124, tw + padX * 2);
  const bh = isHero ? 25 : 23;
  const halfW = bw * 0.5;
  const halfH = bh * 0.5;

  if (!isReal) {
    ctx.globalAlpha = 0.55;
  }

  // 1. Soft Shadow
  ctx.save();
  ctx.fillStyle = 'rgba(0, 0, 0, 0.85)';
  ctx.filter = 'blur(6px)';
  ctx.beginPath();
  ctx.roundRect(-halfW - 5, -halfH - 2, bw + 10, bh + 7, 6);
  ctx.fill();
  ctx.restore();

  // 2. Swallowtail Daoist Plaque Body
  const chamfer = isHero ? 8 : 6;
  const wingNotch = isHero ? 7 : 5;

  ctx.save();
  const bodyGrad = ctx.createLinearGradient(0, -halfH, 0, halfH);
  bodyGrad.addColorStop(0, pal.bg1);
  bodyGrad.addColorStop(1, pal.bg2);
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

  // Plaque Rim
  ctx.strokeStyle = isReal ? pal.rim : 'rgba(148, 163, 184, 0.4)';
  ctx.lineWidth = isHero ? 1.7 : 1.2;
  if (isReal) {
    ctx.shadowColor = pal.glow;
    ctx.shadowBlur = isHero ? 9 : 5;
  }
  ctx.stroke();
  ctx.restore();

  // 3. Inner Engraved Filigree Line
  if (isReal) {
    ctx.save();
    ctx.strokeStyle = pal.gold;
    ctx.lineWidth = 0.85;
    ctx.globalAlpha = 0.42;
    const inPad = 3.0;
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

    // 4. Cloud Curls on Wingtips with Gem Insets
    ctx.save();
    ctx.strokeStyle = pal.gold;
    ctx.lineWidth = 1.2;
    ctx.lineCap = 'round';
    ctx.shadowColor = pal.glow;
    ctx.shadowBlur = 4;

    // Left cloud curl
    ctx.beginPath();
    ctx.moveTo(-halfW + 3, -halfH + 3);
    ctx.quadraticCurveTo(-halfW - 6, -halfH - 2, -halfW - wingNotch - 3, 0);
    ctx.quadraticCurveTo(-halfW - 6, halfH + 2, -halfW + 3, halfH - 3);
    ctx.stroke();
    ctx.fillStyle = pal.gem;
    ctx.beginPath();
    ctx.arc(-halfW - 2, 0, isHero ? 2.5 : 2.0, 0, Math.PI * 2);
    ctx.fill();

    // Right cloud curl
    ctx.beginPath();
    ctx.moveTo(halfW - 3, -halfH + 3);
    ctx.quadraticCurveTo(halfW + 6, -halfH - 2, halfW + wingNotch + 3, 0);
    ctx.quadraticCurveTo(halfW + 6, halfH + 2, halfW - 3, halfH - 3);
    ctx.stroke();
    ctx.fillStyle = pal.gem;
    ctx.beginPath();
    ctx.arc(halfW + 2, 0, isHero ? 2.5 : 2.0, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();

    // 5. Top Crest Diamond & Bottom Knot Notch
    ctx.save();
    ctx.fillStyle = pal.gold;
    ctx.beginPath();
    ctx.moveTo(0, -halfH - (isHero ? 5 : 4));
    ctx.lineTo(isHero ? 4.5 : 3.5, -halfH);
    ctx.lineTo(0, -halfH + (isHero ? 4.5 : 3.5));
    ctx.lineTo(-(isHero ? 4.5 : 3.5), -halfH);
    ctx.closePath();
    ctx.fill();

    ctx.fillStyle = pal.gem;
    ctx.beginPath();
    ctx.arc(0, -halfH, isHero ? 2.0 : 1.5, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = pal.gold;
    ctx.beginPath();
    ctx.moveTo(-3, halfH);
    ctx.lineTo(0, halfH + (isHero ? 3.5 : 2.5));
    ctx.lineTo(3, halfH);
    ctx.closePath();
    ctx.fill();
    ctx.restore();
  }

  // 6. True Tiên Hiệp Handwritten Calligraphy Text
  ctx.save();
  ctx.font = isHero
    ? '700 15px "Charm", "Caveat", cursive'
    : '700 13.5px "Charm", "Caveat", cursive';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillStyle = isReal ? pal.text : 'rgba(148, 163, 184, 0.75)';
  if (isReal) {
    ctx.shadowColor = pal.glow;
    ctx.shadowBlur = isHero ? 7 : 4;
  }
  ctx.fillText(text, 0, 1);
  ctx.restore();

  ctx.restore();
}

// Background troupe (Tier 1 & 2 ambient shadows)
const AMBIENT_BOTS = [
  { id: 'b1', xNorm: 0.08, tier: 1, scale: 0.16, facing: 1, speed: 0.92, phase: 0.12, label: 'Tàn Ảnh #11' },
  { id: 'b2', xNorm: 0.19, tier: 1, scale: 0.16, facing: 1, speed: 1.08, phase: 0.45, label: 'Tàn Ảnh #12' },
  { id: 'b3', xNorm: 0.30, tier: 1, scale: 0.16, facing: 1, speed: 0.95, phase: 0.78, label: 'Tàn Ảnh #13' },
  { id: 'b4', xNorm: 0.41, tier: 1, scale: 0.16, facing: 1, speed: 1.15, phase: 0.23, label: 'Tàn Ảnh #14' },
  { id: 'b5', xNorm: 0.59, tier: 1, scale: 0.16, facing: -1, speed: 1.02, phase: 0.85, label: 'Tàn Ảnh #15' },
  { id: 'b6', xNorm: 0.70, tier: 1, scale: 0.16, facing: -1, speed: 1.12, phase: 0.38, label: 'Tàn Ảnh #16' },
  { id: 'b7', xNorm: 0.81, tier: 1, scale: 0.16, facing: -1, speed: 0.90, phase: 0.65, label: 'Tàn Ảnh #17' },
  { id: 'b8', xNorm: 0.92, tier: 1, scale: 0.16, facing: -1, speed: 1.20, phase: 0.19, label: 'Tàn Ảnh #18' },

  { id: 'b9', xNorm: 0.18, tier: 2, scale: 0.22, facing: 1, speed: 1.00, phase: 0.35, label: 'Tàn Ảnh #21' },
  { id: 'b10', xNorm: 0.30, tier: 2, scale: 0.22, facing: 1, speed: 1.18, phase: 0.68, label: 'Tàn Ảnh #22' },
  { id: 'b11', xNorm: 0.70, tier: 2, scale: 0.22, facing: -1, speed: 0.96, phase: 0.52, label: 'Tàn Ảnh #23' },
  { id: 'b12', xNorm: 0.82, tier: 2, scale: 0.22, facing: -1, speed: 1.05, phase: 0.91, label: 'Tàn Ảnh #24' },
];

// Tier 3: Frontline Peer Blacksmith Slots (Flanking Main Hero)
interface PeerSlotConfig {
  id: number;
  xNorm: number;
  yOffset: number;
  scale: number;
  facing: 1 | -1;
  speed: number;
  phase: number;
  isReal: boolean;
  name: string;
  stance: StanceKey;
}

const DEFAULT_PEER_SLOTS: PeerSlotConfig[] = [
  { id: 0, xNorm: 0.12, yOffset: 6, scale: 0.34, facing: 1, speed: 1.15, phase: 0.1, isReal: false, name: '', stance: 'Q' },
  { id: 1, xNorm: 0.24, yOffset: 2, scale: 0.35, facing: 1, speed: 0.95, phase: 0.35, isReal: false, name: '', stance: 'W' },
  { id: 2, xNorm: 0.36, yOffset: 0, scale: 0.36, facing: 1, speed: 1.05, phase: 0.7, isReal: false, name: '', stance: 'Q' },
  { id: 3, xNorm: 0.64, yOffset: 0, scale: 0.36, facing: -1, speed: 1.0, phase: 0.55, isReal: false, name: '', stance: 'R' },
  { id: 4, xNorm: 0.76, yOffset: 2, scale: 0.35, facing: -1, speed: 1.2, phase: 0.85, isReal: false, name: '', stance: 'E' },
  { id: 5, xNorm: 0.88, yOffset: 6, scale: 0.34, facing: -1, speed: 1.1, phase: 0.65, isReal: false, name: '', stance: 'W' },
];

export const CommunityPanoramicForgeCanvas = forwardRef<
  CommunityPanoramicForgeCanvasHandle,
  CommunityPanoramicForgeCanvasProps
>(function CommunityPanoramicForgeCanvas(
  {
    bossHp,
    bossMaxHp,
    activeStance,
    gameState,
    playerName = '',
    onHeroStrikeAction,
    onPeerAutonomousDamage,
    className = '',
  },
  ref
) {
  const containerRef = useRef<HTMLDivElement | null>(null);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  // Up-to-date refs for 60 FPS animation loop (no effect recreation)
  const bossHpRef = useRef<number>(bossHp);
  const bossMaxHpRef = useRef<number>(bossMaxHp);
  const activeStanceRef = useRef<StanceKey>(activeStance);
  const gameStateRef = useRef<string>(gameState);
  const playerNameRef = useRef<string>(playerName);
  const onHeroStrikeActionRef = useRef(onHeroStrikeAction);
  const onPeerAutonomousDamageRef = useRef(onPeerAutonomousDamage);

  bossHpRef.current = bossHp;
  bossMaxHpRef.current = bossMaxHp;
  activeStanceRef.current = activeStance;
  gameStateRef.current = gameState;
  playerNameRef.current = playerName;
  onHeroStrikeActionRef.current = onHeroStrikeAction;
  onPeerAutonomousDamageRef.current = onPeerAutonomousDamage;

  // Imperative hooks into canvas closure
  const executeHeroStrikeClosureRef = useRef<((forceGolden?: boolean) => void) | null>(null);
  const triggerPeerWaveClosureRef = useRef<(() => void) | null>(null);
  const spawnCombatTextClosureRef = useRef<
    ((text: string, subtext: string, color: string, glowColor: string, isGolden: boolean) => void) | null
  >(null);
  const resetClosureRef = useRef<(() => void) | null>(null);
  const triggerRemotePeerStrikeClosureRef = useRef<((payload: RemotePeerStrikePayload) => void) | null>(null);
  const updateRemotePeersClosureRef = useRef<((peers: RemotePeerInfo[]) => void) | null>(null);
  const spawnTouchRippleClosureRef = useRef<((x: number, y: number) => void) | null>(null);
  const lastTouchTimeRef = useRef<number>(0);

  useImperativeHandle(
    ref,
    () => ({
      triggerHeroStrike: (forceGolden = false) => {
        executeHeroStrikeClosureRef.current?.(forceGolden);
      },
      triggerPeerWave: () => {
        triggerPeerWaveClosureRef.current?.();
      },
      triggerRemotePeerStrike: (payload: RemotePeerStrikePayload) => {
        triggerRemotePeerStrikeClosureRef.current?.(payload);
      },
      updateRemotePeers: (peers: RemotePeerInfo[]) => {
        updateRemotePeersClosureRef.current?.(peers);
      },
      spawnCombatText: (text, subtext, color, glowColor, isGolden) => {
        spawnCombatTextClosureRef.current?.(text, subtext, color, glowColor, isGolden);
      },
      reset: () => {
        resetClosureRef.current?.();
      },
    }),
    []
  );

  const handleInteraction = useCallback((clientX?: number, clientY?: number) => {
    if (document.activeElement instanceof HTMLElement && document.activeElement !== document.body) {
      document.activeElement.blur();
    }
    if (typeof clientX === 'number' && typeof clientY === 'number' && containerRef.current) {
      const rect = containerRef.current.getBoundingClientRect();
      const x = clientX - rect.left;
      const y = clientY - rect.top;
      spawnTouchRippleClosureRef.current?.(x, y);
    }
    if (gameStateRef.current === 'playing' || gameStateRef.current === 'title') {
      onHeroStrikeActionRef.current?.(false);
    }
  }, []);

  const handleTouch = useCallback((e: React.TouchEvent) => {
    lastTouchTimeRef.current = performance.now();
    const touch = e.touches[0] || e.changedTouches[0];
    handleInteraction(touch?.clientX, touch?.clientY);
  }, [handleInteraction]);

  const handleClick = useCallback((e: React.MouseEvent) => {
    if (performance.now() - lastTouchTimeRef.current < 450) return;
    handleInteraction(e.clientX, e.clientY);
  }, [handleInteraction]);

  useEffect(() => {
    const canvas = canvasRef.current;
    const container = containerRef.current;
    if (!canvas || !container) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Load fonts
    if (document.fonts) {
      document.fonts.load('700 15px "Charm"');
      document.fonts.load('700 13.5px "Charm"');
      document.fonts.load('700 14px "Caveat"');
    }

    const base = import.meta.env.BASE_URL || './';
    const cleanBase = base.endsWith('/') ? base : base + '/';

    // -------------------------------------------------------------------------
    // ASSET LOADING
    // -------------------------------------------------------------------------
    interface AssetItem {
      src: string;
      img: HTMLImageElement;
      loaded: boolean;
    }

    const assets: Record<string, AssetItem> = {
      sky1: { src: `${cleanBase}assets/art/sky_states/sky_state_1_pristine.webp`, img: new Image(), loaded: false },
      sky2: { src: `${cleanBase}assets/art/sky_states/sky_state_2_incipient.webp`, img: new Image(), loaded: false },
      sky3: { src: `${cleanBase}assets/art/sky_states/sky_state_3_spreading.webp`, img: new Image(), loaded: false },
      sky4: { src: `${cleanBase}assets/art/sky_states/sky_state_4_severe.webp`, img: new Image(), loaded: false },
      sky5: { src: `${cleanBase}assets/art/sky_states/sky_state_5_cataclysm.webp`, img: new Image(), loaded: false },
      sky6: { src: `${cleanBase}assets/art/sky_states/sky_state_6_shattered.webp`, img: new Image(), loaded: false },
      moon: { src: `${cleanBase}assets/art/sky_celestial_moon.webp`, img: new Image(), loaded: false },
      aurora: { src: `${cleanBase}assets/art/sky_aurora_nebula.webp`, img: new Image(), loaded: false },
      clouds: { src: `${cleanBase}assets/art/sky_drifting_clouds.webp`, img: new Image(), loaded: false },
      mountains: { src: `${cleanBase}assets/art/bg_distant_mountains_clean.webp`, img: new Image(), loaded: false },
      pedestal: { src: `${cleanBase}assets/art/single_forger_pedestal.webp`, img: new Image(), loaded: false },
      mainAltar: { src: `${cleanBase}assets/art/altar_platform.webp`, img: new Image(), loaded: false },
      peerSheet: { src: `${cleanBase}assets/art/peer_blacksmith_strip.webp`, img: new Image(), loaded: false },
      peerShadowSheet: { src: `${cleanBase}assets/art/peer_blacksmith_shadow_strip.webp`, img: new Image(), loaded: false },
      heroSheet: { src: `${cleanBase}assets/art/hero_spritesheet_strip.webp`, img: new Image(), loaded: false },
    };

    Object.values(assets).forEach((asset) => {
      asset.img.onload = () => {
        asset.loaded = true;
      };
      asset.img.src = asset.src;
      if (asset.img.complete) {
        asset.loaded = true;
      }
    });

    let viewW = Math.max(320, container.clientWidth || window.innerWidth);
    let viewH = Math.max(320, container.clientHeight || window.innerHeight);

    const resizeCanvas = () => {
      if (!container || !canvas) return;
      viewW = Math.max(320, container.clientWidth || window.innerWidth);
      viewH = Math.max(320, container.clientHeight || window.innerHeight);
      if (canvas.width !== Math.floor(viewW) || canvas.height !== Math.floor(viewH)) {
        canvas.width = Math.floor(viewW);
        canvas.height = Math.floor(viewH);
      }
    };
    resizeCanvas();

    const ro = new ResizeObserver(resizeCanvas);
    ro.observe(container);

    // Mouse Parallax Tracking
    let targetMouseX = 0;
    let targetMouseY = 0;
    let currentMouseX = 0;
    let currentMouseY = 0;

    const handleMouseMove = (e: MouseEvent) => {
      const rect = container.getBoundingClientRect();
      const nx = ((e.clientX - rect.left) / viewW - 0.5) * 2;
      const ny = ((e.clientY - rect.top) / viewH - 0.5) * 2;
      targetMouseX = Math.max(-1, Math.min(1, nx));
      targetMouseY = Math.max(-1, Math.min(1, ny));
    };
    window.addEventListener('mousemove', handleMouseMove);

    // Stars field
    const stars: Array<{ x: number; y: number; size: number; baseAlpha: number; twinkleSpeed: number; phase: number }> = [];
    for (let i = 0; i < 110; i++) {
      stars.push({
        x: Math.random(),
        y: Math.random() * 0.65,
        size: 0.8 + Math.random() * 1.8,
        baseAlpha: 0.25 + Math.random() * 0.7,
        twinkleSpeed: 0.002 + Math.random() * 0.005,
        phase: Math.random() * Math.PI * 2,
      });
    }

    // Dynamic Peer Slots (6 frontline pedestals)
    const peerSlots: PeerSlotConfig[] = DEFAULT_PEER_SLOTS.map((s) => ({ ...s }));
    const peerStrikeTimers = new Float32Array(peerSlots.length).fill(-1);
    const lastImpactFlags = new Array(peerSlots.length).fill(false);

    // Remote Players Map
    const remotePeersMap = new Map<number, RemotePeerInfo>();

    // Timers & VFX
    let heroStrikeTimer = -1;
    let screenShake = 0;
    let flashIntensity = 0;
    let rhythmPhase = 0.72;
    let textIdCounter = 1;

    const lightningBolts: ActiveLightningBolt2D[] = [];
    const shockwaves: Shockwave2D[] = [];
    const floatingTexts: FloatingCombatText2D[] = [];

    interface TouchRipple2D {
      x: number;
      y: number;
      radius: number;
      maxRadius: number;
      alpha: number;
      color: string;
    }
    const touchRipples: TouchRipple2D[] = [];

    spawnTouchRippleClosureRef.current = (x: number, y: number) => {
      const currentStanceKey = activeStanceRef.current;
      const sect = STANCE_TO_SECT[currentStanceKey] || 'thunder';
      const sc = SECT_COLORS[sect] || SECT_COLORS.thunder;
      touchRipples.push({
        x,
        y,
        radius: 10,
        maxRadius: 65,
        alpha: 0.85,
        color: sc.glow,
      });
      hapticEngine.playStrike();
    };

    const sparkPool: SparkParticle2D[] = Array.from({ length: MAX_SPARK_POOL }, () => ({
      active: false,
      x: 0,
      y: 0,
      vx: 0,
      vy: 0,
      size: 2,
      color: '#FFD166',
      alpha: 1,
      age: 0,
      maxAge: 1,
      isAsh: false,
    }));
    let sparkCursor = 0;

    const spawnParticle = (
      x: number,
      y: number,
      vx: number,
      vy: number,
      size: number,
      color: string,
      maxAge: number,
      isAsh: boolean
    ) => {
      const p = sparkPool[sparkCursor];
      sparkCursor = (sparkCursor + 1) % MAX_SPARK_POOL;
      p.active = true;
      p.x = x;
      p.y = y;
      p.vx = vx;
      p.vy = vy;
      p.size = size;
      p.color = color;
      p.alpha = 1;
      p.age = 0;
      p.maxAge = maxAge;
      p.isAsh = isAsh;
    };

    const spawnLightningBolt = (targetX: number, targetY: number, color = '#00F0FF', power = 1.0) => {
      const startX = targetX + (Math.random() - 0.5) * 90;
      const startY = viewH * 0.08;
      const segments: Point2D[] = [];
      const steps = 7;
      let currX = startX;
      let currY = startY;
      segments.push({ x: currX, y: currY });

      for (let s = 1; s < steps; s++) {
        const frac = s / steps;
        const idealX = startX + (targetX - startX) * frac;
        const idealY = startY + (targetY - startY) * frac;
        currX = idealX + (Math.random() - 0.5) * 42;
        currY = idealY + (Math.random() - 0.5) * 22;
        segments.push({ x: currX, y: currY });
      }
      segments.push({ x: targetX, y: targetY });

      lightningBolts.push({
        segments,
        alpha: 1.0,
        decay: 3.2,
        color,
        lineWidth: 3.2 * power,
      });
    };

    const executeHeroStrikeVisuals = (forceGolden = false) => {
      const currentStanceKey = activeStanceRef.current;
      const sect = STANCE_TO_SECT[currentStanceKey] || 'thunder';
      const sc = SECT_COLORS[sect] || SECT_COLORS.thunder;

      heroStrikeTimer = 0;
      screenShake = forceGolden ? 13 : 8;
      flashIntensity = forceGolden ? 1.4 : 0.95;
      rhythmPhase = 0.05;

      const isPortrait = viewW < viewH;
      const groundY = isPortrait ? viewH * 0.65 : (viewH < 500 ? viewH * 0.81 : viewH * 0.825);
      const renderScale = isPortrait ? Math.min(0.48, Math.max(0.36, viewW / 760)) : 0.38;
      const centerX = viewW * 0.5;
      const heroFootX = centerX - 14;
      const spriteLeft = heroFootX - (360 * renderScale) * 0.46;
      const spriteTop = groundY - (440 * renderScale);
      const impactX = spriteLeft + 213 * renderScale;
      const impactY = spriteTop + 342 * renderScale;

      // 1. Lightning from sky to anvil
      spawnLightningBolt(impactX, impactY, sc.glow, 1.45);

      // 2. Shockwave
      shockwaves.push({
        x: impactX,
        y: impactY,
        radius: 10,
        maxRadius: 75,
        alpha: 1.0,
        color: sc.light,
      });

      // 3. Sparks
      const sparkCount = forceGolden ? 48 : 34;
      for (let i = 0; i < sparkCount; i++) {
        const ang = Math.PI * 1.5 + (Math.random() - 0.5) * 1.8;
        const spd = 120 + Math.random() * 260;
        spawnParticle(
          impactX,
          impactY,
          Math.cos(ang) * spd,
          Math.sin(ang) * spd,
          2.2 + Math.random() * 2.6,
          Math.random() < 0.35 ? '#FFFFFF' : sc.light,
          0.45 + Math.random() * 0.45,
          false
        );
      }
    };

    const spawnCombatTextInternal = (
      text: string,
      subtext: string,
      color: string,
      glowColor: string,
      isGolden: boolean
    ) => {
      const heroX = viewW * 0.5;
      const isPortrait = viewW < viewH;
      const groundY = isPortrait ? viewH * 0.65 : (viewH < 500 ? viewH * 0.81 : viewH * 0.825);

      floatingTexts.push({
        id: textIdCounter++,
        text,
        subtext,
        x: heroX,
        y: groundY - 175,
        vy: -68,
        color,
        glowColor,
        ageSec: 0,
        durationSec: 1.35,
        scale: isGolden ? 1.18 : 1.0,
      });
    };

    const resetSimulation = () => {
      heroStrikeTimer = -1;
      screenShake = 0;
      flashIntensity = 0;
      lightningBolts.length = 0;
      shockwaves.length = 0;
      floatingTexts.length = 0;
      for (const p of sparkPool) p.active = false;
    };

    executeHeroStrikeClosureRef.current = (forceGolden?: boolean) => {
      executeHeroStrikeVisuals(forceGolden);
    };

    triggerPeerWaveClosureRef.current = () => {
      peerSlots.forEach((slot, idx) => {
        peerStrikeTimers[idx] = 0;
        const px = slot.xNorm * viewW;
        const py = viewH * 0.825 + slot.yOffset;
        const sect = STANCE_TO_SECT[slot.stance] || 'thunder';
        spawnLightningBolt(px, py - 8, SECT_COLORS[sect].glow, 0.9);
      });
      screenShake = 10;
      flashIntensity = 0.9;
    };

    spawnCombatTextClosureRef.current = (text, subtext, color, glowColor, isGolden) => {
      spawnCombatTextInternal(text, subtext, color, glowColor, isGolden);
    };

    resetClosureRef.current = () => {
      resetSimulation();
    };

    updateRemotePeersClosureRef.current = (peers: RemotePeerInfo[]) => {
      remotePeersMap.clear();
      for (const p of peers) {
        remotePeersMap.set(p.slotIndex, p);
      }

      // Sync slot configs with real remote peers
      peerSlots.forEach((slot, idx) => {
        const rp = remotePeersMap.get(idx);
        if (rp) {
          slot.isReal = true;
          slot.name = `★ ${rp.name}`;
          slot.stance = rp.stance;
        } else {
          // Keep default empty bot slot
          slot.isReal = false;
          slot.name = '';
          slot.stance = DEFAULT_PEER_SLOTS[idx].stance;
        }
      });
    };

    triggerRemotePeerStrikeClosureRef.current = (payload: RemotePeerStrikePayload) => {
      const slotIdx = payload.slotIndex;
      if (slotIdx >= 0 && slotIdx < peerSlots.length) {
        peerStrikeTimers[slotIdx] = 0;
        const slot = peerSlots[slotIdx];
        const px = slot.xNorm * viewW;
        const py = viewH * 0.825 + slot.yOffset;
        const sect = STANCE_TO_SECT[payload.stance] || 'thunder';
        const sc = SECT_COLORS[sect] || SECT_COLORS.thunder;

        spawnLightningBolt(px + (slot.facing === 1 ? 14 : -14), py - 8, sc.glow, 0.95);

        for (let i = 0; i < 8; i++) {
          const ang = Math.PI * 1.5 + (Math.random() - 0.5) * 1.6;
          const spd = 80 + Math.random() * 160;
          spawnParticle(
            px + (slot.facing === 1 ? 14 : -14),
            py - 8,
            Math.cos(ang) * spd,
            Math.sin(ang) * spd,
            1.8,
            sc.spark,
            0.4,
            false
          );
        }
      }
    };

    // Debug API
    const debugApi = {
      strike: (forceGolden = true) => executeHeroStrikeVisuals(forceGolden),
      triggerPeerWave: () => triggerPeerWaveClosureRef.current?.(),
      reset: () => resetSimulation(),
      getStats: () => ({
        rendererType: 'HTML5_CANVAS_2D_PANORAMA',
        skyRatio: PANORAMA_SKY_RATIO,
        gameState: gameStateRef.current,
        activeStance: activeStanceRef.current,
        peerCount: peerSlots.length,
        floatingTextsCount: floatingTexts.length,
      }),
    };
    (window as unknown as Record<string, unknown>).__celestialForge = debugApi;

    // -------------------------------------------------------------------------
    // MAIN RENDER LOOP (60 FPS)
    // -------------------------------------------------------------------------
    let animFrameId = 0;
    let lastPerfTime = performance.now();

    const render = (now: number) => {
      try {
        const dt = Math.min((now - lastPerfTime) / 1000, 0.05);
        lastPerfTime = now;

        const isPaused = gameStateRef.current === 'paused';
        if (!isPaused) {
          // Smooth mouse parallax lerp
          currentMouseX += (targetMouseX - currentMouseX) * 0.05;
          currentMouseY += (targetMouseY - currentMouseY) * 0.05;

          // Screen shake decay
          if (screenShake > 0) {
            screenShake = Math.max(0, screenShake - 26 * dt);
          }
          if (flashIntensity > 0) {
            flashIntensity = Math.max(0, flashIntensity - 3.4 * dt);
          }

          // Rhythm phase (100 BPM)
          rhythmPhase = (rhythmPhase + dt * (100 / 60)) % 1.0;

          // Hero strike timer
          if (heroStrikeTimer >= 0) {
            heroStrikeTimer += dt;
            if (heroStrikeTimer > HERO_STRIKE_TOTAL_SEC) {
              heroStrikeTimer = -1;
            }
          }

          // Peer strike timers
          for (let i = 0; i < peerStrikeTimers.length; i++) {
            if (peerStrikeTimers[i] >= 0) {
              peerStrikeTimers[i] += dt;
              if (peerStrikeTimers[i] > HERO_STRIKE_TOTAL_SEC) {
                peerStrikeTimers[i] = -1;
              }
            }
          }

          // Autonomous peer strikes for bots
          if (gameStateRef.current === 'playing' && bossHpRef.current > 0) {
            peerSlots.forEach((slot, idx) => {
              if (remotePeersMap.has(idx)) return; // Real players don't auto-strike

              const cycleTime = 1.05 / slot.speed;
              const cycleSec = (now * 0.001 + slot.phase * 10) % cycleTime;
              const progress = cycleSec / cycleTime;
              const isImpactFrame = progress >= 0.60 && progress < 0.78;

              if (isImpactFrame && !lastImpactFlags[idx]) {
                lastImpactFlags[idx] = true;
                const px = slot.xNorm * viewW - currentMouseX * 52;
                const py = viewH * 0.825 + slot.yOffset - currentMouseY * 14;
                const impactX = px + (slot.facing === 1 ? 14 : -14);
                const impactY = py - 8;
                const sect = STANCE_TO_SECT[slot.stance] || 'thunder';

                if (slot.isReal) {
                  spawnLightningBolt(impactX, impactY, SECT_COLORS[sect].glow, 0.9);
                }

                for (let s = 0; s < (slot.isReal ? 8 : 4); s++) {
                  const ang = Math.PI * 1.5 + (Math.random() - 0.5) * 1.6;
                  const spd = 60 + Math.random() * 120;
                  spawnParticle(
                    impactX,
                    impactY,
                    Math.cos(ang) * spd,
                    Math.sin(ang) * spd,
                    slot.isReal ? 2.0 : 1.3,
                    slot.isReal ? SECT_COLORS[sect].spark : '#94A3B8',
                    0.35,
                    false
                  );
                }

                // Autonomous peer chip damage
                if (Math.random() < 0.15) {
                  onPeerAutonomousDamageRef.current?.(1);
                }
              } else if (!isImpactFrame) {
                lastImpactFlags[idx] = false;
              }
            });
          }

          // Lightning bolts decay
          for (let i = lightningBolts.length - 1; i >= 0; i--) {
            const bolt = lightningBolts[i];
            bolt.alpha -= bolt.decay * dt;
            if (bolt.alpha <= 0) {
              lightningBolts.splice(i, 1);
            }
          }

          // Shockwaves decay
          for (let i = shockwaves.length - 1; i >= 0; i--) {
            const sw = shockwaves[i];
            sw.radius += 140 * dt;
            sw.alpha -= 1.9 * dt;
            if (sw.alpha <= 0 || sw.radius >= sw.maxRadius) {
              shockwaves.splice(i, 1);
            }
          }

          // Sparks physics
          const groundBounceY = viewH * 0.835;
          for (let i = 0; i < MAX_SPARK_POOL; i++) {
            const p = sparkPool[i];
            if (!p.active) continue;
            p.age += dt;
            if (p.age >= p.maxAge) {
              p.active = false;
              continue;
            }
            p.vy += 620 * dt;
            p.x += p.vx * dt;
            p.y += p.vy * dt;
            if (p.y >= groundBounceY && p.vy > 0) {
              p.y = groundBounceY;
              p.vy = -p.vy * 0.38;
              p.vx *= 0.75;
            }
            p.alpha = 1 - p.age / p.maxAge;
          }

          // Floating texts
          for (let i = floatingTexts.length - 1; i >= 0; i--) {
            const ft = floatingTexts[i];
            ft.ageSec += dt;
            ft.y += ft.vy * dt;
            ft.vy *= 0.94;
            if (ft.ageSec >= ft.durationSec) {
              floatingTexts.splice(i, 1);
            }
          }
        }

        // =====================================================================
        // CANVAS DRAWING PIPELINE
        // =====================================================================
        ctx.clearRect(0, 0, viewW, viewH);
        ctx.save();

        // Screen Shake
        if (screenShake > 0) {
          const sx = (Math.random() - 0.5) * screenShake;
          const sy = (Math.random() - 0.5) * screenShake;
          ctx.translate(sx, sy);
        }

        const isPortrait = viewW < viewH;
        const groundY = isPortrait ? viewH * 0.65 : (viewH < 500 ? viewH * 0.81 : viewH * 0.825);
        const renderScale = isPortrait ? Math.min(0.48, Math.max(0.36, viewW / 760)) : 0.38;
        const centerX = viewW * 0.5;

        // Determine current Sky State (1 to 6) from bossHp
        const hpFrac = Math.max(0, Math.min(1, bossHpRef.current / (bossMaxHpRef.current || 1)));
        const crackPct = 1 - hpFrac;
        let skyState = 1;
        if (crackPct >= 0.95 || bossHpRef.current <= 0) skyState = 6;
        else if (crackPct >= 0.75) skyState = 5;
        else if (crackPct >= 0.55) skyState = 4;
        else if (crackPct >= 0.35) skyState = 3;
        else if (crackPct >= 0.15) skyState = 2;
        else skyState = 1;

        // ---------------------------------------------------------------------
        // LAYER 0: CELESTIAL BACKGROUND GRADIENT
        // ---------------------------------------------------------------------
        const gradSky = ctx.createLinearGradient(0, 0, 0, viewH);
        if (skyState === 1 || skyState === 2) {
          gradSky.addColorStop(0, '#020409');
          gradSky.addColorStop(0.42, '#060B18');
          gradSky.addColorStop(0.75, '#0A1224');
          gradSky.addColorStop(1, '#020408');
        } else if (skyState === 3) {
          gradSky.addColorStop(0, '#07030F');
          gradSky.addColorStop(0.42, '#150B28');
          gradSky.addColorStop(0.75, '#1E1236');
          gradSky.addColorStop(1, '#07040C');
        } else if (skyState === 4) {
          gradSky.addColorStop(0, '#120404');
          gradSky.addColorStop(0.40, '#220808');
          gradSky.addColorStop(0.75, '#2F0E0E');
          gradSky.addColorStop(1, '#080202');
        } else if (skyState === 5) {
          gradSky.addColorStop(0, '#1C0404');
          gradSky.addColorStop(0.38, '#3A0808');
          gradSky.addColorStop(0.75, '#481010');
          gradSky.addColorStop(1, '#100303');
        } else {
          gradSky.addColorStop(0, '#260804');
          gradSky.addColorStop(0.35, '#4D1204');
          gradSky.addColorStop(0.70, '#5C1808');
          gradSky.addColorStop(1, '#150502');
        }
        ctx.fillStyle = gradSky;
        ctx.fillRect(0, 0, viewW, viewH);

        // Twinkling Celestial Stars
        stars.forEach((s) => {
          const a = s.baseAlpha + Math.sin(now * s.twinkleSpeed + s.phase) * 0.25;
          ctx.fillStyle = `rgba(224, 242, 254, ${Math.max(0, Math.min(1, a))})`;
          ctx.beginPath();
          ctx.arc(s.x * viewW, s.y * viewH, s.size, 0, Math.PI * 2);
          ctx.fill();
        });

        // ---------------------------------------------------------------------
        // LAYER 1: CELESTIAL JADE MOON
        // ---------------------------------------------------------------------
        if (assets.moon.loaded) {
          const mImg = assets.moon.img;
          const moonSize = Math.min(220, viewW * 0.20);
          const moonX = viewW * 0.74 - currentMouseX * 10;
          const moonY = viewH * 0.07 - currentMouseY * 5;

          ctx.save();
          ctx.globalCompositeOperation = 'screen';
          ctx.globalAlpha = skyState >= 5 ? 0.35 : 0.95;
          ctx.drawImage(mImg, moonX, moonY, moonSize, moonSize);
          ctx.restore();
        }

        // ---------------------------------------------------------------------
        // LAYER 2: AURORA NEBULA
        // ---------------------------------------------------------------------
        if (assets.aurora.loaded) {
          const aImg = assets.aurora.img;
          const aW = viewW * 1.05;
          const aH = aW * (aImg.height / aImg.width);
          const aX = (viewW - aW) * 0.5 - currentMouseX * 14;
          const aY = viewH * 0.04 - currentMouseY * 6;

          ctx.save();
          ctx.globalCompositeOperation = 'screen';
          ctx.globalAlpha = 0.55 + Math.sin(now * 0.002) * 0.15 + flashIntensity * 0.3;
          ctx.drawImage(aImg, aX, aY, aW, aH);
          ctx.restore();
        }

        // ---------------------------------------------------------------------
        // LAYER 3: 6 SKY STATES (MÁI VÒM THIÊN GIỚI NỨT VỠ -> TAN BIẾN)
        // ---------------------------------------------------------------------
        const skyKey = `sky${skyState}`;
        const activeSkyAsset = assets[skyKey];
        if (activeSkyAsset && activeSkyAsset.loaded && skyState > 1) {
          const sImg = activeSkyAsset.img;
          const pX = currentMouseX * 18;
          const pY = currentMouseY * 7;
          const sW = viewW * 0.95;
          const sH = sW * (sImg.height / sImg.width);
          const sX = (viewW - sW) * 0.5 - pX;
          const sY = viewH * 0.02 - pY;

          ctx.save();
          ctx.globalCompositeOperation = 'screen';
          const pulse = 0.85 + Math.sin(now * 0.005) * 0.15;
          ctx.globalAlpha = Math.min(1, pulse + flashIntensity * 0.4);
          ctx.drawImage(sImg, sX, sY, sW, sH);
          ctx.restore();
        }

        // ---------------------------------------------------------------------
        // LAYER 4: DRIFTING INKY CLOUDS
        // ---------------------------------------------------------------------
        if (assets.clouds.loaded) {
          const clImg = assets.clouds.img;
          const clW = viewW * 1.15;
          const clH = clW * (clImg.height / clImg.width);
          const clX = (viewW - clW) * 0.5 - currentMouseX * 20;
          const clY = viewH * 0.28 - currentMouseY * 6;

          ctx.save();
          ctx.globalCompositeOperation = 'screen';
          ctx.globalAlpha = 0.22;
          ctx.drawImage(clImg, clX, clY, clW, clH);
          ctx.restore();
        }

        // ---------------------------------------------------------------------
        // LAYER 5: BASALT HORIZON RIDGE (64% HEIGHT)
        // ---------------------------------------------------------------------
        const horizonY = viewH * 0.64;

        // Sương mù chân trời
        const mistGrad = ctx.createLinearGradient(0, horizonY - 45, 0, horizonY + 20);
        mistGrad.addColorStop(0, 'rgba(4, 7, 18, 0)');
        mistGrad.addColorStop(0.6, 'rgba(12, 18, 36, 0.45)');
        mistGrad.addColorStop(1, 'rgba(7, 10, 20, 0.85)');
        ctx.fillStyle = mistGrad;
        ctx.fillRect(0, horizonY - 45, viewW, 65);

        // Dãy núi Basalt xa
        ctx.save();
        const paraRidgeX = currentMouseX * 18;
        ctx.fillStyle = '#060914';
        ctx.strokeStyle = skyState >= 5 ? 'rgba(239, 68, 68, 0.65)' : 'rgba(255, 120, 30, 0.45)';
        ctx.lineWidth = 1.6;
        ctx.beginPath();
        ctx.moveTo(-50, horizonY + 25);
        const ridgeSteps = 32;
        for (let r = 0; r <= ridgeSteps; r++) {
          const rx = (r / ridgeSteps) * (viewW + 100) - 50 - paraRidgeX;
          const peak = Math.sin(r * 1.5 + 0.4) * 16 + Math.cos(r * 2.8) * 10;
          ctx.lineTo(rx, horizonY - Math.abs(peak));
        }
        ctx.lineTo(viewW + 50, horizonY + 45);
        ctx.lineTo(-50, horizonY + 45);
        ctx.closePath();
        ctx.fill();
        ctx.stroke();
        ctx.restore();

        // ---------------------------------------------------------------------
        // LAYER 6: 3 STEPPED BASALT TERRACES (0.685, 0.750, 0.825)
        // ---------------------------------------------------------------------
        const activeSect = STANCE_TO_SECT[activeStanceRef.current] || 'thunder';
        const activeSectColor = SECT_COLORS[activeSect] || SECT_COLORS.thunder;

        const terraceLevels = [
          { y: viewH * 0.685, h: viewH * 0.065, color1: '#0B1122', color2: '#050812', stroke: 'rgba(124, 232, 255, 0.22)', lw: 1.2 },
          { y: viewH * 0.750, h: viewH * 0.075, color1: '#0E162B', color2: '#060914', stroke: 'rgba(124, 232, 255, 0.35)', lw: 1.5 },
          { y: viewH * 0.825, h: viewH * 0.180, color1: '#121D38', color2: '#070B18', stroke: activeSectColor.glow, lw: 2.2 },
        ];

        terraceLevels.forEach((tl, tIdx) => {
          const pX = currentMouseX * (22 + tIdx * 14);
          const ty = tl.y - currentMouseY * (5 + tIdx * 3);

          ctx.save();
          const gradT = ctx.createLinearGradient(0, ty, 0, ty + tl.h);
          gradT.addColorStop(0, tl.color1);
          gradT.addColorStop(1, tl.color2);
          ctx.fillStyle = gradT;

          ctx.beginPath();
          ctx.moveTo(0, ty);
          for (let s = 0; s <= 20; s++) {
            const sx = (s / 20) * viewW;
            const dip = s >= 8 && s <= 12 ? 4 : s % 2 === 0 ? -2 : 2;
            ctx.lineTo(sx - pX, ty + dip);
          }
          ctx.lineTo(viewW, ty + tl.h);
          ctx.lineTo(0, ty + tl.h);
          ctx.closePath();
          ctx.fill();

          ctx.strokeStyle = tl.stroke;
          ctx.lineWidth = tl.lw;
          ctx.shadowColor = tl.stroke;
          ctx.shadowBlur = tIdx === 2 ? 14 : 6;
          ctx.beginPath();
          for (let s = 0; s <= 20; s++) {
            const sx = (s / 20) * viewW;
            const dip = s >= 8 && s <= 12 ? 4 : s % 2 === 0 ? -2 : 2;
            if (s === 0) ctx.moveTo(sx - pX, ty + dip);
            else ctx.lineTo(sx - pX, ty + dip);
          }
          ctx.stroke();
          ctx.restore();
        });

        // ---------------------------------------------------------------------
        // LAYER 7: AMBIENT SHADOW TROUPE (TIER 1 & 2)
        // ---------------------------------------------------------------------
        if (assets.peerShadowSheet.loaded) {
          const sheetShadow = assets.peerShadowSheet.img;
          const FW = 458;
          const FH = 384;

          AMBIENT_BOTS.forEach((bot) => {
            const tLevel = bot.tier === 1 ? terraceLevels[0] : terraceLevels[1];
            const tY = tLevel.y - currentMouseY * (bot.tier === 1 ? 5 : 8);
            const pX = currentMouseX * (bot.tier === 1 ? 26 : 38);
            const bx = bot.xNorm * viewW - pX;
            const by = tY + (bot.tier === 1 ? 22 : 28);

            const cycleTime = 1.05 / bot.speed;
            const cycleSec = (now * 0.001 + bot.phase * 10) % cycleTime;
            const progress = cycleSec / cycleTime;
            let bFrame = 0;
            if (progress < 0.20) bFrame = 0;
            else if (progress < 0.42) bFrame = 1;
            else if (progress < 0.60) bFrame = 2;
            else if (progress < 0.78) bFrame = 3;
            else if (progress < 0.90) bFrame = 4;
            else bFrame = 5;

            const bw = FW * bot.scale;
            const bh = FH * bot.scale;

            // Mini anvil
            ctx.save();
            ctx.fillStyle = '#1E293B';
            ctx.strokeStyle = '#334155';
            ctx.lineWidth = 1.0;
            const anvilX = bx + (bot.facing === 1 ? 8 : -8);
            ctx.beginPath();
            ctx.roundRect(anvilX - 9, by - 6, 18, 8, 2);
            ctx.fill();
            ctx.stroke();
            ctx.restore();

            // Sprite
            ctx.save();
            ctx.translate(bx, by);
            if (bot.facing === -1) ctx.scale(-1, 1);
            ctx.globalAlpha = bot.tier === 1 ? 0.45 : 0.60;
            const sx = bFrame * FW;
            ctx.drawImage(sheetShadow, sx, 0, FW, FH, -bw * 0.42, -bh + 6, bw, bh);
            ctx.restore();

            // (Ambient handwriting label omitted to maintain clean terrace view)
          });
        }

        // ---------------------------------------------------------------------
        // LAYER 8: FRONTLINE PEDESTALS (SINGLE FORGER PEDESTALS)
        // ---------------------------------------------------------------------
        if (assets.pedestal.loaded) {
          const pedImg = assets.pedestal.img;
          peerSlots.forEach((slot) => {
            const paraX = currentMouseX * 52;
            const paraY = currentMouseY * 14;
            const px = slot.xNorm * viewW - paraX;
            const py = groundY + slot.yOffset - paraY;

            const pedW = 160 * (slot.scale / 0.35);
            const pedH = pedW * (pedImg.height / pedImg.width);

            // Shadow
            ctx.save();
            ctx.fillStyle = 'rgba(0,0,0,0.7)';
            ctx.filter = 'blur(10px)';
            ctx.beginPath();
            ctx.ellipse(px, py + pedH * 0.35, pedW * 0.45, 12, 0, 0, Math.PI * 2);
            ctx.fill();
            ctx.restore();

            // Pedestal Image
            ctx.save();
            ctx.drawImage(pedImg, px - pedW * 0.5, py - pedH * 0.28, pedW, pedH);

            // Sect Rune Glow
            if (slot.isReal) {
              const sect = STANCE_TO_SECT[slot.stance] || 'thunder';
              const sc = SECT_COLORS[sect] || SECT_COLORS.thunder;
              ctx.globalAlpha = 0.45 + Math.sin(now * 0.004 + slot.id) * 0.15;
              ctx.filter = 'blur(10px)';
              ctx.fillStyle = sc.glow;
              ctx.beginPath();
              ctx.ellipse(px, py - 4, pedW * 0.3, 8, 0, 0, Math.PI * 2);
              ctx.fill();
            }
            ctx.restore();
          });
        }

        // ---------------------------------------------------------------------
        // LAYER 9: FRONTLINE PEER BLACKSMITHS (ANIMATED 6-FRAME)
        // ---------------------------------------------------------------------
        if (assets.peerSheet.loaded && assets.peerShadowSheet.loaded) {
          const sheetColor = assets.peerSheet.img;
          const sheetShadow = assets.peerShadowSheet.img;
          const PEER_FW = 458;
          const PEER_FH = 384;

          peerSlots.forEach((slot) => {
            const cycleTime = 1.05 / slot.speed;
            const cycleSec = (now * 0.001 + slot.phase * 10) % cycleTime;
            const progress = cycleSec / cycleTime;

            let pFrame = 0;
            if (progress < 0.20) pFrame = 0;
            else if (progress < 0.42) pFrame = 1;
            else if (progress < 0.60) pFrame = 2;
            else if (progress < 0.78) pFrame = 3;
            else if (progress < 0.90) pFrame = 4;
            else pFrame = 5;

            const paraX = currentMouseX * 52;
            const paraY = currentMouseY * 14;
            const px = slot.xNorm * viewW - paraX;
            const py = groundY + slot.yOffset - paraY;

            const pScale = slot.scale;
            const pw = PEER_FW * pScale;
            const ph = PEER_FH * pScale;

            ctx.save();
            ctx.translate(px, py);
            if (slot.facing === -1) {
              ctx.scale(-1, 1);
            }

            const activeImg = slot.isReal ? sheetColor : sheetShadow;
            ctx.globalAlpha = slot.isReal ? 1.0 : 0.45;

            const sx = pFrame * PEER_FW;
            const sy = 0;
            ctx.drawImage(activeImg, sx, sy, PEER_FW, PEER_FH, -pw * 0.42, -ph + 12, pw, ph);
            ctx.restore();

            // Tiên Hiệp Plaque Nameplate (Charm / Caveat Calligraphy) - Only for real connected remote peers
            if (slot.isReal && slot.name && slot.name.trim()) {
              const nameY = py - ph + 4;
              drawXianxiaPlaque(ctx, px, nameY, slot.name, slot.stance, false, slot.isReal);
            }
          });
        }

        // ---------------------------------------------------------------------
        // LAYER 10: CENTRAL ALTAR PLATFORM (MAIN HERO)
        // ---------------------------------------------------------------------
        if (assets.mainAltar.loaded) {
          const aImg = assets.mainAltar.img;
          const aW = isPortrait ? Math.min(260, viewW * 0.58) : Math.min(270, viewW * 0.25);
          const aH = aW * (aImg.height / aImg.width);
          const aX = centerX - aW * 0.5 - currentMouseX * 56;
          const aY = groundY - aH * 0.22 - currentMouseY * 16;

          // Shadow
          ctx.save();
          ctx.fillStyle = 'rgba(0, 0, 0, 0.9)';
          ctx.filter = 'blur(16px)';
          ctx.beginPath();
          ctx.ellipse(centerX - currentMouseX * 56, groundY + aH * 0.30, aW * 0.45, 14, 0, 0, Math.PI * 2);
          ctx.fill();
          ctx.restore();

          // Altar Image
          ctx.save();
          ctx.drawImage(aImg, aX, aY, aW, aH);

          // Central Rune Pool
          const runeColor = activeSectColor.glow;
          const runePulse = 0.35 + Math.sin(now * 0.003) * 0.15 + flashIntensity * 0.45;
          ctx.globalAlpha = runePulse;
          ctx.filter = 'blur(12px)';
          ctx.fillStyle = runeColor;
          ctx.beginPath();
          ctx.ellipse(centerX - currentMouseX * 56, groundY - 2 - currentMouseY * 16, aW * 0.26, 10, 0, 0, Math.PI * 2);
          ctx.fill();
          ctx.restore();
        }

        // ---------------------------------------------------------------------
        // LAYER 11: MAIN HERO (BALANCED 0.38 SCALE, EQUAL PROMINENCE)
        // ---------------------------------------------------------------------
        if (assets.heroSheet.loaded) {
          const sheet = assets.heroSheet.img;
          const stageFootY = groundY - currentMouseY * 18;
          const heroFootX = centerX - 14 - currentMouseX * 64;

          const FRAME_W = 360;
          const FRAME_H = 480;
          const dw = FRAME_W * renderScale;
          const dh = FRAME_H * renderScale;
          const baseLineY = 440 * renderScale;

          // Action frame mapping
          let heroFrameIdx = 0;
          if (heroStrikeTimer >= 0) {
            const p = Math.min(1, heroStrikeTimer / HERO_STRIKE_TOTAL_SEC);
            if (p < 0.18) heroFrameIdx = 1;
            else if (p < 0.38) heroFrameIdx = 2;
            else if (p < 0.62) heroFrameIdx = 3;
            else if (p < 0.82) heroFrameIdx = 4;
            else heroFrameIdx = 5;
          }

          const sx = heroFrameIdx * FRAME_W;
          const sy = 0;
          const spriteLeft = heroFootX - dw * 0.46;
          const spriteTop = stageFootY - baseLineY;

          // Hero Shadow
          ctx.save();
          ctx.fillStyle = 'rgba(0, 0, 0, 0.8)';
          ctx.filter = 'blur(6px)';
          ctx.beginPath();
          ctx.ellipse(heroFootX - 16, stageFootY + 2, 26, 8, 0, 0, Math.PI * 2);
          ctx.fill();
          ctx.beginPath();
          ctx.ellipse(heroFootX + 32, stageFootY + 3, 30, 9, 0, 0, Math.PI * 2);
          ctx.fill();
          ctx.restore();

          // Forge Aura Ring
          ctx.save();
          ctx.strokeStyle = activeSectColor.glow;
          ctx.lineWidth = 1.6;
          ctx.globalAlpha = 0.55 + Math.sin(now * 0.004) * 0.2;
          ctx.beginPath();
          ctx.ellipse(heroFootX + 8, stageFootY, 62, 14, 0, 0, Math.PI * 2);
          ctx.stroke();
          ctx.restore();

          // Hero Sprite
          ctx.save();
          if (heroFrameIdx === 3) {
            ctx.shadowColor = activeSectColor.light;
            ctx.shadowBlur = 25;
          }
          ctx.drawImage(sheet, sx, sy, FRAME_W, FRAME_H, spriteLeft, spriteTop, dw, dh);
          ctx.restore();

          // Contracting Rhythm Ring (100 BPM) on Hero Anvil
          const anvilImpactX = spriteLeft + 213 * renderScale;
          const anvilImpactY = spriteTop + 342 * renderScale;
          const ringScale = 1 - rhythmPhase;
          const isSweetSpot = Math.abs(rhythmPhase - 0.78) <= 0.18;

          ctx.save();
          ctx.strokeStyle = isSweetSpot ? '#FFD166' : activeSectColor.glow;
          ctx.lineWidth = isSweetSpot ? 2.6 : 1.5;
          ctx.globalAlpha = 0.35 + rhythmPhase * 0.55;
          ctx.beginPath();
          ctx.ellipse(
            anvilImpactX,
            anvilImpactY,
            14 + ringScale * 38,
            5 + ringScale * 14,
            0,
            0,
            Math.PI * 2
          );
          ctx.stroke();
          ctx.restore();

          // Balanced Overhead Plaque (Charm / Caveat Calligraphy)
          const stanceMeta = HERO_STANCE_PALETTES[activeStanceRef.current] || HERO_STANCE_PALETTES.Q;
          const heroName = playerNameRef.current.trim() || 'Thợ Rèn Chính';
          const labelText = `${heroName} · [${stanceMeta.nameVn}]`;
          const tagY = stageFootY - 140;
          drawXianxiaPlaque(ctx, centerX - currentMouseX * 64, tagY, labelText, activeStanceRef.current, true, true);
        }

        // ---------------------------------------------------------------------
        // LAYER 12: DYNAMIC LIGHTNING BOLTS
        // ---------------------------------------------------------------------
        for (let i = lightningBolts.length - 1; i >= 0; i--) {
          const bolt = lightningBolts[i];
          ctx.save();
          ctx.globalAlpha = Math.max(0, bolt.alpha);
          ctx.strokeStyle = '#FFFFFF';
          ctx.lineWidth = bolt.lineWidth;
          ctx.shadowColor = bolt.color;
          ctx.shadowBlur = 22;

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

        // ---------------------------------------------------------------------
        // LAYER 13: SHOCKWAVES & SPARKS
        // ---------------------------------------------------------------------
        for (let i = shockwaves.length - 1; i >= 0; i--) {
          const sw = shockwaves[i];
          ctx.save();
          ctx.globalAlpha = Math.max(0, sw.alpha);
          ctx.strokeStyle = sw.color;
          ctx.lineWidth = 2.4 * sw.alpha;
          ctx.beginPath();
          ctx.ellipse(sw.x, sw.y, sw.radius, sw.radius * 0.45, 0, 0, Math.PI * 2);
          ctx.stroke();
          ctx.restore();
        }

        ctx.save();
        for (let i = 0; i < MAX_SPARK_POOL; i++) {
          const p = sparkPool[i];
          if (!p.active || p.alpha <= 0.02) continue;

          ctx.globalAlpha = Math.max(0, Math.min(1, p.alpha));
          ctx.fillStyle = p.color;
          ctx.beginPath();
          ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
          ctx.fill();
        }
        ctx.restore();

        // ---------------------------------------------------------------------
        // LAYER 14: FLOATING COMBAT TEXT
        // ---------------------------------------------------------------------
        for (let i = 0; i < floatingTexts.length; i++) {
          const ft = floatingTexts[i];
          const prog = ft.ageSec / ft.durationSec;
          const alpha = prog < 0.7 ? 1 : 1 - (prog - 0.7) / 0.3;
          const popScale =
            prog < 0.14
              ? ft.scale * (0.7 + (prog / 0.14) * 0.45)
              : ft.scale * (1.15 - prog * 0.15);

          ctx.save();
          ctx.translate(ft.x, ft.y);
          ctx.scale(popScale, popScale);
          ctx.globalAlpha = Math.max(0, Math.min(1, alpha));
          ctx.textAlign = 'center';
          ctx.textBaseline = 'middle';

          ctx.font = '700 24px "Cinzel", serif';
          ctx.lineWidth = 5;
          ctx.strokeStyle = '#050811';
          ctx.strokeText(ft.text, 0, 0);
          ctx.fillStyle = ft.color;
          ctx.fillText(ft.text, 0, 0);

          ctx.font = '700 13px "Charm", "Caveat", cursive';
          ctx.lineWidth = 3;
          ctx.strokeText(ft.subtext, 0, 22);
          ctx.fillStyle = '#F8FAFC';
          ctx.fillText(ft.subtext, 0, 22);
          ctx.restore();
        }

        ctx.restore();
      } catch (err) {
        console.error('Community panoramic render error:', err);
      } finally {
        animFrameId = requestAnimationFrame(render);
      }
    };

    render(performance.now());

    return () => {
      cancelAnimationFrame(animFrameId);
      ro.disconnect();
      window.removeEventListener('mousemove', handleMouseMove);
    };
  }, []);

  return (
    <div
      ref={containerRef}
      tabIndex={0}
      onTouchStart={handleTouch}
      onClick={handleClick}
      onKeyDown={(e) => {
        const isSpace =
          e.code === 'Space' ||
          e.key === ' ' ||
          e.key === 'Spacebar' ||
          e.keyCode === 32 ||
          e.which === 32;
        const isQ = e.code === 'KeyQ' || e.key === 'q' || e.key === 'Q';
        if (isSpace || isQ) {
          e.preventDefault();
          e.stopPropagation();
          onHeroStrikeActionRef.current?.(false);
        }
      }}
      className={`relative w-full h-full overflow-hidden select-none outline-none ${className}`}
    >
      <canvas
        ref={canvasRef}
        data-testid="panoramic-2d-canvas"
        tabIndex={0}
        onTouchStart={handleTouch}
        onClick={handleClick}
        className="block w-full h-full cursor-pointer outline-none"
      />
    </div>
  );
});
