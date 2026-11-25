import os

def patch_canvas():
    path = 'frontend/src/components/CommunityPanoramicForgeCanvas.tsx'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update executeHeroStrikeVisuals to accept isCrit
    old_exec = """    const executeHeroStrikeVisuals = (forceGolden = false) => {
      const currentStanceKey = activeStanceRef.current;
      const sect = STANCE_TO_SECT[currentStanceKey] || 'thunder';
      const sc = SECT_COLORS[sect] || SECT_COLORS.thunder;

      heroStrikeTimer = 0;
      screenShake = forceGolden ? 14 : 8;
      flashIntensity = forceGolden ? 1.5 : 0.95;"""

    new_exec = """    const executeHeroStrikeVisuals = (isCrit = false) => {
      const currentStanceKey = activeStanceRef.current;
      const sect = STANCE_TO_SECT[currentStanceKey] || 'thunder';
      const sc = SECT_COLORS[sect] || SECT_COLORS.thunder;

      heroStrikeTimer = 0;
      screenShake = isCrit ? 13 : 7;
      flashIntensity = isCrit ? 1.3 : 0.85;"""

    assert old_exec in content, "Could not find old_exec in canvas"
    content = content.replace(old_exec, new_exec, 1)

    # 2. Update spawnCombatNumberInternal: only show ⚡ BẠO KÍCH when isCrit, no more ★ HOÀNG KIM
    old_spawn = """      let badgeText: string | undefined = undefined;
      if (isGolden) {
        badgeText = `★ HOÀNG KIM x${multiplier}`;
      } else if (isCrit) {
        badgeText = `⚡ BẠO KÍCH x${multiplier}`;
      } else if (isGlance) {
        badgeText = 'DỘI BÚA';
      }"""

    new_spawn = """      let badgeText: string | undefined = undefined;
      if (isCrit) {
        badgeText = `⚡ BẠO KÍCH x${multiplier}`;
      } else if (isGlance) {
        badgeText = 'DỘI BÚA';
      }"""

    assert old_spawn in content, "Could not find old_spawn in canvas"
    content = content.replace(old_spawn, new_spawn, 1)

    # Update color / scale
    content = content.replace("const scale = isGolden ? 1.35 : isCrit ? 1.22 : isGlance ? 0.92 : 1.05;", "const scale = isCrit ? 1.30 : isGlance ? 0.92 : 1.05;")
    content = content.replace("const color = isGlance ? '#F87171' : isGolden ? '#FFD700' : isCrit ? '#38BDF8' : '#F8FAFC';", "const color = isGlance ? '#F87171' : isCrit ? '#FFD700' : '#F8FAFC';")
    content = content.replace("const glowColor = isGlance ? '#EF4444' : isGolden ? '#F59E0B' : isCrit ? '#00F0FF' : 'rgba(255, 255, 255, 0.4)';", "const glowColor = isGlance ? '#EF4444' : isCrit ? '#F59E0B' : 'rgba(255, 255, 255, 0.4)';")

    # 3. Clean handleInteraction & onKeyDown
    old_interact = """    if (gameStateRef.current === 'playing' || gameStateRef.current === 'title') {
      const now = performance.now();
      const phase = (now % 600) / 600;
      const isSweetSpot = phase >= 0.85 || phase <= 0.10;
      onHeroStrikeActionRef.current?.(isSweetSpot);
    }"""
    new_interact = """    if (gameStateRef.current === 'playing' || gameStateRef.current === 'title') {
      onHeroStrikeActionRef.current?.(false);
    }"""
    assert old_interact in content, "Could not find old_interact in canvas"
    content = content.replace(old_interact, new_interact, 1)

    old_kdown = """        if (isSpace || isQ) {
          e.preventDefault();
          e.stopPropagation();
          const now = performance.now();
          const phase = (now % 600) / 600;
          const isSweetSpot = phase >= 0.85 || phase <= 0.10;
          onHeroStrikeActionRef.current?.(isSweetSpot);
        }"""
    new_kdown = """        if (isSpace || isQ) {
          e.preventDefault();
          e.stopPropagation();
          onHeroStrikeActionRef.current?.(false);
        }"""
    assert old_kdown in content, "Could not find old_kdown in canvas"
    content = content.replace(old_kdown, new_kdown, 1)

    # 4. Remove the Celestial Bagua Rhythm Reticle entirely!
    reticle_start = "          // ---------------------------------------------------------------------\n          // CELESTIAL BAGUA RHYTHM RETICLE (TRẬN ĐỒ CANH NHỊP HOÀNG KIM 100 BPM)"
    reticle_end = "          ctx.restore();\n\n          // Balanced Overhead Plaque (Charm / Caveat Calligraphy)"

    start_idx = content.find(reticle_start)
    end_idx = content.find(reticle_end)
    assert start_idx != -1 and end_idx != -1, f"Could not find reticle block ({start_idx}, {end_idx})"

    content = content[:start_idx] + "          // Hero Dais Surface is completely clean and unobstructed (No rhythm clutter)\n" + content[end_idx + len("          ctx.restore();\n\n"):]

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched CommunityPanoramicForgeCanvas.tsx successfully!")

