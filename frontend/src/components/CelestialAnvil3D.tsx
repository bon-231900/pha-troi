import React, { useEffect, useRef, useImperativeHandle, forwardRef } from 'react';
import * as THREE from 'three';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import {
  DivineStanceId,
  FORGE_BPM,
  FORGE_SPARK_BUFFER_SIZE,
  HAMMER_DOWNSTROKE_SEC,
  HAMMER_REBOUND_SEC,
  HAMMER_STANCES,
  JudgmentGrade,
  PERFECT_TOLERANCE,
  PeerStrikeQuality,
  SPARK_GRAVITY,
  STANCE_KEY_BY_ID,
  StanceKey,
  TARGET_RIM_PROGRESS,
  computeHammerStrikeAngle,
  createForgeSparkBuffer,
  spawnForgeSparkBurst,
} from '../game/rules';

export interface CelestialAnvil3DHandle {
  strike: () => void;
  onPeerStrike: (quality?: PeerStrikeQuality) => void;
}

interface CelestialAnvil3DProps {
  waveProgressRef: React.MutableRefObject<number>;
  currentStance: DivineStanceId;
  activeStance?: StanceKey;
  overdriveActive: boolean;
  globalBurstActive: boolean;
  lastStrikeId: number;
  lastStrikeGrade: JudgmentGrade;
  onStrike: () => void;
}

/**
 * Generates high-resolution procedural CanvasTextures for the Anvil's top face:
 * - Emissive Map: Golden runic grooves & sacred geometry channels
 * - Bump Map: Brushed forged steel grain + carved rune trenches
 */
function createAnvilRuneTextures(maxAnisotropy: number) {
  const size = 512;
  const emissiveCanvas = document.createElement('canvas');
  emissiveCanvas.width = size;
  emissiveCanvas.height = size;
  const eCtx = emissiveCanvas.getContext('2d')!;

  const bumpCanvas = document.createElement('canvas');
  bumpCanvas.width = size;
  bumpCanvas.height = size;
  const bCtx = bumpCanvas.getContext('2d')!;

  eCtx.fillStyle = '#000000';
  eCtx.fillRect(0, 0, size, size);

  bCtx.fillStyle = '#808080';
  bCtx.fillRect(0, 0, size, size);

  for (let i = 0; i < 600; i++) {
    const y = Math.random() * size;
    const len = 30 + Math.random() * 140;
    const x = Math.random() * (size - len);
    bCtx.fillStyle = Math.random() > 0.5 ? 'rgba(255,255,255,0.08)' : 'rgba(0,0,0,0.12)';
    bCtx.fillRect(x, y, len, 1.5);
  }

  const drawRuneStroke = (drawFn: (ctx: CanvasRenderingContext2D) => void, lineWidth: number) => {
    eCtx.save();
    eCtx.strokeStyle = '#FFA000';
    eCtx.shadowColor = '#FFD23F';
    eCtx.shadowBlur = 12;
    eCtx.lineWidth = lineWidth + 2;
    drawFn(eCtx);
    eCtx.stroke();

    eCtx.strokeStyle = '#FFF3B0';
    eCtx.shadowBlur = 0;
    eCtx.lineWidth = Math.max(2, lineWidth - 2);
    drawFn(eCtx);
    eCtx.stroke();
    eCtx.restore();

    bCtx.save();
    bCtx.strokeStyle = '#181818';
    bCtx.lineWidth = lineWidth + 2;
    drawFn(bCtx);
    bCtx.stroke();
    bCtx.restore();
  };

  const cx = size / 2;
  const cy = size / 2;

  drawRuneStroke((ctx) => {
    ctx.beginPath();
    ctx.strokeRect(36, 48, size - 72, size - 96);
  }, 6);

  drawRuneStroke((ctx) => {
    ctx.beginPath();
    ctx.strokeRect(56, 68, size - 112, size - 136);
  }, 3);

  drawRuneStroke((ctx) => {
    ctx.beginPath();
    ctx.arc(cx, cy, 118, 0, Math.PI * 2);
  }, 6);

  drawRuneStroke((ctx) => {
    ctx.beginPath();
    ctx.arc(cx, cy, 82, 0, Math.PI * 2);
  }, 4);

  drawRuneStroke((ctx) => {
    ctx.beginPath();
    ctx.moveTo(cx, 68);
    ctx.lineTo(size - 72, cy);
    ctx.lineTo(cx, size - 68);
    ctx.lineTo(72, cy);
    ctx.closePath();
  }, 5);

  for (let i = 0; i < 8; i++) {
    const angle = (i * Math.PI) / 4;
    drawRuneStroke((ctx) => {
      ctx.beginPath();
      ctx.moveTo(cx + Math.cos(angle) * 36, cy + Math.sin(angle) * 36);
      ctx.lineTo(cx + Math.cos(angle) * 118, cy + Math.sin(angle) * 118);
    }, 4);
  }

  eCtx.fillStyle = '#FFD23F';
  eCtx.beginPath();
  eCtx.arc(cx, cy, 22, 0, Math.PI * 2);
  eCtx.fill();

  const emissiveMap = new THREE.CanvasTexture(emissiveCanvas);
  emissiveMap.colorSpace = THREE.SRGBColorSpace;
  emissiveMap.anisotropy = maxAnisotropy;

  const bumpMap = new THREE.CanvasTexture(bumpCanvas);
  bumpMap.anisotropy = maxAnisotropy;

  return { emissiveMap, bumpMap };
}

/**
 * Generates procedural Mythic Stone + Glowing Ancient Runes textures for the Octagonal Divine Hammer Head
 */
