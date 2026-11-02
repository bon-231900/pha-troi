-- ============================================================================
-- TOÀN DÂN PHÁ TRỜI: POSTGRESQL PRODUCTION SCHEMA
-- Kiến trúc lưu trữ bền vững (Tier 3) kết hợp Write-Behind 30s
-- ============================================================================

-- 1. Bảng Hồ Sơ Thợ Rèn & Tài Nguyên (Players)
CREATE TABLE IF NOT EXISTS players (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(32) UNIQUE NOT NULL,
    guild_id INT NULL,
    prestige_level INT DEFAULT 0,
    spirit_points BIGINT DEFAULT 0,            -- Điểm Thần Hồn (Prestige)
    sky_iron NUMERIC(38, 0) DEFAULT 0,         -- Vụn Thiên Thiết (Số lớn không giới hạn)
    dome_shards BIGINT DEFAULT 0,              -- Tinh Thể Thiên Cấm
    celestial_cores INT DEFAULT 0,             -- Thiên Hỏa Tâm
    eclipse_essence BIGINT DEFAULT 0,          -- Tinh Hoa Nguyệt Thực (Trực Đêm)
    lifetime_iron NUMERIC(38, 0) DEFAULT 0,    -- Tổng quặng cả đời
    total_damage_dealt NUMERIC(38, 0) DEFAULT 0,-- Tổng sát thương đóng góp
    hammer_level INT DEFAULT 1,                -- Cấp búa
    equipped_hammer_type SMALLINT DEFAULT 1,   -- 1: Lôi, 2: Hỏa, 3: Trọng Lực, 4: Huyền Âm
    talents JSONB DEFAULT '{"thanLuc": 0, "nhanQuan": 0, "tamPhap": 0, "tietKiem": 0}',
    is_shadow_nerfed BOOLEAN DEFAULT FALSE,    -- Cờ trừng phạt Bot Macro
    created_at TIMESTAMPTZ DEFAULT NOW(),
    last_online_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index tăng tốc truy vấn đăng nhập & xếp hạng
CREATE INDEX IF NOT EXISTS idx_players_username ON players(username);
CREATE INDEX IF NOT EXISTS idx_players_total_damage ON players(total_damage_dealt DESC);

-- 2. Bảng Lịch Sử Các Tầng Trời & Đài Tưởng Niệm (Hall of Eternity)
CREATE TABLE IF NOT EXISTS celestial_domes (
    layer_number INT PRIMARY KEY,              -- Tầng 1, Tầng 2...
    name VARCHAR(100) NOT NULL,
    max_hp NUMERIC(38, 0) NOT NULL,
    spawned_at TIMESTAMPTZ NOT NULL,
    shattered_at TIMESTAMPTZ NULL,
    lasthit_player_id BIGINT REFERENCES players(id),
    lasthit_player_name VARCHAR(64) NULL,
    lasthit_hammer_snapshot JSONB NULL,        -- Hình ảnh/chỉ số cây búa lịch sử nện vỡ trời
    top_contributors_snapshot JSONB NULL,      -- Snapshot vĩnh viễn Top 10 Đại Công Thần
    golden_shower_ends_at TIMESTAMPTZ NULL     -- Hạn kết thúc 15 Phút Mưa Thiên Lộc
);

-- 3. Bảng Công Xưởng (Bang Hội Thợ Rèn / Forging Clans)
CREATE TABLE IF NOT EXISTS forging_clans (
    id SERIAL PRIMARY KEY,
    name VARCHAR(64) UNIQUE NOT NULL,
    leader_id BIGINT REFERENCES players(id),
    flame_bellows_level INT DEFAULT 1,         -- Cấp Bễ Thổi Lửa Chung
    member_count INT DEFAULT 1,
    total_contribution NUMERIC(38, 0) DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Dữ liệu khởi tạo cho Tầng 1: Thiết Vân Vòm
INSERT INTO celestial_domes (layer_number, name, max_hp, spawned_at)
VALUES (1, 'Thiết Vân Vòm (Vòm Mây Sắt)', 1000000000, NOW())
ON CONFLICT (layer_number) DO NOTHING;
