import * as THREE from 'three';
import {
  SKY_SHATTER_DURATION_SEC,
  SKY_SHATTER_FRAGMENT_COUNT,
  createSkyShatterFragments,
  evaluateSkyShardTransform,
} from '../game/rules';

export const SKY_DOME_VERTEX_SHADER = `
  uniform float uTime;
  uniform float uCrackProgress;

  varying vec3 vUnitDir;
  varying vec3 vNormalDir;
  varying float vDisplacement;

  float hash31(vec3 p) {
    p = fract(p * 0.1031);
    p += dot(p, p.yzx + 33.33);
    return fract((p.x + p.y) * p.z);
  }

  void main() {
    vec3 unitDir = normalize(position);
    vUnitDir = unitDir;
    vNormalDir = normalize(normalMatrix * normal);

    vec3 displaced = position;
    float dispAmount = 0.0;

    // When uCrackProgress > 0.8: Vertex displacement shader jitters & warps the sky dome surface
    if (uCrackProgress > 0.8) {
      float cataclysm = clamp((uCrackProgress - 0.8) / 0.2, 0.0, 1.0);
      float cellPulse = sin(unitDir.x * 14.0 + uTime * 28.0) *
                        cos(unitDir.y * 12.0 - uTime * 32.0) *
                        sin(unitDir.z * 14.0 + uTime * 24.0);
      float highFreqJitter = (hash31(floor(unitDir * 12.0) + vec3(floor(uTime * 20.0))) - 0.5) * 2.0;
      dispAmount = (cellPulse * 0.22 + highFreqJitter * 0.18) * cataclysm;
      displaced += normal * dispAmount;
    }

    vDisplacement = dispAmount;
    gl_Position = projectionMatrix * modelViewMatrix * vec4(displaced, 1.0);
  }
`;

