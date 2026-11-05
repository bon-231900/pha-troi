// Release build: silhouette-live-1793696800
const APP_BUILD_VER = '20261103-multiplayer-p2p-v8';
console.log('App build version:', APP_BUILD_VER);
import React, { useState, useEffect, useRef, useCallback } from 'react';
import {
  RealtimeRoomClient,
  PeerPresence,
  RemoteStrikeMessage,
  WorldStateSyncMessage,
} from './game/realtimeRoom';
import {
  StanceKey,
  JudgmentGrade,
  INITIAL_UPGRADES,
  INITIAL_SPIRIT_NODES,
  ForgeUpgrade,
  SpiritNode,
  calculateStrikeOutcome,
  calculateBasePower,
  calculateSpiritMultiplier,
  getUpgradeCost,
  canUnlockSpiritNode,
  HAMMER_STANCES,
  OVERDRIVE_MAX,
  BOSS_FLOOR_1_MAX_HP,
  BOSS_FLOOR_NAME,
  RESONANCE_MAX_STRIKES,
  SHIELD_BREAK_DURATION_SEC,
  MIN_ANVIL_HEAT,
  MAX_ANVIL_HEAT,
  HEAT_DECAY_PER_SEC,
  AtmosphericSealLayer,
  ATMOSPHERIC_SEAL_LAYERS,
  getAtmosphericSealLayer,
  CONTRIBUTION_TIERS,
  ContributionTier,
  formatInteger,
  EquipmentItem,
  EquipmentSlotKey,
  ItemRarity,
  INITIAL_EQUIPPED_SLOTS,
  MAX_INVENTORY_SLOTS,
  getMaxInventorySlots,
  rollLootDrop,
  openWorldRaidClearChest,
  RuneGem,
  RuneType,
  RuneTier,
  RUNE_GEM_POOL,
  getTemperCost,
  temperEquipment,
  getAscensionCost,
  getUnlockedSockets,
  ascendEquipmentTier,
  getSalvageYield,
  getItemRarityMeta,
  calculateArsenalBonuses,
  checkForgeEquilibrium,
  ForgerRank,
  FORGER_RANKS,
  getForgerRank,
  PlayerClassId,
  PLAYER_CLASSES,
  getPlayerClass,
  OVERDRIVE_TOTAL_CAP,
  getOverdriveTier,
  StanceSkillNode,
  INITIAL_STANCE_SKILLS,
  canUnlockStanceSkill,
  calculateStanceSkillBonuses,
  CelestialVault,
  CELESTIAL_VAULTS,
  getCelestialVault,
  BlacksmithGuild,
  BLACKSMITH_GUILDS,
  getGuild,
  QuenchType,
  QUENCH_OPTIONS,
} from './game/rules';
import { soundEngine } from './game/audio';
import { hapticEngine } from './game/haptics';
import { safeStorage } from './game/storage';
import { TitleScreenModal } from './components/TitleScreenModal';
import { TopBossHeader } from './components/TopBossHeader';
import { LeftTacticalPanel, CombatLogEntry, ChatMessage } from './components/LeftTacticalPanel';
import { RightProgressionPanel, LeaderboardEntry } from './components/RightProgressionPanel';
import { StatusModal } from './components/StatusModal';
import { LoadingScreen } from './components/LoadingScreen';
import { CharacterCreationModal } from './components/CharacterCreationModal';
import { CharacterSelectionModal } from './components/CharacterSelectionModal';
import {
  loadCharacterSlots,
  saveAllCharacterSlots,
  getActiveSlotId,
  setActiveSlotId,
  createCharacterInSlot,
  deleteCharacterSlot,
  updateActiveSlotProgress,
  CharacterProfile,
} from './game/characterSlots';
import { ClassSkillBar } from './components/ClassSkillBar';
import { MultiplayerClient } from './game/multiplayer';
import { serverSyncClient } from './game/serverSync';
import { googleAuthService, GoogleUserProfile } from './game/googleAuth';
import {
  CommunityPanoramicForgeCanvas,
  CommunityPanoramicForgeCanvasHandle,
} from './components/CommunityPanoramicForgeCanvas';
import { LootNotificationFeed, LootToastItem } from './components/LootNotificationFeed';
import { Shield, Hammer, X, Zap, Flame, Sparkles, Eye, EyeOff } from 'lucide-react';

type GameState = 'title' | 'character_select' | 'playing' | 'paused' | 'gameover';

const INITIAL_CHAT: ChatMessage[] = [
  {
    id: 1,
    sender: 'Lôi Đế Tử Vi',
    realm: 'Tầng 9 · Đại Tông Sư',
    content: 'Vòng sóng co đến Gờ Vàng Đe là nện ngay để lấy x3.0 Hoàng Kim (+3 DMG lúc đầu) nhé anh em!',
  },
  {
    id: 2,
    sender: 'Xích Hỏa Chân Nhân',
    realm: 'Tầng 8 · Thần Chùy',
    content: 'Tích đủ 50 nhát là VỠ GIÁP 30s! Dùng Trọng Lực [E] để tích 2 điểm/nhát.',
  },
  {
    id: 3,
    sender: 'Huyền Thiết Kiếm',
    realm: 'Tầng 7 · Hộ Pháp',
    content: 'Gõ đều tay giữ Hỏa Hầu trên 600°C sát thương tăng mạnh lắm.',
  },
];

const INITIAL_RIVALS: LeaderboardEntry[] = [
  { id: 'r1', name: 'Lôi Đế Tử Vi', sect: 'Thiên Lôi Tông', damage: 48600 },
  { id: 'r2', name: 'Xích Hỏa Chân Nhân', sect: 'Phần Thiên Các', damage: 34200 },
  { id: 'r3', name: 'Huyền Thiết Kiếm', sect: 'Vạn Kiếm Sơn', damage: 19800 },
  { id: 'r4', name: 'Cửu U Mặc Khách', sect: 'Đoạn Hồn Cốc', damage: 8400 },
];

function getTimeString(): string {
  const d = new Date();
  const mins = String(d.getMinutes()).padStart(2, '0');
  const secs = String(d.getSeconds()).padStart(2, '0');
  return `${mins}:${secs}`;
}

function getInitialSaveString(): string | null {
  try {
    const storedProfileStr = safeStorage.getItem('phatroi_google_profile');
    if (storedProfileStr) {
      const prof = JSON.parse(storedProfileStr);
      if (prof?.googleId) {
        const accSave = safeStorage.getItem(`phatroi_account_${prof.googleId}`);
        if (accSave && accSave.length > 50 && accSave !== '{}') {
          return accSave;
        }
        return null;
      }
    }
    return safeStorage.getItem('phatroi_guest_save') || safeStorage.getItem('phatroi_save_v6');
  } catch {
    return null;
  }
}

