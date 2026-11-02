import React, { useEffect, useRef, useImperativeHandle, forwardRef } from 'react';
import * as THREE from 'three';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import {
  CRACK_INCREMENT_PER_STRIKE,
  GRAND_SHATTER_SHARD_COUNT,
  LIGHTNING_PILLAR_ASCENT_SEC,
  advanceVaultCrack,
  StanceKey,
} from '../game/rules';
import { soundEngine } from '../game/audio';

// ============================================================================
// 1. THE CRACKING CELESTIAL VAULT SHADER (3D Voronoi Crow's-Foot + Bas-Relief + Shockwave)
// ============================================================================
const CELESTIAL_VAULT_VERTEX_SHADER = `
  uniform float uTime;
  uniform float uCrack;
  uniform float uShockwaveRadius;
  uniform float uShockwaveIntensity;
  uniform vec3 uZenithDir;

  varying vec3 vUnitDir;
  varying vec3 vWorldPos;
  varying vec3 vNormalDir;
  varying float vZenithAngle;

  float hash31(vec3 p) {
    p = fract(p * 0.1031);
    p += dot(p, p.yzx + 33.33);
    return fract((p.x + p.y) * p.z);
  }

  void main() {
    vec3 unitDir = normalize(position);
    vUnitDir = unitDir;
    vNormalDir = normalize(normalMatrix * normal);

    // Angular distance from the zenith impact point (0.0 at zenith -> ~1.6 at horizon)
    float zenithDist = distance(unitDir, normalize(uZenithDir));
    vZenithAngle = zenithDist;

    vec3 displaced = position;

    // Vertex Displacement: Vault surface trembles as uCrack rises and heaves when shockwave passes
    float crackTremor = pow(clamp(uCrack, 0.0, 1.0), 1.6) * 0.28;
    float waveCell = sin(unitDir.x * 16.0 + uTime * 22.0) *
                     cos(unitDir.y * 14.0 - uTime * 26.0) *
                     sin(unitDir.z * 16.0 + uTime * 19.0);
    float jitter = (hash31(floor(unitDir * 14.0) + vec3(floor(uTime * 24.0))) - 0.5) * 2.0;

    float shockRing = exp(-abs(zenithDist - uShockwaveRadius) * 9.5) * uShockwaveIntensity;
    float totalDisp = (waveCell * 0.6 + jitter * 0.4) * crackTremor + shockRing * 0.42;

    displaced += normal * totalDisp;

    vec4 worldPosition = modelMatrix * vec4(displaced, 1.0);
    vWorldPos = worldPosition.xyz;
    gl_Position = projectionMatrix * viewMatrix * worldPosition;
  }
`;

const CELESTIAL_VAULT_FRAGMENT_SHADER = `
  uniform float uTime;
  uniform float uCrack;
  uniform float uShockwaveRadius;
  uniform float uShockwaveIntensity;
  uniform float uStrikeFlash;
  uniform vec3 uZenithDir;

  varying vec3 vUnitDir;
  varying vec3 vWorldPos;
  varying vec3 vNormalDir;
  varying float vZenithAngle;

  vec3 hash33(vec3 p) {
    p = vec3(
      dot(p, vec3(127.1, 311.7, 74.7)),
      dot(p, vec3(269.5, 183.3, 246.1)),
      dot(p, vec3(113.5, 271.9, 124.6))
    );
    return fract(sin(p) * 43758.5453123);
  }

  // 3D Voronoi Noise returning (F1, F2, cellId)
  vec3 voronoi3D(vec3 x) {
    vec3 n = floor(x);
    vec3 f = fract(x);

    float f1 = 8.0;
    float f2 = 8.0;
    float id = 0.0;

    for (int k = -1; k <= 1; k++) {
      for (int j = -1; j <= 1; j++) {
        for (int i = -1; i <= 1; i++) {
          vec3 g = vec3(float(i), float(j), float(k));
          vec3 o = hash33(n + g);
          vec3 r = g + (0.5 + 0.44 * sin(o * 6.2831)) - f;
          float d = dot(r, r);
          if (d < f1) {
            f2 = f1;
            f1 = d;
            id = o.x;
          } else if (d < f2) {
            f2 = d;
          }
        }
      }
    }
    return vec3(sqrt(f1), sqrt(f2), id);
  }

  // Swirling Ancient Oriental Bas-Relief pattern (Vân phù điêu cổ uốn lượn)
  float ancientBasRelief(vec3 dir) {
    vec3 q = dir * 3.8;
    q.xy += 0.35 * vec2(
      sin(q.z * 2.4 + q.y * 1.9),
      cos(q.x * 2.4 - q.z * 1.9)
    );
    q.yz += 0.28 * vec2(
      cos(q.x * 3.1 + q.y * 2.2),
      sin(q.z * 3.1 - q.x * 2.2)
    );
    float scroll1 = sin(q.x * 4.5 + sin(q.y * 4.5 + sin(q.z * 4.5)));
    float scroll2 = cos(length(q.xz) * 7.0 - atan(q.z, q.x) * 4.0);
    return smoothstep(-0.6, 0.7, scroll1 * 0.65 + scroll2 * 0.35);
  }

  void main() {
    vec3 dir = normalize(vUnitDir);
    vec3 zenith = normalize(uZenithDir);
    float zenithDist = distance(dir, zenith);

    // 1. ANCIENT METEORITE STONE (#0B0F19) + SWIRLING BAS-RELIEF CARVINGS
    float relief = ancientBasRelief(dir);
    float fineGrain = ancientBasRelief(dir * 2.7 + vec3(1.9));
    vec3 meteoriteBase = vec3(0.043, 0.059, 0.098); // #0B0F19
    vec3 reliefRidge = vec3(0.095, 0.130, 0.205);
    vec3 reliefTrench = vec3(0.022, 0.030, 0.052);

    vec3 stoneColor = mix(reliefTrench, meteoriteBase, smoothstep(0.0, 0.5, relief));
    stoneColor = mix(stoneColor, reliefRidge, smoothstep(0.45, 1.0, relief) * 0.85);
    stoneColor += vec3(0.03, 0.045, 0.07) * fineGrain;

    // Warm rim illumination cast onto the bas-relief ridges from the zenith fissures
    float zenithGlowFalloff = exp(-zenithDist * 1.85);
    float reliefHighlight = pow(relief, 2.2) * zenithGlowFalloff * (0.25 + uCrack * 1.35);
    stoneColor += vec3(1.0, 0.58, 0.08) * reliefHighlight * 0.42;

    // 2. 3D VORONOI CROW'S-FOOT FRACTURES (Uniform uCrack: 0.0 -> 1.0)
    float effectiveCrack = max(0.03, uCrack);

    // Radial reach from the zenith impact point outward across the vault
    float maxReach = mix(0.16, 1.55, pow(effectiveCrack, 0.78));
    float radialMask = smoothstep(maxReach, max(0.0, maxReach - 0.32), zenithDist);

    vec3 warp = 0.085 * vec3(
      sin(dir.y * 18.0 + dir.z * 13.0),
      cos(dir.z * 18.0 - dir.x * 13.0),
      sin(dir.x * 18.0 + dir.y * 13.0)
    );

    vec3 vPrimary = voronoi3D((dir + warp) * 4.8);
    vec3 vSecondary = voronoi3D((dir - warp * 0.7) * 10.5 + vec3(2.3));
    vec3 vMicro = voronoi3D(dir * 21.0 + vec3(5.1));

    float edge1 = vPrimary.y - vPrimary.x;
    float edge2 = vSecondary.y - vSecondary.x;
    float edge3 = vMicro.y - vMicro.x;

    float width1 = mix(0.018, 0.135, pow(effectiveCrack, 1.25));
    float width2 = mix(0.008, 0.078, pow(effectiveCrack, 1.4));
    float width3 = mix(0.002, 0.045, effectiveCrack * effectiveCrack);

    float crack1 = smoothstep(width1, width1 * 0.08, edge1) * radialMask;
    float crack2 = smoothstep(width2, width2 * 0.10, edge2) * radialMask * smoothstep(0.08, 0.6, effectiveCrack);
    float crack3 = smoothstep(width3, 0.0, edge3) * radialMask * smoothstep(0.25, 0.9, effectiveCrack);

    float zenithScar = smoothstep(0.11 + effectiveCrack * 0.12, 0.0, zenithDist) *
                       smoothstep(width1 * 1.6, 0.0, edge1);

    float totalCrack = clamp(crack1 + crack2 * 0.8 + crack3 * 0.55 + zenithScar, 0.0, 1.0);

    float magmaHalo = exp(-edge1 * mix(26.0, 8.5, effectiveCrack)) * radialMask * (0.35 + effectiveCrack * 0.95);

    vec3 deepEmber = vec3(0.92, 0.28, 0.02);
    vec3 fireGold = vec3(1.0, 0.62, 0.0);    // #FF9E00
    vec3 solarGold = vec3(1.0, 0.85, 0.28);
    vec3 whiteHot = vec3(1.0, 0.98, 0.90);

    float luminanceBoost = 1.35 + uCrack * 2.4 + uStrikeFlash * 1.5;
    vec3 crackEmission = mix(deepEmber, fireGold, smoothstep(0.0, 0.45, totalCrack));
    crackEmission = mix(crackEmission, solarGold, smoothstep(0.4, 0.8, totalCrack));
    crackEmission = mix(crackEmission, whiteHot, pow(totalCrack, 2.4));
    crackEmission *= luminanceBoost;

    // 3. RADIAL SHOCKWAVE
    float shockDist = abs(zenithDist - uShockwaveRadius);
    float shockWaveCore = smoothstep(0.055, 0.0, shockDist) * uShockwaveIntensity;
    float shockWaveGlow = exp(-shockDist * 14.0) * uShockwaveIntensity;
    float shockCrackExcite = smoothstep(0.14, 0.0, edge1) * shockWaveGlow * 1.8;

    vec3 cyanLightning = vec3(0.0, 0.94, 1.0); // #00F0FF
    vec3 shockColor = mix(cyanLightning, fireGold, 0.35) * (shockWaveCore * 2.4 + shockWaveGlow * 1.1 + shockCrackExcite * 1.6);

    vec3 finalColor = stoneColor;
    finalColor += fireGold * magmaHalo * (0.65 + uCrack * 1.1);
    finalColor = mix(finalColor, crackEmission, totalCrack);
    finalColor += shockColor;

    float rimFade = smoothstep(-0.45, 0.05, dir.y);
    finalColor *= (0.4 + 0.6 * rimFade);

    gl_FragColor = vec4(finalColor, 1.0);
  }
`;

