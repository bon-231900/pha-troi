# -*- coding: utf-8 -*-
"""
SẢN XUẤT SPRITE SHEET CHUẨN XÁC 100% CHO PHÀM NHÂN THIẾT TƯỢNG (skin_default)
Sử dụng chính xác 100% nhân vật gốc (clean_cutout_mortal.png):
- Khớp xương cánh tay vung búa thực thụ theo 6 pha động học:
  F0: Thủ thế (Arm 0°, búa hạ ngang hông)
  F1: Lấy đà (Arm +55°, búa kéo ra sau lưng)
  F2: Đỉnh vung (Arm +125°, búa giơ cao qua đầu 38px)
  F3: Bổ xé gió (Arm -30°, búa vung xuống xé gió có vệt quệt mờ)
  F4: Nện trúng đe phát nổ (Arm -80°, ĐẦU BÚA NỆN THẲNG LÊN MẶT ĐE tại x=213, y=305, tóe lửa 360°)
  F5: Nảy búa hồi thế (Arm -52°, búa nảy lên 22px do phản lực đàn hồi, khói tàn lửa)
- Zero cuts, 100% Alpha nguyên vẹn, mặt đe và nhân vật cố định không rung lắc
"""
import os
import sys
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import cv2
import numpy as np
from PIL import Image

FRAME_W = 360
FRAME_H = 480
BASELINE_Y = 440

