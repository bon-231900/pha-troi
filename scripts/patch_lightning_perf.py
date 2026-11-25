# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# 1. Update CommunityPanoramicForgeCanvas.tsx
with open('frontend/src/components/CommunityPanoramicForgeCanvas.tsx', 'r', encoding='utf-8') as f:
    c = f.read()

# Update spawnLightningBolt to cap at 3 bolts max
old_spawn = """    const spawnLightningBolt = (
      targetX: number,
      targetY: number,
      color = '#00F0FF',
      power = 1.0,
      lightColor = '#38BDF8',
      hasGroundTendrils = true
    ) => {
      const bolt = createAdvancedLightningBolt(targetX, targetY, {
        viewH,
        color,
        lightColor,
        power,
        hasGroundTendrils,
      });
      lightningBolts.push(bolt);

      // Spawn accompanying rapid electric zap streak particles
      const newZaps = createElectricZapParticles(targetX, targetY, Math.round(14 * power), lightColor, power);
      electricZaps.push(...newZaps);
    };"""

new_spawn = """    const spawnLightningBolt = (
      targetX: number,
      targetY: number,
      color = '#00F0FF',
      power = 1.0,
      lightColor = '#38BDF8',
      hasGroundTendrils = true
    ) => {
      // Keep at most 3 concurrent bolts for buttery smooth 60 FPS
      if (lightningBolts.length >= 3) {
        lightningBolts.shift();
      }
      const bolt = createAdvancedLightningBolt(targetX, targetY, {
        viewH,
        color,
        lightColor,
        power,
        hasGroundTendrils,
      });
      lightningBolts.push(bolt);

      const newZaps = createElectricZapParticles(targetX, targetY, 10, lightColor, power);
      electricZaps.push(...newZaps);
    };"""

if old_spawn in c:
    c = c.replace(old_spawn, new_spawn, 1)
    print("Patched spawnLightningBolt with strict bolt cap.")
else:
    print("Warning: old_spawn not found!")

# Optimize executeHeroStrikeVisuals (1 bolt for normal strikes, 2 max for crit)
old_strike = """      // 1. Primary High-Definition Multi-Pass Lightning Bolt
      spawnLightningBolt(impactX, impactY, sc.glow, isCrit ? 1.85 : 1.35, sc.light, true);

      // 2. Converging Secondary Bolts on Crit or Thunder Stance
      if (isCrit || (currentStanceKey === 'Q' && Math.random() < 0.45)) {
        const extraBolts = isCrit ? 2 : 1;
        for (let eb = 0; eb < extraBolts; eb++) {
          const startX = impactX + (eb === 0 ? -1 : 1) * (95 + Math.random() * 85);
          const bolt = createAdvancedLightningBolt(impactX, impactY, {
            viewH,
            color: sc.glow,
            lightColor: sc.light,
            power: isCrit ? 1.4 : 1.0,
            startX,
            branchCount: isCrit ? 4 : 2,
            hasGroundTendrils: eb === 0,
          });
          lightningBolts.push(bolt);
        }
      }

      // 3. Multi-tier shockwave
      shockwaves.push({
        x: impactX,
        y: impactY,
        radius: 12,
        maxRadius: isCrit ? 95 : 75,
        alpha: 1.0,
        color: sc.light,
      });

      // 4. Electric Zap Streak Particles
      const zapCount = isCrit ? 28 : 16;
      const newZaps = createElectricZapParticles(impactX, impactY, zapCount, sc.spark, isCrit ? 1.5 : 1.1);
      electricZaps.push(...newZaps);"""

