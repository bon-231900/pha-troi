import React, { useState, useEffect, useRef, useCallback } from 'react';
import {
  StanceKey,
  INITIAL_UPGRADES,
  INITIAL_SPIRIT_NODES,
  ForgeUpgrade,
  SpiritNode,
  calculateStrikeOutcome,
  calculateBasePowerBillions,
  calculateSpiritMultiplier,
  getUpgradeCost,
  canUnlockSpiritNode,
  HAMMER_STANCES,
  OVERDRIVE_MAX,
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

const BOSS_MAX_HP = 1000.0; // 1,000.00B HP

const INITIAL_CHAT: ChatMessage[] = [
  {
    id: 1,
    sender: 'Lôi Đế Tử Vi',
    realm: 'Tầng 9 · Đại Tông Sư',
    content: 'Vòng sóng co đến Gờ Vàng Đe là nện ngay để lấy x3.5 Hoàng Kim nhé anh em!',
  },
  {
    id: 2,
    sender: 'Xích Hỏa Chân Nhân',
    realm: 'Tầng 8 · Thần Chùy',
    content: 'Giáp Boss còn dày, đội hình ưu tiên Phá Giáp Chùy [E] trước!',
  },
  {
    id: 3,
    sender: 'Huyền Thiết Kiếm',
    realm: 'Tầng 7 · Hộ Pháp',
    content: 'Tích đủ 8/8 combo bật Lôi Đình Quá Tải đập sướng tay cực kỳ.',
  },
];

const INITIAL_RIVALS: LeaderboardEntry[] = [
  { id: 'r1', name: 'Lôi Đế Tử Vi', sect: 'Thiên Lôi Tông', damageBillions: 48.6 },
  { id: 'r2', name: 'Xích Hỏa Chân Nhân', sect: 'Phần Thiên Các', damageBillions: 34.2 },
  { id: 'r3', name: 'Huyền Thiết Kiếm', sect: 'Vạn Kiếm Sơn', damageBillions: 19.8 },
  { id: 'r4', name: 'Cửu U Mặc Khách', sect: 'Đoạn Hồn Cốc', damageBillions: 8.4 },
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

  // Boss & Multiplayer Raid State
  const [bossHpBillions, setBossHpBillions] = useState<number>(842.5);
  const [bossTrailHpBillions, setBossTrailHpBillions] = useState<number>(842.5);
  const [bossShieldPct, setBossShieldPct] = useState<number>(68.0);
  const [globalCountdownSec, setGlobalCountdownSec] = useState<number>(180);
  const [globalSynergyPct, setGlobalSynergyPct] = useState<number>(74.0);
  const [globalBurstActive, setGlobalBurstActive] = useState<boolean>(false);
  const [activeForgersCount, setActiveForgersCount] = useState<number>(14820);

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

  // Bottom HUD Visibility State (Can be toggled via H or button to not obstruct hero)
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

  // Resources & Progression (Hydrated safely from storage)
  const [linhThach, setLinhThach] = useState<number>(() => {
    try {
      const s = safeStorage.getItem('phatroi_save_v5');
      if (s) {
        const parsed = JSON.parse(s);
        if (typeof parsed.linhThach === 'number') return parsed.linhThach;
      }
    } catch {}
    return 220;
  });
  const [tinhHoa, setTinhHoa] = useState<number>(() => {
    try {
      const s = safeStorage.getItem('phatroi_save_v5');
      if (s) {
        const parsed = JSON.parse(s);
        if (typeof parsed.tinhHoa === 'number') return parsed.tinhHoa;
      }
    } catch {}
    return 5;
  });
  const [upgrades, setUpgrades] = useState<ForgeUpgrade[]>(() => {
    try {
      const s = safeStorage.getItem('phatroi_save_v5');
      if (s) {
        const parsed = JSON.parse(s);
        if (Array.isArray(parsed.upgrades)) return parsed.upgrades;
      }
    } catch {}
    return INITIAL_UPGRADES;
  });
  const [spiritNodes, setSpiritNodes] = useState<SpiritNode[]>(() => {
    try {
      const s = safeStorage.getItem('phatroi_save_v5');
      if (s) {
        const parsed = JSON.parse(s);
        if (Array.isArray(parsed.spiritNodes)) return parsed.spiritNodes;
      }
    } catch {}
    return INITIAL_SPIRIT_NODES;
  });
  const [playerTotalDamageBillions, setPlayerTotalDamageBillions] = useState<number>(() => {
    try {
      const s = safeStorage.getItem('phatroi_save_v5');
      if (s) {
        const parsed = JSON.parse(s);
        if (typeof parsed.playerTotalDamageBillions === 'number')
          return parsed.playerTotalDamageBillions;
      }
    } catch {}
    return 4.25;
  });

  // UI & Feedback State
  const [lastFeedback, setLastFeedback] = useState<{
    id: number;
    grade: string;
    labelVn: string;
    multiplier: number;
    damageBillions: number;
  } | null>(null);

  const lastMilestonePercentRef = useRef<number>(100);
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
      text: 'Đại Công Trường Vạn Dân khai mở! 14,820 Thợ Rèn đang hợp lực.',
      tone: 'gold',
    },
    {
      id: 2,
      timestamp: '00:02',
      text: 'Cửu U Thiên Ma Đế vận chuyển Giáp Năng Lượng (68%).',
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

  // Auto-save progression to safeStorage
  useEffect(() => {
    const saveState = () => {
      try {
        const payload = {
          linhThach,
          tinhHoa,
          upgrades,
          spiritNodes,
          playerTotalDamageBillions,
          lastActiveTimestamp: Date.now(),
        };
        safeStorage.setItem('phatroi_save_v5', JSON.stringify(payload));
      } catch {}
    };

    const timer = setInterval(saveState, 3000);
    window.addEventListener('beforeunload', saveState);
    return () => {
      clearInterval(timer);
      window.removeEventListener('beforeunload', saveState);
    };
  }, [linhThach, tinhHoa, upgrades, spiritNodes, playerTotalDamageBillions]);

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
        if (hb.hp && hb.maxHp) {
          const curHp = parseFloat(hb.hp);
          const maxHp = parseFloat(hb.maxHp);
          if (!isNaN(curHp) && !isNaN(maxHp) && maxHp > 0) {
            const hpBillions = curHp > 10000 ? curHp / 1e9 : curHp;
            setBossHpBillions(Number(hpBillions.toFixed(2)));
            setBossTrailHpBillions((prev) => Math.max(hpBillions, prev));
          }
        }
        if (typeof hb.res === 'number' && typeof hb.resReq === 'number' && hb.resReq > 0) {
          const shield = Math.max(0, 100 - (hb.res / hb.resReq) * 100);
          setBossShieldPct(Number(shield.toFixed(1)));
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
    setBossHpBillions(842.5);
    setBossTrailHpBillions(842.5);
    setBossShieldPct(68.0);
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
    appendCombatLog('Lò rèn tái khởi động! Vạn dân đồng loạt giáng búa!', 'gold');
  }, [appendCombatLog]);

  // Periodic co-op raid loop
  useEffect(() => {
    if (gameState !== 'playing') return;

    const timer = setInterval(() => {
      setOverdriveTimeLeft((prev) => {
        if (prev <= 0) return 0;
        const next = Math.max(0, prev - 0.5);
        if (next === 0) {
          setOverdriveActive(false);
          setOverdriveCharge(0);
        }
        return next;
      });

      setGlobalCountdownSec((prev) => (prev <= 1 ? 180 : prev - 0.5));

      setBossHpBillions((prevHp) => {
        const alliedChip = 0.24;
        const nextHp = Math.max(1.0, Number((prevHp - alliedChip).toFixed(3)));
        setBossTrailHpBillions((prevTrail) =>
          Math.max(nextHp, Number((prevTrail - 0.45).toFixed(3)))
        );
        return nextHp;
      });

      setGlobalSynergyPct((prevSyn) => Math.min(100, Number((prevSyn + 0.4).toFixed(1))));
      setActiveForgersCount((prevCount) =>
        Math.max(14200, prevCount + Math.floor((Math.random() - 0.48) * 18))
      );
    }, 500);

    return () => clearInterval(timer);
  }, [gameState]);

  const basePowerBillions = calculateBasePowerBillions(upgrades);
  const spiritBonusMult = calculateSpiritMultiplier(spiritNodes);

  // Player Strike Handler
  const handleHeroStrike = useCallback(
    (forceGolden = false) => {
      if (gameState !== 'playing') {
        if (gameState === 'title') startGame();
        return;
      }

      // Generous rhythm judgment: forceGolden or default perfect/great
      const isGoldenHit = forceGolden || Math.random() < 0.45;
      const grade = isGoldenHit ? 'PERFECT' : 'GREAT';

      const outcome = calculateStrikeOutcome({
        grade,
        stance: activeStance,
        basePowerBillions,
        combo,
        overdriveCharge,
        overdriveActive,
        bossShieldPct,
        spiritBonusMult,
        globalBurstActive,
      });

      // 1. Trigger Panoramic Canvas 2D Strike Visuals
      canvasHandleRef.current?.triggerHeroStrike(isGoldenHit);

      // 2. Spawn Floating Text in Canvas
      const stanceData = HAMMER_STANCES[activeStance];
      canvasHandleRef.current?.spawnCombatText(
        isGoldenHit ? 'HOÀNG KIM! x3.5' : 'CHUẨN XÁC! x2.0',
        `${stanceData.name.toUpperCase()} · -${outcome.damageBillions.toFixed(2)}B HP`,
        isGoldenHit ? '#FFD166' : stanceData.color,
        isGoldenHit ? '#FF9E00' : stanceData.color,
        isGoldenHit
      );

      // 3. Audio & Haptics
      soundEngine.playAnvilStrike(
        grade,
        activeStance,
        combo >= 5 || overdriveActive
      );

      // 4. Send strike to multiplayer gateway queue
      mpClientRef.current?.recordStrike({
        stance: activeStance,
        quality: grade,
        damage: outcome.damageBillions,
        resonance: activeStance === 'E' ? 3 : 1,
        offsetMs: 0,
        isCrit: outcome.triggeredOverdrive || overdriveActive || isGoldenHit,
      });

      // 5. Update Combo & Overdrive
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

      // 6. Resources & Damage
      if (outcome.damageBillions > 0) {
        setLinhThach((prev) => prev + outcome.linhThachEarned);
        if (outcome.tinhHoaEarned > 0) {
          setTinhHoa((prev) => prev + outcome.tinhHoaEarned);
        }
        setPlayerTotalDamageBillions((prev) =>
          Number((prev + outcome.damageBillions).toFixed(3))
        );

        setBossShieldPct((prevShield) => {
          const nextShield = Math.max(
            0,
            Number((prevShield - outcome.shieldDepletion).toFixed(2))
          );
          if (prevShield > 0 && nextShield === 0) {
            appendCombatLog(
              'GIÁP NĂNG LƯỢNG TAN VỠ! Sát thương toàn server lên Boss tăng x1.5!',
              'gold'
            );
          }
          return nextShield;
        });

        setGlobalSynergyPct((prevSyn) =>
          Math.min(100, Number((prevSyn + outcome.synergyGain).toFixed(1)))
        );

        setBossHpBillions((prevHp) => {
          const nextHp = Math.max(
            0,
            Number((prevHp - outcome.damageBillions).toFixed(3))
          );

          const nextPct = (nextHp / BOSS_MAX_HP) * 100;
          const currentMilestone = Math.floor(nextPct / 10) * 10;
          const lastMilestone = Math.floor(lastMilestonePercentRef.current / 10) * 10;

          if (currentMilestone < lastMilestone && nextHp > 0) {
            lastMilestonePercentRef.current = currentMilestone;
            appendCombatLog(
              `[THIÊN CẤM CHẤN ĐỘNG] Máu Ma Đế phá vỡ mốc ${currentMilestone}%! Vòm trời Cửu Trọng nứt toác, bão lửa tuôn trào!`,
              'gold'
            );
          }

          if (nextHp <= 0) {
            setGameState('gameover');
            soundEngine.playGlobalBurstFanfare();
          }
          return nextHp;
        });
      }

      feedbackCounterRef.current += 1;
      setLastFeedback({
        id: feedbackCounterRef.current,
        grade,
        labelVn: isGoldenHit ? 'HOÀNG KIM' : 'CHUẨN XÁC',
        multiplier: outcome.displayMultiplier,
        damageBillions: outcome.damageBillions,
      });

      if (isGoldenHit) {
        appendCombatLog(
          `Nhịp Hoàng Kim [${activeStance}]! Giáng -${outcome.damageBillions.toFixed(2)}B HP (x${outcome.displayMultiplier.toFixed(1)})`,
          'gold'
        );
      } else {
        appendCombatLog(
          `Nhịp Chuẩn Xác [${activeStance}]! Giáng -${outcome.damageBillions.toFixed(2)}B HP`,
          'neutral'
        );
      }
    },
    [
      gameState,
      startGame,
      activeStance,
      basePowerBillions,
      combo,
      overdriveCharge,
      overdriveActive,
      bossShieldPct,
      spiritBonusMult,
      globalBurstActive,
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
    setBossHpBillions((prev) => Math.max(0, Number((prev - 18.5).toFixed(2))));
    setBossShieldPct((prev) => Math.max(0, Number((prev - 25).toFixed(1))));
    appendCombatLog(
      'ĐẠI CỘNG HƯỞNG VẠN DÂN BÙNG NỔ! Giáng thiên lôi -18.50B HP & cường hóa toàn server x2.5!',
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
          appendCombatLog(`Nâng cấp thành công: ${u.name} lên Cấp ${u.level + 1}!`, 'gold');
          return { ...u, level: u.level + 1 };
        })
      );
    },
    [linhThach, appendCombatLog]
  );

  const handleUnlockSpiritNode = useCallback(
    (nodeId: string) => {
      if (!canUnlockSpiritNode(nodeId, spiritNodes, tinhHoa)) return;
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
    [spiritNodes, tinhHoa, appendCombatLog]
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
  }, [gameState, startGame, handleHeroStrike, handleSelectStance]);

  const leaderboard: LeaderboardEntry[] = [
    ...INITIAL_RIVALS,
    {
      id: 'player',
      name: 'Bạn · Đại Sư Rèn Đúc',
      sect: 'Thiên Cổ Lò Rèn',
      damageBillions: playerTotalDamageBillions,
      isPlayer: true,
    },
  ].sort((a, b) => b.damageBillions - a.damageBillions);

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

      {/* 1. MAIN PLAYABLE SCENE: Panoramic 2D Community Canvas (18 Online Blacksmiths + Cracking Sky Vault) */}
      <div className="fixed inset-0 w-full h-full z-0 pointer-events-auto">
        <CommunityPanoramicForgeCanvas
          ref={canvasHandleRef}
          bossHp={bossHpBillions}
          bossMaxHp={BOSS_MAX_HP}
          activeStance={activeStance}
          gameState={gameState}
          onHeroStrikeAction={() => handleHeroStrike(false)}
          onPeerAutonomousDamage={(chip) => {
            setBossHpBillions((prev) => Math.max(0, Number((prev - chip * 0.05).toFixed(3))));
          }}
        />
      </div>

      {/* Title Screen Overlay */}
      {gameState === 'title' && <TitleScreenModal onStart={startGame} />}

      {/* Top Floating Diegetic Sky Health Header (Sleek, Translucent, Zero Sky Obstruction) */}
      <TopBossHeader
        bossHpBillions={bossHpBillions}
        bossMaxHpBillions={BOSS_MAX_HP}
        bossTrailHpBillions={bossTrailHpBillions}
        bossShieldPct={bossShieldPct}
        globalCountdownSec={globalCountdownSec}
        globalSynergyPct={globalSynergyPct}
        globalBurstActive={globalBurstActive}
        activeForgersCount={activeForgersCount}
        isOffline={isOffline}
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
                    ? 'bg-slate-900 border-amber-400 text-white shadow-sm shadow-amber-500/25'
                    : 'bg-slate-950/70 border-slate-800 hover:border-slate-700 text-slate-400 hover:text-slate-200'
                }`}
                title={`Phím [${k}] · ${st.name} (${st.title})`}
              >
                <span
                  className="w-4 h-4 rounded text-[10px] font-tech font-bold flex items-center justify-center text-slate-950"
                  style={{ backgroundColor: st.color }}
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

      {/* 4. SLIDE-OUT DRAWER 1 (LEFT): THẾ TRẬN, NHẬT KÝ CHIẾN TRƯỜNG & CHAT */}
      <div
        className={`fixed inset-y-0 left-0 z-40 w-full sm:w-[380px] md:w-[420px] bg-slate-950/95 border-r border-amber-500/30 backdrop-blur-xl shadow-2xl transform transition-transform duration-300 ease-in-out flex flex-col ${
          leftPanelOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <div className="flex items-center justify-between px-4 py-3 border-b border-slate-800 bg-slate-900/80">
          <div className="flex items-center gap-2 text-amber-300 font-tech font-bold text-sm">
            <Shield className="w-4 h-4 text-cyan-400" />
            <span>THẾ TRẬN & TRUYỀN ÂM VẠN DÂN</span>
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
            playerTotalDamageBillions={playerTotalDamageBillions}
            perfectCount={perfectCount}
            maxCombo={maxCombo}
            serverDpsBillions={5.7 + basePowerBillions}
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
            upgrades={upgrades}
            spiritNodes={spiritNodes}
            linhThach={linhThach}
            tinhHoa={tinhHoa}
            leaderboard={leaderboard}
            mobileDrawerOpen={rightPanelOpen}
            onCloseMobileDrawer={() => setRightPanelOpen(false)}
            onBuyUpgrade={handleBuyUpgrade}
            onUnlockSpiritNode={handleUnlockSpiritNode}
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
          playerTotalDamageBillions={playerTotalDamageBillions}
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
