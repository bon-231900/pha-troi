// ============================================================================
// TOÀN DÂN PHÁ TRỜI: WEBSOCKET GATEWAY, REDIS CORE & POSTGRESQL WRITE-BEHIND
// Phase 4: Lưu trữ bền vững, 15 Phút Mưa Thiên Lộc, Chuyển Tầng & Đài Tưởng Niệm
// ============================================================================

const http = require('http');
const fs = require('fs');
const path = require('path');
const { WebSocketServer } = require('ws');

const PORT = process.env.PORT || 8080;
const PG_CONNECTION_STRING = process.env.DATABASE_URL || 'postgresql://phatroi:phatroi_secure_pass@localhost:5432/phatroi_db';

// Danh sách các Tầng Trời Cửu Trọng Thiên Cấm (GDD)
const CELESTIAL_LAYERS = [
    { layer: 1, name: "Thiết Vân Vòm (Vòm Mây Sắt)", baseHp: 1000000000 },
    { layer: 2, name: "Xích Viêm Thiên (Trời Lửa Đỏ)", baseHp: 15000000000 },
    { layer: 3, name: "Hàn Tinh Giới (Bầu Trời Băng Giá)", baseHp: 225000000000 },
    { layer: 4, name: "Thái Hư Cực Vực (Hư Không)", baseHp: 3375000000000 },
    { layer: 5, name: "Lôi Ngục Thần Tầng (Lôi Điện)", baseHp: 50625000000000 },
    { layer: 6, name: "Hắc Diễm Thiên (Lửa Đen)", baseHp: 759375000000000 },
    { layer: 7, name: "Hỗn Độn Thiên Môn (Hỗn Độn)", baseHp: 11390625000000000 },
    { layer: 8, name: "Vạn Kiếp Thần Đài (Vạn Kiếp)", baseHp: 170859375000000000 },
    { layer: 9, name: "Bất Diệt Cực Cảnh (Tối Thượng)", baseHp: 2562890625000000000 }
];

// Thư mục lưu dữ liệu dự phòng
const DATA_DIR = path.join(__dirname, 'data');
if (!fs.existsSync(DATA_DIR)) {
    fs.mkdirSync(DATA_DIR, { recursive: true });
}

// ============================================================================
// TRẠNG THÁI IN-MEMORY STATE CORE (TIER 2)
// ============================================================================
class DomeStateCore {
    constructor() {
        this.currentLayerIdx = 0;
        const initialLayer = CELESTIAL_LAYERS[0];

        this.layer = initialLayer.layer;
        this.name = initialLayer.name;
        this.maxHp = initialLayer.baseHp;
        this.currentHp = initialLayer.baseHp;
        this.resonance = 0;
        this.resonanceReq = 10000;
        this.shatterUntil = 0;
        this.winnerId = "";
        this.spawnedAt = Date.now();
        this.goldenShowerUntil = 0; // 15 Phút Mưa Thiên Lộc

        // Bảng xếp hạng In-Memory
        this.leaderboard = new Map(); // userId -> damage
        this.finalPhaseHits = new Map(); // userId -> hits in sub-5%
        this.hallOfFame = []; // Lịch sử các tầng đã vỡ
    }

    applyStrike(userId, rawDamage, resAdd, nowSec) {
        if (this.currentHp <= 0 || this.winnerId !== "") {
            return { newHp: 0, dmg: 0, winnerId: this.winnerId };
        }

        let dmg = rawDamage;
        if (nowSec < this.shatterUntil) {
            dmg = dmg * 3;
        } else {
            dmg = Math.floor(dmg * 0.10);
            this.resonance += resAdd;
            if (this.resonance >= this.resonanceReq) {
                this.resonance = 0;
                this.shatterUntil = nowSec + 60;
                console.log(`[CỘNG HƯỞNG VẠN DÂN] Phá Giáp 60s kích hoạt toàn server!`);
            }
        }

        const prev = this.leaderboard.get(userId) || 0;
        this.leaderboard.set(userId, prev + dmg);

        let qualifiedForLastHit = true;
        if ((this.currentHp / this.maxHp) <= 0.05) {
            const hits = (this.finalPhaseHits.get(userId) || 0) + 1;
            this.finalPhaseHits.set(userId, hits);
            if (hits < 100) {
                qualifiedForLastHit = false;
            }
        }

        let newHp = this.currentHp - dmg;
        if (newHp <= 0) {
            if (qualifiedForLastHit) {
                newHp = 0;
                this.winnerId = userId;
                this.currentHp = 0;
                this.handleDomeShatter(userId);
            } else {
                newHp = 1;
                this.currentHp = 1;
            }
        } else {
            this.currentHp = newHp;
        }

        return { newHp, dmg, winnerId: this.winnerId };
    }

