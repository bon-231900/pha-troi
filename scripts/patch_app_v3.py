# -*- coding: utf-8 -*-
"""
Script to apply Balance Patch v3.0 logic to App.tsx
"""
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

with open(r'd:\tieu-thuyet\frontend\src\App.tsx', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Imports: add checkForgeEquilibrium
c = c.replace(
    "  calculateArsenalBonuses,\n",
    "  calculateArsenalBonuses,\n  checkForgeEquilibrium,\n"
)

# 2. Fix line 484: 'slate' -> 'neutral'
c = c.replace(
    "appendCombatLog('🍂 Một đồng môn vừa tạm lui về hậu phương nghỉ ngơi.', 'slate');",
    "appendCombatLog('🍂 Một đồng môn vừa tạm lui về hậu phương nghỉ ngơi.', 'neutral');"
)

# 3. Fix line 509: peers mapping
c = c.replace(
    "canvasHandleRef.current?.updateRemotePeers(peers);",
    "canvasHandleRef.current?.updateRemotePeers(peers.map((p) => ({ peerId: p.id, name: p.name, guildId: p.guildId, stance: p.stance, slotIndex: p.slotIndex })));"
)

# 4. Fix line 893: rollLootDrop argument
c = c.replace(
    "const droppedItem = rollLootDrop(\n          grade === 'PERFECT' ? 'perfect' : 'great',",
    "const droppedItem = rollLootDrop(\n          grade,"
)

# 5. Fix line 1676: StatusModal onRestart
c = c.replace(
    "          onResume={() => setGameState('playing')}\n          onReturnTitle={returnToTitle}\n        />",
    "          onResume={() => setGameState('playing')}\n          onReturnTitle={returnToTitle}\n          onRestart={startGame}\n        />"
)

# 6. Add stanceWeave state
target_state_anchor = "const [shieldBreakTimeLeft, setShieldBreakTimeLeft] = useState<number>(0);"
new_state_block = """const [shieldBreakTimeLeft, setShieldBreakTimeLeft] = useState<number>(0);
  const [stanceWeave, setStanceWeave] = useState<{ previousStance: StanceKey; timeLeftSec: number } | null>(null);"""
c = c.replace(target_state_anchor, new_state_block)

# 7. Add stanceWeave countdown to game loop
target_timer_anchor = "setShieldBreakTimeLeft((prev) => {"
new_timer_block = """setStanceWeave((prev) => {
        if (!prev) return null;
        if (prev.timeLeftSec <= 1) return null;
        return { ...prev, timeLeftSec: prev.timeLeftSec - 1 };
      });

      setShieldBreakTimeLeft((prev) => {"""
c = c.replace(target_timer_anchor, new_timer_block)

# 8. Pass upgrades to calculateArsenalBonuses
c = c.replace(
    "const arsenalBonuses = calculateArsenalBonuses(equippedItems);",
    "const arsenalBonuses = calculateArsenalBonuses(equippedItems, upgrades);"
)

# 9. Update handleHeroStrike: remove 45% RNG golden coin-flip, use balanced timing & pass currentFloorId + stanceWeave
old_strike_logic = """      // Rhythm judgment: forceGolden or default perfect/great
      const isGoldenHit = forceGolden || Math.random() < 0.45;
      const grade = isGoldenHit ? 'PERFECT' : 'GREAT';

      const forgerRank = getForgerRank(playerTotalDamage);
      const stanceSkillBonuses = calculateStanceSkillBonuses(stanceSkills, activeStance);

      const outcome = calculateStrikeOutcome({
        grade,
        stance: activeStance,
        basePower,
        combo,
        overdriveCharge,
        overdriveActive,
        bossShieldPct: isShieldBroken ? 0 : bossShieldPct,
        spiritBonusMult,
        globalBurstActive,
        anvilHeat,
        sealDamageReductionPct: currentSeal.damageReductionPct,
        isShieldBroken,
        arsenalBonuses,
        stanceSkillBonuses,
        forgerRankMultiplier: forgerRank.damageMultiplier,
      });"""

new_strike_logic = """      // Rhythm judgment: true skill timing or Overdrive burst (No more 45% RNG auto-crit!)
      const isGoldenHit = forceGolden || overdriveActive || (combo >= 5 && Math.random() < 0.15);
      const grade: JudgmentGrade = isGoldenHit ? 'PERFECT' : 'GREAT';

      const forgerRank = getForgerRank(playerTotalDamage);
      const stanceSkillBonuses = calculateStanceSkillBonuses(stanceSkills, activeStance);

      const outcome = calculateStrikeOutcome({
        grade,
        stance: activeStance,
        basePower,
        combo,
        overdriveCharge,
        overdriveActive,
        bossShieldPct: isShieldBroken ? 0 : bossShieldPct,
        spiritBonusMult,
        globalBurstActive,
        anvilHeat,
        sealDamageReductionPct: currentSeal.damageReductionPct,
        isShieldBroken,
        arsenalBonuses,
        stanceSkillBonuses,
        forgerRankMultiplier: forgerRank.damageMultiplier,
        currentFloorId: currentVaultId,
        stanceWeave,
      });"""
c = c.replace(old_strike_logic, new_strike_logic)

# 10. Update combat text labels for Glancing Hit & True Crit
old_label_logic = """      const stanceData = HAMMER_STANCES[activeStance];
      const isCritHit = outcome.isCrit;
      const combatGradeLabel = isCritHit
        ? `BẠO KÍCH! x${outcome.displayMultiplier}`
        : isGoldenHit
        ? 'HOÀNG KIM! x3.0'
        : 'CHUẨN XÁC! x1.0';

      const combatGradeColor = isCritHit
        ? '#00F0FF'
        : isGoldenHit
        ? '#FFD166'
        : stanceData.color;"""

new_label_logic = """      const stanceData = HAMMER_STANCES[activeStance];
      const isCritHit = outcome.isCrit;
      const isGlancingHit = outcome.isGlancingHit;

      const combatGradeLabel = isGlancingHit
        ? 'DỘI BÚA! (LÒ NGUỘI) x0.6'
        : isCritHit
        ? `⚡ BẠO KÍCH! x${outcome.displayMultiplier}`
        : isGoldenHit
        ? `HOÀNG KIM! x${outcome.displayMultiplier}`
        : 'CHUẨN XÁC! x1.0';

      const combatGradeColor = isGlancingHit
        ? '#EF4444'
        : isCritHit
        ? '#00F0FF'
        : isGoldenHit
        ? '#FFD166'
        : stanceData.color;"""
c = c.replace(old_label_logic, new_label_logic)

# 11. Update combat log for Glancing Hit
old_log_logic = """      if (isCritHit) {
        appendCombatLog(
          `⚡ [BẠO KÍCH BAO TAY] [${activeStance}] giáng -${outcome.damage} DMG! (+${outcome.linhThachEarned} LT)`,
          'cyan'
        );
      } else if (isGoldenHit) {
        appendCombatLog(
          `Nhịp Hoàng Kim [${activeStance}]! Giáng -${outcome.damage} DMG (+${outcome.linhThachEarned} LT)`,
          'gold'
        );
      } else {
        appendCombatLog(
          `Nhịp Chuẩn Xác [${activeStance}]! Giáng -${outcome.damage} DMG (+${outcome.linhThachEarned} LT)`,
          'neutral'
        );
      }"""

new_log_logic = """      if (isGlancingHit) {
        appendCombatLog(
          `⚠️ [DỘI BÚA] Lực Chùy quá cao so với Nhiệt Lò (${arsenalBonuses.coreStats.str} > 2.5x ${arsenalBonuses.coreStats.int})! Sát thương giảm 35%!`,
          'red'
        );
      } else if (isCritHit) {
        appendCombatLog(
          `⚡ [BẠO KÍCH BAO TAY] [${activeStance}] giáng -${outcome.damage} DMG! (+${outcome.linhThachEarned} LT)`,
          'cyan'
        );
      } else if (isGoldenHit) {
        appendCombatLog(
          `Nhịp Hoàng Kim [${activeStance}]! Giáng -${outcome.damage} DMG (+${outcome.linhThachEarned} LT)`,
          'gold'
        );
      } else {
        appendCombatLog(
          `Nhịp Chuẩn Xác [${activeStance}]! Giáng -${outcome.damage} DMG (+${outcome.linhThachEarned} LT)`,
          'neutral'
        );
      }"""
c = c.replace(old_log_logic, new_log_logic)

# 12. Update handleSelectStance: trigger Stance Weaving if combo >= 4
old_stance_logic = """  const handleSelectStance = useCallback(
    (stance: StanceKey) => {
      setActiveStance(stance);
      realtimeRoomRef.current?.updateIdentity(stance, userGuildId);
      soundEngine.playStanceSwitch(stance);
      appendCombatLog(
        `Chuyển thế búa: [${stance}] ${HAMMER_STANCES[stance].name} (${HAMMER_STANCES[stance].title})`,
        'cyan'
      );
    },
    [appendCombatLog]
  );"""

new_stance_logic = """  const handleSelectStance = useCallback(
    (stance: StanceKey) => {
      if (stance === activeStance) return;
      if (combo >= 4) {
        setStanceWeave({ previousStance: activeStance, timeLeftSec: 6 });
        soundEngine.playComboStreakSound?.(5);
        appendCombatLog(
          `✦ [KÍCH HOẠT CHUYỂN THẾ] Giữ lại 50% uy lực [${activeStance}] trong 6 giây!`,
          'gold'
        );
      }
      setActiveStance(stance);
      realtimeRoomRef.current?.updateIdentity(stance, userGuildId);
      soundEngine.playStanceSwitch(stance);
      appendCombatLog(
        `Chuyển thế búa: [${stance}] ${HAMMER_STANCES[stance].name} (${HAMMER_STANCES[stance].title})`,
        'cyan'
      );
    },
    [activeStance, combo, userGuildId, appendCombatLog]
  );"""
c = c.replace(old_stance_logic, new_stance_logic)

# 13. Update handleBuyUpgrade: enforce Forge Equilibrium
old_buy_upgrade = """  const handleBuyUpgrade = useCallback(
    (upgradeId: string) => {
      setUpgrades((prev) =>
        prev.map((u) => {
          if (u.id !== upgradeId) return u;
          const cost = getUpgradeCost(u);
          if (linhThach < cost || u.level >= u.maxLevel) return u;
          setLinhThach((lt) => lt - cost);
          soundEngine.playStanceSwitch('E');
          appendCombatLog(`Rèn Cấp thành công: ${u.name} lên Cấp ${u.level + 1}!`, 'gold');
          return { ...u, level: u.level + 1 };
        })
      );
    },
    [linhThach, appendCombatLog]
  );"""

new_buy_upgrade = """  const handleBuyUpgrade = useCallback(
    (upgradeId: string) => {
      const eqCheck = checkForgeEquilibrium(upgrades, upgradeId);
      if (!eqCheck.allowed) {
        soundEngine.playComboStreakSound?.(1);
        appendCombatLog(
          `🔒 ${eqCheck.reason}`,
          'red'
        );
        return;
      }

      setUpgrades((prev) =>
        prev.map((u) => {
          if (u.id !== upgradeId) return u;
          const cost = getUpgradeCost(u);
          if (linhThach < cost || u.level >= u.maxLevel) return u;
          setLinhThach((lt) => lt - cost);
          soundEngine.playStanceSwitch('E');
          appendCombatLog(`Rèn Cấp thành công: ${u.name} lên Cấp ${u.level + 1}!`, 'gold');
          return { ...u, level: u.level + 1 };
        })
      );
    },
    [linhThach, upgrades, appendCombatLog]
  );"""
c = c.replace(old_buy_upgrade, new_buy_upgrade)

# 14. Pass stanceWeave to LeftTacticalPanel
c = c.replace(
    "            activeStance={activeStance}\n            onSelectStance={handleSelectStance}",
    "            activeStance={activeStance}\n            onSelectStance={handleSelectStance}\n            stanceWeave={stanceWeave}"
)

with open(r'd:\tieu-thuyet\frontend\src\App.tsx', 'w', encoding='utf-8') as f:
    f.write(c)

print("App.tsx đã được nâng cấp Balance Patch v3.0 thành công!")
