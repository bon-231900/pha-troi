# -*- coding: utf-8 -*-
with open('frontend/src/App.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Add lastHeroStrikeTimeRef around line 605
target_ref = "  const realtimeRoomRef = useRef<RealtimeRoomClient | null>(null);"
new_ref = """  const realtimeRoomRef = useRef<RealtimeRoomClient | null>(null);
  const lastHeroStrikeTimeRef = useRef<number>(0);"""

assert target_ref in code, "target_ref not found"
code = code.replace(target_ref, new_ref, 1)

# 2. Add throttle to handleHeroStrike
target_strike = """  const handleHeroStrike = useCallback(
    (forceGolden = false) => {
      if (gameState !== 'playing') {
        if (gameState === 'title') startGame();
        return;
      }"""

new_strike = """  const handleHeroStrike = useCallback(
    (forceGolden = false) => {
      if (gameState !== 'playing') {
        if (gameState === 'title') startGame();
        return;
      }

      // Throttle tối thiểu 100ms giữa các nhát gõ chống spam/macro quá tải đồ họa & âm thanh
      const now = performance.now();
      if (now - lastHeroStrikeTimeRef.current < 100) {
        return;
      }
      lastHeroStrikeTimeRef.current = now;"""

assert target_strike in code, "target_strike not found"
code = code.replace(target_strike, new_strike, 1)

# 3. Add e.repeat check in onKeyDown
target_keydown = """  // Keyboard Shortcuts: Space, Q/W/E/R, P/Esc, M, [ and ]
  useEffect(() => {
    const onKeyDown = (e: KeyboardEvent) => {
      if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) {
        return;
      }"""

new_keydown = """  // Keyboard Shortcuts: Space, Q/W/E/R, P/Esc, M, [ and ]
  useEffect(() => {
    const onKeyDown = (e: KeyboardEvent) => {
      // Chặn hoàn toàn sự kiện giữ im phím (e.repeat) của trình duyệt để không spam đập búa / kỹ năng gây lag
      if (e.repeat) {
        e.preventDefault();
        return;
      }

      if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) {
        return;
      }"""

assert target_keydown in code, "target_keydown not found"
code = code.replace(target_keydown, new_keydown, 1)

with open('frontend/src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(code)

print("Key repeat & strike throttle fix applied successfully to App.tsx!")