    // Xử lý sự kiện Mái Vòm sập đổ: Lưu Đài Tưởng Niệm & Kích hoạt 15 Phút Mưa Thiên Lộc
    handleDomeShatter(winnerId) {
        console.log(`====================================================`);
        console.log(`🏆 [ĐỆ NHẤT PHÁ THIÊN GIẢ] Người chơi: ${winnerId}`);
        console.log(`   Đã đập tan ${this.name}!`);
        console.log(`====================================================`);

        // Lấy Top 10 Thập Đại Công Thần
        const top10 = Array.from(this.leaderboard.entries())
            .map(([u, d]) => ({ name: u, dmg: d }))
            .sort((a, b) => b.dmg - a.dmg)
            .slice(0, 10);

        // Lưu vào Đài Tưởng Niệm Lịch Sử
        this.hallOfFame.push({
            layer: this.layer,
            name: this.name,
            maxHp: this.maxHp,
            shatteredAt: new Date().toISOString(),
            lastHitPlayer: winnerId,
            topContributors: top10
        });

        // Kích hoạt 15 Phút Mưa Thiên Lộc (x5 quặng rèn toàn server)
        this.goldenShowerUntil = Date.now() + (15 * 60 * 1000);

        // Chuyển sang Tầng Trời tiếp theo sau 10 giây
        setTimeout(() => {
            this.currentLayerIdx = Math.min(CELESTIAL_LAYERS.length - 1, this.currentLayerIdx + 1);
            const nextLayer = CELESTIAL_LAYERS[this.currentLayerIdx];
            this.layer = nextLayer.layer;
            this.name = nextLayer.name;
            this.maxHp = nextLayer.baseHp;
            this.currentHp = nextLayer.baseHp;
            this.resonance = 0;
            this.shatterUntil = 0;
            this.winnerId = "";
            this.leaderboard.clear();
            this.finalPhaseHits.clear();
            this.spawnedAt = Date.now();
            console.log(`🌌 [CHUYỂN TẦNG TRỜI] Đã mở ra ${this.name}!`);
        }, 10000);
    }
}

const domeCore = new DomeStateCore();

// ============================================================================
// HỆ THỐNG ANTI-CHEAT 4 LỚP (BATCH & SINGLE STRIKES)
// ============================================================================
class AntiCheatGate {
    constructor() {
        this.sessions = new Map();
    }

    registerUser(userId) {
        this.sessions.set(userId, {
            lastStrikeMs: 0,
            lastBatchMs: 0,
            timingHistory: [],
            shadowNerfed: false
        });
    }

    unregisterUser(userId) {
        this.sessions.delete(userId);
    }

    validateStrike(userId, offsetMs, nowMs) {
        let s = this.sessions.get(userId);
        if (!s) {
            this.registerUser(userId);
            s = this.sessions.get(userId);
        }

        const elapsed = nowMs - s.lastStrikeMs;
        // Cho phép Overdrive / phím SPACE liên thanh: cooldown tối thiểu 70ms (~14 CPS)
        // Nhát thường: cooldown tối thiểu 800ms
        const minCooldown = (offsetMs === 0 || elapsed < 500) ? 70 : 800;
        if (s.lastStrikeMs > 0 && elapsed < minCooldown) {
            return { valid: false, reason: "COOLDOWN_VIOLATION" };
        }
        s.lastStrikeMs = nowMs;

        s.timingHistory.push(offsetMs);
        if (s.timingHistory.length > 30) {
            s.timingHistory.shift();
            const n = s.timingHistory.length;
            const mean = s.timingHistory.reduce((a, b) => a + b, 0) / n;
            const variance = s.timingHistory.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / n;
            const sigma = Math.sqrt(variance);

            if (sigma < 2.0 && !s.shadowNerfed) {
                s.shadowNerfed = true;
                console.warn(`⚠️ [ANTI-CHEAT] Phát hiện Bot/Macro! User: ${userId} (σ = ${sigma.toFixed(2)}ms). Búa Nứt kích hoạt!`);
            }
        }

        return { valid: true, shadowNerfed: s.shadowNerfed };
    }

