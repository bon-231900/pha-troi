import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';

interface CelestialTitleCanvas3DProps {
  className?: string;
}

export const CelestialTitleCanvas3D: React.FC<CelestialTitleCanvas3DProps> = ({ className = '' }) => {
  const mountRef = useRef<HTMLDivElement | null>(null);
  const [hasWebGL, setHasWebGL] = useState(true);

  useEffect(() => {
    const container = mountRef.current;
    if (!container) return;

    // Check WebGL availability
    const testCanvas = document.createElement('canvas');
    const gl = testCanvas.getContext('webgl') || testCanvas.getContext('experimental-webgl');
    if (!gl) {
      setHasWebGL(false);
      return;
    }

    let isDisposed = false;
    let animId: number = 0;

    // Scene & Camera setup
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 100);
    camera.position.set(0, 0, 5.0);

    const renderer = new THREE.WebGLRenderer({
      antialias: true,
      alpha: false,
      powerPreference: 'high-performance',
    });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    renderer.setSize(container.clientWidth, container.clientHeight);
    container.appendChild(renderer.domElement);

    // Texture Loading
    const base = import.meta.env.BASE_URL || './';
    const cleanBase = base.endsWith('/') ? base : base + '/';
    const textureLoader = new THREE.TextureLoader();
    const splashTexture = textureLoader.load(`${cleanBase}assets/art/celestial_splash_bg.webp`);
    splashTexture.colorSpace = THREE.SRGBColorSpace;
    splashTexture.minFilter = THREE.LinearFilter;
    splashTexture.magFilter = THREE.LinearFilter;

    // -------------------------------------------------------------------------
    // 1. BACKGROUND SHADER PLANE (Preserves 100% of the artwork + Living Shimmer)
    // -------------------------------------------------------------------------
    const bgUniforms = {
      uTexture: { value: splashTexture },
      uTime: { value: 0.0 },
      uLightningFlash: { value: 0.0 },
      uResolution: { value: new THREE.Vector2(container.clientWidth, container.clientHeight) },
      uTextureResolution: { value: new THREE.Vector2(1376, 768) },
    };

    const bgVertexShader = `
      varying vec2 vUv;
      void main() {
        vUv = uv;
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
      }
    `;

    const bgFragmentShader = `
      uniform sampler2D uTexture;
      uniform float uTime;
      uniform float uLightningFlash;
      uniform vec2 uResolution;
      uniform vec2 uTextureResolution;
      varying vec2 vUv;

      void main() {
        // Calculate cover UV so 16:9 texture fits any viewport perfectly
        vec2 s = uResolution;
        vec2 i = uTextureResolution;
        float rs = s.x / s.y;
        float ri = i.x / i.y;
        vec2 newUv = vUv;
        if (rs > ri) {
          float scale = ri / rs;
          newUv.y = (newUv.y - 0.5) * scale + 0.5;
        } else {
          float scale = rs / ri;
          newUv.x = (newUv.x - 0.5) * scale + 0.5;
        }

        // Heat shimmer wave over central golden pillar (x: ~0.45..0.55, y: ~0.25..0.85)
        float pillarMask = smoothstep(0.18, 0.0, abs(newUv.x - 0.5)) * smoothstep(0.2, 0.45, newUv.y);
        vec2 distortedUv = newUv;
        if (pillarMask > 0.01) {
          float heat = sin(newUv.y * 35.0 - uTime * 5.0) * cos(newUv.x * 25.0 + uTime * 3.5);
          distortedUv.x += heat * 0.0022 * pillarMask;
        }

        vec4 col = texture2D(uTexture, distortedUv);

        // Breathing golden god-rays pulse at central pillar
        float pulse = 0.5 + 0.5 * sin(uTime * 1.8);
        col.rgb += vec3(0.35, 0.22, 0.05) * pillarMask * (0.15 + 0.12 * pulse);

        // Sky crack lightning flash
        if (uLightningFlash > 0.01) {
          // Upper sky fractures glow with cyan celestial thunder
          float skyHeightMask = smoothstep(0.55, 0.95, newUv.y);
          col.rgb += vec3(0.0, 0.85, 1.0) * uLightningFlash * skyHeightMask * 0.45;
          // Global lightning ambient flash
          col.rgb += vec3(0.12, 0.16, 0.25) * uLightningFlash * 0.28;
        }

        gl_FragColor = col;
      }
    `;

    const bgMaterial = new THREE.ShaderMaterial({
      uniforms: bgUniforms,
      vertexShader: bgVertexShader,
      fragmentShader: bgFragmentShader,
      depthWrite: false,
      depthTest: false,
    });

    // Frustum sizing at z = 0
    const vFOV = (camera.fov * Math.PI) / 180;
    const planeH = 2 * Math.tan(vFOV / 2) * camera.position.z;
    const planeW = planeH * camera.aspect;
    const bgGeometry = new THREE.PlaneGeometry(planeW, planeH);
    const bgMesh = new THREE.Mesh(bgGeometry, bgMaterial);
    scene.add(bgMesh);

    // -------------------------------------------------------------------------
    // 2. 3D FLOATING EMBER PARTICLE SYSTEM (GPU Points)
    // -------------------------------------------------------------------------
    const EMBER_COUNT = 140;
    const emberPositions = new Float32Array(EMBER_COUNT * 3);
    const emberVelocities = new Float32Array(EMBER_COUNT * 3);
    const emberMeta = new Float32Array(EMBER_COUNT * 3); // size, seed, alpha
    const emberColors = new Float32Array(EMBER_COUNT * 3);

    for (let i = 0; i < EMBER_COUNT; i++) {
      // Spread across 3D space in front of background plane
      emberPositions[i * 3 + 0] = (Math.random() - 0.5) * planeW * 1.1;
      emberPositions[i * 3 + 1] = (Math.random() - 0.5) * planeH * 1.1;
      emberPositions[i * 3 + 2] = Math.random() * 2.5 + 0.3; // z between plane (0) and camera (5)

      // Upward convection drift with gentle lateral sway
      emberVelocities[i * 3 + 0] = (Math.random() - 0.5) * 0.25;
      emberVelocities[i * 3 + 1] = Math.random() * 0.35 + 0.15; // upward
      emberVelocities[i * 3 + 2] = (Math.random() - 0.5) * 0.08;

      emberMeta[i * 3 + 0] = Math.random() * 18.0 + 8.0; // size
      emberMeta[i * 3 + 1] = Math.random() * 100.0; // random phase seed
      emberMeta[i * 3 + 2] = Math.random() * 0.5 + 0.5; // base opacity

      // 75% Gold/Amber embers, 25% Cyan lightning sparks
      if (Math.random() < 0.75) {
        emberColors[i * 3 + 0] = 1.0;
        emberColors[i * 3 + 1] = 0.65 + Math.random() * 0.35;
        emberColors[i * 3 + 2] = 0.05 + Math.random() * 0.15;
      } else {
        emberColors[i * 3 + 0] = 0.2;
        emberColors[i * 3 + 1] = 0.9;
        emberColors[i * 3 + 2] = 1.0;
      }
    }

    const emberGeo = new THREE.BufferGeometry();
    emberGeo.setAttribute('position', new THREE.BufferAttribute(emberPositions, 3));
    emberGeo.setAttribute('aVelocity', new THREE.BufferAttribute(emberVelocities, 3));
    emberGeo.setAttribute('aMeta', new THREE.BufferAttribute(emberMeta, 3));
    emberGeo.setAttribute('aColor', new THREE.BufferAttribute(emberColors, 3));

    const emberUniforms = {
      uTime: { value: 0.0 },
      uPixelRatio: { value: Math.min(window.devicePixelRatio || 1, 2) },
    };

    const emberVertexShader = `
      attribute vec3 aVelocity;
      attribute vec3 aMeta;
      attribute vec3 aColor;
      uniform float uTime;
      uniform float uPixelRatio;
      varying vec3 vColor;
      varying float vAlpha;

      void main() {
        vColor = aColor;
        float seed = aMeta.y;
        float baseAlpha = aMeta.z;

        // Twinkle flicker
        float flicker = 0.6 + 0.4 * sin(uTime * 6.0 + seed);
        vAlpha = baseAlpha * flicker;

        vec4 mvPosition = modelViewMatrix * vec4(position, 1.0);
        float dist = length(mvPosition.xyz);
        gl_PointSize = (aMeta.x * uPixelRatio * 3.5) / dist;
        gl_Position = projectionMatrix * mvPosition;
      }
    `;

    const emberFragmentShader = `
      varying vec3 vColor;
      varying float vAlpha;

      void main() {
        // Soft glowing radial circle
        vec2 coord = gl_PointCoord - vec2(0.5);
        float r = length(coord);
        if (r > 0.5) discard;

        float glow = pow(1.0 - (r * 2.0), 1.8);
        gl_FragColor = vec4(vColor * (1.0 + glow * 1.5), vAlpha * glow);
      }
    `;

    const emberMat = new THREE.ShaderMaterial({
      uniforms: emberUniforms,
      vertexShader: emberVertexShader,
      fragmentShader: emberFragmentShader,
      transparent: true,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
    });

    const emberPoints = new THREE.Points(emberGeo, emberMat);
    scene.add(emberPoints);

    // -------------------------------------------------------------------------
    // 3. LIGHTNING CYCLE CONTROLLER
    // -------------------------------------------------------------------------
    let nextLightningTime = 2.5;
    let lightningFlashTimer = 0.0;
    let flashIntensity = 0.0;

    // -------------------------------------------------------------------------
    // 4. MOUSE PARALLAX TRACKING
    // -------------------------------------------------------------------------
    let mouseX = 0;
    let mouseY = 0;
    let targetCamX = 0;
    let targetCamY = 0;

    const handleMouseMove = (e: MouseEvent) => {
      const rect = container.getBoundingClientRect();
      const nx = ((e.clientX - rect.left) / rect.width) * 2 - 1;
      const ny = -(((e.clientY - rect.top) / rect.height) * 2 - 1);
      mouseX = nx;
      mouseY = ny;
    };

    window.addEventListener('mousemove', handleMouseMove, { passive: true });

    // Handle Resize
    const handleResize = () => {
      if (!container || isDisposed) return;
      const w = container.clientWidth;
      const h = container.clientHeight;
      camera.aspect = w / h;
      camera.updateProjectionMatrix();

      // Recalculate background plane geometry
      const newPlaneH = 2 * Math.tan((camera.fov * Math.PI) / 360) * camera.position.z;
      const newPlaneW = newPlaneH * camera.aspect;
      bgMesh.geometry.dispose();
      bgMesh.geometry = new THREE.PlaneGeometry(newPlaneW, newPlaneH);

      bgUniforms.uResolution.value.set(w, h);
      renderer.setSize(w, h);
      emberUniforms.uPixelRatio.value = Math.min(window.devicePixelRatio || 1, 2);
    };

    const ro = new ResizeObserver(() => handleResize());
    ro.observe(container);

    // -------------------------------------------------------------------------
    // 5. 60 FPS MAIN RENDER LOOP
    // -------------------------------------------------------------------------
    let lastTime = performance.now();

    const animate = (now: number) => {
      if (isDisposed) return;
      animId = requestAnimationFrame(animate);

      const dt = Math.min((now - lastTime) / 1000, 0.05);
      lastTime = now;
      const time = now * 0.001;

      // Update uniforms
      bgUniforms.uTime.value = time;
      emberUniforms.uTime.value = time;

      // Celestial Thunder Cycle (Triggers dynamic strike every 3-5 sec)
      if (time > nextLightningTime) {
        flashIntensity = 1.6;
        lightningFlashTimer = 0.22;
        nextLightningTime = time + 3.2 + Math.random() * 2.8;
      }

      if (lightningFlashTimer > 0) {
        lightningFlashTimer -= dt;
        // Jitter lightning strike
        const flicker = Math.sin(lightningFlashTimer * 45.0) > 0 ? 1.0 : 0.35;
        bgUniforms.uLightningFlash.value = flashIntensity * (lightningFlashTimer / 0.22) * flicker;
      } else {
        bgUniforms.uLightningFlash.value = 0.0;
      }

      // Update 3D Embers movement
      const posAttr = emberGeo.attributes.position as THREE.BufferAttribute;
      const posArr = posAttr.array as Float32Array;

      for (let i = 0; i < EMBER_COUNT; i++) {
        const idx = i * 3;
        // Upward drift
        posArr[idx + 1] += emberVelocities[idx + 1] * dt;
        // Lateral sin wave oscillation
        posArr[idx + 0] += Math.sin(time * 1.8 + emberMeta[i * 3 + 1]) * 0.003;

        // Reset if drifted beyond top
        if (posArr[idx + 1] > planeH * 0.6) {
          posArr[idx + 1] = -planeH * 0.55;
          posArr[idx + 0] = (Math.random() - 0.5) * planeW * 0.8;
        }
      }
      posAttr.needsUpdate = true;

      // Smooth Camera Parallax Damping
      targetCamX = mouseX * 0.28;
      targetCamY = mouseY * 0.18;
      camera.position.x += (targetCamX - camera.position.x) * 0.04;
      camera.position.y += (targetCamY - camera.position.y) * 0.04;
      camera.lookAt(0, 0, 0);

      renderer.render(scene, camera);
    };

    animId = requestAnimationFrame(animate);

    // Cleanup
    return () => {
      isDisposed = true;
      cancelAnimationFrame(animId);
      window.removeEventListener('mousemove', handleMouseMove);
      ro.disconnect();

      bgGeometry.dispose();
      bgMaterial.dispose();
      splashTexture.dispose();

      emberGeo.dispose();
      emberMat.dispose();

      renderer.dispose();
      if (container && renderer.domElement && container.contains(renderer.domElement)) {
        container.removeChild(renderer.domElement);
      }
    };
  }, []);

  if (!hasWebGL) {
    // Fallback to static 2D image if WebGL unavailable
    const base = import.meta.env.BASE_URL || './';
    const cleanBase = base.endsWith('/') ? base : base + '/';
    return (
      <div className={`absolute inset-0 -z-10 overflow-hidden bg-slate-950 ${className}`}>
        <img
          src={`${cleanBase}assets/art/celestial_splash_bg.webp`}
          alt="Phá Trời Background"
          className="w-full h-full object-cover object-center filter brightness-[0.9] contrast-[1.05]"
        />
      </div>
    );
  }

  return (
    <div
      ref={mountRef}
      className={`absolute inset-0 -z-10 overflow-hidden bg-slate-950 select-none pointer-events-none ${className}`}
    />
  );
};