// ============================================================================
// 2. VOLUMETRIC GOD RAYS SHADER
// ============================================================================
const GOD_RAY_VERTEX_SHADER = `
  varying vec2 vUv;
  varying vec3 vNormalView;
  varying vec3 vViewDir;

  void main() {
    vUv = uv;
    vec4 mvPos = modelViewMatrix * vec4(position, 1.0);
    vNormalView = normalize(normalMatrix * normal);
    vViewDir = normalize(-mvPos.xyz);
    gl_Position = projectionMatrix * mvPos;
  }
`;

const GOD_RAY_FRAGMENT_SHADER = `
  uniform float uTime;
  uniform float uCrack;
  uniform float uStrikeFlash;
  uniform vec3 uRayColor;
  uniform vec3 uStrikeColor;
  uniform float uRaySeed;

  varying vec2 vUv;
  varying vec3 vNormalView;
  varying vec3 vViewDir;

  void main() {
    float verticalFade = smoothstep(0.0, 0.25, vUv.y) * smoothstep(1.0, 0.72, vUv.y);
    float edgeFresnel = pow(abs(dot(vNormalView, vViewDir)), 1.65);

    float angle = vUv.x * 6.2831853;
    float streaks = 0.55 + 0.45 * sin(angle * 5.0 + uRaySeed * 6.0 + uTime * 1.4) *
                           cos(vUv.y * 8.0 + uTime * 2.2 - uRaySeed * 3.0);

    float baseVisibility = 0.12 + pow(clamp(uCrack, 0.0, 1.0), 0.85) * 0.52 + uStrikeFlash * 0.35;
    float alpha = verticalFade * edgeFresnel * streaks * baseVisibility * 0.14;

    vec3 col = mix(uRayColor, uStrikeColor, clamp(uStrikeFlash * 0.75, 0.0, 1.0));
    gl_FragColor = vec4(col * (0.95 + uCrack * 0.45), clamp(alpha, 0.0, 0.28));
  }
`;

// ============================================================================
// 3. COSMIC NEBULA GALAXY BACKDROP SHADER
// ============================================================================
const COSMIC_NEBULA_VERTEX_SHADER = `
  varying vec3 vDir;
  void main() {
    vDir = normalize(position);
    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
  }
`;

const COSMIC_NEBULA_FRAGMENT_SHADER = `
  uniform float uTime;
  uniform float uReveal;

  varying vec3 vDir;

  float hash(vec3 p) {
    p = fract(p * 0.3183099 + 0.1);
    p *= 17.0;
    return fract(p.x * p.y * p.z * (p.x + p.y + p.z));
  }

  float noise3D(vec3 x) {
    vec3 i = floor(x);
    vec3 f = fract(x);
    f = f * f * (3.0 - 2.0 * f);
    return mix(
      mix(
        mix(hash(i + vec3(0, 0, 0)), hash(i + vec3(1, 0, 0)), f.x),
        mix(hash(i + vec3(0, 1, 0)), hash(i + vec3(1, 1, 0)), f.x),
        f.y
      ),
      mix(
        mix(hash(i + vec3(0, 0, 1)), hash(i + vec3(1, 0, 1)), f.x),
        mix(hash(i + vec3(0, 1, 1)), hash(i + vec3(1, 1, 1)), f.x),
        f.y
      ),
      f.z
    );
  }

  float fbm(vec3 p) {
    float v = 0.0;
    float a = 0.5;
    for (int i = 0; i < 5; i++) {
      v += a * noise3D(p);
      p = p * 2.03 + vec3(1.7, -1.2, 0.9);
      a *= 0.5;
    }
    return v;
  }

  void main() {
    if (uReveal <= 0.001) {
      discard;
    }

    vec3 dir = normalize(vDir);
    float c = cos(uTime * 0.08);
    float s = sin(uTime * 0.08);
    vec3 rotDir = vec3(dir.x * c - dir.z * s, dir.y, dir.x * s + dir.z * c);

    vec3 galaxyCenter = normalize(vec3(0.0, 0.52, -0.85));
    vec3 rel = dir - galaxyCenter;
    float r = length(rel);
    float theta = atan(rel.y, rel.x) + uTime * 0.22 - r * 5.8;

    float spiralArms = pow(0.5 + 0.5 * cos(theta * 2.0), 2.2) * exp(-r * 2.1);
    float nebulaCloud1 = fbm(rotDir * 3.2 + vec3(0.0, uTime * 0.04, 0.0));
    float nebulaCloud2 = fbm(rotDir * 6.4 - vec3(uTime * 0.05, 0.0, nebulaCloud1 * 1.8));

    vec3 deepSpace = vec3(0.015, 0.018, 0.045);
    vec3 violetNebula = vec3(0.38, 0.08, 0.68);
    vec3 magentaNebula = vec3(0.92, 0.22, 0.60);
    vec3 cyanNebula = vec3(0.0, 0.88, 1.0);
    vec3 coreGold = vec3(1.0, 0.78, 0.28);

    vec3 col = deepSpace;
    col = mix(col, violetNebula, smoothstep(0.28, 0.75, nebulaCloud1) * 0.85);
    col = mix(col, magentaNebula, smoothstep(0.38, 0.82, nebulaCloud2) * 0.7);
    col += cyanNebula * spiralArms * (0.75 + 0.5 * nebulaCloud2);
    col += coreGold * exp(-r * 4.5) * 1.85;

    float starField = pow(noise3D(rotDir * 85.0), 18.0) * 3.5;
    col += vec3(0.95, 0.98, 1.0) * starField;

    gl_FragColor = vec4(col * uReveal, 1.0);
  }
`;