def patch_app():
    path = 'frontend/src/App.tsx'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update handleHeroStrike
    old_strike = """      // Rhythm judgment: 100 BPM (600ms per beat) skill timing or Overdrive burst
      const beatPeriod = 600; // ms
      const phase = (now % beatPeriod) / beatPeriod;
      const isRhythmSweetSpot = phase >= 0.85 || phase <= 0.10;

      const isGoldenHit = forceGolden || isRhythmSweetSpot || overdriveActive || (combo >= 5 && Math.random() < 0.10);
      const grade: JudgmentGrade = isGoldenHit ? 'PERFECT' : 'GREAT';"""

    new_strike = """      // Pure Action RPG Strike (Driven by Equipment, Stats, Crit Rate & Overdrive)
      const grade: JudgmentGrade = 'GREAT';"""

    assert old_strike in content, "Could not find old_strike in App.tsx"
    content = content.replace(old_strike, new_strike, 1)

    # 2. Update visuals & combat number triggers
    old_triggers = """      // 1. Trigger Panoramic Canvas 2D Strike Visuals
      canvasHandleRef.current?.triggerHeroStrike(isGoldenHit);

      // 2. Spawn Floating Text in Canvas (Pure Integer RPG numbers: -1 DMG, -3 DMG, -12 DMG)
      const stanceData = HAMMER_STANCES[activeStance];
      const isCritHit = outcome.isCrit;
      const isGlancingHit = outcome.isGlancingHit;

      // Dynamic, juicy combat damage fountain (replaces clunky 2-line text blocks)
      canvasHandleRef.current?.spawnCombatNumber(
        outcome.damage,
        grade,
        outcome.displayMultiplier,
        !!isCritHit,
        isGoldenHit,
        activeStance
      );

      // 3. Audio & Haptics
      soundEngine.playAnvilStrike(
        grade,
        activeStance,
        combo >= 5 || overdriveActive
      );
      hapticEngine.playStrike(outcome.isCrit, isGoldenHit);

      // 4. Update Anvil Heat (Hỏa Hầu)
      setAnvilHeat((prev) => Math.min(MAX_ANVIL_HEAT, prev + outcome.heatGain));

      // 4B. Stance W (Viêm Dương): Burn Stacks Application
      if (activeStance === 'W') {
        const addedBurn = isGoldenHit ? 2 : 1;
        setBurnStacks((prev) => Math.min(80, prev + addedBurn));
      }"""

    new_triggers = """      const isCritHit = !!outcome.isCrit;
      const isOverdriveNow = overdriveActive || outcome.triggeredOverdrive;

      // 1. Trigger Panoramic Canvas 2D Strike Visuals
      canvasHandleRef.current?.triggerHeroStrike(isCritHit);

      // 2. Spawn Floating Text in Canvas (Pure Integer RPG numbers)
      const stanceData = HAMMER_STANCES[activeStance];
      const isGlancingHit = outcome.isGlancingHit;

      // Dynamic, juicy combat damage fountain
      canvasHandleRef.current?.spawnCombatNumber(
        outcome.damage,
        isCritHit ? 'PERFECT' : 'GREAT',
        outcome.displayMultiplier,
        isCritHit,
        false,
        activeStance
      );

      // 3. Audio & Haptics
      soundEngine.playAnvilStrike(
        isCritHit ? 'PERFECT' : 'GREAT',
        activeStance,
        isCritHit || isOverdriveNow
      );
      hapticEngine.playStrike(isCritHit, isOverdriveNow);

      // 4. Update Anvil Heat (Hỏa Hầu)
      setAnvilHeat((prev) => Math.min(MAX_ANVIL_HEAT, prev + outcome.heatGain));

      // 4B. Stance W (Viêm Dương): Burn Stacks Application
      if (activeStance === 'W') {
        const addedBurn = isCritHit ? 2 : 1;
        setBurnStacks((prev) => Math.min(80, prev + addedBurn));
      }"""

    assert old_triggers in content, "Could not find old_triggers in App.tsx"
    content = content.replace(old_triggers, new_triggers, 1)

    # 3. Clean combat logs in App.tsx
    content = content.replace("isGoldenHit,", "false,")
    content = content.replace("if (isGoldenHit) {", "if (isCritHit) {")
    content = content.replace("Chuỗi 15 Hoàng Kim liên tiếp! Thiên lôi giáng -500 DMG xuyên giáp trời!", "Chuỗi Bạo Kích 15 đòn liên tiếp! Thiên lôi giáng -500 DMG xuyên giáp trời!")
    content = content.replace("Nhát búa Hoàng Kim ngưng tụ +${th} Tinh Hoa Thần Hồn!", "Đòn Bạo Kích ngưng tụ +${th} Tinh Hoa Thần Hồn!")
    content = content.replace("labelVn: isCritHit ? 'BẠO KÍCH' : isGoldenHit ? 'HOÀNG KIM' : 'CHUẨN XÁC',", "labelVn: isCritHit ? 'BẠO KÍCH' : isOverdriveNow ? 'BẠO PHÁT' : 'CHUẨN XÁC',")
    content = content.replace("} else if (isGoldenHit) {", "} else if (isCritHit) {")
    content = content.replace("`Nhịp Hoàng Kim [${activeStance}]! Giáng -${outcome.damage} DMG (+${outcome.linhThachEarned} LT)`", "`Bạo Kích [${activeStance}]! Giáng -${outcome.damage} DMG (+${outcome.linhThachEarned} LT)`")

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched App.tsx successfully!")

