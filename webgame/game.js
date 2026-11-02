// ============================================================================
// TOÀN DÂN PHÁ TRỜI: THE CELESTIAL FORGE - CORE ENGINE (PHASE 4: FULL LAUNCH)
// WebSocket 2Hz, Redis Atomic Last-Hit, Anti-Cheat, Hall of Eternity & Persistence
// ============================================================================

// Formatter số lớn gọn đẹp
function formatNum(n) {
    if (n === null || n === undefined || isNaN(n)) return "0";
    if (n < 1000) return Math.floor(n).toLocaleString('vi-VN');
    const suffixes = ["", "K", "M", "B", "T", "Qa", "Qi", "Sx", "Sp", "Oc", "No", "Dc"];
    const i = Math.floor(Math.log10(Math.max(1, n)) / 3);
    if (i >= suffixes.length) return n.toExponential(2);
    const formatted = (n / Math.pow(10, i * 3)).toFixed(2);
    return `${formatted} ${suffixes[i]}`;
}

// Cửu Trọng Thiên Cấm (9 Mái Vòm Thiên Giới - Mức máu cân bằng trải nghiệm đơn & đa người chơi)
const CELESTIAL_LAYERS = [
    { layer: 1, name: "Thiết Vân Vòm (Vòm Mây Sắt)", baseHp: 50000 },
    { layer: 2, name: "Đồng Lôi Vòm (Vòm Sấm Đồng)", baseHp: 250000 },
    { layer: 3, name: "Ngân Cực Vòm (Vòm Cực Quang Bạc)", baseHp: 1500000 },
    { layer: 4, name: "Xích Diễm Vòm (Vòm Lửa Đỏ)", baseHp: 10000000 },
    { layer: 5, name: "Huyền Băng Vòm (Vòm Băng Đen)", baseHp: 80000000 },
    { layer: 6, name: "Tử Tiêu Vòm (Vòm Mây Tím)", baseHp: 500000000 },
    { layer: 7, name: "Hỗn Độn Vòm (Vòm Hỗn Độn)", baseHp: 3000000000 },
    { layer: 8, name: "Thái Cổ Vòm (Vòm Thái Cổ)", baseHp: 20000000000 },
    { layer: 9, name: "Vĩnh Hằng Vòm (Vòm Vĩnh Hằng)", baseHp: 150000000000 }
];

// 4 Loại Thần Chùy (Arsenal)
const HAMMERS = {
    1: { id: 1, name: "Lôi Đình Chùy", icon: "⚡", trait: "+3 Cộng Hưởng", k_hammer: 0.85, res_bonus: 3, ore_bonus: 0 },
    2: { id: 2, name: "Viêm Dương Chùy", icon: "🔥", trait: "Thiêu Đốt & +30% Quặng", k_hammer: 1.0, res_bonus: 1, ore_bonus: 0.3 },
    3: { id: 3, name: "Trọng Lực Chùy", icon: "🌌", trait: "x12 Khi Trúng Hoàng Kim", k_hammer: 12.0, res_bonus: 1, ore_bonus: 0 },
    4: { id: 4, name: "Huyền Âm Chùy", icon: "🎵", trait: "+15% Buff Cộng Đồng", k_hammer: 0.7, res_bonus: 1, ore_bonus: 0.1 }
};

class CelestialForgeGame {
    constructor() {
        // Tài nguyên người chơi
        this.skyIron = 0;             // Vụn Thiên Thiết
        this.domeShards = 0;          // Tinh Thể Thiên Cấm
        this.celestialCores = 0;       // Thiên Hỏa Tâm
        this.eclipseEssence = 0;       // Tinh Hoa Nguyệt Thực (Ca Đêm)
        this.lifetimeIron = 0;         // Tổng quặng tích lũy toàn bộ game
        this.playerDamageDealt = 0;    // Tổng sát thương người chơi đã đóng góp

        // Cấp búa và Đe
        this.hammerLevel = 1;
        this.activeHammer = 1;

        // Chuyển Sinh & Cây Kỹ Năng Thần Hồn (Prestige)
        this.spiritPoints = 0;         // SP hiện có
        this.spiritPointsClaimed = 0;  // Tổng SP đã nhận qua các lần
        this.talents = {
            thanLuc: 0,                // Thần Lực Quán Thế (Damage & Ore)
            nhanQuan: 0,               // Nhãn Quan Thợ Rèn (Mở rộng Điểm Hoàng Kim)
            tamPhap: 0,                // Khôi Lỗi Tâm Pháp (Offline Idle rate)
            tietKiem: 0                // Thiên Công Tiết Kiệm (Giảm giá búa)
        };

        // Bộ đếm Pity (Bảo hiểm nhân phẩm)
        this.pityCoresCounter = 0;     // Soft Pity: 120, Hard Pity: 149
        this.goldenStreak = 0;         // Chuỗi gõ Hoàng Kim liên tiếp

        // Mở khóa tính năng theo tiến độ (Progressive Disclosure / Onboarding)
        this.totalStrikes = 0;         // Tổng số nhát búa đã nện
        this.onboardingStage = 0;      // 0: Khởi đầu, 1: Thanh Nhịp Điệu, 2: Cộng Hưởng & Vũ Khí, 3: Toàn Bộ
        this.skipOnboarding = false;   // Người chơi chủ động bấm Bỏ Qua Hướng Dẫn

        // Trạng thái Thanh Nhịp Điệu (Forge Rhythm Bar)
        this.cursorPos = 0;            // 0 -> 100%
        this.cursorDirection = 1;      // 1: tới, -1: lùi
        this.cursorSpeed = 65;         // % / giây (chu kỳ ~1.5s)
        this.sweetSpotCenter = 68;     // Tọa độ Điểm Hoàng Kim (%)
        this.baseSweetSpotWidth = 14;  // Độ rộng cơ bản (%)

        // Trạng thái Cuồng Nhiệt (Overdrive Fever)
        this.overdriveActive = false;
        this.overdriveTimeLeft = 0;

        // Trạng thái Mái Vòm Thiên Cấm (Client-Side Interpolation & 2Hz Sync)
        this.domeLayer = 1;
        this.domeMaxHp = 50000;        // 50K HP Tầng 1 (Hợp lý cho chơi đơn & lên cấp)
        this.domeCurrentHp = 50000;
        this.domeTargetHp = 50000;
        this.resonance = 0;
        this.resonanceReq = 100;       // Tích 100 nhát búa kích hoạt Phá Giáp
        this.goldenShowerUntil = 0;    // Timestamp kết thúc 15 Phút Mưa Thiên Lộc (Phase 4)
        this.domeName = "Thiết Vân Vòm (Vòm Mây Sắt)";
        this.ccu = 1;                  // Số thợ rèn online (1 ở chế độ độc hành)
        this.serverDps = 0;            // DPS server (0 khi độc hành, chỉ trừ máu khi người chơi nện!)

        // WebSocket State (Phase 3)
        this.ws = null;
        this.isOnline = false;
        this.wsReconnectTimer = null;

        // Định danh & Tabs
        this.username = localStorage.getItem("phatroi_user") || `Thợ Rèn #${Math.floor(Math.random() * 8999 + 1000)}`;
        this.activeTab = 'forge';

        // Bảng Vàng (Leaderboard giả lập chuẩn TAD)
        this.topContributors = [
            { name: "Sơn Lâm", dmg: 142500000 },
            { name: "Hắc Báo", dmg: 128900000 },
            { name: "Thiên Kình", dmg: 114200000 },
            { name: "Ngọc Kiếm", dmg: 98400000 },
            { name: "Thiết Cốt", dmg: 86500000 },
            { name: "Quang Khải", dmg: 72000000 },
            { name: "Bạch Sa", dmg: 64100000 },
            { name: "Hàn Băng", dmg: 55400000 },
            { name: "Lôi Chấn", dmg: 48900000 }
        ];

        // Đài Tưởng Niệm Vĩnh Hằng (Hall of Eternity - Lịch sử các tầng đã vỡ)
        this.hallOfFame = [
            {
                layer: "Khởi Nguyên",
                name: "Thái Sơ Mái Vòm (Kỷ Nguyên Cổ)",
                shatteredAt: "2026-10-31",
                lastHitPlayer: "Bàn Cổ Thợ Rèn",
                topDamager: "Vạn Cổ Đệ Nhất (500.0M)"
            }
        ];

        this.lastFrameTime = performance.now();
        this.init();
    }