export const SKY_DOME_FRAGMENT_SHADER = `
  uniform float uTime;
  uniform float uCrackProgress;

  varying vec3 vUnitDir;
  varying vec3 vNormalDir;
  varying float vDisplacement;

  // 3D Hash for Voronoi cellular feature points
  vec3 hash33(vec3 p) {
    p = vec3(
      dot(p, vec3(127.1, 311.7, 74.7)),
      dot(p, vec3(269.5, 183.3, 246.1)),
      dot(p, vec3(113.5, 271.9, 124.6))
    );
    return fract(sin(p) * 43758.5453123);
  }

  // 3D Voronoi Noise returning (F1: closest distance, F2: second closest distance, cellId)
  // F2 - F1 produces crisp polygonal cellular fracture lines across the 3D hemisphere
  vec3 voronoi3D(vec3 x) {
    vec3 n = floor(x);
    vec3 f = fract(x);

    float f1 = 8.0;
    float f2 = 8.0;
    float cellId = 0.0;

    for (int k = -1; k <= 1; k++) {
      for (int j = -1; j <= 1; j++) {
        for (int i = -1; i <= 1; i++) {
          vec3 g = vec3(float(i), float(j), float(k));
          vec3 o = hash33(n + g);
          vec3 r = g + (0.5 + 0.42 * sin(o * 6.2831)) - f;
          float d = dot(r, r);

          if (d < f1) {
            f2 = f1;
            f1 = d;
            cellId = o.x;
          } else if (d < f2) {
            f2 = d;
          }
        }
      }
    }

    return vec3(sqrt(f1), sqrt(f2), cellId);
  }

  void main() {
    vec3 dir = normalize(vUnitDir);

    // 1. BASE METALLIC DARK IRON CLOUDS (Drifting with uTime even when uCrackProgress = 0.0)
    vec3 cloudSample1 = voronoi3D(dir * 2.6 + vec3(uTime * 0.055, -uTime * 0.02, uTime * 0.04));
    vec3 cloudSample2 = voronoi3D(dir * 5.2 - vec3(uTime * 0.08, uTime * 0.03, -uTime * 0.05));
    float cloudVeins = smoothstep(0.15, 0.75, cloudSample1.x * 0.65 + cloudSample2.x * 0.35);
    float metallicSheen = pow(max(0.0, 1.0 - (cloudSample1.y - cloudSample1.x)), 3.0) * 0.35;

    vec3 darkObsidianSky = vec3(0.035, 0.048, 0.082);
    vec3 ironCloudRidge = vec3(0.11, 0.155, 0.255);
    vec3 steelHighlight = vec3(0.22, 0.31, 0.46);

    vec3 skyColor = mix(darkObsidianSky, ironCloudRidge, cloudVeins);
    skyColor += steelHighlight * metallicSheen;

    // Subtle horizon atmospheric rim
    float horizonFade = smoothstep(0.0, 0.35, max(0.0, dir.y));
    skyColor *= (0.55 + 0.45 * horizonFade);

    // 2. 3D VORONOI CELLULAR CRACKS (Triggered when uCrackProgress > 0.3)
    if (uCrackProgress > 0.3) {
      // In local hemisphere space (theta = 0..PI/2), the zenith pole is at dir.y = 1.0 (length(dir.xz) = 0.0)
      vec2 zenithOffset = dir.xz - vec2(0.0, 0.12);
      float distFromZenith = clamp(length(zenithOffset) * 1.35, 0.0, 1.0);

      // Crack reach expands from zenith (0.0) outward to the dome edges as uCrackProgress rises from 0.3 -> 0.85
      float crackPhase = clamp((uCrackProgress - 0.3) / 0.55, 0.0, 1.0);
      float maxReach = mix(0.28, 1.25, crackPhase);
      float radialMask = smoothstep(maxReach, max(0.0, maxReach - 0.28), distFromZenith);

      // Multi-scale 3D Voronoi cellular fractures
      vec3 vPrimary = voronoi3D(dir * 5.2);
      vec3 vSecondary = voronoi3D(dir * 11.0 + vec3(1.7));

      float edgePrimary = vPrimary.y - vPrimary.x;
      float edgeSecondary = vSecondary.y - vSecondary.x;

      // Cracks widen dramatically when uCrackProgress > 0.8
      float cataclysm = clamp((uCrackProgress - 0.8) / 0.2, 0.0, 1.0);
      float primaryWidth = mix(0.032, 0.155, pow(crackPhase, 1.25)) + cataclysm * 0.07;
      float secondaryWidth = mix(0.015, 0.085, crackPhase * crackPhase) + cataclysm * 0.04;

      float primaryCrack = smoothstep(primaryWidth, primaryWidth * 0.12, edgePrimary) * radialMask;
      float secondaryCrack = smoothstep(secondaryWidth, secondaryWidth * 0.15, edgeSecondary) * radialMask * crackPhase;
      float crackIntensity = clamp(primaryCrack + secondaryCrack * 0.75, 0.0, 1.0);

      // Heated cellular rim halo around the fractures
      float crackHalo = exp(-edgePrimary * mix(20.0, 8.0, crackPhase)) * radialMask * (0.5 + 0.5 * crackPhase);

      // Colors: Golden/Orange (#FFA000 / #FFD23F) for 0.3..0.8, blazing Magma + Cyan Lightning (#00F0FF / #FFF9D6) for > 0.8
      vec3 deepMagmaOrange = vec3(1.0, 0.32, 0.05);
      vec3 brightDivineGold = vec3(1.0, 0.84, 0.25);
      vec3 whiteHotCore = vec3(1.0, 0.98, 0.88);
      vec3 lightningCyan = vec3(0.0, 0.95, 1.0);

      vec3 fissureColor = mix(deepMagmaOrange, brightDivineGold, crackIntensity);
      fissureColor = mix(fissureColor, whiteHotCore, pow(crackIntensity, 2.5));

      if (cataclysm > 0.0) {
        // High-voltage lightning arcs surging through the widened Voronoi cells
        float lightningArc = step(0.62, sin(vPrimary.z * 32.0 + uTime * 22.0)) * cataclysm;
        fissureColor = mix(fissureColor, lightningCyan, lightningArc * 0.72);
        fissureColor += whiteHotCore * cataclysm * 0.55;
      }

      // Apply glowing cracks & heated magma halo onto the metallic sky dome
      skyColor += deepMagmaOrange * crackHalo * (0.85 + cataclysm * 1.1);
      skyColor = mix(skyColor, fissureColor * (1.5 + cataclysm * 1.2), crackIntensity);
    }

    gl_FragColor = vec4(skyColor, 0.96);
  }
`;

export interface ShatterableSkyDomeController {
  group: THREE.Group;
  domeMesh: THREE.Mesh;
  shatterInstancedMesh: THREE.InstancedMesh;
  update: (elapsedSec: number, dt: number, crackProgress: number) => void;
  triggerSkyShatter: () => void;
  resetSkyDome: () => void;
  isShattered: () => boolean;
  getFragmentCount: () => number;
  dispose: () => void;
}

/**
 * Builds the 3D VÒM TRỜI NỨT VỠ (Shatterable Sky Dome) hemisphere + 1,500 Voronoi shard InstancedMesh.
 */
