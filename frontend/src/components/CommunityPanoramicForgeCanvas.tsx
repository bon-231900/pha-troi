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
  createPeerBlacksmithTroupe,
  generate2DLightningBolt,
  evaluateHero2DStrikePose,
  createSkyVaultCrackTree,
  type StanceKey,
  type PeerBlacksmithActor,
  type Point2D,
} from '../game/rules';

export interface CommunityPanoramicForgeCanvasHandle {
  triggerHeroStrike: (forceGolden?: boolean) => void;
  triggerPeerWave: () => void;
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
  onHeroStrikeAction?: (forceGolden: boolean) => void;
  onPeerAutonomousDamage?: (damageAmount: number) => void;
  className?: string;
}

interface ActiveLightningBeam2D {
  id: number;
  mainPoints: Point2D[];
  branches: Point2D[][];
  isHero: boolean;
  rimHex: string;
  coreHex: string;
  ageSec: number;
  durationSec: number;
  impactX: number;
  impactY: number;
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

const SKY_CRACK_TREE = createSkyVaultCrackTree();
const INITIAL_PEER_TROUPE = createPeerBlacksmithTroupe(18);
const MAX_SPARK_POOL = 420;

export const CommunityPanoramicForgeCanvas = forwardRef<
  CommunityPanoramicForgeCanvasHandle,
  CommunityPanoramicForgeCanvasProps
>(function CommunityPanoramicForgeCanvas(
  {
    bossHp,
    bossMaxHp,
    activeStance,
    gameState,
    onHeroStrikeAction,
    onPeerAutonomousDamage,
    className = '',
  },
  ref
) {
  const containerRef = useRef<HTMLDivElement | null>(null);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  // Up-to-date refs for 60 FPS animation loop (never triggers effect restart)
  const bossHpRef = useRef<number>(bossHp);
  const bossMaxHpRef = useRef<number>(bossMaxHp);
  const activeStanceRef = useRef<StanceKey>(activeStance);
  const gameStateRef = useRef<string>(gameState);
  const onHeroStrikeActionRef = useRef(onHeroStrikeAction);
  const onPeerAutonomousDamageRef = useRef(onPeerAutonomousDamage);

  bossHpRef.current = bossHp;
  bossMaxHpRef.current = bossMaxHp;
  activeStanceRef.current = activeStance;
  gameStateRef.current = gameState;
  onHeroStrikeActionRef.current = onHeroStrikeAction;
  onPeerAutonomousDamageRef.current = onPeerAutonomousDamage;

  // Imperative hooks into canvas closure
  const executeHeroStrikeClosureRef = useRef<((forceGolden?: boolean) => void) | null>(null);
  const triggerPeerWaveClosureRef = useRef<(() => void) | null>(null);
  const spawnCombatTextClosureRef = useRef<
    ((text: string, subtext: string, color: string, glowColor: string, isGolden: boolean) => void) | null
  >(null);
  const resetClosureRef = useRef<(() => void) | null>(null);

  useImperativeHandle(
    ref,
    () => ({
      triggerHeroStrike: (forceGolden = false) => {
        executeHeroStrikeClosureRef.current?.(forceGolden);
      },
      triggerPeerWave: () => {
        triggerPeerWaveClosureRef.current?.();
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

  const handleCanvasClick = useCallback(() => {
    if (gameStateRef.current === 'playing' || gameStateRef.current === 'title') {
      onHeroStrikeActionRef.current?.(false);
    }
  }, []);

  useEffect(() => {
    const canvas = canvasRef.current;
    const container = containerRef.current;
    if (!canvas || !container) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

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

    let elapsedSec = 0;
    let heroStrikeTimer = -1;
    let screenShakeTimer = -1;
    let skyImpactFlash = 0;
    let rhythmPhase = 0.72;
    let hitstopTimer = 0;
    let boltIdCounter = 1;
    let textIdCounter = 1;

    const peerActors: PeerBlacksmithActor[] = INITIAL_PEER_TROUPE.map((p) => ({ ...p }));
    const peerLastCycleIndex = new Int32Array(peerActors.length).fill(-1);
    const peerActiveStrikeTimers = new Float32Array(peerActors.length).fill(-1);

    const activeBeams: ActiveLightningBeam2D[] = [];
    const floatingTexts: FloatingCombatText2D[] = [];

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

    const spawnAnvilSparkBurst = (
      originX: number,
      originY: number,
      count: number,
      primaryHex: string,
      isHero: boolean
    ) => {
      for (let i = 0; i < count; i++) {
        const angle = -Math.PI * (0.12 + Math.random() * 0.76);
        const speed = (isHero ? 180 : 95) + Math.random() * (isHero ? 340 : 140);
        const colorChoice =
          i % 3 === 0 ? '#FFF8D6' : i % 3 === 1 ? primaryHex : '#FF9E00';
        spawnParticle(
          originX + (Math.random() - 0.5) * (isHero ? 26 : 10),
          originY,
          Math.cos(angle) * speed,
          Math.sin(angle) * speed - (isHero ? 60 : 20),
          isHero ? 2.4 + Math.random() * 3.2 : 1.4 + Math.random() * 1.8,
          colorChoice,
          0.42 + Math.random() * 0.48,
          false
        );
      }
    };

    const spawnSkyMetallicAsh = (impactX: number, impactY: number, count: number) => {
      for (let i = 0; i < count; i++) {
        const spreadX = impactX + (Math.random() - 0.5) * viewW * 0.42;
        const spreadY = impactY + (Math.random() - 0.3) * viewH * 0.22;
        const ashColor =
          i % 3 === 0 ? '#FFD166' : i % 3 === 1 ? '#FF7B29' : '#90E0EF';
        spawnParticle(
          spreadX,
          Math.max(20, spreadY),
          (Math.random() - 0.5) * 38,
          42 + Math.random() * 88,
          1.8 + Math.random() * 2.8,
          ashColor,
          1.4 + Math.random() * 1.5,
          true
        );
      }
    };

    const triggerPeerStrike = (peerIndex: number) => {
      const peer = peerActors[peerIndex];
      if (!peer) return;
      peerActiveStrikeTimers[peerIndex] = 0;

      const px = peer.xNorm * viewW;
      const py = peer.yNorm * viewH;
      const anvilX = px + peer.facing * 20 * peer.scale;
      const anvilY = py - 14 * peer.scale;

      const targetX = viewW * (0.28 + (peer.xNorm - 0.5) * 0.44 + (Math.random() - 0.5) * 0.12);
      const targetY = viewH * (0.11 + Math.random() * 0.16);

      const bolt = generate2DLightningBolt(
        anvilX,
        anvilY,
        targetX,
        targetY,
        false,
        Math.floor((elapsedSec * 1000 + peerIndex * 313) % 99999)
      );

      activeBeams.push({
        id: boltIdCounter++,
        mainPoints: bolt.mainPoints,
        branches: bolt.branches,
        isHero: false,
        rimHex: peer.beamColorHex,
        coreHex: '#F0FAFF',
        ageSec: 0,
        durationSec: 0.42,
        impactX: targetX,
        impactY: targetY,
      });

      spawnAnvilSparkBurst(anvilX, anvilY, 6, peer.beamColorHex, false);

      if (gameStateRef.current === 'playing' && bossHpRef.current > 0) {
        onPeerAutonomousDamageRef.current?.(0.18 + Math.random() * 0.12);
      }
    };

    const executeHeroStrikeVisuals = (forceGolden = false) => {
      const currentStanceKey = activeStanceRef.current;
      const palette = HERO_STANCE_PALETTES[currentStanceKey] || HERO_STANCE_PALETTES.Q;

      heroStrikeTimer = 0;
      screenShakeTimer = 0;
      skyImpactFlash = 1.0;
      hitstopTimer = 0.032;

      const heroX = viewW * 0.5;
      const heroBaseY = viewH * 0.875;
      const anvilTopX = heroX + 34;
      const anvilTopY = heroBaseY - 46;

      rhythmPhase = 0.05;

      // 1. Anvil spark burst
      spawnAnvilSparkBurst(anvilTopX, anvilTopY, 38, palette.sparkHex, true);

      // 2. Colossal branching hero lightning beam
      const skyImpactX = viewW * (0.5 + (Math.random() - 0.5) * 0.08);
      const skyImpactY = viewH * (0.12 + Math.random() * 0.05);
      const heroBolt = generate2DLightningBolt(
        anvilTopX,
        anvilTopY,
        skyImpactX,
        skyImpactY,
        true,
        Math.floor(performance.now() + Math.random() * 7919)
      );

      activeBeams.push({
        id: boltIdCounter++,
        mainPoints: heroBolt.mainPoints,
        branches: heroBolt.branches,
        isHero: true,
        rimHex: palette.rimHex,
        coreHex: palette.coreHex,
        ageSec: 0,
        durationSec: 0.68,
        impactX: skyImpactX,
        impactY: skyImpactY,
      });

      // 3. Falling metallic sky ash
      spawnSkyMetallicAsh(skyImpactX, skyImpactY, 26);
    };

    const spawnCombatTextInternal = (
      text: string,
      subtext: string,
      color: string,
      glowColor: string,
      isGolden: boolean
    ) => {
      const heroX = viewW * 0.5;
      const heroBaseY = viewH * 0.875;

      floatingTexts.push({
        id: textIdCounter++,
        text,
        subtext,
        x: heroX,
        y: heroBaseY - 142,
        vy: -65,
        color,
        glowColor,
        ageSec: 0,
        durationSec: 1.25,
        scale: isGolden ? 1.18 : 1.0,
      });
    };

    const resetSimulation = () => {
      heroStrikeTimer = -1;
      screenShakeTimer = -1;
      skyImpactFlash = 0;
      activeBeams.length = 0;
      floatingTexts.length = 0;
      for (const p of sparkPool) p.active = false;
    };

    executeHeroStrikeClosureRef.current = (forceGolden?: boolean) => {
      executeHeroStrikeVisuals(forceGolden);
    };
    triggerPeerWaveClosureRef.current = () => {
      for (let i = 0; i < 5; i++) {
        triggerPeerStrike((i * 3) % peerActors.length);
      }
    };
    spawnCombatTextClosureRef.current = (text, subtext, color, glowColor, isGolden) => {
      spawnCombatTextInternal(text, subtext, color, glowColor, isGolden);
    };
    resetClosureRef.current = () => {
      resetSimulation();
    };

    // Seed initial peer sparks
    for (let i = 0; i < 3; i++) {
      triggerPeerStrike(i * 5 + 1);
    }

    // Expose debug API for automated inspection
    const debugApi = {
      strike: (forceGolden = true) => executeHeroStrikeVisuals(forceGolden),
      triggerPeerWave: () => {
        for (let i = 0; i < 6; i++) {
          triggerPeerStrike((i * 2 + 1) % peerActors.length);
        }
      },
      reset: () => resetSimulation(),
      getStats: () => ({
        rendererType: 'HTML5_CANVAS_2D_PANORAMA',
        skyRatio: PANORAMA_SKY_RATIO,
        gameState: gameStateRef.current,
        activeStance: activeStanceRef.current,
        peerCount: peerActors.length,
        activeBeams: activeBeams.length,
        floatingTextsCount: floatingTexts.length,
        screenShakeActive: screenShakeTimer >= 0 && screenShakeTimer <= SCREEN_SHAKE_DURATION_SEC,
      }),
    };
    (window as unknown as Record<string, unknown>).__celestialForge = debugApi;
    (window as unknown as Record<string, unknown>).__celestialVault = debugApi;

    // Drawing helpers
    const drawLightningPolyline = (
      points: Point2D[],
      strokeStyle: string,
      lineWidth: number,
      glowColor: string,
      glowWidth: number,
      alpha: number
    ) => {
      if (!points || points.length < 2) return;
      ctx.save();
      ctx.lineCap = 'round';
      ctx.lineJoin = 'round';
      ctx.beginPath();
      ctx.moveTo(points[0].x, points[0].y);
      for (let i = 1; i < points.length; i++) {
        ctx.lineTo(points[i].x, points[i].y);
      }
      if (glowWidth > 0) {
        ctx.globalAlpha = Math.max(0, Math.min(1, alpha * 0.28));
        ctx.strokeStyle = glowColor;
        ctx.lineWidth = lineWidth + glowWidth * 0.65;
        ctx.stroke();
      }
      ctx.globalAlpha = Math.max(0, Math.min(1, alpha));
      ctx.strokeStyle = strokeStyle;
      ctx.lineWidth = lineWidth;
      ctx.stroke();
      ctx.restore();
    };

    const drawBlacksmith2DSilhouette = (
      cx: number,
      footY: number,
      scale: number,
      facing: 1 | -1,
      hammerAngleRad: number,
      torsoOffsetY: number,
      squashX: number,
      squashY: number,
      rimHex: string,
      coreHex: string,
      isMainHero: boolean,
      label?: string
    ) => {
      ctx.save();
      ctx.translate(cx, footY);
      ctx.scale(scale * squashX, scale * squashY);

      // 1. Ground Forge Aura Ring under feet + Anvil
      ctx.save();
      ctx.fillStyle = rimHex;
      ctx.globalAlpha = isMainHero ? 0.16 : 0.1;
      ctx.beginPath();
      ctx.ellipse(14 * facing, 0, isMainHero ? 88 : 48, isMainHero ? 18 : 10, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();

      // 2. Anvil
      const anvilX = 34 * facing;
      ctx.save();
      ctx.translate(anvilX, 0);

      ctx.fillStyle = '#080C16';
      ctx.strokeStyle = isMainHero ? '#FFB703' : rimHex;
      ctx.lineWidth = isMainHero ? 2.4 : 1.5;

      ctx.beginPath();
      ctx.moveTo(-26, 0);
      ctx.lineTo(26, 0);
      ctx.lineTo(20, -12);
      ctx.lineTo(14, -28);
      ctx.lineTo(34, -36);
      ctx.lineTo(28, -45);
      ctx.lineTo(-28, -45);
      ctx.lineTo(-32, -35);
      ctx.lineTo(-14, -28);
      ctx.lineTo(-20, -12);
      ctx.closePath();
      ctx.fill();
      ctx.stroke();

      ctx.strokeStyle = isMainHero ? '#FFD166' : coreHex;
      ctx.lineWidth = isMainHero ? 2.6 : 1.6;
      ctx.beginPath();
      ctx.moveTo(-24, -42);
      ctx.lineTo(24, -42);
      ctx.moveTo(-11, -22);
      ctx.lineTo(11, -22);
      ctx.stroke();
      ctx.restore();

      // 3. Blacksmith Silhouette
      ctx.save();
      ctx.scale(facing, 1);
      ctx.translate(-14, torsoOffsetY);

      ctx.fillStyle = '#060913';
      ctx.strokeStyle = rimHex;
      ctx.lineWidth = isMainHero ? 2.8 : 1.8;
      ctx.lineJoin = 'round';
      ctx.lineCap = 'round';

      if (isMainHero) {
        ctx.save();
        ctx.fillStyle = '#0B1020';
        ctx.strokeStyle = rimHex;
        ctx.lineWidth = 2.0;
        ctx.beginPath();
        ctx.moveTo(-18, -78);
        ctx.quadraticCurveTo(-52, -62, -64, -18);
        ctx.quadraticCurveTo(-40, -24, -22, -46);
        ctx.closePath();
        ctx.fill();
        ctx.stroke();
        ctx.restore();
      }

      ctx.beginPath();
      ctx.moveTo(-22, -torsoOffsetY);
      ctx.lineTo(-16, -42);
      ctx.lineTo(-24, -84);
      ctx.lineTo(-12, -98);
      ctx.lineTo(18, -96);
      ctx.lineTo(14, -50);
      ctx.lineTo(24, -torsoOffsetY);
      ctx.lineTo(10, -torsoOffsetY);
      ctx.lineTo(3, -38);
      ctx.lineTo(-6, -38);
      ctx.lineTo(-10, -torsoOffsetY);
      ctx.closePath();
      ctx.fill();
      if (isMainHero) {
        ctx.save();
        ctx.globalAlpha = 0.28;
        ctx.lineWidth = 7.5;
        ctx.stroke();
        ctx.restore();
      }
      ctx.stroke();

      // Head
      ctx.beginPath();
      ctx.arc(3, -110, 11.5, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();

      // Visor Eye
      ctx.fillStyle = coreHex;
      ctx.beginPath();
      ctx.ellipse(8, -111, 3.8, 1.8, -0.1, 0, Math.PI * 2);
      ctx.fill();

      // Chest Sigil
      if (isMainHero) {
        ctx.strokeStyle = coreHex;
        ctx.lineWidth = 1.8;
        ctx.beginPath();
        ctx.moveTo(-4, -82);
        ctx.lineTo(8, -82);
        ctx.lineTo(2, -66);
        ctx.closePath();
        ctx.stroke();
      }

      // Arm & Hammer
      ctx.save();
      ctx.translate(10, -90);
      ctx.rotate(hammerAngleRad);

      if (hammerAngleRad > 0.1) {
        ctx.save();
        ctx.strokeStyle = `${rimHex}88`;
        ctx.lineWidth = isMainHero ? 10 : 5;
        ctx.beginPath();
        ctx.arc(0, 0, isMainHero ? 64 : 44, -1.3, 0.15);
        ctx.stroke();
        ctx.restore();
      }

      ctx.fillStyle = '#060913';
      ctx.strokeStyle = rimHex;
      ctx.lineWidth = isMainHero ? 2.5 : 1.7;
      ctx.beginPath();
      ctx.roundRect(-6, -8, 14, 34, 6);
      ctx.fill();
      ctx.stroke();

      const shaftLen = isMainHero ? 66 : 48;
      ctx.strokeStyle = isMainHero ? '#FFD166' : coreHex;
      ctx.lineWidth = isMainHero ? 4.5 : 3.0;
      ctx.beginPath();
      ctx.moveTo(0, 8);
      ctx.lineTo(0, -shaftLen);
      ctx.stroke();

      ctx.translate(0, -shaftLen);
      const hw = isMainHero ? 28 : 18;
      const hh = isMainHero ? 16 : 11;
      ctx.fillStyle = '#090E1C';
      ctx.strokeStyle = rimHex;
      ctx.lineWidth = isMainHero ? 3.0 : 2.0;

      ctx.beginPath();
      ctx.moveTo(-hw * 0.75, -hh);
      ctx.lineTo(hw * 0.75, -hh);
      ctx.lineTo(hw, -hh * 0.45);
      ctx.lineTo(hw, hh * 0.45);
      ctx.lineTo(hw * 0.75, hh);
      ctx.lineTo(-hw * 0.75, hh);
      ctx.lineTo(-hw, hh * 0.45);
      ctx.lineTo(-hw, -hh * 0.45);
      ctx.closePath();
      ctx.fill();
      if (isMainHero) {
        ctx.save();
        ctx.globalAlpha = 0.32;
        ctx.lineWidth = 9.0;
        ctx.stroke();
        ctx.restore();
      }
      ctx.stroke();

      ctx.strokeStyle = coreHex;
      ctx.lineWidth = isMainHero ? 2.2 : 1.4;
      ctx.beginPath();
      ctx.moveTo(-hw * 0.55, 0);
      ctx.lineTo(hw * 0.55, 0);
      ctx.moveTo(0, -hh * 0.55);
      ctx.lineTo(0, hh * 0.55);
      ctx.stroke();

      ctx.restore();
      ctx.restore();

      // 4. Overhead Badge
      if (label) {
        ctx.save();
        const labelY = -138 + torsoOffsetY * 0.4;
        ctx.font = isMainHero
          ? '700 13px "Chakra Petch", sans-serif'
          : '600 11.5px "Chakra Petch", monospace';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';

        const textMetrics = ctx.measureText(label);
        const padX = 8;
        const boxW = textMetrics.width + padX * 2;
        const boxH = isMainHero ? 22 : 19;

        ctx.fillStyle = isMainHero ? 'rgba(6, 10, 20, 0.88)' : 'rgba(6, 10, 20, 0.76)';
        ctx.strokeStyle = isMainHero ? rimHex : 'rgba(148, 163, 184, 0.4)';
        ctx.lineWidth = isMainHero ? 1.5 : 1;
        ctx.beginPath();
        ctx.roundRect(-boxW * 0.5, labelY - boxH * 0.5, boxW, boxH, 4);
        ctx.fill();
        ctx.stroke();

        ctx.fillStyle = isMainHero ? coreHex : '#E2E8F0';
        ctx.fillText(label, 0, labelY + 0.5);
        ctx.restore();
      }

      ctx.restore();
    };

    let animFrameId = 0;
    let lastPerfTime = performance.now();

    const renderFrame = (now: number) => {
      try {
        const rawDt = Math.min((now - lastPerfTime) / 1000, 0.05);
        lastPerfTime = now;

        const isPaused = gameStateRef.current === 'paused';
        if (!isPaused) {
          if (hitstopTimer > 0) {
            hitstopTimer = Math.max(0, hitstopTimer - rawDt);
          }
          const simDt = hitstopTimer > 0 ? rawDt * 0.2 : rawDt;
          elapsedSec += simDt;

          rhythmPhase = (rhythmPhase + simDt * (100 / 60)) % 1.0;

          if (heroStrikeTimer >= 0) {
            heroStrikeTimer += rawDt;
            if (heroStrikeTimer > HERO_STRIKE_TOTAL_SEC) {
              heroStrikeTimer = -1;
            }
          }

          if (screenShakeTimer >= 0) {
            screenShakeTimer += rawDt;
            if (screenShakeTimer > SCREEN_SHAKE_DURATION_SEC) {
              screenShakeTimer = -1;
            }
          }

          if (skyImpactFlash > 0) {
            skyImpactFlash = Math.max(0, skyImpactFlash - rawDt * 3.8);
          }

          // Autonomous Peer schedule
          for (let i = 0; i < peerActors.length; i++) {
            const peer = peerActors[i];
            const cycleIndex = Math.floor(
              (elapsedSec + peer.strikeOffsetSec) / peer.strikePeriodSec
            );
            if (
              peerLastCycleIndex[i] !== -1 &&
              cycleIndex > peerLastCycleIndex[i] &&
              bossHpRef.current > 0
            ) {
              triggerPeerStrike(i);
            }
            peerLastCycleIndex[i] = cycleIndex;

            if (peerActiveStrikeTimers[i] >= 0) {
              peerActiveStrikeTimers[i] += simDt;
              if (peerActiveStrikeTimers[i] > HERO_STRIKE_TOTAL_SEC) {
                peerActiveStrikeTimers[i] = -1;
              }
            }
          }

          // Active beams
          for (let i = activeBeams.length - 1; i >= 0; i--) {
            activeBeams[i].ageSec += rawDt;
            if (activeBeams[i].ageSec >= activeBeams[i].durationSec) {
              activeBeams.splice(i, 1);
            }
          }

          // Sparks & ash
          const groundBounceY = viewH * 0.91;
          for (let i = 0; i < MAX_SPARK_POOL; i++) {
            const p = sparkPool[i];
            if (!p.active) continue;
            p.age += simDt;
            if (p.age >= p.maxAge) {
              p.active = false;
              continue;
            }
            if (p.isAsh) {
              p.x += (p.vx + Math.sin(elapsedSec * 3.2 + i) * 18) * simDt;
              p.y += p.vy * simDt;
              p.alpha = (1 - p.age / p.maxAge) * (0.65 + 0.35 * Math.sin(elapsedSec * 16 + i));
            } else {
              p.vy += 690 * simDt;
              p.x += p.vx * simDt;
              p.y += p.vy * simDt;
              if (p.y >= groundBounceY && p.vy > 0) {
                p.y = groundBounceY;
                p.vy = -p.vy * 0.42;
                p.vx *= 0.78;
              }
              p.alpha = 1 - p.age / p.maxAge;
            }
          }

          // Floating texts
          for (let i = floatingTexts.length - 1; i >= 0; i--) {
            const ft = floatingTexts[i];
            ft.ageSec += rawDt;
            ft.y += ft.vy * rawDt;
            ft.vy *= 0.94;
            if (ft.ageSec >= ft.durationSec) {
              floatingTexts.splice(i, 1);
            }
          }
        }

        // ======================================================================
        // RENDERING
        // ======================================================================
        ctx.save();
        ctx.setTransform(1, 0, 0, 1, 0, 0);

        // Screen Shake
        if (screenShakeTimer >= 0 && screenShakeTimer <= SCREEN_SHAKE_DURATION_SEC) {
          const decay = 1 - screenShakeTimer / SCREEN_SHAKE_DURATION_SEC;
          const mag = decay * 11;
          const sx = (Math.sin(elapsedSec * 190) + (Math.random() - 0.5)) * mag;
          const sy = (Math.cos(elapsedSec * 210) + (Math.random() - 0.5)) * mag;
          ctx.translate(sx, sy);
        }

        const horizonY = viewH * PANORAMA_SKY_RATIO;
        const crackRatio = Math.max(
          0.12,
          Math.min(1.0, 1 - bossHpRef.current / (bossMaxHpRef.current || 1) + 0.12)
        );
        const currentStanceMeta = HERO_STANCE_PALETTES[activeStanceRef.current] || HERO_STANCE_PALETTES.Q;

        // ----------------------------------------------------------------------
        // LAYER 1: SKY VAULT (TOP 65%)
        // ----------------------------------------------------------------------
        const skyGrad = ctx.createLinearGradient(0, 0, 0, horizonY);
        skyGrad.addColorStop(0, '#04060D');
        skyGrad.addColorStop(0.45, '#0B1022');
        skyGrad.addColorStop(0.82, '#171128');
        skyGrad.addColorStop(1, '#261424');
        ctx.fillStyle = skyGrad;
        ctx.fillRect(0, 0, viewW, horizonY + 4);

        const zenithX = viewW * 0.5;
        const zenithY = viewH * 0.14;
        const magmaRadius = viewW * (0.28 + crackRatio * 0.26);
        const zenithGlow = ctx.createRadialGradient(
          zenithX,
          zenithY,
          12,
          zenithX,
          zenithY,
          magmaRadius
        );
        zenithGlow.addColorStop(
          0,
          `rgba(255, 140, 26, ${0.28 + crackRatio * 0.36 + skyImpactFlash * 0.32})`
        );
        zenithGlow.addColorStop(
          0.45,
          `rgba(220, 38, 38, ${0.14 + crackRatio * 0.22 + skyImpactFlash * 0.18})`
        );
        zenithGlow.addColorStop(1, 'rgba(4, 6, 13, 0)');
        ctx.fillStyle = zenithGlow;
        ctx.fillRect(0, 0, viewW, horizonY);

        // Storm cloud layers
        ctx.fillStyle = 'rgba(8, 11, 22, 0.52)';
        for (let c = 0; c < 10; c++) {
          const drift = ((elapsedSec * (8 + (c % 3) * 4) + c * 170) % (viewW + 360)) - 180;
          const cy = viewH * (0.08 + (c % 4) * 0.12);
          const rx = 140 + (c % 3) * 65;
          const ry = 34 + (c % 2) * 16;
          ctx.beginPath();
          ctx.ellipse(drift, cy, rx, ry, 0, 0, Math.PI * 2);
          ctx.fill();
        }

        // Molten Cracks
        ctx.save();
        ctx.lineCap = 'round';
        ctx.lineJoin = 'round';
        for (let i = 0; i < SKY_CRACK_TREE.length; i++) {
          const branch = SKY_CRACK_TREE[i];
          if (crackRatio < branch.threshold) continue;

          const branchIntensity = Math.min(
            1,
            (crackRatio - branch.threshold) / Math.max(0.15, 1 - branch.threshold)
          );
          const pts = branch.points;
          const visibleCount = Math.max(
            2,
            Math.min(pts.length, Math.ceil(pts.length * (0.35 + branchIntensity * 0.65)))
          );

          ctx.beginPath();
          ctx.moveTo(pts[0].x * viewW, pts[0].y * viewH);
          for (let k = 1; k < visibleCount; k++) {
            ctx.lineTo(pts[k].x * viewW, pts[k].y * viewH);
          }

          ctx.strokeStyle = `rgba(255, 55, 15, ${0.22 + branchIntensity * 0.28 + skyImpactFlash * 0.2})`;
          ctx.lineWidth = branch.weight * (3.2 + crackRatio * 2.2) + skyImpactFlash * 3.5;
          ctx.stroke();

          ctx.strokeStyle = `rgba(255, 145, 0, ${0.55 + branchIntensity * 0.4 + skyImpactFlash * 0.25})`;
          ctx.lineWidth = branch.weight * (1.35 + crackRatio * 0.85) + skyImpactFlash * 1.4;
          ctx.stroke();

          ctx.strokeStyle =
            skyImpactFlash > 0.25
              ? '#FFFFFF'
              : `rgba(255, 232, 140, ${0.7 + branchIntensity * 0.3})`;
          ctx.lineWidth = Math.max(1.0, branch.weight * 0.55);
          ctx.stroke();
        }
        ctx.restore();

        // Distant sheet lightning
        const ambientThunder = Math.pow(Math.max(0, Math.sin(elapsedSec * 3.7) * Math.cos(elapsedSec * 9.3)), 8);
        if (ambientThunder > 0.25) {
          ctx.fillStyle = `rgba(180, 230, 255, ${ambientThunder * 0.09})`;
          ctx.fillRect(0, 0, viewW, horizonY);
        }

        // Zenith Sigil
        ctx.save();
        ctx.translate(zenithX, zenithY);
        ctx.strokeStyle = `rgba(255, 158, 0, ${0.42 + crackRatio * 0.45})`;
        ctx.lineWidth = 1.6;
        ctx.beginPath();
        ctx.arc(0, 0, 34 + Math.sin(elapsedSec * 3) * 3, 0, Math.PI * 2);
        ctx.stroke();
        ctx.strokeStyle = `rgba(255, 71, 26, ${0.32 + crackRatio * 0.5})`;
        ctx.beginPath();
        ctx.arc(0, 0, 56 + crackRatio * 18, 0, Math.PI * 2);
        ctx.stroke();
        ctx.restore();

        // ----------------------------------------------------------------------
        // LAYER 2: BASALT PLATEAU (BOTTOM 35%)
        // ----------------------------------------------------------------------
        const groundGrad = ctx.createLinearGradient(0, horizonY, 0, viewH);
        groundGrad.addColorStop(0, '#0D1220');
        groundGrad.addColorStop(0.35, '#090D18');
        groundGrad.addColorStop(1, '#04060B');
        ctx.fillStyle = groundGrad;
        ctx.fillRect(0, horizonY, viewW, viewH - horizonY);

        // Jagged Basalt Ridge
        ctx.fillStyle = '#070A14';
        ctx.strokeStyle = 'rgba(255, 120, 30, 0.38)';
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.moveTo(0, horizonY + 12);
        const ridgeSteps = 24;
        for (let r = 0; r <= ridgeSteps; r++) {
          const rx = (r / ridgeSteps) * viewW;
          const peak = Math.sin(r * 1.7) * 14 + Math.cos(r * 3.1) * 8;
          ctx.lineTo(rx, horizonY - Math.abs(peak));
        }
        ctx.lineTo(viewW, horizonY + 24);
        ctx.lineTo(0, horizonY + 24);
        ctx.closePath();
        ctx.fill();
        ctx.stroke();

        // 3 Stepped Quartz Terraces
        const terraceYLevels = [viewH * 0.705, viewH * 0.772, viewH * 0.842];
        terraceYLevels.forEach((ty, idx) => {
          const stepH = viewH * 0.065;
          const stepGrad = ctx.createLinearGradient(0, ty, 0, ty + stepH);
          stepGrad.addColorStop(0, idx === 2 ? '#131C31' : '#0F172A');
          stepGrad.addColorStop(1, '#060912');
          ctx.fillStyle = stepGrad;

          ctx.beginPath();
          ctx.moveTo(0, ty);
          for (let s = 0; s <= 16; s++) {
            const sx = (s / 16) * viewW;
            const dip = s >= 7 && s <= 9 ? 6 : (s % 2 === 0 ? -3 : 3);
            ctx.lineTo(sx, ty + dip);
          }
          ctx.lineTo(viewW, ty + stepH);
          ctx.lineTo(0, ty + stepH);
          ctx.closePath();
          ctx.fill();

          ctx.strokeStyle =
            idx === 2
              ? `${currentStanceMeta.rimHex}66`
              : 'rgba(124, 232, 255, 0.28)';
          ctx.lineWidth = idx === 2 ? 2.0 : 1.3;
          ctx.beginPath();
          for (let s = 0; s <= 16; s++) {
            const sx = (s / 16) * viewW;
            const dip = s >= 7 && s <= 9 ? 6 : (s % 2 === 0 ? -3 : 3);
            if (s === 0) ctx.moveTo(sx, ty + dip);
            else ctx.lineTo(sx, ty + dip);
          }
          ctx.stroke();
        });

        // ----------------------------------------------------------------------
        // LAYER 3: LIGHTNING BEAMS
        // ----------------------------------------------------------------------
        for (let i = 0; i < activeBeams.length; i++) {
          const beam = activeBeams[i];
          const progress = beam.ageSec / beam.durationSec;
          const alpha = (1 - progress) * (0.82 + 0.18 * Math.sin(elapsedSec * 90 + beam.id));

          if (beam.isHero) {
            drawLightningPolyline(beam.mainPoints, beam.rimHex, 14, beam.rimHex, 28, alpha * 0.42);
            drawLightningPolyline(beam.mainPoints, beam.rimHex, 6.5, beam.rimHex, 16, alpha * 0.85);
            drawLightningPolyline(beam.mainPoints, '#FFFFFF', 2.8, beam.coreHex, 8, alpha);

            for (const br of beam.branches) {
              drawLightningPolyline(br, beam.rimHex, 4.2, beam.rimHex, 12, alpha * 0.72);
              drawLightningPolyline(br, '#FFFFFF', 1.5, '#FFFFFF', 4, alpha * 0.9);
            }
          } else {
            drawLightningPolyline(beam.mainPoints, beam.rimHex, 3.6, beam.rimHex, 10, alpha * 0.45);
            drawLightningPolyline(beam.mainPoints, beam.coreHex, 1.4, beam.rimHex, 4, alpha * 0.78);
            for (const br of beam.branches) {
              drawLightningPolyline(br, beam.rimHex, 1.2, beam.rimHex, 4, alpha * 0.5);
            }
          }

          ctx.save();
          const burstRadius = (beam.isHero ? 26 : 12) + progress * (beam.isHero ? 95 : 36);
          ctx.strokeStyle = beam.isHero ? '#FFD166' : beam.rimHex;
          ctx.lineWidth = beam.isHero ? 2.8 * (1 - progress) : 1.5 * (1 - progress);
          ctx.globalAlpha = Math.max(0, alpha * 0.85);
          ctx.beginPath();
          ctx.ellipse(
            beam.impactX,
            beam.impactY,
            burstRadius,
            burstRadius * 0.45,
            0,
            0,
            Math.PI * 2
          );
          ctx.stroke();
          ctx.restore();
        }

        // ----------------------------------------------------------------------
        // LAYER 4: 18 PEER BLACKSMITHS
        // ----------------------------------------------------------------------
        for (let i = 0; i < peerActors.length; i++) {
          const peer = peerActors[i];
          const px = peer.xNorm * viewW;
          const py = peer.yNorm * viewH;
          const peerPose = evaluateHero2DStrikePose(
            peerActiveStrikeTimers[i],
            elapsedSec + peer.strikeOffsetSec
          );

          drawBlacksmith2DSilhouette(
            px,
            py,
            peer.scale,
            peer.facing,
            peerPose.hammerAngleRad,
            peerPose.torsoOffsetY,
            peerPose.scaleX,
            peerPose.scaleY,
            peer.beamColorHex,
            '#E2F8FF',
            false,
            peer.label
          );
        }

        // ----------------------------------------------------------------------
        // LAYER 5: CENTER MAIN HERO & ANVIL
        // ----------------------------------------------------------------------
        const heroX = viewW * 0.5;
        const heroY = viewH * 0.885;
        const heroPose = evaluateHero2DStrikePose(heroStrikeTimer, elapsedSec);

        // Hero Altar Platform
        ctx.save();
        ctx.translate(heroX, heroY + 6);
        ctx.fillStyle = '#0B1222';
        ctx.strokeStyle = currentStanceMeta.rimHex;
        ctx.lineWidth = 2.4;
        ctx.beginPath();
        ctx.moveTo(-135, 16);
        ctx.lineTo(135, 16);
        ctx.lineTo(108, -12);
        ctx.lineTo(-108, -12);
        ctx.closePath();
        ctx.fill();
        ctx.stroke();

        // Contracting Rhythm Ring (100 BPM)
        const anvilCenterOffset = 38;
        const ringScale = 1 - rhythmPhase;
        const isSweetSpot = Math.abs(rhythmPhase - 0.78) <= 0.18;
        ctx.strokeStyle = isSweetSpot ? '#FFD166' : currentStanceMeta.rimHex;
        ctx.lineWidth = isSweetSpot ? 3.2 : 1.8;
        ctx.globalAlpha = 0.35 + rhythmPhase * 0.55;
        ctx.beginPath();
        ctx.ellipse(
          anvilCenterOffset,
          -4,
          24 + ringScale * 76,
          7 + ringScale * 22,
          0,
          0,
          Math.PI * 2
        );
        ctx.stroke();
        ctx.restore();

        // Main Hero Silhouette
        drawBlacksmith2DSilhouette(
          heroX,
          heroY,
          1.14,
          1,
          heroPose.hammerAngleRad,
          heroPose.torsoOffsetY,
          heroPose.scaleX,
          heroPose.scaleY,
          currentStanceMeta.rimHex,
          currentStanceMeta.coreHex,
          true,
          `THỢ RÈN CHÍNH · [${currentStanceMeta.key}] ${currentStanceMeta.nameVn.toUpperCase()}`
        );

        // ----------------------------------------------------------------------
        // LAYER 6: SPARKS & ASH
        // ----------------------------------------------------------------------
        ctx.save();
        for (let i = 0; i < MAX_SPARK_POOL; i++) {
          const p = sparkPool[i];
          if (!p.active || p.alpha <= 0.02) continue;

          ctx.globalAlpha = Math.max(0, Math.min(1, p.alpha));
          ctx.fillStyle = p.color;
          ctx.strokeStyle = p.color;

          if (p.isAsh) {
            ctx.beginPath();
            ctx.moveTo(p.x, p.y - p.size);
            ctx.lineTo(p.x + p.size * 0.75, p.y);
            ctx.lineTo(p.x, p.y + p.size);
            ctx.lineTo(p.x - p.size * 0.75, p.y);
            ctx.closePath();
            ctx.fill();
          } else {
            ctx.lineWidth = p.size;
            ctx.lineCap = 'round';
            ctx.beginPath();
            ctx.moveTo(p.x, p.y);
            ctx.lineTo(p.x - p.vx * 0.024, p.y - p.vy * 0.024);
            ctx.stroke();
          }
        }
        ctx.restore();

        // ----------------------------------------------------------------------
        // LAYER 7: FLOATING COMBAT TEXT
        // ----------------------------------------------------------------------
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

          ctx.font = '700 12px "Chakra Petch", sans-serif';
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
        animFrameId = requestAnimationFrame(renderFrame);
      }
    };

    renderFrame(performance.now());

    return () => {
      cancelAnimationFrame(animFrameId);
      ro.disconnect();
    };
  }, []); // Mounts once, decoupled from component state updates

  return (
    <div
      ref={containerRef}
      className={`relative w-full h-full overflow-hidden select-none ${className}`}
    >
      <canvas
        ref={canvasRef}
        data-testid="panoramic-2d-canvas"
        onClick={handleCanvasClick}
        className="block w-full h-full cursor-pointer"
      />
    </div>
  );
});
