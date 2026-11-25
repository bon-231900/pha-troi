// =====================================================================
// PHÁ TRỜI - HIGH-PERFORMANCE ZERO-LAG LIGHTNING & PLASMA VFX ENGINE
// Optimized for rock-solid 60 FPS on Mobile & PC using GPU Additive Blending
// (Zero expensive shadowBlur Gaussian CPU passes, 100% batched vector paths).
// =====================================================================

export interface Point2D {
  x: number;
  y: number;
}

export interface LightningBranch {
  segments: Point2D[];
  lineWidth: number;
}

export interface AdvancedLightningBolt {
  id: number;
  mainSegments: Point2D[];
  branches: LightningBranch[];
  groundTendrils: LightningBranch[];
  alpha: number;
  maxAlpha: number;
  decay: number;
  color: string;
  lightColor: string;
  lineWidth: number;
  power: number;
  age: number;
  impactX: number;
  impactY: number;
  impactRadius: number;
  hasImpactBurst: boolean;
  flickerSeed: number;
}

export interface ElectricZapParticle {
  active: boolean;
  x: number;
  y: number;
  prevX: number;
  prevY: number;
  vx: number;
  vy: number;
  life: number;
  maxLife: number;
  color: string;
  lineWidth: number;
}

const HEX_RGB_CACHE = new Map<string, string>();
export function hexToRgb(hex: string): string {
  if (HEX_RGB_CACHE.has(hex)) return HEX_RGB_CACHE.get(hex)!;
  let clean = hex.replace('#', '');
  if (clean.length === 3) {
    clean = clean.split('').map((c) => c + c).join('');
  }
  const num = parseInt(clean, 16);
  if (isNaN(num)) return '0, 240, 255';
  const r = (num >> 16) & 255;
  const g = (num >> 8) & 255;
  const b = num & 255;
  const res = `${r}, ${g}, ${b}`;
  HEX_RGB_CACHE.set(hex, res);
  return res;
}

let boltIdCounter = 1;

/**
 * Creates an optimized fractal lightning bolt (fast math, concise segment count).
 */
export function createAdvancedLightningBolt(
  targetX: number,
  targetY: number,
  options: {
    viewH: number;
    color?: string;
    lightColor?: string;
    power?: number;
    decay?: number;
    startX?: number;
    startY?: number;
    branchCount?: number;
    hasGroundTendrils?: boolean;
  }
): AdvancedLightningBolt {
  const power = options.power ?? 1.0;
  const color = options.color ?? '#00F0FF';
  const lightColor = options.lightColor ?? '#38BDF8';
  // Snappy, realistic lightning lifespan: ~0.12 - 0.16s
  const decay = options.decay ?? (7.2 / Math.max(0.7, power));
  const branchCount = Math.min(3, options.branchCount ?? (power > 1.3 ? 3 : 2));
  const hasGroundTendrils = options.hasGroundTendrils ?? true;

  const startX = options.startX ?? (targetX + (Math.random() - 0.5) * 110);
  const startY = options.startY ?? Math.max(15, options.viewH * (0.04 + Math.random() * 0.05));

  const dx = targetX - startX;
  const dy = targetY - startY;
  const totalDist = Math.sqrt(dx * dx + dy * dy);
  const nx = -dy / totalDist;
  const ny = dx / totalDist;

  // 1. High-Performance Fractal Trunk (10-12 segments are plenty for sharp jaggedness)
  const steps = 11;
  const mainSegments: Point2D[] = [];
  mainSegments.push({ x: startX, y: startY });

  for (let s = 1; s < steps; s++) {
    const frac = s / steps;
    const envelope = Math.sin(frac * Math.PI);
    const primaryOffset = (Math.random() - 0.5) * 44 * envelope * Math.min(1.4, power);

    const curX = startX + dx * frac + nx * primaryOffset;
    const curY = startY + dy * frac + ny * primaryOffset;
    mainSegments.push({ x: curX, y: curY });
  }
  mainSegments.push({ x: targetX, y: targetY });

  // 2. Secondary Fractal Branches (2-3 branches max for high FPS)
  const branches: LightningBranch[] = [];
  const branchNodes = [3, 6, 8];
  for (let b = 0; b < branchCount; b++) {
    const nodeIdx = branchNodes[b] || 5;
    if (nodeIdx >= mainSegments.length) continue;
    const node = mainSegments[nodeIdx];
    const prevNode = mainSegments[nodeIdx - 1];

    const segDx = node.x - prevNode.x;
    const segDy = node.y - prevNode.y;
    const side = b % 2 === 0 ? 1 : -1;
    const branchAngle = Math.atan2(segDy, segDx) + side * (0.45 + Math.random() * 0.35);

    const branchLength = (40 + Math.random() * 55) * Math.min(1.4, power);
    const branchSteps = 4;
    const branchSegs: Point2D[] = [{ x: node.x, y: node.y }];

    let curBx = node.x;
    let curBy = node.y;
    const stepLen = branchLength / branchSteps;

    for (let bs = 1; bs <= branchSteps; bs++) {
      const stepAngle = branchAngle + (Math.random() - 0.5) * 0.5;
      curBx += Math.cos(stepAngle) * stepLen;
      curBy += Math.sin(stepAngle) * stepLen;
      branchSegs.push({ x: curBx, y: curBy });
    }

    branches.push({
      segments: branchSegs,
      lineWidth: 2.0 * Math.min(1.3, power),
    });
  }

  // 3. Ground Surface Creepers (2 horizontal sparks on anvil face)
  const groundTendrils: LightningBranch[] = [];
  if (hasGroundTendrils) {
    const creeperCount = 2;
    for (let c = 0; c < creeperCount; c++) {
      const side = c === 0 ? 1 : -1;
      const spreadX = (22 + Math.random() * 35) * side;
      const cSegs: Point2D[] = [
        { x: targetX, y: targetY },
        { x: targetX + spreadX * 0.45 + (Math.random() - 0.5) * 6, y: targetY + (Math.random() - 0.5) * 4 },
        { x: targetX + spreadX, y: targetY + (Math.random() - 0.5) * 5 },
      ];
      groundTendrils.push({
        segments: cSegs,
        lineWidth: 1.6,
      });
    }
  }

  return {
    id: boltIdCounter++,
    mainSegments,
    branches,
    groundTendrils,
    alpha: 1.0,
    maxAlpha: 1.0,
    decay,
    color,
    lightColor,
    lineWidth: (3.2 + Math.random() * 0.8) * Math.min(1.5, power),
    power,
    age: 0,
    impactX: targetX,
    impactY: targetY,
    impactRadius: Math.min(48, 22 * power),
    hasImpactBurst: true,
    flickerSeed: Math.random() * 100,
  };
}

