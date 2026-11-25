with open('frontend/src/game/characterSlots.ts', 'r', encoding='utf-8') as f:
    c = f.read()

target = '''            if (!slot.progress.equippedItems || typeof slot.progress.equippedItems !== 'object') {
              slot.progress.equippedItems = ensureAllEquippedSlots(slot.progress.equippedItems);
              dirty = true;
            }'''

replacement = '''            if (!slot.progress.equippedItems || typeof slot.progress.equippedItems !== 'object') {
              slot.progress.equippedItems = ensureAllEquippedSlots(slot.progress.equippedItems);
              dirty = true;
            }
            // Auto-heal tutorial flag for existing players
            if (slot.progress.tutorialCompleted === undefined) {
              if (
                (slot.progress.playerTotalDamage || 0) > 0 ||
                (slot.progress.linhThach || 0) > 0 ||
                (slot.level || 1) > 1
              ) {
                slot.progress.tutorialCompleted = true;
                slot.progress.tutorialStep = 5;
                dirty = true;
              }
            }
            if (slot.progress.tutorialCompleted) {
              safeStorage.setItem('phatroi_tutorial_seen', '1');
            }'''

assert target in c, 'target not found'
c = c.replace(target, replacement, 1)

with open('frontend/src/game/characterSlots.ts', 'w', encoding='utf-8') as f:
    f.write(c)

print('Updated characterSlots.ts successfully!')
