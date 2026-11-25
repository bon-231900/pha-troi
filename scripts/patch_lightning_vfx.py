# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# 1. Update CommunityPanoramicForgeCanvas.tsx
with open('frontend/src/components/CommunityPanoramicForgeCanvas.tsx', 'r', encoding='utf-8') as f:
    c = f.read()

# Add imports from lightningVFX
old_imports = """import {
  PANORAMA_SKY_RATIO,
  HERO_STRIKE_TOTAL_SEC,
  SCREEN_SHAKE_DURATION_SEC,
  HERO_STANCE_PALETTES,
  type StanceKey,
  type Point2D,
} from '../game/rules';"""

new_imports = """import {
  PANORAMA_SKY_RATIO,
  HERO_STRIKE_TOTAL_SEC,
  SCREEN_SHAKE_DURATION_SEC,
  HERO_STANCE_PALETTES,
  type StanceKey,
  type Point2D,
} from '../game/rules';
import {
  type AdvancedLightningBolt,
  type ElectricZapParticle,
  createAdvancedLightningBolt,
  drawAdvancedLightningBolt,
  createElectricZapParticles,
  updateAndDrawElectricZaps,
  drawSkyLightningFlash,
} from '../game/lightningVFX';"""

if old_imports in c:
    c = c.replace(old_imports, new_imports, 1)
    print("Added lightningVFX imports.")
else:
    print("Warning: old_imports not found!")

# Add triggerThunderStorm to handle interface
old_handle = """export interface CommunityPanoramicForgeCanvasHandle {
  triggerHeroStrike: (forceGolden?: boolean) => void;
  triggerPeerWave: () => void;"""

new_handle = """export interface CommunityPanoramicForgeCanvasHandle {
  triggerHeroStrike: (forceGolden?: boolean) => void;
  triggerThunderStorm: (count?: number, power?: number) => void;
  triggerPeerWave: () => void;"""

if old_handle in c:
    c = c.replace(old_handle, new_handle, 1)
    print("Updated CommunityPanoramicForgeCanvasHandle interface.")
else:
    print("Warning: old_handle not found!")

# Add closure ref
old_closure = """  const spawnTouchRippleClosureRef = useRef<((x: number, y: number) => void) | null>(null);
  const lastTouchTimeRef = useRef<number>(0);

  useImperativeHandle(
    ref,
    () => ({
      triggerHeroStrike: (forceGolden = false) => {
        executeHeroStrikeClosureRef.current?.(forceGolden);
      },
      triggerPeerWave: () => {"""

new_closure = """  const spawnTouchRippleClosureRef = useRef<((x: number, y: number) => void) | null>(null);
  const triggerThunderStormClosureRef = useRef<((count?: number, power?: number) => void) | null>(null);
  const lastTouchTimeRef = useRef<number>(0);

  useImperativeHandle(
    ref,
    () => ({
      triggerHeroStrike: (forceGolden = false) => {
        executeHeroStrikeClosureRef.current?.(forceGolden);
      },
      triggerThunderStorm: (count = 6, power = 2.0) => {
        triggerThunderStormClosureRef.current?.(count, power);
      },
      triggerPeerWave: () => {"""

if old_closure in c:
    c = c.replace(old_closure, new_closure, 1)
    print("Updated imperative handle & closure ref.")
else:
    print("Warning: old_closure not found!")

# Replace ActiveLightningBolt2D interface with comment
old_bolt_interface = """interface ActiveLightningBolt2D {
  segments: Point2D[];
  alpha: number;
  decay: number;
  color: string;
  lineWidth: number;
}"""

if old_bolt_interface in c:
    c = c.replace(old_bolt_interface, "// ActiveLightningBolt2D superseded by AdvancedLightningBolt in lightningVFX.ts", 1)
    print("Replaced ActiveLightningBolt2D interface.")
else:
    print("Warning: old_bolt_interface not found!")

# Update state variables in canvas effect
old_bolt_var = "    const lightningBolts: ActiveLightningBolt2D[] = [];"
new_bolt_var = """    const lightningBolts: AdvancedLightningBolt[] = [];
    const electricZaps: ElectricZapParticle[] = [];"""

if old_bolt_var in c:
    c = c.replace(old_bolt_var, new_bolt_var, 1)
    print("Updated lightningBolts & electricZaps variables.")
else:
    print("Warning: old_bolt_var not found!")