export function createShatterableSkyDome(): ShatterableSkyDomeController {
  const group = new THREE.Group();

  // 1. MESH CƠ SỞ: Inverted Hemisphere (phiLength = Math.PI * 2, thetaLength = Math.PI / 2)
  // Encloses the entire upper forge stage
  const domeGeo = new THREE.SphereGeometry(
    11.5,
    64,
    36,
    0,
    Math.PI * 2,
    0,
    Math.PI / 2
  );

  const domeUniforms = {
    uTime: { value: 0 },
    uCrackProgress: { value: 0 },
  };

  const domeMat = new THREE.ShaderMaterial({
    uniforms: domeUniforms,
    vertexShader: SKY_DOME_VERTEX_SHADER,
    fragmentShader: SKY_DOME_FRAGMENT_SHADER,
    side: THREE.DoubleSide,
    transparent: true,
    depthWrite: false,
    fog: false,
  });

  const domeMesh = new THREE.Mesh(domeGeo, domeMat);
  // Tilt backward (-1.42 rad) so the hemisphere's zenith apex sits right in the upper sky above the Anvil & Hammer
  // and the hemisphere completely encloses the entire camera view behind the forge!
  domeMesh.position.set(0, 0.2, 0.5);
  domeMesh.rotation.x = -1.42;
  domeMesh.renderOrder = 0;
  group.add(domeMesh);

  // 2. SHATTER SYSTEM (HP = 0): InstancedMesh of 1,500 sharp triangular Voronoi fragments
  const shardGeo = new THREE.ConeGeometry(0.42, 0.14, 3);
  shardGeo.rotateX(Math.PI / 2);

  const shardMat = new THREE.MeshStandardMaterial({
    color: 0x1e293b,
    metalness: 0.88,
    roughness: 0.25,
    emissive: new THREE.Color(0xff9500),
    emissiveIntensity: 2.2,
    side: THREE.DoubleSide,
    fog: false,
  });

  const shatterInstancedMesh = new THREE.InstancedMesh(
    shardGeo,
    shardMat,
    SKY_SHATTER_FRAGMENT_COUNT
  );
  shatterInstancedMesh.instanceMatrix.setUsage(THREE.DynamicDrawUsage);
  shatterInstancedMesh.visible = false;
  shatterInstancedMesh.frustumCulled = false;
  shatterInstancedMesh.renderOrder = 4;
  group.add(shatterInstancedMesh);

  // Color variation per Voronoi shard (Gold, Magma Orange, Electric Cyan, Dark Metallic Iron)
  const shardColor = new THREE.Color();
  for (let i = 0; i < SKY_SHATTER_FRAGMENT_COUNT; i++) {
    const r = i % 5;
    if (r === 0) shardColor.setHex(0xffd23f);
    else if (r === 1) shardColor.setHex(0xff5500);
    else if (r === 2) shardColor.setHex(0x00f0ff);
    else shardColor.setHex(0x334155);
    shatterInstancedMesh.setColorAt(i, shardColor);
  }
  if (shatterInstancedMesh.instanceColor) {
    shatterInstancedMesh.instanceColor.needsUpdate = true;
  }

  let shatterState = createSkyShatterFragments(SKY_SHATTER_FRAGMENT_COUNT, 9.2);
  let shattered = false;
  let shatterElapsed = 0;

  const dummy = new THREE.Object3D();

  const updateShatterInstances = (elapsedShatter: number) => {
    for (let i = 0; i < SKY_SHATTER_FRAGMENT_COUNT; i++) {
      const tr = evaluateSkyShardTransform(
        shatterState,
        i,
        elapsedShatter,
        SKY_SHATTER_DURATION_SEC
      );
      dummy.position.set(tr.x, tr.y, tr.z);
      dummy.rotation.set(tr.rx, tr.ry, tr.rz);
      dummy.scale.setScalar(tr.scale);
      dummy.updateMatrix();
      shatterInstancedMesh.setMatrixAt(i, dummy.matrix);
    }
    shatterInstancedMesh.instanceMatrix.needsUpdate = true;
  };

  const triggerSkyShatter = () => {
    shatterState = createSkyShatterFragments(SKY_SHATTER_FRAGMENT_COUNT, 9.2);
    shattered = true;
    shatterElapsed = 0;
    domeMesh.visible = false;
    shatterInstancedMesh.visible = true;
    updateShatterInstances(0);
  };

  const resetSkyDome = () => {
    shattered = false;
    shatterElapsed = 0;
    domeMesh.visible = true;
    shatterInstancedMesh.visible = false;
    domeUniforms.uCrackProgress.value = 0;
  };

  const update = (elapsedSec: number, dt: number, crackProgress: number) => {
    domeUniforms.uTime.value = elapsedSec;
    const clampedCrack = Math.max(0, Math.min(1, crackProgress));
    domeUniforms.uCrackProgress.value = clampedCrack;

    // Auto-trigger sky shatter if crackProgress reaches 1.0 (Boss HP === 0)
    if (clampedCrack >= 1.0 && !shattered) {
      triggerSkyShatter();
    }

    if (shattered) {
      shatterElapsed += dt;
      updateShatterInstances(shatterElapsed);
      if (shatterElapsed >= SKY_SHATTER_DURATION_SEC) {
        shatterInstancedMesh.visible = false;
      }
    }
  };

  const dispose = () => {
    domeGeo.dispose();
    domeMat.dispose();
    shardGeo.dispose();
    shardMat.dispose();
    shatterInstancedMesh.dispose();
  };

  return {
    group,
    domeMesh,
    shatterInstancedMesh,
    update,
    triggerSkyShatter,
    resetSkyDome,
    isShattered: () => shattered,
    getFragmentCount: () => SKY_SHATTER_FRAGMENT_COUNT,
    dispose,
  };
}
