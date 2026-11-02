-- ============================================================================
-- TOÀN DÂN PHÁ TRỜI: REDIS ATOMIC STRIKE LUA SCRIPT
-- Xử lý trừ máu Mái Vòm, tích lũy Cộng Hưởng, Bảng Xếp Hạng & Khóa 1-HP Last Hit
-- ============================================================================

-- KEYS[1]: dome:current:state (Hash: hp, resonance, shatter_until, winner_id, max_hp)
-- KEYS[2]: dome:current:leaderboard_dmg (Sorted Set: user_id -> total_dmg)
-- KEYS[3]: dome:current:final_phase_hits (Hash: user_id -> hits_in_sub_5_percent)
-- ARGV[1]: user_id
-- ARGV[2]: raw_damage
-- ARGV[3]: resonance_add
-- ARGV[4]: current_timestamp_sec

local state = redis.call('HMGET', KEYS[1], 'hp', 'resonance', 'shatter_until', 'winner_id', 'max_hp')
local current_hp = tonumber(state[1]) or 0
local resonance = tonumber(state[2]) or 0
local shatter_until = tonumber(state[3]) or 0
local winner_id = state[4] or ""
local max_hp = tonumber(state[5]) or 1000000000
local now = tonumber(ARGV[4]) or 0

-- 1. Nếu Mái Vòm đã bị đập vỡ rồi (hoặc đã có người ăn Last Hit), từ chối mọi sát thương
if current_hp <= 0 or (winner_id and winner_id ~= "") then
    return {0, 0, winner_id, resonance, shatter_until}
end

local dmg = tonumber(ARGV[2]) or 0
local res_add = tonumber(ARGV[3]) or 1

-- 2. Kiểm tra trạng thái Cộng Hưởng Vạn Dân (Phá Giáp x3 Sát Thương trong 60 giây)
if now < shatter_until then
    dmg = dmg * 3
else
    -- Nếu đang có Giáp Thần Lực, giảm 90% sát thương nhận vào, tích điểm Cộng Hưởng
    dmg = math.floor(dmg * 0.10)
    resonance = resonance + res_add
    if resonance >= 10000 then
        resonance = 0
        shatter_until = now + 60 -- Kích hoạt Phá Giáp 60 giây toàn server
        redis.call('HSET', KEYS[1], 'shatter_until', shatter_until)
        redis.call('PUBLISH', 'channel:armor_shattered', tostring(shatter_until))
    end
    redis.call('HSET', KEYS[1], 'resonance', resonance)
end

-- 3. Ghi nhận đóng góp vào Bảng Xếp Hạng Toàn Cầu (Sorted Set)
if dmg > 0 then
    redis.call('ZINCRBY', KEYS[2], dmg, ARGV[1])
end

-- 4. Nếu máu dưới 5%, đếm số nhát búa để xét tư cách ăn Last Hit (chống bot clone ăn may)
local qualified_for_lasthit = true
if (current_hp / max_hp) <= 0.05 then
    local hits = redis.call('HINCRBY', KEYS[3], ARGV[1], 1)
    if hits < 100 then
        qualified_for_lasthit = false
    end
end

-- 5. Trừ máu Mái Vòm và xử lý Đòn Kết Liễu (Last Hit)
local new_hp = current_hp - dmg
if new_hp <= 0 then
    if qualified_for_lasthit then
        -- Chốt người chiến thắng vĩ đại duy nhất!
        new_hp = 0
        winner_id = ARGV[1]
        redis.call('HMSET', KEYS[1], 'hp', 0, 'winner_id', winner_id)
        redis.call('PUBLISH', 'channel:dome_shattered', winner_id)
    else
        -- Nếu chưa đủ 100 nhát búa ở phase 5% cuối, giữ Mái Vòm ở đúng 1 HP!
        -- Nhường trọn cơ hội kết liễu cho những thợ rèn thực thụ!
        new_hp = 1
        redis.call('HSET', KEYS[1], 'hp', 1)
    end
else
    redis.call('HSET', KEYS[1], 'hp', new_hp)
end

return {new_hp, dmg, winner_id, resonance, shatter_until}