/**
 * Fast batched polyline path builder (does not call stroke, zero allocations)
 */
function appendPolylinePath(ctx: CanvasRenderingContext2D, pts: Point2D[]) {
  if (pts.length < 2) return;
  ctx.moveTo(pts[0].x, pts[0].y);
  for (let i = 1; i < pts.length; i++) {
    ctx.lineTo(pts[i].x, pts[i].y);
  }
}

/**
 * Ultra-fast multi-pass additive lightning renderer (ZERO shadowBlur).
 * Blends layers directly in the GPU framebuffer via 'lighter'.
 */
export function drawAdvancedLightningBolt(
  ctx: CanvasRenderingContext2D,
  bolt: AdvancedLightningBolt
) {
  if (bolt.alpha <= 0.03) return;

  ctx.save();
  ctx.globalCompositeOperation = 'lighter';
  ctx.lineCap = 'round';
  ctx.lineJoin = 'round';

  const effAlpha = Math.max(0, Math.min(1, bolt.alpha));

  // -------------------------------------------------------------
  // PASS 1: Broad Corona Glow (Thick stroke, low alpha) - ZERO BLUR
  // -------------------------------------------------------------
  ctx.strokeStyle = bolt.color;
  ctx.lineWidth = bolt.lineWidth * 2.8;
  ctx.globalAlpha = effAlpha * 0.28;
  ctx.beginPath();
  appendPolylinePath(ctx, bolt.mainSegments);
  for (let b = 0; b < bolt.branches.length; b++) {
    appendPolylinePath(ctx, bolt.branches[b].segments);
  }
  for (let c = 0; c < bolt.groundTendrils.length; c++) {
    appendPolylinePath(ctx, bolt.groundTendrils[c].segments);
  }
  ctx.stroke();

  // -------------------------------------------------------------
  // PASS 2: Ionized Arc Body (Medium stroke, vibrant color)
  // -------------------------------------------------------------
  ctx.strokeStyle = bolt.lightColor;
  ctx.lineWidth = bolt.lineWidth * 1.5;
  ctx.globalAlpha = effAlpha * 0.65;
  ctx.beginPath();
  appendPolylinePath(ctx, bolt.mainSegments);
  for (let b = 0; b < bolt.branches.length; b++) {
    appendPolylinePath(ctx, bolt.branches[b].segments);
  }
  for (let c = 0; c < bolt.groundTendrils.length; c++) {
    appendPolylinePath(ctx, bolt.groundTendrils[c].segments);
  }
  ctx.stroke();

  // -------------------------------------------------------------
  // PASS 3: Hyper-Hot Plasma Core (Crisp, blinding pure white)
  // -------------------------------------------------------------
  ctx.strokeStyle = '#FFFFFF';
  ctx.lineWidth = Math.max(1.2, bolt.lineWidth * 0.55);
  ctx.globalAlpha = effAlpha;
  ctx.beginPath();
  appendPolylinePath(ctx, bolt.mainSegments);
  for (let b = 0; b < bolt.branches.length; b++) {
    appendPolylinePath(ctx, bolt.branches[b].segments);
  }
  ctx.stroke();

  // -------------------------------------------------------------
  // PASS 4: Ground Zero Impact Plasma Flare (Single simple radial burst)
  // -------------------------------------------------------------
  if (bolt.hasImpactBurst && effAlpha > 0.2) {
    const burstR = bolt.impactRadius * effAlpha;
    ctx.fillStyle = '#FFFFFF';
    ctx.globalAlpha = effAlpha * 0.85;
    ctx.beginPath();
    ctx.arc(bolt.impactX, bolt.impactY, burstR * 0.45, 0, Math.PI * 2);
    ctx.fill();

    ctx.strokeStyle = bolt.lightColor;
    ctx.lineWidth = 2.0;
    ctx.globalAlpha = effAlpha * 0.65;
    ctx.beginPath();
    ctx.arc(bolt.impactX, bolt.impactY, burstR, 0, Math.PI * 2);
    ctx.stroke();
  }

  ctx.restore();
}

