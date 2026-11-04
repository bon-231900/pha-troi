# -*- coding: utf-8 -*-
import os

APP_PATH = r"d:\tieu-thuyet\frontend\src\App.tsx"

with open(APP_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add import
old_import = "import { serverSyncClient } from './game/serverSync';"
new_import = """import { serverSyncClient } from './game/serverSync';
import { googleAuthService, GoogleUserProfile } from './game/googleAuth';"""

if old_import in content and "googleAuthService" not in content:
    content = content.replace(old_import, new_import, 1)

# 2. Add state
old_state = "const [isServerSynced, setIsServerSynced] = useState<boolean>(false);"
new_state = """const [isServerSynced, setIsServerSynced] = useState<boolean>(false);
  const [googleUser, setGoogleUser] = useState<GoogleUserProfile | null>(() => googleAuthService.getProfile());"""

if old_state in content and "setGoogleUser" not in content:
    content = content.replace(old_state, new_state, 1)

# 3. Add Google Auth logic after resetGame
target_reset_end = """    appendCombatLog('Lò rèn tái khởi động! Vạn dân đồng loạt giáng búa vào Tầng 1!', 'gold');
  }, [appendCombatLog]);"""

google_logic = """    appendCombatLog('Lò rèn tái khởi động! Vạn dân đồng loạt giáng búa vào Tầng 1!', 'gold');
  }, [appendCombatLog]);

  // Google Sign-In & Cloud Save Integration
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

if target_reset_end in content and "handleGoogleLogin" not in content:
    content = content.replace(target_reset_end, google_logic, 1)

# 4. Pass props to TopBossHeader
old_header_props = """        isOffline={isOffline}
        isCloudflareServerOnline={isServerSynced}"""

new_header_props = """        isOffline={isOffline}
        isCloudflareServerOnline={isServerSynced}
        googleProfile={googleUser}
        onGoogleLogin={handleGoogleLogin}
        onGoogleLogout={handleGoogleLogout}"""

if old_header_props in content and "googleProfile=" not in content:
    content = content.replace(old_header_props, new_header_props, 1)

with open(APP_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("Successfully patched App.tsx for Google Auth!")