function createHammerStoneRuneTextures(maxAnisotropy: number) {
  const size = 512;
  const emissiveCanvas = document.createElement('canvas');
  emissiveCanvas.width = size;
  emissiveCanvas.height = size;
  const eCtx = emissiveCanvas.getContext('2d')!;

  const bumpCanvas = document.createElement('canvas');
  bumpCanvas.width = size;
  bumpCanvas.height = size;
  const bCtx = bumpCanvas.getContext('2d')!;

  eCtx.fillStyle = '#000000';
  eCtx.fillRect(0, 0, size, size);

  bCtx.fillStyle = '#707070';
  bCtx.fillRect(0, 0, size, size);

  // Ancient stone pitting & mineral grain on bump map
  for (let i = 0; i < 900; i++) {
    const x = Math.random() * size;
    const y = Math.random() * size;
    const r = 1 + Math.random() * 3.5;
    bCtx.fillStyle = Math.random() > 0.5 ? 'rgba(255,255,255,0.12)' : 'rgba(0,0,0,0.18)';
    bCtx.beginPath();
    bCtx.arc(x, y, r, 0, Math.PI * 2);
    bCtx.fill();
  }

  // Draw 8 panels of carved ancient Oriental-Cyber runes around the octagonal facets
  eCtx.strokeStyle = '#FFFFFF';
  eCtx.shadowColor = '#FFFFFF';
  eCtx.shadowBlur = 10;
  eCtx.lineWidth = 5;

  bCtx.strokeStyle = '#121212';
  bCtx.lineWidth = 7;

  // Upper & lower circumferential rune rings
  [95, 417].forEach((ry) => {
    eCtx.beginPath();
    eCtx.moveTo(0, ry);
    eCtx.lineTo(size, ry);
    eCtx.stroke();

    bCtx.beginPath();
    bCtx.moveTo(0, ry);
    bCtx.lineTo(size, ry);
    bCtx.stroke();
  });

  // 8 Octagonal Facet Ancient Glyphs (Cổ Tự Phát Sáng)
  const panelWidth = size / 8;
  for (let i = 0; i < 8; i++) {
    const px = i * panelWidth + panelWidth / 2;
    const py = size / 2;

    const drawGlyph = (ctx: CanvasRenderingContext2D) => {
      ctx.beginPath();
      // Outer diamond sigil
      ctx.moveTo(px, py - 95);
      ctx.lineTo(px + 22, py);
      ctx.lineTo(px, py + 95);
      ctx.lineTo(px - 22, py);
      ctx.closePath();
      // Vertical spine & crossbars
      ctx.moveTo(px, py - 115);
      ctx.lineTo(px, py + 115);
      ctx.moveTo(px - 18, py - 42);
      ctx.lineTo(px + 18, py - 42);
      ctx.moveTo(px - 18, py + 42);
      ctx.lineTo(px + 18, py + 42);
      ctx.stroke();
    };

    drawGlyph(eCtx);
    drawGlyph(bCtx);
  }

  const hammerEmissiveMap = new THREE.CanvasTexture(emissiveCanvas);
  hammerEmissiveMap.colorSpace = THREE.SRGBColorSpace;
  hammerEmissiveMap.wrapS = THREE.RepeatWrapping;
  hammerEmissiveMap.wrapT = THREE.ClampToEdgeWrapping;
  hammerEmissiveMap.anisotropy = maxAnisotropy;

  const hammerBumpMap = new THREE.CanvasTexture(bumpCanvas);
  hammerBumpMap.wrapS = THREE.RepeatWrapping;
  hammerBumpMap.wrapT = THREE.ClampToEdgeWrapping;
  hammerBumpMap.anisotropy = maxAnisotropy;

  return { hammerEmissiveMap, hammerBumpMap };
}

const RADIAL_RHYTHM_VERTEX_SHADER = `
  varying vec2 vUv;
  void main() {
    vUv = uv;
    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
  }
`;

const RADIAL_RHYTHM_FRAGMENT_SHADER = `
  varying vec2 vUv;
  uniform float uTime;
  uniform float uWaveProgress;
  uniform float uTargetRim;
  uniform float uRimFlash;
  uniform float uOverdrive;
  uniform vec3 uStanceColor;
  uniform vec3 uGoldColor;
  uniform vec3 uCyanColor;

  void main() {
    vec2 centered = vUv - vec2(0.5);
    float dist = length(centered);
    if (dist > 0.495) {
      discard;
    }

    float angle = atan(centered.y, centered.x);

    float outerR = 0.47;
    float innerR = 0.08;
    float waveR = mix(outerR, innerR, clamp(uWaveProgress, 0.0, 1.0));
    float rimR = mix(outerR, innerR, uTargetRim);

    float outerRing = smoothstep(0.008, 0.0, abs(dist - outerR)) * 0.35;
    float spokeMask = smoothstep(0.96, 1.0, cos(angle * 8.0)) * smoothstep(innerR, outerR, dist) * 0.14;
    float warmZone = smoothstep(0.055, 0.0, abs(dist - rimR)) * 0.16;

    float rimLine = smoothstep(0.012 + uRimFlash * 0.010, 0.0, abs(dist - rimR));
    float rimHalo = exp(-abs(dist - rimR) * (42.0 - uRimFlash * 18.0)) * (0.45 + uRimFlash * 1.15);

    float runeWaveMod = 0.003 * sin(angle * 12.0 - uTime * 6.0);
    float dWave = abs(dist - (waveR + runeWaveMod));
    float waveCore = smoothstep(0.013, 0.001, dWave);
    float waveGlow = exp(-dWave * 36.0) * 0.78;
    float wake = smoothstep(waveR, waveR + 0.065, dist) * step(dist, waveR + 0.065) * 0.25;

    vec3 activeWaveCol = mix(uCyanColor, uStanceColor, 0.55);
    if (uOverdrive > 0.5) {
      activeWaveCol = mix(uCyanColor, uGoldColor, 0.5 + 0.5 * sin(uTime * 14.0));
    }
    vec3 finalWaveCol = mix(activeWaveCol, uGoldColor, clamp(uRimFlash * 1.25, 0.0, 1.0));

    vec3 color = vec3(0.0);
    color += uStanceColor * (outerRing + spokeMask);
    color += vec3(1.0, 0.55, 0.1) * warmZone;
    color += mix(uGoldColor, vec3(1.0, 0.97, 0.82), uRimFlash) * (rimLine * (1.1 + uRimFlash * 1.4) + rimHalo);
    color += finalWaveCol * (waveCore * 1.35 + waveGlow + wake);

    float alpha = clamp(
      outerRing + spokeMask + warmZone + rimLine * 0.95 + rimHalo * 0.8 + waveCore + waveGlow * 0.85 + wake,
      0.0,
      0.98
    );

    gl_FragColor = vec4(color, alpha);
  }
`;

/**
 * GPU Vertex Shader for the 3,000-particle Spark System (THREE.Points):
 * Evaluates upward launch velocity, gravity (uGravity), air drag, anvil floor bounce,
 * perspective point sizing, and fade-out entirely on the GPU for 60 FPS on mobile & desktop.
 */
const FORGE_SPARKS_VERTEX_SHADER = `
  attribute vec3 aVelocity;
  attribute vec3 aColor;
  attribute vec3 aTiming; // x: spawnTime, y: duration, z: basePointSize
  attribute float aAlpha;

  uniform float uTime;
  uniform float uGravity;
  uniform float uPixelRatio;

  varying vec3 vColor;
  varying float vAlpha;

  void main() {
    float age = uTime - aTiming.x;
    float duration = max(0.05, aTiming.y);

    if (age < 0.0 || age > duration || aAlpha <= 0.001) {
      gl_Position = vec4(0.0, 0.0, 2.0, 1.0);
      gl_PointSize = 0.0;
      vAlpha = 0.0;
      vColor = vec3(0.0);
      return;
    }

    float lifeRatio = clamp(age / duration, 0.0, 1.0);

    // Ballistic arc under gravity: p(t) = p0 + v0 * age - 0.5 * g * age^2
    float drag = 1.0 - lifeRatio * 0.24;
    vec3 worldPos = position;
    worldPos.x += aVelocity.x * age * drag;
    worldPos.y += aVelocity.y * age - 0.5 * uGravity * age * age;
    worldPos.z += aVelocity.z * age * drag;

    // Elastic micro-bounce if sparks reach the anvil plinth floor (y < -0.95)
    if (worldPos.y < -0.95) {
      worldPos.y = -0.95 + abs(worldPos.y + 0.95) * 0.28;
    }

    vec4 mvPosition = modelViewMatrix * vec4(worldPos, 1.0);
    gl_Position = projectionMatrix * mvPosition;

    float fadeOut = 1.0 - smoothstep(0.35, 1.0, lifeRatio);
    vAlpha = aAlpha * fadeOut;
    vColor = aColor;

    float dist = max(1.2, -mvPosition.z);
    gl_PointSize = clamp(aTiming.z * uPixelRatio * (5.2 / dist) * (0.65 + 0.35 * fadeOut), 3.0, 48.0);
  }
`;