// ============================================================================
// 4. MULTI-EFFECT CELESTIAL EMBER & PLASMA SPARK SHADER
// ============================================================================
const EMBER_PARTICLES_VERTEX_SHADER = `
  attribute vec3 aVelocity;
  attribute vec3 aColor;
  attribute vec3 aTiming;
  attribute vec2 aSeed;

  uniform float uTime;
  uniform float uGravity;
  uniform float uPixelRatio;

  varying vec3 vColor;
  varying float vAlpha;
  varying float vLife;
  varying float vPhase;
  varying float vArchetype;

  void main() {
    float age = uTime - aTiming.x;
    float duration = max(0.1, aTiming.y);

    if (age < 0.0 || age > duration || aTiming.z <= 0.01) {
      gl_Position = vec4(0.0, 0.0, 2.0, 1.0);
      gl_PointSize = 0.0;
      vAlpha = 0.0;
      vColor = vec3(0.0);
      vLife = 0.0;
      vPhase = 0.0;
      vArchetype = 0.0;
      return;
    }

    float life = clamp(age / duration, 0.0, 1.0);
    vec3 pos = position + aVelocity * age;
    pos.y -= 0.5 * uGravity * age * age;

    float swirlAngle = age * 5.2 + aSeed.x * 6.2831;
    float swirlRadius = (0.08 + life * 0.28) * (0.6 + 0.4 * sin(aSeed.x * 19.0));
    pos.x += cos(swirlAngle) * swirlRadius;
    pos.z += sin(swirlAngle) * swirlRadius;

    if (pos.y < -2.1 && length(pos.xz - vec2(0.0, 0.6)) < 1.35) {
      pos.y = -2.1 + abs(pos.y + 2.1) * 0.35;
    }

    vec4 mvPos = modelViewMatrix * vec4(pos, 1.0);
    gl_Position = projectionMatrix * mvPos;

    float fadeIn = smoothstep(0.0, 0.08, life);
    float fadeOut = 1.0 - smoothstep(0.42, 1.0, life);
    vAlpha = fadeIn * fadeOut;
    vColor = aColor;
    vLife = life;
    vPhase = aSeed.x;
    vArchetype = aSeed.y;

    float dist = max(1.5, -mvPos.z);
    float pulse = 0.85 + 0.25 * sin(uTime * 14.0 + aSeed.x * 17.0);
    gl_PointSize = clamp(aTiming.z * uPixelRatio * (7.2 / dist) * pulse * (0.45 + 0.55 * fadeOut), 6.0, 68.0);
  }
`;

const EMBER_PARTICLES_FRAGMENT_SHADER = `
  uniform float uTime;

  varying vec3 vColor;
  varying float vAlpha;
  varying float vLife;
  varying float vPhase;
  varying float vArchetype;

  void main() {
    if (vAlpha <= 0.01) discard;
    vec2 uv = gl_PointCoord - vec2(0.5);
    float d = length(uv);
    if (d > 0.5) discard;

    float rotAngle = uTime * (1.8 + vArchetype * 1.4) + vPhase * 6.2831853;
    float c = cos(rotAngle);
    float s = sin(rotAngle);
    vec2 rUv = vec2(uv.x * c - uv.y * s, uv.x * s + uv.y * c);

    float crossSpike = exp(-abs(rUv.x) * 26.0) * exp(-abs(rUv.y) * 4.2) +
                       exp(-abs(rUv.y) * 26.0) * exp(-abs(rUv.x) * 4.2);
    float polarAngle = atan(rUv.y, rUv.x);
    float starRays = pow(max(0.0, cos(polarAngle * 3.0)), 10.0) * exp(-d * 6.0);

    float ringRadius = 0.11 + vLife * 0.21;
    float plasmaRing = exp(-abs(d - ringRadius) * 28.0) * (1.0 - vLife * 0.65);

    float core = exp(-d * 15.0);
    float corona = exp(-d * 5.2) * smoothstep(0.5, 0.16, d);
    float twinkle = 0.78 + 0.22 * sin(uTime * 19.0 + vPhase * 23.0);

    vec3 whiteHot = vec3(1.0, 0.99, 0.94);
    vec3 midTone = vColor;
    vec3 outerRim = mix(vec3(1.0, 0.16, 0.02), vec3(0.05, 0.38, 1.0), vArchetype);

    vec3 chromatic = mix(outerRim, midTone, smoothstep(0.45, 0.14, d));
    chromatic = mix(chromatic, whiteHot, clamp(core * 1.15 + crossSpike * 0.55, 0.0, 1.0));
    chromatic += mix(vec3(1.0, 0.65, 0.1), vec3(0.0, 0.95, 1.0), 1.0 - vArchetype) * plasmaRing * 0.85;

    float intensity = (core * 1.45 + crossSpike * 0.95 + starRays * 0.55 + plasmaRing * 0.75 + corona * 0.55) * twinkle;
    float finalAlpha = clamp(vAlpha * intensity * smoothstep(0.5, 0.18, d), 0.0, 1.0);
    if (finalAlpha <= 0.015) discard;

    gl_FragColor = vec4(chromatic * intensity, finalAlpha);
  }
`;

// ============================================================================
// 5. CELESTIAL GALAXY STAR DIFFRACTION SHADER
// ============================================================================
const GALAXY_STAR_VERTEX_SHADER = `
  attribute vec3 aColor;
  attribute vec2 aStarMeta;

  uniform float uTime;
  uniform float uPixelRatio;

  varying vec3 vColor;
  varying float vPhase;

  void main() {
    vColor = aColor;
    vPhase = aStarMeta.y;

    vec4 mvPos = modelViewMatrix * vec4(position, 1.0);
    gl_Position = projectionMatrix * mvPos;

    float dist = max(2.0, -mvPos.z);
    float shimmer = 0.82 + 0.28 * sin(uTime * 3.8 + aStarMeta.y * 19.0);
    gl_PointSize = clamp(aStarMeta.x * uPixelRatio * (18.0 / dist) * shimmer, 5.0, 46.0);
  }
`;

const GALAXY_STAR_FRAGMENT_SHADER = `
  uniform float uTime;
  uniform float uReveal;

  varying vec3 vColor;
  varying float vPhase;

  void main() {
    if (uReveal <= 0.01) discard;
    vec2 uv = gl_PointCoord - vec2(0.5);
    float d = length(uv);
    if (d > 0.5) discard;

    float angle = uTime * 0.45 + vPhase * 6.2831853;
    float c = cos(angle);
    float s = sin(angle);
    vec2 rUv = vec2(uv.x * c - uv.y * s, uv.x * s + uv.y * c);

    float mainCross = exp(-abs(rUv.x) * 28.0) * exp(-abs(rUv.y) * 4.5) +
                      exp(-abs(rUv.y) * 28.0) * exp(-abs(rUv.x) * 4.5);
    vec2 diagUv = vec2((rUv.x + rUv.y) * 0.7071, (rUv.x - rUv.y) * 0.7071);
    float diagCross = (exp(-abs(diagUv.x) * 34.0) * exp(-abs(diagUv.y) * 6.0) +
                       exp(-abs(diagUv.y) * 34.0) * exp(-abs(diagUv.x) * 6.0)) * 0.55;

    float core = exp(-d * 18.0);
    float halo = exp(-d * 5.8) * smoothstep(0.5, 0.18, d);
    float intensity = (core * 1.4 + mainCross * 0.9 + diagCross + halo * 0.65) * uReveal;

    vec3 starCol = mix(vColor, vec3(1.0, 0.99, 0.96), clamp(core + mainCross * 0.5, 0.0, 1.0));
    float alpha = clamp(intensity * smoothstep(0.5, 0.2, d), 0.0, 1.0);
    if (alpha <= 0.015) discard;

    gl_FragColor = vec4(starCol * intensity, alpha);
  }
`;

// ============================================================================
// 6. 3D OBSIDIAN-MAGMA CRYSTAL SHARD SHADER
// ============================================================================
const SHARD_CRYSTAL_VERTEX_SHADER = `
  varying vec3 vLocalPos;
  varying vec3 vWorldNormal;
  varying vec3 vViewDir;
  varying vec3 vInstanceTint;

  void main() {
    vLocalPos = position;
    #ifdef USE_INSTANCING_COLOR
      vInstanceTint = instanceColor;
    #else
      vInstanceTint = vec3(1.0, 0.62, 0.0);
    #endif

    mat4 instModel = modelMatrix * instanceMatrix;
    vec4 worldPos = instModel * vec4(position, 1.0);
    vec4 mvPos = viewMatrix * worldPos;

    vWorldNormal = normalize(mat3(instModel) * normal);
    vViewDir = normalize(cameraPosition - worldPos.xyz);

    gl_Position = projectionMatrix * mvPos;
  }
`;

const SHARD_CRYSTAL_FRAGMENT_SHADER = `
  uniform float uTime;

  varying vec3 vLocalPos;
  varying vec3 vWorldNormal;
  varying vec3 vViewDir;
  varying vec3 vInstanceTint;

  float hash31(vec3 p) {
    p = fract(p * 0.1031);
    p += dot(p, p.yzx + 33.33);
    return fract((p.x + p.y) * p.z);
  }

  void main() {
    vec3 N = normalize(vWorldNormal);
    vec3 V = normalize(vViewDir);

    vec3 lightDir = normalize(vec3(0.2, 0.85, 0.48));
    float diff = max(0.0, dot(N, lightDir));
    vec3 obsidianBase = vec3(0.025, 0.035, 0.065) + vec3(0.04, 0.055, 0.09) * diff;

    vec3 p = vLocalPos * 9.5;
    float veinPattern = abs(sin(p.x * 2.4 + cos(p.y * 2.8) + sin(p.z * 2.6 + uTime * 1.8)));
    float veinMask = smoothstep(0.24, 0.02, veinPattern);
    float pulse = 0.75 + 0.25 * sin(uTime * 6.5 + hash31(floor(vLocalPos * 4.0)) * 6.28);

    float fresnel = pow(1.0 - abs(dot(N, V)), 2.6);
    vec3 H = normalize(lightDir + V);
    float spec = pow(max(0.0, dot(N, H)), 28.0);

    vec3 magmaGold = vec3(1.0, 0.62, 0.05);
    vec3 whiteCore = vec3(1.0, 0.96, 0.82);
    vec3 rimTone = mix(magmaGold, vInstanceTint, 0.45);

    vec3 col = obsidianBase;
    col += rimTone * veinMask * 1.45 * pulse;
    col += mix(rimTone, whiteCore, 0.4) * fresnel * 1.65;
    col += vec3(0.85, 0.95, 1.0) * spec * 0.9;

    gl_FragColor = vec4(col, 1.0);
  }
`;

