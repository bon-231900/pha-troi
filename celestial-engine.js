// ============================================================================
// DỰ ÁN WEBGAME "PHÁ TRỜI" - THE CELESTIAL FORGE (phatroi.com)
// CORE ENGINE, STANCE MANAGER, PRESTIGE TREE, ECONOMIC MODEL & MULTIPLAYER SYNC
// Architect: Antigravity Core Engine
// UI/Audio/Canvas Partner: Gemini 4 Argon (Google AI Studio)
// ============================================================================

(function (root, factory) {
    if (typeof define === 'function' && define.amd) {
        define([], factory);
    } else if (typeof module === 'object' && module.exports) {
        module.exports = factory();
    } else {
        root.CelestialEngine = factory();
    }
}(typeof self !== 'undefined' ? self : this, function () {
    'use strict';

    // =========================================================================
    // 1. STANCE MANAGER & STANCE DEFINITIONS (Task 1)
    // =========================================================================
    const STANCE_TYPES = {
        THUNDER_PEAK: 'THUNDER_PEAK',         // Lôi Đỉnh
        SOLAR_FLAME: 'SOLAR_FLAME',           // Viêm Dương
        GRAVITY_BURST: 'GRAVITY_BURST',       // Trọng Lực
        MYSTIC_RESONANCE: 'MYSTIC_RESONANCE'  // Huyền Âm
    };

    const STANCES = {
        [STANCE_TYPES.THUNDER_PEAK]: {
            id: 1,
            key: STANCE_TYPES.THUNDER_PEAK,
            name: "Lôi Đỉnh Thế",
            title: "Lôi Đỉnh (Thunder Peak)",
            icon: "⚡",
            color: "#38bdf8",
            trait: "+3 Điểm Cộng Hưởng Phá Giáp mỗi nhát đập",
            resBonus: 3,
            oreBonus: 0.0,
            baseDmgMult: 1.0,
            goldenDmgMult: 3.5,
            desc: "Tập trung lôi đình kích hoạt xung chấn cấm chế, đẩy nhanh tốc độ Phá Giáp gấp 3 lần."
        },
        [STANCE_TYPES.SOLAR_FLAME]: {
            id: 2,
            key: STANCE_TYPES.SOLAR_FLAME,
            name: "Viêm Dương Thế",
            title: "Viêm Dương (Solar Flame)",
            icon: "🔥",
            color: "#f97316",
            trait: "Gây DoT Thiêu Đốt liên tục & +30% Quặng rèn",
            resBonus: 1,
            oreBonus: 0.30,
            baseDmgMult: 1.0,
            goldenDmgMult: 3.5,
            dotConfig: {
                durationMs: 3000,
                tickIntervalMs: 1000,
                tickDmgRatio: 0.35 // 35% base damage mỗi giây thiêu đốt
            },
            desc: "Nung chảy Thiết Vân Vòm bằng thiên hỏa, tăng sản lượng quặng khai thác và đốt cháy boss theo thời gian."
        },
        [STANCE_TYPES.GRAVITY_BURST]: {
            id: 3,
            key: STANCE_TYPES.GRAVITY_BURST,
            name: "Trọng Lực Thế",
            title: "Trọng Lực (Gravity Burst)",
            icon: "🌌",
            color: "#a855f7",
            trait: "x12 Sát Thương khi trúng Điểm Hoàng Kim",
            resBonus: 1,
            oreBonus: 0.0,
            baseDmgMult: 0.20, // Đánh trượt hoặc lệch nhịp chỉ gây 20% sát thương
            goldenDmgMult: 12.0, // Đánh chuẩn Hoàng Kim bộc phá x12 sát thương
            desc: "Dồn toàn bộ áp lực hư không vào một điểm chính xác. Cực đại sát thương bạo phát khi chuẩn nhịp."
        },
        [STANCE_TYPES.MYSTIC_RESONANCE]: {
            id: 4,
            key: STANCE_TYPES.MYSTIC_RESONANCE,
            name: "Huyền Âm Thế",
            title: "Huyền Âm (Mystic Resonance)",
            icon: "🎵",
            color: "#10b981",
            trait: "+15% Quặng & Buff Tốc Độ Tự Động Hóa (+25%)",
            resBonus: 1,
            oreBonus: 0.15,
            autoRateBonus: 0.25,
            baseDmgMult: 0.85,
            goldenDmgMult: 3.0,
            desc: "Hòa nhịp vào đạo âm trời đất, tối ưu hóa công suất khôi lỗi rèn đúc và năng suất ngoại tuyến."
        }
    };

    // =========================================================================
    // 2. CÂY KỸ NĂNG THẦN HỒN - PRESTIGE SKILL TREE (Task 3)
    // 4 Nhánh Tinh Đồ: WARRIOR, MASSES, FORTUNE, SPIRIT
    // =========================================================================
    const CONSTELLATIONS = {
        WARRIOR_PATH: 'WARRIOR_PATH', // Chiến Thần
        MASSES_PATH: 'MASSES_PATH',   // Vạn Dân
        FORTUNE_PATH: 'FORTUNE_PATH', // Thiên Phú
        SPIRIT_PATH: 'SPIRIT_PATH'    // Linh Khí
    };

    const PRESTIGE_TREE = {
        // --- NHÁNH 1: CHIẾN THẦN (WARRIOR_PATH) ---
        'warrior_1': {
            id: 'warrior_1',
            path: CONSTELLATIONS.WARRIOR_PATH,
            name: "Chiến Ý Khởi Nguyên",
            icon: "⚔️",
            tier: 1,
            maxLevel: 10,
            prerequisites: [],
            costFn: (lv) => 1 + lv,
            desc: "Tăng +20% Sát Thương Cơ Bản cho mỗi nhát đập thần chùy.",
            effectDesc: (lv) => `+${lv * 20}% Sát Thương Thần Chùy`,
            apply: (stats, lv) => { stats.damageBonus += lv * 0.20; }
        },
        'warrior_2': {
            id: 'warrior_2',
            path: CONSTELLATIONS.WARRIOR_PATH,
            name: "Khai Nhãn Thần Đồng",
            icon: "👁️",
            tier: 2,
            maxLevel: 5,
            prerequisites: [{ id: 'warrior_1', level: 3 }],
            costFn: (lv) => 2 + lv * 2,
            desc: "Nới rộng độ rộng Điểm Hoàng Kim (Sweet Spot) thêm +1.5% cung tròn mỗi cấp.",
            effectDesc: (lv) => `+${(lv * 1.5).toFixed(1)}% Độ Rộng Hoàng Kim`,
            apply: (stats, lv) => { stats.sweetSpotWidthBonus += lv * 1.5; }
        },
        'warrior_3': {
            id: 'warrior_3',
            path: CONSTELLATIONS.WARRIOR_PATH,
            name: "Liệt Phách Bạo Kích",
            icon: "💥",
            tier: 3,
            maxLevel: 5,
            prerequisites: [{ id: 'warrior_2', level: 2 }],
            costFn: (lv) => 4 + lv * 3,
            desc: "+5% Tỷ Lệ Bạo Kích & +50% Sát Thương Bạo Kích mỗi cấp.",
            effectDesc: (lv) => `+${lv * 5}% Crit Rate, +${lv * 50}% Crit DMG`,
            apply: (stats, lv) => {
                stats.critRateBonus += lv * 0.05;
                stats.critDmgBonus += lv * 0.50;
            }
        },
        'warrior_4': {
            id: 'warrior_4',
            path: CONSTELLATIONS.WARRIOR_PATH,
            name: "Vạn Quân Phá Diệt",
            icon: "⚡",
            tier: 4,
            maxLevel: 1,
            prerequisites: [{ id: 'warrior_3', level: 3 }],
            costFn: () => 15,
            desc: "Khi đạt Chuỗi Hoàng Kim từ 5 nhát trở lên, nhân đôi (x2) toàn bộ sát thương gây ra.",
            effectDesc: (lv) => lv > 0 ? "x2 Sát thương khi Chuỗi Hoàng Kim >= 5" : "Chưa kích hoạt",
            apply: (stats, lv) => { stats.comboOverdriveBonus = lv > 0; }
        },

        // --- NHÁNH 2: VẠN DÂN (MASSES_PATH) ---
        'masses_1': {
            id: 'masses_1',
            path: CONSTELLATIONS.MASSES_PATH,
            name: "Đồng Tâm Hiệp Lực",
            icon: "🤝",
            tier: 1,
            maxLevel: 5,
            prerequisites: [],
            costFn: (lv) => 1 + lv,
            desc: "Mỗi nhát búa đóng góp thêm +1 Điểm Cộng Hưởng Phá Giáp cho toàn server.",
            effectDesc: (lv) => `+${lv} Điểm Cộng Hưởng / Nhát`,
            apply: (stats, lv) => { stats.resonanceGainBonus += lv; }
        },
        'masses_2': {
            id: 'masses_2',
            path: CONSTELLATIONS.MASSES_PATH,
            name: "Hào Quang Khu Rèn",
            icon: "🛡️",
            tier: 2,
            maxLevel: 5,
            prerequisites: [{ id: 'masses_1', level: 2 }],
            costFn: (lv) => 2 + lv * 2,
            desc: "Tăng +10% Sát thương bản thân và tỏa hào quang tăng +5% cho toàn bộ đồng đội trong Khu Rèn.",
            effectDesc: (lv) => `+${lv * 10}% Solo DMG / +${lv * 5}% District Aura`,
            apply: (stats, lv) => {
                stats.districtAuraBonus += lv * 0.05;
                stats.damageBonus += lv * 0.10;
            }
        },
        'masses_3': {
            id: 'masses_3',
            path: CONSTELLATIONS.MASSES_PATH,
            name: "Triệu Hồi Thiên Lôi",
            icon: "🌩️",
            tier: 3,
            maxLevel: 2,
            prerequisites: [{ id: 'masses_2', level: 3 }],
            costFn: (lv) => 5 + lv * 5,
            desc: "Giảm ngưỡng tích lũy Phá Giáp của Mái Vòm từ 100 điểm xuống còn 90 (Cấp 1) và 80 (Cấp 2).",
            effectDesc: (lv) => `Ngưỡng Phá Giáp: ${100 - lv * 10} Điểm`,
            apply: (stats, lv) => { stats.shatterThresholdReduction += lv * 10; }
        },
        'masses_4': {
            id: 'masses_4',
            path: CONSTELLATIONS.MASSES_PATH,
            name: "Vạn Dân Triều Bái",
            icon: "👑",
            tier: 4,
            maxLevel: 1,
            prerequisites: [{ id: 'masses_3', level: 1 }],
            costFn: () => 15,
            desc: "Trong 30 giây Đại Hợp Âm, mỗi nhát gõ Perfect của bạn đóng góp x2 giá trị vào thanh Buff Toàn Cầu.",
            effectDesc: (lv) => lv > 0 ? "x2 Điểm Đại Hợp Âm toàn server" : "Chưa kích hoạt",
            apply: (stats, lv) => { stats.pulseContributionMultiplier = lv > 0 ? 2.0 : 1.0; }
        },

        // --- NHÁNH 3: THIÊN PHÚ (FORTUNE_PATH) ---
        'fortune_1': {
            id: 'fortune_1',
            path: CONSTELLATIONS.FORTUNE_PATH,
            name: "Thiên Công Tiết Kiệm",
            icon: "🪙",
            tier: 1,
            maxLevel: 4,
            prerequisites: [],
            costFn: (lv) => 2 + lv * 2,
            desc: "Giảm hệ số chi phí lạm phát nâng cấp búa từ 1.18 xuống tối thiểu 1.14 (-0.01 mỗi cấp).",
            effectDesc: (lv) => `Hệ số Chi Phí: ${(1.18 - lv * 0.01).toFixed(2)} (Chuẩn: 1.18)`,
            apply: (stats, lv) => { stats.costDiscountFactor += lv * 0.01; }
        },
        'fortune_2': {
            id: 'fortune_2',
            path: CONSTELLATIONS.FORTUNE_PATH,
            name: "Khí Vận Hanh Thông",
            icon: "🌟",
            tier: 2,
            maxLevel: 5,
            prerequisites: [{ id: 'fortune_1', level: 2 }],
            costFn: (lv) => 3 + lv * 2,
            desc: "Giảm ngưỡng Hard Pity rơi Thiên Hỏa Tâm từ 149 xuống 99 nhát (-10 nhát mỗi cấp).",
            effectDesc: (lv) => `Bảo Hiểm Hard Pity: ${149 - lv * 10} Nhát`,
            apply: (stats, lv) => { stats.pityThresholdReduction += lv * 10; }
        },
        'fortune_3': {
            id: 'fortune_3',
            path: CONSTELLATIONS.FORTUNE_PATH,
            name: "Kho Báu Thiên Ngoại",
            icon: "💎",
            tier: 3,
            maxLevel: 5,
            prerequisites: [{ id: 'fortune_2', level: 2 }],
            costFn: (lv) => 3 + lv * 3,
            desc: "+20% Tỷ lệ rơi Tinh Thể Thiên Cấm & Quặng Vụn từ mỗi nhát búa.",
            effectDesc: (lv) => `+${lv * 20}% Sản Lượng Rơi Quặng & Tinh Thể`,
            apply: (stats, lv) => { stats.oreDropBonus += lv * 0.20; }
        },
        'fortune_4': {
            id: 'fortune_4',
            path: CONSTELLATIONS.FORTUNE_PATH,
            name: "Nguyệt Thực Phúc Lộc",
            icon: "🌙",
            tier: 4,
            maxLevel: 1,
            prerequisites: [{ id: 'fortune_3', level: 3 }],
            costFn: () => 12,
            desc: "Trong khung giờ Trực Đêm (00:00 - 06:00), Tinh Hoa Nguyệt Thực có 30% tỷ lệ rơi x2 viên.",
            effectDesc: (lv) => lv > 0 ? "30% cơ hội nhân đôi Tinh Hoa Nguyệt Thực" : "Chưa kích hoạt",
            apply: (stats, lv) => { stats.eclipseDoubleDropChance = lv > 0 ? 0.30 : 0.0; }
        },

        // --- NHÁNH 4: LINH KHÍ (SPIRIT_PATH) ---
        'spirit_1': {
            id: 'spirit_1',
            path: CONSTELLATIONS.SPIRIT_PATH,
            name: "Khôi Lỗi Sơ Khai",
            icon: "🤖",
            tier: 1,
            maxLevel: 5,
            prerequisites: [],
            costFn: (lv) => 1 + lv,
            desc: "Khai mở và tăng công suất Khôi Lỗi Tự Động Rèn (từ 0.5 nhát/giây lên 2.5 nhát/giây).",
            effectDesc: (lv) => `Tự động gõ: ${(lv * 0.5).toFixed(1)} Nhát/s`,
            apply: (stats, lv) => { stats.autoForgeSpeed = lv * 0.5; }
        },
        'spirit_2': {
            id: 'spirit_2',
            path: CONSTELLATIONS.SPIRIT_PATH,
            name: "Dưỡng Hồn Đêm Dài",
            icon: "⏳",
            tier: 2,
            maxLevel: 5,
            prerequisites: [{ id: 'spirit_1', level: 2 }],
            costFn: (lv) => 2 + lv * 2,
            desc: "Tăng hiệu suất thu nhập Offline từ 20% cơ bản lên tối đa 95% công suất rèn (+15%/cấp).",
            effectDesc: (lv) => `Hiệu suất Offline: ${20 + lv * 15}% Công Suất`,
            apply: (stats, lv) => { stats.offlineEfficiencyBonus += lv * 0.15; }
        },
        'spirit_3': {
            id: 'spirit_3',
            path: CONSTELLATIONS.SPIRIT_PATH,
            name: "Linh Thức Tự Động",
            icon: "🔮",
            tier: 3,
            maxLevel: 3,
            prerequisites: [{ id: 'spirit_2', level: 2 }],
            costFn: (lv) => 4 + lv * 3,
            desc: "Khôi lỗi tự động rèn có thêm +10% cơ hội chạm trúng Điểm Hoàng Kim (+10%/cấp).",
            effectDesc: (lv) => `Auto Golden Rate: +${lv * 10}%`,
            apply: (stats, lv) => { stats.autoGoldenChance += lv * 0.10; }
        },
        'spirit_4': {
            id: 'spirit_4',
            path: CONSTELLATIONS.SPIRIT_PATH,
            name: "Thần Hồn Bất Diệt",
            icon: "✨",
            tier: 4,
            maxLevel: 1,
            prerequisites: [{ id: 'spirit_3', level: 1 }],
            costFn: () => 10,
            desc: "Gia tăng giới hạn thời gian tích lũy ngoại tuyến tối đa từ 8 giờ lên 24 giờ liên tục.",
            effectDesc: (lv) => lv > 0 ? "Tích lũy Offline tối đa 24 Giờ" : "Giới hạn 8 Giờ",
            apply: (stats, lv) => { stats.maxOfflineHours = lv > 0 ? 24 : 8; }
        }
    };

    // =========================================================================
    // 3. KINH TẾ & CƠ CHẾ BẢO HIỂM RƠI ĐỒ (Task 4)
    // =========================================================================
    const EconomyEngine = {
        /**
         * Công thức chi phí nâng cấp búa chuẩn hóa:
         * Cost(L) = floor(10 * (1.18 - Discount)^(L - 1))
         */
        calcHammerCost: function (level, costDiscount = 0) {
            const baseMultiplier = Math.max(1.10, 1.18 - costDiscount);
            return Math.max(10, Math.floor(10 * Math.pow(baseMultiplier, Math.max(0, level - 1))));
        },

        /**
         * Tính tổng chi phí mua n cấp liên tiếp (Cấp số nhân)
         */
        calcBulkCost: function (currentLevel, count, costDiscount = 0) {
            const r = Math.max(1.10, 1.18 - costDiscount);
            let total = 0;
            // Với n nhỏ, tính trực tiếp để tránh sai số dấu phẩy động
            if (count <= 25) {
                for (let i = 0; i < count; i++) {
                    total += Math.floor(10 * Math.pow(r, currentLevel + i - 1));
                }
                return total;
            }
            // Với n lớn, dùng công thức tổng cấp số nhân
            const a = 10 * Math.pow(r, currentLevel - 1);
            total = Math.floor(a * (Math.pow(r, count) - 1) / (r - 1));
            return total;
        },

        /**
         * Tính số cấp tối đa mua được với lượng Vụn Thiên Thiết hiện có
         */
        calcMaxAffordable: function (currentLevel, availableIron, costDiscount = 0) {
            let count = 0;
            let tempIron = availableIron;
            const r = Math.max(1.10, 1.18 - costDiscount);
            while (true) {
                const nextCost = Math.floor(10 * Math.pow(r, currentLevel + count - 1));
                if (tempIron >= nextCost) {
                    tempIron -= nextCost;
                    count++;
                    if (count >= 1000) break; // Giới hạn an toàn
                } else {
                    break;
                }
            }
            return count;
        },

        /**
         * Công thức sản lượng quặng chuẩn hóa:
         * Yield(L) = max(1, floor(2 * 1.11^(L - 1) * Multiplier))
         */
        calcOreYield: function (level, options = {}) {
            const {
                rhythmMultiplier = 1.0,
                stanceBonus = 0.0,
                treeBonus = 0.0,
                milestoneMultiplier = 1.0,
                isGoldenShower = false,
                isGlobalPulse = false
            } = options;

            const baseYield = 2 * Math.pow(1.11, Math.max(0, level - 1));
            let totalMultiplier = rhythmMultiplier * (1 + stanceBonus + treeBonus) * milestoneMultiplier;

            if (isGoldenShower) totalMultiplier *= 5.0; // 15 Phút Mưa Thiên Lộc x5
            if (isGlobalPulse) totalMultiplier *= 5.0;   // Đại Hợp Âm Buff x5

            return Math.max(1, Math.floor(baseYield * totalMultiplier));
        },

        /**
         * Cơ chế Bảo hiểm Rơi Đồ (Drop & Pity System):
         * - Hard Pity: 149 nhát (hoặc giảm về 99 theo cây Thiên Phú)
         * - Soft Pity: Bắt đầu từ 120 nhát (hoặc maxPity - 29), tỷ lệ tăng tuyến tính
         * - Base Chance: 0.5% (0.005)
         */
        rollCelestialCore: function (currentPity, maxPity = 149) {
            const hardPity = Math.max(50, maxPity);
            const softPity = hardPity - 29;
            const baseChance = 0.005;

            // 1. Chạm ngưỡng Hard Pity -> 100% Rơi Chắc Chắn
            if (currentPity >= hardPity - 1) {
                return { dropped: true, newPity: 0, reason: 'HARD_PITY', chance: 1.0 };
            }

            // 2. Vùng Soft Pity -> Tỷ lệ tăng dần theo mỗi nhát vượt ngưỡng
            let currentChance = baseChance;
            if (currentPity >= softPity) {
                const steps = currentPity - softPity + 1;
                const totalSteps = hardPity - softPity;
                currentChance = baseChance + (steps / totalSteps) * (1.0 - baseChance);
            }

            const roll = Math.random();
            if (roll < currentChance) {
                return {
                    dropped: true,
                    newPity: 0,
                    reason: currentPity >= softPity ? 'SOFT_PITY' : 'NATURAL_DROP',
                    chance: currentChance
                };
            }

            return { dropped: false, newPity: currentPity + 1, chance: currentChance };
        },

        /**
         * Kiểm tra khung giờ Trực Đêm (Night Watch) 00:00 - 06:00
         */
        isNightWatchHour: function (timestamp = Date.now()) {
            const date = new Date(timestamp);
            const hours = date.getHours();
            return hours >= 0 && hours < 6;
        },

        /**
         * Rơi Tinh Hoa Nguyệt Thực trong khung 00:00 - 06:00
         */
        rollEclipseEssence: function (isNightWatch, doubleChance = 0.0) {
            if (!isNightWatch) return 0;
            // Tỷ lệ cơ bản 15% khi đánh trúng nhịp chuẩn trong đêm
            if (Math.random() < 0.15) {
                if (doubleChance > 0 && Math.random() < doubleChance) {
                    return 2;
                }
                return 1;
            }
            return 0;
        }
    };

    // =========================================================================
    // 4. CLIENT-SIDE BATCHED TICKS & MULTIPLAYER PROTOCOL (Task 2)
    // =========================================================================
    class MultiplayerBatchClient {
        constructor(options = {}) {
            this.serverUrl = options.serverUrl || (location.protocol === 'https:' ? `wss://${location.host}` : `ws://${location.host}:8080`);
            this.playerId = options.playerId || `Thợ_Rèn_${Math.floor(Math.random() * 89999 + 10000)}`;
            this.districtId = options.districtId || "D-1";
            this.batchIntervalMs = 1000; // Gom đòn đánh mỗi 1.0s

            this.ws = null;
            this.isConnected = false;
            this.pendingHits = [];
            this.batchTimer = null;
            this.reconnectTimer = null;

            // Event Callbacks
            this.onHeartbeat = options.onHeartbeat || null;
            this.onDistrictSparks = options.onDistrictSparks || null;
            this.onGlobalPulse = options.onGlobalPulse || null;
        }

        connect() {
            try {
                this.ws = new WebSocket(this.serverUrl);
                this.ws.onopen = () => {
                    this.isConnected = true;
                    // Gửi tin nhắn gia nhập Khu Rèn
                    this.ws.send(JSON.stringify({
                        type: 'join_district',
                        playerId: this.playerId,
                        districtId: this.districtId
                    }));
                    this.startBatchLoop();
                };

                this.ws.onmessage = (event) => {
                    try {
                        const data = JSON.parse(event.data);
                        this.handleServerMessage(data);
                    } catch (e) {
                        console.error("[Multiplayer] Lỗi parse tin nhắn server:", e);
                    }
                };

                this.ws.onclose = () => {
                    this.isConnected = false;
                    this.stopBatchLoop();
                    this.scheduleReconnect();
                };

                this.ws.onerror = () => {
                    this.ws.close();
                };
            } catch (err) {
                this.scheduleReconnect();
            }
        }

        scheduleReconnect() {
            if (this.reconnectTimer) return;
            this.reconnectTimer = setTimeout(() => {
                this.reconnectTimer = null;
                this.connect();
            }, 3000);
        }

        /**
         * Gom một đòn đánh vào bộ đệm Client-Side
         */
        recordStrike(hitData) {
            // hitData: { stance, quality, damage, resonance, offsetMs, isCrit }
            this.pendingHits.push({
                stance: hitData.stance || STANCE_TYPES.THUNDER_PEAK,
                quality: hitData.quality || 'warm',
                damage: Math.floor(hitData.damage || 0),
                resonance: hitData.resonance || 1,
                offsetMs: hitData.offsetMs || 0,
                isCrit: !!hitData.isCrit,
                timestamp: Date.now()
            });

            // Nếu bộ đệm vượt quá 20 đòn (Overdrive), đẩy ngay không cần chờ tick
            if (this.pendingHits.length >= 20) {
                this.flushBatch();
            }
        }

        startBatchLoop() {
            if (this.batchTimer) clearInterval(this.batchTimer);
            this.batchTimer = setInterval(() => this.flushBatch(), this.batchIntervalMs);
        }

        stopBatchLoop() {
            if (this.batchTimer) {
                clearInterval(this.batchTimer);
                this.batchTimer = null;
            }
        }

        flushBatch() {
            if (!this.isConnected || !this.ws || this.ws.readyState !== WebSocket.OPEN) return;
            if (this.pendingHits.length === 0) return;

            const packet = {
                type: 'batch_strike',
                playerId: this.playerId,
                districtId: this.districtId,
                timestamp: Date.now(),
                hits: this.pendingHits
            };

            this.ws.send(JSON.stringify(packet));
            this.pendingHits = []; // Reset bộ đệm sau khi gửi
        }

        handleServerMessage(msg) {
            if (msg.type === 'heartbeat' || msg.t) {
                if (this.onHeartbeat) this.onHeartbeat(msg);
                if (msg.districtSparks && this.onDistrictSparks) {
                    this.onDistrictSparks(msg.districtSparks);
                }
                if (msg.globalPulse && this.onGlobalPulse) {
                    this.onGlobalPulse(msg.globalPulse);
                }
            }
        }
    }

    // =========================================================================
    // 5. CORE GAMEPLAY STORE & REACTIVE ENGINE (Task 1, 2, 3, 4, 5)
    // =========================================================================
    class CelestialCoreStore {
        constructor() {
            // 1. Trạng thái Thần Chùy & Stance
            this.currentStance = STANCE_TYPES.THUNDER_PEAK;
            this.comboCount = 0;
            this.goldenStreak = 0;
            this.maxGoldenStreak = 0;
            this.hammerLevel = 1;

            // 2. Trạng thái Mái Vòm & Armor Shatter
            this.currentHp = 50000;
            this.maxHp = 50000;
            this.layer = 1;
            this.domeName = "Thiết Vân Vòm";
            this.resonance = 0;
            this.resonanceReq = 100;
            this.isBrokenArmor = false;
            this.shatterUntil = 0;

            // 3. Tài nguyên
            this.skyIron = 0;
            this.domeShards = 0;
            this.celestialCores = 0;
            this.eclipseEssence = 0;
            this.spiritPoints = 0;
            this.spiritPointsClaimed = 0;

            // 4. Bảo hiểm Pity
            this.pityCounter = 0;

            // 5. Kỹ năng Thần Hồn (Prestige Skills)
            this.skills = {};
            Object.keys(PRESTIGE_TREE).forEach(k => { this.skills[k] = 0; });

            // 6. DoT Buffs & Sự Kiện Server
            this.activeDots = []; // Burn DoT ticks
            this.goldenShowerUntil = 0;
            this.globalPulseState = {
                phase: 'countdown', // 'countdown' | 'pulse_window' | 'buff_active'
                timeRemaining: 180,
                perfectRatio: 0.0,
                buffActive: false,
                buffMultiplier: 1.0
            };

            // 7. Event Listeners Registry (Task 5 - Gemini 4 Argon Contract)
            this.listeners = {
                bossHp: new Set(),
                armorResonance: new Set(),
                globalPulse: new Set(),
                districtSparks: new Set(),
                stanceChanged: new Set(),
                skillsUpdated: new Set(),
                toast: new Set()
            };

            // 8. Multiplayer Client Instance
            this.multiplayer = null;

            // Vòng lặp cập nhật DoT và hiệu ứng thời gian thực
            this.startHeartbeatLoop();
        }

        // =====================================================================
        // TÍNH TOÁN THUỘC TÍNH TỔNG HỢP TỪ CÂY KỸ NĂNG (Aggregated Stats)
        // =====================================================================
        getAggregatedStats() {
            const stats = {
                damageBonus: 0.0,
                sweetSpotWidthBonus: 0.0,
                critRateBonus: 0.0,
                critDmgBonus: 0.0,
                comboOverdriveBonus: false,
                resonanceGainBonus: 0,
                districtAuraBonus: 0.0,
                shatterThresholdReduction: 0,
                pulseContributionMultiplier: 1.0,
                costDiscountFactor: 0.0,
                pityThresholdReduction: 0,
                oreDropBonus: 0.0,
                eclipseDoubleDropChance: 0.0,
                autoForgeSpeed: 0.0,
                offlineEfficiencyBonus: 0.0,
                autoGoldenChance: 0.0,
                maxOfflineHours: 8
            };

            for (const [nodeId, level] of Object.entries(this.skills)) {
                if (level > 0 && PRESTIGE_TREE[nodeId]) {
                    PRESTIGE_TREE[nodeId].apply(stats, level);
                }
            }
            return stats;
        }

        // =====================================================================
        // STANCE MANAGEMENT (Zero-delay, Combo Preserved) - Task 1
        // =====================================================================
        changeStance(newStance) {
            if (!STANCES[newStance] || this.currentStance === newStance) return false;
            const prevStance = this.currentStance;
            this.currentStance = newStance;

            // Thông báo tức thì cho UI mà KHÔNG làm gián đoạn chuỗi combo
            this.emit('stanceChanged', {
                prevStance: prevStance,
                newStance: newStance,
                stanceInfo: STANCES[newStance],
                comboCount: this.comboCount,
                goldenStreak: this.goldenStreak
            });
            return true;
        }

        // =====================================================================
        // PRESTIGE TREE ENGINE (Unlock, Validation & Reset) - Task 3
        // =====================================================================
        canUnlockSkill(nodeId) {
            const def = PRESTIGE_TREE[nodeId];
            if (!def) return { canUnlock: false, reason: "NODE_NOT_FOUND" };

            const curLv = this.skills[nodeId] || 0;
            if (curLv >= def.maxLevel) return { canUnlock: false, reason: "MAX_LEVEL_REACHED" };

            // Kiểm tra điều kiện tiên quyết (Prerequisites)
            for (const pre of def.prerequisites) {
                const parentLv = this.skills[pre.id] || 0;
                if (parentLv < pre.level) {
                    const parentDef = PRESTIGE_TREE[pre.id];
                    return {
                        canUnlock: false,
                        reason: `Yêu cầu [${parentDef.name}] đạt Cấp ${pre.level}`
                    };
                }
            }

            const cost = def.costFn(curLv);
            if (this.spiritPoints < cost) {
                return { canUnlock: false, reason: `Cần ${cost} SP Thần Hồn (Hiện có: ${this.spiritPoints})` };
            }

            return { canUnlock: true, cost: cost };
        }

        upgradeSkill(nodeId) {
            const check = this.canUnlockSkill(nodeId);
            if (!check.canUnlock) return false;

            this.spiritPoints -= check.cost;
            this.skills[nodeId] = (this.skills[nodeId] || 0) + 1;

            const stats = this.getAggregatedStats();
            // Cập nhật lại ngưỡng Phá Giáp nếu có giảm từ nhánh Vạn Dân
            this.resonanceReq = Math.max(50, 100 - stats.shatterThresholdReduction);

            this.emit('skillsUpdated', {
                nodeId: nodeId,
                level: this.skills[nodeId],
                remainingSP: this.spiritPoints,
                stats: stats
            });
            return true;
        }

        /**
         * Reset Prestige: Hoàn nguyên cấp búa và Vụn Thiên Thiết nhưng BẢO LƯU/HOÀN TRẢ 100% SP
         */
        resetPrestige() {
            // Tính tổng SP đã đầu tư vào cây kỹ năng
            let refundedSP = 0;
            for (const [nodeId, lv] of Object.entries(this.skills)) {
                if (lv > 0 && PRESTIGE_TREE[nodeId]) {
                    const def = PRESTIGE_TREE[nodeId];
                    for (let l = 0; l < lv; l++) {
                        refundedSP += def.costFn(l);
                    }
                }
                this.skills[nodeId] = 0;
            }

            this.spiritPoints += refundedSP;
            this.hammerLevel = 1;
            this.skyIron = 0;
            this.comboCount = 0;
            this.goldenStreak = 0;

            const stats = this.getAggregatedStats();
            this.emit('skillsUpdated', {
                reset: true,
                refundedSP: refundedSP,
                totalSP: this.spiritPoints,
                stats: stats
            });
            return refundedSP;
        }

        // =====================================================================
        // GAMEPLAY STRIKE ENGINE & HIT SUBMISSION (Task 1 & Task 4)
        // =====================================================================
        submitStrike(params = {}) {
            const quality = params.quality || 'warm'; // 'cold' | 'warm' | 'golden'
            const offsetMs = params.offsetMs || 0;
            const stance = STANCES[this.currentStance];
            const stats = this.getAggregatedStats();

            // 1. Cập nhật chuỗi Combo
            if (quality === 'golden') {
                this.goldenStreak++;
                this.comboCount++;
                this.maxGoldenStreak = Math.max(this.maxGoldenStreak, this.goldenStreak);
            } else if (quality === 'warm') {
                this.comboCount++;
                this.goldenStreak = 0;
            } else {
                this.comboCount = 0;
                this.goldenStreak = 0;
            }

            // 2. Tính toán Sát thương
            const baseHammerDmg = Math.floor(10 * Math.pow(1.11, this.hammerLevel - 1));
            let rhythmMult = stance.baseDmgMult;
            if (quality === 'golden') {
                rhythmMult = stance.goldenDmgMult;
            } else if (quality === 'cold') {
                rhythmMult = 0.3;
            }

            // Crit Calculation
            const baseCritChance = quality === 'golden' ? 0.20 : 0.05;
            const critRate = Math.min(0.85, baseCritChance + stats.critRateBonus);
            const isCrit = Math.random() < critRate;
            const critMult = isCrit ? (2.5 + stats.critDmgBonus) : 1.0;

            // Combo Overdrive Bonus (Nhánh Chiến Thần)
            const comboMult = (stats.comboOverdriveBonus && this.goldenStreak >= 5) ? 2.0 : 1.0;

            let finalDamage = Math.floor(baseHammerDmg * rhythmMult * (1 + stats.damageBonus) * critMult * comboMult);

            // 3. Cơ chế Phá Giáp (Armor Shatter - Task 1)
            let resToAdd = stance.resBonus + stats.resonanceGainBonus;
            if (this.isBrokenArmor) {
                finalDamage = finalDamage * 3; // x3 Sát thương khi boss trong trạng thái BROKEN_ARMOR
            } else {
                finalDamage = Math.max(1, Math.floor(finalDamage * 0.10)); // Giáp Thiết Vân giảm 90% DMG
                this.resonance += resToAdd;

                // Kiểm tra kích hoạt Phá Giáp
                const targetResReq = Math.max(50, 100 - stats.shatterThresholdReduction);
                if (this.resonance >= targetResReq) {
                    this.resonance = 0;
                    this.isBrokenArmor = true;
                    this.shatterUntil = Date.now() + 60000; // 60 giây Phá Giáp
                    this.emit('armorResonance', {
                        resonance: 0,
                        maxResonance: targetResReq,
                        isBroken: true,
                        shatterTimeLeft: 60
                    });
                } else {
                    this.emit('armorResonance', {
                        resonance: this.resonance,
                        maxResonance: targetResReq,
                        isBroken: false,
                        shatterTimeLeft: 0
                    });
                }
            }

            // 4. DoT Thiêu Đốt cho Stance SOLAR_FLAME
            if (this.currentStance === STANCE_TYPES.SOLAR_FLAME) {
                this.activeDots.push({
                    id: Math.random().toString(36).substring(2, 9),
                    expiresAt: Date.now() + 3000,
                    nextTick: Date.now() + 1000,
                    tickDmg: Math.max(1, Math.floor(baseHammerDmg * 0.35))
                });
            }

            // 5. Tính toán Rơi Quặng & Tài Nguyên (Task 4)
            const isGoldenShower = Date.now() < this.goldenShowerUntil;
            const isGlobalPulseBuff = this.globalPulseState.buffActive;
            const oreEarned = EconomyEngine.calcOreYield(this.hammerLevel, {
                rhythmMultiplier: quality === 'golden' ? 2.5 : (quality === 'cold' ? 0.3 : 1.0),
                stanceBonus: stance.oreBonus,
                treeBonus: stats.oreDropBonus,
                milestoneMultiplier: this.hammerLevel >= 5 ? 1.5 : 1.0,
                isGoldenShower: isGoldenShower,
                isGlobalPulse: isGlobalPulseBuff
            });

            this.skyIron += oreEarned;

            // 6. Rơi Thiên Hỏa Tâm (Pity Logic)
            const hardPityCap = Math.max(50, 149 - stats.pityThresholdReduction);
            const coreRoll = EconomyEngine.rollCelestialCore(this.pityCounter, hardPityCap);
            this.pityCounter = coreRoll.newPity;
            let droppedCore = false;
            if (coreRoll.dropped) {
                this.celestialCores++;
                droppedCore = true;
            }

            // 7. Rơi Tinh Hoa Nguyệt Thực (Khung 00:00 - 06:00)
            const isNightWatch = EconomyEngine.isNightWatchHour();
            const eclipseCount = (quality === 'golden') ? EconomyEngine.rollEclipseEssence(isNightWatch, stats.eclipseDoubleDropChance) : 0;
            this.eclipseEssence += eclipseCount;

            // 8. Trừ máu Mái Vòm (Client Optimistic)
            this.currentHp = Math.max(0, this.currentHp - finalDamage);
            this.emit('bossHp', {
                currentHp: this.currentHp,
                maxHp: this.maxHp,
                percent: (this.currentHp / this.maxHp) * 100,
                dps: 0,
                layer: this.layer,
                name: this.domeName
            });

            // 9. Gửi đòn đánh vào bộ đệm Multiplayer Batched Ticks (Task 2)
            if (this.multiplayer) {
                this.multiplayer.recordStrike({
                    stance: this.currentStance,
                    quality: quality,
                    damage: finalDamage,
                    resonance: resToAdd,
                    offsetMs: offsetMs,
                    isCrit: isCrit
                });
            }

            return {
                damage: finalDamage,
                oreEarned: oreEarned,
                isCrit: isCrit,
                quality: quality,
                stance: this.currentStance,
                droppedCore: droppedCore,
                eclipseCount: eclipseCount,
                pityCounter: this.pityCounter,
                hardPityCap: hardPityCap
            };
        }

        // =====================================================================
        // VÒNG LẶP TICK NỘI TẠI & QUẢN LÝ THỜI GIAN
        // =====================================================================
        startHeartbeatLoop() {
            setInterval(() => {
                const now = Date.now();

                // 1. Quản lý trạng thái Hết Hạn Phá Giáp
                if (this.isBrokenArmor && now >= this.shatterUntil) {
                    this.isBrokenArmor = false;
                    const stats = this.getAggregatedStats();
                    this.emit('armorResonance', {
                        resonance: 0,
                        maxResonance: Math.max(50, 100 - stats.shatterThresholdReduction),
                        isBroken: false,
                        shatterTimeLeft: 0
                    });
                }

                // 2. Xử lý DoT Thiêu Đốt (Burn Ticks)
                if (this.activeDots.length > 0) {
                    let totalDotDmg = 0;
                    this.activeDots = this.activeDots.filter(dot => {
                        if (now >= dot.expiresAt) return false;
                        if (now >= dot.nextTick) {
                            totalDotDmg += dot.tickDmg;
                            dot.nextTick = now + 1000;
                        }
                        return true;
                    });

                    if (totalDotDmg > 0) {
                        this.currentHp = Math.max(0, this.currentHp - totalDotDmg);
                        this.emit('bossHp', {
                            currentHp: this.currentHp,
                            maxHp: this.maxHp,
                            percent: (this.currentHp / this.maxHp) * 100,
                            layer: this.layer,
                            name: this.domeName
                        });
                    }
                }
            }, 500);
        }

        // =====================================================================
        // GEMINI 4 ARGON API INTERFACE & EVENT EMITTER (Task 5)
        // =====================================================================
        on(event, callback) {
            if (this.listeners[event]) {
                this.listeners[event].add(callback);
            }
            return () => this.off(event, callback);
        }

        off(event, callback) {
            if (this.listeners[event]) {
                this.listeners[event].delete(callback);
            }
        }

        emit(event, data) {
            if (this.listeners[event]) {
                this.listeners[event].forEach(cb => {
                    try { cb(data); } catch (e) { console.error(`[Event: ${event}] Lỗi callback:`, e); }
                });
            }
        }

        // Convenience Subscriptions
        onBossHpUpdated(callback) { return this.on('bossHp', callback); }
        onArmorResonanceChanged(callback) { return this.on('armorResonance', callback); }
        onGlobalPulseTriggered(callback) { return this.on('globalPulse', callback); }
        onDistrictSparksReceived(callback) { return this.on('districtSparks', callback); }
        onStanceChanged(callback) { return this.on('stanceChanged', callback); }
        onSkillsUpdated(callback) { return this.on('skillsUpdated', callback); }

        /**
         * Lấy snapshot trạng thái sạch cho UI
         */
        getState() {
            return {
                stance: this.currentStance,
                stanceInfo: STANCES[this.currentStance],
                hammerLevel: this.hammerLevel,
                comboCount: this.comboCount,
                goldenStreak: this.goldenStreak,
                boss: {
                    currentHp: this.currentHp,
                    maxHp: this.maxHp,
                    layer: this.layer,
                    name: this.domeName,
                    resonance: this.resonance,
                    resonanceReq: this.resonanceReq,
                    isBrokenArmor: this.isBrokenArmor,
                    shatterSec: Math.max(0, Math.ceil((this.shatterUntil - Date.now()) / 1000))
                },
                wallets: {
                    skyIron: this.skyIron,
                    domeShards: this.domeShards,
                    celestialCores: this.celestialCores,
                    eclipseEssence: this.eclipseEssence,
                    spiritPoints: this.spiritPoints
                },
                pity: {
                    current: this.pityCounter,
                    max: Math.max(50, 149 - this.getAggregatedStats().pityThresholdReduction)
                },
                skills: { ...this.skills },
                stats: this.getAggregatedStats(),
                globalPulse: { ...this.globalPulseState }
            };
        }
    }

    // =========================================================================
    // EXPORT UNIFIED CELESTIAL ENGINE
    // =========================================================================
    const defaultInstance = new CelestialCoreStore();

    return {
        STANCES,
        STANCE_TYPES,
        CONSTELLATIONS,
        PRESTIGE_TREE,
        EconomyEngine,
        MultiplayerBatchClient,
        CelestialCoreStore,
        defaultInstance: defaultInstance,
        createEngine: (options) => new CelestialCoreStore(options),

        // Direct Global Interface for Gemini 4 Argon (Task 5 API Contract)
        getState: () => defaultInstance.getState(),
        submitStrike: (params) => defaultInstance.submitStrike(params),
        changeStance: (newStance) => defaultInstance.changeStance(newStance),
        upgradeSkill: (nodeId) => defaultInstance.upgradeSkill(nodeId),
        canUnlockSkill: (nodeId) => defaultInstance.canUnlockSkill(nodeId),
        resetPrestige: () => defaultInstance.resetPrestige(),
        onBossHpUpdated: (cb) => defaultInstance.onBossHpUpdated(cb),
        onArmorResonanceChanged: (cb) => defaultInstance.onArmorResonanceChanged(cb),
        onGlobalPulseTriggered: (cb) => defaultInstance.onGlobalPulseTriggered(cb),
        onDistrictSparksReceived: (cb) => defaultInstance.onDistrictSparksReceived(cb),
        onStanceChanged: (cb) => defaultInstance.onStanceChanged(cb),
        onSkillsUpdated: (cb) => defaultInstance.onSkillsUpdated(cb)
    };
}));
