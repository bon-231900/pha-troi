# -*- coding: utf-8 -*-
import sys

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

with open('frontend/src/App.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update rules imports
old_rules = """  ForgerRank,
  FORGER_RANKS,
  getForgerRank,"""

new_rules = """  ForgerRank,
  FORGER_RANKS,
  getForgerRank,
  PlayerClassId,
  PLAYER_CLASSES,
  getPlayerClass,
  OVERDRIVE_TOTAL_CAP,
  getOverdriveTier,"""

code = code.replace(old_rules, new_rules, 1)

# 2. Add Component imports
old_comp = """import { LoadingScreen } from './components/LoadingScreen';"""
new_comp = """import { LoadingScreen } from './components/LoadingScreen';
import { CharacterCreationModal } from './components/CharacterCreationModal';
import { ClassSkillBar } from './components/ClassSkillBar';"""

code = code.replace(old_comp, new_comp, 1)

# 3. Add playerClassId, showClassModal and skillCooldowns states
target_state_pos = """  const [autoSalvageTiers, setAutoSalvageTiers] = useState<{ tierE: boolean; tierD: boolean; tierC: boolean }>(() => {
    try {
      const s = getInitialSaveString();
      if (s) {
        const parsed = JSON.parse(s);
        if (parsed.autoSalvageTiers) return parsed.autoSalvageTiers;
      }
    } catch {}
    return { tierE: false, tierD: false, tierC: false };
  });"""

class_states = """  const [autoSalvageTiers, setAutoSalvageTiers] = useState<{ tierE: boolean; tierD: boolean; tierC: boolean }>(() => {
    try {
      const s = getInitialSaveString();
      if (s) {
        const parsed = JSON.parse(s);
        if (parsed.autoSalvageTiers) return parsed.autoSalvageTiers;
      }
    } catch {}
    return { tierE: false, tierD: false, tierC: false };
  });

  // Balance Patch v3.3: Single-Class Commitment & 4-Skill Kit
  const [playerClassId, setPlayerClassId] = useState<PlayerClassId | null>(() => {
    try {
      const s = getInitialSaveString();
      if (s) {
        const parsed = JSON.parse(s);
        if (parsed.playerClassId && PLAYER_CLASSES[parsed.playerClassId as PlayerClassId]) {
          return parsed.playerClassId as PlayerClassId;
        }
      }
      const savedClass = safeStorage.getItem('phatroi_player_class');
      if (savedClass && PLAYER_CLASSES[savedClass as PlayerClassId]) {
        return savedClass as PlayerClassId;
      }
    } catch {}
    return null;
  });

  const [showClassModal, setShowClassModal] = useState<boolean>(false);
  const [skillCooldowns, setSkillCooldowns] = useState<{ W: number; E: number; R: number }>({
    W: 0,
    E: 0,
    R: 0,
  });

  // Cooldown countdown timer
  useEffect(() => {
    const timer = setInterval(() => {
      setSkillCooldowns((prev) => {
        if (prev.W <= 0 && prev.E <= 0 && prev.R <= 0) return prev;
        return {
          W: Math.max(0, Number((prev.W - 0.2).toFixed(1))),
          E: Math.max(0, Number((prev.E - 0.2).toFixed(1))),
          R: Math.max(0, Number((prev.R - 0.2).toFixed(1))),
        };
      });
    }, 200);
    return () => clearInterval(timer);
  }, []);"""

code = code.replace(target_state_pos, class_states, 1)

# 4. Update loadSaveData and resetToFreshCharacter
old_load = """      if (parsed.autoSalvageTiers) setAutoSalvageTiers(parsed.autoSalvageTiers);"""
new_load = """      if (parsed.autoSalvageTiers) setAutoSalvageTiers(parsed.autoSalvageTiers);
      if (parsed.playerClassId && PLAYER_CLASSES[parsed.playerClassId as PlayerClassId]) {
        setPlayerClassId(parsed.playerClassId as PlayerClassId);
      }"""
code = code.replace(old_load, new_load, 1)

old_reset = """    setAutoSalvageTiers({ tierE: false, tierD: false, tierC: false });"""
new_reset = """    setAutoSalvageTiers({ tierE: false, tierD: false, tierC: false });
    setPlayerClassId(null);"""
code = code.replace(old_reset, new_reset, 1)

# 5. Add playerClassId to save payloads
code = code.replace("autoSalvageTiers,\n          upgrades,", "autoSalvageTiers,\n          playerClassId,\n          upgrades,")
code = code.replace("autoSalvageTiers: { tierE: false, tierD: false, tierC: false },\n          upgrades:", "autoSalvageTiers: { tierE: false, tierD: false, tierC: false },\n          playerClassId: null,\n          upgrades:")

# 6. Add handlers: handleCommitClass and handleCastClassSkill
handlers_code = """  // Balance Patch v3.3: Class Commitment & Active Class Skill Handlers
  const handleCommitClass = useCallback(
    (classId: PlayerClassId, name: string) => {
      setPlayerClassId(classId);
      safeStorage.setItem('phatroi_player_class', classId);
      safeStorage.setItem('phatroi_user_name', name);
      const cls = getPlayerClass(classId);
      setActiveStance(cls.stanceKey);
      setUserGuildId(cls.guildId);
      setShowClassModal(false);
      soundEngine.playGlobalBurstFanfare();
      appendCombatLog(`🎉 [BÁI SƯ THÀNH CÔNG] Bạn đã gia nhập [${cls.name} · ${cls.sectTitle}]! Bắt đầu tu luyện bộ chiêu thức Q W E R.`, 'gold');
    },
    [appendCombatLog]
  );

  const handleCastClassSkill = useCallback(
    (slotKey: 'W' | 'E' | 'R') => {
      const cls = getPlayerClass(playerClassId || 'thunder');
      const sk = cls.skills[slotKey];
      const totalForgeLvl = upgrades.reduce((sum, u) => sum + u.level, 0);

      if (totalForgeLvl < sk.unlockLevel) {
        appendCombatLog(`🔒 [CHƯA MỞ KHÓA] Kỹ năng [${sk.name}] yêu cầu Tổng Cấp Lò Rèn đạt Cấp ${sk.unlockLevel}!`, 'red');
        return;
      }

      if (slotKey === 'W') {
        if (skillCooldowns.W > 0) return;
        setSkillCooldowns((prev) => ({ ...prev, W: sk.cooldownSec }));

        if (cls.id === 'thunder') {
          soundEngine.playStanceSwitch('Q');
          canvasHandleRef.current?.spawnCombatText('⚡ LÔI QUANG BỘ!', 'BẢO TOÀN COMBO & XUYÊN GIÁP +20%', '#00F0FF', '#FFFFFF', true);
          appendCombatLog('⚡ [LÔI QUANG BỘ] 3 nhát gõ tiếp theo bảo toàn Combo nếu gõ trượt và chuyển 20% DEX thành Xuyên Giáp PEN!', 'cyan');
        } else if (cls.id === 'fire') {
          soundEngine.playStanceSwitch('W');
          setAnvilHeat((h) => Math.max(100, h - 150));
          setServerFurnaceHeat((sf) => Math.min(10000, sf + 100));
          canvasHandleRef.current?.spawnCombatText('🔥 THUẬT KHỐNG HỎA!', 'ĐIỀU HÒA LÒ & TRUYỀN +100°C VÀO SERVER', '#FF4D00', '#FFD700', true);
          appendCombatLog('🔥 [THUẬT KHỐNG HỎA] Hạ nhiệt đe cá nhân -150°C và bơm +100°C vào Đại Hỏa Hẩu Server!', 'gold');
        } else if (cls.id === 'gravity') {
          soundEngine.playStanceSwitch('E');
          const dmg = Math.round(basePower * 3.5);
          setBossHp((hp) => Math.max(0, hp - dmg));
          setPlayerTotalDamage((prev) => prev + dmg);
          canvasHandleRef.current?.spawnCombatText('🏔️ THÁI SƠN ÁP ĐỈNH!', `KHÓA HỒI GIÁP 4S · -${dmg} DMG`, '#A855F7', '#FFFFFF', true);
          appendCombatLog(`🏔️ [THÁI SƠN ÁP ĐỈNH] Đập nát Mái Vòm -${dmg} DMG và khóa cứng 100% tốc độ tự hồi giáp trong 4 giây!`, 'gold');
        } else if (cls.id === 'mystic') {
          soundEngine.playStanceSwitch('R');
          setServerAnvilHp((ahp) => Math.min(10000, ahp + 150));
          canvasHandleRef.current?.spawnCombatText('🎶 NGỌC BÍCH HỘ THỂ!', 'HỒI PHỤC +150 ĐỘ BỀN ĐẠI ĐE SERVER', '#10B981', '#FFFFFF', true);
          appendCombatLog('🎶 [NGỌC BÍCH HỘ THỂ] Sóng âm bao bọc xưởng rèn, hồi phục +150 Độ Bền Đại Đe Server!', 'cyan');
        }
      } else if (slotKey === 'E') {
        if (overdriveCharge < 8) {
          appendCombatLog('⚠️ Kỹ năng [E] yêu cầu tối thiểu 8 ô Overdrive!', 'red');
          return;
        }
        if (skillCooldowns.E > 0) return;
        setOverdriveCharge((prev) => Math.max(0, prev - 8));
        setSkillCooldowns((prev) => ({ ...prev, E: sk.cooldownSec }));

        if (cls.id === 'thunder') {
          soundEngine.playGlobalBurstFanfare();
          const dmg = Math.round(basePower * 6 + combo * 25);
          setBossHp((hp) => Math.max(0, hp - dmg));
          setPlayerTotalDamage((prev) => prev + dmg);
          canvasHandleRef.current?.spawnCombatText('🌩️ BÃO PLASMA CUỒNG KÍCH!', `8 LUỒNG SÉT -${dmg} DMG`, '#00F0FF', '#FFD700', true);
          appendCombatLog(`🌩️ [BÃO PLASMA CUỒNG KÍCH] Xả 8 luồng sét giáng -${dmg} DMG vào Bầu Trời!`, 'gold');
        } else if (cls.id === 'fire') {
          soundEngine.playGlobalBurstFanfare();
          const detonateDmg = Math.round(burnStacks * 150 + basePower * 3.5);
          setBossHp((hp) => Math.max(0, hp - detonateDmg));
          setPlayerTotalDamage((prev) => prev + detonateDmg);
          setBurnStacks((prev) => Math.floor(prev * 0.5));
          canvasHandleRef.current?.spawnCombatText('💥 HỎA DIỆM BÙNG PHÁT!', `KÍCH NỔ TRO TÀN: -${detonateDmg} DMG`, '#FF4D00', '#FFFFFF', true);
          appendCombatLog(`💥 [HỎA DIỆM BÙNG PHÁT] Kích nổ Tro Tàn giáng -${detonateDmg} DMG và làm mềm giáp Bầu Trời -20%!`, 'gold');
        } else if (cls.id === 'gravity') {
          soundEngine.playGlobalBurstFanfare();
          const dmg = Math.round(basePower * 7.5);
          setBossHp((hp) => Math.max(0, hp - dmg));
          setPlayerTotalDamage((prev) => prev + dmg);
          setResonanceStrikes((res) => Math.min(50, res + 20));
          canvasHandleRef.current?.spawnCombatText('🌌 ĐỊA CHẤN HƯ KHÔNG!', `-20 ĐIỂM PHÁ GIÁP · -${dmg} DMG`, '#A855F7', '#FFFFFF', true);
          appendCombatLog(`🌌 [ĐỊA CHẤN HƯ KHÔNG] Không gian nứt vỡ! Trừ thẳng -20 nhát Phá Giáp và giáng -${dmg} DMG!`, 'gold');
        } else if (cls.id === 'mystic') {
          soundEngine.playGlobalBurstFanfare();
          setOverdriveCharge((prev) => Math.min(OVERDRIVE_TOTAL_CAP, prev + 2));
          setServerAnvilHp((ahp) => Math.min(10000, ahp + 200));
          canvasHandleRef.current?.spawnCombatText('📢 TIẾNG VANG VẠN DÂN!', '+2 OD & +15% CRIT TOÀN KÊNH', '#10B981', '#FFD700', true);
          appendCombatLog('📢 [TIẾNG VANG VẠN DÂN] Năng lượng sóng âm vang vọng toàn kênh! Nạp +2 OD và tăng Crit cho toàn server!', 'cyan');
        }
      } else if (slotKey === 'R') {
        if (overdriveCharge < 16) {
          appendCombatLog('⚠️ Kỹ năng Tối Thượng [R] yêu cầu nạp đầy Overdrive Tầng 3 (16+ điểm)!', 'red');
          return;
        }
        if (skillCooldowns.R > 0) return;
        setOverdriveCharge((prev) => Math.max(0, prev - 16));
        setSkillCooldowns((prev) => ({ ...prev, R: sk.cooldownSec }));

        if (cls.id === 'thunder') {
          soundEngine.playGlobalBurstFanfare();
          const ultDmg = Math.round(basePower * 16);
          setBossHp((hp) => Math.max(0, hp - ultDmg));
          setPlayerTotalDamage((prev) => prev + ultDmg);
          canvasHandleRef.current?.spawnCombatText('👑 THIÊN LÔI GIÁNG THẾ!', `CỘT LÔI TỐI THƯỢNG -${ultDmg} DMG`, '#00F0FF', '#FFD700', true);
          appendCombatLog(`👑 [THIÊN LÔI GIÁNG THẾ] Đại chiêu thức thứ 4! Triệu hồi cột lôi xé toạc Mái Vòm -${ultDmg} DMG (khuếch đại x2.2 Raid)!`, 'gold');
        } else if (cls.id === 'fire') {
          soundEngine.playGlobalBurstFanfare();
          const ultDmg = Math.round(basePower * 15);
          setBossHp((hp) => Math.max(0, hp - ultDmg));
          setPlayerTotalDamage((prev) => prev + ultDmg);
          setServerFurnaceHeat(10000);
          canvasHandleRef.current?.spawnCombatText('☀️ HỎA NGỤC ĐỒNG QUY!', `MẶT TRỜI RỰC CHÁY: -${ultDmg} DMG`, '#FF4D00', '#FFD700', true);
          appendCombatLog(`☀️ [HỎA NGỤC ĐỒNG QUY] Đại chiêu thức thứ 4! Lò Rèn bốc cháy ngút trời, khóa cứng Đại Hỏa Hẩu 10,000°C!`, 'gold');
        } else if (cls.id === 'gravity') {
          soundEngine.playGlobalBurstFanfare();
          const mult = isShieldBroken || bossHp <= BOSS_FLOOR_1_MAX_HP * 0.3 ? 5.0 : 2.5;
          const ultDmg = Math.round(basePower * 16 * (mult / 2.5));
          setBossHp((hp) => Math.max(0, hp - ultDmg));
          setPlayerTotalDamage((prev) => prev + ultDmg);
          canvasHandleRef.current?.spawnCombatText('⚡ HƯ KHÔNG ĐOẠT MỆNH!', `TRẢM SÁT BẠO KÍCH: -${ultDmg} DMG`, '#A855F7', '#FF1A53', true);
          appendCombatLog(`⚡ [HƯ KHÔNG ĐOẠT MỆNH] Đại chiêu thức thứ 4! Đại chùy phán quyết giáng đòn kết liễu -${ultDmg} DMG!`, 'gold');
        } else if (cls.id === 'mystic') {
          soundEngine.playGlobalBurstFanfare();
          const ultDmg = Math.round(basePower * 12);
          setBossHp((hp) => Math.max(0, hp - ultDmg));
          setPlayerTotalDamage((prev) => prev + ultDmg);
          setShieldBreakTimeLeft((prev) => prev + 8);
          canvasHandleRef.current?.spawnCombatText('✨ KHÚC KHẢI HOÀN BẤT DIỆT!', `KÉO DÀI VỠ GIÁP +8S · +50% MF TOÀN RAID`, '#10B981', '#FFD700', true);
          appendCombatLog('✨ [KHÚC KHẢI HOÀN BẤT DIỆT] Đại chiêu thức thứ 4! Cố định trạng thái Vỡ Giáp thêm +8 giây và tăng +50% Magic Find cho toàn Raid!', 'gold');
        }
      }
    },
    [playerClassId, upgrades, skillCooldowns, overdriveCharge, basePower, combo, burnStacks, isShieldBroken, bossHp, appendCombatLog]
  );
"""

insert_pos = "  // Claim Personal Contribution Tier Handler"
code = code.replace(insert_pos, handlers_code + "\n\n  // Claim Personal Contribution Tier Handler", 1)

# 7. Update Keydown Listener: Q strikes anvil, W/E/R cast class skills
old_keydown = """      if (e.code === 'Space') {
        e.preventDefault();
        handleHeroStrike(false);
      } else if (e.code === 'KeyQ') {
        e.preventDefault();
        handleSelectStance('Q');
      } else if (e.code === 'KeyW') {
        e.preventDefault();
        handleSelectStance('W');
      } else if (e.code === 'KeyE') {
        e.preventDefault();
        handleSelectStance('E');
      } else if (e.code === 'KeyR') {
        e.preventDefault();
        handleSelectStance('R');
      }"""

new_keydown = """      if (e.code === 'Space' || e.code === 'KeyQ') {
        e.preventDefault();
        handleHeroStrike(false);
      } else if (e.code === 'KeyW') {
        e.preventDefault();
        handleCastClassSkill('W');
      } else if (e.code === 'KeyE') {
        e.preventDefault();
        handleCastClassSkill('E');
      } else if (e.code === 'KeyR') {
        e.preventDefault();
        handleCastClassSkill('R');
      }"""

code = code.replace(old_keydown, new_keydown, 1)

with open('frontend/src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(code)

print("Part 1 of App.tsx patch completed!")