new_strike = """      // 1. Primary High-Definition Multi-Pass Lightning Bolt
      spawnLightningBolt(impactX, impactY, sc.glow, isCrit ? 1.4 : 1.15, sc.light, true);

      // 2. Converging Secondary Bolt ONLY on Crit (keeps active bolts <= 2)
      if (isCrit) {
        const startX = impactX + (Math.random() < 0.5 ? -1 : 1) * (70 + Math.random() * 50);
        const bolt = createAdvancedLightningBolt(impactX, impactY, {
          viewH,
          color: sc.glow,
          lightColor: sc.light,
          power: 1.1,
          startX,
          branchCount: 2,
          hasGroundTendrils: false,
        });
        lightningBolts.push(bolt);
      }

      // 3. Multi-tier shockwave
      shockwaves.push({
        x: impactX,
        y: impactY,
        radius: 12,
        maxRadius: isCrit ? 95 : 75,
        alpha: 1.0,
        color: sc.light,
      });

      // 4. Electric Zap Streak Particles (capped to 10 max)
      const zapCount = isCrit ? 10 : 6;
      const newZaps = createElectricZapParticles(impactX, impactY, zapCount, sc.spark, isCrit ? 1.3 : 1.0);
      electricZaps.push(...newZaps);"""

if old_strike in c:
    c = c.replace(old_strike, new_strike, 1)
    print("Optimized executeHeroStrikeVisuals.")
else:
    print("Warning: old_strike not found!")

# Optimize triggerThunderStorm (4 bolts max instead of unbounded)
old_storm = """    triggerThunderStormClosureRef.current = (count = 6, power = 2.0) => {
      const isPortrait = viewW < viewH;
      const groundY = isPortrait ? viewH * 0.65 : (viewH < 500 ? viewH * 0.81 : viewH * 0.825);
      const renderScale = isPortrait ? Math.min(0.48, Math.max(0.36, viewW / 760)) : 0.38;
      const centerX = viewW * 0.5;
      const heroFootX = centerX - 14;
      const impactX = heroFootX + 28 * renderScale;
      const impactY = groundY + 4;

      screenShake = 22;
      flashIntensity = 2.4;

      for (let i = 0; i < count; i++) {
        setTimeout(() => {
          const offsetX = (Math.random() - 0.5) * 60;
          const startX = impactX + (Math.random() - 0.5) * 260;
          const bolt = createAdvancedLightningBolt(impactX + offsetX, impactY, {
            viewH,
            color: '#00F0FF',
            lightColor: '#38BDF8',
            power: power * (0.85 + Math.random() * 0.35),
            startX,
            branchCount: 5,
          });
          lightningBolts.push(bolt);

          const zaps = createElectricZapParticles(impactX + offsetX, impactY, 20, '#E0FFFF', power);
          electricZaps.push(...zaps);
        }, i * 50);
      }
    };"""

new_storm = """    triggerThunderStormClosureRef.current = (count = 4, power = 1.6) => {
      const isPortrait = viewW < viewH;
      const groundY = isPortrait ? viewH * 0.65 : (viewH < 500 ? viewH * 0.81 : viewH * 0.825);
      const renderScale = isPortrait ? Math.min(0.48, Math.max(0.36, viewW / 760)) : 0.38;
      const centerX = viewW * 0.5;
      const heroFootX = centerX - 14;
      const impactX = heroFootX + 28 * renderScale;
      const impactY = groundY + 4;

      screenShake = 16;
      flashIntensity = 1.8;

      const actualCount = Math.min(4, count);
      for (let i = 0; i < actualCount; i++) {
        setTimeout(() => {
          if (lightningBolts.length >= 3) lightningBolts.shift();
          const offsetX = (Math.random() - 0.5) * 40;
          const startX = impactX + (Math.random() - 0.5) * 160;
          const bolt = createAdvancedLightningBolt(impactX + offsetX, impactY, {
            viewH,
            color: '#00F0FF',
            lightColor: '#38BDF8',
            power: power * 0.9,
            startX,
            branchCount: 2,
          });
          lightningBolts.push(bolt);

          const zaps = createElectricZapParticles(impactX + offsetX, impactY, 8, '#E0FFFF', 1.0);
          electricZaps.push(...zaps);
        }, i * 75);
      }
    };"""

if old_storm in c:
    c = c.replace(old_storm, new_storm, 1)
    print("Optimized triggerThunderStorm.")
else:
    print("Warning: old_storm not found!")

