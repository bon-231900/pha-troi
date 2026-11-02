import React, { useState, useEffect, useRef, useCallback } from 'react';
import {
  StanceKey,
  INITIAL_UPGRADES,
  INITIAL_SPIRIT_NODES,
  ForgeUpgrade,
  SpiritNode,
  judgeRhythmWave,
  calculateStrikeOutcome,
  calculateBasePowerBillions,
  calculateSpiritMultiplier,
  getUpgradeCost,
  canUnlockSpiritNode,
  HAMMER_STANCES,
  TARGET_RIM_PROGRESS,
  FORGE_BPM,
  getBpmWaveSpeed,
} from './game/rules';
import { soundEngine } from './game/audio';
import { TitleScreenModal } from './components/TitleScreenModal';
import { TopBossHeader } from './components/TopBossHeader';
import { RadialForgeCenter, FloatingFeedback } from './components/RadialForgeCenter';
import {
  LeftTacticalPanel,
  CombatLogEntry,
  ChatMessage,
} from './components/LeftTacticalPanel';
import {
  RightProgressionPanel,
  LeaderboardEntry,
} from './components/RightProgressionPanel';
import { StatusModal } from './components/StatusModal';
import { MultiplayerClient } from './game/multiplayer';

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

  // Resources & Progression (Hydrated from localStorage)
  const [linhThach, setLinhThach] = useState<number>(() => {
    try {
      const s = localStorage.getItem('phatroi_save_v5');
      if (s) {
        const parsed = JSON.parse(s);
        if (typeof parsed.linhThach === 'number') return parsed.linhThach;
      }
    } catch {}
    return 220;
  });
  const [tinhHoa, setTinhHoa] = useState<number>(() => {
    try {
      const s = localStorage.getItem('phatroi_save_v5');
      if (s) {
        const parsed = JSON.parse(s);
        if (typeof parsed.tinhHoa === 'number') return parsed.tinhHoa;
      }
    } catch {}
    return 5;
  });
  const [upgrades, setUpgrades] = useState<ForgeUpgrade[]>(() => {
    try {
      const s = localStorage.getItem('phatroi_save_v5');
      if (s) {
        const parsed = JSON.parse(s);
        if (Array.isArray(parsed.upgrades)) return parsed.upgrades;
      }
    } catch {}
    return INITIAL_UPGRADES;
  });
  const [spiritNodes, setSpiritNodes] = useState<SpiritNode[]>(() => {
    try {
      const s = localStorage.getItem('phatroi_save_v5');
      if (s) {
        const parsed = JSON.parse(s);
        if (Array.isArray(parsed.spiritNodes)) return parsed.spiritNodes;
      }
    } catch {}
    return INITIAL_SPIRIT_NODES;
  });
  const [playerTotalDamageBillions, setPlayerTotalDamageBillions] = useState<number>(() => {
    try {
      const s = localStorage.getItem('phatroi_save_v5');
      if (s) {
        const parsed = JSON.parse(s);
        if (typeof parsed.playerTotalDamageBillions === 'number') return parsed.playerTotalDamageBillions;
      }
    } catch {}
    return 4.25;
  });

  // UI & Feedback State
  const [lastFeedback, setLastFeedback] = useState<FloatingFeedback | null>(null);
  const [shakeClass, setShakeClass] = useState<string>('');
  const [muted, setMuted] = useState<boolean>(false);
  const [mobileDrawerOpen, setMobileDrawerOpen] = useState<boolean>(false);

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

  // High-frequency Rhythm Wave progress ref (0 = outer ring, 1 = center)
  // Advanced in lockstep with the Three.js 100 BPM shader loop in CelestialAnvil3D
  const waveProgressRef = useRef<number>(TARGET_RIM_PROGRESS - 0.04);
  const feedbackCounterRef = useRef<number>(1);
  const logCounterRef = useRef<number>(10);
  const mpClientRef = useRef<MultiplayerClient | null>(null);

  // Auto-save progression to localStorage
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
        localStorage.setItem('phatroi_save_v5', JSON.stringify(payload));
      } catch {}
    };

    const timer = setInterval(saveState, 3000);
    window.addEventListener('beforeunload', saveState);
    return () => {
      clearInterval(timer);
      window.removeEventListener('beforeunload', saveState);
    };
  }, [linhThach, tinhHoa, upgrades, spiritNodes, playerTotalDamageBillions]);

  // Connect to Multiplayer Gateway (Local ws or wss://api.phatroi.com)
  useEffect(() => {
    const mp = new MultiplayerClient({
      onConnected: (districtId) => {
        appendCombatLog(`Đã kết nối vào Phân Khu Vạn Dân [${districtId}]!`, 'cyan');
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
      onPeerSparks: (sparkCount) => {
        // Peer sparks visual feedback
      },
    });

    mp.connect();
    mpClientRef.current = mp;

    return () => {
      mp.disconnect();
    };
  }, [appendCombatLog]);

  // Sync document.body.dataset.state for Ultra Mode verification
  useEffect(() => {
    document.body.dataset.state = gameState;
  }, [gameState]);

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

  const startGame = useCallback(() => {
    if (document.activeElement instanceof HTMLElement) {
      document.activeElement.blur();
    }
    waveProgressRef.current = TARGET_RIM_PROGRESS - 0.04;
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
    waveProgressRef.current = TARGET_RIM_PROGRESS - 0.04;
    document.body.dataset.state = 'playing';
    setGameState('playing');
    appendCombatLog('Lò rèn tái khởi động! Vạn dân đồng loạt giáng búa!', 'gold');
  }, [appendCombatLog]);

  // 1-second interval for Global Beat Bar countdown, Overdrive duration, and Server Co-op DPS
  useEffect(() => {
    if (gameState !== 'playing') return;

    const timer = setInterval(() => {
      // Update Overdrive remaining time
      setOverdriveTimeLeft((prev) => {
        if (prev <= 0) return 0;
        const next = Math.max(0, prev - 0.5);
        if (next === 0) {
          setOverdriveActive(false);
          setOverdriveCharge(0);
        }
        return next;
      });

      // Global countdown & server co-op damage tick
      setGlobalCountdownSec((prev) => {
        if (prev <= 1) {
          return 180;
        }
        return prev - 0.5;
      });

      // Allied Vạn Dân Forgers continuous chip damage & synergy
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

  // Handle Player Anvil Strike (Space or Click/Touch)
  const handleStrike = useCallback(() => {
    if (gameState !== 'playing') return;

    const currentProg = waveProgressRef.current;
    const judgment = judgeRhythmWave(currentProg);

    const outcome = calculateStrikeOutcome({
      grade: judgment.grade,
      stance: activeStance,
      basePowerBillions,
      combo,
      overdriveCharge,
      overdriveActive,
      bossShieldPct,
      spiritBonusMult,
      globalBurstActive,
    });

    soundEngine.playAnvilStrike(
      judgment.grade,
      activeStance,
      overdriveActive || outcome.triggeredOverdrive
    );

    // Send strike to Multiplayer Gateway batch queue
    mpClientRef.current?.recordStrike({
      stance: activeStance,
      quality: judgment.grade,
      damage: outcome.damageBillions,
      resonance: activeStance === 'E' ? 3 : 1,
      offsetMs: Math.round((currentProg - TARGET_RIM_PROGRESS) * 1000),
      isCrit: outcome.triggeredOverdrive || overdriveActive || judgment.grade === 'PERFECT',
    });

    // Reset wave to 0.62 so a ~0.3s rhythm interval hits TARGET_RIM_PROGRESS (0.78) cleanly
    waveProgressRef.current = 0.62;

    setCombo(outcome.nextCombo);
    setMaxCombo((prev) => Math.max(prev, outcome.nextCombo));
    if (judgment.grade === 'PERFECT') {
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

    if (outcome.damageBillions > 0) {
      setLinhThach((prev) => prev + outcome.linhThachEarned);
      if (outcome.tinhHoaEarned > 0) {
        setTinhHoa((prev) => prev + outcome.tinhHoaEarned);
      }
      setPlayerTotalDamageBillions((prev) =>
        Number((prev + outcome.damageBillions).toFixed(3))
      );

      setBossShieldPct((prevShield) => {
        const nextShield = Math.max(0, Number((prevShield - outcome.shieldDepletion).toFixed(2)));
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
        const nextHp = Math.max(0, Number((prevHp - outcome.damageBillions).toFixed(3)));
        if (nextHp <= 0) {
          setGameState('gameover');
        }
        return nextHp;
      });
    }

    // Visual Screen Shake on PERFECT or Overdrive
    if (judgment.grade === 'PERFECT') {
      setShakeClass(
        overdriveActive || outcome.triggeredOverdrive
          ? 'animate-shake-heavy'
          : 'animate-shake-light'
      );
      setTimeout(() => setShakeClass(''), 240);
      appendCombatLog(
        `Nhịp Hoàng Kim [${activeStance}]! Giáng -${outcome.damageBillions.toFixed(2)}B HP (x${outcome.displayMultiplier.toFixed(1)})`,
        'gold'
      );
    } else if (judgment.grade === 'GREAT') {
      appendCombatLog(
        `Nhịp Chuẩn Xác [${activeStance}]! Giáng -${outcome.damageBillions.toFixed(2)}B HP`,
        'neutral'
      );
    } else {
      appendCombatLog('Trượt nhịp! Búa xì khói đen, đứt chuỗi Combo.', 'red');
    }

    feedbackCounterRef.current += 1;
    setLastFeedback({
      id: feedbackCounterRef.current,
      grade: judgment.grade,
      labelVn: judgment.labelVn,
      multiplier: outcome.displayMultiplier,
      damageBillions: outcome.damageBillions,
      stance: activeStance,
      overdrive: overdriveActive || outcome.triggeredOverdrive,
    });
  }, [
    gameState,
    activeStance,
    basePowerBillions,
    combo,
    overdriveCharge,
    overdriveActive,
    bossShieldPct,
    spiritBonusMult,
    globalBurstActive,
    appendCombatLog,
  ]);

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
    setTimeout(() => {
      setGlobalBurstActive(false);
    }, 8000);
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

  // Global Keyboard Shortcuts (Space, Q/W/E/R, P/Esc, M)
  useEffect(() => {
    const onKeyDown = (e: KeyboardEvent) => {
      // Ignore shortcuts when typing inside chat input
      if (
        e.target instanceof HTMLInputElement ||
        e.target instanceof HTMLTextAreaElement
      ) {
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
        setGameState((prev) => (prev === 'playing' ? 'paused' : prev === 'paused' ? 'playing' : prev));
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

      if (gameState !== 'playing') return;

      if (e.code === 'Space') {
        e.preventDefault();
        // Snap wave close to Golden Rim when pressing Space near the beat or evaluate current wave
        handleStrike();
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
  }, [gameState, startGame, handleStrike, handleSelectStance]);

  // Build Live Sorted Leaderboard including Player
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

  return (
    <div
      className="min-h-screen h-screen w-full bg-[#080A10] text-slate-100 flex flex-col overflow-hidden"
      data-stance={activeStance}
      data-overdrive={overdriveActive ? 'true' : 'false'}
      data-target-rim={TARGET_RIM_PROGRESS}
    >
      {/* Title Screen Overlay */}
      {gameState === 'title' && <TitleScreenModal onStart={startGame} />}

      {/* Top Multiplayer Boss Raid Header */}
      <TopBossHeader
        bossName="Cửu U Thiên Ma Đế · Hắc Diên Cự Thần"
        bossRealm="Cửu Trọng Thiên · Tầng Đỉnh Phong"
        bossHpBillions={bossHpBillions}
        bossMaxHpBillions={BOSS_MAX_HP}
        bossTrailHpBillions={bossTrailHpBillions}
        bossShieldPct={bossShieldPct}
        globalCountdownSec={globalCountdownSec}
        globalSynergyPct={globalSynergyPct}
        globalBurstActive={globalBurstActive}
        activeForgersCount={activeForgersCount}
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
      />

      {/* Ergonomic 3-Column Desktop / One-Thumb Mobile Main Workspace */}
      <div className="flex-1 flex overflow-hidden max-w-[1440px] w-full mx-auto">
        {/* Column 1 (Left): Thế Trận, Boss Log & Mini-Chat */}
        <LeftTacticalPanel
          activeStance={activeStance}
          playerTotalDamageBillions={playerTotalDamageBillions}
          perfectCount={perfectCount}
          maxCombo={maxCombo}
          serverDpsBillions={4.85 + basePowerBillions}
          combatLogs={combatLogs}
          chatMessages={chatMessages}
          onSendChat={handleSendChat}
        />

        {/* Column 2 (Center): Lò Rèn Trung Tâm, Bão Lửa Vạn Dân Canvas & Vòng Tròn Nhịp Điệu */}
        <RadialForgeCenter
          waveProgressRef={waveProgressRef}
          activeStance={activeStance}
          combo={combo}
          overdriveCharge={overdriveCharge}
          overdriveActive={overdriveActive}
          overdriveTimeLeft={overdriveTimeLeft}
          globalBurstActive={globalBurstActive}
          lastFeedback={lastFeedback}
          shakeClass={shakeClass}
          linhThach={linhThach}
          tinhHoa={tinhHoa}
          basePowerBillions={basePowerBillions}
          onStrike={handleStrike}
          onSelectStance={handleSelectStance}
          onOpenMobileDrawer={() => setMobileDrawerOpen(true)}
        />

        {/* Column 3 (Right + Mobile Bottom Sheet Drawer): Nâng Cấp, Cây Thần Hồn, Bảng Vàng */}
        <RightProgressionPanel
          upgrades={upgrades}
          spiritNodes={spiritNodes}
          linhThach={linhThach}
          tinhHoa={tinhHoa}
          leaderboard={leaderboard}
          mobileDrawerOpen={mobileDrawerOpen}
          onCloseMobileDrawer={() => setMobileDrawerOpen(false)}
          onBuyUpgrade={handleBuyUpgrade}
          onUnlockSpiritNode={handleUnlockSpiritNode}
        />
      </div>

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