    init() {
        this.loadSave();
        this.bindEvents();
        this.setupFxCanvas();
        this.updateNightWatchStatus();
        this.updateNetworkBadge(false);
        this.fetchHallOfFame();
        this.connectWebSocket();
        this.renderAll();

        // Vòng lặp đồ họa 60 FPS
        requestAnimationFrame((t) => this.animationLoop(t));

        // Nếu offline, chạy giả lập Server Tick 2Hz (500ms)
        setInterval(() => {
            if (!this.isOnline) {
                this.serverTick2HzSimulation();
            }
        }, 500);

        // Auto Save mỗi 3 giây
        setInterval(() => this.saveGame(), 3000);

        // Kiểm tra giờ trực đêm mỗi phút
        setInterval(() => this.updateNightWatchStatus(), 60000);

        // Kiểm tra thưởng offline khi mở lại
        this.checkOfflineProgress();
    }

    // =========================================================================
    // PHASE 3 & 4: WEBSOCKET GATEWAY & REST API INTEGRATION
    // =========================================================================
    async fetchHallOfFame() {
        try {
            const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
            const protocol = window.location.protocol === 'https:' ? 'https:' : 'http:';
            const endpoint = isLocal ? 'http://localhost:8080/api/hall-of-fame' : `${protocol}//api.phatroi.com/api/hall-of-fame`;
            const res = await fetch(endpoint, { mode: 'cors' });
            if (res.ok) {
                const data = await res.json();
                if (data && Array.isArray(data.hallOfFame) && data.hallOfFame.length > 0) {
                    this.hallOfFame = data.hallOfFame;
                    if (data.currentLayer) this.domeLayer = data.currentLayer;
                    if (data.currentDomeName) this.domeName = data.currentDomeName;
                    this.renderLeaderboardTab();
                    this.renderFirmamentStatus();
                }
            }
        } catch (e) {
            // Standalone or offline fallback
        }
    }

    connectWebSocket() {
        try {
            const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            // Cổng 8080 cho localhost, hoặc wss://api.phatroi.com cho production
            const endpoint = isLocal ? 'ws://localhost:8080' : `${protocol}//api.phatroi.com`;

            this.ws = new WebSocket(endpoint);

            this.ws.onopen = () => {
                this.isOnline = true;
                this.updateNetworkBadge(true);
                this.pushTicker(`🌐 [MẠNG LƯỚI TOÀN DÂN] Đã kết nối thành công tới WebSocket Gateway!`);
            };

            this.ws.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    if (data.type === 'init') {
                        if (data.layer) this.domeLayer = Number(data.layer);
                        if (data.name) this.domeName = data.name;
                        if (data.hp) this.domeTargetHp = Number(data.hp);
                        if (data.maxHp) this.domeMaxHp = Number(data.maxHp);
                        if (data.res) this.resonance = Number(data.res);
                        if (data.resReq) this.resonanceReq = Number(data.resReq);
                        if (data.shatterUntil) this.shatterUntil = Number(data.shatterUntil) * 1000;
                        if (data.goldenShowerUntil) this.goldenShowerUntil = Number(data.goldenShowerUntil);
                    } else if (data.hp) {
                        // Nhận Broadcast 2Hz từ Server
                        if (data.layer) this.domeLayer = Number(data.layer);
                        if (data.name) this.domeName = data.name;
                        this.domeTargetHp = Number(data.hp);
                        if (data.maxHp) this.domeMaxHp = Number(data.maxHp);
                        this.resonance = Number(data.res);
                        this.resonanceReq = Number(data.resReq);
                        this.serverDps = Number(data.dps);
                        this.ccu = Number(data.ccu);
                        if (data.shatter_sec > 0) {
                            this.shatterUntil = Date.now() + (data.shatter_sec * 1000);
                        }
                        if (typeof data.golden_shower_sec !== 'undefined') {
                            if (data.golden_shower_sec > 0) {
                                this.goldenShowerUntil = Date.now() + (data.golden_shower_sec * 1000);
                            } else if (this.goldenShowerUntil > Date.now()) {
                                this.goldenShowerUntil = 0;
                            }
                        }

                        // Lên lịch render các đòn đánh FX của cộng đồng từ mảng fx: [Lôi, Hỏa, Trọng Lực, Huyền Âm]
                        if (Array.isArray(data.fx)) {
                            data.fx.forEach((count, hIdx) => {
                                for (let i = 0; i < Math.min(6, count); i++) {
                                    const delay = Math.random() * 450;
                                    setTimeout(() => this.spawnStrikeFx(hIdx + 1, false), delay);
                                }
                            });
                        }
                    }
                    this.renderDomeHp();
                    this.renderFirmamentStatus();
                } catch (e) {
                    console.warn("Lỗi phân giải gói tin WebSocket:", e);
                }
            };

            this.ws.onerror = () => {
                this.handleWsDisconnect();
            };

