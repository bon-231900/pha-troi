import os

def patch_canvas():
    path = 'frontend/src/components/CommunityPanoramicForgeCanvas.tsx'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update executeHeroStrikeVisuals impact coords and do not reset rhythmPhase
    old_visuals = """      heroStrikeTimer = 0;
      screenShake = forceGolden ? 13 : 8;
      flashIntensity = forceGolden ? 1.4 : 0.95;
      rhythmPhase = 0.05;

      const isPortrait = viewW < viewH;
      let groundY = isPortrait ? viewH * 0.65 : (viewH < 500 ? viewH * 0.81 : viewH * 0.825);
      const renderScale = isPortrait ? Math.min(0.48, Math.max(0.36, viewW / 760)) : 0.38;
      const centerX = viewW * 0.5;
      const heroFootX = centerX - 14;
      const spriteLeft = heroFootX - (360 * renderScale) * 0.46;
      const spriteTop = groundY - (440 * renderScale);
      const impactX = spriteLeft + 213 * renderScale;
      const impactY = spriteTop + 342 * renderScale;"""

    new_visuals = """      heroStrikeTimer = 0;
      screenShake = forceGolden ? 14 : 8;
      flashIntensity = forceGolden ? 1.5 : 0.95;

      const isPortrait = viewW < viewH;
      let groundY = isPortrait ? viewH * 0.65 : (viewH < 500 ? viewH * 0.81 : viewH * 0.825);
      const renderScale = isPortrait ? Math.min(0.48, Math.max(0.36, viewW / 760)) : 0.38;
      const centerX = viewW * 0.5;
      const heroFootX = centerX - 14;
      const spriteLeft = heroFootX - (360 * renderScale) * 0.46;
      const spriteTop = groundY - (440 * renderScale);
      const impactX = heroFootX + 28 * renderScale;
      const impactY = groundY + 4;"""

    assert old_visuals in content, "Could not find old_visuals in canvas"
    content = content.replace(old_visuals, new_visuals, 1)

    # 2. Update handleInteraction to evaluate rhythm sweet spot
    old_interaction = """    if (gameStateRef.current === 'playing' || gameStateRef.current === 'title') {
      onHeroStrikeActionRef.current?.(false);
    }"""

    new_interaction = """    if (gameStateRef.current === 'playing' || gameStateRef.current === 'title') {
      const now = performance.now();
      const phase = (now % 600) / 600;
      const isSweetSpot = phase >= 0.85 || phase <= 0.10;
      onHeroStrikeActionRef.current?.(isSweetSpot);
    }"""

    assert old_interaction in content, "Could not find old_interaction in canvas"
    content = content.replace(old_interaction, new_interaction, 1)

    # 3. Update onKeyDown to evaluate rhythm sweet spot
    old_keydown = """        if (isSpace || isQ) {
          e.preventDefault();
          e.stopPropagation();
          onHeroStrikeActionRef.current?.(false);
        }"""

    new_keydown = """        if (isSpace || isQ) {
          e.preventDefault();
          e.stopPropagation();
          const now = performance.now();
          const phase = (now % 600) / 600;
          const isSweetSpot = phase >= 0.85 || phase <= 0.10;
          onHeroStrikeActionRef.current?.(isSweetSpot);
        }"""

    assert old_keydown in content, "Could not find old_keydown in canvas"
    content = content.replace(old_keydown, new_keydown, 1)

    # 4. Replace rhythm ring drawing with full Celestial Bagua Reticle
    old_ring = """          // Contracting Rhythm Ring (100 BPM) on Hero Anvil - Glowing Multi-Layer Qi Pulse
          const anvilImpactX = spriteLeft + 213 * renderScale;
          const anvilImpactY = spriteTop + 342 * renderScale;
          const ringScale = 1 - rhythmPhase;
          const isSweetSpot = Math.abs(rhythmPhase - 0.78) <= 0.18;

          ctx.save();
          ctx.shadowColor = isSweetSpot ? '#FFD700' : activeSectColor.glow;
          ctx.shadowBlur = isSweetSpot ? 14 : 7;
          ctx.strokeStyle = isSweetSpot ? '#FFF3B0' : activeSectColor.light;
          ctx.lineWidth = isSweetSpot ? 2.5 : 1.4;
          ctx.globalAlpha = 0.4 + rhythmPhase * 0.55;
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

          if (isSweetSpot) {
            ctx.strokeStyle = '#FFFFFF';
            ctx.lineWidth = 1.0;
            ctx.globalAlpha = 0.8;
            ctx.beginPath();
            ctx.ellipse(
              anvilImpactX,
              anvilImpactY,
              14 + ringScale * 38 * 0.96,
              5 + ringScale * 14 * 0.96,
              0,
              0,
              Math.PI * 2
            );
            ctx.stroke();
          }
          ctx.restore();"""

    new_ring = """          // ---------------------------------------------------------------------
          // CELESTIAL BAGUA RHYTHM RETICLE (TRẬN ĐỒ CANH NHỊP HOÀNG KIM 100 BPM)
          // ---------------------------------------------------------------------
          const beatPeriod = 600; // 100 BPM = 600ms per beat
          const currentBeatPhase = (now % beatPeriod) / beatPeriod;
          const isSweetSpot = currentBeatPhase >= 0.85 || currentBeatPhase <= 0.10;
          const isNearSweet = currentBeatPhase >= 0.70 && !isSweetSpot;

          const reticleX = heroFootX + 28 * renderScale;
          const reticleY = stageFootY + 6;
          const tilt = 0.44; // 2.5D Isometric platform perspective

          // Responsive spacious target ring (easily visible on all screen sizes)
          const targetRx = Math.round(isPortrait ? Math.max(42, viewW * 0.08) : Math.max(48, Math.min(62, viewW * 0.04)));
          const targetRy = Math.round(targetRx * tilt);

          // Contracting Approach Ring: shrinks from 2.8x down to 1.0x target radius
          const ringProgress = currentBeatPhase <= 0.10 ? 1.0 : currentBeatPhase;
          const approachScale = 1.0 + Math.max(0, 1.0 - ringProgress) * 1.9;
          const approachRx = targetRx * approachScale;
          const approachRy = approachRx * tilt;

          ctx.save();

          // 1. Dais Surface Ambient Qi Aura Pool
          const daisAura = ctx.createRadialGradient(
            reticleX, reticleY, 2,
            reticleX, reticleY, targetRx * 1.55
          );
          daisAura.addColorStop(0, isSweetSpot ? 'rgba(255, 215, 0, 0.45)' : `${activeSectColor.glow}30`);
          daisAura.addColorStop(0.55, isSweetSpot ? 'rgba(245, 158, 11, 0.22)' : `${activeSectColor.glow}12`);
          daisAura.addColorStop(1, 'rgba(0, 0, 0, 0)');
          ctx.fillStyle = daisAura;
          ctx.beginPath();
          ctx.ellipse(reticleX, reticleY, targetRx * 1.55, targetRy * 1.55, 0, 0, Math.PI * 2);
          ctx.fill();

          // 2. Stationary Target Ring (Vòng Trận Đích Cố Định)
          // High-contrast primary outer rim
          ctx.lineWidth = isSweetSpot ? 3.6 : 2.4;
          ctx.strokeStyle = isSweetSpot ? '#FFD700' : activeSectColor.light;
          ctx.shadowColor = isSweetSpot ? '#FFD700' : activeSectColor.glow;
          ctx.shadowBlur = isSweetSpot ? 20 : 8;
          ctx.beginPath();
          ctx.ellipse(reticleX, reticleY, targetRx, targetRy, 0, 0, Math.PI * 2);
          ctx.stroke();

          // Fine inner concentric guide
          ctx.lineWidth = 1.2;
          ctx.strokeStyle = isSweetSpot ? '#FFFFFF' : 'rgba(255, 255, 255, 0.45)';
          ctx.shadowBlur = isSweetSpot ? 8 : 0;
          ctx.beginPath();
          ctx.ellipse(reticleX, reticleY, targetRx * 0.82, targetRy * 0.82, 0, 0, Math.PI * 2);
          ctx.stroke();

          // 4 Sacred Cardinal Bagua Ticks (Càn, Khôn, Khảm, Ly)
          const tickAngles = [0, Math.PI * 0.5, Math.PI, Math.PI * 1.5];
          for (let i = 0; i < 4; i++) {
            const ang = tickAngles[i];
            const tx = reticleX + Math.cos(ang) * targetRx;
            const ty = reticleY + Math.sin(ang) * targetRy;

            ctx.fillStyle = isSweetSpot ? '#FFFDE7' : activeSectColor.light;
            ctx.shadowColor = isSweetSpot ? '#FFD700' : activeSectColor.glow;
            ctx.shadowBlur = isSweetSpot ? 14 : 4;

            const dSize = isSweetSpot ? 4.5 : 3.2;
            ctx.beginPath();
            ctx.moveTo(tx, ty - dSize * tilt);
            ctx.lineTo(tx + dSize, ty);
            ctx.lineTo(tx, ty + dSize * tilt);
            ctx.lineTo(tx - dSize, ty);
            ctx.closePath();
            ctx.fill();
          }

          // Center Focal Forge Core (Bát Quái Đích Điểm)
          ctx.fillStyle = isSweetSpot ? '#FFFFFF' : activeSectColor.light;
          ctx.shadowColor = isSweetSpot ? '#FFD700' : activeSectColor.glow;
          ctx.shadowBlur = isSweetSpot ? 16 : 4;
          ctx.beginPath();
          ctx.arc(reticleX, reticleY, isSweetSpot ? 4.0 : 2.5, 0, Math.PI * 2);
          ctx.fill();

          // 3. Contracting Approach Wave (Vòng Sóng Nhịp Co Dần)
          if (!isSweetSpot || currentBeatPhase >= 0.85) {
            const waveAlpha = Math.min(1.0, 0.4 + (1.0 - (approachScale - 1.0) / 1.9) * 0.6);
            ctx.globalAlpha = waveAlpha;

            const waveStroke = isSweetSpot
              ? '#FFFDE7'
              : isNearSweet
              ? '#F59E0B'
              : activeSectColor.light;
            const waveGlow = isSweetSpot
              ? '#FFD700'
              : isNearSweet
              ? '#F59E0B'
              : activeSectColor.glow;

            ctx.strokeStyle = waveStroke;
            ctx.shadowColor = waveGlow;
            ctx.shadowBlur = isSweetSpot ? 24 : isNearSweet ? 14 : 7;
            ctx.lineWidth = isSweetSpot ? 4.0 : isNearSweet ? 3.0 : 2.4;

            ctx.beginPath();
            ctx.ellipse(reticleX, reticleY, approachRx, approachRy, 0, 0, Math.PI * 2);
            ctx.stroke();

            // 4 Inward Guiding Beads on Approach Ring
            if (approachScale > 1.2) {
              ctx.fillStyle = waveStroke;
              ctx.shadowBlur = 8;
              for (let i = 0; i < 4; i++) {
                const ang = tickAngles[i];
                const cx = reticleX + Math.cos(ang) * approachRx;
                const cy = reticleY + Math.sin(ang) * approachRy;
                ctx.beginPath();
                ctx.arc(cx, cy, 3.0, 0, Math.PI * 2);
                ctx.fill();
              }
            }
          }

          // 4. Sweet Spot Resonance Flash & Floating Calligraphy (✧ HOÀNG KIM ✧)
          if (isSweetSpot) {
            ctx.globalAlpha = 0.95;
            ctx.strokeStyle = '#FFFFFF';
            ctx.lineWidth = 2.0;
            ctx.shadowColor = '#FFD700';
            ctx.shadowBlur = 18;
            ctx.beginPath();
            ctx.ellipse(reticleX, reticleY, targetRx * 1.03, targetRy * 1.03, 0, 0, Math.PI * 2);
            ctx.stroke();

            // Floating Golden Prompt
            ctx.font = 'bold 12px "Cinzel", "Noto Serif", sans-serif';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillStyle = '#FFFDE7';
            ctx.shadowColor = '#FFD700';
            ctx.shadowBlur = 16;
            ctx.fillText('✧ HOÀNG KIM ✧', reticleX, reticleY - targetRy - 15);
          }

          ctx.restore();"""

    assert old_ring in content, "Could not find old_ring in canvas"
    content = content.replace(old_ring, new_ring, 1)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched CommunityPanoramicForgeCanvas.tsx successfully!")