export default function App() {
  const [gameState, setGameState] = useState<GameState>(() => {
    if (typeof window !== 'undefined') {
      const params = new URLSearchParams(window.location.search);
      if (params.get('autostart') === '1') {
        return 'playing';
      }
    }
    return 'title';
  });

  // Boss & Multiplayer Raid State (De-inflated RPG integer numbers)
  const [bossHp, setBossHp] = useState<number>(() => {
    try {
      const s = getInitialSaveString();
      if (s) {
        const parsed = JSON.parse(s);
        const vaultId = typeof parsed.currentVaultId === 'number' && parsed.currentVaultId >= 1 && parsed.currentVaultId <= 9 ? parsed.currentVaultId : 1;
        const vault = getCelestialVault(vaultId);
        if (typeof parsed.bossHp === 'number' && parsed.bossHp >= 10_000_000 && parsed.bossHp <= vault.maxHp) {
          return parsed.bossHp;
        }
        return vault.maxHp;
      }
    } catch {}
    return BOSS_FLOOR_1_MAX_HP;
  });
  const [bossTrailHp, setBossTrailHp] = useState<number>(bossHp);
  const [bossShieldPct, setBossShieldPct] = useState<number>(100.0);
  const [globalCountdownSec, setGlobalCountdownSec] = useState<number>(180);
  const [globalSynergyPct, setGlobalSynergyPct] = useState<number>(74.0);
  const [globalBurstActive, setGlobalBurstActive] = useState<boolean>(false);
  const [activeForgersCount, setActiveForgersCount] = useState<number>(520);
  const [isServerSynced, setIsServerSynced] = useState<boolean>(false);
  const [googleUser, setGoogleUser] = useState<GoogleUserProfile | null>(() => googleAuthService.getProfile());
  const [playerId] = useState<string>(() => {
    const saved = safeStorage.getItem('phatroi_user');
    if (saved) return saved;
    const created = `Tho_Ren_${Math.floor(Math.random() * 89999 + 10000)}`;
    safeStorage.setItem('phatroi_user', created);
    return created;
  });
  const [playerName, setPlayerName] = useState<string>(() => {
    const saved = safeStorage.getItem('phatroi_user_name');
    if (saved) return saved;
    return `Thợ Rèn #${playerId.slice(-4)}`;
  });
  const [activeSlotId, setActiveSlotIdState] = useState<1 | 2 | 3>(() => getActiveSlotId(googleUser?.googleId));
  const [characterSlots, setCharacterSlots] = useState<(CharacterProfile | null)[]>(() => loadCharacterSlots(googleUser?.googleId));
  const [creatingSlotId, setCreatingSlotId] = useState<(1 | 2 | 3) | null>(null);
  const pendingServerBatchRef = useRef({
    damage: 0,
    raidContribution: 0,
    shatterPoints: 0,
    furnaceCooling: 0,
    anvilRepair: 0,
  });

  // New Mechanics: Anvil Heat (Hỏa Hầu) & Phá Giáp Resonance
  const [anvilHeat, setAnvilHeat] = useState<number>(100); // 100°C - 1000°C
  const [resonanceStrikes, setResonanceStrikes] = useState<number>(0); // 0 - 50 strikes
  const [isShieldBroken, setIsShieldBroken] = useState<boolean>(false);
  const [shieldBreakTimeLeft, setShieldBreakTimeLeft] = useState<number>(0);
  const [stanceWeave, setStanceWeave] = useState<{ previousStance: StanceKey; timeLeftSec: number } | null>(null);
  const [claimedMilestones, setClaimedMilestones] = useState<string[]>(() => {
    try {
      const s = getInitialSaveString();
      if (s) {
        const parsed = JSON.parse(s);
        if (Array.isArray(parsed.claimedMilestones)) return parsed.claimedMilestones;
      }
    } catch {}
    return [];
  });

  // Player Forge & Rhythm State
  const [activeStance, setActiveStance] = useState<StanceKey>('Q');
  const [combo, setCombo] = useState<number>(0);
  const [maxCombo, setMaxCombo] = useState<number>(0);
  const [perfectCount, setPerfectCount] = useState<number>(0);
  const [overdriveCharge, setOverdriveCharge] = useState<number>(0);
  const [overdriveActive, setOverdriveActive] = useState<boolean>(false);
  const [overdriveTimeLeft, setOverdriveTimeLeft] = useState<number>(0);

  // Side Panels Collapsed State (Default closed for 100% unobstructed community panorama)
  const [leftPanelOpen, setLeftPanelOpen] = useState<boolean>(false);
  const [rightPanelOpen, setRightPanelOpen] = useState<boolean>(false);

  // Bottom-Right Corner Loot Drop Notification Feed
  const [lootToasts, setLootToasts] = useState<LootToastItem[]>([]);
  const lastBagFullToastTimeRef = useRef<number>(0);

  const addLootToast = useCallback((toast: Omit<LootToastItem, 'id' | 'timestamp'>) => {
    const id = `loot_${Date.now()}_${Math.random().toString(36).substring(2, 6)}`;
    setLootToasts((prev) => [
      { ...toast, id, timestamp: Date.now() },
      ...prev.slice(0, 3), // max 4 toasts
    ]);
  }, []);

  const dismissLootToast = useCallback((id: string) => {
    setLootToasts((prev) => prev.filter((t) => t.id !== id));
  }, []);

  // Bottom HUD Visibility State (Can be toggled via H or button)
  const [hudVisible, setHudVisible] = useState<boolean>(() => {
    try {
      const saved = safeStorage.getItem('phatroi_hud_visible');
      if (saved !== null) return saved === 'true';
    } catch {}
    return true;
  });

  const toggleHudVisibility = useCallback(() => {
    setHudVisible((prev) => {
      const next = !prev;
      safeStorage.setItem('phatroi_hud_visible', String(next));
      return next;
    });
  }, []);

  // Network & Loading State
  const [isOffline, setIsOffline] = useState<boolean>(true);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  // Resources & Progression: Starting at 0 LT per design spec
  const [linhThach, setLinhThach] = useState<number>(() => {
    try {
      const s = getInitialSaveString();
      if (s) {
        const parsed = JSON.parse(s);
        if (typeof parsed.linhThach === 'number') return parsed.linhThach;
      }
    } catch {}
    return 0; // Starts at 0 LT!
  });
  const [tinhHoa, setTinhHoa] = useState<number>(() => {
    try {
      const s = getInitialSaveString();
      if (s) {
        const parsed = JSON.parse(s);
        if (typeof parsed.tinhHoa === 'number') return parsed.tinhHoa;
      }
    } catch {}
    return 0; // Starts at 0 Tinh Hoa!
  });
  const [ironDust, setIronDust] = useState<number>(() => {
    try {
      const s = getInitialSaveString();
      if (s) {
        const parsed = JSON.parse(s);
        if (typeof parsed.ironDust === 'number') return parsed.ironDust;
      }
    } catch {}
    return 0;
  });
  const [celestialStars, setCelestialStars] = useState<number>(() => {
    try {
      const s = getInitialSaveString();
      if (s) {
        const parsed = JSON.parse(s);
        if (typeof parsed.celestialStars === 'number') return parsed.celestialStars;
      }
    } catch {}
    return 0;
  });
  const [anvilPityCount, setAnvilPityCount] = useState<number>(() => {
    try {
      const s = getInitialSaveString();
      if (s) {
        const parsed = JSON.parse(s);
        if (typeof parsed.anvilPityCount === 'number') return parsed.anvilPityCount;
      }
    } catch {}
    return 0;
  });
  const [raidPityCount, setRaidPityCount] = useState<number>(() => {
    try {
      const s = getInitialSaveString();
      if (s) {
        const parsed = JSON.parse(s);
        if (typeof parsed.raidPityCount === 'number') return parsed.raidPityCount;
      }
    } catch {}
    return 0;
  });
  const [autoSalvageTiers, setAutoSalvageTiers] = useState<{ tierE: boolean; tierD: boolean; tierC: boolean }>(() => {
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
  }, []);
  const [upgrades, setUpgrades] = useState<ForgeUpgrade[]>(() => {
    try {
      const s = getInitialSaveString();
      if (s) {
        const parsed = JSON.parse(s);
        if (Array.isArray(parsed.upgrades)) return parsed.upgrades;
      }
    } catch {}
    return INITIAL_UPGRADES;
  });
  const [spiritNodes, setSpiritNodes] = useState<SpiritNode[]>(() => {
    try {
      const s = getInitialSaveString();
      if (s) {
        const parsed = JSON.parse(s);
        if (Array.isArray(parsed.spiritNodes)) return parsed.spiritNodes;
      }
    } catch {}
    return INITIAL_SPIRIT_NODES;
  });
  const [playerTotalDamage, setPlayerTotalDamage] = useState<number>(() => {
    try {
      const s = getInitialSaveString();
      if (s) {
        const parsed = JSON.parse(s);
        if (typeof parsed.playerTotalDamage === 'number') return parsed.playerTotalDamage;
      }
    } catch {}
    return 0;
  });

  // World Raid v3.1 Mechanics States
  const [serverFurnaceHeat, setServerFurnaceHeat] = useState<number>(() => {
    try {
      const s = getInitialSaveString();
      if (s) {
        const parsed = JSON.parse(s);
        if (typeof parsed.serverFurnaceHeat === 'number') return parsed.serverFurnaceHeat;
      }
    } catch {}
    return 1500;
  });

  const [serverAnvilHp, setServerAnvilHp] = useState<number>(() => {
    try {
      const s = getInitialSaveString();
      if (s) {
        const parsed = JSON.parse(s);
        if (typeof parsed.serverAnvilHp === 'number') return parsed.serverAnvilHp;
      }
    } catch {}
    return 10000;
  });

  const [activeArmorBreakPoints, setActiveArmorBreakPoints] = useState<number>(0);
  const [armorRegenFrozenTime, setArmorRegenFrozenTime] = useState<number>(0);

  const [raidContributionScore, setRaidContributionScore] = useState<number>(() => {
    try {
      const s = getInitialSaveString();
      if (s) {
        const parsed = JSON.parse(s);
        if (typeof parsed.raidContributionScore === 'number') return parsed.raidContributionScore;
      }
    } catch {}
    return 0;
  });

  const [phaseCheckActive, setPhaseCheckActive] = useState<boolean>(false);
  const [phaseCheckTimeLeft, setPhaseCheckTimeLeft] = useState<number>(0);
  const triggeredPhaseChecksRef = useRef<Record<string, boolean>>({});
  const anvilStrikeTickCounterRef = useRef<number>(0);
  const hasReceivedInitialSyncRef = useRef<boolean>(false);

  // ARPG Equipment & Backpack State (Procedural Drops & Affixes)
  const [equippedItems, setEquippedItems] = useState<Record<EquipmentSlotKey, EquipmentItem | null>>(() => {
    try {
      const s = getInitialSaveString();
      if (s) {
        const parsed = JSON.parse(s);
        if (parsed.equippedItems && typeof parsed.equippedItems === 'object') {
          return parsed.equippedItems;
        }
      }
    } catch {}
    return INITIAL_EQUIPPED_SLOTS;
  });

  const [inventory, setInventory] = useState<EquipmentItem[]>(() => {
    try {
      const s = getInitialSaveString();
      if (s) {
        const parsed = JSON.parse(s);
        if (Array.isArray(parsed.inventory)) {
          return parsed.inventory;
        }
      }
    } catch {}
    return [];
  });

  // Bag of Ancient Rune Gems (Phù Thạch Khảm Nạm)
  const [runePouch, setRunePouch] = useState<RuneGem[]>(() => {
    try {
      const s = getInitialSaveString();
      if (s) {
        const parsed = JSON.parse(s);
        if (Array.isArray(parsed.runePouch)) {
          return parsed.runePouch;
        }
      }
    } catch {}
    return [];
  });

  // Phase 2: Kỹ Pháp Tứ Thế & Stance Skills Progression
  const [stanceSkills, setStanceSkills] = useState<StanceSkillNode[]>(() => {
    try {
      const s = getInitialSaveString();
      if (s) {
        const parsed = JSON.parse(s);
        if (Array.isArray(parsed.stanceSkills) && parsed.stanceSkills.length === INITIAL_STANCE_SKILLS.length) {
          return parsed.stanceSkills;
        }
      }
    } catch {}
    return INITIAL_STANCE_SKILLS;
  });

  // Viêm Dương [W] Burn DoT Stacks (0 - 80)
  const [burnStacks, setBurnStacks] = useState<number>(0);
  const goldenStreakRef = useRef<number>(0);

  // Phase 3: Cửu Trọng Thiên & Phường Rèn Vạn Dân & Đại Hỏa Lò
  const [currentVaultId, setCurrentVaultId] = useState<number>(() => {
    try {
      const s = getInitialSaveString();
      if (s) {
        const parsed = JSON.parse(s);
        if (typeof parsed.currentVaultId === 'number' && parsed.currentVaultId >= 1 && parsed.currentVaultId <= 9) {
          return parsed.currentVaultId;
        }
      }
    } catch {}
    return 1;
  });

  const latestWorldStateRef = useRef<WorldStateSyncMessage>({
    senderId: '',
    senderName: '',
    vaultId: 1,
    bossHp,
    bossTrailHp,
    serverFurnaceHeat,
    serverAnvilHp,
    activeArmorBreakPoints,
    isShieldBroken,
    shieldBreakTimeLeft,
    timestamp: Date.now(),
  });

  useEffect(() => {
    latestWorldStateRef.current = {
      senderId: '',
      senderName: '',
      vaultId: currentVaultId,
      bossHp,
      bossTrailHp,
      serverFurnaceHeat,
      serverAnvilHp,
      activeArmorBreakPoints,
      isShieldBroken,
      shieldBreakTimeLeft,
      timestamp: Date.now(),
    };
  }, [currentVaultId, bossHp, bossTrailHp, serverFurnaceHeat, serverAnvilHp, activeArmorBreakPoints, isShieldBroken, shieldBreakTimeLeft]);

  const [userGuildId, setUserGuildId] = useState<string>(() => {
    try {
      const s = getInitialSaveString();
      if (s) {
        const parsed = JSON.parse(s);
        if (typeof parsed.userGuildId === 'string' && BLACKSMITH_GUILDS.some((g) => g.id === parsed.userGuildId)) {
          return parsed.userGuildId;
        }
      }
    } catch {}
    return 'guild_thien_thai';
  });

  const [guildHearths, setGuildHearths] = useState<Record<string, { level: number; exp: number }>>(() => {
    try {
      const s = getInitialSaveString();
      if (s) {
        const parsed = JSON.parse(s);
        if (parsed.guildHearths && typeof parsed.guildHearths === 'object') {
          return parsed.guildHearths;
        }
      }
    } catch {}
    return {
      guild_thien_thai: { level: 1, exp: 0 },
      guild_phan_thien: { level: 1, exp: 0 },
      guild_van_kiem: { level: 1, exp: 0 },
      guild_doan_hon: { level: 1, exp: 0 },
    };
  });

  // UI & Feedback State
  const [lastFeedback, setLastFeedback] = useState<{
    id: number;
    grade: string;
    labelVn: string;
    multiplier: number;
    damage: number;
  } | null>(null);

  const lastMilestonePercentRef = useRef<number>(100);
  const lastSealLayerIdRef = useRef<number>(1);
  const [muted, setMuted] = useState<boolean>(false);

  // Global user interaction listener to unlock AudioContext on first tap
  useEffect(() => {
    const handleFirstGesture = () => {
      soundEngine.unlockAudio();
    };
    window.addEventListener('pointerdown', handleFirstGesture, { once: true });
    window.addEventListener('keydown', handleFirstGesture, { once: true });
    return () => {
      window.removeEventListener('pointerdown', handleFirstGesture);
      window.removeEventListener('keydown', handleFirstGesture);
    };
  }, []);

  const [combatLogs, setCombatLogs] = useState<CombatLogEntry[]>([
    {
      id: 1,
      timestamp: '00:01',
      text: 'Đại Công Trường Vạn Dân khai mở! 520 Thợ Rèn đang cùng hợp lực.',
      tone: 'gold',
    },
    {
      id: 2,
      timestamp: '00:02',
      text: 'Vòm Trời Thiết Vân giáng thế (Lớp 1: Thiết Bì · Giảm 80% DMG). Tích 50 nhát để Phá Giáp!',
      tone: 'cyan',
    },
  ]);
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>(INITIAL_CHAT);

  // Panoramic Canvas Ref
  const canvasHandleRef = useRef<CommunityPanoramicForgeCanvasHandle | null>(null);
  const feedbackCounterRef = useRef<number>(1);
  const logCounterRef = useRef<number>(10);
  const mpClientRef = useRef<MultiplayerClient | null>(null);
  const realtimeRoomRef = useRef<RealtimeRoomClient | null>(null);
  const lastHeroStrikeTimeRef = useRef<number>(0);
  const gameStateRef = useRef(gameState);
  useEffect(() => {
    gameStateRef.current = gameState;
  }, [gameState]);
  const handleHeroStrikeRef = useRef<(forceGolden?: boolean) => void>(() => {});
  const [onlinePeers, setOnlinePeers] = useState<PeerPresence[]>([]);

  const appendCombatLog = useCallback(
    (text: string, tone: CombatLogEntry['tone'] = 'neutral') => {
      logCounterRef.current += 1;
      const nextId = logCounterRef.current;
      setCombatLogs((prev) => [
        { id: nextId, timestamp: getTimeString(), text, tone },
        ...prev.slice(0, 24),
      ]);
    },
    []
  );

  // Sync document.body.dataset.state
  useEffect(() => {
    document.body.dataset.state = gameState;
  }, [gameState]);

  // Auto-save progression to safeStorage (Account vs Guest slot separation)
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
          runePouch,
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
        updateActiveSlotProgress(activeSlotId, payload, googleUser?.googleId);
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
  }, [googleUser, bossHp, linhThach, tinhHoa, upgrades, spiritNodes, stanceSkills, equippedItems, inventory, playerTotalDamage, claimedMilestones, currentVaultId, userGuildId, guildHearths, serverFurnaceHeat, serverAnvilHp, raidContributionScore]);

  // Connect to Multiplayer Gateway (Offline Fallback if server unreachable)
  useEffect(() => {
    const mp = new MultiplayerClient({
      onConnected: (districtId) => {
        setIsOffline(false);
        appendCombatLog(`Đã kết nối vào Phân Khu Vạn Dân [${districtId}]!`, 'cyan');
      },
      onDisconnected: () => {
        setIsOffline(true);
      },
      onOfflineMode: (offline) => {
        setIsOffline(offline);
      },
      onHeartbeat: (hb) => {
        if (hb.ccu) {
          setActiveForgersCount(hb.ccu);
        }
        if (hb.globalPulse) {
          if (typeof hb.globalPulse.timeRemaining === 'number') {
            setGlobalCountdownSec(Math.round(hb.globalPulse.timeRemaining));
          }
          if (typeof hb.globalPulse.perfectRatio === 'number') {
            setGlobalSynergyPct(Math.min(100, Math.round(hb.globalPulse.perfectRatio * 100)));
          }
          if (hb.globalPulse.buffActive) {
            setGlobalBurstActive(true);
          }
        }
      },
      onPeerSparks: () => {},
    });

    mp.connect();
    mpClientRef.current = mp;

    // Real-time P2P & BroadcastChannel Room for instant cross-browser and cross-device sync
    const room = new RealtimeRoomClient({
      onPeerJoined: (peer) => {
        setIsOffline(false);
        appendCombatLog(
          `⚡ [VẠN DÂN HỢP LỰC] Đồng môn [${peer.name}] vừa bước vào Đại Công Trường!`,
          'gold'
        );
        soundEngine.playComboStreakSound?.(4);
        // If we are room leader, proactively send world state to the newcomer
        if (room.isLeader()) {
          room.broadcastWorldState(latestWorldStateRef.current);
        }
      },
      onPeerLeft: (peerId) => {
        appendCombatLog('🍂 Một đồng môn vừa tạm lui về hậu phương nghỉ ngơi.', 'neutral');
      },
      onRemoteStrike: (strike) => {
        canvasHandleRef.current?.triggerRemotePeerStrike(strike);
        soundEngine.playAnvilStrike(strike.isGolden ? 'PERFECT' : 'GREAT', strike.stance, false);

        setBossHp((prev) => Math.max(0, prev - strike.damage));
        setBossTrailHp((prev) => Math.max(0, prev - strike.damage));

        appendCombatLog(`🔨 [ĐỒNG MÔN LIÊN THỦ] ${strike.name} nện búa gây -${strike.damage} DMG!`, 'cyan');
      },
      onRemoteChat: (chat) => {
        setChatMessages((prev) => [
          ...prev,
          {
            id: Date.now(),
            sender: `${chat.author}`,
            realm: chat.guildId ? (getGuild(chat.guildId)?.name || 'Vạn Dân') : 'Vạn Dân',
            content: chat.text,
            isPlayer: false,
          },
        ]);
      },
      onPeersChange: (peers) => {
        setOnlinePeers(peers);
        canvasHandleRef.current?.updateRemotePeers(peers.map((p) => ({ peerId: p.id, name: p.name, guildId: p.guildId, stance: p.stance, slotIndex: p.slotIndex })));
        setActiveForgersCount(peers.length > 0 ? peers.length + 1 : 480);
        setIsOffline(peers.length === 0);
      },
      onRequestWorldState: () => latestWorldStateRef.current,
      onWorldStateSync: (state) => {
        if (!state || typeof state.bossHp !== 'number') return;

        // Synchronize vault tier if remote peer is on another tier
        if (typeof state.vaultId === 'number' && state.vaultId >= 1 && state.vaultId <= 9) {
          setCurrentVaultId((prevVault) => (prevVault !== state.vaultId ? state.vaultId : prevVault));
        }

        // Synchronize Boss HP: snap if drift > 15 HP or on initial room sync
        setBossHp((localHp) => {
          const diff = Math.abs(localHp - state.bossHp);
          if (diff > 15 || !hasReceivedInitialSyncRef.current) {
            hasReceivedInitialSyncRef.current = true;
            setBossTrailHp(state.bossTrailHp || state.bossHp);
            return state.bossHp;
          }
          return localHp;
        });

        // Synchronize Server Furnace Heat
        if (typeof state.serverFurnaceHeat === 'number') {
          setServerFurnaceHeat((localHeat) => {
            if (Math.abs(localHeat - state.serverFurnaceHeat) > 20 || !hasReceivedInitialSyncRef.current) {
              return state.serverFurnaceHeat;
            }
            return localHeat;
          });
        }

        // Synchronize Server Anvil HP
        if (typeof state.serverAnvilHp === 'number') {
          setServerAnvilHp((localAnvil) => {
            if (Math.abs(localAnvil - state.serverAnvilHp) > 20 || !hasReceivedInitialSyncRef.current) {
              return state.serverAnvilHp;
            }
            return localAnvil;
          });
        }

        // Synchronize Active Armor Break Points
        if (typeof state.activeArmorBreakPoints === 'number') {
          setActiveArmorBreakPoints((localBreak) => {
            if (Math.abs(localBreak - state.activeArmorBreakPoints) > 5 || !hasReceivedInitialSyncRef.current) {
              return state.activeArmorBreakPoints;
            }
            return localBreak;
          });
        }

        // Synchronize Shield Break status
        if (typeof state.isShieldBroken === 'boolean') {
          setIsShieldBroken(state.isShieldBroken);
          if (typeof state.shieldBreakTimeLeft === 'number') {
            setShieldBreakTimeLeft(state.shieldBreakTimeLeft);
          }
        }
      },
    });

    realtimeRoomRef.current = room;
    room.init(userGuildId, activeStance, currentVaultId);

    // Actively request world state from any active peer on mount
    room.requestWorldState();
    const syncT1 = setTimeout(() => room.requestWorldState(), 600);
    const syncT2 = setTimeout(() => room.requestWorldState(), 1800);

    return () => {
      clearTimeout(syncT1);
      clearTimeout(syncT2);
      mp.disconnect();
      room.destroy();
    };
  }, [userGuildId, activeStance, currentVaultId, appendCombatLog]);

  // Cloudflare Worker API: Initial Global World State Fetch & Periodic Poll (10s)
  useEffect(() => {
    let isCancelled = false;

    const syncWithServer = async () => {
      try {
        const state = await serverSyncClient.fetchBossState(currentVaultId);
        if (state && !isCancelled) {
          setIsServerSynced(true);
          // Snap boss HP if drift > 20 HP or on initial load
          setBossHp((localHp) => {
            if (Math.abs(localHp - state.currentHp) > 20 || !hasReceivedInitialSyncRef.current) {
              hasReceivedInitialSyncRef.current = true;
              setBossTrailHp(state.currentHp);
              return state.currentHp;
            }
            return localHp;
          });

          if (typeof state.serverFurnaceHeat === 'number') {
            setServerFurnaceHeat((localHeat) => (Math.abs(localHeat - state.serverFurnaceHeat) > 20 ? state.serverFurnaceHeat : localHeat));
          }
          if (typeof state.serverAnvilHp === 'number') {
            setServerAnvilHp((localAnvil) => (Math.abs(localAnvil - state.serverAnvilHp) > 20 ? state.serverAnvilHp : localAnvil));
          }
          if (state.isShieldBroken !== undefined) {
            setIsShieldBroken(state.isShieldBroken);
          }
        } else if (!isCancelled) {
          setIsServerSynced(false);
        }
      } catch {
        if (!isCancelled) setIsServerSynced(false);
      }
    };

    // Immediate initial sync
    syncWithServer();

    // Periodic poll every 10 seconds for idle/background sync
    const pollTimer = setInterval(syncWithServer, 10000);

    return () => {
      isCancelled = true;
      clearInterval(pollTimer);
    };
  }, [currentVaultId]);

  // Cloudflare Worker API: 3-Second Batched Strike Flush
  useEffect(() => {
    const flushBatch = async () => {
      const batch = pendingServerBatchRef.current;
      if (batch.damage <= 0 && batch.raidContribution <= 0 && batch.shatterPoints <= 0) {
        return;
      }

      // Snapshot and reset
      const payload = {
        playerId,
        playerName,
        vaultId: currentVaultId,
        damage: batch.damage,
        raidContribution: batch.raidContribution,
        shatterPoints: batch.shatterPoints,
        furnaceCooling: batch.furnaceCooling,
        anvilRepair: batch.anvilRepair,
      };

      pendingServerBatchRef.current = {
        damage: 0,
        raidContribution: 0,
        shatterPoints: 0,
        furnaceCooling: 0,
        anvilRepair: 0,
      };

      const resState = await serverSyncClient.sendBatchedStrike(payload);
      if (resState) {
        setIsServerSynced(true);
        setBossHp((localHp) => {
          if (Math.abs(localHp - resState.currentHp) > 25) {
            setBossTrailHp(resState.currentHp);
            return resState.currentHp;
          }
          return localHp;
        });
        if (typeof resState.serverFurnaceHeat === 'number') {
          setServerFurnaceHeat((localHeat) => (Math.abs(localHeat - resState.serverFurnaceHeat) > 20 ? resState.serverFurnaceHeat : localHeat));
        }
        if (typeof resState.serverAnvilHp === 'number') {
          setServerAnvilHp((localAnvil) => (Math.abs(localAnvil - resState.serverAnvilHp) > 20 ? resState.serverAnvilHp : localAnvil));
        }
      }
    };

    const batchTimer = setInterval(flushBatch, 3000);
    return () => clearInterval(batchTimer);
  }, [playerId, playerName, currentVaultId]);

  const startGame = useCallback(() => {
    soundEngine.unlockAudio();
    soundEngine.playAnvilStrike('PERFECT', 'Q', false);
    if (document.activeElement instanceof HTMLElement) {
      document.activeElement.blur();
    }
    document.body.dataset.state = 'playing';
    setGameState('playing');
  }, []);

  const resetGame = useCallback(() => {
    if (document.activeElement instanceof HTMLElement) {
      document.activeElement.blur();
    }
    const vault = getCelestialVault(currentVaultId);
    setBossHp(vault.maxHp);
    setBossTrailHp(vault.maxHp);
    setBossShieldPct(100.0);
    setIsShieldBroken(false);
    setShieldBreakTimeLeft(0);
    setResonanceStrikes(0);
    setAnvilHeat(100);
    setActiveArmorBreakPoints(0);
    setArmorRegenFrozenTime(0);
    setServerFurnaceHeat(vault.meltingThreshold);
    setServerAnvilHp(10000);
    setPhaseCheckActive(false);
    setPhaseCheckTimeLeft(0);
    triggeredPhaseChecksRef.current = {};
    setGlobalCountdownSec(180);
    setGlobalSynergyPct(74.0);
    setGlobalBurstActive(false);
    setCombo(0);
    setOverdriveCharge(0);
    setOverdriveActive(false);
    setOverdriveTimeLeft(0);
    canvasHandleRef.current?.reset();
    document.body.dataset.state = 'playing';
    setGameState('playing');
    appendCombatLog('Lò rèn tái khởi động! Vạn dân đồng loạt giáng búa vào Tầng 1!', 'gold');
  }, [appendCombatLog]);

  // Helper to load save payload into React state
  const loadSaveData = useCallback((saveJsonStr: string) => {
    try {
      const parsed = JSON.parse(saveJsonStr);
      if (typeof parsed.linhThach === 'number') setLinhThach(parsed.linhThach);
      if (typeof parsed.tinhHoa === 'number') setTinhHoa(parsed.tinhHoa);
      if (typeof parsed.ironDust === 'number') setIronDust(parsed.ironDust);
      if (typeof parsed.celestialStars === 'number') setCelestialStars(parsed.celestialStars);
      if (typeof parsed.anvilPityCount === 'number') setAnvilPityCount(parsed.anvilPityCount);
      if (typeof parsed.raidPityCount === 'number') setRaidPityCount(parsed.raidPityCount);
      if (parsed.autoSalvageTiers) setAutoSalvageTiers(parsed.autoSalvageTiers);
      if (parsed.playerClassId && PLAYER_CLASSES[parsed.playerClassId as PlayerClassId]) {
        setPlayerClassId(parsed.playerClassId as PlayerClassId);
      }
      if (Array.isArray(parsed.upgrades)) setUpgrades(parsed.upgrades);
      if (Array.isArray(parsed.spiritNodes)) setSpiritNodes(parsed.spiritNodes);
      if (Array.isArray(parsed.stanceSkills)) setStanceSkills(parsed.stanceSkills);
      if (Array.isArray(parsed.runePouch)) setRunePouch(parsed.runePouch);
      if (parsed.equippedItems && typeof parsed.equippedItems === 'object') {
        const validatedEquipped: Record<EquipmentSlotKey, EquipmentItem> = { ...INITIAL_EQUIPPED_SLOTS };
        for (const k of Object.keys(INITIAL_EQUIPPED_SLOTS) as EquipmentSlotKey[]) {
          if (parsed.equippedItems[k]) {
            const item = parsed.equippedItems[k];
            const unlocked = getUnlockedSockets(item.rarity || 'common');
            validatedEquipped[k] = {
              ...item,
              level: typeof item.level === 'number' && item.level >= 1 ? item.level : 1,
              unlockedSockets: unlocked,
              sockets: Array.isArray(item.sockets) ? item.sockets : [],
            };
          }
        }
        setEquippedItems(validatedEquipped);
      }
      if (Array.isArray(parsed.inventory) && parsed.inventory.length > 0) {
        let extraDust = 0;
        let extraLT = 0;
        let extraTH = 0;
        for (const it of parsed.inventory) {
          const y = getSalvageYield(it);
          extraDust += y.ironDust;
          extraLT += y.linhThach;
          extraTH += y.tinhHoa;
        }
        if (extraDust > 0) setIronDust((d) => d + extraDust);
        if (extraLT > 0) setLinhThach((lt) => lt + extraLT);
        if (extraTH > 0) setTinhHoa((th) => th + extraTH);
        setInventory([]);
      }
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
    setIronDust(0);
    setCelestialStars(0);
    setAnvilPityCount(0);
    setRaidPityCount(0);
    setAutoSalvageTiers({ tierE: false, tierD: false, tierC: false });
    setPlayerClassId(null);
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

  // Helper to load a character slot profile into React state
  const loadSlotProfile = useCallback(
    (profile: CharacterProfile) => {
      setActiveSlotId(profile.slotId, googleUser?.googleId);
      setActiveSlotIdState(profile.slotId);
      setPlayerClassId(profile.classId);
      setPlayerName(profile.characterName);
      safeStorage.setItem('phatroi_user_name', profile.characterName);
      safeStorage.setItem('phatroi_player_class', profile.classId);

      const prog = profile.progress;
      if (typeof prog.bossHp === 'number' && prog.bossHp >= 10_000_000) {
        setBossHp(prog.bossHp);
      }
      setLinhThach(prog.linhThach || 0);
      setTinhHoa(prog.tinhHoa || 0);
      setUpgrades(Array.isArray(prog.upgrades) ? prog.upgrades : INITIAL_UPGRADES);
      setSpiritNodes(Array.isArray(prog.spiritNodes) ? prog.spiritNodes : INITIAL_SPIRIT_NODES);
      setStanceSkills(
        Array.isArray(prog.stanceSkills) && prog.stanceSkills.length === INITIAL_STANCE_SKILLS.length
          ? prog.stanceSkills
          : INITIAL_STANCE_SKILLS
      );
      setEquippedItems(prog.equippedItems && typeof prog.equippedItems === 'object' ? prog.equippedItems : INITIAL_EQUIPPED_SLOTS);
      setInventory(Array.isArray(prog.inventory) ? prog.inventory : []);
      setPlayerTotalDamage(prog.playerTotalDamage || 0);
      setClaimedMilestones(Array.isArray(prog.claimedMilestones) ? prog.claimedMilestones : []);
      setCurrentVaultId(typeof prog.currentVaultId === 'number' ? prog.currentVaultId : 1);
      setUserGuildId(prog.userGuildId || 'thiet_hai');

      const cls = getPlayerClass(profile.classId);
      if (cls) setActiveStance(cls.stanceKey);
    },
    [googleUser]
  );

  // Keep latest state ref to avoid re-triggering GSI init on every hammer strike
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
          ironDust: 0,
          celestialStars: 0,
          anvilPityCount: 0,
          raidPityCount: 0,
          autoSalvageTiers: { tierE: false, tierD: false, tierC: false },
          playerClassId: null,
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
  }, [loadSaveData, resetToFreshCharacter, appendCombatLog]);

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
          ironDust,
          celestialStars,
          anvilPityCount,
          raidPityCount,
          autoSalvageTiers,
          playerClassId,
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
  }, [googleUser, bossHp, linhThach, tinhHoa, upgrades, spiritNodes, stanceSkills, equippedItems, inventory, playerTotalDamage, claimedMilestones, currentVaultId, userGuildId, guildHearths, serverFurnaceHeat, serverAnvilHp, raidContributionScore, loadSaveData, resetToFreshCharacter, appendCombatLog]);

  // Periodic co-op raid loop & Simulation Tick (Runs every 500ms)
  useEffect(() => {
    if (gameState !== 'playing') return;

    const timer = setInterval(() => {
      const vault = getCelestialVault(currentVaultId);
      anvilStrikeTickCounterRef.current += 1;
      const is10sTick = anvilStrikeTickCounterRef.current % 20 === 0;

      // 1. Overdrive cooldown
      setOverdriveTimeLeft((prev) => {
        if (prev <= 0) return 0;
        const next = Math.max(0, prev - 0.5);
        if (next === 0) {
          setOverdriveActive(false);
          setOverdriveCharge(0);
        }
        return next;
      });

      // 2. Shield break countdown (30s)
      setStanceWeave((prev) => {
        if (!prev) return null;
        if (prev.timeLeftSec <= 1) return null;
        return { ...prev, timeLeftSec: prev.timeLeftSec - 1 };
      });

      setShieldBreakTimeLeft((prev) => {
        if (prev <= 0) return 0;
        const next = Math.max(0, prev - 0.5);
        if (next === 0) {
          setIsShieldBroken(false);
          setBossShieldPct(100.0);
          appendCombatLog('Vòm Trời tái lập Giáp Năng Lượng! Tiếp tục hợp lực Phá Giáp.', 'cyan');
        }
        return next;
      });

      // 2B. World Raid: Active Armor Regeneration vs Troupe Breakers
      if (!isShieldBroken) {
        setArmorRegenFrozenTime((frozenSec) => {
          if (frozenSec > 0) return Math.max(0, frozenSec - 0.5);
          const regenDecay = vault.armorRegenPerSec * 0.5;
          const breakerCount = Math.max(1, Math.round(activeForgersCount * 0.25));
          const breakerGain = breakerCount * (0.8 + Math.random() * 0.4) * 0.5;
          const netBreakGain = breakerGain - regenDecay;

          setActiveArmorBreakPoints((prev) => {
            const next = Math.max(0, Math.min(vault.armorBreakMaxPoints, prev + netBreakGain));
            if (next >= vault.armorBreakMaxPoints) {
              setIsShieldBroken(true);
              setShieldBreakTimeLeft(SHIELD_BREAK_DURATION_SEC);
              soundEngine.playGlobalBurstFanfare();
              appendCombatLog(
                `⚡ [WORLD RAID] ĐẠI CÔNG TRƯỜNG PHÁ GIÁP THÀNH CÔNG! Bầu trời ${vault.name} nứt toác, toàn server x1.5 sát thương!`,
                'gold'
              );
              return 0;
            }
            return next;
          });
          return 0;
        });
      }

      // 2B-Sync: Room Leader periodic world state broadcast (every 2.5s)
      if (anvilStrikeTickCounterRef.current % 5 === 0) {
        if (realtimeRoomRef.current?.isLeader()) {
          realtimeRoomRef.current.broadcastWorldState(latestWorldStateRef.current);
        }
      }

      // 2C. World Raid: Global Server Furnace vs Celestial Chill
      const chillDelta = vault.serverChillPerSec * 0.5;
      const melterCount = Math.max(1, Math.round(activeForgersCount * 0.25));
      const melterHeat = melterCount * (2.2 + Math.random() * 1.2) * 0.5;
      const netServerHeat = melterHeat + chillDelta;
      setServerFurnaceHeat((prev) => Math.max(0, Math.min(10000, Math.round(prev + netServerHeat))));

      // 2D. World Raid: Great Server Anvil Durability & Wipe Check
      const healerCount = Math.max(1, Math.round(activeForgersCount * 0.20));
      const healerRepair = Math.round(healerCount * (0.5 + Math.random() * 0.4) * 0.5);
      const skyAnvilStrikeDmg = is10sTick ? Math.floor(150 + Math.random() * 120) : 0;
      if (is10sTick) {
        appendCombatLog(`⚡ [THIÊN LÔI PHẠT ĐE] Bầu trời giáng sấm sét gây -${skyAnvilStrikeDmg} HP vào Đại Đe Thần!`, 'cyan');
      }

      setServerAnvilHp((prev) => {
        const next = Math.min(10000, prev + healerRepair - skyAnvilStrikeDmg);
        if (next <= 0) {
          // RAID WIPE TRIGGERED!
          setBossHp((hp) => Math.min(vault.maxHp, Math.round(hp + vault.maxHp * 0.15)));
          appendCombatLog(
            `⚠️ [RAID WIPE · THIÊN KIẾP PHẢN PHỆ] ĐẠI ĐE THẦN ĐÃ VỠ VỤN! Bầu trời hấp thu linh khí và hồi phục 15% HP!`,
            'gold'
          );
          soundEngine.playGlobalBurstFanfare();
          return 5000;
        }
        return next;
      });

      // 2E. World Raid: Phase Check (Tứ Trụ Khai Thiên) Countdown
      setPhaseCheckTimeLeft((prev) => {
        if (prev <= 0) return 0;
        const next = Math.max(0, prev - 0.5);
        if (next === 0) {
          setPhaseCheckActive(false);
          appendCombatLog(`✨ [TỨ TRỤ KHAI THIÊN] Vượt qua Thiên Đạo Phán Quyết! Toàn server nhận thưởng cống hiến!`, 'gold');
          setLinhThach((lt) => lt + 1500);
          setTinhHoa((th) => th + 8);
        }
        return next;
      });

      // 3. Anvil Heat idle cooling (-2.5°C per 500ms down to 100°C)
      setAnvilHeat((prev) => Math.max(MIN_ANVIL_HEAT, Math.round(prev - HEAT_DECAY_PER_SEC * 0.5)));

      // 3B. Viêm Dương Burn DoT tick (every 500ms)
      setBurnStacks((currentBurn) => {
        if (currentBurn <= 0) return 0;
        const burnTickDmg = Math.max(1, Math.round(currentBurn * 1.5));
        setBossHp((prevHp) => Math.max(0, prevHp - burnTickDmg));
        setPlayerTotalDamage((prevDmg) => prevDmg + burnTickDmg);
        return Math.random() < 0.25 ? currentBurn - 1 : currentBurn;
      });

      // 4. Global countdown
      setGlobalCountdownSec((prev) => (prev <= 1 ? 180 : prev - 0.5));

      // 5. Realistic Server Output Simulation:
      // 500 CCU * 30 hits/min * 8 DMG = 7.2M/hour = ~2,000 DMG/s = ~1,000 DMG per 500ms
      setBossHp((prevHp) => {
        const alliedChip = 1000 + Math.floor((Math.random() - 0.5) * 200);
        const nextHp = Math.max(0, prevHp - alliedChip);

        setBossTrailHp((prevTrail) => Math.max(nextHp, prevTrail - 1200));

        // Check Atmospheric Seal Layer transitions (75%, 50%, 25%)
        const currentSeal = getAtmosphericSealLayer(nextHp, vault.maxHp);
        if (currentSeal.id > lastSealLayerIdRef.current) {
          lastSealLayerIdRef.current = currentSeal.id;
          soundEngine.playGlobalBurstFanfare();

          // Reward all players: Thiên Hàng Vũ Lộ!
          setLinhThach((lt) => lt + 1000);
          setTinhHoa((th) => th + 5);

          appendCombatLog(
            `💥 [THIÊN HÀNG VŨ LỘ] Vòm Trời bị phá sập một tầng! Tiến vào ${currentSeal.name}! Mọi thợ rèn nhận +1,000 LT & +5 Tinh Hoa!`,
            'gold'
          );
        }

        // World Raid: Tứ Trụ Khai Thiên (Phase Checks at 75%, 50%, 25%)
        const hpRatio = nextHp / vault.maxHp;
        for (const milestone of [0.75, 0.50, 0.25]) {
          const checkKey = `${vault.id}_${milestone}`;
          if (hpRatio <= milestone && !triggeredPhaseChecksRef.current[checkKey]) {
            triggeredPhaseChecksRef.current[checkKey] = true;
            setPhaseCheckActive(true);
            setPhaseCheckTimeLeft(30);
            soundEngine.playGlobalBurstFanfare();
            appendCombatLog(
              `⚡ [TỨ TRỤ KHAI THIÊN] Vòm Trời tụt xuống ${(milestone * 100).toFixed(0)}% HP! 4 Lõi Phong Ấn khai mở trong 30 giây!`,
              'gold'
            );
          }
        }

        if (nextHp <= 0) {
          setGameState('gameover');
          soundEngine.playGlobalBurstFanfare();
        }
        return nextHp;
      });

      setGlobalSynergyPct((prevSyn) => Math.min(100, Number((prevSyn + 0.4).toFixed(1))));
      setActiveForgersCount((prevCount) =>
        Math.max(480, prevCount + Math.floor((Math.random() - 0.48) * 8))
      );
    }, 500);

    return () => clearInterval(timer);
  }, [gameState, appendCombatLog]);

  const basePower = calculateBasePower(upgrades);
  const spiritBonusMult = calculateSpiritMultiplier(spiritNodes);
  const currentVault = getCelestialVault(currentVaultId);
  const currentSeal = getAtmosphericSealLayer(bossHp, currentVault.maxHp);
  const tier2Unlocked = playerTotalDamage >= 100_000 || claimedMilestones.includes('tier_3');
  const arsenalBonuses = calculateArsenalBonuses(equippedItems, upgrades);
  const effectiveRankScore = Math.max(playerTotalDamage, raidContributionScore);
  const forgerRank = getForgerRank(effectiveRankScore);
  const currentGuild = getGuild(userGuildId);

  // Player Strike Handler
  const handleHeroStrike = useCallback(
    (forceGolden = false) => {
      soundEngine.unlockAudio();
      const currentSt = gameStateRef.current;
      if (currentSt !== 'playing') {
        if (currentSt === 'title') startGame();
        return;
      }

      // Throttle tối thiểu 100ms giữa các nhát gõ chống spam/macro quá tải đồ họa & âm thanh
      const now = performance.now();
      if (now - lastHeroStrikeTimeRef.current < 100) {
        return;
      }
      lastHeroStrikeTimeRef.current = now;

      // Rhythm judgment: true skill timing or Overdrive burst (No more 45% RNG auto-crit!)
      const isGoldenHit = forceGolden || overdriveActive || (combo >= 5 && Math.random() < 0.15);
      const grade: JudgmentGrade = isGoldenHit ? 'PERFECT' : 'GREAT';

      const effectiveRankScore = Math.max(playerTotalDamage, raidContributionScore);
  const forgerRank = getForgerRank(effectiveRankScore);
      const stanceSkillBonuses = calculateStanceSkillBonuses(stanceSkills, activeStance);

      const outcome = calculateStrikeOutcome({
        grade,
        stance: activeStance,
        basePower,
        combo,
        overdriveCharge,
        overdriveActive,
        bossShieldPct: isShieldBroken ? 0 : bossShieldPct,
        spiritBonusMult,
        globalBurstActive,
        anvilHeat,
        sealDamageReductionPct: currentSeal.damageReductionPct,
        isShieldBroken,
        arsenalBonuses,
        stanceSkillBonuses,
        forgerRankMultiplier: forgerRank.damageMultiplier,
        currentFloorId: currentVaultId,
        stanceWeave,
        serverFurnaceHeat,
        vaultMeltingThreshold: currentVault.meltingThreshold,
        isFrozenSky: serverFurnaceHeat < currentVault.meltingThreshold,
      });

      // 1. Trigger Panoramic Canvas 2D Strike Visuals
      canvasHandleRef.current?.triggerHeroStrike(isGoldenHit);

      // 2. Spawn Floating Text in Canvas (Pure Integer RPG numbers: -1 DMG, -3 DMG, -12 DMG)
      const stanceData = HAMMER_STANCES[activeStance];
      const isCritHit = outcome.isCrit;
      const isGlancingHit = outcome.isGlancingHit;

      // Dynamic, juicy combat damage fountain (replaces clunky 2-line text blocks)
      canvasHandleRef.current?.spawnCombatNumber(
        outcome.damage,
        grade,
        outcome.displayMultiplier,
        !!isCritHit,
        isGoldenHit,
        activeStance
      );

      // 3. Audio & Haptics
      soundEngine.playAnvilStrike(
        grade,
        activeStance,
        combo >= 5 || overdriveActive
      );
      hapticEngine.playStrike(outcome.isCrit, isGoldenHit);

      // 4. Update Anvil Heat (Hỏa Hầu)
      setAnvilHeat((prev) => Math.min(MAX_ANVIL_HEAT, prev + outcome.heatGain));

      // 4B. Stance W (Viêm Dương): Burn Stacks Application
      if (activeStance === 'W') {
        const addedBurn = isGoldenHit ? 2 : 1;
        setBurnStacks((prev) => Math.min(80, prev + addedBurn));
      }

      // 4C. World Raid: Update Server Furnace Heat, Anvil Repair & Frozen Regen
      if (outcome.serverHeatGain !== 0) {
        setServerFurnaceHeat((prev) => Math.max(0, Math.min(10000, prev + outcome.serverHeatGain)));
      }
      if (outcome.anvilRepairGain > 0) {
        setServerAnvilHp((prev) => Math.min(10000, prev + outcome.anvilRepairGain));
      }
      if (outcome.anvilDamage > 0) {
        setServerAnvilHp((prev) => Math.max(0, prev - outcome.anvilDamage));
      }
      if (outcome.freezeRegenSec > 0) {
        setArmorRegenFrozenTime((t) => Math.min(5, t + outcome.freezeRegenSec));
      }
      setRaidContributionScore((rcs) => rcs + outcome.raidContributionGain);

      // 4D. Accumulate into Cloudflare Worker strike batch (Batched 3s Flush)
      pendingServerBatchRef.current.damage += outcome.damage;
      pendingServerBatchRef.current.raidContribution += outcome.raidContributionGain;
      pendingServerBatchRef.current.shatterPoints += outcome.armorBreakGain;
      pendingServerBatchRef.current.furnaceCooling += outcome.serverHeatGain;
      pendingServerBatchRef.current.anvilRepair += outcome.anvilRepairGain;

      // 5. Update Phá Giáp Resonance (Active Armor Break Points)
      if (!isShieldBroken) {
        setActiveArmorBreakPoints((prev) => {
          const next = prev + outcome.armorBreakGain;
          if (next >= currentVault.armorBreakMaxPoints) {
            setIsShieldBroken(true);
            setShieldBreakTimeLeft(SHIELD_BREAK_DURATION_SEC);
            soundEngine.playGlobalBurstFanfare();
            appendCombatLog(
              `⚡ GIÁP BẦU TRỜI TAN VỠ! Toàn server dồn sát thương x1.5 trong 30 giây!`,
              'gold'
            );

            // Phase 2: Stance W Master Perk (Hỏa Ngục Đồng Quy)
            const w5Unlocked = stanceSkills.some((s) => s.id === 'w_tier_5' && s.unlocked);
            if (w5Unlocked && burnStacks > 0) {
              const detonateDmg = Math.round(burnStacks * 15 * 3);
              setBossHp((hp) => Math.max(0, hp - detonateDmg));
              setPlayerTotalDamage((dmg) => dmg + detonateDmg);
              canvasHandleRef.current?.spawnCombatText(
                '🔥 HỎA NGỤC ĐỒNG QUY! BÙNG NỔ',
                `KÍCH NỔ ${burnStacks} TẦNG LỬA: -${detonateDmg} DMG`,
                '#FF4D00',
                '#FFD700',
                true
              );
              appendCombatLog(
                `🔥 [HỎA NGỤC ĐỒNG QUY] Vỡ giáp kích nổ toàn bộ ${burnStacks} tầng lửa, giáng bạo liệt -${detonateDmg} DMG!`,
                'gold'
              );
              setBurnStacks(0);
            }

            return 0;
          }
          return next;
        });
      }

      // 6. Send strike to multiplayer gateway queue & broadcast to real-time peers
      mpClientRef.current?.recordStrike({
        stance: activeStance,
        quality: grade,
        damage: outcome.damage,
        resonance: outcome.resonanceGain,
        offsetMs: 0,
        isCrit: outcome.triggeredOverdrive || overdriveActive || isGoldenHit,
      });

      realtimeRoomRef.current?.broadcastStrike(
        outcome.damage,
        isGoldenHit,
        !!outcome.isCrit
      );

      // 7. Update Combo & Overdrive
      setCombo(outcome.nextCombo);
      setMaxCombo((prev) => Math.max(prev, outcome.nextCombo));
      if (grade === 'PERFECT') {
        setPerfectCount((prev) => prev + 1);
      }

      setOverdriveCharge(outcome.nextOverdriveCharge);
      if (outcome.triggeredOverdrive) {
        setOverdriveActive(true);
        setOverdriveTimeLeft(8.0);
        appendCombatLog(
          'LÔI ĐÌNH QUÁ TẢI 8/8! Toàn bộ Đe Thần rực sáng bão điện, Sát Thương x2.0!',
          'cyan'
        );
      }

      // 8. Resources & Damage (Linh Thạch: 1-2 on great, 5 on perfect)
      if (outcome.damage > 0) {
        setLinhThach((prev) => prev + outcome.linhThachEarned);
        if (outcome.tinhHoaEarned > 0) {
          setTinhHoa((prev) => prev + outcome.tinhHoaEarned);
          appendCombatLog('Thu được +1 Tinh Hoa Thần Hồn từ nhát búa Hoàng Kim!', 'cyan');
        }
        setPlayerTotalDamage((prev) => prev + outcome.damage);

        setGlobalSynergyPct((prevSyn) => Math.min(100, Number((prevSyn + 0.1).toFixed(1))));

        setBossHp((prevHp) => {
          const nextHp = Math.max(0, prevHp - outcome.damage);
          if (nextHp <= 0) {
            setGameState('gameover');
            soundEngine.playGlobalBurstFanfare();
          }
          return nextHp;
        });

        // 8B. Phase 2 Stance Master Perks
        // Stance Q Master Perk: Thiên Lôi Giáng Thế (15 consecutive Perfect hits triggers -500 pure DMG)
        if (activeStance === 'Q') {
          if (isGoldenHit) {
            goldenStreakRef.current += 1;
            const q5Unlocked = stanceSkills.some((s) => s.id === 'q_tier_5' && s.unlocked);
            if (goldenStreakRef.current >= 15 && q5Unlocked) {
              goldenStreakRef.current = 0;
              const pureLightningDmg = 500;
              setBossHp((hp) => Math.max(0, hp - pureLightningDmg));
              setPlayerTotalDamage((dmg) => dmg + pureLightningDmg);
              soundEngine.playGlobalBurstFanfare();
              canvasHandleRef.current?.spawnCombatText(
                '⚡ THIÊN LÔI GIÁNG THẾ! -500 DMG',
                'SẤM SÉT XUYÊN THỦNG 100% GIÁP TRỜI',
                '#00F0FF',
                '#FFFFFF',
                true
              );
              appendCombatLog(
                '⚡ [THIÊN LÔI GIÁNG THẾ] Chuỗi 15 Hoàng Kim liên tiếp! Thiên lôi giáng -500 DMG xuyên giáp trời!',
                'gold'
              );
            }
          } else {
            goldenStreakRef.current = 0;
          }
        } else {
          goldenStreakRef.current = 0;
        }

        // Stance E Master Perk: Hư Không Đoạt Mệnh (Boss HP <= 30%, 30% execute chance for x5.0)
        if (activeStance === 'E') {
          const e5Unlocked = stanceSkills.some((s) => s.id === 'e_tier_5' && s.unlocked);
          if (e5Unlocked && bossHp <= BOSS_FLOOR_1_MAX_HP * 0.3) {
            if (Math.random() < 0.3) {
              const executeBonusDmg = outcome.damage * 4;
              setBossHp((hp) => Math.max(0, hp - executeBonusDmg));
              setPlayerTotalDamage((dmg) => dmg + executeBonusDmg);
              canvasHandleRef.current?.spawnCombatText(
                '☠️ HƯ KHÔNG ĐOẠT MỆNH! x5.0',
                `TRẢM SÁT BẦU TRỜI: -${outcome.damage * 5} DMG`,
                '#A855F7',
                '#FFD700',
                true
              );
              appendCombatLog(
                `☠️ [HƯ KHÔNG ĐOẠT MỆNH] Trảm sát kích hoạt x5.0 sát thương (-${outcome.damage * 5} DMG)!`,
                'gold'
              );
            }
          }
        }

        // Phase 3: Tam Điểm Lôi Hỏa (Co-op Beat Chain with Blacksmith Guild)
        if (combo >= 6 && isGoldenHit && Math.random() < 0.25) {
          const tamDiemDmg = 1500;
          setBossHp((hp) => Math.max(0, hp - tamDiemDmg));
          setPlayerTotalDamage((dmg) => dmg + tamDiemDmg);
          soundEngine.playGlobalBurstFanfare();
          canvasHandleRef.current?.spawnCombatText(
            '💥 TAM ĐIỂM LÔI HỎA! -1,500 DMG',
            '3 ĐỒNG MÔN PHƯỜNG RÈN HỢP LỰC TRẢM THIÊN',
            '#FFD700',
            '#FF4D00',
            true
          );
          appendCombatLog(
            `💥 [TAM ĐIỂM LÔI HỎA] Vũ điệu Khai Thiên hòa nhịp! Đồng môn ${currentGuild.name} phóng 3 cột lôi hỏa giáng -1,500 DMG!`,
            'gold'
          );
        }

        // 9. Procedural ARPG Loot Drop Check with MMORPG Drop Table & Dual Pity
        const dropResult = rollLootDrop({
          grade,
          isOverdrive: outcome.triggeredOverdrive || overdriveActive,
          isShieldBreak: isShieldBroken,
          magicFindPct: arsenalBonuses.magicFindPct,
          vaultFloorId: currentVaultId,
          anvilPityCount,
        });

        if (dropResult.newPityCount !== anvilPityCount) {
          setAnvilPityCount(dropResult.newPityCount);
        }

        // 1. Regular Material Drop: Iron Dust (Bụi Thiết)
        if (dropResult.ironDustDrop && dropResult.ironDustDrop > 0) {
          const dust = dropResult.ironDustDrop;
          setIronDust((d) => d + dust);
          appendCombatLog(`⚙️ Thu nhặt +${dust} Bụi Thiết từ tàn dư đe thép!`, 'cyan');
        }

        // 2. Super Rare Material: Tinh Hoa Thần Hồn
        if (dropResult.tinhHoaDrop && dropResult.tinhHoaDrop > 0) {
          const th = dropResult.tinhHoaDrop;
          setTinhHoa((prev) => prev + th);
          addLootToast({
            type: 'tinhHoa',
            tinhHoaAmount: th,
          });
          soundEngine.playGlobalBurstFanfare();
          appendCombatLog(`✨ [THIÊN ĐỊA TINH HOA] Nhát búa Hoàng Kim ngưng tụ +${th} Tinh Hoa Thần Hồn!`, 'gold');
        }

        // 3. Truly Rare Rune Gem Drop (Phù Thạch Khảm Nạm)
        if (dropResult.gemDrop) {
          const gem = dropResult.gemDrop;
          setRunePouch((prev) => [gem, ...prev]);
          addLootToast({
            type: 'gem',
            gem,
          });
          soundEngine.playGlobalBurstFanfare();
          appendCombatLog(`💎 [THẦN KHÍ KHẢM BẢO] Chấn động rớt xuống Phù Thạch: [${gem.name}] (${gem.statLabel})!`, 'gold');
        }
      }

      feedbackCounterRef.current += 1;
      setLastFeedback({
        id: feedbackCounterRef.current,
        grade,
        labelVn: isCritHit ? 'BẠO KÍCH' : isGoldenHit ? 'HOÀNG KIM' : 'CHUẨN XÁC',
        multiplier: outcome.displayMultiplier,
        damage: outcome.damage,
      });

      if (isGlancingHit) {
        appendCombatLog(
          `⚠️ [DỘI BÚA] Lực Chùy quá cao so với Nhiệt Lò (${arsenalBonuses.coreStats.str} > 2.5x ${arsenalBonuses.coreStats.int})! Sát thương giảm 35%!`,
          'red'
        );
      } else if (isCritHit) {
        appendCombatLog(
          `⚡ [BẠO KÍCH BAO TAY] [${activeStance}] giáng -${outcome.damage} DMG! (+${outcome.linhThachEarned} LT)`,
          'cyan'
        );
      } else if (isGoldenHit) {
        appendCombatLog(
          `Nhịp Hoàng Kim [${activeStance}]! Giáng -${outcome.damage} DMG (+${outcome.linhThachEarned} LT)`,
          'gold'
        );
      } else {
        appendCombatLog(
          `Nhịp Chuẩn Xác [${activeStance}]! Giáng -${outcome.damage} DMG (+${outcome.linhThachEarned} LT)`,
          'neutral'
        );
      }
    },
    [
      gameState,
      startGame,
      activeStance,
      basePower,
      combo,
      overdriveCharge,
      overdriveActive,
      bossShieldPct,
      spiritBonusMult,
      globalBurstActive,
      anvilHeat,
      currentSeal.damageReductionPct,
      isShieldBroken,
      arsenalBonuses,
      stanceSkills,
      playerTotalDamage,
      burnStacks,
      bossHp,
      currentGuild,
      currentVault,
      appendCombatLog,
    ]
  );

  const handleSelectStance = useCallback(
    (stance: StanceKey) => {
      if (stance === activeStance) return;
      if (combo >= 4) {
        setStanceWeave({ previousStance: activeStance, timeLeftSec: 6 });
        soundEngine.playComboStreakSound?.(5);
        appendCombatLog(
          `✦ [KÍCH HOẠT CHUYỂN THẾ] Giữ lại 50% uy lực [${activeStance}] trong 6 giây!`,
          'gold'
        );
      }
      setActiveStance(stance);
      realtimeRoomRef.current?.updateIdentity(stance, userGuildId);
      soundEngine.playStanceSwitch(stance);
      appendCombatLog(
        `Chuyển thế búa: [${stance}] ${HAMMER_STANCES[stance].name} (${HAMMER_STANCES[stance].title})`,
        'cyan'
      );
    },
    [activeStance, combo, userGuildId, appendCombatLog]
  );

  const handleTriggerGlobalBurst = useCallback(() => {
    if (globalSynergyPct < 100 && !globalBurstActive) return;
    const r5Unlocked = stanceSkills.some((s) => s.id === 'r_tier_5' && s.unlocked);
    const burstDurationMs = r5Unlocked ? 23000 : 8000;
    const burstDamage = r5Unlocked ? 37500 : 25000;

    soundEngine.playGlobalBurstFanfare();
    setGlobalBurstActive(true);
    setGlobalSynergyPct(0);
    setBossHp((prev) => Math.max(0, prev - burstDamage));
    setPlayerTotalDamage((prev) => prev + burstDamage);
    setIsShieldBroken(true);
    setShieldBreakTimeLeft(r5Unlocked ? 45 : 30);
    appendCombatLog(
      r5Unlocked
        ? '🎶 [KHÚC KHẢI HOÀN] ĐẠI CỘNG HƯỞNG BÙNG NỔ! Giáng thiên lôi x1.5 (-37,500 DMG) & duy trì hào quang 23 giây!'
        : 'ĐẠI CỘNG HƯỞNG VẠN DÂN BÙNG NỔ! Giáng thiên lôi -25,000 DMG & vỡ giáp toàn vòm trời!',
      'gold'
    );
    setTimeout(() => setGlobalBurstActive(false), burstDurationMs);
  }, [globalSynergyPct, globalBurstActive, stanceSkills, appendCombatLog]);

  const handleUnlockStanceSkill = useCallback(
    (skillId: string) => {
      const rank = getForgerRank(playerTotalDamage);
      if (!canUnlockStanceSkill(skillId, stanceSkills, tinhHoa, rank.tier)) return;
      const target = stanceSkills.find((s) => s.id === skillId);
      if (!target) return;

      setTinhHoa((th) => th - target.costTinhHoa);
      setStanceSkills((prev) =>
        prev.map((s) => (s.id === skillId ? { ...s, unlocked: true } : s))
      );
      soundEngine.playGlobalBurstFanfare();
      const stanceName = HAMMER_STANCES[target.stance].name;
      appendCombatLog(
        `✨ [LĨNH HỘI KỸ PHÁP] Đã khai mở [Tầng ${target.tier}: ${target.name}] của thế [${stanceName}]!`,
        'gold'
      );
    },
    [stanceSkills, tinhHoa, playerTotalDamage, appendCombatLog]
  );

  // Phase 3: Celestial Vaults, Blacksmith Guilds & Quenching Handlers
  const handleSelectVault = useCallback(
    (vaultId: number) => {
      const v = getCelestialVault(vaultId);
      setCurrentVaultId(vaultId);
      setBossHp(v.maxHp);
      setBossTrailHp(v.maxHp);
      setBossShieldPct(100.0);
      setIsShieldBroken(false);
      setShieldBreakTimeLeft(0);
      setResonanceStrikes(0);
      soundEngine.playGlobalBurstFanfare();
      appendCombatLog(
        `🌌 [CHUYỂN VÒM TRỜI] Đã tiến vào ${v.title} (${v.name})! Trùm trấn thủ: [${v.bossName}] (${formatInteger(
          v.maxHp
        )} HP)!`,
        'cyan'
      );
    },
    [appendCombatLog]
  );

  const handleSelectGuild = useCallback(
    (guildId: string) => {
      const g = getGuild(guildId);
      setUserGuildId(guildId);
      soundEngine.playStanceSwitch(g.preferredStance);
      appendCombatLog(
        `🚩 [GIA NHẬP PHƯỜNG RÈN] Bạn đã gia nhập [${g.name}]! Nhận hào quang: ${g.auraPerk}!`,
        'gold'
      );
    },
    [appendCombatLog]
  );

  const handleDonateHearth = useCallback(
    (guildId: string, amount: number) => {
      if (linhThach < amount) return;
      setLinhThach((lt) => lt - amount);
      setGuildHearths((prev) => {
        const current = prev[guildId] || { level: 1, exp: 0 };
        const nextExp = current.exp + amount;
        const expNeeded = current.level * 1000;
        let nextLevel = current.level;
        let remainingExp = nextExp;

        if (nextExp >= expNeeded && nextLevel < 10) {
          nextLevel += 1;
          remainingExp = nextExp - expNeeded;
          soundEngine.playGlobalBurstFanfare();
          appendCombatLog(
            `🔥 [ĐẠI HỎA LÒ THĂNG CẤP] Đại Hỏa Lò Phường Rèn đã đạt CẤP ${nextLevel}! Hào quang bang hội tăng thêm!`,
            'gold'
          );
        } else {
          soundEngine.playStanceSwitch('W');
          appendCombatLog(
            `🔥 [QUYÊN GÓP HỎA LÒ] Đã đóng góp +${amount} Linh Thạch vào Đại Hỏa Lò!`,
            'cyan'
          );
        }

        return {
          ...prev,
          [guildId]: { level: nextLevel, exp: remainingExp },
        };
      });
    },
    [linhThach, appendCombatLog]
  );

  const handleQuenchItem = useCallback(
    (itemId: string, quenchType: QuenchType) => {
      if (linhThach < 150 || tinhHoa < 1) return;
      setLinhThach((lt) => lt - 150);
      setTinhHoa((th) => th - 1);

      const updateItem = (item: EquipmentItem | null) => {
        if (!item || item.id !== itemId) return item;
        return { ...item, quench: quenchType };
      };

      setEquippedItems((prev) => {
        const next = { ...prev };
        for (const key of Object.keys(next) as EquipmentSlotKey[]) {
          if (next[key]?.id === itemId) {
            next[key] = updateItem(next[key]);
          }
        }
        return next;
      });

      setInventory((prev) => prev.map((it) => (it.id === itemId ? updateItem(it)! : it)));

      soundEngine.playGlobalBurstFanfare();
      const quenchMeta = QUENCH_OPTIONS.find((q) => q.type === quenchType);
      appendCombatLog(
        `✨ [TÔI LỬA NGUYÊN TỐ] Đã tôi [${quenchMeta?.name}] cho trang bị thành công!`,
        'gold'
      );
    },
    [linhThach, tinhHoa, appendCombatLog]
  );

  const handleBuyUpgrade = useCallback(
    (upgradeId: string) => {
      const eqCheck = checkForgeEquilibrium(upgrades, upgradeId);
      if (!eqCheck.allowed) {
        soundEngine.playComboStreakSound?.(1);
        appendCombatLog(
          `🔒 ${eqCheck.reason}`,
          'red'
        );
        return;
      }

      setUpgrades((prev) =>
        prev.map((u) => {
          if (u.id !== upgradeId) return u;
          const cost = getUpgradeCost(u);
          if (linhThach < cost || u.level >= u.maxLevel) return u;
          setLinhThach((lt) => lt - cost);
          soundEngine.playStanceSwitch('E');
          appendCombatLog(`Rèn Cấp thành công: ${u.name} lên Cấp ${u.level + 1}!`, 'gold');
          return { ...u, level: u.level + 1 };
        })
      );
    },
    [linhThach, upgrades, appendCombatLog]
  );

  const handleUnlockSpiritNode = useCallback(
    (nodeId: string) => {
      if (!canUnlockSpiritNode(nodeId, spiritNodes, tinhHoa, tier2Unlocked)) return;
      const target = spiritNodes.find((n) => n.id === nodeId);
      if (!target) return;
      setTinhHoa((th) => th - target.costTinhHoa);
      setSpiritNodes((prev) =>
        prev.map((n) => (n.id === nodeId ? { ...n, unlocked: true } : n))
      );
      soundEngine.playGlobalBurstFanfare();
      appendCombatLog(
        `Khai mở Chòm Sao Thần Hồn: ${target.name} (+${Math.round(target.bonusMult * 100)}% Công Lực)!`,
        'cyan'
      );
    },
    [spiritNodes, tinhHoa, tier2Unlocked, appendCombatLog]
  );

  // ARPG Equipment & Backpack Handlers (Equip, Unequip, Salvage, Quick Salvage)
  const handleEquipItem = useCallback(
    (item: EquipmentItem) => {
      const currentEquipped = equippedItems[item.slotKey];
      setEquippedItems((prev) => ({
        ...prev,
        [item.slotKey]: item,
      }));
      setInventory((prev) => {
        const withoutItem = prev.filter((it) => it.id !== item.id);
        return currentEquipped ? [currentEquipped, ...withoutItem] : withoutItem;
      });
      soundEngine.playStanceSwitch('E');
      appendCombatLog(`⚔️ Đã trang bị: [${item.name}]!`, 'gold');
    },
    [equippedItems, appendCombatLog]
  );

  const handleUnequipItem = useCallback(
    (slotKey: EquipmentSlotKey) => {
      const item = equippedItems[slotKey];
      if (!item) return;
      if (inventory.length >= MAX_INVENTORY_SLOTS) {
        appendCombatLog('Túi đồ đã đầy, không thể tháo trang bị!', 'red');
        return;
      }
      setEquippedItems((prev) => ({
        ...prev,
        [slotKey]: null,
      }));
      setInventory((prev) => [item, ...prev]);
      soundEngine.playStanceSwitch('Q');
      appendCombatLog(`Đã tháo [${item.name}] về túi đồ.`, 'cyan');
    },
    [equippedItems, inventory.length, appendCombatLog]
  );

  const handleSalvageItem = useCallback(
    (item: EquipmentItem) => {
      const yieldReward = getSalvageYield(item);
      setLinhThach((prev) => prev + yieldReward.linhThach);
      if (yieldReward.tinhHoa > 0) {
        setTinhHoa((prev) => prev + yieldReward.tinhHoa);
      }
      if (yieldReward.ironDust > 0) {
        setIronDust((prev) => prev + yieldReward.ironDust);
      }
      if (yieldReward.celestialStar > 0) {
        setCelestialStars((prev) => prev + yieldReward.celestialStar);
      }
      if (equippedItems[item.slotKey]?.id === item.id) {
        setEquippedItems((prev) => ({
          ...prev,
          [item.slotKey]: null,
        }));
      } else {
        setInventory((prev) => prev.filter((it) => it.id !== item.id));
      }
      soundEngine.playStanceSwitch('W');
      appendCombatLog(
        `♻️ Phân giải [${item.name}]: Thu được +${yieldReward.ironDust} Bụi Thiết, +${yieldReward.linhThach} Linh Thạch${
          yieldReward.tinhHoa > 0 ? `, +${yieldReward.tinhHoa} Tinh Hoa` : ''
        }${yieldReward.celestialStar > 0 ? `, +${yieldReward.celestialStar} Thiên Tinh` : ''}!`,
        'gold'
      );
    },
    [equippedItems, appendCombatLog]
  );

  const handleQuickSalvage = useCallback(
    (rarities: ItemRarity[]) => {
      const targetItems = inventory.filter((it) => rarities.includes(it.rarity));
      if (targetItems.length === 0) return;

      let totalLT = 0;
      let totalTH = 0;
      let totalDust = 0;
      let totalStars = 0;
      targetItems.forEach((it) => {
        const r = getSalvageYield(it);
        totalLT += r.linhThach;
        totalTH += r.tinhHoa;
        totalDust += r.ironDust;
        totalStars += r.celestialStar;
      });

      setLinhThach((prev) => prev + totalLT);
      if (totalTH > 0) setTinhHoa((prev) => prev + totalTH);
      if (totalDust > 0) setIronDust((prev) => prev + totalDust);
      if (totalStars > 0) setCelestialStars((prev) => prev + totalStars);

      setInventory((prev) => prev.filter((it) => !rarities.includes(it.rarity)));
      soundEngine.playGlobalBurstFanfare();
      appendCombatLog(
        `♻️ [PHÂN GIẢI NHANH] Đã tách ${targetItems.length} món trang bị! Thu được +${totalDust} Bụi Thiết, +${totalLT.toLocaleString(
          'en-US'
        )} Linh Thạch${totalTH > 0 ? `, +${totalTH} Tinh Hoa` : ''}${totalStars > 0 ? `, +${totalStars} Thiên Tinh` : ''}!`,
        'cyan'
      );
    },
    [inventory, appendCombatLog]
  );

  const handleToggleAutoSalvage = useCallback((tierKey: 'tierE' | 'tierD' | 'tierC') => {
    setAutoSalvageTiers((prev) => ({
      ...prev,
      [tierKey]: !prev[tierKey],
    }));
  }, []);

  // =========================================================================
  // PERMANENT ARSENAL HANDLERS: TEMPERING, ASCENSION & RUNE SOCKETING
  // =========================================================================
  const handleTemperEquipment = useCallback(
    (slotKey: EquipmentSlotKey) => {
      const item = equippedItems[slotKey];
      if (!item) return;
      const currentLvl = item.level || 1;
      if (currentLvl >= 20) {
        appendCombatLog(`⚠️ [${item.name}] đã đạt cấp tối đa 20/20! Hãy thối hỏa đột phá bậc.`, 'gold');
        return;
      }
      const cost = getTemperCost(item);
      if (ironDust < cost.ironDust || linhThach < cost.linhThach) {
        appendCombatLog(
          `⚠️ Không đủ tài nguyên Tôi Luyện! Cần ${cost.ironDust} Bụi Thiết & ${cost.linhThach.toLocaleString()} Linh Thạch.`,
          'red'
        );
        return;
      }

      setIronDust((d) => d - cost.ironDust);
      setLinhThach((lt) => lt - cost.linhThach);

      const tempered = temperEquipment(item);
      setEquippedItems((prev) => ({
        ...prev,
        [slotKey]: tempered,
      }));

      soundEngine.playAnvilStrike('GREAT', activeStance, false);
      canvasHandleRef.current?.spawnCombatText(
        `CẤP ${tempered.level}!`,
        `+${tempered.baseStatValue} ${tempered.baseStatUnit}`,
        '#F59E0B',
        '#FFD700',
        true
      );
      appendCombatLog(
        `🔥 [TÔI LUYỆN] Đã rèn [${item.name}] lên Cấp ${tempered.level}/20! (${tempered.baseStatLabel}: +${tempered.baseStatValue} ${tempered.baseStatUnit})`,
        'cyan'
      );
    },
    [equippedItems, ironDust, linhThach, activeStance, appendCombatLog]
  );

  const handleAscendEquipment = useCallback(
    (slotKey: EquipmentSlotKey) => {
      const item = equippedItems[slotKey];
      if (!item) return;
      const currentLvl = item.level || 1;
      if (currentLvl < 20) {
        appendCombatLog(
          `⚠️ Cần tôi luyện [${item.name}] đạt Cấp 20 mới có thể thối hỏa đột phá bậc! (Hiện tại: Cấp ${currentLvl}/20)`,
          'red'
        );
        return;
      }
      const cost = getAscensionCost(item);
      if (!cost) {
        appendCombatLog(`⚠️ [${item.name}] đã đạt cảnh giới tối cao Thiên Đạo Thần Khí!`, 'gold');
        return;
      }
      if (ironDust < cost.ironDust || tinhHoa < cost.tinhHoa || celestialStars < cost.celestialStars) {
        appendCombatLog(
          `⚠️ Chưa đủ nguyên liệu Đột Phá Bậc: Cần ${cost.ironDust.toLocaleString()} Bụi Thiết, ${cost.tinhHoa} Tinh Hoa${
            cost.celestialStars > 0 ? `, ${cost.celestialStars} Thiên Tinh` : ''
          }!`,
          'red'
        );
        return;
      }

      setIronDust((d) => d - cost.ironDust);
      setTinhHoa((th) => th - cost.tinhHoa);
      if (cost.celestialStars > 0) {
        setCelestialStars((cs) => cs - cost.celestialStars);
      }

      const ascended = ascendEquipmentTier(item);
      if (!ascended) return;

      setEquippedItems((prev) => ({
        ...prev,
        [slotKey]: ascended,
      }));

      soundEngine.playGlobalBurstFanfare();
      canvasHandleRef.current?.spawnCombatText(
        '🌟 ĐỘT PHÁ THẦN KHÍ!',
        `${ascended.name} [${cost.targetTierName}]`,
        '#EC4899',
        '#F59E0B',
        true
      );
      appendCombatLog(
        `⚡ [THỐI HỎA ĐỘT PHÁ] Kỳ tích xuất hiện! [${item.name}] đã đột phá lên [${cost.targetTierName}] - [${ascended.name}]! Khai mở ${
          ascended.unlockedSockets || 0
        } Lỗ Khảm Phù Thạch!`,
        'gold'
      );
    },
    [equippedItems, ironDust, tinhHoa, celestialStars, appendCombatLog]
  );

  const handleSocketGem = useCallback(
    (slotKey: EquipmentSlotKey, socketIndex: number, gemId: string) => {
      const item = equippedItems[slotKey];
      if (!item) return;
      const unlocked = item.unlockedSockets || getUnlockedSockets(item.rarity);
      if (socketIndex < 0 || socketIndex >= unlocked) {
        appendCombatLog('⚠️ Lỗ khảm này chưa mở khóa! Hãy đột phá phẩm bậc trang bị.', 'red');
        return;
      }

      const gem = runePouch.find((g) => g.id === gemId);
      if (!gem) return;

      const currentSockets = [...(item.sockets || [])];
      while (currentSockets.length < unlocked) currentSockets.push(null);

      const oldGem = currentSockets[socketIndex];
      currentSockets[socketIndex] = gem;

      setEquippedItems((prev) => ({
        ...prev,
        [slotKey]: {
          ...item,
          sockets: currentSockets,
        },
      }));

      setRunePouch((prev) => {
        const remaining = prev.filter((g) => g.id !== gemId);
        return oldGem ? [oldGem, ...remaining] : remaining;
      });

      soundEngine.playStanceSwitch('Q');
      appendCombatLog(`🔮 [KHẢM NẠM] Đã khảm [${gem.name}] vào ${item.slotName}! (+${gem.value} ${gem.statLabel})`, 'cyan');
    },
    [equippedItems, runePouch, appendCombatLog]
  );

  const handleUnsocketGem = useCallback(
    (slotKey: EquipmentSlotKey, socketIndex: number) => {
      const item = equippedItems[slotKey];
      if (!item || !item.sockets || !item.sockets[socketIndex]) return;

      const removedGem = item.sockets[socketIndex]!;
      const updatedSockets = [...item.sockets];
      updatedSockets[socketIndex] = null;

      setEquippedItems((prev) => ({
        ...prev,
        [slotKey]: {
          ...item,
          sockets: updatedSockets,
        },
      }));

      setRunePouch((prev) => [removedGem, ...prev]);
      soundEngine.playStanceSwitch('E');
      appendCombatLog(`✨ [THÁO PHÙ THẠCH] Đã gỡ [${removedGem.name}] về Túi Phù Thạch an toàn.`, 'gold');
    },
    [equippedItems, appendCombatLog]
  );

  const handleAscendItem = useCallback(
    (item: EquipmentItem) => {
      if (item.rarity !== 'legendary') return;
      if (ironDust < 1000 || tinhHoa < 10 || celestialStars < 1) {
        appendCombatLog('⚠️ Không đủ nguyên liệu Thăng Bậc (Cần 1,000 Bụi Thiết, 10 Tinh Hoa, 1 Thiên Tinh)!', 'red');
        return;
      }
      setIronDust((d) => d - 1000);
      setTinhHoa((th) => th - 10);
      setCelestialStars((s) => s - 1);

      const ascended = ascendEquipmentTier(item);
      if (equippedItems[item.slotKey]?.id === item.id) {
        setEquippedItems((prev) => ({
          ...prev,
          [item.slotKey]: ascended,
        }));
      } else {
        setInventory((prev) => prev.map((it) => (it.id === item.id ? ascended : it)));
      }
      soundEngine.playGlobalBurstFanfare();
      canvasHandleRef.current?.spawnCombatText(
        '🌟 THẦN THÔNG TIER S!',
        ascended.name,
        '#FF1A53',
        '#FFD700',
        true
      );
      appendCombatLog(
        `🌟 [THĂNG BẬC THẦN KHÍ] Chúc mừng! Trang bị [${item.name}] đã đột phá lên Tier S: [${ascended.name}]!`,
        'gold'
      );
    },
    [ironDust, tinhHoa, celestialStars, equippedItems, appendCombatLog]
  );

  // Balance Patch v3.3: Class Commitment & Active Class Skill Handlers
  const handleCommitClass = useCallback(
    (classId: PlayerClassId, name: string) => {
      const targetSlot = creatingSlotId || activeSlotId;
      const newProfile = createCharacterInSlot(targetSlot, name, classId, googleUser?.googleId);
      const updatedSlots = loadCharacterSlots(googleUser?.googleId);
      setCharacterSlots(updatedSlots);
      loadSlotProfile(newProfile);
      setCreatingSlotId(null);
      setGameState('playing');
      safeStorage.setItem('phatroi_player_class', classId);
      safeStorage.setItem('phatroi_user_name', name);
      const cls = getPlayerClass(classId);
      setActiveStance(cls.stanceKey);
      setUserGuildId(cls.guildId);
      soundEngine.playGlobalBurstFanfare();
      appendCombatLog(`🎉 [BÁI SƯ THÀNH CÔNG] Bạn đã gia nhập [${cls.name} · ${cls.sectTitle}]! Bắt đầu tu luyện bộ chiêu thức Q W E R.`, 'gold');
    },
    [creatingSlotId, activeSlotId, googleUser, loadSlotProfile, appendCombatLog]
  );

  const handleSelectSlot = useCallback(
    (slotId: 1 | 2 | 3) => {
      const profile = characterSlots[slotId - 1];
      if (profile) {
        loadSlotProfile(profile);
        setGameState('playing');
        appendCombatLog(`⚔️ [XUẤT TRẬN] Tu sĩ [${profile.characterName}] đã nhập trận tại Slot #${slotId}!`, 'gold');
      } else {
        setCreatingSlotId(slotId);
      }
    },
    [characterSlots, loadSlotProfile, appendCombatLog]
  );

  const handleCreateNewInSlot = useCallback((slotId: 1 | 2 | 3) => {
    setCreatingSlotId(slotId);
  }, []);

  const handleDeleteSlot = useCallback(
    (slotId: 1 | 2 | 3) => {
      deleteCharacterSlot(slotId, googleUser?.googleId);
      const updated = loadCharacterSlots(googleUser?.googleId);
      setCharacterSlots(updated);
      appendCombatLog(`💨 [GIẢI THỂ] Đã giải thể đệ tử tại Slot #${slotId}.`, 'red');
    },
    [googleUser, appendCombatLog]
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


  // Claim Personal Contribution Tier Handler
  const handleClaimMilestone = useCallback(
    (tierId: string) => {
      const tier = CONTRIBUTION_TIERS.find((t) => t.id === tierId);
      if (!tier || claimedMilestones.includes(tierId) || playerTotalDamage < tier.damageRequired) {
        return;
      }

      setClaimedMilestones((prev) => [...prev, tierId]);
      setLinhThach((lt) => lt + tier.rewardLinhThach);
      setTinhHoa((th) => th + tier.rewardTinhHoa);
      soundEngine.playGlobalBurstFanfare();

      appendCombatLog(
        `🎉 [CỐNG HIẾN] Mở khóa Cột Mốc [${tier.title}]! Nhận +${tier.rewardLinhThach} LT, +${tier.rewardTinhHoa} Tinh Hoa!`,
        'gold'
      );
    },
    [claimedMilestones, playerTotalDamage, appendCombatLog]
  );

  const handleSendChat = useCallback((content: string) => {
    setChatMessages((prev) => [
      ...prev,
      {
        id: Date.now(),
        sender: 'Bạn · Đại Sư Rèn Đúc',
        realm: 'Cửu Trọng Thiên',
        content,
        isPlayer: true,
      },
    ]);
    realtimeRoomRef.current?.broadcastChat(content);
  }, []);

  useEffect(() => {
    handleHeroStrikeRef.current = handleHeroStrike;
  }, [handleHeroStrike]);

  useEffect(() => {
    if (gameState === 'playing') {
      window.focus();
      if (document.body) document.body.focus();
    }
  }, [gameState]);

  // Keyboard Shortcuts: Space, Q/W/E/R, P/Esc, M, [ and ]
  useEffect(() => {
    const onKeyDown = (e: KeyboardEvent) => {
      const isInput =
        e.target instanceof HTMLInputElement ||
        e.target instanceof HTMLTextAreaElement ||
        (e.target instanceof HTMLElement && e.target.isContentEditable);
      if (isInput) return;

      const isSpace =
        e.code === 'Space' ||
        e.key === ' ' ||
        e.key === 'Spacebar' ||
        e.keyCode === 32 ||
        e.which === 32;

      const isQ = e.code === 'KeyQ' || e.key === 'q' || e.key === 'Q';

      // Chống nuốt phím Space: Ngăn chặn cuộn trang & giải phóng focus khỏi nút bấm
      if (isSpace) {
        e.preventDefault();
        if (document.activeElement instanceof HTMLElement && document.activeElement !== document.body) {
          if (document.activeElement.tagName === 'BUTTON' || document.activeElement.tagName === 'A') {
            document.activeElement.blur();
          }
        }
      }

      const currentSt = gameStateRef.current;

      if (currentSt === 'title') {
        if (isSpace || e.code === 'Enter' || e.key === 'Enter') {
          e.preventDefault();
          e.stopPropagation();
          setGameState('character_select');
        }
        return;
      }

      if (currentSt === 'character_select') {
        if (isSpace || e.code === 'Enter' || e.key === 'Enter') {
          if (creatingSlotId !== null) return;
          e.preventDefault();
          e.stopPropagation();
          const targetSlot = activeSlotId || 1;
          const profile = characterSlots[targetSlot - 1];
          if (profile) {
            handleSelectSlot(targetSlot);
          } else {
            handleCreateNewInSlot(targetSlot);
          }
        }
        return;
      }

      if (e.code === 'KeyP' || e.code === 'Escape' || e.key === 'p' || e.key === 'P' || e.key === 'Escape') {
        e.preventDefault();
        setGameState((prev) =>
          prev === 'playing' ? 'paused' : prev === 'paused' ? 'playing' : prev
        );
        return;
      }

      if (e.code === 'KeyM' || e.key === 'm' || e.key === 'M') {
        e.preventDefault();
        setMuted((prev) => {
          const next = !prev;
          soundEngine.muted = next;
          return next;
        });
        return;
      }

      // Hotkeys for toggling UX/UI Side Panels
      if (e.code === 'BracketLeft') {
        e.preventDefault();
        setLeftPanelOpen((prev) => !prev);
        return;
      }
      if (e.code === 'BracketRight') {
        e.preventDefault();
        setRightPanelOpen((prev) => !prev);
        return;
      }

      if (e.code === 'KeyH' || e.key === 'h' || e.key === 'H') {
        e.preventDefault();
        toggleHudVisibility();
        return;
      }

      if (currentSt !== 'playing') return;

      if (isSpace || isQ) {
        e.preventDefault();
        e.stopPropagation();
        handleHeroStrikeRef.current(false);
      } else if (e.code === 'KeyW' || e.key === 'w' || e.key === 'W') {
        e.preventDefault();
        handleCastClassSkill('W');
      } else if (e.code === 'KeyE' || e.key === 'e' || e.key === 'E') {
        e.preventDefault();
        handleCastClassSkill('E');
      } else if (e.code === 'KeyR' || e.key === 'r' || e.key === 'R') {
        e.preventDefault();
        handleCastClassSkill('R');
      }
    };

    window.addEventListener('keydown', onKeyDown, true);
    document.addEventListener('keydown', onKeyDown, true);
    return () => {
      window.removeEventListener('keydown', onKeyDown, true);
      document.removeEventListener('keydown', onKeyDown, true);
    };
  }, [
    activeSlotId,
    characterSlots,
    creatingSlotId,
    handleSelectSlot,
    handleCreateNewInSlot,
    handleCastClassSkill,
    toggleHudVisibility,
  ]);

  const leaderboard: LeaderboardEntry[] = [
    ...INITIAL_RIVALS,
    {
      id: 'player',
      name: 'Bạn · Đại Sư Rèn Đúc',
      sect: 'Thiên Cổ Lò Rèn',
      damage: playerTotalDamage,
      isPlayer: true,
    },
  ].sort((a, b) => b.damage - a.damage);

  const stanceKeys: StanceKey[] = ['Q', 'W', 'E', 'R'];

  return (
    <div
      className="relative min-h-screen h-screen w-screen overflow-hidden bg-[#04060C] text-slate-100 select-none font-sans"
      data-stance={activeStance}
      data-overdrive={overdriveActive ? 'true' : 'false'}
      data-state={gameState}
    >
      {/* 0. Forge Atmospheric Loading Screen */}
      {isLoading && <LoadingScreen onLoaded={() => setIsLoading(false)} />}

      {/* 1. MAIN PLAYABLE SCENE: Panoramic 2D Community Canvas */}
      <div className="fixed inset-0 w-full h-full z-0 pointer-events-auto">
        <CommunityPanoramicForgeCanvas
          ref={canvasHandleRef}
          bossHp={bossHp}
          bossMaxHp={currentVault.maxHp}
          activeStance={activeStance}
          gameState={gameState}
          playerName={playerName}
          onHeroStrikeAction={() => handleHeroStrike(false)}
          onPeerAutonomousDamage={(chip) => {
            setBossHp((prev) => Math.max(0, prev - chip));
          }}
        />
      </div>

      {/* Title Screen Overlay */}
      {gameState === 'title' && (
        <TitleScreenModal
          onStart={() => setGameState('character_select')}
          googleProfile={googleUser}
          onGoogleLogin={handleGoogleLogin}
        />
      )}

      {/* Top Floating Diegetic Sky Health Header (Zero Sky Obstruction) */}
      <TopBossHeader
        bossName={`${currentVault.name} · ${currentVault.bossName}`}
        bossHp={bossHp}
        bossMaxHp={currentVault.maxHp}
        bossTrailHp={bossTrailHp}
        bossShieldPct={isShieldBroken ? 0 : bossShieldPct}
        globalCountdownSec={globalCountdownSec}
        globalSynergyPct={globalSynergyPct}
        globalBurstActive={globalBurstActive}
        activeForgersCount={activeForgersCount}
        realOnlinePeersCount={onlinePeers.length}
        isOffline={isOffline}
        isCloudflareServerOnline={isServerSynced}
        googleProfile={googleUser}
        onGoogleLogin={handleGoogleLogin}
        onGoogleLogout={handleGoogleLogout}
        anvilHeat={anvilHeat}
        resonanceStrikes={resonanceStrikes}
        isShieldBroken={isShieldBroken}
        shieldBreakTimeLeft={shieldBreakTimeLeft}
        currentSealLayer={currentSeal}
        serverFurnaceHeat={serverFurnaceHeat}
        vaultMeltingThreshold={currentVault.meltingThreshold}
        serverChillRate={currentVault.serverChillPerSec}
        serverAnvilHp={serverAnvilHp}
        serverAnvilMaxHp={10000}
        activeArmorBreakPoints={Math.round(activeArmorBreakPoints)}
        armorBreakMaxPoints={currentVault.armorBreakMaxPoints}
        armorRegenRate={currentVault.armorRegenPerSec}
        isArmorRegenFrozen={armorRegenFrozenTime > 0}
        raidContributionScore={raidContributionScore}
        phaseCheckActive={phaseCheckActive}
        phaseCheckTimeLeft={Math.ceil(phaseCheckTimeLeft)}
        muted={muted}
        onToggleMute={() => {
          setMuted((prev) => {
            const next = !prev;
            soundEngine.muted = next;
            return next;
          });
        }}
        onPause={() =>
          setGameState((prev) => (prev === 'playing' ? 'paused' : 'playing'))
        }
        onTriggerGlobalBurst={handleTriggerGlobalBurst}
        leftPanelOpen={leftPanelOpen}
        onToggleLeftPanel={() => setLeftPanelOpen((prev) => !prev)}
        rightPanelOpen={rightPanelOpen}
        onToggleRightPanel={() => setRightPanelOpen((prev) => !prev)}
        playerClass={getPlayerClass(playerClassId || 'thunder')}
        onSwitchCharacter={() => setGameState('character_select')}
      />

      {/* 3. CORNER HUD DOCKS (Positioned at corners to leave the Center Hero & Anvil 100% Unobstructed) */}
      {/* 3A. Bottom-Left Dock: 4 Class Skills Q W E R + 3-Tier Overcharge Gauge */}
      <ClassSkillBar
        playerClass={getPlayerClass(playerClassId || 'thunder')}
        overdriveCharge={overdriveCharge}
        overdriveActive={overdriveActive}
        overdriveTimeLeft={overdriveTimeLeft}
        totalForgeLevel={upgrades.reduce((sum, u) => sum + u.level, 0)}
        cooldowns={skillCooldowns}
        onCastSkill={handleCastClassSkill}
        onHeroStrike={() => handleHeroStrike(false)}
        hudVisible={hudVisible}
      />

      {/* 3B. Bottom-Right Controls: Primary Strike Trigger + Toggle HUD Button */}
      <div className="hidden sm:flex fixed bottom-3 right-3 sm:right-5 z-20 items-center gap-2 pointer-events-auto">
        {hudVisible && (
          <>
            <button
              type="button"
              onClick={() => setGameState('character_select')}
              className="px-3 py-2 sm:px-4 sm:py-2.5 rounded-xl bg-slate-900/90 hover:bg-slate-800 border border-amber-500/40 text-xs sm:text-sm font-tech font-bold text-amber-300 tracking-wider shadow-lg hover:border-amber-400 transition-all cursor-pointer active:scale-95 whitespace-nowrap flex items-center gap-1.5"
              title="Đổi Nhân Vật (3 Slots) & Vào Bệ Đá Bát Quái"
            >
              <span>⚡ ĐỔI TU SĨ (3 SLOTS)</span>
            </button>

            <button
              type="button"
              onClick={(e) => {
                (e.currentTarget as HTMLElement)?.blur();
                handleHeroStrike(false);
              }}
              onFocus={(e) => (e.currentTarget as HTMLElement)?.blur()}
              className="px-4 py-2 sm:px-5 sm:py-2.5 rounded-xl bg-gradient-to-r from-amber-500/20 via-orange-500/20 to-amber-500/20 hover:from-amber-500/30 hover:to-amber-500/30 border border-amber-500/50 text-xs sm:text-sm font-tech font-bold text-amber-300 tracking-wider shadow-lg hover:border-amber-400 transition-all cursor-pointer active:scale-95 whitespace-nowrap"
            >
              🔨 NỆN BÚA [SPACE]
            </button>
          </>
        )}

        {/* Toggle HUD Button [Phím H] */}
        <button
          type="button"
          onClick={toggleHudVisibility}
          className={`flex items-center gap-1.5 px-3 py-2 sm:py-2.5 rounded-xl backdrop-blur-md border text-xs font-tech font-bold tracking-wider cursor-pointer transition-all shadow-lg ${
            !hudVisible
              ? 'bg-amber-400 text-slate-950 border-amber-300 shadow-amber-500/25'
              : 'bg-slate-950/85 hover:bg-slate-900 border-slate-800 text-slate-300 hover:text-amber-300'
          }`}
          title={hudVisible ? 'Ẩn thanh điều khiển [Phím H]' : 'Hiện thanh điều khiển [Phím H]'}
        >
          {hudVisible ? (
            <>
              <EyeOff className="w-4 h-4 text-slate-400" />
              <span className="hidden md:inline">Ẩn HUD [H]</span>
            </>
          ) : (
            <>
              <Eye className="w-4 h-4 text-slate-950" />
              <span>Hiện HUD [H]</span>
            </>
          )}
        </button>
      </div>

      {/* 4. SLIDE-OUT DRAWER 1 (LEFT): THẾ TRẬN, CỐNG HIẾN & CHAT */}
      <div
        className={`fixed inset-y-0 left-0 z-40 w-full sm:w-[380px] md:w-[420px] bg-slate-950/95 border-r border-amber-500/30 backdrop-blur-xl shadow-2xl transform transition-transform duration-300 ease-in-out flex flex-col ${
          leftPanelOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <div className="flex items-center justify-between px-4 py-3 border-b border-slate-800 bg-slate-900/80">
          <div className="flex items-center gap-2 text-amber-300 font-tech font-bold text-sm">
            <Shield className="w-4 h-4 text-cyan-400" />
            <span>THẾ TRẬN & CỐNG HIẾN VẠN DÂN</span>
          </div>
          <button
            type="button"
            onClick={() => setLeftPanelOpen(false)}
            className="p-1 rounded-lg hover:bg-slate-800 text-slate-400 hover:text-slate-100 cursor-pointer"
          >
            <X className="w-5 h-5" />
          </button>
        </div>
        <div className="flex-1 overflow-y-auto">
          <LeftTacticalPanel
            activeStance={activeStance}
            playerTotalDamage={playerTotalDamage}
            perfectCount={perfectCount}
            maxCombo={maxCombo}
            serverDps={2000}
            claimedMilestones={claimedMilestones}
            onClaimMilestone={handleClaimMilestone}
            combatLogs={combatLogs}
            chatMessages={chatMessages}
            onSendChat={handleSendChat}
            currentVaultId={currentVaultId}
            onSelectVault={handleSelectVault}
            userGuildId={userGuildId}
            onSelectGuild={handleSelectGuild}
            guildHearths={guildHearths}
            onDonateHearth={handleDonateHearth}
            linhThach={linhThach}
          />
        </div>
      </div>

      {/* 5. SLIDE-OUT DRAWER 2 (RIGHT): NÂNG CẤP, THẦN HỒN & BẢNG VÀNG */}
      <div
        className={`fixed inset-y-0 right-0 z-40 w-full sm:w-[400px] md:w-[440px] bg-slate-950/95 border-l border-amber-500/30 backdrop-blur-xl shadow-2xl transform transition-transform duration-300 ease-in-out flex flex-col pt-safe pb-safe ${
          rightPanelOpen ? 'translate-x-0' : 'translate-x-full'
        }`}
      >
        <div className="flex items-center justify-between px-4 py-3 border-b border-slate-800 bg-slate-900/80">
          <div className="flex items-center gap-2 text-amber-300 font-tech font-bold text-sm">
            <Hammer className="w-4 h-4 text-amber-400" />
            <span>LÒ RÈN, VŨ KHÍ & KỸ PHÁP</span>
          </div>
          <button
            type="button"
            onClick={() => setRightPanelOpen(false)}
            className="p-1 rounded-lg hover:bg-slate-800 text-slate-400 hover:text-slate-100 cursor-pointer"
          >
            <X className="w-5 h-5" />
          </button>
        </div>
        <div className="flex-1 overflow-y-auto">
          <RightProgressionPanel
            equippedItems={equippedItems}
            inventory={inventory}
            upgrades={upgrades}
            spiritNodes={spiritNodes}
            stanceSkills={stanceSkills}
            forgerRank={forgerRank}
            playerTotalDamage={playerTotalDamage}
            burnStacks={burnStacks}
            linhThach={linhThach}
            tinhHoa={tinhHoa}
            ironDust={ironDust}
            celestialStars={celestialStars}
            anvilPityCount={anvilPityCount}
            raidPityCount={raidPityCount}
            autoSalvageTiers={autoSalvageTiers}
            tier2Unlocked={tier2Unlocked}
            leaderboard={leaderboard}
            mobileDrawerOpen={rightPanelOpen}
            onCloseMobileDrawer={() => setRightPanelOpen(false)}
            onBuyUpgrade={handleBuyUpgrade}
            onUnlockSpiritNode={handleUnlockSpiritNode}
            onUnlockStanceSkill={handleUnlockStanceSkill}
            onEquipItem={handleEquipItem}
            onUnequipItem={handleUnequipItem}
            onSalvageItem={handleSalvageItem}
            onQuickSalvage={handleQuickSalvage}
            onQuenchItem={handleQuenchItem}
            onAscendItem={handleAscendItem}
            onToggleAutoSalvage={handleToggleAutoSalvage}
            playerClass={getPlayerClass(playerClassId || 'thunder')}
            runePouch={runePouch}
            onTemperEquipment={handleTemperEquipment}
            onAscendEquipment={handleAscendEquipment}
            onSocketGem={handleSocketGem}
            onUnsocketGem={handleUnsocketGem}
              />
        </div>
      </div>

      {/* Modern Bottom-Right Loot Notification Stream */}
      <LootNotificationFeed
        notifications={lootToasts}
        onDismiss={dismissLootToast}
        onOpenInventory={() => setRightPanelOpen(true)}
      />

      {/* Backdrop Dimmer when either side drawer is open */}
      {(leftPanelOpen || rightPanelOpen) && (
        <div
          className="fixed inset-0 z-35 bg-black/50 backdrop-blur-[2px] transition-opacity cursor-pointer"
          onClick={() => {
            setLeftPanelOpen(false);
            setRightPanelOpen(false);
          }}
        />
      )}

      {/* Character Selection Hub (3 Slots Multi-Profile) */}
      {gameState === 'character_select' && (
        <CharacterSelectionModal
          slots={characterSlots}
          activeSlotId={activeSlotId}
          onSelectSlot={handleSelectSlot}
          onCreateNewInSlot={handleCreateNewInSlot}
          onDeleteSlot={handleDeleteSlot}
          onBackToTitle={() => setGameState('title')}
        />
      )}

      {/* Character Creation Modal when creating in a slot */}
      {creatingSlotId !== null && (
        <CharacterCreationModal
          slotId={creatingSlotId}
          currentClassId={null}
          currentName=""
          isInitialCreation={true}
          onConfirm={handleCommitClass}
          onCancel={() => setCreatingSlotId(null)}
        />
      )}

      {/* Fallback Single-Class Commitment Modal (if playing without class) */}
      {(!playerClassId && gameState === 'playing' && creatingSlotId === null) && (
        <CharacterCreationModal
          slotId={activeSlotId}
          currentClassId={playerClassId}
          currentName={playerName}
          isInitialCreation={true}
          onConfirm={handleCommitClass}
        />
      )}

      {/* Pause & Victory Status Modal */}
      {(gameState === 'paused' || gameState === 'gameover') && (
        <StatusModal
          mode={gameState}
          playerTotalDamage={playerTotalDamage}
          maxCombo={maxCombo}
          perfectCount={perfectCount}
          onResume={() => setGameState('playing')}
          onReturnTitle={() => setGameState('title')}
          onRestart={startGame}
          onSwitchCharacter={() => {
            setGameState('character_select');
          }}
        />
      )}
    </div>
  );
}