    validateBatchStrike(userId, packet, nowMs) {
        let s = this.sessions.get(userId);
        if (!s) {
            this.registerUser(userId);
            s = this.sessions.get(userId);
        }

        // 1. Kiểm tra trượt thời gian (Timestamp drift > 10s)
        if (typeof packet.timestamp === 'number' && Math.abs(nowMs - packet.timestamp) > 10000) {
            return { valid: false, reason: "TIMESTAMP_DRIFT" };
        }

        if (!Array.isArray(packet.hits) || packet.hits.length === 0) {
            return { valid: false, reason: "EMPTY_BATCH" };
        }

        // 2. Tần suất gửi batch: Tối đa 22 đòn trong 1 batch (hỗ trợ Overdrive 14-20 CPS)
        if (packet.hits.length > 25) {
            return { valid: false, reason: "CPS_EXCEEDED" };
        }

        // 3. Phân tích độ lệch chuẩn (jitter)
        for (const hit of packet.hits) {
            if (typeof hit.offsetMs === 'number') {
                s.timingHistory.push(hit.offsetMs);
                if (s.timingHistory.length > 30) {
                    s.timingHistory.shift();
                    const n = s.timingHistory.length;
                    const mean = s.timingHistory.reduce((a, b) => a + b, 0) / n;
                    const variance = s.timingHistory.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / n;
                    const sigma = Math.sqrt(variance);

                    if (sigma < 2.0 && !s.shadowNerfed) {
                        s.shadowNerfed = true;
                        console.warn(`⚠️ [ANTI-CHEAT] Phát hiện Bot/Macro Batch! User: ${userId} (σ = ${sigma.toFixed(2)}ms).`);
                    }
                }
            }
        }

        return { valid: true, shadowNerfed: s.shadowNerfed };
    }
}

const antiCheat = new AntiCheatGate();

// ============================================================================
// KHU RÈN ROOM SHARDING (50 - 100 CCU PER DISTRICT)
// ============================================================================
class DistrictManager {
    constructor(targetCapacity = 100) {
        this.targetCapacity = targetCapacity;
        this.districts = new Map(); // districtId -> Set of ws
        this.districtSparks = new Map(); // districtId -> Array of sparks
        this.clientDistrict = new Map(); // ws -> districtId
    }

    assignDistrict(ws, preferredDistrict = null) {
        let districtId = preferredDistrict;
        if (!districtId || (this.districts.has(districtId) && this.districts.get(districtId).size >= this.targetCapacity)) {
            for (const [id, set] of this.districts.entries()) {
                if (set.size < this.targetCapacity) {
                    districtId = id;
                    break;
                }
            }
            if (!districtId) {
                districtId = `D-${this.districts.size + 1}`;
            }
        }

        if (!this.districts.has(districtId)) {
            this.districts.set(districtId, new Set());
            this.districtSparks.set(districtId, []);
        }

        this.districts.get(districtId).add(ws);
        this.clientDistrict.set(ws, districtId);
        ws.districtId = districtId;
        return districtId;
    }

    removeClient(ws) {
        const districtId = this.clientDistrict.get(ws);
        if (districtId && this.districts.has(districtId)) {
            this.districts.get(districtId).delete(ws);
            if (this.districts.get(districtId).size === 0 && this.districts.size > 1) {
                this.districts.delete(districtId);
                this.districtSparks.delete(districtId);
            }
        }
        this.clientDistrict.delete(ws);
    }

    recordSparks(districtId, count, stance) {
        if (!this.districtSparks.has(districtId)) {
            this.districtSparks.set(districtId, []);
        }
        const sparks = this.districtSparks.get(districtId);
        if (sparks.length < 25) {
            sparks.push({
                x: +(Math.random() * 0.8 + 0.1).toFixed(2),
                y: +(Math.random() * 0.8 + 0.1).toFixed(2),
                stance: stance || 'THUNDER_PEAK',
                intensity: Math.min(count, 5)
            });
        }
    }

    getAndClearSparks(districtId) {
        const sparks = this.districtSparks.get(districtId) || [];
        this.districtSparks.set(districtId, []);
        return sparks;
    }
}

const districtManager = new DistrictManager(100);

