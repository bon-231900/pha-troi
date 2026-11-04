# -*- coding: utf-8 -*-
with open('frontend/src/App.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

old_block = """  // Google Sign-In & Cloud Save Integration (Strict Account vs Guest Separation)
  useEffect(() => {
    googleAuthService.initGsi(() => '');

    googleAuthService.onLogin((profile, remoteSaveData) => {
      // 1. Lưu giữ nguyên vẹn dữ liệu Chế Độ Khách hiện tại vào slot khách (độc lập tuyệt đối)
      try {
        const guestPayload = {
          bossHp,
          linhThach,
          tinhHoa,
          ironDust,
          celestialStars,
          anvilPityCount,
          raidPityCount,
          autoSalvageTiers,
          upgrades,
          spiritNodes,
          stanceSkills,
          equippedItems,
          inventory,
          playerTotalDamage,
          claimedMilestones,
          currentVaultId,
          userGuildId,
          guildHearths,
          serverFurnaceHeat,
          serverAnvilHp,
          raidContributionScore,
          lastActiveTimestamp: Date.now(),
        };
        safeStorage.setItem('phatroi_guest_save', JSON.stringify(guestPayload));
      } catch {}"""

new_block = """  // Keep latest state ref to avoid re-triggering GSI init on every hammer strike
  const latestGuestStateRef = useRef({
    bossHp,
    linhThach,
    tinhHoa,
    ironDust,
    celestialStars,
    anvilPityCount,
    raidPityCount,
    autoSalvageTiers,
    upgrades,
    spiritNodes,
    stanceSkills,
    equippedItems,
    inventory,
    playerTotalDamage,
    claimedMilestones,
    currentVaultId,
    userGuildId,
    guildHearths,
    serverFurnaceHeat,
    serverAnvilHp,
    raidContributionScore,
  });
  latestGuestStateRef.current = {
    bossHp,
    linhThach,
    tinhHoa,
    ironDust,
    celestialStars,
    anvilPityCount,
    raidPityCount,
    autoSalvageTiers,
    upgrades,
    spiritNodes,
    stanceSkills,
    equippedItems,
    inventory,
    playerTotalDamage,
    claimedMilestones,
    currentVaultId,
    userGuildId,
    guildHearths,
    serverFurnaceHeat,
    serverAnvilHp,
    raidContributionScore,
  };

  // Google Sign-In & Cloud Save Integration (Strict Account vs Guest Separation)
  useEffect(() => {
    googleAuthService.initGsi(() => '');

    googleAuthService.onLogin((profile, remoteSaveData) => {
      // 1. Lưu giữ nguyên vẹn dữ liệu Chế Độ Khách hiện tại vào slot khách (độc lập tuyệt đối)
      try {
        const guestPayload = {
          ...latestGuestStateRef.current,
          lastActiveTimestamp: Date.now(),
        };
        safeStorage.setItem('phatroi_guest_save', JSON.stringify(guestPayload));
      } catch {}"""

old_dep = """    });
  }, [appendCombatLog, bossHp, linhThach, tinhHoa, upgrades, spiritNodes, stanceSkills, equippedItems, inventory, playerTotalDamage, claimedMilestones, currentVaultId, userGuildId, guildHearths, serverFurnaceHeat, serverAnvilHp, raidContributionScore, loadSaveData, resetToFreshCharacter]);"""

new_dep = """    });
  }, [loadSaveData, resetToFreshCharacter, appendCombatLog]);"""

if old_block in code and old_dep in code:
    code = code.replace(old_block, new_block, 1)
    code = code.replace(old_dep, new_dep, 1)
    with open('frontend/src/App.tsx', 'w', encoding='utf-8') as f:
        f.write(code)
    print("Fixed GSI effect successfully!")
else:
    print("Failed to find target block")
