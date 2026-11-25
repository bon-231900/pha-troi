with open('frontend/src/App.tsx', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Imports
target_import = "import { LootNotificationFeed, LootToastItem } from './components/LootNotificationFeed';"
replacement_import = """import { LootNotificationFeed, LootToastItem } from './components/LootNotificationFeed';
import { BeginnerTutorialGuide } from './components/BeginnerTutorialGuide';
import { ForgeGuideHelpModal } from './components/ForgeGuideHelpModal';"""

assert target_import in c, 'target_import not found'
c = c.replace(target_import, replacement_import, 1)

# 2. States
target_state = "  const [burnStacks, setBurnStacks] = useState<number>(0);\n  const goldenStreakRef = useRef<number>(0);"
replacement_state = """  const [burnStacks, setBurnStacks] = useState<number>(0);
  const goldenStreakRef = useRef<number>(0);

  // Beginner Tutorial & Onboarding Guide State
  const [tutorialCompleted, setTutorialCompleted] = useState<boolean>(() => {
    try {
      const s = getInitialSaveString();
      if (s) {
        const parsed = JSON.parse(s);
        if (typeof parsed.tutorialCompleted === 'boolean') return parsed.tutorialCompleted;
        if ((parsed.playerTotalDamage || 0) > 10000) return true;
      }
    } catch {}
    return false;
  });
  const [tutorialStep, setTutorialStep] = useState<number>(() => {
    try {
      const s = getInitialSaveString();
      if (s) {
        const parsed = JSON.parse(s);
        if (typeof parsed.tutorialStep === 'number') return parsed.tutorialStep;
        if (parsed.tutorialCompleted) return 5;
      }
    } catch {}
    return 1;
  });
  const [tutorialStrikes, setTutorialStrikes] = useState<number>(0);
  const [tutorialHeatStrikes, setTutorialHeatStrikes] = useState<number>(0);
  const [tutorialSkillUsed, setTutorialSkillUsed] = useState<boolean>(false);
  const [isGuideModalOpen, setIsGuideModalOpen] = useState<boolean>(false);"""

assert target_state in c, 'target_state not found'
c = c.replace(target_state, replacement_state, 1)

# 3. Save State Payload
target_save = """          serverFurnaceHeat,
          serverAnvilHp,
          raidContributionScore,
          lastActiveTimestamp: Date.now(),
        };"""

replacement_save = """          serverFurnaceHeat,
          serverAnvilHp,
          raidContributionScore,
          ironDust,
          celestialStars,
          anvilPityCount,
          raidPityCount,
          tutorialCompleted,
          tutorialStep,
          lastActiveTimestamp: Date.now(),
        };"""

assert target_save in c, 'target_save not found'
c = c.replace(target_save, replacement_save, 1)

# 4. loadSlotProfile
target_load = """      setLinhThach(prog.linhThach || 0);
      setTinhHoa(prog.tinhHoa || 0);"""

replacement_load = """      setLinhThach(prog.linhThach || 0);
      setTinhHoa(prog.tinhHoa || 0);
      if (typeof prog.ironDust === 'number') setIronDust(prog.ironDust);
      if (typeof prog.celestialStars === 'number') setCelestialStars(prog.celestialStars);
      if (typeof prog.anvilPityCount === 'number') setAnvilPityCount(prog.anvilPityCount);
      if (typeof prog.raidPityCount === 'number') setRaidPityCount(prog.raidPityCount);

      const isDone = typeof prog.tutorialCompleted === 'boolean'
        ? prog.tutorialCompleted
        : ((prog.playerTotalDamage || 0) > 10000 || (profile.level || 1) > 1);
      setTutorialCompleted(isDone);
      setTutorialStep(prog.tutorialStep || (isDone ? 5 : 1));
      setTutorialStrikes(0);
      setTutorialHeatStrikes(0);
      setTutorialSkillUsed(false);"""

assert target_load in c, 'target_load not found'
c = c.replace(target_load, replacement_load, 1)

# 5. Add Claim & Skip handlers before handleCastClassSkill
target_handlers_pos = "  const handleCastClassSkill = useCallback("
replacement_handlers = """  const handleClaimTutorialReward = useCallback(() => {
    setLinhThach((lt) => lt + 500);
    setIronDust((d) => d + 50);
    setTutorialCompleted(true);
    setTutorialStep(5);
    soundEngine.playGlobalBurstFanfare();
    canvasHandleRef.current?.spawnCombatText('🎉 NHẬP MÔN THÀNH CÔNG!', '+500 LT & +50 BỤI THIẾT', '#10B981', '#FFD700', true);
    appendCombatLog('🎁 [QUÀ TÂN THỦ] Chúc mừng đạo hữu nhập môn thành công! Nhận được +500 Linh Thạch và +50 Bụi Thiết để tôi luyện thần binh!', 'gold');
    try {
      updateActiveSlotProgress(activeSlotId, {
        tutorialCompleted: true,
        tutorialStep: 5,
        linhThach: linhThach + 500,
        ironDust: ironDust + 50,
        lastActiveTimestamp: Date.now(),
      }, googleUser?.googleId);
    } catch {}
  }, [activeSlotId, googleUser, linhThach, ironDust, appendCombatLog]);

  const handleSkipTutorial = useCallback(() => {
    setLinhThach((lt) => lt + 500);
    setIronDust((d) => d + 50);
    setTutorialCompleted(true);
    setTutorialStep(5);
    soundEngine.playGlobalBurstFanfare();
    canvasHandleRef.current?.spawnCombatText('🎁 BỎ QUA & NHẬN QUÀ!', '+500 LT & +50 BỤI THIẾT', '#10B981', '#FFD700', true);
    appendCombatLog('🎁 [QUÀ TÂN THỦ] Bạn đã nhận quà nhập môn: +500 Linh Thạch & +50 Bụi Thiết!', 'gold');
    try {
      updateActiveSlotProgress(activeSlotId, {
        tutorialCompleted: true,
        tutorialStep: 5,
        linhThach: linhThach + 500,
        ironDust: ironDust + 50,
        lastActiveTimestamp: Date.now(),
      }, googleUser?.googleId);
    } catch {}
  }, [activeSlotId, googleUser, linhThach, ironDust, appendCombatLog]);

  const handleCastClassSkill = useCallback("""

assert target_handlers_pos in c, 'target_handlers_pos not found'
c = c.replace(target_handlers_pos, replacement_handlers, 1)

# 6. Tutorial step progression inside handleHeroStrike
target_strike_end = """      // 5. Update Phá Giáp Resonance (Active Armor Break Points)"""
replacement_strike_end = """      // Tutorial Step 1 & 2 Progression
      if (!tutorialCompleted) {
        if (tutorialStep === 1) {
          setTutorialStrikes((prev) => {
            const next = prev + 1;
            if (next >= 3) {
              setTutorialStep(2);
              canvasHandleRef.current?.spawnCombatText('✨ BƯỚC 1 HOÀN THÀNH!', 'THỔI BÙNG HỎA LÒ!', '#F59E0B', '#FFFFFF', true);
              appendCombatLog('🌟 [HƯỚNG DẪN TÂN THỦ] Hoàn thành Bước 1! Hãy tiếp tục gõ để thổi bùng Hỏa Lò.', 'gold');
            }
            return next;
          });
        } else if (tutorialStep === 2) {
          setTutorialHeatStrikes((prev) => {
            const next = prev + 1;
            if (next >= 5) {
              setTutorialStep(3);
              setOverdriveCharge((ov) => Math.max(ov, 2));
              canvasHandleRef.current?.spawnCombatText('🔥 HỎA LÒ RỰC CHÁY!', 'THỨC TỈNH TUYỆT KỸ [W]!', '#FF4D00', '#F59E0B', true);
              appendCombatLog('⚡ [HƯỚNG DẪN TÂN THỦ] Hoàn thành Bước 2! Năng lượng Thần Lực đã nạp sẵn, hãy bấm phím [W] để tung chiêu thức!', 'cyan');
            }
            return next;
          });
        }
      }

      // 5. Update Phá Giáp Resonance (Active Armor Break Points)"""

assert target_strike_end in c, 'target_strike_end not found'
c = c.replace(target_strike_end, replacement_strike_end, 1)

# 7. Tutorial step 3 progression inside handleCastClassSkill
target_cast_skill = """      if (slotKey === 'W') {
        if (skillCooldowns.W > 0) return;"""
replacement_cast_skill = """      // Tutorial Step 3 Progression
      if (!tutorialCompleted && tutorialStep === 3) {
        setTutorialSkillUsed(true);
        setTutorialStep(4);
        canvasHandleRef.current?.spawnCombatText('⚡ TUYỆT KỸ BÙNG NỔ!', 'MỞ LÒ RÈN NHẬN QUÀ!', '#06B6D4', '#F59E0B', true);
        appendCombatLog('🛡️ [HƯỚNG DẪN TÂN THỦ] Hoàn thành Bước 3! Hãy bấm nút [LÒ RÈN] (phím ] ) để nhận Gói Quà Nhập Môn!', 'gold');
      }

      if (slotKey === 'W') {
        if (skillCooldowns.W > 0) return;"""

assert target_cast_skill in c, 'target_cast_skill not found'
c = c.replace(target_cast_skill, replacement_cast_skill, 1)

# 8. Add onOpenGuide to TopBossHeader
target_header_pause = """        onPause={() =>
          setGameState((prev) => (prev === 'playing' ? 'paused' : 'playing'))
        }"""
replacement_header_pause = """        onOpenGuide={() => setIsGuideModalOpen(true)}
        onPause={() =>
          setGameState((prev) => (prev === 'playing' ? 'paused' : 'playing'))
        }"""

assert target_header_pause in c, 'target_header_pause not found'
c = c.replace(target_header_pause, replacement_header_pause, 1)

# 9. Add onOpenGuide to StatusModal
target_status_modal = """          onEquipSkin={handleEquipSkin}
        />"""
replacement_status_modal = """          onEquipSkin={handleEquipSkin}
          onOpenGuide={() => setIsGuideModalOpen(true)}
        />"""

assert target_status_modal in c, 'target_status_modal not found'
c = c.replace(target_status_modal, replacement_status_modal, 1)

# 10. Render BeginnerTutorialGuide and ForgeGuideHelpModal in JSX
target_bottom_panels = "{/* 5. SLIDE-OUT DRAWER 2 (RIGHT): NÂNG CẤP, THẦN HỒN & BẢNG VÀNG - CELESTIAL STELE BOARD */}"
replacement_bottom_panels = """{/* Beginner Tutorial Guide HUD (Floating Daoist Jade Scroll) */}
      {gameState === 'playing' && !tutorialCompleted && (
        <BeginnerTutorialGuide
          currentStep={tutorialStep}
          strikesCount={tutorialStrikes}
          heatStrikesCount={tutorialHeatStrikes}
          hasUsedSkill={tutorialSkillUsed}
          rightPanelOpen={rightPanelOpen}
          playerClassName={getPlayerClass(playerClassId || 'thunder').name}
          onClaimReward={handleClaimTutorialReward}
          onSkipTutorial={handleSkipTutorial}
          onOpenForgePanel={() => setRightPanelOpen(true)}
        />
      )}

      {/* Forge Rules & Mechanics Help Guide Modal */}
      <ForgeGuideHelpModal
        isOpen={isGuideModalOpen}
        onClose={() => setIsGuideModalOpen(false)}
        playerClassName={getPlayerClass(playerClassId || 'thunder').name}
      />

      {/* 5. SLIDE-OUT DRAWER 2 (RIGHT): NÂNG CẤP, THẦN HỒN & BẢNG VÀNG - CELESTIAL STELE BOARD */}"""

assert target_bottom_panels in c, 'target_bottom_panels not found'
c = c.replace(target_bottom_panels, replacement_bottom_panels, 1)

with open('frontend/src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(c)

print('Updated App.tsx successfully!')