def patch_app():
    path = 'frontend/src/App.tsx'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    old_strike_logic = """      // Rhythm judgment: true skill timing or Overdrive burst (No more 45% RNG auto-crit!)
      const isGoldenHit = forceGolden || overdriveActive || (combo >= 5 && Math.random() < 0.15);
      const grade: JudgmentGrade = isGoldenHit ? 'PERFECT' : 'GREAT';"""

    new_strike_logic = """      // Rhythm judgment: 100 BPM (600ms per beat) skill timing or Overdrive burst
      const beatPeriod = 600; // ms
      const phase = (now % beatPeriod) / beatPeriod;
      const isRhythmSweetSpot = phase >= 0.85 || phase <= 0.10;

      const isGoldenHit = forceGolden || isRhythmSweetSpot || overdriveActive || (combo >= 5 && Math.random() < 0.10);
      const grade: JudgmentGrade = isGoldenHit ? 'PERFECT' : 'GREAT';"""

    assert old_strike_logic in content, "Could not find old_strike_logic in App.tsx"
    content = content.replace(old_strike_logic, new_strike_logic, 1)

    old_canvas_prop = """          onHeroStrikeAction={() => handleHeroStrike(false)}"""
    new_canvas_prop = """          onHeroStrikeAction={(isGolden) => handleHeroStrike(isGolden)}"""

    assert old_canvas_prop in content, "Could not find old_canvas_prop in App.tsx"
    content = content.replace(old_canvas_prop, new_canvas_prop, 1)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched App.tsx successfully!")