/**
 * Creates rapid electric zap particles (capped pool, zero lag)
 */
export function createElectricZapParticles(
  originX: number,
  originY: number,
  count = 12,
  color = '#00F0FF',
  power = 1.0
): ElectricZapParticle[] {
  const actualCount = Math.min(14, count);
  const particles: ElectricZapParticle[] = [];
  for (let i = 0; i < actualCount; i++) {
    const ang = Math.PI * 1.5 + (Math.random() - 0.5) * 2.0;
    const speed = (160 + Math.random() * 260) * Math.min(1.4, power);
    const life = 0.16 + Math.random() * 0.14;
    particles.push({
      active: true,
      x: originX,
      y: originY,
      prevX: originX,
      prevY: originY,
      vx: Math.cos(ang) * speed,
      vy: Math.sin(ang) * speed,
      life,
      maxLife: life,
      color: Math.random() < 0.45 ? '#FFFFFF' : color,
      lineWidth: 1.4 + Math.random() * 1.0,
    });
  }
  return particles;
}

/**
 * Updates and renders electric zap particles in a SINGLE batched draw call (ZERO shadowBlur).
 */
export function updateAndDrawElectricZaps(
  ctx: CanvasRenderingContext2D,
  zaps: ElectricZapParticle[],
  dt: number
) {
  if (zaps.length === 0) return;

  // Cap array size to prevent memory bloat
  if (zaps.length > 24) {
    zaps.splice(0, zaps.length - 24);
  }

  ctx.save();
  ctx.globalCompositeOperation = 'lighter';
  ctx.lineCap = 'round';

  ctx.strokeStyle = '#38BDF8';
  ctx.lineWidth = 1.8;
  ctx.beginPath();

  for (let i = zaps.length - 1; i >= 0; i--) {
    const p = zaps[i];
    if (!p.active) {
      zaps.splice(i, 1);
      continue;
    }

    p.life -= dt;
    if (p.life <= 0) {
      zaps.splice(i, 1);
      continue;
    }

    p.prevX = p.x;
    p.prevY = p.y;
    p.x += p.vx * dt;
    p.y += p.vy * dt;

    // Batch streak into active path
    ctx.moveTo(p.prevX, p.prevY);
    ctx.lineTo(p.x, p.y);
  }

  ctx.globalAlpha = 0.75;
  ctx.stroke();

  ctx.restore();
}

/**
 * Renders an optimized sky flash (simple top-to-bottom fill, 0ms lag)
 */
export function drawSkyLightningFlash(
  ctx: CanvasRenderingContext2D,
  viewW: number,
  viewH: number,
  color: string,
  intensity: number
) {
  if (intensity <= 0.05) return;

  ctx.save();
  ctx.globalCompositeOperation = 'screen';
  const rgb = hexToRgb(color);
  const flashAlpha = Math.min(0.35, intensity * 0.25);

  ctx.fillStyle = `rgba(${rgb}, ${flashAlpha})`;
  ctx.fillRect(0, 0, viewW, viewH * 0.65);
  ctx.restore();
}
