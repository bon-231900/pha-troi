# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

with open('frontend/src/components/InteractiveAltarPreview.tsx', 'r', encoding='utf-8') as f:
    c = f.read()

# Add imports
old_imp = """import { SECT_CLASSES, SECT_DEFAULT_SKIN, CHARACTER_SKINS } from '../game/rules';"""
new_imp = """import { SECT_CLASSES, SECT_DEFAULT_SKIN, CHARACTER_SKINS } from '../game/rules';
import {
  type AdvancedLightningBolt,
  type ElectricZapParticle,
  createAdvancedLightningBolt,
  drawAdvancedLightningBolt,
  createElectricZapParticles,
  updateAndDrawElectricZaps,
} from '../game/lightningVFX';"""

if old_imp in c:
    c = c.replace(old_imp, new_imp, 1)
    print("Added imports to InteractiveAltarPreview.")
else:
    print("Warning: old_imp not found!")

# Replace refs
old_refs = """  const lightningBoltsRef = useRef<LightningBolt[]>([]);
  const shockwavesRef = useRef<Shockwave[]>([]);"""

new_refs = """  const lightningBoltsRef = useRef<AdvancedLightningBolt[]>([]);
  const electricZapsRef = useRef<ElectricZapParticle[]>([]);
  const shockwavesRef = useRef<Shockwave[]>([]);"""

if old_refs in c:
    c = c.replace(old_refs, new_refs, 1)
    print("Updated lightningBoltsRef in InteractiveAltarPreview.")
else:
    print("Warning: old_refs not found!")

# Replace bolt generation in triggerStrike
old_bolt_gen = """      // Celestial lightning bolt from sky to anvil
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
      });"""

new_bolt_gen = """      // Celestial fractal lightning bolt from sky to anvil
      const bolt = createAdvancedLightningBolt(impactX, impactY, {
        viewH: ch,
        color: pal.glow,
        lightColor: pal.core,
        power: rating === 'PERFECT' ? 1.6 : 1.15,
        branchCount: rating === 'PERFECT' ? 4 : 2,
      });
      lightningBoltsRef.current.push(bolt);

      const zaps = createElectricZapParticles(impactX, impactY, rating === 'PERFECT' ? 20 : 12, pal.glow, 1.2);
      electricZapsRef.current.push(...zaps);"""

if old_bolt_gen in c:
    c = c.replace(old_bolt_gen, new_bolt_gen, 1)
    print("Updated bolt generation in triggerStrike.")
else:
    print("Warning: old_bolt_gen not found!")

# Replace bolt render in loop
old_bolt_render = """      // 8. Lightning Bolts
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
      }"""

new_bolt_render = """      // 8. Dynamic Advanced Lightning Bolts & Electric Zaps
      for (let i = lightningBoltsRef.current.length - 1; i >= 0; i--) {
        const bolt = lightningBoltsRef.current[i];
        bolt.age += dt;
        bolt.alpha -= bolt.decay * dt;
        if (bolt.alpha <= 0) {
          lightningBoltsRef.current.splice(i, 1);
          continue;
        }
        drawAdvancedLightningBolt(ctx, bolt, performance.now());
      }
      updateAndDrawElectricZaps(ctx, electricZapsRef.current, dt);"""

if old_bolt_render in c:
    c = c.replace(old_bolt_render, new_bolt_render, 1)
    print("Updated lightning rendering in InteractiveAltarPreview.")
else:
    print("Warning: old_bolt_render not found!")

with open('frontend/src/components/InteractiveAltarPreview.tsx', 'w', encoding='utf-8') as f:
    f.write(c)

print("Saved InteractiveAltarPreview.tsx successfully!")