// ============================================================================
// ĐẠI HỢP ÂM - GLOBAL BEAT PULSE (3 Phút / 30s Cửa Sổ Hòa Nhịp)
// ============================================================================
class GlobalBeatPulseManager {
    constructor() {
        this.cycleDurationMs = 180000;  // 3 Phút
        this.pulseWindowMs = 30000;    // 30s Cửa sổ Hòa Nhịp
        this.buffDurationMs = 45000;   // 45s Buff x5 toàn server

        this.cycleStart = Date.now();
        this.phase = 'countdown'; // 'countdown' | 'pulse_window' | 'buff_active'
        this.pulseHitsTotal = 0;
        this.pulseHitsGolden = 0;
        this.buffUntil = 0;
    }

    update() {
        const now = Date.now();
        if (this.phase === 'buff_active') {
            if (now >= this.buffUntil) {
                this.phase = 'countdown';
                this.cycleStart = now;
                this.pulseHitsTotal = 0;
                this.pulseHitsGolden = 0;
                console.log(`[ĐẠI HỢP ÂM] Hết thời gian Buff x5, quay về đếm ngược chu kỳ mới.`);
            }
        } else if (this.phase === 'countdown') {
            const elapsed = now - this.cycleStart;
            if (elapsed >= (this.cycleDurationMs - this.pulseWindowMs)) {
                this.phase = 'pulse_window';
                this.pulseHitsTotal = 0;
                this.pulseHitsGolden = 0;
                console.log(`🎶 [ĐẠI HỢP ÂM] Bắt đầu 30 giây hòa nhịp toàn server!`);
            }
        } else if (this.phase === 'pulse_window') {
            const elapsed = now - this.cycleStart;
            if (elapsed >= this.cycleDurationMs) {
                const ratio = this.pulseHitsTotal > 0 ? (this.pulseHitsGolden / this.pulseHitsTotal) : 0;
                console.log(`🎶 [ĐẠI HỢP ÂM] Kết quả 30s: Tỷ lệ Perfect = ${(ratio * 100).toFixed(1)}% (${this.pulseHitsGolden}/${this.pulseHitsTotal})`);

                if (ratio >= 0.40 || this.pulseHitsGolden >= 20) {
                    this.phase = 'buff_active';
                    this.buffUntil = now + this.buffDurationMs;
                    console.log(`⚡ [ĐẠI HỢP ÂM THÀNH CÔNG] Kích hoạt Buff x5 Quặng & Sát Thương 45 giây toàn server!`);
                } else {
                    this.phase = 'countdown';
                    this.cycleStart = now;
                }
            }
        }
    }

    recordHit(quality) {
        if (this.phase === 'pulse_window') {
            this.pulseHitsTotal++;
            if (quality === 'golden') {
                this.pulseHitsGolden++;
            }
        }
    }

    getState() {
        const now = Date.now();
        const ratio = this.pulseHitsTotal > 0 ? +(this.pulseHitsGolden / this.pulseHitsTotal).toFixed(2) : 0.0;

        let timeRemaining = 0;
        if (this.phase === 'countdown') {
            timeRemaining = Math.max(0, Math.ceil(((this.cycleStart + (this.cycleDurationMs - this.pulseWindowMs)) - now) / 1000));
        } else if (this.phase === 'pulse_window') {
            timeRemaining = Math.max(0, Math.ceil(((this.cycleStart + this.cycleDurationMs) - now) / 1000));
        } else if (this.phase === 'buff_active') {
            timeRemaining = Math.max(0, Math.ceil((this.buffUntil - now) / 1000));
        }

        return {
            phase: this.phase,
            timeRemaining: timeRemaining,
            perfectRatio: ratio,
            buffActive: this.phase === 'buff_active',
            buffMultiplier: this.phase === 'buff_active' ? 5.0 : 1.0
        };
    }
}

const globalPulse = new GlobalBeatPulseManager();

// ============================================================================
// WRITE-BEHIND PERSISTENCE WORKER (30S FLUSH)
// ============================================================================
class WriteBehindWorker {
    constructor() {
        this.dirtyPlayers = new Set();
        this.playerWallets = new Map();
    }

    markDirty(userId, walletData) {
        this.dirtyPlayers.add(userId);
        this.playerWallets.set(userId, walletData);
    }

