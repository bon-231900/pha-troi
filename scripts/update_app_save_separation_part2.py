# -*- coding: utf-8 -*-
import sys

def main():
    with open('frontend/src/App.tsx', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update Auto-save to write to separated key
    old_autosave = """  // Auto-save progression to safeStorage (v6)
  useEffect(() => {
    const saveState = () => {
      try {
        const payload = {
          bossHp,
          linhThach,
          tinhHoa,
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
        safeStorage.setItem('phatroi_save_v6', JSON.stringify(payload));
      } catch {}
    };

    const timer = setInterval(saveState, 3000);
    window.addEventListener('beforeunload', saveState);
    return () => {
      clearInterval(timer);
      window.removeEventListener('beforeunload', saveState);
    };
  }, [bossHp, linhThach, tinhHoa, upgrades, spiritNodes, stanceSkills, equippedItems, inventory, playerTotalDamage, claimedMilestones, currentVaultId, userGuildId, guildHearths, serverFurnaceHeat, serverAnvilHp, raidContributionScore]);"""

    new_autosave = """  // Auto-save progression to safeStorage (Account vs Guest slot separation)
  useEffect(() => {
    const saveState = () => {
      try {
        const payload = {
          bossHp,
          linhThach,
          tinhHoa,
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
        const activeKey = googleUser ? `phatroi_account_${googleUser.googleId}` : 'phatroi_guest_save';
        safeStorage.setItem(activeKey, JSON.stringify(payload));
        // Also keep legacy key synced only if guest
        if (!googleUser) {
          safeStorage.setItem('phatroi_save_v6', JSON.stringify(payload));
        }
      } catch {}
    };

    const timer = setInterval(saveState, 3000);
    window.addEventListener('beforeunload', saveState);
    return () => {
      clearInterval(timer);
      window.removeEventListener('beforeunload', saveState);
    };
  }, [googleUser, bossHp, linhThach, tinhHoa, upgrades, spiritNodes, stanceSkills, equippedItems, inventory, playerTotalDamage, claimedMilestones, currentVaultId, userGuildId, guildHearths, serverFurnaceHeat, serverAnvilHp, raidContributionScore]);"""

    if old_autosave in content:
        content = content.replace(old_autosave, new_autosave)
        print("Updated auto-save effect.")
    else:
        print("[Warning] old_autosave not found, checking with normalize...")
        old_autosave_norm = "\n".join([line.rstrip() for line in old_autosave.splitlines()])
        content_norm = "\n".join([line.rstrip() for line in content.splitlines()])
        if old_autosave_norm in content_norm:
            content = content_norm.replace(old_autosave_norm, new_autosave)
            print("Updated auto-save effect with normalized lines.")
        else:
            print("[Error] could not find auto-save effect")

    # 2. Update Google Sign-In & Logout block
    old_auth_block = """  // Google Sign-In & Cloud Save Integration
  useEffect(() => {
    const getLocalSaveJson = () => {
      try {
        return safeStorage.getItem('phatroi_save_v6') || '{}';
      } catch {
        return '{}';
      }
    };

    googleAuthService.initGsi(getLocalSaveJson);

    googleAuthService.onLogin((profile, remoteSaveData) => {
      setGoogleUser(profile);
      appendCombatLog(`☁️ [GOOGLE CLOUD] Đăng nhập thành công tài khoản [${profile.name}]!`, 'gold');

      if (remoteSaveData && remoteSaveData.length > 50) {
        try {
          const parsed = JSON.parse(remoteSaveData);
          if (typeof parsed.linhThach === 'number') setLinhThach(parsed.linhThach);
          if (typeof parsed.tinhHoa === 'number') setTinhHoa(parsed.tinhHoa);
          if (Array.isArray(parsed.upgrades)) setUpgrades(parsed.upgrades);
          if (Array.isArray(parsed.spiritNodes)) setSpiritNodes(parsed.spiritNodes);
          if (Array.isArray(parsed.stanceSkills)) setStanceSkills(parsed.stanceSkills);
          if (parsed.equippedItems && typeof parsed.equippedItems === 'object') setEquippedItems(parsed.equippedItems);
          if (Array.isArray(parsed.inventory)) setInventory(parsed.inventory);
          if (typeof parsed.playerTotalDamage === 'number') setPlayerTotalDamage(parsed.playerTotalDamage);
          if (typeof parsed.raidContributionScore === 'number') setRaidContributionScore(parsed.raidContributionScore);
          if (typeof parsed.currentVaultId === 'number' && parsed.currentVaultId >= 1) setCurrentVaultId(parsed.currentVaultId);
          safeStorage.setItem('phatroi_save_v6', remoteSaveData);
          appendCombatLog('🎉 Đã phục hồi toàn bộ Búa, Đe & Túi đồ từ Đám mây Cloudflare D1!', 'cyan');
        } catch (e) {
          console.error('[Restore Save Error]', e);
        }
      } else {
        const localData = getLocalSaveJson();
        googleAuthService.pushCloudSave(localData);
        appendCombatLog('🛡️ Tiến độ hiện tại của bạn đã được sao lưu vĩnh viễn lên Mây!', 'cyan');
        // Auto-transition into playing if currently at title screen
        setGameState((st) => {
          if (st === 'title') {
            soundEngine.unlockAudio();
            soundEngine.playAnvilStrike('PERFECT', 'Q', false);
            document.body.dataset.state = 'playing';
            return 'playing';
          }
          return st;
        });
      }
    });
  }, [appendCombatLog]);

  // Periodic Auto Cloud Save (Every 30s when logged in)
  useEffect(() => {
    if (!googleUser) return;
    const timer = setInterval(() => {
      try {
        const saveStr = safeStorage.getItem('phatroi_save_v6');
        if (saveStr) {
          googleAuthService.pushCloudSave(saveStr);
        }
      } catch {}
    }, 30000);
    return () => clearInterval(timer);
  }, [googleUser]);

  const handleGoogleLogin = useCallback(() => {
    googleAuthService.promptLogin();
  }, []);

  const handleGoogleLogout = useCallback(() => {
    googleAuthService.logout();
    setGoogleUser(null);
    appendCombatLog('Đã đăng xuất tài khoản Google.', 'neutral');
  }, [appendCombatLog]);"""

    new_auth_block = """  // Helper to load save payload into React state
  const loadSaveData = useCallback((saveJsonStr: string) => {
    try {
      const parsed = JSON.parse(saveJsonStr);
      if (typeof parsed.linhThach === 'number') setLinhThach(parsed.linhThach);
      if (typeof parsed.tinhHoa === 'number') setTinhHoa(parsed.tinhHoa);
      if (Array.isArray(parsed.upgrades)) setUpgrades(parsed.upgrades);
      if (Array.isArray(parsed.spiritNodes)) setSpiritNodes(parsed.spiritNodes);
      if (Array.isArray(parsed.stanceSkills)) setStanceSkills(parsed.stanceSkills);
      if (parsed.equippedItems && typeof parsed.equippedItems === 'object') setEquippedItems(parsed.equippedItems);
      if (Array.isArray(parsed.inventory)) setInventory(parsed.inventory);
      if (typeof parsed.playerTotalDamage === 'number') setPlayerTotalDamage(parsed.playerTotalDamage);
      if (typeof parsed.raidContributionScore === 'number') setRaidContributionScore(parsed.raidContributionScore);
      if (typeof parsed.currentVaultId === 'number' && parsed.currentVaultId >= 1) setCurrentVaultId(parsed.currentVaultId);
      if (Array.isArray(parsed.claimedMilestones)) setClaimedMilestones(parsed.claimedMilestones);
      if (parsed.guildHearths && typeof parsed.guildHearths === 'object') setGuildHearths(parsed.guildHearths);
      if (typeof parsed.userGuildId === 'string' && BLACKSMITH_GUILDS.some((g) => g.id === parsed.userGuildId)) {
        setUserGuildId(parsed.userGuildId);
      }
    } catch (e) {
      console.error('[Load Save Error]', e);
    }
  }, []);

  // Helper to reset to fresh starting character (Level 1, empty bag, starter gear)
  const resetToFreshCharacter = useCallback(() => {
    setLinhThach(0);
    setTinhHoa(0);
    setUpgrades(INITIAL_UPGRADES);
    setSpiritNodes(INITIAL_SPIRIT_NODES);
    setStanceSkills(INITIAL_STANCE_SKILLS);
    setEquippedItems(INITIAL_EQUIPPED_SLOTS);
    setInventory([]);
    setPlayerTotalDamage(0);
    setRaidContributionScore(0);
    setCurrentVaultId(1);
    setClaimedMilestones([]);
    setGuildHearths({});
    setUserGuildId('thiet_hai');
  }, []);

  // Google Sign-In & Cloud Save Integration (Strict Account vs Guest Separation)
  useEffect(() => {
    googleAuthService.initGsi(() => '');

    googleAuthService.onLogin((profile, remoteSaveData) => {
      // 1. Lưu giữ nguyên vẹn dữ liệu Chế Độ Khách hiện tại vào slot khách (độc lập tuyệt đối)
      try {
        const guestPayload = {
          bossHp,
          linhThach,
          tinhHoa,
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
      } catch {}

      setGoogleUser(profile);

      const accountKey = `phatroi_account_${profile.googleId}`;
      const localAccountCache = safeStorage.getItem(accountKey);

      // 2. Kiểm tra dữ liệu đám mây của tài khoản Google này
      const hasCloudData = remoteSaveData && remoteSaveData.length > 50 && remoteSaveData !== '{}';
      const hasLocalAccountData = localAccountCache && localAccountCache.length > 50 && localAccountCache !== '{}';

      if (hasCloudData) {
        // Đã từng chơi trên tài khoản Google này -> nạp lại toàn bộ tiến độ của tài khoản
        loadSaveData(remoteSaveData);
        safeStorage.setItem(accountKey, remoteSaveData);
        appendCombatLog(`🎉 [TÀI KHOẢN] Đã nạp thành công tiến độ đám mây của [${profile.name}]!`, 'cyan');
      } else if (hasLocalAccountData) {
        loadSaveData(localAccountCache);
        googleAuthService.pushCloudSave(localAccountCache);
        appendCombatLog(`🎉 [TÀI KHOẢN] Đã nạp tiến độ tài khoản [${profile.name}]!`, 'cyan');
      } else {
        // Tài khoản Google mới tinh -> BẮT ĐẦU TỪ ĐẦU (Tách rời 100% với Khách)
        resetToFreshCharacter();
        const freshPayload = {
          bossHp: BOSS_FLOOR_1_MAX_HP,
          linhThach: 0,
          tinhHoa: 0,
          upgrades: INITIAL_UPGRADES,
          spiritNodes: INITIAL_SPIRIT_NODES,
          stanceSkills: INITIAL_STANCE_SKILLS,
          equippedItems: INITIAL_EQUIPPED_SLOTS,
          inventory: [],
          playerTotalDamage: 0,
          claimedMilestones: [],
          currentVaultId: 1,
          userGuildId: 'thiet_hai',
          guildHearths: {},
          serverFurnaceHeat: 0,
          serverAnvilHp: 10000,
          raidContributionScore: 0,
          lastActiveTimestamp: Date.now(),
        };
        const freshStr = JSON.stringify(freshPayload);
        safeStorage.setItem(accountKey, freshStr);
        googleAuthService.pushCloudSave(freshStr);
        appendCombatLog(`✨ [TÀI KHOẢN MỚI] Chào mừng [${profile.name}]! Đã khởi tạo nhân vật tân thủ tách biệt hoàn toàn.`, 'gold');
      }

      // Auto-transition into playing if currently at title screen
      setGameState((st) => {
        if (st === 'title') {
          soundEngine.unlockAudio();
          soundEngine.playAnvilStrike('PERFECT', 'Q', false);
          document.body.dataset.state = 'playing';
          return 'playing';
        }
        return st;
      });
    });
  }, [appendCombatLog, bossHp, linhThach, tinhHoa, upgrades, spiritNodes, stanceSkills, equippedItems, inventory, playerTotalDamage, claimedMilestones, currentVaultId, userGuildId, guildHearths, serverFurnaceHeat, serverAnvilHp, raidContributionScore, loadSaveData, resetToFreshCharacter]);

  // Periodic Auto Cloud Save (Every 30s when logged in with Google)
  useEffect(() => {
    if (!googleUser) return;
    const timer = setInterval(() => {
      try {
        const key = `phatroi_account_${googleUser.googleId}`;
        const saveStr = safeStorage.getItem(key);
        if (saveStr) {
          googleAuthService.pushCloudSave(saveStr);
        }
      } catch {}
    }, 30000);
    return () => clearInterval(timer);
  }, [googleUser]);

  const handleGoogleLogin = useCallback(() => {
    googleAuthService.promptLogin();
  }, []);

  const handleGoogleLogout = useCallback(() => {
    // Lưu lại tiến độ tài khoản Google trước khi đăng xuất
    if (googleUser) {
      try {
        const accountPayload = {
          bossHp,
          linhThach,
          tinhHoa,
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
        const str = JSON.stringify(accountPayload);
        safeStorage.setItem(`phatroi_account_${googleUser.googleId}`, str);
        googleAuthService.pushCloudSave(str);
      } catch {}
    }

    googleAuthService.logout();
    setGoogleUser(null);

    // Khôi phục lại toàn bộ dữ liệu Chế Độ Khách
    const guestSave = safeStorage.getItem('phatroi_guest_save') || safeStorage.getItem('phatroi_save_v6');
    if (guestSave) {
      loadSaveData(guestSave);
      appendCombatLog('Đã đăng xuất Google. Khôi phục lại dữ liệu nhân vật Chế Độ Khách.', 'neutral');
    } else {
      resetToFreshCharacter();
    }
    setGameState('title');
  }, [googleUser, bossHp, linhThach, tinhHoa, upgrades, spiritNodes, stanceSkills, equippedItems, inventory, playerTotalDamage, claimedMilestones, currentVaultId, userGuildId, guildHearths, serverFurnaceHeat, serverAnvilHp, raidContributionScore, loadSaveData, resetToFreshCharacter, appendCombatLog]);"""

    if old_auth_block in content:
        content = content.replace(old_auth_block, new_auth_block)
        print("Updated auth block successfully.")
    else:
        old_auth_norm = "\n".join([line.rstrip() for line in old_auth_block.splitlines()])
        content_norm = "\n".join([line.rstrip() for line in content.splitlines()])
        if old_auth_norm in content_norm:
            content = content_norm.replace(old_auth_norm, new_auth_block)
            print("Updated auth block with normalized lines.")
        else:
            print("[Error] could not find auth block")

    with open('frontend/src/App.tsx', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Part 2 finished.")

if __name__ == '__main__':
    main()
