# -*- coding: utf-8 -*-
with open('frontend/src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update imports
old_slots_imp = "createCharacterInSlot,\n  deleteCharacterSlot,\n  updateActiveSlotProgress,\n  CharacterProfile,"
new_slots_imp = "createCharacterInSlot,\n  deleteCharacterSlot,\n  updateActiveSlotProgress,\n  updateCharacterSkinInSlot,\n  CharacterProfile,"
if old_slots_imp not in content:
    old_slots_imp = old_slots_imp.replace("\n", "\r\n")
    new_slots_imp = new_slots_imp.replace("\n", "\r\n")
content = content.replace(old_slots_imp, new_slots_imp, 1)

old_rules_imp = "import {\n  HAMMER_TIERS,\n  STANCE_METAS,"
new_rules_imp = "import {\n  SECT_DEFAULT_SKIN,\n  CHARACTER_SKINS,\n  HAMMER_TIERS,\n  STANCE_METAS,"
if old_rules_imp not in content:
    old_rules_imp = old_rules_imp.replace("\n", "\r\n")
    new_rules_imp = new_rules_imp.replace("\n", "\r\n")
content = content.replace(old_rules_imp, new_rules_imp, 1)

# 2. Add equippedSkinId state near playerClassId state
old_class_state = "const [playerClassId, setPlayerClassId] = useState<PlayerClassId | null>(null);"
new_class_state = """const [playerClassId, setPlayerClassId] = useState<PlayerClassId | null>(null);
  const [equippedSkinId, setEquippedSkinId] = useState<string>(() => {
    return safeStorage.getItem('phatroi_equipped_skin') || 'skin_default';
  });"""
if old_class_state not in content:
    old_class_state = old_class_state.replace("\n", "\r\n")
    new_class_state = new_class_state.replace("\n", "\r\n")
content = content.replace(old_class_state, new_class_state, 1)

# 3. Update loadSlotProfile to sync equippedSkinId
old_load_slot = """      setPlayerName(profile.characterName);
      safeStorage.setItem('phatroi_user_name', profile.characterName);
      safeStorage.setItem('phatroi_player_class', profile.classId);"""

new_load_slot = """      setPlayerName(profile.characterName);
      safeStorage.setItem('phatroi_user_name', profile.characterName);
      safeStorage.setItem('phatroi_player_class', profile.classId);
      const skin = profile.equippedSkinId || SECT_DEFAULT_SKIN[profile.classId] || 'skin_default';
      setEquippedSkinId(skin);
      safeStorage.setItem('phatroi_equipped_skin', skin);
      if (realtimeClientRef.current) {
        const cls = getPlayerClass(profile.classId);
        realtimeClientRef.current.updateIdentity(cls.stanceKey, cls.guildId, profile.characterName, skin);
      }"""

if old_load_slot not in content:
    old_load_slot = old_load_slot.replace("\n", "\r\n")
    new_load_slot = new_load_slot.replace("\n", "\r\n")
content = content.replace(old_load_slot, new_load_slot, 1)

# 4. Update handleCommitClass
old_commit = """  const handleCommitClass = useCallback(
    (classId: PlayerClassId, name: string) => {
      const targetSlot = creatingSlotId || activeSlotId;
      const newProfile = createCharacterInSlot(targetSlot, name, classId, googleUser?.googleId);"""

new_commit = """  const handleCommitClass = useCallback(
    (classId: PlayerClassId, name: string, skinId?: string) => {
      const targetSlot = creatingSlotId || activeSlotId;
      const finalSkinId = skinId || SECT_DEFAULT_SKIN[classId] || 'skin_default';
      const newProfile = createCharacterInSlot(targetSlot, name, classId, googleUser?.googleId, finalSkinId);"""

if old_commit not in content:
    old_commit = old_commit.replace("\n", "\r\n")
    new_commit = new_commit.replace("\n", "\r\n")
content = content.replace(old_commit, new_commit, 1)

# Add skin state update in handleCommitClass
old_commit_body = """      setActiveStance(cls.stanceKey);
      setUserGuildId(cls.guildId);
      soundEngine.playGlobalBurstFanfare();"""

new_commit_body = """      setActiveStance(cls.stanceKey);
      setUserGuildId(cls.guildId);
      setEquippedSkinId(finalSkinId);
      safeStorage.setItem('phatroi_equipped_skin', finalSkinId);
      if (realtimeClientRef.current) {
        realtimeClientRef.current.updateIdentity(cls.stanceKey, cls.guildId, name, finalSkinId);
      }
      soundEngine.playGlobalBurstFanfare();"""

if old_commit_body not in content:
    old_commit_body = old_commit_body.replace("\n", "\r\n")
    new_commit_body = new_commit_body.replace("\n", "\r\n")
content = content.replace(old_commit_body, new_commit_body, 1)

# 5. Add handleEquipSkin handler
old_select_slot = """  const handleSelectSlot = useCallback("""
new_handler = """  const handleEquipSkin = useCallback(
    (skinId: string) => {
      setEquippedSkinId(skinId);
      safeStorage.setItem('phatroi_equipped_skin', skinId);
      updateCharacterSkinInSlot(activeSlotId, skinId, googleUser?.googleId);
      const updated = loadCharacterSlots(googleUser?.googleId);
      setCharacterSlots(updated);
      if (realtimeClientRef.current) {
        realtimeClientRef.current.updateIdentity(undefined, undefined, undefined, skinId);
      }
      soundEngine.playAnvilStrike('PERFECT', 'Q', false);
      const sName = CHARACTER_SKINS[skinId]?.name || 'Trang Phục Mới';
      appendCombatLog(`👘 [Y PHỤC] Bạn đã khoác lên [${sName}]!`, 'cyan');
    },
    [activeSlotId, googleUser, appendCombatLog]
  );

  const handleSelectSlot = useCallback("""

if old_select_slot not in content:
    old_select_slot = old_select_slot.replace("\n", "\r\n")
    new_handler = new_handler.replace("\n", "\r\n")
content = content.replace(old_select_slot, new_handler, 1)

# 6. Pass equippedSkinId to CommunityPanoramicForgeCanvas
old_canvas = """        <CommunityPanoramicForgeCanvas
          ref={canvasRef}
          activeStance={activeStance}
          bossHpPct={bossHpPct}
          skyState={skyState}
          isHitFlashing={isHitFlashing}
          playerName={playerName}
          onAnvilHit={handleCanvasAnvilHit}
        />"""

new_canvas = """        <CommunityPanoramicForgeCanvas
          ref={canvasRef}
          activeStance={activeStance}
          bossHpPct={bossHpPct}
          skyState={skyState}
          isHitFlashing={isHitFlashing}
          playerName={playerName}
          equippedSkinId={equippedSkinId}
          onAnvilHit={handleCanvasAnvilHit}
        />"""

if old_canvas not in content:
    old_canvas = old_canvas.replace("\n", "\r\n")
    new_canvas = new_canvas.replace("\n", "\r\n")
content = content.replace(old_canvas, new_canvas, 1)

# 7. Pass equippedSkinId and onEquipSkin to StatusModal
old_status_modal = """        <StatusModal
          isOpen={true}
          onClose={() => setGameState('playing')}
          onRestart={startGame}
          onReturnTitle={() => setGameState('title')}
          onSwitchCharacter={() => {
            setGameState('character_select');
          }}
          onToggleMute={toggleMute}
          muted={isMuted}
          playerClass={playerClassId ? getPlayerClass(playerClassId) : undefined}
        />"""

new_status_modal = """        <StatusModal
          isOpen={true}
          onClose={() => setGameState('playing')}
          onRestart={startGame}
          onReturnTitle={() => setGameState('title')}
          onSwitchCharacter={() => {
            setGameState('character_select');
          }}
          onToggleMute={toggleMute}
          muted={isMuted}
          playerClass={playerClassId ? getPlayerClass(playerClassId) : undefined}
          equippedSkinId={equippedSkinId}
          onEquipSkin={handleEquipSkin}
        />"""

if old_status_modal not in content:
    old_status_modal = old_status_modal.replace("\n", "\r\n")
    new_status_modal = new_status_modal.replace("\n", "\r\n")
content = content.replace(old_status_modal, new_status_modal, 1)

with open('frontend/src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS: App.tsx patched with skin support!")