def patch_interactive_preview():
    path = 'frontend/src/components/InteractiveAltarPreview.tsx'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update executeStrike: pure RPG strike
    old_strike = """    // Rhythm calculation: 100 BPM = 600ms period
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

    new_strike = """    // Action RPG Strike: Base Power + Chance of Critical Hit
    const isCrit = Math.random() < 0.25;
    const rating: 'PERFECT' | 'GREAT' | 'HIT' = isCrit ? 'PERFECT' : 'GREAT';
    const multiplier = isCrit ? 2.2 : 1.0;
    const baseDamage = isCrit ? 880 : 420;"""

    assert old_strike in content, "Could not find old_strike in InteractiveAltarPreview.tsx"
    content = content.replace(old_strike, new_strike, 1)

    # 2. Remove Section 6 Celestial Bagua Rhythm Reticle
    reticle_start = "      // 6. Celestial Bagua Rhythm Reticle (100 BPM)"
    reticle_end = "      ctx.restore();\n\n      // 7. Shockwaves"
    start_idx = content.find(reticle_start)
    end_idx = content.find(reticle_end)
    assert start_idx != -1 and end_idx != -1, f"Could not find reticle block in preview ({start_idx}, {end_idx})"

    content = content[:start_idx] + "      // Hero Dais Surface is completely clean and unobstructed\n" + content[end_idx + len("      ctx.restore();\n\n"):]

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched InteractiveAltarPreview.tsx successfully!")

def patch_right_panel():
    path = 'frontend/src/components/RightProgressionPanel.tsx'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    old_text = "Phù Thạch là kỳ trân dị bảo cực hiếm trong vũ trụ (rơi với tỉ lệ cực thấp khi nhát gõ Hoàng Kim hoặc phá vỡ Khiên Vòm Trời). Hãy kiên trì rèn đúc!"
    new_text = "Phù Thạch là kỳ trân dị bảo cực hiếm trong vũ trụ (rơi khi xuất hiện Bạo Kích hoặc phá vỡ Khiên Vòm Trời). Hãy kiên trì rèn đúc!"

    if old_text in content:
        content = content.replace(old_text, new_text, 1)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Patched RightProgressionPanel.tsx successfully!")

if __name__ == '__main__':
    patch_canvas()
    patch_app()
    patch_interactive_preview()
    patch_right_panel()