# Remove shadowBlur from shockwaves in LAYER 13
old_sw_render = """        for (let i = shockwaves.length - 1; i >= 0; i--) {
          const sw = shockwaves[i];
          ctx.save();
          ctx.globalCompositeOperation = 'lighter';
          ctx.globalAlpha = Math.max(0, sw.alpha);

          // Outer colored electric shockwave ring
          ctx.strokeStyle = sw.color;
          ctx.shadowColor = sw.color;
          ctx.shadowBlur = 18;
          ctx.lineWidth = 3.2 * sw.alpha;
          ctx.beginPath();
          ctx.ellipse(sw.x, sw.y, sw.radius, sw.radius * 0.45, 0, 0, Math.PI * 2);
          ctx.stroke();

          // Inner white-hot shock core
          ctx.strokeStyle = '#FFFFFF';
          ctx.shadowBlur = 4;
          ctx.lineWidth = 1.4 * sw.alpha;
          ctx.beginPath();
          ctx.ellipse(sw.x, sw.y, sw.radius * 0.92, sw.radius * 0.45 * 0.92, 0, 0, Math.PI * 2);
          ctx.stroke();

          ctx.restore();
        }"""

new_sw_render = """        for (let i = shockwaves.length - 1; i >= 0; i--) {
          const sw = shockwaves[i];
          ctx.save();
          ctx.globalCompositeOperation = 'lighter';
          ctx.globalAlpha = Math.max(0, sw.alpha);

          // Outer colored electric ring (NO shadowBlur - uses GPU additive blending)
          ctx.strokeStyle = sw.color;
          ctx.lineWidth = 3.5 * sw.alpha;
          ctx.beginPath();
          ctx.ellipse(sw.x, sw.y, sw.radius, sw.radius * 0.45, 0, 0, Math.PI * 2);
          ctx.stroke();

          // Inner white-hot shock core
          ctx.strokeStyle = '#FFFFFF';
          ctx.lineWidth = 1.5 * sw.alpha;
          ctx.beginPath();
          ctx.ellipse(sw.x, sw.y, sw.radius * 0.90, sw.radius * 0.45 * 0.90, 0, 0, Math.PI * 2);
          ctx.stroke();

          ctx.restore();
        }"""

if old_sw_render in c:
    c = c.replace(old_sw_render, new_sw_render, 1)
    print("Removed shadowBlur from shockwaves in LAYER 13.")
else:
    print("Warning: old_sw_render not found!")

# Fix drawSkyLightningFlash call in LAYER 12
old_layer12_call = """        // Atmospheric Sky Lightning Flash (Illuminates sky, moon & clouds)
        if (lightningBolts.length > 0 && flashIntensity > 0.05) {
          const mainBolt = lightningBolts[lightningBolts.length - 1];
          drawSkyLightningFlash(ctx, viewW, viewH, mainBolt.impactX, mainBolt.color, flashIntensity);
        }

        // Multi-Pass Shader Lightning Rendering (Additive Blending)
        for (let i = 0; i < lightningBolts.length; i++) {
          drawAdvancedLightningBolt(ctx, lightningBolts[i], now);
        }"""

new_layer12_call = """        // Atmospheric Sky Lightning Flash (Illuminates sky, moon & clouds)
        if (lightningBolts.length > 0 && flashIntensity > 0.05) {
          const mainBolt = lightningBolts[lightningBolts.length - 1];
          drawSkyLightningFlash(ctx, viewW, viewH, mainBolt.color, flashIntensity);
        }

        // Multi-Pass Shader Lightning Rendering (Additive Blending, Zero shadowBlur)
        for (let i = 0; i < lightningBolts.length; i++) {
          drawAdvancedLightningBolt(ctx, lightningBolts[i]);
        }"""

if old_layer12_call in c:
    c = c.replace(old_layer12_call, new_layer12_call, 1)
    print("Updated LAYER 12 call parameters.")
else:
    print("Warning: old_layer12_call not found!")

with open('frontend/src/components/CommunityPanoramicForgeCanvas.tsx', 'w', encoding='utf-8') as f:
    f.write(c)

print("CommunityPanoramicForgeCanvas.tsx optimized successfully!")