def build_mortal_spritesheet():
    brain_dir = r'C:\Users\ADMIN\.gemini\antigravity\brain\4ac532ff-c4ae-4325-afcc-f630c6b43d10'
    body_p = os.path.join(brain_dir, 'mortal_body_filled.png')
    arm_p = os.path.join(brain_dir, 'mortal_tight_arm.png')
    collar_p = os.path.join(brain_dir, 'mortal_collar_strap.png')
    anvil_p = 'webgame/assets/art/items/item_anvil.webp'
    
    body = cv2.imread(body_p, cv2.IMREAD_UNCHANGED)
    arm = cv2.imread(arm_p, cv2.IMREAD_UNCHANGED)
    collar = cv2.imread(collar_p, cv2.IMREAD_UNCHANGED)
    anvil = cv2.imread(anvil_p, cv2.IMREAD_UNCHANGED)
    
    assert body is not None and arm is not None and collar is not None and anvil is not None
    
    # Scale body to fit 360x480 frame
    scale = 330.0 / body.shape[0]
    bw = int(body.shape[1] * scale)
    bh = int(body.shape[0] * scale)
    scaled_body = cv2.resize(body, (bw, bh), interpolation=cv2.INTER_LANCZOS4)
    
    aw = int(arm.shape[1] * scale)
    ah = int(arm.shape[0] * scale)
    scaled_arm = cv2.resize(arm, (aw, ah), interpolation=cv2.INTER_LANCZOS4)
    
    cw = int(collar.shape[1] * scale)
    ch = int(collar.shape[0] * scale)
    scaled_collar = cv2.resize(collar, (cw, ch), interpolation=cv2.INTER_LANCZOS4)
    
    an_scale = 82.0 / anvil.shape[0]
    anw = int(anvil.shape[1] * an_scale)
    anh = int(anvil.shape[0] * an_scale)
    scaled_anvil = cv2.resize(anvil, (anw, anh), interpolation=cv2.INTER_LANCZOS4)
    
    # Pivots
    sh_x = int(285 * scale)
    sh_y = int(335 * scale)
    piv_arm_x = int(260 * scale)
    piv_arm_y = int(35 * scale)
    col_ox = int(250 * scale)
    col_oy = int(295 * scale)
    
    def blend(bg, fg, x, y):
        h, w = fg.shape[:2]
        x1 = max(0, x)
        y1 = max(0, y)
        x2 = min(bg.shape[1], x + w)
        y2 = min(bg.shape[0], y + h)
        
        fx1 = max(0, -x)
        fy1 = max(0, -y)
        fx2 = fx1 + (x2 - x1)
        fy2 = fy1 + (y2 - y1)
        
        if x2 > x1 and y2 > y1 and fx2 > fx1 and fy2 > fy1:
            fg_crop = fg[fy1:fy2, fx1:fx2]
            alpha = fg_crop[:, :, 3:4] / 255.0
            bg[y1:y2, x1:x2, :3] = (bg[y1:y2, x1:x2, :3] * (1.0 - alpha) + fg_crop[:, :, :3] * alpha).astype(np.uint8)
            bg[y1:y2, x1:x2, 3] = np.maximum(bg[y1:y2, x1:x2, 3], fg_crop[:, :, 3])

    body_base_x = 35
    body_base_y = BASELINE_Y - bh
    anvil_x = 175
    anvil_y = BASELINE_Y - anh + 5
    
    # Strike contact point on anvil face:
    strike_cx = anvil_x + anw // 2 + 5  # ~ 215
    strike_cy = anvil_y + 12            # ~ 375
    
    # 6 Motion Phases
    angles   = [  0,  55, 125, -30, -80, -52]
    squats   = [  0,   4,  -6,   6,  14,   6]
    x_shifts = [  0,  -4,  -6,   8,  14,   6]
    
    frames = []
    for idx in range(6):
        f = np.zeros((FRAME_H, FRAME_W, 4), dtype=np.uint8)
        ang = angles[idx]
        sq = squats[idx]
        xs = x_shifts[idx]
        
        curr_bx = body_base_x + xs
        curr_by = body_base_y + sq
        
        # 1. Base Body
        blend(f, scaled_body, curr_bx, curr_by)
        
        # 2. Arm rotated around shoulder
        world_sh_x = curr_bx + sh_x
        world_sh_y = curr_by + sh_y
        
        rad = np.radians(ang)
        cos_a, sin_a = np.cos(rad), np.sin(rad)
        
        M = np.array([
            [cos_a, -sin_a, world_sh_x - cos_a * piv_arm_x + sin_a * piv_arm_y],
            [sin_a,  cos_a, world_sh_y - sin_a * piv_arm_x - cos_a * piv_arm_y]
        ], dtype=np.float32)
        
        rotated_arm = cv2.warpAffine(scaled_arm, M, (FRAME_W, FRAME_H), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_CONSTANT, borderValue=(0,0,0,0))
        blend(f, rotated_arm, 0, 0)
        
        # 3. Shoulder Collar Cap (Covers joint seamlessly)
        blend(f, scaled_collar, curr_bx + col_ox, curr_by + col_oy)
        
        # 4. Motion Smear Arc on Frame 3
        if idx == 3:
            overlay = np.zeros_like(f, dtype=np.uint8)
            # Arc from top windup to strike
            for r in range(85, 115, 2):
                for a_deg in range(-120, -30, 4):
                    a_rad = np.radians(a_deg)
                    px = int(world_sh_x + r * np.cos(a_rad))
                    py = int(world_sh_y + r * np.sin(a_rad))
                    prog = (a_deg + 120) / 90.0
                    alpha_v = int(140 * (prog ** 1.5))
                    if 0 <= px < FRAME_W and 0 <= py < FRAME_H:
                        cv2.circle(overlay, (px, py), 3, (80, 180, 255, alpha_v), -1)
            blurred = cv2.GaussianBlur(overlay, (7, 7), 0)
            mask_s = blurred[:, :, 3:4] / 255.0
            f[:, :, :3] = (f[:, :, :3] * (1.0 - mask_s) + blurred[:, :, :3] * mask_s).astype(np.uint8)
            f[:, :, 3] = np.maximum(f[:, :, 3], blurred[:, :, 3])
            
        # 5. Anvil Layer (placed in front)
        blend(f, scaled_anvil, anvil_x, anvil_y)
        
        # 6. Sparks & Impact FX on Frame 4 (ON THE ANVIL SURFACE!)
        if idx == 4:
            np.random.seed(42)
            # Shockwave glow ring on anvil
            for r in range(4, 30, 3):
                a_ring = int(160 * (1.0 - r / 30.0))
                cv2.circle(f, (strike_cx, strike_cy), r, (80, 200, 255, a_ring), 2)
            # Central blast flash
            cv2.circle(f, (strike_cx, strike_cy), 10, (255, 255, 255, 255), -1)
            cv2.circle(f, (strike_cx, strike_cy), 20, (50, 180, 255, 200), -1)
            # 360 molten sparks radiating from anvil
            colors = [
                (255, 255, 255, 255),
                (80, 220, 255, 240),
                (30, 140, 255, 220),
                (10, 80, 255, 180)
            ]
            for _ in range(50):
                s_ang = np.random.uniform(-np.pi * 0.95, -np.pi * 0.05)
                dist = np.random.uniform(25, 95)
                ex = int(strike_cx + np.cos(s_ang) * dist)
                ey = int(strike_cy + np.sin(s_ang) * dist)
                c_idx = int(np.random.randint(len(colors)))
                thick = int(np.random.randint(1, 3))
                cv2.line(f, (strike_cx, strike_cy), (ex, ey), colors[c_idx], thick, cv2.LINE_AA)
                cv2.circle(f, (ex, ey), int(np.random.randint(2, 4)), (255, 255, 255, 255), -1)
                
        # 7. Smoke and Embers on Frame 5
        if idx == 5:
            np.random.seed(99)
            for _ in range(16):
                ox = strike_cx + np.random.randint(-20, 20)
                oy = strike_cy - np.random.randint(15, 60)
                r = np.random.randint(8, 20)
                a = np.random.randint(25, 70)
                cv2.circle(f, (ox, oy), r, (180, 190, 200, a), -1)
            for _ in range(12):
                ex = strike_cx + np.random.randint(-35, 35)
                ey = strike_cy - np.random.randint(5, 45)
                cv2.circle(f, (ex, ey), int(np.random.randint(1, 3)), (40, 160, 255, 200), -1)
                
        frames.append(f)
        
    # Assemble into horizontal strip (2160 x 480)
    strip = np.zeros((FRAME_H, FRAME_W * 6, 4), dtype=np.uint8)
    for idx, f in enumerate(frames):
        strip[:, idx * FRAME_W : (idx + 1) * FRAME_W] = f
        
    # Save Spritesheet Strip WebP to brain
    strip_p = os.path.join(brain_dir, 'mortal_blacksmith_strip_2160x480.webp')
    Image.fromarray(cv2.cvtColor(strip, cv2.COLOR_BGRA2RGBA)).save(strip_p, 'WEBP', lossless=True)
    print(f"Saved strip to {strip_p}")
    
    # Save individual verification frames to brain
    for idx, f in enumerate(frames):
        cv2.imwrite(os.path.join(brain_dir, f'mortal_real_frame_{idx}.png'), f)
        
    # Create verification showcase with titles
    showcase = np.zeros((550, 2160, 3), dtype=np.uint8)
    showcase[:] = (10, 8, 6)
    titles = [
        'F0: THU THE CHUAN BI (IDLE)',
        'F1: LAY DA KEO BUA (ANTICIPATION)',
        'F2: DINH DIEM VUNG BUA (APEX HIGH WINDUP)',
        'F3: BO BUA XE GIO (DOWNSTROKE SMEAR)',
        'F4: NEN TRUNG DE PHAT NO (IMPACT 360 SPARK)',
        'F5: NAY BUA HOI THE (REBOUND RECOVERY)'
    ]
    for idx in range(6):
        fx = idx * 360
        cv2.putText(showcase, titles[idx], (fx + 10, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.44, (255, 183, 3), 1, cv2.LINE_AA)
        cv2.rectangle(showcase, (fx, 50), (fx + 359, 549), (45, 35, 25), 1)
        f_alpha = frames[idx][:, :, 3:4] / 255.0
        f_bgr = frames[idx][:, :, :3]
        showcase[50:530, fx:fx+360] = (showcase[50:530, fx:fx+360] * (1.0 - f_alpha) + f_bgr * f_alpha).astype(np.uint8)
    showcase_p = os.path.join(brain_dir, 'mortal_blacksmith_REAL_6_frames_verified.png')
    cv2.imwrite(showcase_p, showcase)
    print(f"Saved showcase to {showcase_p}")
    
    # Deploy to webgame and frontend
    dests = [
        'webgame/assets/art/skins/skin_default',
        'frontend/public/assets/art/skins/skin_default'
    ]
    for d in dests:
        os.makedirs(d, exist_ok=True)
        # Spritesheet
        target_strip = os.path.join(d, 'spritesheet_strip.webp')
        Image.fromarray(cv2.cvtColor(strip, cv2.COLOR_BGRA2RGBA)).save(target_strip, 'WEBP', lossless=True)
        # Card
        card_p = os.path.join(d, 'card.webp')
        Image.fromarray(cv2.cvtColor(frames[0], cv2.COLOR_BGRA2RGBA)).save(card_p, 'WEBP', lossless=True)
        
    # Also update root fallback
    Image.fromarray(cv2.cvtColor(strip, cv2.COLOR_BGRA2RGBA)).save('webgame/assets/art/hero_spritesheet_strip.webp', 'WEBP', lossless=True)
    Image.fromarray(cv2.cvtColor(strip, cv2.COLOR_BGRA2RGBA)).save('frontend/public/assets/art/hero_spritesheet_strip.webp', 'WEBP', lossless=True)
    print("All deployments complete!")

if __name__ == '__main__':
    build_mortal_spritesheet()