            this.ws.onclose = () => {
                this.handleWsDisconnect();
            };
        } catch (e) {
            this.handleWsDisconnect();
        }
    }

    handleWsDisconnect() {
        this.isOnline = false;
        this.updateNetworkBadge(false);
        // Tự động thử kết nối lại sau 15 giây
        if (!this.wsReconnectTimer) {
            this.wsReconnectTimer = setTimeout(() => {
                this.wsReconnectTimer = null;
                this.connectWebSocket();
            }, 15000);
        }
    }

    updateNetworkBadge(online) {
        const modeBadge = document.getElementById('gameModeBadge');
        const liveNetBadge = document.getElementById('liveNetBadge');
        const ccuEl = document.getElementById('ccuText');
        const dpsEl = document.getElementById('dpsText');

        if (online) {
            if (modeBadge) {
                modeBadge.style.background = 'rgba(16, 185, 129, 0.15)';
                modeBadge.style.borderColor = 'rgba(16, 185, 129, 0.4)';
                modeBadge.style.color = '#6ee7b7';
                modeBadge.innerText = '🌐 CHẾ ĐỘ: VẠN DÂN (CO-OP)';
            }
            if (liveNetBadge) {
                liveNetBadge.className = 'ticker-icon connected';
                liveNetBadge.innerText = '🟢 LIVE · ĐỒNG BỘ SERVER:';
            }
            if (ccuEl) ccuEl.innerText = `🔥 ${this.ccu} Thợ Rèn`;
            if (dpsEl) dpsEl.innerText = `${formatNum(this.serverDps)} DMG/s`;
        } else {
            if (modeBadge) {
                modeBadge.style.background = 'rgba(168, 85, 247, 0.15)';
                modeBadge.style.borderColor = 'rgba(168, 85, 247, 0.4)';
                modeBadge.style.color = '#d8b4fe';
                modeBadge.innerText = '🎮 CHẾ ĐỘ: ĐỘC HÀNH (SOLO)';
            }
            if (liveNetBadge) {
                liveNetBadge.className = 'ticker-icon offline';
                liveNetBadge.innerText = '⚪ NGOẠI TUYẾN (OFFLINE):';
            }
            if (ccuEl) ccuEl.innerText = `👤 1 Thợ Rèn`;
            const currentDmg = this.calcFinalDamage('normal', false);
            if (dpsEl) dpsEl.innerText = `Sức đập: ${formatNum(currentDmg)} DMG`;
        }
    }

    // =========================================================================
    // HỆ THỐNG TOÁN HỌC & CÂY KỸ NĂNG THẦN HỒN TIỆM CẬN (MMD)
    // =========================================================================

    getCostDiscount() {
        const lv = this.talents.tietKiem;
        return 0.50 * (1 - Math.exp(-0.06 * lv));
    }

    getSweetSpotWidth() {
        const lv = this.talents.nhanQuan;
        const bonus = 18 * (1 - Math.exp(-0.08 * lv));
        return this.baseSweetSpotWidth + bonus;
    }

    getSpiritDamageBonus() {
        const lv = this.talents.thanLuc;
        const talentBonus = 0.25 * lv * Math.pow(1.05, lv);
        const baseSpBonus = this.spiritPointsClaimed * 0.10;
        return talentBonus + baseSpBonus;
    }

    getIdleEfficiency() {
        const lv = this.talents.tamPhap;
        const bonus = 0.45 * (1 - Math.exp(-0.07 * lv));
        return 0.40 + bonus;
    }

    calcHammerUpgradeCost(L) {
        const discount = this.getCostDiscount();
        return Math.floor(10 * Math.pow(1.18, L - 1) * (1 - discount));
    }

    calcIronDrop(L, m_rhythm) {
        const hammer = HAMMERS[this.activeHammer];
        const b_ore = hammer.ore_bonus + (this.talents.thanLuc * 0.15);
        let drop = Math.floor(2 * Math.pow(1.11, L - 1) * m_rhythm * (1 + b_ore));
        
        // Phase 4: Sự kiện 15 Phút Mưa Thiên Lộc (x5 quặng toàn server)
        if (Date.now() < this.goldenShowerUntil) {
            drop *= 5;
        }

        return Math.max(1, drop);
    }

    calcMilestoneMultiplier(L) {
        const m10 = Math.floor(L / 10);
        const m25 = Math.floor(L / 25);
        return Math.pow(2, m10) * Math.pow(3, m25);
    }

    calcBaseDamage(L) {
        const milestone = this.calcMilestoneMultiplier(L);
        return Math.floor(10 * Math.pow(1.11, L - 1) * milestone);
    }

    calcFinalDamage(zone, isCrit) {
        const base = this.calcBaseDamage(this.hammerLevel);
        const hammer = HAMMERS[this.activeHammer];

        let k_rhythm = 1.0;
        if (this.overdriveActive) k_rhythm = 1.8;
        else if (zone === 'golden') k_rhythm = 3.5;
        else if (zone === 'cold') k_rhythm = 0.5;

        let k_hammer = hammer.k_hammer;
        if (this.activeHammer === 3 && zone !== 'golden') {
            k_hammer = 0.2;
        }

        const k_crit = isCrit ? 2.5 : 1.0;
        const b_spirit = 1 + this.getSpiritDamageBonus();

        const isShattered = Date.now() < this.shatterUntil;
        const k_armor = isShattered ? 3.0 : 0.10;

        let finalDmg = base * k_rhythm * k_hammer * k_crit * b_spirit * k_armor;
        return Math.max(1, Math.floor(finalDmg));
    }

    calcTotalPrestigeSP() {
        if (this.lifetimeIron < 1000000) return 0;
        return Math.floor(12 * Math.pow(this.lifetimeIron / 1000000, 0.24));
    }

    calcClaimableSP() {
        return Math.max(0, this.calcTotalPrestigeSP() - this.spiritPointsClaimed);
    }

    triggerPrestige() {
        const gain = this.calcClaimableSP();
        if (gain <= 0 && this.hammerLevel < 75) {
            this.openModal(
                "CHƯA ĐỦ ĐIỀU KIỆN TÔI LUYỆN",
                "Bạn cần đạt tối thiểu <b>Cấp Búa 75</b> hoặc tích lũy hơn <b>1.000.000 Vụn Thiên Thiết</b> để có thể ngưng tụ Điểm Thần Hồn!"
            );
            return;
        }

        const confirmRebirth = confirm(
            `Tôi Luyện Thần Hồn sẽ ném Búa hiện tại vào Lò Hỗn Độn để quay về Cấp 1 và Vụn Thiên Thiết = 0.\n\nĐổi lại, bạn nhận được ${gain} ĐIỂM THẦN HỒN để nâng cấp Cổ Ngữ Vĩnh Viễn!\n\nBạn có chắc chắn muốn chuyển sinh không?`
        );
        if (!confirmRebirth) return;

        this.spiritPoints += gain;
        this.spiritPointsClaimed += gain;
        this.skyIron = 0;
        this.hammerLevel = 1;
        this.goldenStreak = 0;

        window.soundManager.playRebirthGong();
        this.saveGame();
        this.renderAll();

        this.openModal(
            "TÔI LUYỆN THẦN HỒN THÀNH CÔNG!",
            `Bạn đã tái sinh với thể phách thợ rèn tối thượng và nhận được <b>+${gain} Điểm Thần Hồn</b>!<br>Hãy vào tab 'Thần Hồn' để mở khóa các đặc quyền Cổ Ngữ.`
        );
    }

    upgradeTalent(talentKey) {
        const lv = this.talents[talentKey];
        const costs = {
            thanLuc: Math.floor(2 * Math.pow(1.35, lv)),
            nhanQuan: Math.floor(5 * Math.pow(1.50, lv)),
            tamPhap: Math.floor(4 * Math.pow(1.45, lv)),
            tietKiem: Math.floor(5 * Math.pow(1.55, lv))
        };
        const cost = costs[talentKey] || 9999;

        if (this.spiritPoints >= cost) {
            this.spiritPoints -= cost;
            this.talents[talentKey]++;
            window.soundManager.playUpgrade();
            this.renderAll();
        }
    }

    // =========================================================================
    // THAO TÁC NỆN BÚA & GỬI GÓI TIN WEBSOCKET
    // =========================================================================

    updateNightWatchStatus() {
        const hour = new Date().getHours();
        const isNight = hour >= 0 && hour < 6;
        const badge = document.getElementById('nightBadge');
        if (badge) {
            badge.style.display = isNight ? 'flex' : 'none';
        }
        this.isNightWatch = isNight;
    }

    handleStrike(event = null) {
        window.soundManager.ensureContext();
        this.totalStrikes++;

        // 1. Chế độ Overdrive Fever
        if (this.overdriveActive) {
            this.executeOverdriveStrike(event);
            return;
        }

        // 2. Canh nhịp
        const currentWidth = this.getSweetSpotWidth();
        const diff = Math.abs(this.cursorPos - this.sweetSpotCenter);
        const halfWidth = currentWidth / 2;

        let zone = 'cold';
        let m_rhythm = 0.3;

        // Nếu đang ở Giai đoạn 0 (chưa mở khóa Thanh Nhịp Điệu), luôn tính chuẩn Warm để người mới không bị phạt
        if (this.onboardingStage === 0 && !this.skipOnboarding) {
            zone = 'warm';
            m_rhythm = 1.0;
            this.goldenStreak = 0;
        } else if (diff <= halfWidth) {
            zone = 'golden';
            m_rhythm = 2.5;
            this.goldenStreak++;
        } else if (diff <= halfWidth * 2.5) {
            zone = 'warm';
            m_rhythm = 1.0;
            this.goldenStreak = 0;
        } else {
            zone = 'cold';
            m_rhythm = 0.3;
            this.goldenStreak = 0;
        }

        let critChance = zone === 'golden' ? 0.20 : 0.05;
        if (this.isNightWatch) critChance = 1.0;
        const isCrit = Math.random() < critChance;

        const damage = this.calcFinalDamage(zone, isCrit);
        const ironEarned = this.calcIronDrop(this.hammerLevel, m_rhythm);

        this.skyIron += ironEarned;
        this.lifetimeIron += ironEarned;
        this.playerDamageDealt += damage;

        // Kiểm tra tiến trình mở khóa Onboarding
        this.checkOnboardingProgression();

        // GỬI GÓI TIN HÀNH ĐỘNG LÊN WEBSOCKET GATEWAY (~24 BYTES)
        if (this.isOnline && this.ws && this.ws.readyState === WebSocket.OPEN) {
            const offsetMs = Math.round(diff * 15); // Ước lượng độ lệch ms
            this.ws.send(JSON.stringify([1, offsetMs, this.activeHammer]));
        }

        window.soundManager.playAnvilStrike(zone, isCrit);
        this.rollDrops(zone);

        const resAdd = HAMMERS[this.activeHammer].res_bonus;
        this.addResonance(resAdd);

        // Optimistic UI: Rút máu cục bộ trước khi nhận broadcast
        this.domeTargetHp = Math.max(0, this.domeTargetHp - damage);

        this.showFloatingDamage(event, damage, zone, isCrit);
        this.triggerAnvilBounce();
        this.spawnStrikeFx(this.activeHammer, true);

        if (zone === 'golden') {
            this.shiftSweetSpot();
        }

        if (this.goldenStreak >= 8) {
            this.triggerOverdrive();
        }

        this.renderAll();
    }

    executeOverdriveStrike(event) {
        this.totalStrikes++;
        const isCrit = Math.random() < 0.25;
        const damage = this.calcFinalDamage('golden', isCrit);
        const ironEarned = this.calcIronDrop(this.hammerLevel, 1.8);

        this.skyIron += ironEarned;
        this.lifetimeIron += ironEarned;
        this.playerDamageDealt += damage;
        this.checkOnboardingProgression();

        if (this.isOnline && this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify([1, 0, this.activeHammer]));
        }

        window.soundManager.playOverdriveStrike();
        this.domeTargetHp = Math.max(0, this.domeTargetHp - damage);
        this.addResonance(2);

        this.showFloatingDamage(event, damage, 'crit', isCrit);
        this.spawnStrikeFx(this.activeHammer, true);
        this.triggerAnvilBounce();
    }

    shiftSweetSpot() {
        this.sweetSpotCenter = Math.floor(45 + Math.random() * 35);
        const el = document.getElementById('goldenZone');
        const width = this.getSweetSpotWidth();
        if (el) {
            el.style.left = `${this.sweetSpotCenter - width / 2}%`;
            el.style.width = `${width}%`;
        }
    }

    triggerOverdrive() {
        this.overdriveActive = true;
        this.overdriveTimeLeft = 10.0;
        this.goldenStreak = 0;
        window.soundManager.playOverdriveStart();

        const arena = document.getElementById('anvilArena');
        const banner = document.getElementById('overdriveBanner');
        if (arena) arena.classList.add('overdrive-mode');
        if (banner) banner.style.display = 'block';

        this.pushTicker(`🔥 [OVERDRIVE] ${this.username} vừa kích hoạt Cuồng Nhiệt Bão Sấm Sét 10s!`);
    }

    rollDrops(zone) {
        if (zone !== 'golden') return;

        const shardChance = Math.min(0.35, 0.08 + 0.005 * this.goldenStreak);
        if (Math.random() < shardChance) {
            this.domeShards++;
        }

        this.pityCoresCounter++;
        let coreChance = 0.005;
        if (this.pityCoresCounter > 120) {
            coreChance = 0.005 + (this.pityCoresCounter - 120) * 0.035;
        }
        if (this.pityCoresCounter >= 149 || Math.random() < coreChance) {
            this.celestialCores++;
            this.pityCoresCounter = 0;
            this.pushTicker(`⭐ [BẢO HIỂM THẦN TÂM] Bạn vừa đập rơi 1 Thiên Hỏa Tâm!`);
        }

        if (this.isNightWatch && Math.random() < 0.15) {
            this.eclipseEssence++;
            this.pushTicker(`🌙 [TRỰC ĐÊM] Bạn vừa thu hoạch được 1 Tinh Hoa Nguyệt Thực!`);
        }
    }

    addResonance(amount) {
        this.resonance += amount;
        if (this.resonance >= this.resonanceReq) {
            this.resonance = 0;
            this.shatterUntil = Date.now() + 60000;
            window.soundManager.playFirmamentShatter();
            this.triggerShatterFlash();
            this.pushTicker(`⚡ [CỘNG HƯỞNG VẠN DÂN] Phá vỡ Giáp Thần Lực! Toàn server x3 Sát Thương trong 60 giây!`);
        }
    }

    triggerShatterFlash() {
        const flash = document.getElementById('shatterFlash');
        if (flash) {
            flash.classList.add('active');
            setTimeout(() => flash.classList.remove('active'), 400);
        }
    }

    // =========================================================================
    // NÂNG CẤP BÚA & TABS
    // =========================================================================
    upgradeHammer() {
        const cost = this.calcHammerUpgradeCost(this.hammerLevel);
        if (this.skyIron >= cost) {
            this.skyIron -= cost;
            this.hammerLevel++;
            window.soundManager.playUpgrade();
            this.checkOnboardingProgression();
            this.renderAll();
        }
    }

    switchHammer(id) {
        this.activeHammer = parseInt(id);
        document.querySelectorAll('.hammer-btn').forEach(b => {
            b.classList.toggle('active', parseInt(b.getAttribute('data-id')) === this.activeHammer);
        });
        this.renderAll();
    }

    switchTab(tabKey) {
        if (tabKey === 'prestige' && this.onboardingStage < 3 && !this.skipOnboarding) {
            this.pushTicker("🔒 Tính năng Thần Hồn sẽ mở khóa khi bạn đạt Cấp búa 15 hoặc 100 nhát búa!");
            return;
        }
        this.activeTab = tabKey;
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.toggle('active', btn.getAttribute('data-tab') === tabKey);
        });
        document.querySelectorAll('.tab-pane').forEach(pane => {
            pane.classList.toggle('active', pane.getAttribute('id') === `pane-${tabKey}`);
        });
        this.renderAll();
    }

    // =========================================================================
    // CLIENT LERP 60 FPS & ANIMATION LOOP
    // =========================================================================
    animationLoop(now) {
        const dt = (now - this.lastFrameTime) / 1000;
        this.lastFrameTime = now;

        if (!this.overdriveActive) {
            this.cursorPos += this.cursorDirection * this.cursorSpeed * dt;
            if (this.cursorPos >= 100) {
                this.cursorPos = 100;
                this.cursorDirection = -1;
            } else if (this.cursorPos <= 0) {
                this.cursorPos = 0;
                this.cursorDirection = 1;
            }
            const cursorEl = document.getElementById('rhythmCursor');
            if (cursorEl) cursorEl.style.left = `${this.cursorPos}%`;
        } else {
            this.overdriveTimeLeft -= dt;
            const timerEl = document.getElementById('overdriveTimer');
            if (timerEl) timerEl.innerText = `${Math.max(0, this.overdriveTimeLeft).toFixed(1)}s`;

            if (this.overdriveTimeLeft <= 0) {
                this.overdriveActive = false;
                const arena = document.getElementById('anvilArena');
                const banner = document.getElementById('overdriveBanner');
                if (arena) arena.classList.remove('overdrive-mode');
                if (banner) banner.style.display = 'none';
            }
        }

        // Nội suy tuyến tính (Lerp) 60 FPS mượt mà
        if (Math.abs(this.domeCurrentHp - this.domeTargetHp) > 0.5) {
            this.domeCurrentHp += (this.domeTargetHp - this.domeCurrentHp) * 0.15;
            this.renderDomeHp();
        } else if (this.domeCurrentHp !== this.domeTargetHp) {
            this.domeCurrentHp = this.domeTargetHp;
            this.renderDomeHp();
        }

        // Phase 4: Sự kiện 15 Phút Mưa Thiên Lộc (x5 quặng)
        const showerBanner = document.getElementById('goldenShowerBanner');
        const showerTimer = document.getElementById('showerTimerText');
        if (Date.now() < this.goldenShowerUntil) {
            if (showerBanner) showerBanner.style.display = 'block';
            if (showerTimer) {
                const secLeft = Math.max(0, Math.ceil((this.goldenShowerUntil - Date.now()) / 1000));
                const m = Math.floor(secLeft / 60).toString().padStart(2, '0');
                const s = (secLeft % 60).toString().padStart(2, '0');
                showerTimer.innerText = `${m}:${s}`;
            }
        } else {
            if (showerBanner) showerBanner.style.display = 'none';
        }

        requestAnimationFrame((t) => this.animationLoop(t));
    }

    // =========================================================================
    // MÔ PHỎNG CỤC BỘ KHI NGOẠI TUYẾN (OFFLINE STANDBY SIMULATION)
    // =========================================================================
    serverTick2HzSimulation() {
        // Tuyệt đối không tự trừ máu khi chơi đơn/ngoại tuyến (Máu chỉ giảm khi người chơi nện búa!)
        if (this.isOnline && this.serverDps > 0) {
            const serverDamageTick = (this.serverDps / 2);
            this.domeTargetHp = Math.max(0, this.domeTargetHp - serverDamageTick);
        }

        const hpPct = this.domeTargetHp / this.domeMaxHp;
        const card = document.getElementById('firmamentCard');
        if (card) {
            card.classList.toggle('final-phase', hpPct <= 0.05);
        }

        if (this.domeTargetHp <= 0) {
            this.handleFirmamentShattered();
        }

        this.renderFirmamentStatus();
    }

    handleFirmamentShattered() {
        const shatteredLayer = this.domeLayer;
        const shatteredName = this.domeName;

        // Lưu vào Đài Tưởng Niệm Lịch Sử
        this.hallOfFame.unshift({
            layer: shatteredLayer,
            name: shatteredName,
            maxHp: this.domeMaxHp,
            shatteredAt: new Date().toLocaleDateString('vi-VN'),
            lastHitPlayer: this.username,
            topContributors: [...this.topContributors].slice(0, 3)
        });

        // Kích hoạt 15 Phút Mưa Thiên Lộc (x5 quặng rèn toàn server)
        this.goldenShowerUntil = Date.now() + (15 * 60 * 1000);

        // Phần thưởng phá vỡ Mái Vòm cho người chơi
        const shardReward = 500 * shatteredLayer;
        this.domeShards += shardReward;
        this.celestialCores += 1;

        // Tiến lên tầng tiếp theo trong Cửu Trọng Thiên Cấm
        this.domeLayer = Math.min(9, this.domeLayer + 1);
        const nextCfg = CELESTIAL_LAYERS[this.domeLayer - 1] || { name: `Tầng ${this.domeLayer}`, baseHp: this.domeMaxHp * 3.5 };
        this.domeName = nextCfg.name;
        this.domeMaxHp = nextCfg.baseHp;
        this.domeCurrentHp = this.domeMaxHp;
        this.domeTargetHp = this.domeMaxHp;
        this.resonance = 0;

        window.soundManager.playFirmamentShatter();
        this.triggerShatterFlash();
        this.saveGame();
        this.renderAll();

        this.openModal(
            "MÁI VÒM THIÊN CẤM SẬP ĐỔ!",
            `Toàn thể thợ rèn đã đập tan nát <b>${shatteredName} (Tầng ${shatteredLayer})</b>!<br><br>
            • <b>Đệ Nhất Phá Thiên Giả (Last Hit)</b>: Khắc tên vàng <b>${this.username}</b> vĩnh viễn lên Đài Tưởng Niệm Vĩnh Hằng!<br>
            • <b>Thưởng Phá Vòm</b>: Nhận ngay <b>+${formatNum(shardReward)} Tinh Thể Thiên Cấm</b> & <b>+1 Thiên Hỏa Tâm</b>!<br>
            • <b>Đại Lộc Toàn Server</b>: Kích hoạt <b>15 Phút Mưa Thiên Lộc (x5 Sản Lượng Quặng)</b>!`
        );
    }

    // =========================================================================
    // CANVAS FX RENDERING
    // =========================================================================
    setupFxCanvas() {
        const canvas = document.getElementById('fxCanvas');
        if (!canvas) return;
        this.canvasCtx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        window.addEventListener('resize', () => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
            this.initHorizonFires();
        });

        this.fxParticles = [];
        this.initHorizonFires();

        const renderFx = () => {
            this.canvasCtx.clearRect(0, 0, canvas.width, canvas.height);
            this.renderHorizonFires();

            // Phase 4: Sinh hạt Mưa Thiên Lộc (Golden Rain) khi sự kiện đang diễn ra
            if (Date.now() < this.goldenShowerUntil && Math.random() < 0.45) {
                this.fxParticles.push({
                    x: Math.random() * canvas.width,
                    y: -10,
                    speedX: (Math.random() - 0.5) * 1.5,
                    speedY: -(Math.random() * 4 + 2), // Rơi từ trên trời xuống
                    size: Math.random() * 3 + 1.5,
                    alpha: 1.0,
                    color: '#fbbf24'
                });
            }

            for (let i = this.fxParticles.length - 1; i >= 0; i--) {
                const p = this.fxParticles[i];
                p.y -= p.speedY;
                p.x += p.speedX;
                p.alpha -= 0.02;
                if (p.alpha <= 0 || p.y < -20 || p.y > canvas.height + 20) {
                    this.fxParticles.splice(i, 1);
                    continue;
                }
                this.canvasCtx.beginPath();
                this.canvasCtx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
                this.canvasCtx.fillStyle = p.color;
                this.canvasCtx.globalAlpha = p.alpha;
                this.canvasCtx.fill();
            }
            requestAnimationFrame(renderFx);
        };
        requestAnimationFrame(renderFx);
    }

    initHorizonFires() {
        this.horizonFires = [];
        const width = window.innerWidth;
        const height = window.innerHeight;
        const fireCount = Math.floor(Math.min(80, width / 18));

        for (let i = 0; i < fireCount; i++) {
            this.horizonFires.push({
                x: Math.random() * width,
                y: height * 0.72 + (Math.random() * height * 0.22),
                radius: Math.random() * 3 + 1.5,
                baseAlpha: Math.random() * 0.4 + 0.2,
                flickerSpeed: Math.random() * 0.08 + 0.02,
                phase: Math.random() * Math.PI * 2
            });
        }
    }

    renderHorizonFires() {
        const now = Date.now() / 1000;
        this.horizonFires.forEach(f => {
            const alpha = f.baseAlpha + Math.sin(now * f.flickerSpeed * 20 + f.phase) * 0.15;
            this.canvasCtx.beginPath();
            this.canvasCtx.arc(f.x, f.y, f.radius, 0, Math.PI * 2);
            this.canvasCtx.fillStyle = '#f97316';
            this.canvasCtx.globalAlpha = Math.max(0.05, alpha);
            this.canvasCtx.fill();
        });
    }

    spawnStrikeFx(hammerId, isPlayer = false) {
        if (!this.canvasCtx) return;
        const width = window.innerWidth;
        const height = window.innerHeight;

        const colors = { 1: '#38bdf8', 2: '#ef4444', 3: '#c084fc', 4: '#f59e0b' };
        const color = colors[hammerId] || '#f59e0b';

        const originX = isPlayer ? width * 0.5 : Math.random() * width;
        const originY = isPlayer ? height * 0.68 : height * 0.75 + Math.random() * 40;

        const count = isPlayer ? 4 : 2;
        for (let i = 0; i < count; i++) {
            this.fxParticles.push({
                x: originX + (Math.random() * 40 - 20),
                y: originY,
                speedX: (Math.random() - 0.5) * 2,
                speedY: Math.random() * 12 + 10,
                size: isPlayer ? Math.random() * 3.5 + 2 : Math.random() * 2 + 1,
                alpha: 1.0,
                color: color
            });
        }
    }

    showFloatingDamage(event, dmg, zone, isCrit) {
        const arena = document.getElementById('anvilArena');
        if (!arena) return;

        const el = document.createElement('div');
        el.className = `floating-dmg ${isCrit ? 'crit' : (zone === 'golden' ? 'golden' : 'normal')}`;
        el.innerText = isCrit ? `BẠO KÍCH! +${formatNum(dmg)}` : `+${formatNum(dmg)}`;

        let x = arena.clientWidth / 2 + (Math.random() * 60 - 30);
        let y = arena.clientHeight / 2 - 20;

        el.style.left = `${x}px`;
        el.style.top = `${y}px`;
        arena.appendChild(el);

        setTimeout(() => el.remove(), 750);
    }

    triggerAnvilBounce() {
        const sprite = document.getElementById('anvilSprite');
        if (sprite) {
            sprite.style.transform = 'scale(0.88) translateY(6px)';
            setTimeout(() => sprite.style.transform = 'scale(1) translateY(0)', 70);
        }
    }

    pushTicker(text) {
        const el = document.getElementById('tickerText');
        if (el) el.innerText = text;
    }

    // =========================================================================
    // PROGRESSIVE DISCLOSURE (MỞ KHÓA TÍNH NĂNG THEO TIẾN ĐỘ)
    // =========================================================================
    checkOnboardingProgression() {
        if (this.skipOnboarding || this.onboardingStage >= 3) return;

        let targetStage = 0;

        // Giai đoạn 3: Cấp búa >= 15 HOẶC nhát búa >= 100 HOẶC có tài nguyên hiếm HOẶC đã có SP
        if (this.hammerLevel >= 15 || this.totalStrikes >= 100 || this.domeShards > 0 || this.celestialCores > 0 || this.spiritPointsClaimed > 0) {
            targetStage = 3;
        }
        // Giai đoạn 2: Nhát búa >= 40 HOẶC cấp búa >= 5
        else if (this.totalStrikes >= 40 || this.hammerLevel >= 5) {
            targetStage = 2;
        }
        // Giai đoạn 1: Nhát búa >= 15 HOẶC cấp búa >= 2
        else if (this.totalStrikes >= 15 || this.hammerLevel >= 2) {
            targetStage = 1;
        }

        if (targetStage > this.onboardingStage) {
            const unlockedStage = targetStage;
            this.onboardingStage = targetStage;
            this.handleOnboardingUnlock(unlockedStage);
        }
    }

    handleOnboardingUnlock(stage) {
        window.soundManager.playUpgrade();
        if (stage === 1) {
            this.pushTicker(`✨ [MỚI MỞ KHÓA] Thanh Canh Nhịp Điệu! Canh vạch sáng vào vùng Hoàng Kim (Vàng) khi nện búa để nhận x3.5 Sát Thương & x2.5 Quặng!`);
            const rhythm = document.getElementById('rhythmSection');
            if (rhythm) {
                rhythm.classList.add('unlock-reveal');
                setTimeout(() => rhythm.classList.remove('unlock-reveal'), 1000);
            }
        } else if (stage === 2) {
            this.pushTicker(`⚡ [MỚI MỞ KHÓA] Thanh Cộng Hưởng & Giá Treo 4 Thần Chùy (Lôi Đình, Viêm Dương, Trọng Lực, Huyền Âm)! Chuyển đổi linh hoạt theo chiến thuật!`);
            const res = document.getElementById('resonanceContainer');
            const arsenal = document.getElementById('arsenalBar');
            if (res) {
                res.classList.add('unlock-reveal');
                setTimeout(() => res.classList.remove('unlock-reveal'), 1000);
            }
            if (arsenal) {
                arsenal.classList.add('unlock-reveal');
                setTimeout(() => arsenal.classList.remove('unlock-reveal'), 1000);
            }
        } else if (stage >= 3) {
            this.pushTicker(`💎 [MỞ KHÓA TOÀN BỘ] Đầy đủ 4 Kho Tài Nguyên Cấp Cao & Con Đường Tu Luyện Thần Hồn đã khai mở!`);
            const walletGrid = document.getElementById('walletGrid');
            const prestigeTab = document.getElementById('tabBtnPrestige');
            if (walletGrid) {
                walletGrid.classList.add('unlock-reveal');
                setTimeout(() => walletGrid.classList.remove('unlock-reveal'), 1000);
            }
            if (prestigeTab) {
                prestigeTab.classList.add('unlock-reveal');
                setTimeout(() => prestigeTab.classList.remove('unlock-reveal'), 1000);
            }
        }
        this.renderOnboarding();
    }

    renderOnboarding() {
        const isFull = this.skipOnboarding || this.onboardingStage >= 3;
        const stage = isFull ? 3 : this.onboardingStage;

        const rhythmSection = document.getElementById('rhythmSection');
        const arsenalBar = document.getElementById('arsenalBar');
        const resContainer = document.getElementById('resonanceContainer');
        const walletGrid = document.getElementById('walletGrid');
        const shardsItem = document.getElementById('walletShardsItem');
        const coresItem = document.getElementById('walletCoresItem');
        const eclipseItem = document.getElementById('walletEclipseItem');
        const quickSkipBtn = document.getElementById('btnQuickSkipOnboarding');
        const prestigeTab = document.getElementById('tabBtnPrestige');

        if (stage === 0) {
            if (rhythmSection) rhythmSection.classList.add('onboarding-hidden');
            if (arsenalBar) arsenalBar.classList.add('onboarding-hidden');
            if (resContainer) resContainer.classList.add('onboarding-hidden');
            if (walletGrid) walletGrid.classList.add('stage-compact');
            if (shardsItem) shardsItem.classList.add('onboarding-hidden');
            if (coresItem) coresItem.classList.add('onboarding-hidden');
            if (eclipseItem) eclipseItem.classList.add('onboarding-hidden');
            if (quickSkipBtn) quickSkipBtn.style.display = 'inline-flex';
            if (prestigeTab) {
                prestigeTab.classList.add('locked');
                prestigeTab.title = "Mở khóa ở Cấp búa 15 hoặc 100 nhát búa";
                prestigeTab.innerHTML = "🔒 THẦN HỒN";
            }
        } else if (stage === 1) {
            if (rhythmSection) rhythmSection.classList.remove('onboarding-hidden');
            if (arsenalBar) arsenalBar.classList.add('onboarding-hidden');
            if (resContainer) resContainer.classList.add('onboarding-hidden');
            if (walletGrid) walletGrid.classList.add('stage-compact');
            if (shardsItem) shardsItem.classList.add('onboarding-hidden');
            if (coresItem) coresItem.classList.add('onboarding-hidden');
            if (eclipseItem) eclipseItem.classList.add('onboarding-hidden');
            if (quickSkipBtn) quickSkipBtn.style.display = 'inline-flex';
            if (prestigeTab) {
                prestigeTab.classList.add('locked');
                prestigeTab.title = "Mở khóa ở Cấp búa 15 hoặc 100 nhát búa";
                prestigeTab.innerHTML = "🔒 THẦN HỒN";
            }
        } else if (stage === 2) {
            if (rhythmSection) rhythmSection.classList.remove('onboarding-hidden');
            if (arsenalBar) arsenalBar.classList.remove('onboarding-hidden');
            if (resContainer) resContainer.classList.remove('onboarding-hidden');
            if (walletGrid) walletGrid.classList.add('stage-compact');
            if (shardsItem) shardsItem.classList.add('onboarding-hidden');
            if (coresItem) coresItem.classList.add('onboarding-hidden');
            if (eclipseItem) eclipseItem.classList.add('onboarding-hidden');
            if (quickSkipBtn) quickSkipBtn.style.display = 'inline-flex';
            if (prestigeTab) {
                prestigeTab.classList.add('locked');
                prestigeTab.title = "Mở khóa ở Cấp búa 15 hoặc 100 nhát búa";
                prestigeTab.innerHTML = "🔒 THẦN HỒN";
            }
        } else {
            // Stage 3 (hoặc Bỏ qua): Mở toàn bộ
            if (rhythmSection) rhythmSection.classList.remove('onboarding-hidden');
            if (arsenalBar) arsenalBar.classList.remove('onboarding-hidden');
            if (resContainer) resContainer.classList.remove('onboarding-hidden');
            if (walletGrid) walletGrid.classList.remove('stage-compact');
            if (shardsItem) shardsItem.classList.remove('onboarding-hidden');
            if (coresItem) coresItem.classList.remove('onboarding-hidden');
            if (eclipseItem) eclipseItem.classList.remove('onboarding-hidden');
            if (quickSkipBtn) quickSkipBtn.style.display = 'none';
            if (prestigeTab) {
                prestigeTab.classList.remove('locked');
                prestigeTab.title = "Tôi Luyện Thần Hồn (Prestige)";
                prestigeTab.innerHTML = "🌀 THẦN HỒN";
            }
        }
    }

    skipTutorial() {
        this.skipOnboarding = true;
        this.onboardingStage = 3;
        this.renderOnboarding();
        this.saveGame();
        this.pushTicker(`⚡ [GIAO DIỆN] Đã mở khóa hiển thị toàn bộ tính năng trò chơi!`);
        window.soundManager.playUpgrade();
    }

    // =========================================================================
    // UI RENDERING
    // =========================================================================
    renderAll() {
        this.renderWallets();
        this.renderDomeHp();
        this.renderFirmamentStatus();
        this.renderUpgradeCard();
        this.renderPrestigeTab();
        this.renderLeaderboardTab();
        this.renderOnboarding();
    }

    renderWallets() {
        const ironEl = document.getElementById('valSkyIron');
        const shardEl = document.getElementById('valDomeShards');
        const coreEl = document.getElementById('valCelestialCores');
        const eclipseEl = document.getElementById('valEclipse');

        if (ironEl) ironEl.innerText = formatNum(this.skyIron);
        if (shardEl) shardEl.innerText = formatNum(this.domeShards);
        if (coreEl) coreEl.innerText = `${this.celestialCores} (Pity: ${this.pityCoresCounter}/149)`;
        if (eclipseEl) eclipseEl.innerText = formatNum(this.eclipseEssence);

        const streakEl = document.getElementById('streakVal');
        if (streakEl) streakEl.innerText = `${this.goldenStreak}/8`;
    }

    renderDomeHp() {
        const fill = document.getElementById('domeHpFill');
        const text = document.getElementById('domeHpText');
        if (fill && text) {
            const pct = Math.max(0, Math.min(100, (this.domeCurrentHp / this.domeMaxHp) * 100));
            fill.style.width = `${pct}%`;
            fill.classList.toggle('final', pct <= 5);
            text.innerText = `${formatNum(this.domeCurrentHp)} / ${formatNum(this.domeMaxHp)} (${pct.toFixed(2)}%)`;

            const sealEl = document.getElementById('subSealText');
            if (sealEl) {
                let sealName = "Phong Ấn 1 (100% ➔ 85%)";
                if (pct <= 5) sealName = "🔥 GIAI ĐOẠN CUỐI (5% ➔ 0% SĂN LAST HIT)";
                else if (pct <= 15) sealName = "Phong Ấn 6 (15% ➔ 0%)";
                else if (pct <= 30) sealName = "Phong Ấn 5 (30% ➔ 15%)";
                else if (pct <= 50) sealName = "Phong Ấn 4 (50% ➔ 30%)";
                else if (pct <= 70) sealName = "Phong Ấn 3 (70% ➔ 50%)";
                else if (pct <= 85) sealName = "Phong Ấn 2 (85% ➔ 70%)";
                sealEl.innerText = `• ${sealName}`;
            }
        }

        const resFill = document.getElementById('resFill');
        const resText = document.getElementById('resText');
        if (resFill && resText) {
            const resPct = Math.min(100, (this.resonance / this.resonanceReq) * 100);
            resFill.style.width = `${resPct}%`;
            resText.innerText = `${formatNum(this.resonance)} / ${formatNum(this.resonanceReq)}`;
        }
    }

    renderFirmamentStatus() {
        const card = document.getElementById('firmamentCard');
        const pill = document.getElementById('domeStatusPill');
        const isShattered = Date.now() < this.shatterUntil;
        const hpPct = this.domeCurrentHp / this.domeMaxHp;
        const isFinalPhase = hpPct <= 0.05;

        if (card) {
            card.className = `firmament-card layer-${this.domeLayer} ${isShattered ? 'shatter-mode' : ''} ${isFinalPhase ? 'final-phase' : ''}`;
        }

        const nameEl = document.getElementById('domeNameText');
        const layerEl = document.getElementById('domeLayerPill');
        if (nameEl) nameEl.innerText = `🌌 Tầng ${this.domeLayer}: ${this.domeName}`;
        if (layerEl) layerEl.innerText = `Tầng ${this.domeLayer}/9`;

        if (pill) {
            if (isShattered) {
                const remainSec = Math.ceil((this.shatterUntil - Date.now()) / 1000);
                pill.className = 'dome-status-pill shattered';
                pill.innerText = `🔥 PHÁ GIÁP VẠN DÂN x3 SÁT THƯƠNG (${remainSec}s)`;
            } else {
                pill.className = 'dome-status-pill armored';
                pill.innerText = `🛡️ GIÁP THẦN LỰC (GIẢM 90% DMG)`;
            }
        }
    }

    renderUpgradeCard() {
        const cost = this.calcHammerUpgradeCost(this.hammerLevel);
        const baseDmg = this.calcBaseDamage(this.hammerLevel);
        const nextBaseDmg = this.calcBaseDamage(this.hammerLevel + 1);
        const canAfford = this.skyIron >= cost;

        const nextMilestone = this.hammerLevel < 10 ? 10 : (this.hammerLevel < 25 ? 25 : Math.ceil((this.hammerLevel + 1) / 10) * 10);

        const card = document.getElementById('hammerUpgradeCard');
        if (card) {
            card.className = `upgrade-card ${canAfford ? '' : 'disabled'}`;
            document.getElementById('upgradeLvl').innerText = `Cấp ${this.hammerLevel}`;
            document.getElementById('upgradeCost').innerText = `⚡ ${formatNum(cost)} Vụn Thiên Thiết`;
            document.getElementById('upgradeDesc').innerText = `Sát thương cơ bản: ${formatNum(baseDmg)} ➔ ${formatNum(nextBaseDmg)} (Mốc tiếp theo: Cấp ${nextMilestone})`;
        }
    }

    renderPrestigeTab() {
        const claimable = this.calcClaimableSP();
        const spEl = document.getElementById('spBalanceText');
        const claimBtn = document.getElementById('btnPrestigeClaim');

        if (spEl) spEl.innerText = `${this.spiritPoints} SP`;
        if (claimBtn) {
            claimBtn.innerText = `TÔI LUYỆN THẦN HỒN (+${claimable} SP)`;
            claimBtn.disabled = claimable <= 0 && this.hammerLevel < 75;
        }

        const talentsDef = [
            { key: 'thanLuc', name: 'Thần Lực Quán Thế', desc: '+25% Sát Thương & Quặng/cấp', costFn: (lv) => Math.floor(2 * Math.pow(1.35, lv)) },
            { key: 'nhanQuan', name: 'Nhãn Quan Thợ Rèn', desc: `Mở rộng Điểm Hoàng Kim (+${(18 * (1 - Math.exp(-0.08 * this.talents.nhanQuan))).toFixed(1)}% / Max +18%)`, costFn: (lv) => Math.floor(5 * Math.pow(1.50, lv)) },
            { key: 'tamPhap', name: 'Khôi Lỗi Tâm Pháp', desc: `Tăng công suất gõ Offline (${(this.getIdleEfficiency() * 100).toFixed(1)}% / Max 85%)`, costFn: (lv) => Math.floor(4 * Math.pow(1.45, lv)) },
            { key: 'tietKiem', name: 'Thiên Công Tiết Kiệm', desc: `Giảm chi phí nâng búa (-${(this.getCostDiscount() * 100).toFixed(1)}% / Max 50%)`, costFn: (lv) => Math.floor(5 * Math.pow(1.55, lv)) }
        ];

        talentsDef.forEach(t => {
            const lv = this.talents[t.key];
            const cost = t.costFn(lv);
            const canAfford = this.spiritPoints >= cost;

            const card = document.getElementById(`talent-${t.key}`);
            if (card) {
                card.className = `upgrade-card ${canAfford ? '' : 'disabled'}`;
                card.querySelector('.upgrade-lvl').innerText = `Cấp ${lv}`;
                card.querySelector('.upgrade-desc').innerText = t.desc;
                card.querySelector('.upgrade-cost-row').innerText = `⭐ ${cost} SP`;
            }
        });
    }

    renderLeaderboardTab() {
        const titleEl = document.getElementById('currentDomeHofTitle');
        if (titleEl) {
            titleEl.innerText = `🏆 ĐÀI TƯỞNG NIỆM TẦNG ${this.domeLayer}: ${this.domeName.toUpperCase()}`;
        }

        const container = document.getElementById('hofList');
        if (container) {
            container.innerHTML = "";
            const list = [...this.topContributors, { name: `${this.username} (Bạn)`, dmg: this.playerDamageDealt }]
                .sort((a, b) => b.dmg - a.dmg)
                .slice(0, 10);

            list.forEach((item, idx) => {
                const div = document.createElement('div');
                div.className = 'hof-item';
                div.innerHTML = `
                    <span class="hof-rank">#${idx + 1}</span>
                    <span class="hof-name">${item.name}</span>
                    <span class="hof-dmg">${formatNum(item.dmg)} DMG</span>
                `;
                container.appendChild(div);
            });
        }

        const eternityContainer = document.getElementById('eternityList');
        if (eternityContainer) {
            eternityContainer.innerHTML = "";
            if (!this.hallOfFame || this.hallOfFame.length === 0) {
                eternityContainer.innerHTML = `<div style="font-size: 0.75rem; color: #94a3b8; font-style: italic; padding: 4px;">Chưa có tầng trời nào bị đập tan. Hãy là người đầu tiên!</div>`;
            } else {
                this.hallOfFame.forEach(item => {
                    const card = document.createElement('div');
                    card.className = 'eternity-card';
                    card.innerHTML = `
                        <div class="eternity-header">
                            <span>⚡ Tầng ${item.layer}: ${item.name || item.domeName}</span>
                            <span style="font-size: 0.7rem; color: #a855f7;">${item.shatteredAt ? item.shatteredAt.slice(0, 10) : 'Kỷ Nguyên Trước'}</span>
                        </div>
                        <div class="eternity-row">
                            <span>👑 Đệ Nhất Phá Thiên (Last Hit):</span>
                            <b style="color: #38bdf8;">${item.lastHitPlayer || item.lastHit || 'Khuyết danh'}</b>
                        </div>
                        <div class="eternity-row">
                            <span>⚔️ Top Sát Thương:</span>
                            <b style="color: #fef08a;">${Array.isArray(item.topContributors) && item.topContributors[0] ? `${item.topContributors[0].name} (${formatNum(item.topContributors[0].dmg)})` : (item.topDamager || 'Sơn Lâm (142.5M)')}</b>
                        </div>
                    `;
                    eternityContainer.appendChild(card);
                });
            }
        }
    }

    // =========================================================================
    // EVENT BINDINGS
    // =========================================================================
    bindEvents() {
        const anvil = document.getElementById('anvilWrapper');
        if (anvil) {
            anvil.addEventListener('pointerdown', (e) => this.handleStrike(e));
        }

        // Global Spacebar Handler (Bắt phím SPACE toàn cục)
        window.addEventListener('keydown', (e) => {
            if (e.code === 'Space' || e.key === ' ' || e.keyCode === 32) {
                const active = document.activeElement;
                const isTyping = active && (
                    active.tagName === 'INPUT' ||
                    active.tagName === 'TEXTAREA' ||
                    active.isContentEditable
                );

                if (isTyping) return; // Cho phép gõ khoảng trắng trong ô nhập liệu (ví dụ ô dán Save)

                // Chặn hành vi mặc định (cuộn trang hoặc kích hoạt lại button đang focus)
                e.preventDefault();

                // Blur nút đang focus để tránh nhấp nháy hoặc bấm nhầm
                if (active && (active.tagName === 'BUTTON' || active.tagName === 'A' || active.getAttribute('role') === 'button')) {
                    active.blur();
                }

                if (!e.repeat) {
                    const anvilWrapper = document.getElementById('anvilWrapper');
                    if (anvilWrapper) anvilWrapper.classList.add('pressed');

                    // Kích hoạt nhát búa
                    this.handleStrike();
                }
            }
        }, { capture: true });

        window.addEventListener('keyup', (e) => {
            if (e.code === 'Space' || e.key === ' ' || e.keyCode === 32) {
                const anvilWrapper = document.getElementById('anvilWrapper');
                if (anvilWrapper) anvilWrapper.classList.remove('pressed');
            }
        }, { capture: true });

        // Tự động giải phóng focus sau khi click nút bất kỳ để phím SPACE luôn sẵn sàng
        document.addEventListener('pointerup', (e) => {
            if (e.target && (e.target.tagName === 'BUTTON' || e.target.closest('button'))) {
                const btn = e.target.tagName === 'BUTTON' ? e.target : e.target.closest('button');
                setTimeout(() => {
                    if (document.activeElement === btn) btn.blur();
                }, 50);
            }
        });

        document.querySelectorAll('.hammer-btn').forEach(btn => {
            btn.onclick = () => this.switchHammer(btn.getAttribute('data-id'));
        });

        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.onclick = () => this.switchTab(btn.getAttribute('data-tab'));
        });

        const upCard = document.getElementById('hammerUpgradeCard');
        if (upCard) {
            upCard.onclick = () => this.upgradeHammer();
        }

        const prestigeBtn = document.getElementById('btnPrestigeClaim');
        if (prestigeBtn) {
            prestigeBtn.onclick = () => this.triggerPrestige();
        }

        ['thanLuc', 'nhanQuan', 'tamPhap', 'tietKiem'].forEach(k => {
            const card = document.getElementById(`talent-${k}`);
            if (card) {
                card.onclick = () => this.upgradeTalent(k);
            }
        });

        const audioBtn = document.getElementById('btnAudio');
        if (audioBtn) {
            audioBtn.onclick = () => {
                const muted = window.soundManager.toggleMute();
                audioBtn.innerText = muted ? "🔇 TẮT ÂM" : "🔊 BẬT ÂM";
            };
        }

        const nameBtn = document.getElementById('btnName');
        if (nameBtn) {
            nameBtn.onclick = () => {
                const newName = prompt("Nhập Biệt Hiệu Thợ Rèn của bạn:", this.username);
                if (newName && newName.trim()) {
                    this.username = newName.trim();
                    localStorage.setItem("phatroi_user", this.username);
                    nameBtn.innerText = `👤 ${this.username}`;
                    this.renderAll();
                }
            };
            nameBtn.innerText = `👤 ${this.username}`;
        }

        const exportBtn = document.getElementById('btnExportSave');
        if (exportBtn) {
            exportBtn.onclick = () => {
                const data = btoa(JSON.stringify(this.getSaveState()));
                prompt("Sao chép mã lưu trữ dữ liệu của bạn bên dưới:", data);
            };
        }

        const quickSkip = document.getElementById('btnQuickSkipOnboarding');
        if (quickSkip) {
            quickSkip.onclick = () => this.skipTutorial();
        }

        const skipBtn = document.getElementById('btnSkipOnboarding');
        if (skipBtn) {
            skipBtn.onclick = () => {
                this.skipTutorial();
                alert("Đã mở khóa toàn bộ giao diện trò chơi!");
            };
        }

        const importBtn = document.getElementById('btnImportSave');
        if (importBtn) {
            importBtn.onclick = () => {
                const data = prompt("Dán mã lưu trữ dữ liệu vào đây:");
                if (!data) return;
                try {
                    const parsed = JSON.parse(atob(data));
                    if (parsed && typeof parsed.skyIron !== 'undefined') {
                        this.applyLoadedState(parsed);
                        this.saveGame();
                        this.renderAll();
                        alert("Đã khôi phục dữ liệu thành công!");
                    }
                } catch (e) {
                    alert("Mã lưu trữ không hợp lệ!");
                }
            };
        }

        const modalBtn = document.getElementById('modalBtn');
        if (modalBtn) modalBtn.onclick = () => this.closeModal();
    }

    openModal(title, body) {
        document.getElementById('modalTitle').innerText = title;
        document.getElementById('modalBody').innerHTML = body;
        document.getElementById('infoModal').classList.add('open');
    }

    closeModal() {
        document.getElementById('infoModal').classList.remove('open');
    }

    // =========================================================================
    // SAVE / OFFLINE
    // =========================================================================
    getSaveState() {
        return {
            skyIron: this.skyIron,
            domeShards: this.domeShards,
            celestialCores: this.celestialCores,
            eclipseEssence: this.eclipseEssence,
            lifetimeIron: this.lifetimeIron,
            playerDamageDealt: this.playerDamageDealt,
            hammerLevel: this.hammerLevel,
            activeHammer: this.activeHammer,
            spiritPoints: this.spiritPoints,
            spiritPointsClaimed: this.spiritPointsClaimed,
            talents: this.talents,
            domeLayer: this.domeLayer,
            domeName: this.domeName,
            domeCurrentHp: this.domeCurrentHp,
            domeMaxHp: this.domeMaxHp,
            hallOfFame: this.hallOfFame,
            goldenShowerUntil: this.goldenShowerUntil,
            totalStrikes: this.totalStrikes,
            onboardingStage: this.onboardingStage,
            skipOnboarding: this.skipOnboarding,
            lastSaveTime: Date.now()
        };
    }

    applyLoadedState(s) {
        this.skyIron = s.skyIron || 0;
        this.domeShards = s.domeShards || 0;
        this.celestialCores = s.celestialCores || 0;
        this.eclipseEssence = s.eclipseEssence || 0;
        this.lifetimeIron = s.lifetimeIron || 0;
        this.playerDamageDealt = s.playerDamageDealt || 0;
        this.hammerLevel = s.hammerLevel || 1;
        this.activeHammer = s.activeHammer || 1;
        this.spiritPoints = s.spiritPoints || 0;
        this.spiritPointsClaimed = s.spiritPointsClaimed || 0;
        this.talents = Object.assign(this.talents, s.talents || {});
        if (s.domeLayer) this.domeLayer = s.domeLayer;
        if (s.domeName) this.domeName = s.domeName;
        if (Array.isArray(s.hallOfFame) && s.hallOfFame.length > 0) this.hallOfFame = s.hallOfFame;
        if (s.goldenShowerUntil) this.goldenShowerUntil = s.goldenShowerUntil;

        this.totalStrikes = s.totalStrikes || 0;
        this.skipOnboarding = !!s.skipOnboarding;

        // Tự động mở khóa 100% nếu là người chơi cũ
        const isVeteranPlayer = (
            this.hammerLevel > 10 ||
            this.spiritPointsClaimed > 0 ||
            this.totalStrikes >= 100 ||
            this.lifetimeIron > 10000 ||
            this.playerDamageDealt > 10000 ||
            this.domeLayer > 1 ||
            this.domeShards > 0 ||
            this.celestialCores > 0 ||
            this.skipOnboarding
        );

        if (isVeteranPlayer) {
            this.onboardingStage = 3;
        } else if (typeof s.onboardingStage !== 'undefined') {
            this.onboardingStage = s.onboardingStage;
        } else {
            // Xác định stage dựa trên chỉ số hiện có
            if (this.hammerLevel >= 15 || this.totalStrikes >= 100) {
                this.onboardingStage = 3;
            } else if (this.hammerLevel >= 5 || this.totalStrikes >= 40) {
                this.onboardingStage = 2;
            } else if (this.hammerLevel >= 2 || this.totalStrikes >= 15) {
                this.onboardingStage = 1;
            } else {
                this.onboardingStage = 0;
            }
        }

        // Auto-fix cân bằng lại nếu save cũ lưu mức máu 1 tỷ của giai đoạn test
        const targetBaseHp = CELESTIAL_LAYERS[this.domeLayer - 1]?.baseHp || 50000;
        if (!s.domeMaxHp || s.domeMaxHp >= 1000000000 || (s.domeCurrentHp && s.domeCurrentHp >= 1000000000)) {
            this.domeMaxHp = targetBaseHp;
            this.domeCurrentHp = targetBaseHp;
            this.domeTargetHp = targetBaseHp;
        } else if (s.domeCurrentHp && s.domeMaxHp) {
            this.domeMaxHp = s.domeMaxHp;
            this.domeCurrentHp = Math.min(s.domeCurrentHp, s.domeMaxHp);
            this.domeTargetHp = this.domeCurrentHp;
        } else {
            this.domeMaxHp = targetBaseHp;
            this.domeCurrentHp = targetBaseHp;
            this.domeTargetHp = targetBaseHp;
        }
    }

    saveGame() {
        localStorage.setItem("phatroi_cforge_save_v2", JSON.stringify(this.getSaveState()));
    }

    loadSave() {
        const raw = localStorage.getItem("phatroi_cforge_save_v2") || localStorage.getItem("phatroi_cforge_save");
        if (raw) {
            try {
                this.applyLoadedState(JSON.parse(raw));
            } catch (e) {
                console.error("Lỗi đọc save:", e);
            }
        }
    }

    checkOfflineProgress() {
        const raw = localStorage.getItem("phatroi_cforge_save_v2");
        if (!raw) return;
        try {
            const s = JSON.parse(raw);
            if (s.lastSaveTime) {
                const diffSec = Math.floor((Date.now() - s.lastSaveTime) / 1000);
                if (diffSec > 15) {
                    const cappedSec = Math.min(86400, diffSec);
                    const efficiency = this.getIdleEfficiency();
                    const strikes = Math.floor(cappedSec / 2);
                    const ironEarned = strikes * this.calcIronDrop(this.hammerLevel, 1.0) * efficiency;
                    this.skyIron += ironEarned;
                    this.lifetimeIron += ironEarned;

                    this.openModal(
                        "DƯ NHIỆT KHÔI LỖI",
                        `Trong lúc bạn vắng mặt (${Math.floor(cappedSec / 60)} phút), Khôi Lỗi thợ rèn (hiệu suất <b>${(efficiency * 100).toFixed(0)}%</b>) đã gõ tự động <b>${strikes}</b> nhát búa và thu về <b>+${formatNum(ironEarned)} Vụn Thiên Thiết</b>!`
                    );
                }
            }
        } catch (e) {}
    }
}

window.addEventListener('DOMContentLoaded', () => {
    window.game = new CelestialForgeGame();
});