export interface CelestialVaultStage3DHandle {
  strike: (grade?: string, stance?: StanceKey) => void;
  triggerGrandShatter: () => void;
  reset: () => void;
  setCrack: (val: number) => void;
  getStats: () => {
    uCrack: number;
    isShattered: boolean;
    grandShatterShardCount: number;
  };
}

interface CelestialVaultStage3DProps {
  crackProgress: number;
  activeStance?: StanceKey;
  overdriveActive?: boolean;
  onStrike?: () => void;
  onGrandShatter?: () => void;
  onResetVault?: () => void;
}

export const CelestialVaultStage3D = forwardRef<
  CelestialVaultStage3DHandle,
  CelestialVaultStage3DProps
>(({ crackProgress, activeStance = 'Q', overdriveActive = false, onStrike, onGrandShatter, onResetVault }, ref) => {
  const mountRef = useRef<HTMLDivElement | null>(null);

  const crackRef = useRef<number>(crackProgress);
  const shatteredRef = useRef<boolean>(false);
  const triggerStrikeRef = useRef<((grade?: string, stance?: StanceKey) => void) | null>(null);
  const resetVaultRef = useRef<(() => void) | null>(null);
  const triggerGrandShatterRef = useRef<(() => void) | null>(null);

  // Sync external crackProgress prop to internal ref
  useEffect(() => {
    if (!shatteredRef.current) {
      crackRef.current = Math.max(0, Math.min(1, crackProgress));
    }
  }, [crackProgress]);

  useImperativeHandle(ref, () => ({
    strike: (grade, stance) => {
      triggerStrikeRef.current?.(grade, stance);
    },
    triggerGrandShatter: () => {
      triggerGrandShatterRef.current?.();
    },
    reset: () => {
      resetVaultRef.current?.();
    },
    setCrack: (val: number) => {
      const clamped = Math.max(0, Math.min(1, val));
      crackRef.current = clamped;
      if (clamped >= 1.0) {
        triggerGrandShatterRef.current?.();
      }
    },
    getStats: () => ({
      uCrack: crackRef.current,
      isShattered: shatteredRef.current,
      grandShatterShardCount: GRAND_SHATTER_SHARD_COUNT,
    }),
  }));

  useEffect(() => {
    const container = mountRef.current;
    if (!container) return;

    const isSoftwareGl = (() => {
      try {
        const probe = document.createElement('canvas');
        const gl = probe.getContext('webgl2') || probe.getContext('webgl');
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

    // 1. Scene, Camera & Renderer
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x04060c);

    const width = Math.max(320, container.clientWidth || window.innerWidth);
    const height = Math.max(320, container.clientHeight || window.innerHeight);

    const camera = new THREE.PerspectiveCamera(58, width / height, 0.1, 140);
    const baseCamPos = new THREE.Vector3(0, -2.55, 6.2);
    const baseLookAt = new THREE.Vector3(0, 2.35, -3.5);
    camera.position.copy(baseCamPos);
    camera.lookAt(baseLookAt);

    const renderer = new THREE.WebGLRenderer({
      antialias: !isSoftwareGl,
      powerPreference: 'high-performance',
    });
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.22;
    renderer.setPixelRatio(isSoftwareGl ? 1 : Math.min(window.devicePixelRatio, 2));
    renderer.setSize(width, height);
    renderer.domElement.style.width = '100%';
    renderer.domElement.style.height = '100%';
    renderer.domElement.style.display = 'block';
    container.innerHTML = '';
    container.appendChild(renderer.domElement);

    const pmremGenerator = new THREE.PMREMGenerator(renderer);
    const envTarget = pmremGenerator.fromScene(new RoomEnvironment(), 0.04);
    scene.environment = envTarget.texture;
    pmremGenerator.dispose();

    // 2. Lighting
    const ambientAbyssLight = new THREE.HemisphereLight(0x162038, 0x04060c, 0.55);
    scene.add(ambientAbyssLight);

    const zenithWorldPos = new THREE.Vector3(0, 5.4, -3.8);
    const anvilTopWorldPos = new THREE.Vector3(0, -2.02, 0.65);

    const vaultCrackPointLight = new THREE.PointLight(0xff9e00, 18.0, 28.0, 1.3);
    vaultCrackPointLight.position.copy(zenithWorldPos);
    scene.add(vaultCrackPointLight);

    const vaultCrackDownLight = new THREE.SpotLight(0xff9e00, 36.0, 30.0, Math.PI / 3.2, 0.65, 1.2);
    vaultCrackDownLight.position.copy(zenithWorldPos);
    vaultCrackDownLight.target.position.copy(anvilTopWorldPos);
    scene.add(vaultCrackDownLight);
    scene.add(vaultCrackDownLight.target);

    const anvilRimLight = new THREE.PointLight(0xff9e00, 4.5, 8.0, 1.5);
    anvilRimLight.position.set(0, -1.35, 1.45);
    scene.add(anvilRimLight);

    const lightningFlashLight = new THREE.PointLight(0x00f0ff, 0.0, 32.0, 1.2);
    lightningFlashLight.position.set(0, 1.8, -1.2);
    scene.add(lightningFlashLight);

    // 3. Minimalist Glowing Metallic Anvil Pedestal
    const anvilGroup = new THREE.Group();
    anvilGroup.position.set(0, -2.55, 0.65);
    scene.add(anvilGroup);

    const anvilMetalMat = new THREE.MeshStandardMaterial({
      color: 0x0c1220,
      metalness: 0.92,
      roughness: 0.24,
      envMapIntensity: 0.55,
      emissive: new THREE.Color(0xff8800),
      emissiveIntensity: 0.08,
    });

    const anvilRuneRimMat = new THREE.MeshStandardMaterial({
      color: 0xffb703,
      metalness: 0.95,
      roughness: 0.15,
      emissive: new THREE.Color(0xff9e00),
      emissiveIntensity: 1.35,
    });

    const anvilCyanCoreMat = new THREE.MeshBasicMaterial({
      color: 0x00f0ff,
      transparent: true,
      opacity: 0.85,
    });

    const plinthGeo = new THREE.CylinderGeometry(1.45, 1.85, 0.34, 8);
    plinthGeo.rotateY(Math.PI / 8);
    const plinthMesh = new THREE.Mesh(plinthGeo, anvilMetalMat);
    plinthMesh.position.y = -0.32;
    anvilGroup.add(plinthMesh);

    const waistGeo = new THREE.BoxGeometry(1.52, 0.38, 0.92);
    const waistMesh = new THREE.Mesh(waistGeo, anvilMetalMat);
    waistMesh.position.y = 0.02;
    anvilGroup.add(waistMesh);

    const anvilTopGeo = new THREE.BoxGeometry(2.15, 0.22, 1.12);
    const anvilTopMesh = new THREE.Mesh(anvilTopGeo, anvilMetalMat);
    anvilTopMesh.position.y = 0.32;
    anvilGroup.add(anvilTopMesh);

    const hornGeo = new THREE.ConeGeometry(0.36, 0.85, 4);
    hornGeo.rotateY(Math.PI / 4);
    hornGeo.rotateZ(Math.PI / 2);
    const leftHorn = new THREE.Mesh(hornGeo, anvilMetalMat);
    leftHorn.position.set(-1.38, 0.28, 0);
    leftHorn.scale.set(1, 1, 1.35);
    anvilGroup.add(leftHorn);

    const rightHorn = new THREE.Mesh(hornGeo, anvilMetalMat);
    rightHorn.rotation.z = -Math.PI;
    rightHorn.position.set(1.38, 0.28, 0);
    rightHorn.scale.set(1, 1, 1.35);
    anvilGroup.add(rightHorn);

    const rimStripGeo = new THREE.BoxGeometry(2.2, 0.04, 1.16);
    const rimStripMesh = new THREE.Mesh(rimStripGeo, anvilRuneRimMat);
    rimStripMesh.position.y = 0.42;
    anvilGroup.add(rimStripMesh);

    const sealRingGeo = new THREE.RingGeometry(0.28, 0.36, 32);
    sealRingGeo.rotateX(-Math.PI / 2);
    const sealRingMesh = new THREE.Mesh(sealRingGeo, anvilCyanCoreMat);
    sealRingMesh.position.y = 0.445;
    anvilGroup.add(sealRingMesh);

    // 4. The Cracking Celestial Vault
    const vaultRadius = 15.5;
    const vaultGeo = new THREE.SphereGeometry(vaultRadius, 96, 64, 0, Math.PI * 2, 0, Math.PI * 0.62);
    const localZenithDir = new THREE.Vector3(0.0, 0.97, 0.24).normalize();

    const vaultUniforms = {
      uTime: { value: 0 },
      uCrack: { value: crackRef.current },
      uShockwaveRadius: { value: 5.0 },
      uShockwaveIntensity: { value: 0.0 },
      uStrikeFlash: { value: 0.0 },
      uZenithDir: { value: localZenithDir },
    };

    const vaultMat = new THREE.ShaderMaterial({
      uniforms: vaultUniforms,
      vertexShader: CELESTIAL_VAULT_VERTEX_SHADER,
      fragmentShader: CELESTIAL_VAULT_FRAGMENT_SHADER,
      side: THREE.BackSide,
      depthWrite: true,
    });

    const vaultMesh = new THREE.Mesh(vaultGeo, vaultMat);
    vaultMesh.position.set(0, -1.8, -1.2);
    vaultMesh.rotation.x = -1.08;
    vaultMesh.renderOrder = 1;
    scene.add(vaultMesh);

    // 5. Volumetric God Rays
    const godRaysGroup = new THREE.Group();
    scene.add(godRaysGroup);

    const godRayMaterials: THREE.ShaderMaterial[] = [];
    const rayConfigs = [
      { x: 0.0, z: -0.2, tiltX: 0.36, tiltZ: 0.0, topR: 0.45, botR: 1.85, seed: 0.1 },
      { x: -1.1, z: -0.6, tiltX: 0.34, tiltZ: 0.18, topR: 0.35, botR: 1.55, seed: 1.4 },
      { x: 1.1, z: -0.6, tiltX: 0.34, tiltZ: -0.18, topR: 0.35, botR: 1.55, seed: 2.7 },
      { x: -2.2, z: -1.2, tiltX: 0.30, tiltZ: 0.32, topR: 0.42, botR: 1.9, seed: 3.9 },
      { x: 2.2, z: -1.2, tiltX: 0.30, tiltZ: -0.32, topR: 0.42, botR: 1.9, seed: 5.2 },
      { x: -0.55, z: -1.5, tiltX: 0.42, tiltZ: 0.08, topR: 0.3, botR: 1.4, seed: 6.5 },
      { x: 0.55, z: -1.5, tiltX: 0.42, tiltZ: -0.08, topR: 0.3, botR: 1.4, seed: 7.8 },
    ];

    rayConfigs.forEach((cfg) => {
      const rayGeo = new THREE.CylinderGeometry(cfg.topR, cfg.botR, 11.5, 24, 1, true);
      const rayMat = new THREE.ShaderMaterial({
        uniforms: {
          uTime: { value: 0 },
          uCrack: { value: crackRef.current },
          uStrikeFlash: { value: 0 },
          uRayColor: { value: new THREE.Color(0xff9e00) },
          uStrikeColor: { value: new THREE.Color(0x00f0ff) },
          uRaySeed: { value: cfg.seed },
        },
        vertexShader: GOD_RAY_VERTEX_SHADER,
        fragmentShader: GOD_RAY_FRAGMENT_SHADER,
        transparent: true,
        depthWrite: false,
        side: THREE.DoubleSide,
        blending: THREE.AdditiveBlending,
      });

      const rayMesh = new THREE.Mesh(rayGeo, rayMat);
      rayMesh.position.set(cfg.x, 2.35, cfg.z - 1.6);
      rayMesh.rotation.x = cfg.tiltX;
      rayMesh.rotation.z = cfg.tiltZ;
      rayMesh.renderOrder = 3;
      godRaysGroup.add(rayMesh);
      godRayMaterials.push(rayMat);
    });

    // 6. 0.1s Cyan Lightning Pillar & Zenith Shockwave Ring
    const lightningGroup = new THREE.Group();
    lightningGroup.visible = false;
    scene.add(lightningGroup);

    const beamVector = new THREE.Vector3().subVectors(zenithWorldPos, anvilTopWorldPos);
    const beamLength = beamVector.length();
    const beamMidpoint = new THREE.Vector3().addVectors(anvilTopWorldPos, zenithWorldPos).multiplyScalar(0.5);

    const coreBeamGeo = new THREE.CylinderGeometry(0.11, 0.22, beamLength, 16, 1, true);
    const coreBeamMat = new THREE.MeshBasicMaterial({
      color: 0x00f0ff,
      transparent: true,
      opacity: 0.95,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
      side: THREE.DoubleSide,
    });
    const coreBeamMesh = new THREE.Mesh(coreBeamGeo, coreBeamMat);
    coreBeamMesh.position.copy(beamMidpoint);
    coreBeamMesh.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), beamVector.clone().normalize());
    lightningGroup.add(coreBeamMesh);

    const outerBeamGeo = new THREE.CylinderGeometry(0.38, 0.62, beamLength, 12, 8, true);
    const outerBeamMat = new THREE.MeshBasicMaterial({
      color: 0x80f8ff,
      wireframe: true,
      transparent: true,
      opacity: 0.75,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
    });
    const outerBeamMesh = new THREE.Mesh(outerBeamGeo, outerBeamMat);
    outerBeamMesh.position.copy(beamMidpoint);
    outerBeamMesh.quaternion.copy(coreBeamMesh.quaternion);
    lightningGroup.add(outerBeamMesh);

    const zenithShockRingGeo = new THREE.RingGeometry(0.68, 0.75, 64);
    const zenithShockRingMat = new THREE.MeshBasicMaterial({
      color: 0x00f0ff,
      transparent: true,
      opacity: 0.0,
      side: THREE.DoubleSide,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
    });
    const zenithShockRing = new THREE.Mesh(zenithShockRingGeo, zenithShockRingMat);
    zenithShockRing.position.copy(zenithWorldPos);
    zenithShockRing.lookAt(baseCamPos);
    zenithShockRing.renderOrder = 4;
    scene.add(zenithShockRing);

    // 7. Curated High-Shader Embers (280 GPU particles) & 3D Obsidian Debris (36 Shards)
    const emberCapacity = 280;
    const emberPositions = new Float32Array(emberCapacity * 3);
    const emberVelocities = new Float32Array(emberCapacity * 3);
    const emberColors = new Float32Array(emberCapacity * 3);
    const emberTimings = new Float32Array(emberCapacity * 3);
    const emberSeeds = new Float32Array(emberCapacity * 2);
    for (let i = 0; i < emberCapacity; i++) {
      emberTimings[i * 3] = -100;
      emberSeeds[i * 2] = Math.random();
      emberSeeds[i * 2 + 1] = i % 3 === 0 ? 1.0 : 0.0;
    }

    const emberGeo = new THREE.BufferGeometry();
    const emberPosAttr = new THREE.BufferAttribute(emberPositions, 3);
    const emberVelAttr = new THREE.BufferAttribute(emberVelocities, 3);
    const emberColAttr = new THREE.BufferAttribute(emberColors, 3);
    const emberTimAttr = new THREE.BufferAttribute(emberTimings, 3);
    const emberSeedAttr = new THREE.BufferAttribute(emberSeeds, 2);
    emberPosAttr.setUsage(THREE.DynamicDrawUsage);
    emberVelAttr.setUsage(THREE.DynamicDrawUsage);
    emberColAttr.setUsage(THREE.DynamicDrawUsage);
    emberTimAttr.setUsage(THREE.DynamicDrawUsage);
    emberSeedAttr.setUsage(THREE.DynamicDrawUsage);

    emberGeo.setAttribute('position', emberPosAttr);
    emberGeo.setAttribute('aVelocity', emberVelAttr);
    emberGeo.setAttribute('aColor', emberColAttr);
    emberGeo.setAttribute('aTiming', emberTimAttr);
    emberGeo.setAttribute('aSeed', emberSeedAttr);

    const emberUniforms = {
      uTime: { value: 0 },
      uGravity: { value: 5.8 },
      uPixelRatio: { value: renderer.getPixelRatio() },
    };

    const emberMat = new THREE.ShaderMaterial({
      uniforms: emberUniforms,
      vertexShader: EMBER_PARTICLES_VERTEX_SHADER,
      fragmentShader: EMBER_PARTICLES_FRAGMENT_SHADER,
      transparent: true,
      depthWrite: false,
      blending: THREE.AdditiveBlending,
    });

    const emberPoints = new THREE.Points(emberGeo, emberMat);
    emberPoints.frustumCulled = false;
    emberPoints.renderOrder = 5;
    scene.add(emberPoints);

    let emberCursor = 0;
    const spawnFallingEmbersAndSparks = (currentTime: number, count: number, fromAnvil: boolean) => {
      for (let i = 0; i < count; i++) {
        const idx = (emberCursor + i) % emberCapacity;
        const i3 = idx * 3;
        const i2 = idx * 2;

        if (fromAnvil) {
          const angle = Math.random() * Math.PI * 2;
          const speed = 1.6 + Math.random() * 4.2;
          emberPositions[i3] = (Math.random() - 0.5) * 1.1;
          emberPositions[i3 + 1] = -2.0;
          emberPositions[i3 + 2] = 0.65 + (Math.random() - 0.5) * 0.6;

          emberVelocities[i3] = Math.cos(angle) * speed;
          emberVelocities[i3 + 1] = 3.8 + Math.random() * 5.2;
          emberVelocities[i3 + 2] = Math.sin(angle) * speed;

          const isCyan = i % 2 === 0;
          emberColors[i3] = isCyan ? 0.0 : 1.0;
          emberColors[i3 + 1] = isCyan ? 0.94 : 0.72 + Math.random() * 0.22;
          emberColors[i3 + 2] = isCyan ? 1.0 : 0.14;
          emberSeeds[i2] = Math.random();
          emberSeeds[i2 + 1] = isCyan ? 1.0 : 0.0;
        } else {
          const spreadRadius = 0.8 + crackRef.current * 5.5;
          const theta = Math.random() * Math.PI * 2;
          const r = Math.random() * spreadRadius;
          emberPositions[i3] = Math.cos(theta) * r * 1.3;
          emberPositions[i3 + 1] = 3.5 + Math.random() * 3.1;
          emberPositions[i3 + 2] = -2.0 - Math.random() * 4.0;

          emberVelocities[i3] = (Math.random() - 0.5) * 2.0;
          emberVelocities[i3 + 1] = -1.0 - Math.random() * 2.5;
          emberVelocities[i3 + 2] = 0.8 + Math.random() * 2.4;

          const isArcSpark = i % 4 === 0;
          emberColors[i3] = isArcSpark ? 0.1 : 1.0;
          emberColors[i3 + 1] = isArcSpark ? 0.92 : 0.48 + Math.random() * 0.38;
          emberColors[i3 + 2] = isArcSpark ? 1.0 : 0.08 + Math.random() * 0.18;
          emberSeeds[i2] = Math.random();
          emberSeeds[i2 + 1] = isArcSpark ? 1.0 : 0.0;
        }

        const lead = (i / Math.max(1, count)) * 0.14;
        emberTimings[i3] = currentTime - lead;
        emberTimings[i3 + 1] = 1.6 + Math.random() * 1.3;
        emberTimings[i3 + 2] = fromAnvil ? 22.0 + Math.random() * 16.0 : 20.0 + Math.random() * 18.0;
      }
      emberCursor = (emberCursor + count) % emberCapacity;
      emberPosAttr.needsUpdate = true;
      emberVelAttr.needsUpdate = true;
      emberColAttr.needsUpdate = true;
      emberTimAttr.needsUpdate = true;
      emberSeedAttr.needsUpdate = true;
    };

    // 3D Falling Stone Debris (36 Shards)
    const debrisCount = 36;
    const debrisGeo = new THREE.OctahedronGeometry(0.22, 1);
    const shardShaderUniforms = { uTime: { value: 0 } };
    const debrisMat = new THREE.ShaderMaterial({
      uniforms: shardShaderUniforms,
      vertexShader: SHARD_CRYSTAL_VERTEX_SHADER,
      fragmentShader: SHARD_CRYSTAL_FRAGMENT_SHADER,
      side: THREE.DoubleSide,
    });
    const debrisInstanced = new THREE.InstancedMesh(debrisGeo, debrisMat, debrisCount);
    debrisInstanced.instanceMatrix.setUsage(THREE.DynamicDrawUsage);
    debrisInstanced.frustumCulled = false;
    scene.add(debrisInstanced);

    const tmpDebrisColor = new THREE.Color();
    for (let i = 0; i < debrisCount; i++) {
      tmpDebrisColor.setHex(i % 3 === 0 ? 0x00f0ff : 0xff9e00);
      debrisInstanced.setColorAt(i, tmpDebrisColor);
    }
    if (debrisInstanced.instanceColor) {
      debrisInstanced.instanceColor.needsUpdate = true;
    }

    const debrisState = Array.from({ length: debrisCount }, () => ({
      active: false,
      x: 0,
      y: -50,
      z: 0,
      vx: 0,
      vy: 0,
      vz: 0,
      rx: 0,
      ry: 0,
      rz: 0,
      wx: 0,
      wy: 0,
      wz: 0,
      scale: 0,
    }));
    let debrisCursor = 0;

    const spawnFallingStoneDebris = (burstCount: number) => {
      const spread = 1.2 + crackRef.current * 4.8;
      for (let i = 0; i < burstCount; i++) {
        const d = debrisState[debrisCursor];
        debrisCursor = (debrisCursor + 1) % debrisCount;
        d.active = true;
        d.x = (Math.random() - 0.5) * spread * 2.0;
        d.y = 3.8 + Math.random() * 3.2;
        d.z = -1.8 - Math.random() * 4.2;
        d.vx = (Math.random() - 0.5) * 2.2;
        d.vy = -1.6 - Math.random() * 2.8;
        d.vz = 1.1 + Math.random() * 2.5;
        d.rx = Math.random() * Math.PI * 2;
        d.ry = Math.random() * Math.PI * 2;
        d.rz = Math.random() * Math.PI * 2;
        d.wx = (Math.random() - 0.5) * 7.5;
        d.wy = (Math.random() - 0.5) * 7.5;
        d.wz = (Math.random() - 0.5) * 7.5;
        d.scale = 0.55 + Math.random() * 0.85;
      }
    };

    // 8. The Grand Shatter System
    const nebulaDomeGeo = new THREE.SphereGeometry(42, 64, 48);
    const nebulaUniforms = {
      uTime: { value: 0 },
      uReveal: { value: 0.0 },
    };
    const nebulaDomeMat = new THREE.ShaderMaterial({
      uniforms: nebulaUniforms,
      vertexShader: COSMIC_NEBULA_VERTEX_SHADER,
      fragmentShader: COSMIC_NEBULA_FRAGMENT_SHADER,
      side: THREE.BackSide,
      depthWrite: false,
    });
    const nebulaDomeMesh = new THREE.Mesh(nebulaDomeGeo, nebulaDomeMat);
    nebulaDomeMesh.visible = false;
    nebulaDomeMesh.renderOrder = 0;
    scene.add(nebulaDomeMesh);

    const galaxyStarCount = 420;
    const galaxyPositions = new Float32Array(galaxyStarCount * 3);
    const galaxyColors = new Float32Array(galaxyStarCount * 3);
    const galaxyStarMeta = new Float32Array(galaxyStarCount * 2);
    const cCore = new THREE.Color(0xffd23f);
    const cCyanArm = new THREE.Color(0x00f0ff);
    const cMagentaArm = new THREE.Color(0xec4899);
    const cVioletOuter = new THREE.Color(0x8b5cf6);

    for (let i = 0; i < galaxyStarCount; i++) {
      const i3 = i * 3;
      const i2 = i * 2;
      const arm = i % 5;
      const radius = Math.pow(Math.random(), 1.35) * 17.5;
      const spinAngle = radius * 0.85;
      const armAngle = (arm * Math.PI * 2) / 5 + spinAngle;
      const randomX = Math.pow(Math.random(), 2.0) * (Math.random() < 0.5 ? 1 : -1) * 1.6;
      const randomY = Math.pow(Math.random(), 2.0) * (Math.random() < 0.5 ? 1 : -1) * 0.65;
      const randomZ = Math.pow(Math.random(), 2.0) * (Math.random() < 0.5 ? 1 : -1) * 1.6;

      galaxyPositions[i3] = Math.cos(armAngle) * radius + randomX;
      galaxyPositions[i3 + 1] = randomY;
      galaxyPositions[i3 + 2] = Math.sin(armAngle) * radius + randomZ;

      const t = radius / 17.5;
      const mixed = cCore.clone();
      if (t < 0.35) {
        mixed.lerp(cCyanArm, t / 0.35);
      } else if (t < 0.7) {
        mixed.copy(cCyanArm).lerp(cMagentaArm, (t - 0.35) / 0.35);
      } else {
        mixed.copy(cMagentaArm).lerp(cVioletOuter, (t - 0.7) / 0.3);
      }
      galaxyColors[i3] = mixed.r;
      galaxyColors[i3 + 1] = mixed.g;
      galaxyColors[i3 + 2] = mixed.b;

      galaxyStarMeta[i2] = 10.0 + Math.random() * 18.0;
      galaxyStarMeta[i2 + 1] = Math.random();
    }

    const galaxyGeo = new THREE.BufferGeometry();
    galaxyGeo.setAttribute('position', new THREE.BufferAttribute(galaxyPositions, 3));
    galaxyGeo.setAttribute('aColor', new THREE.BufferAttribute(galaxyColors, 3));
    galaxyGeo.setAttribute('aStarMeta', new THREE.BufferAttribute(galaxyStarMeta, 2));

    const galaxyUniforms = {
      uTime: { value: 0 },
      uReveal: { value: 0.0 },
      uPixelRatio: { value: renderer.getPixelRatio() },
    };
    const galaxyMat = new THREE.ShaderMaterial({
      uniforms: galaxyUniforms,
      vertexShader: GALAXY_STAR_VERTEX_SHADER,
      fragmentShader: GALAXY_STAR_FRAGMENT_SHADER,
      transparent: true,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
    });
    const galaxyPoints = new THREE.Points(galaxyGeo, galaxyMat);
    galaxyPoints.position.set(0, 5.2, -14.5);
    galaxyPoints.rotation.x = 0.92;
    galaxyPoints.rotation.z = -0.24;
    galaxyPoints.visible = false;
    scene.add(galaxyPoints);

    const grandShardGeo = new THREE.OctahedronGeometry(0.38, 1);
    grandShardGeo.scale(1.25, 0.45, 0.9);
    const grandShardMat = new THREE.ShaderMaterial({
      uniforms: shardShaderUniforms,
      vertexShader: SHARD_CRYSTAL_VERTEX_SHADER,
      fragmentShader: SHARD_CRYSTAL_FRAGMENT_SHADER,
      side: THREE.DoubleSide,
    });

    const grandShatterMesh = new THREE.InstancedMesh(grandShardGeo, grandShardMat, GRAND_SHATTER_SHARD_COUNT);
    grandShatterMesh.instanceMatrix.setUsage(THREE.DynamicDrawUsage);
    grandShatterMesh.visible = false;
    grandShatterMesh.frustumCulled = false;
    grandShatterMesh.renderOrder = 4;
    scene.add(grandShatterMesh);

    const shardColor = new THREE.Color();
    const shardOrigins = new Float32Array(GRAND_SHATTER_SHARD_COUNT * 3);
    const shardVelocities = new Float32Array(GRAND_SHATTER_SHARD_COUNT * 3);
    const shardRotations = new Float32Array(GRAND_SHATTER_SHARD_COUNT * 3);
    const shardAngularVel = new Float32Array(GRAND_SHATTER_SHARD_COUNT * 3);
    const shardBaseScales = new Float32Array(GRAND_SHATTER_SHARD_COUNT);

    const goldenRatio = (1 + Math.sqrt(5)) / 2;
    for (let i = 0; i < GRAND_SHATTER_SHARD_COUNT; i++) {
      const i3 = i * 3;
      const u = (i + 0.5) / GRAND_SHATTER_SHARD_COUNT;
      const r = 0.24 + 0.76 * Math.sqrt(u);
      const phi = (2 * Math.PI * i) / goldenRatio;

      const nx = r * Math.cos(phi);
      const ny = r * Math.sin(phi);
      const nz = -Math.sqrt(Math.max(0.05, 1.0 - r * r * 0.65));

      shardOrigins[i3] = nx * 8.5;
      shardOrigins[i3 + 1] = 2.4 + ny * 5.6;
      shardOrigins[i3 + 2] = nz * 6.0 - 2.2;

      const speed = 11.5 + (i % 19) * 1.25;
      shardVelocities[i3] = nx * speed * 1.65;
      shardVelocities[i3 + 1] = ny * speed * 1.35 + 1.8;
      shardVelocities[i3 + 2] = nz * speed * 0.75 + 5.2;

      shardRotations[i3] = (i * 1.1) % (Math.PI * 2);
      shardRotations[i3 + 1] = (i * 1.9) % (Math.PI * 2);
      shardRotations[i3 + 2] = (i * 2.7) % (Math.PI * 2);

      shardAngularVel[i3] = ((i % 9) - 4) * 3.4;
      shardAngularVel[i3 + 1] = ((i % 7) - 3) * 3.8;
      shardAngularVel[i3 + 2] = ((i % 11) - 5) * 3.1;

      shardBaseScales[i] = 0.42 + (i % 7) * 0.12;

      if (i % 3 === 0) shardColor.setHex(0xff9e00);
      else if (i % 4 === 0) shardColor.setHex(0x00f0ff);
      else shardColor.setHex(0xffd23f);
      grandShatterMesh.setColorAt(i, shardColor);
    }
    if (grandShatterMesh.instanceColor) {
      grandShatterMesh.instanceColor.needsUpdate = true;
    }

    // Interactive Controllers
    let elapsed = 0;
    let lightningTimer = -1;
    let shockwaveTimer = -1;
    let strikeFlash = 0;
    let cameraShake = 0;
    let shatterElapsed = -1;

    const executeGrandShatter = () => {
      if (shatteredRef.current) return;
      shatteredRef.current = true;
      shatterElapsed = 0;
      cameraShake = 0.85;

      soundEngine.playGlobalBurstFanfare();

      vaultMesh.visible = false;
      godRaysGroup.visible = false;
      grandShatterMesh.visible = true;
      nebulaDomeMesh.visible = true;
      galaxyPoints.visible = true;

      spawnFallingEmbersAndSparks(elapsed, 45, false);
      spawnFallingStoneDebris(14);
      onGrandShatter?.();
    };

    const executeStrike = (grade: string = 'PERFECT', stance: StanceKey = activeStance) => {
      if (shatteredRef.current) return;

      const result = advanceVaultCrack(crackRef.current, CRACK_INCREMENT_PER_STRIKE);
      crackRef.current = result.nextCrack;

      // 1. Launch 0.1s Cyan Lightning Impulse Pillar
      lightningTimer = 0;
      lightningGroup.visible = true;

      // 2. Trigger Radial Shockwave
      shockwaveTimer = 0;
      strikeFlash = 1.0;
      cameraShake = 0.28 + result.nextCrack * 0.25;

      // 3. Play strike audio
      soundEngine.playAnvilStrike(grade as any, stance, result.nextCrack >= 0.75 || overdriveActive);

      // 4. Spawn embers and shards
      spawnFallingEmbersAndSparks(elapsed, 16, true);
      spawnFallingEmbersAndSparks(elapsed, 20, false);
      spawnFallingStoneDebris(5);

      onStrike?.();

      if (result.triggeredGrandShatter || result.nextCrack >= 1.0) {
        executeGrandShatter();
      }
    };

    const resetVault = () => {
      crackRef.current = 0.0;
      shatteredRef.current = false;
      shatterElapsed = -1;
      lightningTimer = -1;
      shockwaveTimer = -1;
      strikeFlash = 0;
      cameraShake = 0;

      vaultMesh.visible = true;
      godRaysGroup.visible = true;
      grandShatterMesh.visible = false;
      nebulaDomeMesh.visible = false;
      galaxyPoints.visible = false;
      lightningGroup.visible = false;
      vaultUniforms.uCrack.value = 0.0;
      vaultUniforms.uShockwaveIntensity.value = 0.0;
      onResetVault?.();
    };

    triggerStrikeRef.current = executeStrike;
    resetVaultRef.current = resetVault;
    triggerGrandShatterRef.current = executeGrandShatter;

    // Window global debug API
    (window as unknown as Record<string, unknown>).__celestialVault = {
      strike: executeStrike,
      setCrack: (val: number) => {
        const clamped = Math.max(0, Math.min(1, val));
        crackRef.current = clamped;
        if (clamped >= 1.0) executeGrandShatter();
        else if (shatteredRef.current) {
          resetVault();
          crackRef.current = clamped;
        }
      },
      triggerGrandShatter: executeGrandShatter,
      reset: resetVault,
      getStats: () => ({
        uCrack: crackRef.current,
        isShattered: shatteredRef.current,
        grandShatterShardCount: GRAND_SHATTER_SHARD_COUNT,
      }),
    };

    const ro = new ResizeObserver(() => {
      if (!container) return;
      const w = Math.max(320, container.clientWidth);
      const h = Math.max(320, container.clientHeight);
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h);
      emberUniforms.uPixelRatio.value = renderer.getPixelRatio();
    });
    ro.observe(container);

    let frameId = 0;
    let lastTime = performance.now();
    let ambientEmberTimer = 0;
    const dummy = new THREE.Object3D();

    const tick = () => {
      const now = performance.now();
      const dt = Math.min((now - lastTime) / 1000, 0.05);
      lastTime = now;
      elapsed += dt;

      const currentCrack = crackRef.current;

      ambientEmberTimer += dt;
      if (!shatteredRef.current && currentCrack > 0.08 && ambientEmberTimer >= 0.24) {
        ambientEmberTimer = 0;
        spawnFallingEmbersAndSparks(elapsed, Math.ceil(3 + currentCrack * 7), false);
      }

      if (lightningTimer >= 0) {
        lightningTimer += dt;
        if (lightningTimer <= LIGHTNING_PILLAR_ASCENT_SEC) {
          const progress = Math.min(1.0, lightningTimer / LIGHTNING_PILLAR_ASCENT_SEC);
          const currentMid = new THREE.Vector3().lerpVectors(anvilTopWorldPos, zenithWorldPos, progress * 0.5);
          coreBeamMesh.position.copy(currentMid);
          coreBeamMesh.scale.set(1.0 + Math.random() * 0.35, progress, 1.0 + Math.random() * 0.35);
          outerBeamMesh.position.copy(currentMid);
          outerBeamMesh.scale.set(1.2 + Math.random() * 0.6, progress, 1.2 + Math.random() * 0.6);
          outerBeamMesh.rotation.y = Math.random() * Math.PI * 2;
          coreBeamMat.opacity = 1.0;
          outerBeamMat.opacity = 0.85;
          lightningFlashLight.intensity = 45.0;
        } else if (lightningTimer <= 0.32) {
          const fade = 1.0 - (lightningTimer - LIGHTNING_PILLAR_ASCENT_SEC) / 0.22;
          coreBeamMesh.position.copy(beamMidpoint);
          coreBeamMesh.scale.set(fade * (0.8 + Math.random() * 0.5), 1.0, fade);
          outerBeamMesh.position.copy(beamMidpoint);
          outerBeamMesh.scale.set(fade * 1.4, 1.0, fade * 1.4);
          outerBeamMesh.rotation.y = Math.random() * Math.PI * 2;
          coreBeamMat.opacity = fade;
          outerBeamMat.opacity = fade * 0.75;
          lightningFlashLight.intensity = fade * 38.0;
        } else {
          lightningGroup.visible = false;
          lightningFlashLight.intensity = 0.0;
          lightningTimer = -1;
        }
      }

      if (shockwaveTimer >= 0) {
        shockwaveTimer += dt;
        const duration = 0.95;
        if (shockwaveTimer <= duration) {
          const prog = shockwaveTimer / duration;
          const easeOut = 1.0 - Math.pow(1.0 - prog, 2.2);
          vaultUniforms.uShockwaveRadius.value = easeOut * 1.65;
          vaultUniforms.uShockwaveIntensity.value = (1.0 - prog) * 1.35;

          const ringScale = 0.5 + easeOut * 11.5;
          zenithShockRing.scale.setScalar(ringScale);
          zenithShockRingMat.opacity = (1.0 - prog) * 0.52;
        } else {
          vaultUniforms.uShockwaveIntensity.value = 0.0;
          zenithShockRingMat.opacity = 0.0;
          shockwaveTimer = -1;
        }
      }

      if (strikeFlash > 0) {
        strikeFlash = Math.max(0, strikeFlash - dt * 3.2);
      }

      vaultUniforms.uTime.value = elapsed;
      vaultUniforms.uCrack.value = currentCrack;
      vaultUniforms.uStrikeFlash.value = strikeFlash;

      godRayMaterials.forEach((mat) => {
        mat.uniforms.uTime.value = elapsed;
        mat.uniforms.uCrack.value = currentCrack;
        mat.uniforms.uStrikeFlash.value = strikeFlash;
      });

      vaultCrackPointLight.intensity = 10.0 + currentCrack * 34.0 + strikeFlash * 25.0;
      vaultCrackDownLight.intensity = 22.0 + currentCrack * 55.0 + strikeFlash * 35.0;
      anvilMetalMat.emissiveIntensity = 0.06 + currentCrack * 0.22 + strikeFlash * 0.28;
      anvilRuneRimMat.emissiveIntensity = 1.1 + currentCrack * 2.2 + strikeFlash * 1.8;

      emberUniforms.uTime.value = elapsed;
      shardShaderUniforms.uTime.value = elapsed;

      for (let i = 0; i < debrisCount; i++) {
        const d = debrisState[i];
        if (!d.active) {
          dummy.position.set(0, -100, 0);
          dummy.scale.setScalar(0);
          dummy.updateMatrix();
          debrisInstanced.setMatrixAt(i, dummy.matrix);
          continue;
        }
        d.vy -= 7.8 * dt;
        d.x += d.vx * dt;
        d.y += d.vy * dt;
        d.z += d.vz * dt;
        d.rx += d.wx * dt;
        d.ry += d.wy * dt;
        d.rz += d.wz * dt;
        d.scale = Math.max(0, d.scale - dt * 0.32);

        if (d.y < -4.5 || d.scale <= 0.01) {
          d.active = false;
        }

        dummy.position.set(d.x, d.y, d.z);
        dummy.rotation.set(d.rx, d.ry, d.rz);
        dummy.scale.setScalar(d.scale);
        dummy.updateMatrix();
        debrisInstanced.setMatrixAt(i, dummy.matrix);
      }
      debrisInstanced.instanceMatrix.needsUpdate = true;

      if (shatteredRef.current && shatterElapsed >= 0) {
        shatterElapsed += dt;
        nebulaUniforms.uTime.value = elapsed;
        const reveal = Math.min(1.0, 0.35 + shatterElapsed * 2.2);
        nebulaUniforms.uReveal.value = reveal;
        galaxyUniforms.uTime.value = elapsed;
        galaxyUniforms.uReveal.value = reveal;

        galaxyPoints.rotation.y = elapsed * 0.16;

        const shardDuration = 3.6;
        const progress = Math.min(1.0, shatterElapsed / shardDuration);
        const scaleFade = Math.max(0, 1.0 - progress * progress);

        for (let i = 0; i < GRAND_SHATTER_SHARD_COUNT; i++) {
          const i3 = i * 3;
          const sx = shardOrigins[i3] + shardVelocities[i3] * shatterElapsed;
          const sy =
            shardOrigins[i3 + 1] +
            shardVelocities[i3 + 1] * shatterElapsed -
            0.5 * 2.4 * shatterElapsed * shatterElapsed;
          const sz = shardOrigins[i3 + 2] + shardVelocities[i3 + 2] * shatterElapsed;

          dummy.position.set(sx, sy, sz);
          dummy.rotation.set(
            shardRotations[i3] + shardAngularVel[i3] * shatterElapsed,
            shardRotations[i3 + 1] + shardAngularVel[i3 + 1] * shatterElapsed,
            shardRotations[i3 + 2] + shardAngularVel[i3 + 2] * shatterElapsed
          );
          dummy.scale.setScalar(shardBaseScales[i] * scaleFade);
          dummy.updateMatrix();
          grandShatterMesh.setMatrixAt(i, dummy.matrix);
        }
        grandShatterMesh.instanceMatrix.needsUpdate = true;
      }

      if (cameraShake > 0) {
        cameraShake = Math.max(0, cameraShake - dt * 1.6);
        const s = cameraShake * cameraShake * 0.35;
        camera.position.set(
          baseCamPos.x + (Math.random() - 0.5) * s,
          baseCamPos.y + (Math.random() - 0.5) * s,
          baseCamPos.z + (Math.random() - 0.5) * s * 0.5
        );
      } else {
        camera.position.copy(baseCamPos);
      }
      camera.lookAt(baseLookAt);

      renderer.render(scene, camera);
      frameId = requestAnimationFrame(tick);
    };

    tick();

    return () => {
      cancelAnimationFrame(frameId);
      ro.disconnect();
      vaultGeo.dispose();
      vaultMat.dispose();
      emberGeo.dispose();
      emberMat.dispose();
      debrisGeo.dispose();
      debrisMat.dispose();
      nebulaDomeGeo.dispose();
      nebulaDomeMat.dispose();
      galaxyGeo.dispose();
      galaxyMat.dispose();
      grandShardGeo.dispose();
      grandShardMat.dispose();
      envTarget.dispose();
      renderer.dispose();
    };
  }, []);

  return <div ref={mountRef} className="w-full h-full" />;
});
