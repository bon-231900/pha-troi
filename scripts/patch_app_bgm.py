with open('frontend/src/App.tsx', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Add gameState BGM controller
target_gesture = '''    window.addEventListener('pointerdown', handleFirstGesture, { once: true });
    window.addEventListener('keydown', handleFirstGesture, { once: true });
    return () => {
      window.removeEventListener('pointerdown', handleFirstGesture);
      window.removeEventListener('keydown', handleFirstGesture);
    };
  }, []);'''

replacement_gesture = '''    window.addEventListener('pointerdown', handleFirstGesture, { once: true });
    window.addEventListener('keydown', handleFirstGesture, { once: true });
    return () => {
      window.removeEventListener('pointerdown', handleFirstGesture);
      window.removeEventListener('keydown', handleFirstGesture);
    };
  }, []);

  // Sync BGM with Game State (Pause on pause/modal, resume on playing)
  useEffect(() => {
    if (gameState === 'playing') {
      soundEngine.resumeBgm();
    } else if (gameState === 'paused' || gameState === 'character_select') {
      soundEngine.pauseBgm();
    }
  }, [gameState]);'''

assert target_gesture in c, 'target_gesture not found'
c = c.replace(target_gesture, replacement_gesture, 1)

# 2. Replace soundEngine.muted = next; with soundEngine.setMuted(next);
c = c.replace('soundEngine.muted = next;', 'soundEngine.setMuted(next);')

with open('frontend/src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(c)

print('Updated App.tsx with BGM control successfully!')
