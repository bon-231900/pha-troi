-- ==============================================================================
-- DỰ ÁN WEBGAME "PHÁ TRỜI" (PHATROI.COM) - D1 DATABASE SCHEMA
-- Bền vững, trừ máu nguyên tử (Atomic Write), Bảng xếp hạng Vạn Dân
-- ==============================================================================

CREATE TABLE IF NOT EXISTS boss_state (
    vault_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    current_hp REAL NOT NULL,
    max_hp REAL NOT NULL,
    current_armor REAL NOT NULL,
    max_armor REAL NOT NULL,
    server_furnace_heat REAL DEFAULT 0,
    server_anvil_hp REAL DEFAULT 10000,
    shatter_until INTEGER DEFAULT 0,
    last_strike_at INTEGER NOT NULL,
    updated_at INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS leaderboard (
    player_id TEXT PRIMARY KEY,
    player_name TEXT NOT NULL,
    guild_id TEXT DEFAULT 'Vạn Dân',
    total_damage REAL NOT NULL DEFAULT 0,
    raid_score REAL NOT NULL DEFAULT 0,
    last_hit_at INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_leaderboard_damage ON leaderboard(total_damage DESC);
CREATE INDEX IF NOT EXISTS idx_leaderboard_raid_score ON leaderboard(raid_score DESC);

-- Khởi tạo mặc định đủ 9 tầng Cửu Trọng Thiên Cấm (đồng bộ với CELESTIAL_VAULTS)
INSERT OR IGNORE INTO boss_state (
    vault_id, name, current_hp, max_hp, current_armor, max_armor,
    server_furnace_heat, server_anvil_hp, shatter_until, last_strike_at, updated_at
) VALUES
    (1, 'Thiết Vân Vòm', 1500000000, 1500000000, 500, 500, 0, 10000, 0, 0, 1730700000000),
    (2, 'Cổ Đồng Thiên', 4500000000, 4500000000, 1000, 1000, 0, 10000, 0, 0, 1730700000000),
    (3, 'Lôi Tiêu Điện', 12000000000, 12000000000, 1800, 1800, 0, 10000, 0, 0, 1730700000000),
    (4, 'Hàn Băng Thần', 30000000000, 30000000000, 2800, 2800, 0, 10000, 0, 0, 1730700000000),
    (5, 'Xích Diễm Giới', 75000000000, 75000000000, 4200, 4200, 0, 10000, 0, 0, 1730700000000),
    (6, 'Huyền Thủy Hải', 180000000000, 180000000000, 6000, 6000, 0, 10000, 0, 0, 1730700000000),
    (7, 'Bát Quái Phong', 420000000000, 420000000000, 8500, 8500, 0, 10000, 0, 0, 1730700000000),
    (8, 'Hư Không Đoạn', 950000000000, 950000000000, 12000, 12000, 0, 10000, 0, 0, 1730700000000),
    (9, 'Hỗn Độn Thiên', 2500000000000, 2500000000000, 18000, 18000, 0, 10000, 0, 0, 1730700000000);

-- Bảng Hồ Sơ Người Chơi & Cloud Save (Đồng bộ đa thiết bị qua Google Sign-In)
CREATE TABLE IF NOT EXISTS player_profiles (
    google_id TEXT PRIMARY KEY,
    email TEXT NOT NULL,
    display_name TEXT NOT NULL,
    avatar_url TEXT DEFAULT '',
    save_data TEXT NOT NULL,
    last_sync_at INTEGER NOT NULL,
    created_at INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_player_profiles_email ON player_profiles(email);
