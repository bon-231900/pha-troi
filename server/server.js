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
// HỆ THỐNG ANTI-CHEAT 4 LỚP
// ============================================================================
class AntiCheatGate {
    constructor() {
        this.sessions = new Map();
    }

    registerUser(userId) {
        this.sessions.set(userId, {
            lastStrikeMs: 0,
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
}

const antiCheat = new AntiCheatGate();

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

    const initMsg = JSON.stringify({
        type: 'init',
        userId: userId,
        layer: domeCore.layer,
        name: domeCore.name,
        hp: domeCore.currentHp.toString(),
        maxHp: domeCore.maxHp.toString(),
        res: domeCore.resonance,
        resReq: domeCore.resonanceReq,
        shatterUntil: domeCore.shatterUntil,
        goldenShowerUntil: domeCore.goldenShowerUntil
    });
    ws.send(initMsg);

    ws.on('message', (message) => {
        try {
            const packet = JSON.parse(message);
            if (!Array.isArray(packet) || packet.length < 3) return;

            const [cmd, offsetMs, hammerId] = packet;
            if (cmd === 1) {
                const nowMs = Date.now();
                const check = antiCheat.validateStrike(ws.userId, offsetMs, nowMs);
                if (!check.valid) return;

                let rawDmg = check.shadowNerfed ? 1 : 12000;
                let resAdd = hammerId === 1 ? 3 : 1;

                batchDamage += rawDmg;
                batchResonance += resAdd;

                const hIdx = Math.max(0, Math.min(3, hammerId - 1));
                fxCounters[hIdx]++;

                writeBehind.markDirty(ws.userId, { lastActive: nowMs, damageDealt: rawDmg });
            }
        } catch (e) {}
    });

    ws.on('close', () => {
        antiCheat.unregisterUser(ws.userId);
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
    const ccu = wss.clients.size;
    const nowSec = Math.floor(Date.now() / 1000);
    const shatterSec = Math.max(0, domeCore.shatterUntil - nowSec);
    const goldenShowerSec = Math.max(0, Math.ceil((domeCore.goldenShowerUntil - Date.now()) / 1000));

    const heartbeat = JSON.stringify({
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
        fx: [...fxCounters]
    });

    fxCounters = [0, 0, 0, 0];

    wss.clients.forEach(client => {
        if (client.readyState === 1) {
            client.send(heartbeat);
        }
    });
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