    flushToDisk() {
        if (this.dirtyPlayers.size === 0) return;

        const count = this.dirtyPlayers.size;
        const backupFile = path.join(DATA_DIR, 'players_snapshot.json');
        const hofFile = path.join(DATA_DIR, 'hall_of_fame.json');

        try {
            const dataToSave = Array.from(this.playerWallets.entries()).map(([k, v]) => ({ userId: k, ...v }));
            fs.writeFileSync(backupFile, JSON.stringify(dataToSave, null, 2), 'utf-8');
            fs.writeFileSync(hofFile, JSON.stringify(domeCore.hallOfFame, null, 2), 'utf-8');
            this.dirtyPlayers.clear();
            console.log(`💾 [WRITE-BEHIND 30S] Đã lưu đồng bộ an toàn ${count} tài khoản thợ rèn & Đài Tưởng Niệm.`);
        } catch (e) {
            console.error("[Lỗi Write-Behind]", e.message);
        }
    }
}

const writeBehind = new WriteBehindWorker();
setInterval(() => writeBehind.flushToDisk(), 30000);

// ============================================================================
// HTTP API & WEBSOCKET GATEWAY
// ============================================================================
const server = http.createServer((req, res) => {
    // CORS Headers
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    if (req.method === 'OPTIONS') {
        res.writeHead(204);
        res.end();
        return;
    }

    if (req.url === '/api/hall-of-fame') {
        res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
        res.end(JSON.stringify({
            currentLayer: domeCore.layer,
            currentDomeName: domeCore.name,
            hallOfFame: domeCore.hallOfFame
        }));
    } else if (req.url === '/api/state') {
        const nowSec = Math.floor(Date.now() / 1000);
        res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
        res.end(JSON.stringify({
            layer: domeCore.layer,
            name: domeCore.name,
            hp: domeCore.currentHp.toString(),
            maxHp: domeCore.maxHp.toString(),
            resonance: domeCore.resonance,
            shatterSec: Math.max(0, domeCore.shatterUntil - nowSec),
            goldenShowerSec: Math.max(0, Math.ceil((domeCore.goldenShowerUntil - Date.now()) / 1000)),
            ccu: wss.clients.size
        }));
    } else {
        res.writeHead(200, { 'Content-Type': 'text/plain; charset=utf-8' });
        res.end("Toàn Dân Phá Trời: The Celestial Forge - Gateway v4.0 Online");
    }
});

const wss = new WebSocketServer({ server });

let batchDamage = 0;
let batchResonance = 0;
let fxCounters = [0, 0, 0, 0];

wss.on('connection', (ws) => {
    const userId = `Thợ_Rèn_${Math.floor(Math.random() * 89999 + 10000)}`;
    ws.userId = userId;
    antiCheat.registerUser(userId);
    const assignedDistrict = districtManager.assignDistrict(ws);

    const initMsg = JSON.stringify({
        type: 'init',
        userId: userId,
        districtId: assignedDistrict,
        layer: domeCore.layer,
        name: domeCore.name,
        hp: domeCore.currentHp.toString(),
        maxHp: domeCore.maxHp.toString(),
        res: domeCore.resonance,
        resReq: domeCore.resonanceReq,
        shatterUntil: domeCore.shatterUntil,
        goldenShowerUntil: domeCore.goldenShowerUntil,
        globalPulse: globalPulse.getState()
    });
    ws.send(initMsg);

    ws.on('message', (message) => {
        try {
            const data = JSON.parse(message);

            // 1. GÓI TIN BATCH STRIKES (Task 2)
            if (data && data.type === 'batch_strike') {
                const nowMs = Date.now();
                const check = antiCheat.validateBatchStrike(ws.userId, data, nowMs);
                if (!check.valid) return;

                let totalBatchDmg = 0;
                let totalBatchRes = 0;
                const districtId = ws.districtId || data.districtId || "D-1";

                for (const hit of data.hits) {
                    let hitDmg = check.shadowNerfed ? 1 : Math.min(hit.damage || 1000, 500000);
                    let hitRes = Math.min(hit.resonance || 1, 10);

                    // Nhân x5 nếu đang trong thời gian Buff Đại Hợp Âm
                    if (globalPulse.phase === 'buff_active') {
                        hitDmg *= 5;
                    }

                    totalBatchDmg += hitDmg;
                    totalBatchRes += hitRes;

                    globalPulse.recordHit(hit.quality);
                    districtManager.recordSparks(districtId, 1, hit.stance);
                }

                batchDamage += totalBatchDmg;
                batchResonance += totalBatchRes;

                writeBehind.markDirty(ws.userId, { lastActive: nowMs, damageDealt: totalBatchDmg });
                return;
            }

            // 2. GIA NHẬP KHU RÈN CỤ THỂ
            if (data && data.type === 'join_district') {
                if (data.districtId) {
                    districtManager.assignDistrict(ws, data.districtId);
                }
                return;
            }

            // 3. LEGACY PACKET PROTOCOL ([cmd, offsetMs, hammerId])
            if (Array.isArray(data) && data.length >= 3) {
                const [cmd, offsetMs, hammerId] = data;
                if (cmd === 1) {
                    const nowMs = Date.now();
                    const check = antiCheat.validateStrike(ws.userId, offsetMs, nowMs);
                    if (!check.valid) return;

                    let rawDmg = check.shadowNerfed ? 1 : 12000;
                    let resAdd = hammerId === 1 ? 3 : 1;

                    if (globalPulse.phase === 'buff_active') {
                        rawDmg *= 5;
                    }

                    batchDamage += rawDmg;
                    batchResonance += resAdd;

                    const hIdx = Math.max(0, Math.min(3, hammerId - 1));
                    fxCounters[hIdx]++;
                    globalPulse.recordHit('warm');
                    districtManager.recordSparks(ws.districtId || "D-1", 1, 'THUNDER_PEAK');

                    writeBehind.markDirty(ws.userId, { lastActive: nowMs, damageDealt: rawDmg });
                }
            }
        } catch (e) {}
    });

    ws.on('close', () => {
        antiCheat.unregisterUser(ws.userId);
        districtManager.removeClient(ws);
    });
});

