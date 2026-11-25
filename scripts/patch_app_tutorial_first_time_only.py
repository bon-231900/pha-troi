with open('frontend/src/App.tsx', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Update useState(tutorialCompleted)
target_state = """  // Beginner Tutorial & Onboarding Guide State
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
  });"""

replacement_state = """  // Beginner Tutorial & Onboarding Guide State
  // QUY TẮC CỐT LÕI: Chỉ hiển thị DUY NHẤT LẦN ĐẦU TIÊN cho người chơi mới tinh (New User).
  // Đã từng chơi, đã xem hoặc từng bỏ qua -> 100% không bao giờ tự động hiện lại phiền toái.
  const [tutorialCompleted, setTutorialCompleted] = useState<boolean>(() => {
    try {
      if (safeStorage.getItem('phatroi_tutorial_seen') === '1') {
        return true;
      }
      const s = getInitialSaveString();
      if (s) {
        const parsed = JSON.parse(s);
        if (parsed.tutorialCompleted === true) {
          safeStorage.setItem('phatroi_tutorial_seen', '1');
          return true;
        }
        if (
          (parsed.playerTotalDamage || 0) > 0 ||
          (parsed.linhThach || 0) > 0 ||
          (parsed.level || 1) > 1 ||
          (Array.isArray(parsed.inventory) && parsed.inventory.length > 0)
        ) {
          safeStorage.setItem('phatroi_tutorial_seen', '1');
          return true;
        }
      }
    } catch {}
    return false;
  });"""

# 2. Update loadSlotProfile
target_load = """      const isDone = typeof prog.tutorialCompleted === 'boolean'
        ? prog.tutorialCompleted
        : ((prog.playerTotalDamage || 0) > 10000 || (profile.level || 1) > 1);
      setTutorialCompleted(isDone);
      setTutorialStep(prog.tutorialStep || (isDone ? 5 : 1));"""

replacement_load = """      const isDone =
        safeStorage.getItem('phatroi_tutorial_seen') === '1' ||
        (typeof prog.tutorialCompleted === 'boolean'
          ? prog.tutorialCompleted
          : ((prog.playerTotalDamage || 0) > 0 || (profile.level || 1) > 1 || (prog.linhThach || 0) > 0));
      setTutorialCompleted(isDone);
      if (isDone) safeStorage.setItem('phatroi_tutorial_seen', '1');
      setTutorialStep(prog.tutorialStep || (isDone ? 5 : 1));"""

# 3. Update handleClaimTutorialReward & handleSkipTutorial to set permanent device flag
target_claim = """  const handleClaimTutorialReward = useCallback(() => {
    setLinhThach((lt) => lt + 500);
    setIronDust((d) => d + 50);
    setTutorialCompleted(true);
    setTutorialStep(5);"""

replacement_claim = """  const handleClaimTutorialReward = useCallback(() => {
    safeStorage.setItem('phatroi_tutorial_seen', '1');
    setLinhThach((lt) => lt + 500);
    setIronDust((d) => d + 50);
    setTutorialCompleted(true);
    setTutorialStep(5);"""

target_skip = """  const handleSkipTutorial = useCallback(() => {
    setLinhThach((lt) => lt + 500);
    setIronDust((d) => d + 50);
    setTutorialCompleted(true);
    setTutorialStep(5);"""

replacement_skip = """  const handleSkipTutorial = useCallback(() => {
    safeStorage.setItem('phatroi_tutorial_seen', '1');
    setLinhThach((lt) => lt + 500);
    setIronDust((d) => d + 50);
    setTutorialCompleted(true);
    setTutorialStep(5);"""

assert target_state in c, 'target_state not found'
assert target_load in c, 'target_load not found'
assert target_claim in c, 'target_claim not found'
assert target_skip in c, 'target_skip not found'

c = c.replace(target_state, replacement_state, 1)
c = c.replace(target_load, replacement_load, 1)
c = c.replace(target_claim, replacement_claim, 1)
c = c.replace(target_skip, replacement_skip, 1)

with open('frontend/src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(c)

print('Updated App.tsx with strict first-time-only logic successfully!')
