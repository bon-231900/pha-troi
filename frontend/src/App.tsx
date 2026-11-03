import React, { useState, useEffect, useRef, useCallback } from 'react';
import {
  StanceKey,
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
  rollLootDrop,
  getSalvageYield,
  getItemRarityMeta,
  calculateArsenalBonuses,
} from './game/rules';
import { soundEngine } from './game/audio';
import { safeStorage } from './game/storage';
import { TitleScreenModal } from './components/TitleScreenModal';
import { TopBossHeader } from './components/TopBossHeader';
import { LeftTacticalPanel, CombatLogEntry, ChatMessage } from './components/LeftTacticalPanel';
import { RightProgressionPanel, LeaderboardEntry } from './components/RightProgressionPanel';
import { StatusModal } from './components/StatusModal';
import { LoadingScreen } from './components/LoadingScreen';
import { MultiplayerClient } from './game/multiplayer';
import {
  CommunityPanoramicForgeCanvas,
  CommunityPanoramicForgeCanvasHandle,
} from './components/CommunityPanoramicForgeCanvas';
import { Shield, Hammer, X, Zap, Flame, Sparkles, Eye, EyeOff } from 'lucide-react';

type GameState = 'title' | 'playing' | 'paused' | 'gameover';

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
      const s = safeStorage.getItem('phatroi_save_v6');
      if (s) {
        const parsed = JSON.parse(s);
        if (typeof parsed.bossHp === 'number' && parsed.bossHp > 0 && parsed.bossHp <= BOSS_FLOOR_1_MAX_HP) {
          return parsed.bossHp;
        }
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

  // New Mechanics: Anvil Heat (Hỏa Hầu) & Phá Giáp Resonance
  const [anvilHeat, setAnvilHeat] = useState<number>(100); // 100°C - 1000°C
  const [resonanceStrikes, setResonanceStrikes] = useState<number>(0); // 0 - 50 strikes
  const [isShieldBroken, setIsShieldBroken] = useState<boolean>(false);
  const [shieldBreakTimeLeft, setShieldBreakTimeLeft] = useState<number>(0);
  const [claimedMilestones, setClaimedMilestones] = useState<string[]>(() => {
    try {
      const s = safeStorage.getItem('phatroi_save_v6');
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
      const s = safeStorage.getItem('phatroi_save_v6');
      if (s) {
        const parsed = JSON.parse(s);
        if (typeof parsed.linhThach === 'number') return parsed.linhThach;
      }
    } catch {}
    return 0; // Starts at 0 LT!
  });
  const [tinhHoa, setTinhHoa] = useState<number>(() => {
    try {
      const s = safeStorage.getItem('phatroi_save_v6');
      if (s) {
        const parsed = JSON.parse(s);
        if (typeof parsed.tinhHoa === 'number') return parsed.tinhHoa;
      }
    } catch {}
    return 0; // Starts at 0 Tinh Hoa!
  });
  const [upgrades, setUpgrades] = useState<ForgeUpgrade[]>(() => {
    try {
      const s = safeStorage.getItem('phatroi_save_v6');
      if (s) {
        const parsed = JSON.parse(s);
        if (Array.isArray(parsed.upgrades)) return parsed.upgrades;
      }
    } catch {}
    return INITIAL_UPGRADES;
  });
  const [spiritNodes, setSpiritNodes] = useState<SpiritNode[]>(() => {
    try {
      const s = safeStorage.getItem('phatroi_save_v6');
      if (s) {
        const parsed = JSON.parse(s);
        if (Array.isArray(parsed.spiritNodes)) return parsed.spiritNodes;
      }
    } catch {}
    return INITIAL_SPIRIT_NODES;
  });
  const [playerTotalDamage, setPlayerTotalDamage] = useState<number>(() => {
    try {
      const s = safeStorage.getItem('phatroi_save_v6');
      if (s) {
        const parsed = JSON.parse(s);
        if (typeof parsed.playerTotalDamage === 'number') return parsed.playerTotalDamage;
      }
    } catch {}
    return 0;
  });

  // ARPG Equipment & Backpack State (Procedural Drops & Affixes)
  const [equippedItems, setEquippedItems] = useState<Record<EquipmentSlotKey, EquipmentItem | null>>(() => {
    try {
      const s = safeStorage.getItem('phatroi_save_v6');
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
      const s = safeStorage.getItem('phatroi_save_v6');
      if (s) {
        const parsed = JSON.parse(s);
        if (Array.isArray(parsed.inventory)) {
          return parsed.inventory;
        }
      }
    } catch {}
    return [];
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

  // Auto-save progression to safeStorage (v6)
  useEffect(() => {
    const saveState = () => {
      try {
        const payload = {
          bossHp,
          linhThach,
          tinhHoa,
          upgrades,
          spiritNodes,
          equippedItems,
          inventory,
          playerTotalDamage,
          claimedMilestones,
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
  }, [bossHp, linhThach, tinhHoa, upgrades, spiritNodes, equippedItems, inventory, playerTotalDamage, claimedMilestones]);

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

    return () => {
      mp.disconnect();
    };
  }, [appendCombatLog]);

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
    setBossHp(BOSS_FLOOR_1_MAX_HP);
    setBossTrailHp(BOSS_FLOOR_1_MAX_HP);
    setBossShieldPct(100.0);
    setIsShieldBroken(false);
    setShieldBreakTimeLeft(0);
    setResonanceStrikes(0);
    setAnvilHeat(100);
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

  // Periodic co-op raid loop & Simulation Tick (Runs every 500ms)
  useEffect(() => {
    if (gameState !== 'playing') return;

    const timer = setInterval(() => {
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
      setShieldBreakTimeLeft((prev) => {
        if (prev <= 0) return 0;
        const next = Math.max(0, prev - 0.5);
        if (next === 0) {
          setIsShieldBroken(false);
          setBossShieldPct(100.0);
          appendCombatLog('Vòm Trời tái lập Giáp Năng Lượng! Tiếp tục tích 50 nhát để Phá Giáp.', 'cyan');
        }
        return next;
      });

      // 3. Anvil Heat idle cooling (-2.5°C per 500ms down to 100°C)
      setAnvilHeat((prev) => Math.max(MIN_ANVIL_HEAT, Math.round(prev - HEAT_DECAY_PER_SEC * 0.5)));

      // 4. Global countdown
      setGlobalCountdownSec((prev) => (prev <= 1 ? 180 : prev - 0.5));

      // 5. Realistic Server Output Simulation:
      // 500 CCU * 30 hits/min * 8 DMG = 7.2M/hour = ~2,000 DMG/s = ~1,000 DMG per 500ms
      setBossHp((prevHp) => {
        const alliedChip = 1000 + Math.floor((Math.random() - 0.5) * 200);
        const nextHp = Math.max(0, prevHp - alliedChip);

        setBossTrailHp((prevTrail) => Math.max(nextHp, prevTrail - 1200));

        // Check Atmospheric Seal Layer transitions (75%, 50%, 25%)
        const currentSeal = getAtmosphericSealLayer(nextHp, BOSS_FLOOR_1_MAX_HP);
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
  const currentSeal = getAtmosphericSealLayer(bossHp, BOSS_FLOOR_1_MAX_HP);
  const tier2Unlocked = playerTotalDamage >= 100_000 || claimedMilestones.includes('tier_3');
  const arsenalBonuses = calculateArsenalBonuses(equippedItems);

  // Player Strike Handler
  const handleHeroStrike = useCallback(
    (forceGolden = false) => {
      if (gameState !== 'playing') {
        if (gameState === 'title') startGame();
        return;
      }

      // Rhythm judgment: forceGolden or default perfect/great
      const isGoldenHit = forceGolden || Math.random() < 0.45;
      const grade = isGoldenHit ? 'PERFECT' : 'GREAT';

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
      });

      // 1. Trigger Panoramic Canvas 2D Strike Visuals
      canvasHandleRef.current?.triggerHeroStrike(isGoldenHit);

      // 2. Spawn Floating Text in Canvas (Pure Integer RPG numbers: -1 DMG, -3 DMG, -12 DMG)
      const stanceData = HAMMER_STANCES[activeStance];
      const isCritHit = outcome.isCrit;
      const combatGradeLabel = isCritHit
        ? `BẠO KÍCH! x${outcome.displayMultiplier}`
        : isGoldenHit
        ? 'HOÀNG KIM! x3.0'
        : 'CHUẨN XÁC! x1.0';

      const combatGradeColor = isCritHit
        ? '#00F0FF'
        : isGoldenHit
        ? '#FFD166'
        : stanceData.color;

      canvasHandleRef.current?.spawnCombatText(
        combatGradeLabel,
        `${stanceData.name.toUpperCase()} · -${outcome.damage} DMG`,
        combatGradeColor,
        isCritHit ? '#0099FF' : isGoldenHit ? '#FF9E00' : stanceData.color,
        isGoldenHit || !!isCritHit
      );

      // 3. Audio & Haptics
      soundEngine.playAnvilStrike(
        grade,
        activeStance,
        combo >= 5 || overdriveActive
      );

      // 4. Update Anvil Heat (Hỏa Hầu)
      setAnvilHeat((prev) => Math.min(MAX_ANVIL_HEAT, prev + outcome.heatGain));

      // 5. Update Phá Giáp Resonance
      if (!isShieldBroken) {
        setResonanceStrikes((prev) => {
          const next = prev + outcome.resonanceGain;
          if (next >= RESONANCE_MAX_STRIKES) {
            setIsShieldBroken(true);
            setShieldBreakTimeLeft(SHIELD_BREAK_DURATION_SEC);
            soundEngine.playGlobalBurstFanfare();
            appendCombatLog(
              '⚡ GIÁP NĂNG LƯỢNG TAN VỠ! Sát thương toàn server lên Boss tăng x1.5 trong 30 giây!',
              'gold'
            );
            return 0;
          }
          return next;
        });
      }

      // 6. Send strike to multiplayer gateway queue
      mpClientRef.current?.recordStrike({
        stance: activeStance,
        quality: grade,
        damage: outcome.damage,
        resonance: outcome.resonanceGain,
        offsetMs: 0,
        isCrit: outcome.triggeredOverdrive || overdriveActive || isGoldenHit,
      });

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

        // 9. Procedural ARPG Loot Drop Check
        const droppedItem = rollLootDrop(
          grade === 'PERFECT' ? 'perfect' : 'great',
          outcome.triggeredOverdrive || overdriveActive,
          isShieldBroken
        );
        if (droppedItem) {
          setInventory((prevInv) => {
            if (prevInv.length >= MAX_INVENTORY_SLOTS) {
              appendCombatLog(
                `⚠️ [TÚI ĐỒ ĐẦY] Rơi [${droppedItem.name}] nhưng rương đã kín chỗ (${MAX_INVENTORY_SLOTS}/${MAX_INVENTORY_SLOTS})! Hãy phân giải bớt.`,
                'red'
              );
              return prevInv;
            }
            const rMeta = getItemRarityMeta(droppedItem.rarity);
            soundEngine.playGlobalBurstFanfare();
            canvasHandleRef.current?.spawnCombatText(
              `🎁 RƠI ${rMeta.label.toUpperCase()}!`,
              droppedItem.name,
              rMeta.hex,
              '#FFFFFF',
              true
            );
            appendCombatLog(
              `🎁 [RƠI TRANG BỊ] Bạn vừa nhặt được [${droppedItem.name}] (${rMeta.label})! Đã chuyển vào Túi Đồ.`,
              droppedItem.rarity === 'mythic' || droppedItem.rarity === 'legendary' ? 'gold' : 'cyan'
            );
            return [droppedItem, ...prevInv];
          });
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

      if (isCritHit) {
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
      appendCombatLog,
    ]
  );

  const handleSelectStance = useCallback(
    (stance: StanceKey) => {
      setActiveStance(stance);
      soundEngine.playStanceSwitch(stance);
      appendCombatLog(
        `Chuyển thế búa: [${stance}] ${HAMMER_STANCES[stance].name} (${HAMMER_STANCES[stance].title})`,
        'cyan'
      );
    },
    [appendCombatLog]
  );

  const handleTriggerGlobalBurst = useCallback(() => {
    if (globalSynergyPct < 100 && !globalBurstActive) return;
    soundEngine.playGlobalBurstFanfare();
    setGlobalBurstActive(true);
    setGlobalSynergyPct(0);
    setBossHp((prev) => Math.max(0, prev - 25000));
    setIsShieldBroken(true);
    setShieldBreakTimeLeft(30);
    appendCombatLog(
      'ĐẠI CỘNG HƯỞNG VẠN DÂN BÙNG NỔ! Giáng thiên lôi -25,000 DMG & vỡ giáp toàn vòm trời!',
      'gold'
    );
    setTimeout(() => setGlobalBurstActive(false), 8000);
  }, [globalSynergyPct, globalBurstActive, appendCombatLog]);

  const handleBuyUpgrade = useCallback(
    (upgradeId: string) => {
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
    [linhThach, appendCombatLog]
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
        `♻️ Phân giải [${item.name}]: Thu được +${yieldReward.linhThach} Linh Thạch${
          yieldReward.tinhHoa > 0 ? `, +${yieldReward.tinhHoa} Tinh Hoa` : ''
        }!`,
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
      targetItems.forEach((it) => {
        const r = getSalvageYield(it);
        totalLT += r.linhThach;
        totalTH += r.tinhHoa;
      });

      setLinhThach((prev) => prev + totalLT);
      if (totalTH > 0) setTinhHoa((prev) => prev + totalTH);

      setInventory((prev) => prev.filter((it) => !rarities.includes(it.rarity)));
      soundEngine.playGlobalBurstFanfare();
      appendCombatLog(
        `♻️ [PHÂN GIẢI NHANH] Đã tách ${targetItems.length} món trang bị! Thu được +${totalLT.toLocaleString(
          'en-US'
        )} Linh Thạch${totalTH > 0 ? `, +${totalTH} Tinh Hoa` : ''}!`,
        'cyan'
      );
    },
    [inventory, appendCombatLog]
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
  }, []);

  // Keyboard Shortcuts: Space, Q/W/E/R, P/Esc, M, [ and ]
  useEffect(() => {
    const onKeyDown = (e: KeyboardEvent) => {
      if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) {
        return;
      }

      if (gameState === 'title') {
        if (e.code === 'Space' || e.code === 'Enter') {
          e.preventDefault();
          startGame();
        }
        return;
      }

      if (e.code === 'KeyP' || e.code === 'Escape') {
        e.preventDefault();
        setGameState((prev) =>
          prev === 'playing' ? 'paused' : prev === 'paused' ? 'playing' : prev
        );
        return;
      }

      if (e.code === 'KeyM') {
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

      if (e.code === 'KeyH') {
        e.preventDefault();
        toggleHudVisibility();
        return;
      }

      if (gameState !== 'playing') return;

      if (e.code === 'Space') {
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
      }
    };

    window.addEventListener('keydown', onKeyDown);
    return () => window.removeEventListener('keydown', onKeyDown);
  }, [gameState, startGame, handleHeroStrike, handleSelectStance, toggleHudVisibility]);

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
          bossMaxHp={BOSS_FLOOR_1_MAX_HP}
          activeStance={activeStance}
          gameState={gameState}
          onHeroStrikeAction={() => handleHeroStrike(false)}
          onPeerAutonomousDamage={(chip) => {
            setBossHp((prev) => Math.max(0, prev - chip));
          }}
        />
      </div>

      {/* Title Screen Overlay */}
      {gameState === 'title' && <TitleScreenModal onStart={startGame} />}

      {/* Top Floating Diegetic Sky Health Header (Zero Sky Obstruction) */}
      <TopBossHeader
        bossName={BOSS_FLOOR_NAME}
        bossHp={bossHp}
        bossMaxHp={BOSS_FLOOR_1_MAX_HP}
        bossTrailHp={bossTrailHp}
        bossShieldPct={isShieldBroken ? 0 : bossShieldPct}
        globalCountdownSec={globalCountdownSec}
        globalSynergyPct={globalSynergyPct}
        globalBurstActive={globalBurstActive}
        activeForgersCount={activeForgersCount}
        isOffline={isOffline}
        anvilHeat={anvilHeat}
        resonanceStrikes={resonanceStrikes}
        isShieldBroken={isShieldBroken}
        shieldBreakTimeLeft={shieldBreakTimeLeft}
        currentSealLayer={currentSeal}
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
        onRestart={resetGame}
        onTriggerGlobalBurst={handleTriggerGlobalBurst}
        leftPanelOpen={leftPanelOpen}
        onToggleLeftPanel={() => setLeftPanelOpen((prev) => !prev)}
        rightPanelOpen={rightPanelOpen}
        onToggleRightPanel={() => setRightPanelOpen((prev) => !prev)}
      />

      {/* 3. CORNER HUD DOCKS (Positioned at corners to leave the Center Hero & Anvil 100% Unobstructed) */}
      {/* 3A. Bottom-Left Dock: 4 Hammer Stances + Overdrive 8/8 Bar */}
      <div
        className={`fixed bottom-3 left-3 sm:left-5 z-20 flex flex-col gap-1.5 pointer-events-auto max-w-[310px] sm:max-w-[360px] transition-all duration-300 ${
          hudVisible
            ? 'opacity-100 translate-y-0'
            : 'opacity-0 translate-y-6 pointer-events-none'
        }`}
      >
        {/* 4 Hammer Stances Bar (Q - W - E - R) */}
        <div
          role="group"
          aria-label="4 Thế Búa Q W E R"
          className="flex items-center gap-1 sm:gap-1.5 p-1 rounded-xl bg-slate-950/85 border border-slate-800/90 backdrop-blur-md shadow-lg"
        >
          {stanceKeys.map((k) => {
            const st = HAMMER_STANCES[k];
            const isSelected = activeStance === k;
            return (
              <button
                key={k}
                type="button"
                onClick={() => handleSelectStance(k)}
                className={`flex items-center gap-1 px-2 py-1.5 rounded-lg border transition-all cursor-pointer ${
                  isSelected
                    ? 'bg-slate-900 border-amber-400 text-amber-300 shadow-md shadow-amber-500/20 scale-[1.02]'
                    : 'bg-slate-950/60 border-slate-800 text-slate-400 hover:text-slate-200 hover:border-slate-700'
                }`}
                title={`[${k}] ${st.name} - ${st.role}`}
              >
                <span
                  className="w-4 h-4 rounded text-[10px] font-tech font-bold flex items-center justify-center"
                  style={{
                    backgroundColor: isSelected ? st.color : 'rgba(255,255,255,0.06)',
                    color: isSelected ? '#05070F' : '#94A3B8',
                  }}
                >
                  {k}
                </span>
                <span className="hidden sm:inline text-xs font-semibold whitespace-nowrap">
                  {st.name}
                </span>
              </button>
            );
          })}
        </div>

        {/* Overdrive 8/8 Bar */}
        <div
          className={`rounded-xl px-2.5 py-1.5 border backdrop-blur-md transition-colors ${
            overdriveActive
              ? 'bg-cyan-500/20 border-cyan-400 shadow-md shadow-cyan-400/20'
              : 'bg-slate-950/85 border-slate-800/90'
          }`}
        >
          <div className="flex items-center justify-between text-[10px] sm:text-[11px] font-tech mb-1">
            <span className={overdriveActive ? 'text-cyan-300 font-bold' : 'text-slate-400'}>
              {overdriveActive
                ? `LÔI ĐÌNH QUÁ TẢI (${overdriveTimeLeft.toFixed(1)}s)`
                : 'Overdrive · Chuỗi 8/8'}
            </span>
            <span className="font-bold text-amber-300">
              {overdriveActive ? 'x2.0 DMG' : `${overdriveCharge.toFixed(1)}/8`}
            </span>
          </div>

          <div className="grid grid-cols-8 gap-0.5 sm:gap-1">
            {Array.from({ length: OVERDRIVE_MAX }).map((_, idx) => {
              const filled = overdriveActive || overdriveCharge >= idx + 1;
              const half = !filled && overdriveCharge >= idx + 0.5;
              return (
                <div
                  key={idx}
                  className={`h-1.5 rounded-sm transition-all ${
                    overdriveActive
                      ? 'bg-cyan-400 shadow-sm shadow-cyan-400/60'
                      : filled
                      ? 'bg-amber-400'
                      : half
                      ? 'bg-amber-400/50'
                      : 'bg-slate-800'
                  }`}
                />
              );
            })}
          </div>
        </div>
      </div>

      {/* 3B. Bottom-Right Controls: Primary Strike Trigger + Toggle HUD Button */}
      <div className="fixed bottom-3 right-3 sm:right-5 z-20 flex items-center gap-2 pointer-events-auto">
        {hudVisible && (
          <button
            type="button"
            onClick={() => handleHeroStrike(false)}
            className="px-4 py-2 sm:px-5 sm:py-2.5 rounded-xl bg-gradient-to-r from-amber-500/20 via-orange-500/20 to-amber-500/20 hover:from-amber-500/30 hover:to-amber-500/30 border border-amber-500/50 text-xs sm:text-sm font-tech font-bold text-amber-300 tracking-wider shadow-lg hover:border-amber-400 transition-all cursor-pointer active:scale-95 whitespace-nowrap"
          >
            NỆN BÚA [SPACE]
          </button>
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
          />
        </div>
      </div>

      {/* 5. SLIDE-OUT DRAWER 2 (RIGHT): NÂNG CẤP, THẦN HỒN & BẢNG VÀNG */}
      <div
        className={`fixed inset-y-0 right-0 z-40 w-full sm:w-[400px] md:w-[440px] bg-slate-950/95 border-l border-amber-500/30 backdrop-blur-xl shadow-2xl transform transition-transform duration-300 ease-in-out flex flex-col ${
          rightPanelOpen ? 'translate-x-0' : 'translate-x-full'
        }`}
      >
        <div className="flex items-center justify-between px-4 py-3 border-b border-slate-800 bg-slate-900/80">
          <div className="flex items-center gap-2 text-amber-300 font-tech font-bold text-sm">
            <Hammer className="w-4 h-4 text-amber-400" />
            <span>LÒ RÈN & THẦN HỒN</span>
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
            linhThach={linhThach}
            tinhHoa={tinhHoa}
            tier2Unlocked={tier2Unlocked}
            leaderboard={leaderboard}
            mobileDrawerOpen={rightPanelOpen}
            onCloseMobileDrawer={() => setRightPanelOpen(false)}
            onBuyUpgrade={handleBuyUpgrade}
            onUnlockSpiritNode={handleUnlockSpiritNode}
            onEquipItem={handleEquipItem}
            onUnequipItem={handleUnequipItem}
            onSalvageItem={handleSalvageItem}
            onQuickSalvage={handleQuickSalvage}
          />
        </div>
      </div>

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

      {/* Pause & Victory Status Modal */}
      {(gameState === 'paused' || gameState === 'gameover') && (
        <StatusModal
          mode={gameState}
          playerTotalDamage={playerTotalDamage}
          maxCombo={maxCombo}
          perfectCount={perfectCount}
          onResume={() => setGameState('playing')}
          onRestart={resetGame}
          onReturnTitle={() => setGameState('title')}
        />
      )}
    </div>
  );
}