def patch_interactive_preview():
    path = 'frontend/src/components/InteractiveAltarPreview.tsx'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    old_strike = """    // Rhythm calculation: 100 BPM = 600ms period
    const now = performance.now();
    const beatPeriod = 600; // ms
    const phase = (now % beatPeriod) / beatPeriod;
    const sweetSpot = 0.78;
    const diff = Math.abs(phase - sweetSpot);

    let rating: 'PERFECT' | 'GREAT' | 'HIT' = 'HIT';
    let baseDamage = 350;
    let multiplier = 1.0;

    if (diff <= 0.10 || diff >= 0.90) {
      rating = 'PERFECT';
      multiplier = 2.8;
      baseDamage = 980;
    } else if (diff <= 0.22 || diff >= 0.78) {
      rating = 'GREAT';
      multiplier = 1.8;
      baseDamage = 620;
    } else {
      rating = 'HIT';
      multiplier = 1.1;
      baseDamage = 380;
    }"""

    new_strike = """    // Rhythm calculation: 100 BPM = 600ms period
    const now = performance.now();
    const beatPeriod = 600; // ms
    const phase = (now % beatPeriod) / beatPeriod;
    const isSweetSpot = phase >= 0.85 || phase <= 0.10;
    const isGreat = (phase >= 0.72 && phase < 0.85) || (phase > 0.10 && phase <= 0.22);

    let rating: 'PERFECT' | 'GREAT' | 'HIT' = 'HIT';
    let baseDamage = 350;
    let multiplier = 1.0;

    if (isSweetSpot) {
      rating = 'PERFECT';
      multiplier = 2.8;
      baseDamage = 980;
    } else if (isGreat) {
      rating = 'GREAT';
      multiplier = 1.8;
      baseDamage = 620;
    } else {
      rating = 'HIT';
      multiplier = 1.1;
      baseDamage = 380;
    }"""

    assert old_strike in content, "Could not find old_strike in InteractiveAltarPreview.tsx"
    content = content.replace(old_strike, new_strike, 1)

    old_ring = """      // 6. Contracting 100 BPM Rhythm Ring on Anvil
      const anvilImpactX = spriteLeft + 213 * renderScale;
      const anvilImpactY = spriteTop + 342 * renderScale;

      const beatPeriod = 600; // 100 BPM = 600ms
      const rhythmPhase = (now % beatPeriod) / beatPeriod;
      const ringScale = 1.0 - rhythmPhase;
      const isSweetSpot = Math.abs(rhythmPhase - 0.78) <= 0.12;

      ctx.save();
      ctx.strokeStyle = isSweetSpot ? '#FFD166' : pal.glow;
      ctx.lineWidth = isSweetSpot ? 2.8 : 1.4;
      ctx.shadowColor = isSweetSpot ? '#FFD166' : pal.glow;
      ctx.shadowBlur = isSweetSpot ? 12 : 5;
      ctx.globalAlpha = 0.4 + rhythmPhase * 0.55;

      ctx.beginPath();
      ctx.ellipse(
        anvilImpactX,
        anvilImpactY,
        12 + ringScale * 38,
        5 + ringScale * 14,
        0,
        0,
        Math.PI * 2
      );
      ctx.stroke();

      // Static target ring on anvil
      ctx.strokeStyle = '#FFFFFF';
      ctx.lineWidth = 1.0;
      ctx.globalAlpha = 0.5;
      ctx.beginPath();
      ctx.ellipse(anvilImpactX, anvilImpactY, 13, 5.5, 0, 0, Math.PI * 2);
      ctx.stroke();
      ctx.restore();"""

    new_ring = """      // 6. Celestial Bagua Rhythm Reticle (100 BPM)
      const beatPeriod = 600;
      const currentBeatPhase = (now % beatPeriod) / beatPeriod;
      const isSweetSpot = currentBeatPhase >= 0.85 || currentBeatPhase <= 0.10;
      const isNearSweet = currentBeatPhase >= 0.70 && !isSweetSpot;

      const reticleX = cw * 0.5 + 16;
      const reticleY = stageFootY + 4;
      const tilt = 0.44;

      const targetRx = Math.round(Math.max(40, cw * 0.10));
      const targetRy = Math.round(targetRx * tilt);

      const ringProgress = currentBeatPhase <= 0.10 ? 1.0 : currentBeatPhase;
      const approachScale = 1.0 + Math.max(0, 1.0 - ringProgress) * 1.9;
      const approachRx = targetRx * approachScale;
      const approachRy = approachRx * tilt;

      ctx.save();

      // Aura Pool
      const daisAura = ctx.createRadialGradient(
        reticleX, reticleY, 2,
        reticleX, reticleY, targetRx * 1.55
      );
      daisAura.addColorStop(0, isSweetSpot ? 'rgba(255, 215, 0, 0.45)' : `${pal.glow}30`);
      daisAura.addColorStop(0.55, isSweetSpot ? 'rgba(245, 158, 11, 0.22)' : `${pal.glow}12`);
      daisAura.addColorStop(1, 'rgba(0, 0, 0, 0)');
      ctx.fillStyle = daisAura;
      ctx.beginPath();
      ctx.ellipse(reticleX, reticleY, targetRx * 1.55, targetRy * 1.55, 0, 0, Math.PI * 2);
      ctx.fill();

      // Stationary Target Ring
      ctx.lineWidth = isSweetSpot ? 3.6 : 2.4;
      ctx.strokeStyle = isSweetSpot ? '#FFD700' : pal.glow;
      ctx.shadowColor = isSweetSpot ? '#FFD700' : pal.glow;
      ctx.shadowBlur = isSweetSpot ? 20 : 8;
      ctx.beginPath();
      ctx.ellipse(reticleX, reticleY, targetRx, targetRy, 0, 0, Math.PI * 2);
      ctx.stroke();

      ctx.lineWidth = 1.2;
      ctx.strokeStyle = isSweetSpot ? '#FFFFFF' : 'rgba(255, 255, 255, 0.45)';
      ctx.shadowBlur = isSweetSpot ? 8 : 0;
      ctx.beginPath();
      ctx.ellipse(reticleX, reticleY, targetRx * 0.82, targetRy * 0.82, 0, 0, Math.PI * 2);
      ctx.stroke();

      // 4 Cardinal Bagua Ticks
      const tickAngles = [0, Math.PI * 0.5, Math.PI, Math.PI * 1.5];
      for (let i = 0; i < 4; i++) {
        const ang = tickAngles[i];
        const tx = reticleX + Math.cos(ang) * targetRx;
        const ty = reticleY + Math.sin(ang) * targetRy;

        ctx.fillStyle = isSweetSpot ? '#FFFDE7' : pal.glow;
        ctx.shadowColor = isSweetSpot ? '#FFD700' : pal.glow;
        ctx.shadowBlur = isSweetSpot ? 14 : 4;

        const dSize = isSweetSpot ? 4.5 : 3.2;
        ctx.beginPath();
        ctx.moveTo(tx, ty - dSize * tilt);
        ctx.lineTo(tx + dSize, ty);
        ctx.lineTo(tx, ty + dSize * tilt);
        ctx.lineTo(tx - dSize, ty);
        ctx.closePath();
        ctx.fill();
      }

      // Center Focal Core
      ctx.fillStyle = isSweetSpot ? '#FFFFFF' : pal.glow;
      ctx.shadowColor = isSweetSpot ? '#FFD700' : pal.glow;
      ctx.shadowBlur = isSweetSpot ? 16 : 4;
      ctx.beginPath();
      ctx.arc(reticleX, reticleY, isSweetSpot ? 4.0 : 2.5, 0, Math.PI * 2);
      ctx.fill();

      // Contracting Approach Wave
      if (!isSweetSpot || currentBeatPhase >= 0.85) {
        const waveAlpha = Math.min(1.0, 0.4 + (1.0 - (approachScale - 1.0) / 1.9) * 0.6);
        ctx.globalAlpha = waveAlpha;

        const waveStroke = isSweetSpot
          ? '#FFFDE7'
          : isNearSweet
          ? '#F59E0B'
          : pal.glow;
        const waveGlow = isSweetSpot
          ? '#FFD700'
          : isNearSweet
          ? '#F59E0B'
          : pal.glow;

        ctx.strokeStyle = waveStroke;
        ctx.shadowColor = waveGlow;
        ctx.shadowBlur = isSweetSpot ? 24 : isNearSweet ? 14 : 7;
        ctx.lineWidth = isSweetSpot ? 4.0 : isNearSweet ? 3.0 : 2.4;

        ctx.beginPath();
        ctx.ellipse(reticleX, reticleY, approachRx, approachRy, 0, 0, Math.PI * 2);
        ctx.stroke();
      }

      // Sweet Spot Resonance Flash & Floating Calligraphy
      if (isSweetSpot) {
        ctx.globalAlpha = 0.95;
        ctx.strokeStyle = '#FFFFFF';
        ctx.lineWidth = 2.0;
        ctx.shadowColor = '#FFD700';
        ctx.shadowBlur = 18;
        ctx.beginPath();
        ctx.ellipse(reticleX, reticleY, targetRx * 1.03, targetRy * 1.03, 0, 0, Math.PI * 2);
        ctx.stroke();

        ctx.font = 'bold 12px "Cinzel", "Noto Serif", sans-serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillStyle = '#FFFDE7';
        ctx.shadowColor = '#FFD700';
        ctx.shadowBlur = 16;
        ctx.fillText('✧ HOÀNG KIM ✧', reticleX, reticleY - targetRy - 15);
      }

      ctx.restore();"""

    assert old_ring in content, "Could not find old_ring in InteractiveAltarPreview.tsx"
    content = content.replace(old_ring, new_ring, 1)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched InteractiveAltarPreview.tsx successfully!")

if __name__ == '__main__':
    patch_canvas()
    patch_app()
    patch_interactive_preview()