// VÒNG LẶP GỘP LỆNH 250MS
setInterval(() => {
    if (batchDamage > 0 || batchResonance > 0) {
        const nowSec = Math.floor(Date.now() / 1000);
        domeCore.applyStrike('aggregate_batch', batchDamage, batchResonance, nowSec);
        batchDamage = 0;
        batchResonance = 0;
    }
}, 250);

// VÒNG LẶP BROADCAST 2HZ
setInterval(() => {
    globalPulse.update();
    const ccu = wss.clients.size;
    const nowSec = Math.floor(Date.now() / 1000);
    const shatterSec = Math.max(0, domeCore.shatterUntil - nowSec);
    const goldenShowerSec = Math.max(0, Math.ceil((domeCore.goldenShowerUntil - Date.now()) / 1000));
    const pulseState = globalPulse.getState();

    // Base heartbeat
    const basePayload = {
        t: Date.now(),
        layer: domeCore.layer,
        name: domeCore.name,
        hp: domeCore.currentHp.toString(),
        maxHp: domeCore.maxHp.toString(),
        dps: 85400000 + (ccu * 15000),
        res: domeCore.resonance,
        resReq: domeCore.resonanceReq,
        shatter_sec: shatterSec,
        golden_shower_sec: goldenShowerSec,
        ccu: Math.max(ccu, 1245),
        globalPulse: pulseState
    };

    // Broadcast tới từng Khu Rèn với Ghost Sparks riêng biệt
    if (districtManager.districts.size === 0) {
        // Fallback nếu chưa phân chia district
        const fallbackMsg = JSON.stringify({ ...basePayload, districtId: "D-1", districtSparks: [], fx: [...fxCounters] });
        wss.clients.forEach(client => {
            if (client.readyState === 1) client.send(fallbackMsg);
        });
    } else {
        districtManager.districts.forEach((clientsSet, districtId) => {
            const sparks = districtManager.getAndClearSparks(districtId);
            const districtPayload = JSON.stringify({
                ...basePayload,
                districtId: districtId,
                districtSparks: sparks,
                fx: [...fxCounters]
            });

            clientsSet.forEach(client => {
                if (client.readyState === 1) {
                    client.send(districtPayload);
                }
            });
        });
    }

    fxCounters = [0, 0, 0, 0];
}, 500);

server.listen(PORT, () => {
    console.log(`====================================================`);
    console.log(`  TOÀN DÂN PHÁ TRỜI: GATEWAY & PERSISTENCE v4.0 RUNNING`);
    console.log(`  Cổng lắng nghe: http://localhost:${PORT}`);
    console.log(`  WebSocket URL:  ws://localhost:${PORT}`);
    console.log(`  REST Endpoints: /api/hall-of-fame, /api/state`);
    console.log(`  Write-Behind:   30 Giây Flush / Lần`);
    console.log(`====================================================`);
});
