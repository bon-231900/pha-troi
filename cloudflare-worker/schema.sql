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

-- Khởi tạo mặc định Tầng 1: Thiết Vân Vòm (1.500.000.000 HP)
INSERT OR IGNORE INTO boss_state (
    vault_id, name, current_hp, max_hp, current_armor, max_armor, 
    server_furnace_heat, server_anvil_hp, shatter_until, last_strike_at, updated_at
) VALUES (
    1, 'Thiết Vân Vòm', 1500000000, 1500000000, 500, 500, 
    0, 10000, 0, 0, 1730700000000
);