# Replace spawnLightningBolt function
old_spawn_fn = """    const spawnLightningBolt = (targetX: number, targetY: number, color = '#00F0FF', power = 1.0) => {
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
    };"""

new_spawn_fn = """    const spawnLightningBolt = (
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

if old_spawn_fn in c:
    c = c.replace(old_spawn_fn, new_spawn_fn, 1)
    print("Replaced spawnLightningBolt with fractal generator.")
else:
    print("Warning: old_spawn_fn not found!")

# Replace executeHeroStrikeVisuals
old_strike_fn = """    const executeHeroStrikeVisuals = (isCrit = false) => {
      const currentStanceKey = activeStanceRef.current;
      const sect = STANCE_TO_SECT[currentStanceKey] || 'thunder';
      const sc = SECT_COLORS[sect] || SECT_COLORS.thunder;

      heroStrikeTimer = 0;
      screenShake = isCrit ? 13 : 7;
      flashIntensity = isCrit ? 1.3 : 0.85;

      const isPortrait = viewW < viewH;
      let groundY = isPortrait ? viewH * 0.65 : (viewH < 500 ? viewH * 0.81 : viewH * 0.825);
      const renderScale = isPortrait ? Math.min(0.48, Math.max(0.36, viewW / 760)) : 0.38;
      const centerX = viewW * 0.5;
      const heroFootX = centerX - 14;
      const spriteLeft = heroFootX - (360 * renderScale) * 0.46;
      const spriteTop = groundY - (440 * renderScale);
      const impactX = heroFootX + 28 * renderScale;
      const impactY = groundY + 4;

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
      const sparkCount = isCrit ? 44 : 24;
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
    };"""

new_strike_fn = """    const executeHeroStrikeVisuals = (isCrit = false) => {
      const currentStanceKey = activeStanceRef.current;
      const sect = STANCE_TO_SECT[currentStanceKey] || 'thunder';
      const sc = SECT_COLORS[sect] || SECT_COLORS.thunder;

      heroStrikeTimer = 0;
      screenShake = isCrit ? 16 : 8;
      flashIntensity = isCrit ? 1.6 : 0.95;

      const isPortrait = viewW < viewH;
      let groundY = isPortrait ? viewH * 0.65 : (viewH < 500 ? viewH * 0.81 : viewH * 0.825);
      const renderScale = isPortrait ? Math.min(0.48, Math.max(0.36, viewW / 760)) : 0.38;
      const centerX = viewW * 0.5;
      const heroFootX = centerX - 14;
      const impactX = heroFootX + 28 * renderScale;
      const impactY = groundY + 4;

      // 1. Primary High-Definition Multi-Pass Lightning Bolt
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
      electricZaps.push(...newZaps);

      // 5. Molten Sparks
      const sparkCount = isCrit ? 44 : 24;
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
    };"""

if old_strike_fn in c:
    c = c.replace(old_strike_fn, new_strike_fn, 1)
    print("Replaced executeHeroStrikeVisuals.")
else:
    print("Warning: old_strike_fn not found!")

# Add triggerThunderStormClosureRef implementation
old_reset_fn = """    const resetSimulation = () => {
      heroStrikeTimer = -1;
      screenShake = 0;
      flashIntensity = 0;
      lightningBolts.length = 0;
      shockwaves.length = 0;
      floatingTexts.length = 0;
      for (const p of sparkPool) p.active = false;
    };"""

new_reset_fn = """    const resetSimulation = () => {
      heroStrikeTimer = -1;
      screenShake = 0;
      flashIntensity = 0;
      lightningBolts.length = 0;
      electricZaps.length = 0;
      shockwaves.length = 0;
      floatingTexts.length = 0;
      for (const p of sparkPool) p.active = false;
    };

    triggerThunderStormClosureRef.current = (count = 6, power = 2.0) => {
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

if old_reset_fn in c:
    c = c.replace(old_reset_fn, new_reset_fn, 1)
    print("Added triggerThunderStormClosureRef & updated reset.")
else:
    print("Warning: old_reset_fn not found!")

# Update lightningBolts decay in update loop
old_decay_loop = """          // Lightning bolts decay
          for (let i = lightningBolts.length - 1; i >= 0; i--) {
            const bolt = lightningBolts[i];
            bolt.alpha -= bolt.decay * dt;
            if (bolt.alpha <= 0) {
              lightningBolts.splice(i, 1);
            }
          }"""

new_decay_loop = """          // Lightning bolts decay
          for (let i = lightningBolts.length - 1; i >= 0; i--) {
            const bolt = lightningBolts[i];
            bolt.age += dt;
            bolt.alpha -= bolt.decay * dt;
            if (bolt.alpha <= 0) {
              lightningBolts.splice(i, 1);
            }
          }"""

if old_decay_loop in c:
    c = c.replace(old_decay_loop, new_decay_loop, 1)
    print("Updated bolt age & decay in loop.")
else:
    print("Warning: old_decay_loop not found!")

# Replace LAYER 12 Rendering
old_layer12 = """        // ---------------------------------------------------------------------
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
        }"""

new_layer12 = """        // ---------------------------------------------------------------------
        // LAYER 12: DYNAMIC ADVANCED LIGHTNING BOLTS & ELECTRIC ZAPS
        // ---------------------------------------------------------------------
        // Atmospheric Sky Lightning Flash (Illuminates sky, moon & clouds)
        if (lightningBolts.length > 0 && flashIntensity > 0.05) {
          const mainBolt = lightningBolts[lightningBolts.length - 1];
          drawSkyLightningFlash(ctx, viewW, viewH, mainBolt.impactX, mainBolt.color, flashIntensity);
        }

        // Multi-Pass Shader Lightning Rendering (Additive Blending)
        for (let i = 0; i < lightningBolts.length; i++) {
          drawAdvancedLightningBolt(ctx, lightningBolts[i], now);
        }

        // Electric Zap Streak Particles (High Voltage Ionization)
        updateAndDrawElectricZaps(ctx, electricZaps, dt);"""

if old_layer12 in c:
    c = c.replace(old_layer12, new_layer12, 1)
    print("Replaced LAYER 12 with multi-pass shader lightning rendering.")
else:
    print("Warning: old_layer12 not found!")

# Enhance LAYER 13 Shockwaves
old_layer13 = """        for (let i = shockwaves.length - 1; i >= 0; i--) {
          const sw = shockwaves[i];
          ctx.save();
          ctx.globalAlpha = Math.max(0, sw.alpha);
          ctx.strokeStyle = sw.color;
          ctx.lineWidth = 2.4 * sw.alpha;
          ctx.beginPath();
          ctx.ellipse(sw.x, sw.y, sw.radius, sw.radius * 0.45, 0, 0, Math.PI * 2);
          ctx.stroke();
          ctx.restore();
        }"""

new_layer13 = """        for (let i = shockwaves.length - 1; i >= 0; i--) {
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

if old_layer13 in c:
    c = c.replace(old_layer13, new_layer13, 1)
    print("Enhanced LAYER 13 shockwaves with dual-ring lighter glow.")
else:
    print("Warning: old_layer13 not found!")

with open('frontend/src/components/CommunityPanoramicForgeCanvas.tsx', 'w', encoding='utf-8') as f:
    f.write(c)

print("Saved CommunityPanoramicForgeCanvas.tsx successfully!")

# 2. Update App.tsx for Thunder Skills
with open('frontend/src/App.tsx', 'r', encoding='utf-8') as f:
    app = f.read()

# Trigger Thunder Storm on Thunder E (Bão Plasma Cuồng Kích)
old_thunder_e = """        if (cls.id === 'thunder') {
          soundEngine.playGlobalBurstFanfare();
          const dmg = Math.round(basePower * 6 + combo * 25);
          setBossHp((hp) => Math.max(0, hp - dmg));
          setPlayerTotalDamage((prev) => prev + dmg);
          canvasHandleRef.current?.spawnCombatText('🌩️ BÃO PLASMA CUỒNG KÍCH!', `8 LUỒNG SÉT -${dmg} DMG`, '#00F0FF', '#FFD700', true);
          appendCombatLog(`🌩️ [BÃO PLASMA CUỒNG KÍCH] Xả 8 luồng sét giáng -${dmg} DMG vào Bầu Trời!`, 'gold');"""

new_thunder_e = """        if (cls.id === 'thunder') {
          soundEngine.playGlobalBurstFanfare();
          const dmg = Math.round(basePower * 6 + combo * 25);
          setBossHp((hp) => Math.max(0, hp - dmg));
          setPlayerTotalDamage((prev) => prev + dmg);
          canvasHandleRef.current?.triggerThunderStorm(8, 2.0);
          canvasHandleRef.current?.spawnCombatText('🌩️ BÃO PLASMA CUỒNG KÍCH!', `8 LUỒNG SÉT -${dmg} DMG`, '#00F0FF', '#FFD700', true);
          appendCombatLog(`🌩️ [BÃO PLASMA CUỒNG KÍCH] Xả 8 luồng sét giáng -${dmg} DMG vào Bầu Trời!`, 'gold');"""

if old_thunder_e in app:
    app = app.replace(old_thunder_e, new_thunder_e, 1)
    print("Hooked Thunder E into triggerThunderStorm.")
else:
    print("Warning: old_thunder_e not found!")

# Trigger Thunder Storm on Thunder R (Thiên Lôi Giáng Thế)
old_thunder_r = """        if (cls.id === 'thunder') {
          soundEngine.playGlobalBurstFanfare();
          const ultDmg = Math.round(basePower * 16);
          setBossHp((hp) => Math.max(0, hp - ultDmg));
          setPlayerTotalDamage((prev) => prev + ultDmg);
          canvasHandleRef.current?.spawnCombatText('👑 THIÊN LÔI GIÁNG THẾ!', `CỘT LÔI TỐI THƯỢNG -${ultDmg} DMG`, '#00F0FF', '#FFD700', true);
          appendCombatLog(`👑 [THIÊN LÔI GIÁNG THẾ] Đại chiêu thức thứ 4! Triệu hồi cột lôi xé toạc Mái Vòm -${ultDmg} DMG (khuếch đại x2.2 Raid)!`, 'gold');"""

new_thunder_r = """        if (cls.id === 'thunder') {
          soundEngine.playGlobalBurstFanfare();
          const ultDmg = Math.round(basePower * 16);
          setBossHp((hp) => Math.max(0, hp - ultDmg));
          setPlayerTotalDamage((prev) => prev + ultDmg);
          canvasHandleRef.current?.triggerThunderStorm(14, 2.8);
          canvasHandleRef.current?.spawnCombatText('👑 THIÊN LÔI GIÁNG THẾ!', `CỘT LÔI TỐI THƯỢNG -${ultDmg} DMG`, '#00F0FF', '#FFD700', true);
          appendCombatLog(`👑 [THIÊN LÔI GIÁNG THẾ] Đại chiêu thức thứ 4! Triệu hồi cột lôi xé toạc Mái Vòm -${ultDmg} DMG (khuếch đại x2.2 Raid)!`, 'gold');"""

if old_thunder_r in app:
    app = app.replace(old_thunder_r, new_thunder_r, 1)
    print("Hooked Thunder R into triggerThunderStorm.")
else:
    print("Warning: old_thunder_r not found!")

# Trigger mini lightning burst on Thunder W (Lôi Quang Bộ)
old_thunder_w = """        if (cls.id === 'thunder') {
          soundEngine.playGlobalBurstFanfare();
          canvasHandleRef.current?.spawnCombatText('⚡ LÔI QUANG BỘ!', 'BẢO TOÀN COMBO & XUYÊN GIÁP +20%', '#00F0FF', '#FFFFFF', true);
          appendCombatLog('⚡ [LÔI QUANG BỘ] Thân pháp hóa lôi điện! Bảo toàn combo và tăng 20% xuyên giáp trong 6 giây!', 'cyan');"""

new_thunder_w = """        if (cls.id === 'thunder') {
          soundEngine.playGlobalBurstFanfare();
          canvasHandleRef.current?.triggerThunderStorm(4, 1.4);
          canvasHandleRef.current?.spawnCombatText('⚡ LÔI QUANG BỘ!', 'BẢO TOÀN COMBO & XUYÊN GIÁP +20%', '#00F0FF', '#FFFFFF', true);
          appendCombatLog('⚡ [LÔI QUANG BỘ] Thân pháp hóa lôi điện! Bảo toàn combo và tăng 20% xuyên giáp trong 6 giây!', 'cyan');"""

if old_thunder_w in app:
    app = app.replace(old_thunder_w, new_thunder_w, 1)
    print("Hooked Thunder W into triggerThunderStorm.")
else:
    print("Warning: old_thunder_w not found!")

with open('frontend/src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(app)

print("Saved App.tsx successfully!")
print("Lightning graphics patch applied completely!")