const FORGE_SPARKS_FRAGMENT_SHADER = `
  varying vec3 vColor;
  varying float vAlpha;

  void main() {
    if (vAlpha <= 0.01) {
      discard;
    }
    vec2 uv = gl_PointCoord - vec2(0.5);
    float dist = length(uv);
    if (dist > 0.5) {
      discard;
    }

    // Hot white-gold diamond core + soft radial ember halo
    float diamond = max(0.0, 1.0 - (abs(uv.x) + abs(uv.y)) * 2.1);
    float core = smoothstep(0.28, 0.0, dist);
    float halo = exp(-dist * 5.2);
    float intensity = clamp(core * 1.35 + diamond * 0.7 + halo * 0.9, 0.0, 1.8);

    vec3 finalCol = mix(vColor, vec3(1.0, 0.99, 0.94), core * 0.7);
    gl_FragColor = vec4(finalCol * intensity, clamp(vAlpha * (halo * 0.95 + core), 0.0, 1.0));
  }
`;

export const CelestialAnvil3D = forwardRef<CelestialAnvil3DHandle, CelestialAnvil3DProps>(
  (
    {
      waveProgressRef,
      currentStance,
      overdriveActive,
      globalBurstActive,
      lastStrikeId,
      lastStrikeGrade,
      onStrike,
    },
    ref
  ) => {
    const mountRef = useRef<HTMLDivElement | null>(null);
    const imperativeStrikeTriggerRef = useRef<number>(0);
    const peerStrikeQueueRef = useRef<PeerStrikeQuality[]>([]);

    // Expose imperative strike() and onPeerStrike(quality) methods
    useImperativeHandle(ref, () => ({
      strike: () => {
        imperativeStrikeTriggerRef.current += 1;
        onStrike();
      },
      onPeerStrike: (quality: PeerStrikeQuality = 'GREAT') => {
        peerStrikeQueueRef.current.push(quality);
      },
    }));

    const livePropsRef = useRef({
      currentStance,
      overdriveActive,
      globalBurstActive,
      lastStrikeId,
      lastStrikeGrade,
    });

    useEffect(() => {
      livePropsRef.current = {
        currentStance,
        overdriveActive,
        globalBurstActive,
        lastStrikeId,
        lastStrikeGrade,
      };
    }, [currentStance, overdriveActive, globalBurstActive, lastStrikeId, lastStrikeGrade]);

    useEffect(() => {
      const container = mountRef.current;
      if (!container) return;

      const isSoftwareGl = (() => {
        try {
          const probeCanvas = document.createElement('canvas');
          const gl = probeCanvas.getContext('webgl2') || probeCanvas.getContext('webgl');
          if (!gl) return true;
          const ext = gl.getExtension('WEBGL_debug_renderer_info');
          const param = ext ? ext.UNMASKED_RENDERER_WEBGL : gl.RENDERER;
          const gpu = String(gl.getParameter(param));
          gl.getExtension('WEBGL_lose_context')?.loseContext();
          return /SwiftShader|llvmpipe|softpipe|Software|Basic Render/i.test(gpu);
        } catch {
          return true;
        }
      })();

      const scene = new THREE.Scene();
      const bgHex = 0x080a10;
      scene.background = new THREE.Color(bgHex);
      scene.fog = new THREE.FogExp2(bgHex, 0.055);

      const width = Math.max(300, container.clientWidth || 520);
      const height = Math.max(300, container.clientHeight || 420);

      const camera = new THREE.PerspectiveCamera(40, width / height, 0.1, 60);
      const baseCamPos = new THREE.Vector3(0, 4.35, 5.25);
      const baseLookAt = new THREE.Vector3(0, 0.12, 0);
      camera.position.copy(baseCamPos);
      camera.lookAt(baseLookAt);

      const renderer = new THREE.WebGLRenderer({
        antialias: !isSoftwareGl,
        powerPreference: 'high-performance',
      });
      renderer.outputColorSpace = THREE.SRGBColorSpace;
      renderer.toneMapping = THREE.ACESFilmicToneMapping;
      renderer.toneMappingExposure = 1.18;
      renderer.setPixelRatio(isSoftwareGl ? 1 : Math.min(window.devicePixelRatio, 2));
      renderer.setSize(width, height);
      renderer.shadowMap.enabled = !isSoftwareGl;
      renderer.shadowMap.type = THREE.PCFSoftShadowMap;

      renderer.domElement.setAttribute('data-testid', 'three-forge-canvas');
      renderer.domElement.style.width = '100%';
      renderer.domElement.style.height = '100%';
      renderer.domElement.style.display = 'block';
      container.innerHTML = '';
      container.appendChild(renderer.domElement);

      const pmremGenerator = new THREE.PMREMGenerator(renderer);
      const envTarget = pmremGenerator.fromScene(new RoomEnvironment(), 0.04);
      scene.environment = envTarget.texture;
      pmremGenerator.dispose();

      // LIGHTING & ENVIRONMENT
      const hemiLight = new THREE.HemisphereLight(0x0099ff, 0xff4500, 0.85);
      hemiLight.position.set(0, 8, 0);
      scene.add(hemiLight);

      const cyanDirLight = new THREE.DirectionalLight(0x00f0ff, 3.6);
      cyanDirLight.position.set(-3.2, 6.2, 3.4);
      if (!isSoftwareGl) {
        cyanDirLight.castShadow = true;
        cyanDirLight.shadow.mapSize.set(1024, 1024);
        const d = 4.5;
        cyanDirLight.shadow.camera.left = -d;
        cyanDirLight.shadow.camera.right = d;
        cyanDirLight.shadow.camera.top = d;
        cyanDirLight.shadow.camera.bottom = -d;
        cyanDirLight.shadow.camera.near = 0.5;
        cyanDirLight.shadow.camera.far = 16;
        cyanDirLight.shadow.bias = -0.0005;
      }
      scene.add(cyanDirLight);

      const fireUnderLight = new THREE.PointLight(0xff6b00, 22, 10, 1.5);
      fireUnderLight.position.set(0, -0.45, 0.85);
      scene.add(fireUnderLight);

      const fireBackLight = new THREE.PointLight(0xff3b30, 14, 9, 1.5);
      fireBackLight.position.set(0, -0.35, -0.95);
      scene.add(fireBackLight);

      const rimPulseLight = new THREE.PointLight(0xffd23f, 4.0, 7, 1.8);
      rimPulseLight.position.set(0, 1.15, 0);
      scene.add(rimPulseLight);

      // PROCEDURAL THẦN ĐE (Anvil)
      const maxAniso = renderer.capabilities.getMaxAnisotropy();
      const { emissiveMap, bumpMap } = createAnvilRuneTextures(maxAniso);
      const { hammerEmissiveMap, hammerBumpMap } = createHammerStoneRuneTextures(maxAniso);

      const anvilGroup = new THREE.Group();
      scene.add(anvilGroup);

      const shadowDiscGeo = new THREE.CircleGeometry(2.8, 32);
      shadowDiscGeo.rotateX(-Math.PI / 2);
      const shadowDiscMat = new THREE.MeshBasicMaterial({
        color: 0x020408,
        transparent: true,
        opacity: 0.65,
        depthWrite: false,
      });
      const shadowDisc = new THREE.Mesh(shadowDiscGeo, shadowDiscMat);
      shadowDisc.position.y = -1.18;
      anvilGroup.add(shadowDisc);

      const darkObsidianMat = new THREE.MeshStandardMaterial({
        color: 0x111625,
        metalness: 0.78,
        roughness: 0.52,
        bumpMap,
        bumpScale: 0.015,
      });

      const forgedSteelShoulderMat = new THREE.MeshStandardMaterial({
        color: 0x1e293b,
        metalness: 0.86,
        roughness: 0.32,
        bumpMap,
        bumpScale: 0.02,
      });

      const anvilTopFaceMat = new THREE.MeshStandardMaterial({
        color: 0x283548,
        metalness: 0.9,
        roughness: 0.2,
        bumpMap,
        bumpScale: 0.035,
        emissive: new THREE.Color(0xffd23f),
        emissiveMap,
        emissiveIntensity: 1.45,
      });

      const goldenRimMat = new THREE.MeshStandardMaterial({
        color: 0xffd23f,
        metalness: 0.92,
        roughness: 0.18,
        emissive: new THREE.Color(0xffa000),
        emissiveIntensity: 0.95,
      });

      const magmaCoreMat = new THREE.MeshStandardMaterial({
        color: 0xff3b30,
        roughness: 0.3,
        metalness: 0.2,
        emissive: new THREE.Color(0xff6b00),
        emissiveIntensity: 2.4,
      });

      const basePlinthGeo = new THREE.CylinderGeometry(1.75, 2.05, 0.36, 8);
      basePlinthGeo.rotateY(Math.PI / 8);
      const basePlinth = new THREE.Mesh(basePlinthGeo, darkObsidianMat);
      basePlinth.position.y = -1.0;
      basePlinth.receiveShadow = true;
      anvilGroup.add(basePlinth);

      const stepBoxGeo = new THREE.BoxGeometry(2.3, 0.22, 1.48);
      const stepBox = new THREE.Mesh(stepBoxGeo, forgedSteelShoulderMat);
      stepBox.position.y = -0.72;
      anvilGroup.add(stepBox);

      const waistGeo = new THREE.BoxGeometry(1.68, 0.72, 1.12);
      const waistMesh = new THREE.Mesh(waistGeo, darkObsidianMat);
      waistMesh.position.y = -0.26;
      anvilGroup.add(waistMesh);

      const coreSlitGeo = new THREE.BoxGeometry(0.92, 0.34, 1.16);
      const coreSlit = new THREE.Mesh(coreSlitGeo, magmaCoreMat);
      coreSlit.position.y = -0.26;
      anvilGroup.add(coreSlit);

      const buttressGeo = new THREE.CylinderGeometry(0.16, 0.24, 0.76, 6);
      [
        [-0.86, -0.26, 0.56],
        [0.86, -0.26, 0.56],
        [-0.86, -0.26, -0.56],
        [0.86, -0.26, -0.56],
      ].forEach(([bx, by, bz]) => {
        const col = new THREE.Mesh(buttressGeo, forgedSteelShoulderMat);
        col.position.set(bx, by, bz);
        anvilGroup.add(col);
      });

      const leftHornGeo = new THREE.CylinderGeometry(0.18, 0.58, 1.05, 4);
      leftHornGeo.rotateY(Math.PI / 4);
      leftHornGeo.rotateZ(Math.PI / 2);
      const leftHorn = new THREE.Mesh(leftHornGeo, forgedSteelShoulderMat);
      leftHorn.position.set(-1.52, 0.14, 0);
      leftHorn.scale.set(1.0, 1.0, 1.45);
      anvilGroup.add(leftHorn);

      const rightHornGeo = new THREE.CylinderGeometry(0.22, 0.58, 0.95, 4);
      rightHornGeo.rotateY(Math.PI / 4);
      rightHornGeo.rotateZ(-Math.PI / 2);
      const rightHorn = new THREE.Mesh(rightHornGeo, forgedSteelShoulderMat);
      rightHorn.position.set(1.48, 0.14, 0);
      rightHorn.scale.set(1.0, 1.0, 1.45);
      anvilGroup.add(rightHorn);

      const topFaceGeo = new THREE.BoxGeometry(2.36, 0.26, 1.42);
      const topFaceMesh = new THREE.Mesh(topFaceGeo, anvilTopFaceMat);
      topFaceMesh.position.y = 0.22;
      topFaceMesh.castShadow = true;
      topFaceMesh.receiveShadow = true;
      anvilGroup.add(topFaceMesh);

      const frontBackRimGeo = new THREE.BoxGeometry(2.44, 0.06, 0.06);
      const frontRim = new THREE.Mesh(frontBackRimGeo, goldenRimMat);
      frontRim.position.set(0, 0.35, 0.72);
      const backRim = new THREE.Mesh(frontBackRimGeo, goldenRimMat);
      backRim.position.set(0, 0.35, -0.72);
      const sideRimGeo = new THREE.BoxGeometry(0.06, 0.06, 1.48);
      const leftRim = new THREE.Mesh(sideRimGeo, goldenRimMat);
      leftRim.position.set(-1.2, 0.35, 0);
      const rightRim = new THREE.Mesh(sideRimGeo, goldenRimMat);
      rightRim.position.set(1.2, 0.35, 0);
      anvilGroup.add(frontRim, backRim, leftRim, rightRim);

      // ============================================================================
      // THẦN CHÙY (DIVINE HAMMER) - Long Leather-Wrapped Handle + Octagonal Stone Head
      // ============================================================================
      // Pivot positioned at (1.58, 0.82, 0):
      // - When rotation.z === 0 (Strike Impact): Hammer handle is horizontal and the Octagonal Head sits at (0, 0.82, 0), striking perpendicular to the Anvil face!
      // - When rotation.z === -Math.PI / 4 (Idle 45 degrees): Hammer is raised at a 45-degree angle above the Anvil!
      const hammerPivot = new THREE.Group();
      hammerPivot.position.set(1.58, 0.82, 0);
      scene.add(hammerPivot);

      // 1A. Long Leather-Wrapped Handle (Cán búa dài bọc da)
      const leatherShaftMat = new THREE.MeshStandardMaterial({
        color: 0x4a2511, // Deep saddle leather brown
        roughness: 0.78,
        metalness: 0.12,
        bumpMap,
        bumpScale: 0.025,
      });

      const leatherBandMat = new THREE.MeshStandardMaterial({
        color: 0x2e1508, // Darker braided leather wrap bands
        roughness: 0.85,
        metalness: 0.08,
      });

      const bronzeTrimMat = new THREE.MeshStandardMaterial({
        color: 0xffd23f,
        metalness: 0.9,
        roughness: 0.22,
      });

      // Main long handle shaft along negative X from pivot (0) to hammer head (-1.58)
      const shaftGeo = new THREE.CylinderGeometry(0.068, 0.085, 1.92, 12);
      shaftGeo.rotateZ(Math.PI / 2);
      const shaftMesh = new THREE.Mesh(shaftGeo, leatherShaftMat);
      shaftMesh.position.set(-0.78, 0, 0);
      hammerPivot.add(shaftMesh);

      // Braided Leather Grip Rings along the shaft
      const gripRingGeo = new THREE.TorusGeometry(0.082, 0.018, 8, 16);
      gripRingGeo.rotateY(Math.PI / 2);
      for (let g = 0; g < 7; g++) {
        const ring = new THREE.Mesh(gripRingGeo, g % 2 === 0 ? leatherBandMat : bronzeTrimMat);
        ring.position.set(-0.08 - g * 0.18, 0, 0);
        hammerPivot.add(ring);
      }

      // Pommel End-Cap (Đốc búa đồng thau bát giác)
      const pommelGeo = new THREE.CylinderGeometry(0.13, 0.09, 0.18, 8);
      pommelGeo.rotateZ(Math.PI / 2);
      const pommelMesh = new THREE.Mesh(pommelGeo, bronzeTrimMat);
      pommelMesh.position.set(0.18, 0, 0);
      hammerPivot.add(pommelMesh);

      // Heavy Golden-Bronze Collar Guard meeting the Hammer Head
      const collarGeo = new THREE.CylinderGeometry(0.18, 0.13, 0.24, 8);
      collarGeo.rotateZ(Math.PI / 2);
      const collarMesh = new THREE.Mesh(collarGeo, bronzeTrimMat);
      collarMesh.position.set(-1.42, 0, 0);
      hammerPivot.add(collarMesh);

      // 1B. Octagonal Mythic Stone Hammer Head with Glowing Carved Ancient Runes
      const hammerHeadGroup = new THREE.Group();
      hammerHeadGroup.position.set(-1.58, 0, 0);
      hammerPivot.add(hammerHeadGroup);

      const mythicStoneHeadMat = new THREE.MeshStandardMaterial({
        color: 0x1e2536, // Dark mythic basalt/obsidian stone
        roughness: 0.42,
        metalness: 0.55,
        bumpMap: hammerBumpMap,
        bumpScale: 0.045,
        emissive: new THREE.Color(0x00f0ff),
        emissiveMap: hammerEmissiveMap,
        emissiveIntensity: 2.2,
      });

      // 8-sided Octagonal Stone Prism oriented vertically (perpendicular to anvil when striking)
      const octHeadGeo = new THREE.CylinderGeometry(0.39, 0.39, 0.96, 8);
      octHeadGeo.rotateY(Math.PI / 8);
      const octHeadMesh = new THREE.Mesh(octHeadGeo, mythicStoneHeadMat);
      octHeadMesh.castShadow = true;
      hammerHeadGroup.add(octHeadMesh);

      // Bottom & Top Beveled Octagonal Striking Caps
      const capGeo = new THREE.CylinderGeometry(0.39, 0.31, 0.12, 8);
      capGeo.rotateY(Math.PI / 8);
      const bottomStrikeCap = new THREE.Mesh(capGeo, forgedSteelShoulderMat);
      bottomStrikeCap.position.y = -0.52;
      hammerHeadGroup.add(bottomStrikeCap);

      const topStrikeCap = new THREE.Mesh(capGeo, forgedSteelShoulderMat);
      topStrikeCap.rotation.z = Math.PI;
      topStrikeCap.position.y = 0.52;
      hammerHeadGroup.add(topStrikeCap);

      // Central Golden Rune Band wrapping the Octagonal Head
      const centerBandGeo = new THREE.CylinderGeometry(0.415, 0.415, 0.14, 8);
      centerBandGeo.rotateY(Math.PI / 8);
      const centerBandMesh = new THREE.Mesh(centerBandGeo, bronzeTrimMat);
      hammerHeadGroup.add(centerBandMesh);

      // ============================================================================
      // 3. 4 THẾ BÚA (STANCE SKINS) VISUAL FX MESHES
      // ============================================================================
      // Skin 1: 'THUNDER' (Lôi Đỉnh) - Neon Cyan Wireframe Lightning Cage (MeshBasicMaterial wireframe jitter)
      const thunderCageGroup = new THREE.Group();
      hammerHeadGroup.add(thunderCageGroup);

      const thunderWireMat1 = new THREE.MeshBasicMaterial({
        color: 0x00f0ff,
        wireframe: true,
        transparent: true,
        opacity: 0.85,
        blending: THREE.AdditiveBlending,
      });
      const thunderWireMat2 = new THREE.MeshBasicMaterial({
        color: 0x80f8ff,
        wireframe: true,
        transparent: true,
        opacity: 0.65,
        blending: THREE.AdditiveBlending,
      });

      const thunderCageGeo1 = new THREE.IcosahedronGeometry(0.58, 1);
      const thunderCageMesh1 = new THREE.Mesh(thunderCageGeo1, thunderWireMat1);
      thunderCageMesh1.scale.set(0.95, 1.25, 0.95);
      thunderCageGroup.add(thunderCageMesh1);

      const thunderCageGeo2 = new THREE.OctahedronGeometry(0.64, 1);
      const thunderCageMesh2 = new THREE.Mesh(thunderCageGeo2, thunderWireMat2);
      thunderCageMesh2.scale.set(0.9, 1.3, 0.9);
      thunderCageGroup.add(thunderCageMesh2);

      // Skin 2: 'FIRE' (Viêm Dương) - Rising Fire & Smoke Plumes around Hammer Head
      const firePlumeGroup = new THREE.Group();
      hammerHeadGroup.add(firePlumeGroup);

      const firePuffs: Array<{
        mesh: THREE.Mesh;
        mat: THREE.MeshStandardMaterial;
        phase: number;
        radius: number;
        angle: number;
      }> = [];
      const puffGeo = new THREE.DodecahedronGeometry(0.14, 0);
      for (let i = 0; i < 14; i++) {
        const isSmoke = i % 3 === 0;
        const puffMat = new THREE.MeshStandardMaterial({
          color: isSmoke ? 0x1e293b : 0xff3b30,
          emissive: new THREE.Color(isSmoke ? 0xff4500 : 0xff6b00),
          emissiveIntensity: isSmoke ? 0.8 : 2.8,
          roughness: 0.7,
          transparent: true,
          opacity: 0.85,
        });
        const puffMesh = new THREE.Mesh(puffGeo, puffMat);
        firePlumeGroup.add(puffMesh);
        firePuffs.push({
          mesh: puffMesh,
          mat: puffMat,
          phase: (i / 14) * Math.PI * 2,
          radius: 0.34 + (i % 3) * 0.08,
          angle: (i / 14) * Math.PI * 2,
        });
      }

      // Skin 3: 'GRAVITY' (Trọng Lực) - Deep Purple Gravity Halo & Distortion Rings
      const gravityAuraGroup = new THREE.Group();
      hammerHeadGroup.add(gravityAuraGroup);

      const gravityShellMat = new THREE.MeshBasicMaterial({
        color: 0x9333ea,
        transparent: true,
        opacity: 0.38,
        side: THREE.DoubleSide,
        blending: THREE.AdditiveBlending,
        depthWrite: false,
      });
      const gravityRingMat = new THREE.MeshBasicMaterial({
        color: 0xc084fc,
        wireframe: true,
        transparent: true,
        opacity: 0.75,
        blending: THREE.AdditiveBlending,
      });

      const gravityShellGeo = new THREE.CylinderGeometry(0.54, 0.54, 1.15, 8, 1, true);
      const gravityShellMesh = new THREE.Mesh(gravityShellGeo, gravityShellMat);
      gravityAuraGroup.add(gravityShellMesh);

      const gravityTorusGeo = new THREE.TorusGeometry(0.62, 0.035, 8, 24);
      const gravityOrbit1 = new THREE.Mesh(gravityTorusGeo, gravityRingMat);
      const gravityOrbit2 = new THREE.Mesh(gravityTorusGeo, gravityRingMat);
      gravityOrbit2.rotation.x = Math.PI / 2;
      gravityAuraGroup.add(gravityOrbit1, gravityOrbit2);

      // Skin 4: 'MYSTIC' (Huyền Âm) - Jade-Emerald Translucent Expanding Soundwave Rings
      const mysticWaveGroup = new THREE.Group();
      mysticWaveGroup.position.set(0, 0.38, 0);
      scene.add(mysticWaveGroup);

      const mysticHeadRingsGroup = new THREE.Group();
      hammerHeadGroup.add(mysticHeadRingsGroup);

      const mysticSonicRings: Array<{
        mesh: THREE.Mesh;
        mat: THREE.MeshBasicMaterial;
        offset: number;
      }> = [];
      const sonicRingGeo = new THREE.RingGeometry(0.42, 0.52, 36);
      sonicRingGeo.rotateX(-Math.PI / 2);

      for (let w = 0; w < 4; w++) {
        const wMat = new THREE.MeshBasicMaterial({
          color: w % 2 === 0 ? 0x10b981 : 0x2dd4bf, // Jade-emerald (xanh ngọc bích)
          transparent: true,
          opacity: 0.65,
          side: THREE.DoubleSide,
          blending: THREE.AdditiveBlending,
          depthWrite: false,
        });
        const wMesh = new THREE.Mesh(sonicRingGeo, wMat);
        mysticWaveGroup.add(wMesh);
        mysticSonicRings.push({
          mesh: wMesh,
          mat: wMat,
          offset: w * 0.25,
        });
      }

      // Jade halo around hammer head in MYSTIC stance
      const mysticHaloGeo = new THREE.RingGeometry(0.46, 0.56, 24);
      const mysticHaloMat = new THREE.MeshBasicMaterial({
        color: 0x2dd4bf,
        transparent: true,
        opacity: 0.6,
        side: THREE.DoubleSide,
        blending: THREE.AdditiveBlending,
      });
      const mysticHeadHalo = new THREE.Mesh(mysticHaloGeo, mysticHaloMat);
      mysticHeadRingsGroup.add(mysticHeadHalo);

      // VÒNG NHỊP RADIAL (Horizontal Plane + Custom GLSL Fragment Shader at 100 BPM)
      const rhythmPlaneGeo = new THREE.PlaneGeometry(7.2, 7.2, 1, 1);
      rhythmPlaneGeo.rotateX(-Math.PI / 2);

      const initialStanceKey = STANCE_KEY_BY_ID[currentStance] || 'Q';
      const rhythmUniforms = {
        uTime: { value: 0 },
        uWaveProgress: { value: waveProgressRef.current },
        uTargetRim: { value: TARGET_RIM_PROGRESS },
        uRimFlash: { value: 0 },
        uOverdrive: { value: 0 },
        uStanceColor: { value: new THREE.Color(HAMMER_STANCES[initialStanceKey].color) },
        uGoldColor: { value: new THREE.Color(0xffd23f) },
        uCyanColor: { value: new THREE.Color(0x00f0ff) },
      };

      const rhythmShaderMat = new THREE.ShaderMaterial({
        uniforms: rhythmUniforms,
        vertexShader: RADIAL_RHYTHM_VERTEX_SHADER,
        fragmentShader: RADIAL_RHYTHM_FRAGMENT_SHADER,
        transparent: true,
        depthWrite: false,
        side: THREE.DoubleSide,
        blending: THREE.AdditiveBlending,
        polygonOffset: true,
        polygonOffsetFactor: -1,
        polygonOffsetUnits: -1,
      });

      const rhythmPlaneMesh = new THREE.Mesh(rhythmPlaneGeo, rhythmShaderMat);
      rhythmPlaneMesh.position.y = 0.36;
      rhythmPlaneMesh.renderOrder = 2;
      scene.add(rhythmPlaneMesh);

      // ============================================================================
      // 3,000-PARTICLE GPU SPARK SYSTEM (THREE.Points + Float32Array + GPU Vertex Shader)
      // - Self Strike: Large, dazzling golden sparks (#FFD23F / #FFF6C2)
      // - Peer Strike (onPeerStrike Ghost Sparks): Smaller translucent white/pale-cyan sparks
      // ============================================================================
      const sparkBuffer = createForgeSparkBuffer(FORGE_SPARK_BUFFER_SIZE);

      const sparkGeo = new THREE.BufferGeometry();
      const posAttr = new THREE.BufferAttribute(sparkBuffer.positions, 3);
      const velAttr = new THREE.BufferAttribute(sparkBuffer.velocities, 3);
      const colAttr = new THREE.BufferAttribute(sparkBuffer.colors, 3);
      const timAttr = new THREE.BufferAttribute(sparkBuffer.timings, 3);
      const alpAttr = new THREE.BufferAttribute(sparkBuffer.alphas, 1);

      posAttr.setUsage(THREE.DynamicDrawUsage);
      velAttr.setUsage(THREE.DynamicDrawUsage);
      colAttr.setUsage(THREE.DynamicDrawUsage);
      timAttr.setUsage(THREE.DynamicDrawUsage);
      alpAttr.setUsage(THREE.DynamicDrawUsage);

      sparkGeo.setAttribute('position', posAttr);
      sparkGeo.setAttribute('aVelocity', velAttr);
      sparkGeo.setAttribute('aColor', colAttr);
      sparkGeo.setAttribute('aTiming', timAttr);
      sparkGeo.setAttribute('aAlpha', alpAttr);

      const sparkUniforms = {
        uTime: { value: 0 },
        uGravity: { value: SPARK_GRAVITY },
        uPixelRatio: { value: renderer.getPixelRatio() },
      };

      const sparkMat = new THREE.ShaderMaterial({
        uniforms: sparkUniforms,
        vertexShader: FORGE_SPARKS_VERTEX_SHADER,
        fragmentShader: FORGE_SPARKS_FRAGMENT_SHADER,
        transparent: true,
        depthWrite: false,
        blending: THREE.AdditiveBlending,
      });

      const sparkPoints = new THREE.Points(sparkGeo, sparkMat);
      sparkPoints.frustumCulled = false;
      sparkPoints.renderOrder = 3;
      scene.add(sparkPoints);

      const markSparkAttributesDirty = () => {
        posAttr.needsUpdate = true;
        velAttr.needsUpdate = true;
        colAttr.needsUpdate = true;
        timAttr.needsUpdate = true;
        alpAttr.needsUpdate = true;
      };

      const emitPeerStrikeSparks = (quality: PeerStrikeQuality, currentTime: number) => {
        spawnForgeSparkBurst(sparkBuffer, {
          origin: 'PEER',
          quality,
          currentTime,
        });
        markSparkAttributesDirty();
      };

      const emitSelfStrikeSparks = (quality: JudgmentGrade, currentTime: number) => {
        spawnForgeSparkBurst(sparkBuffer, {
          origin: 'SELF',
          quality,
          currentTime,
        });
        markSparkAttributesDirty();
      };

      // Seed initial Ghost Sparks so the anvil immediately radiates with peer blacksmith activity
      for (let s = 0; s < 18; s++) {
        spawnForgeSparkBurst(sparkBuffer, {
          origin: 'PEER',
          quality: s % 2 === 0 ? 'PERFECT' : 'GREAT',
          currentTime: -s * 0.035,
        });
      }
      markSparkAttributesDirty();

      // Expose global helper for automated verification & external peer event hooks
      (window as unknown as Record<string, unknown>).__celestialForge = {
        onPeerStrike: (quality: PeerStrikeQuality = 'GREAT') => {
          peerStrikeQueueRef.current.push(quality);
        },
        strike: () => {
          imperativeStrikeTriggerRef.current += 1;
          onStrike();
        },
        getSparkStats: () => ({
          bufferCapacity: sparkBuffer.capacity,
          cursor: sparkBuffer.cursor,
          totalSpawned: sparkBuffer.totalSpawned,
        }),
      };

      if (!isSoftwareGl) {
        renderer.compile(scene, camera);
      }

      const ro = new ResizeObserver(() => {
        if (!container) return;
        const w = Math.max(260, container.clientWidth);
        const h = Math.max(260, container.clientHeight);
        camera.aspect = w / h;
        camera.updateProjectionMatrix();
        renderer.setSize(w, h);
        sparkUniforms.uPixelRatio.value = renderer.getPixelRatio();
      });
      ro.observe(container);

      let frameId = 0;
      let lastTime = performance.now();
      let elapsed = 0;
      let peerSpawnTimer = 0;
      let handledStrikeId = livePropsRef.current.lastStrikeId;
      let handledImperativeId = imperativeStrikeTriggerRef.current;
      // strikeElapsed < 0 means idle at 45 degrees; >= 0 means active strike animation (0..0.08s slam, 0.08..0.32s rebound)
      let strikeElapsed = -1;
      let cameraTrauma = 0;

      function afterDraw(cb: () => void) {
        const gl = renderer.getContext() as WebGL2RenderingContext;
        if (gl && typeof gl.fenceSync === 'function') {
          const sync = gl.fenceSync(gl.SYNC_GPU_COMMANDS_COMPLETE, 0);
          gl.flush();
          const poll = () => {
            const state = sync && gl.getSyncParameter(sync, gl.SYNC_STATUS);
            if (state === gl.UNSIGNALED) {
              frameId = window.setTimeout(poll, 5);
            } else {
              if (sync) gl.deleteSync(sync);
              frameId = window.setTimeout(cb, 80);
            }
          };
          frameId = window.setTimeout(poll, 5);
        } else {
          frameId = window.setTimeout(cb, 80);
        }
      }

      const tick = () => {
        const now = performance.now();
        const dt = Math.min((now - lastTime) / 1000, 0.05);
        lastTime = now;
        elapsed += dt;

        // Advance the 100 BPM Radial Rhythm Wave directly in lockstep with the 3D shader render loop
        const speed = FORGE_BPM / 60 / 2;
        let nextWave = waveProgressRef.current + dt * speed;
        if (nextWave >= 1.0) {
          nextWave -= 1.0;
        }
        waveProgressRef.current = nextWave;

        const props = livePropsRef.current;
        const stanceId = props.currentStance;
        const stanceKey = STANCE_KEY_BY_ID[stanceId] || 'Q';
        const stanceCfg = HAMMER_STANCES[stanceKey];
        const waveProg = waveProgressRef.current;

        // Process queued external onPeerStrike(quality) events (Ghost Sparks)
        while (peerStrikeQueueRef.current.length > 0) {
          const q = peerStrikeQueueRef.current.shift()!;
          emitPeerStrikeSparks(q, elapsed);
        }

        // Simulate continuous real-time peer strikes from the 14,820 Vạn Dân blacksmiths
        // Higher frequency when the 100 BPM rhythm wave crosses the Golden Anvil Rim or during Global Burst
        const nearRim = Math.abs(waveProg - TARGET_RIM_PROGRESS) < 0.14;
        const peerInterval = props.globalBurstActive ? 0.045 : nearRim ? 0.065 : 0.12;
        peerSpawnTimer += dt;
        if (peerSpawnTimer >= peerInterval) {
          peerSpawnTimer = 0;
          const peerQuality: PeerStrikeQuality =
            nearRim || Math.random() > 0.45 ? 'PERFECT' : 'GREAT';
          emitPeerStrikeSparks(peerQuality, elapsed);
        }

        // Trigger Self Strike animation & large Dazzling Golden Sparks when lastStrikeId or imperative strike() updates
        if (
          props.lastStrikeId !== handledStrikeId ||
          imperativeStrikeTriggerRef.current !== handledImperativeId
        ) {
          handledStrikeId = props.lastStrikeId;
          handledImperativeId = imperativeStrikeTriggerRef.current;
          strikeElapsed = 0; // Starts 0.08s downstroke to perpendicular (0 rad)

          // Gravity stance ('GRAVITY') produces amplified camera tremor on impact
          const baseTrauma = props.lastStrikeGrade === 'PERFECT' ? 0.38 : 0.2;
          cameraTrauma = stanceId === 'GRAVITY' ? baseTrauma * 1.85 : baseTrauma;

          if (props.lastStrikeGrade !== 'MISS') {
            emitSelfStrikeSparks(props.lastStrikeGrade, elapsed);
          }
        }

        // Advance Hammer Strike timer & compute smooth angle (45 deg idle -> 0 rad in 0.08s -> 45 deg rebound)
        if (strikeElapsed >= 0) {
          strikeElapsed += dt;
          if (strikeElapsed >= HAMMER_DOWNSTROKE_SEC + HAMMER_REBOUND_SEC) {
            strikeElapsed = -1;
          }
        }

        const currentHammerAngle = computeHammerStrikeAngle(strikeElapsed, elapsed);
        // Negative Z rotation raises the hammer on the left of the pivot (+1.58, 0.82, 0) up to +45 degrees above the anvil
        hammerPivot.rotation.z = -currentHammerAngle;

        // Anvil vertical compression recoil right around t = 0.08s impact
        if (strikeElapsed >= 0.04 && strikeElapsed <= 0.18) {
          const impactPulse = Math.sin(((strikeElapsed - 0.04) / 0.14) * Math.PI);
          anvilGroup.position.y = -impactPulse * (stanceId === 'GRAVITY' ? 0.12 : 0.07);
        } else {
          anvilGroup.position.y = 0;
        }

        // Update 4 STANCE SKINS on the Divine Hammer
        thunderCageGroup.visible = stanceId === 'THUNDER';
        firePlumeGroup.visible = stanceId === 'FIRE';
        gravityAuraGroup.visible = stanceId === 'GRAVITY';
        mysticWaveGroup.visible = stanceId === 'MYSTIC';
        mysticHeadRingsGroup.visible = stanceId === 'MYSTIC';

        if (stanceId === 'THUNDER') {
          // Lôi Đỉnh: Glowing electric cyan runes + high-frequency jittering wireframe lightning cages
          mythicStoneHeadMat.emissive.setHex(0x00f0ff);
          mythicStoneHeadMat.emissiveIntensity = 2.6 + Math.random() * 1.2;
          thunderCageMesh1.rotation.set(
            Math.random() * Math.PI,
            Math.random() * Math.PI,
            Math.random() * Math.PI
          );
          const jitter1 = 0.92 + Math.random() * 0.22;
          thunderCageMesh1.scale.set(0.95 * jitter1, 1.25 * jitter1, 0.95 * jitter1);

          thunderCageMesh2.rotation.set(
            Math.random() * Math.PI,
            Math.random() * Math.PI,
            Math.random() * Math.PI
          );
          thunderWireMat1.opacity = 0.55 + Math.random() * 0.45;
        } else if (stanceId === 'FIRE') {
          // Viêm Dương: Blazing crimson-orange emissive runes & rising fire-smoke plumes
          mythicStoneHeadMat.emissive.setHex(0xff3b30);
          mythicStoneHeadMat.emissiveIntensity = 3.2 + Math.sin(elapsed * 12) * 0.6;
          firePuffs.forEach((p, idx) => {
            const cycle = (elapsed * 1.8 + p.phase) % 1.0;
            const py = -0.35 + cycle * 1.25;
            const spread = 1.0 + cycle * 0.45;
            p.mesh.position.set(
              Math.cos(p.angle + elapsed * 2.0) * p.radius * spread,
              py,
              Math.sin(p.angle + elapsed * 2.0) * p.radius * spread
            );
            const s = (1.0 - cycle * 0.65) * (0.9 + 0.2 * Math.sin(elapsed * 8 + idx));
            p.mesh.scale.setScalar(Math.max(0.1, s));
            p.mat.opacity = (1.0 - cycle) * 0.85;
          });
        } else if (stanceId === 'GRAVITY') {
          // Trọng Lực: Deep violet-purple aura + counter-rotating gravity rings
          mythicStoneHeadMat.emissive.setHex(0x9333ea);
          mythicStoneHeadMat.emissiveIntensity = 2.8 + Math.sin(elapsed * 6) * 0.5;
          gravityShellMesh.rotation.y = elapsed * 2.2;
          gravityShellMesh.scale.setScalar(1.0 + 0.08 * Math.sin(elapsed * 8.0));
          gravityOrbit1.rotation.x = elapsed * 3.4;
          gravityOrbit1.rotation.y = elapsed * 2.1;
          gravityOrbit2.rotation.y = -elapsed * 3.0;
          gravityOrbit2.rotation.z = elapsed * 2.5;
        } else if (stanceId === 'MYSTIC') {
          // Huyền Âm: Jade-emerald runes + expanding concentric translucent soundwave rings
          mythicStoneHeadMat.emissive.setHex(0x10b981);
          mythicStoneHeadMat.emissiveIntensity = 2.4 + Math.sin(elapsed * 5) * 0.4;
          mysticHeadHalo.rotation.z = elapsed * 1.8;
          mysticHeadHalo.scale.setScalar(1.0 + 0.12 * Math.sin(elapsed * 6.0));

          mysticSonicRings.forEach((ring) => {
            const prog = (elapsed * 0.65 + ring.offset) % 1.0;
            const scale = 0.8 + prog * 4.2;
            ring.mesh.scale.setScalar(scale);
            ring.mat.opacity = (1.0 - prog) * 0.58;
          });
        }

        // Calculate proximity of the 100 BPM contracting wave to the Anvil's Golden Rim
        const rimDist = Math.abs(waveProg - TARGET_RIM_PROGRESS);
        const rimProximity = Math.max(0, 1 - rimDist / (PERFECT_TOLERANCE * 1.15));
        const rimFlash = Math.pow(rimProximity, 1.5);

        // Update Custom GLSL Shader Uniforms (Rhythm Ring + 3,000-Particle GPU Vertex Shader)
        rhythmUniforms.uTime.value = elapsed;
        rhythmUniforms.uWaveProgress.value = waveProg;
        rhythmUniforms.uRimFlash.value = rimFlash;
        rhythmUniforms.uOverdrive.value = props.overdriveActive ? 1.0 : 0.0;
        rhythmUniforms.uStanceColor.value.set(stanceCfg.color);

        sparkUniforms.uTime.value = elapsed;

        const overdriveBoost = props.overdriveActive ? 1.2 : 0.0;
        anvilTopFaceMat.emissiveIntensity = 1.35 + rimFlash * 2.6 + overdriveBoost;
        goldenRimMat.emissiveIntensity = 0.85 + rimFlash * 3.8 + overdriveBoost;
        rimPulseLight.intensity = 3.2 + rimFlash * 12.0 + overdriveBoost * 5.0;

        const bpmBeatPulse = 0.5 + 0.5 * Math.sin(elapsed * ((FORGE_BPM / 60) * Math.PI * 2));
        fireUnderLight.intensity = 20.0 + bpmBeatPulse * 6.5;

        // Camera tremor (amplified when GRAVITY stance strikes)
        if (cameraTrauma > 0) {
          cameraTrauma = Math.max(0, cameraTrauma - dt * 1.75);
          const shake = cameraTrauma * cameraTrauma * 0.28;
          camera.position.set(
            baseCamPos.x + (Math.random() - 0.5) * shake,
            baseCamPos.y + (Math.random() - 0.5) * shake,
            baseCamPos.z + (Math.random() - 0.5) * shake * 0.5
          );
        } else {
          camera.position.copy(baseCamPos);
        }
        camera.lookAt(baseLookAt);

        renderer.render(scene, camera);

        if (isSoftwareGl) {
          afterDraw(tick);
        } else {
          frameId = requestAnimationFrame(tick);
        }
      };

      tick();

      return () => {
        cancelAnimationFrame(frameId);
        clearTimeout(frameId);
        ro.disconnect();
        envTarget.dispose();
        emissiveMap.dispose();
        bumpMap.dispose();
        hammerEmissiveMap.dispose();
        hammerBumpMap.dispose();
        rhythmPlaneGeo.dispose();
        rhythmShaderMat.dispose();
        sparkGeo.dispose();
        sparkMat.dispose();
        renderer.dispose();
      };
    }, [waveProgressRef]);

    return (
      <div
        className="relative w-full h-64 sm:h-72 md:h-80 flex items-center justify-center"
        data-current-stance={currentStance}
        data-spark-buffer={FORGE_SPARK_BUFFER_SIZE}
      >
        <div
          ref={mountRef}
          className="w-full h-full rounded-2xl overflow-hidden border border-slate-800/80 shadow-inner"
        />

        <button
          type="button"
          aria-label="Đập Đe Thần Thoại 3D [Space hoặc Click]"
          onClick={() => {
            imperativeStrikeTriggerRef.current += 1;
            onStrike();
          }}
          className="absolute inset-0 w-full h-full rounded-2xl focus:outline-none focus-visible:ring-2 focus-visible:ring-amber-400 cursor-pointer bg-transparent"
        />
      </div>
    );
  }
);
