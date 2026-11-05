with open('frontend/src/App.tsx', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Update CommunityPanoramicForgeCanvas props
old_canvas = """        <CommunityPanoramicForgeCanvas
          ref={canvasHandleRef}
          bossHp={bossHp}
          bossMaxHp={currentVault.maxHp}
          activeStance={activeStance}
          gameState={gameState}
          playerName={playerName}
          onHeroStrikeAction={() => handleHeroStrike(false)}
        />"""

new_canvas = """        <CommunityPanoramicForgeCanvas
          ref={canvasHandleRef}
          bossHp={bossHp}
          bossMaxHp={currentVault.maxHp}
          activeStance={activeStance}
          gameState={gameState}
          playerName={playerName}
          onHeroStrikeAction={() => handleHeroStrike(false)}
          equippedSkinId={equippedSkinId}
        />"""

assert old_canvas in c, 'old_canvas not found in App.tsx'
c = c.replace(old_canvas, new_canvas, 1)

# 2. Update StatusModal props
old_status = """          playerClass={getPlayerClass(playerClassId || 'thunder')}
          activeCharacterName={playerName}
        />"""

new_status = """          playerClass={getPlayerClass(playerClassId || 'thunder')}
          activeCharacterName={playerName}
          equippedSkinId={equippedSkinId}
          onEquipSkin={handleEquipSkin}
        />"""

assert old_status in c, 'old_status not found in App.tsx'
c = c.replace(old_status, new_status, 1)

with open('frontend/src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(c)

print('App.tsx patched successfully!')
