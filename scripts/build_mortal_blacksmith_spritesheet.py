# -*- coding: utf-8 -*-
"""
Script sản xuất trọn bộ Sprite Sheet 6 Khung Hình hoàn chỉnh cho Phàm Nhân Thiết Tượng (skin_default)
Quy chuẩn:
- Độ phân giải mỗi frame: 360 x 480 px
- Dải Spritesheet: 2160 x 480 px (6 frames)
- Chân nhân vật luôn chạm đất tại y = 440 px (chống rung giật 100%)
- Tâm tiếp xúc đe rèn tại (x = 213, y = 342) px
- Zero cuts: Alpha thân thể = 255 liên tục
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
ANVIL_STRIKE_X = 213
ANVIL_STRIKE_Y = 342

def make_clean_cutout(bgr, bg_thresh=18, ramp=16):
    max_c = np.max(bgr, axis=2).astype(np.float32)
    alpha = np.clip((max_c - bg_thresh) / float(ramp), 0.0, 1.0) * 255.0
    alpha = alpha.astype(np.uint8)
    
    bin_mask = (alpha > 50).astype(np.uint8) * 255
    contours, _ = cv2.findContours(bin_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    solid = np.zeros_like(alpha)
    for c in contours:
        if cv2.contourArea(c) > 1000:
            cv2.drawContours(solid, [c], -1, 255, -1)
            
    final_alpha = np.where(solid > 0, np.maximum(alpha, 255), alpha)
    b, g, r = cv2.split(bgr)
    return cv2.merge([b, g, r, final_alpha])

def crop_to_bbox(c):
    alpha = c[:, :, 3]
    ys, xs = (alpha > 30).nonzero()
    return c[ys.min():ys.max()+1, xs.min():xs.max()+1]

def draw_spark_burst(frame, cx, cy, intensity=1.0, count=45, seed=42):
    """Vẽ tia lửa sắt nổ bung 360 độ và vòng sóng xung kích tại điểm va chạm búa-đe"""
    np.random.seed(seed)
    overlay = np.zeros_like(frame, dtype=np.float32)
    
    # 1. Shockwave glow ring
    for r in range(4, 28):
        alpha_ring = int(180 * (1.0 - r / 28.0) * intensity)
        cv2.circle(frame, (cx, cy), r, (80, 200, 255, alpha_ring), 2)
        
    # 2. Central blast flash
    cv2.circle(frame, (cx, cy), 12, (255, 255, 255, int(255 * intensity)), -1)
    cv2.circle(frame, (cx, cy), 22, (50, 180, 255, int(200 * intensity)), -1)
    cv2.circle(frame, (cx, cy), 35, (20, 100, 255, int(110 * intensity)), -1)

    spark_colors = [
        (255, 255, 255, 255), # White hot
        (100, 220, 255, 240), # Gold
        (40, 140, 255, 220),  # Orange-red
        (20, 80, 255, 180)    # Deep amber
    ]

    # 3. High-velocity molten iron spark streaks
    for _ in range(count):
        angle = np.random.uniform(-np.pi * 0.95, -np.pi * 0.05) # Hướng bung lên trên và 2 bên
        speed = np.random.uniform(25, 85) * intensity
        dx = int(np.cos(angle) * speed)
        dy = int(np.sin(angle) * speed)
        
        color_choice = spark_colors[np.random.randint(len(spark_colors))]
        thickness = int(np.random.randint(1, 4))
        
        # Arc streak
        pt1 = (cx + int(dx * 0.15), cy + int(dy * 0.15))
        pt2 = (cx + dx, cy + dy)
        cv2.line(frame, pt1, pt2, color_choice, thickness, cv2.LINE_AA)
        
        # Spark head dot
        cv2.circle(frame, pt2, int(np.random.randint(2, 4)), (255, 255, 255, 255), -1)

def draw_motion_smear(frame, cx, cy, start_angle=-70, end_angle=20, radius=90):
    """Vẽ vệt quệt mờ xé gió (Motion Smear Arc) cho nhát búa bổ xuống ở Frame 3"""
    overlay = np.zeros_like(frame, dtype=np.uint8)
    
    # Draw arc fan
    for r in range(radius - 18, radius + 22, 2):
        for ang_deg in range(start_angle, end_angle, 3):
            rad = np.radians(ang_deg)
            # Progress 0.0 (top) to 1.0 (bottom)
            prog = (ang_deg - start_angle) / float(end_angle - start_angle)
            px = int(cx + r * np.cos(rad))
            py = int(cy + r * np.sin(rad))
            
            # Alpha builds up towards the strike
            alpha = int(160 * (prog ** 1.8))
            color = (
                int(50 + 150 * prog),
                int(140 + 100 * prog),
                int(255),
                alpha
            )
            if 0 <= px < FRAME_W and 0 <= py < FRAME_H:
                cv2.circle(overlay, (px, py), 4, color, -1)
                
    # Blur overlay for smooth motion blur
    blurred = cv2.GaussianBlur(overlay, (9, 9), 0)
    # Blend onto frame
    mask = blurred[:, :, 3:4] / 255.0
    frame[:, :, :3] = (frame[:, :, :3] * (1.0 - mask) + blurred[:, :, :3] * mask).astype(np.uint8)
    frame[:, :, 3] = np.maximum(frame[:, :, 3], blurred[:, :, 3])

def draw_smoke_rebound(frame, cx, cy, count=15):
    """Vẽ khói mỏng và tàn lửa rơi ở Frame 5"""
    np.random.seed(99)
    for _ in range(count):
        ox = cx + np.random.randint(-25, 25)
        oy = cy - np.random.randint(10, 65)
        r = np.random.randint(8, 22)
        alpha = np.random.randint(25, 75)
        cv2.circle(frame, (ox, oy), r, (180, 190, 200, alpha), -1)
        
    # Falling ember specks
    for _ in range(12):
        ex = cx + np.random.randint(-40, 40)
        ey = cy - np.random.randint(-10, 45)
        cv2.circle(frame, (ex, ey), np.random.choice([1, 2]), (40, 160, 255, 200), -1)

print("Helper functions ready.")


# Main Generation Pipeline
def build_spritesheet():
    brain_dir = r'C:\Users\ADMIN\.gemini\antigravity\brain\4ac532ff-c4ae-4325-afcc-f630c6b43d10'
    p1 = os.path.join(brain_dir, 'mortal_tight_idle.png')
    p2 = os.path.join(brain_dir, 'mortal_tight_strike.png')
    
    c1 = cv2.imread(p1, cv2.IMREAD_UNCHANGED)
    c2 = cv2.imread(p2, cv2.IMREAD_UNCHANGED)
    
    assert c1 is not None, f"Missing {p1}"
    assert c2 is not None, f"Missing {p2}"
    
    # Scale both to fit standard 360x480 frame
    # In c1, target character height = 340px (from head to feet)
    scale1 = 340.0 / c1.shape[0]
    w1 = int(c1.shape[1] * scale1)
    h1 = int(c1.shape[0] * scale1)
    char_idle = cv2.resize(c1, (w1, h1), interpolation=cv2.INTER_LANCZOS4)
    
    # In c2 (strike pose), hammer is overhead, target character height head-to-feet is identical to c1
    scale2 = (340.0 / 756.0) * 0.90 # 0.4047
    w2 = int(c2.shape[1] * scale2)
    h2 = int(c2.shape[0] * scale2)
    char_strike = cv2.resize(c2, (w2, h2), interpolation=cv2.INTER_LANCZOS4)
    
    # Anvil prop from clean blacksmith dais or props
    anvil_p = 'webgame/assets/art/items/item_anvil.webp'
    anvil_img = None
    if os.path.exists(anvil_p):
        anvil_raw = cv2.imread(anvil_p, cv2.IMREAD_UNCHANGED)
        if anvil_raw is not None:
            # Scale anvil to width ~90px, height ~75px
            anvil_scale = 85.0 / anvil_raw.shape[0]
            an_w = int(anvil_raw.shape[1] * anvil_scale)
            an_h = int(anvil_raw.shape[0] * anvil_scale)
            anvil_img = cv2.resize(anvil_raw, (an_w, an_h), interpolation=cv2.INTER_LANCZOS4)
            
    frames = []
    
    def blend_fg(bg, fg, x, y):
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

    def affine_transform(img, angle_deg, scale_x, scale_y, tx, ty, pivot_x, pivot_y):
        rad = np.radians(angle_deg)
        cos_a = np.cos(rad)
        sin_a = np.sin(rad)
        
        # Affine matrix centered on pivot
        M = np.array([
            [scale_x * cos_a, -scale_y * sin_a, tx + pivot_x - scale_x * cos_a * pivot_x + scale_y * sin_a * pivot_y],
            [scale_x * sin_a,  scale_y * cos_a, ty + pivot_y - scale_x * sin_a * pivot_x - scale_y * cos_a * pivot_y]
        ], dtype=np.float32)
        
        warped = cv2.warpAffine(img, M, (FRAME_W, FRAME_H), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_CONSTANT, borderValue=(0,0,0,0))
        return warped

    # -------------------------------------------------------------
    # FRAME 0: Thủ thế chuẩn bị (Idle Ready)
    # -------------------------------------------------------------
    f0 = np.zeros((FRAME_H, FRAME_W, 4), dtype=np.uint8)
    char_f0 = affine_transform(char_idle, angle_deg=0, scale_x=1.0, scale_y=1.0, tx=0, ty=0, pivot_x=char_idle.shape[1]//2, pivot_y=char_idle.shape[0])
    blend_fg(f0, char_f0, 10, BASELINE_Y - char_idle.shape[0])
    if anvil_img is not None:
        blend_fg(f0, anvil_img, ANVIL_STRIKE_X - 18, BASELINE_Y - anvil_img.shape[0] + 5)
    frames.append(f0)
    
    # -------------------------------------------------------------
    # FRAME 1: Lấy đà kéo búa (Anticipation / Backswing)
    # -------------------------------------------------------------
    f1 = np.zeros((FRAME_H, FRAME_W, 4), dtype=np.uint8)
    char_f1 = affine_transform(char_idle, angle_deg=-4, scale_x=0.98, scale_y=1.02, tx=-6, ty=4, pivot_x=char_idle.shape[1]//2, pivot_y=char_idle.shape[0])
    blend_fg(f1, char_f1, 8, BASELINE_Y - char_idle.shape[0])
    if anvil_img is not None:
        blend_fg(f1, anvil_img, ANVIL_STRIKE_X - 18, BASELINE_Y - anvil_img.shape[0] + 5)
    frames.append(f1)
    
    # -------------------------------------------------------------
    # FRAME 2: Giơ búa đỉnh điểm (Apex / High Windup)
    # -------------------------------------------------------------
    f2 = np.zeros((FRAME_H, FRAME_W, 4), dtype=np.uint8)
    char_f2 = affine_transform(char_strike, angle_deg=-3, scale_x=1.0, scale_y=1.02, tx=-10, ty=-8, pivot_x=char_strike.shape[1]//2, pivot_y=char_strike.shape[0])
    blend_fg(f2, char_f2, -15, BASELINE_Y - char_strike.shape[0] - 8)
    if anvil_img is not None:
        blend_fg(f2, anvil_img, ANVIL_STRIKE_X - 18, BASELINE_Y - anvil_img.shape[0] + 5)
    frames.append(f2)
    
    # -------------------------------------------------------------
    # FRAME 3: Bổ búa xé gió (Downstroke / Smear Arc)
    # -------------------------------------------------------------
    f3 = np.zeros((FRAME_H, FRAME_W, 4), dtype=np.uint8)
    char_f3 = affine_transform(char_strike, angle_deg=7, scale_x=1.03, scale_y=0.96, tx=16, ty=10, pivot_x=char_strike.shape[1]//2, pivot_y=char_strike.shape[0])
    blend_fg(f3, char_f3, 0, BASELINE_Y - char_strike.shape[0] + 6)
    # Draw Motion Smear Arc
    draw_motion_smear(f3, cx=ANVIL_STRIKE_X - 25, cy=ANVIL_STRIKE_Y - 90, start_angle=-65, end_angle=25, radius=110)
    if anvil_img is not None:
        blend_fg(f3, anvil_img, ANVIL_STRIKE_X - 18, BASELINE_Y - anvil_img.shape[0] + 5)
    frames.append(f3)
    
    # -------------------------------------------------------------
    # FRAME 4: Nện trúng đe phát nổ (Impact / Spark Burst)
    # -------------------------------------------------------------
    f4 = np.zeros((FRAME_H, FRAME_W, 4), dtype=np.uint8)
    char_f4 = affine_transform(char_strike, angle_deg=10, scale_x=1.05, scale_y=0.92, tx=22, ty=18, pivot_x=char_strike.shape[1]//2, pivot_y=char_strike.shape[0])
    blend_fg(f4, char_f4, 5, BASELINE_Y - char_strike.shape[0] + 14)
    if anvil_img is not None:
        blend_fg(f4, anvil_img, ANVIL_STRIKE_X - 18, BASELINE_Y - anvil_img.shape[0] + 5)
    # Draw 360° Molten Spark Burst
    draw_spark_burst(f4, cx=ANVIL_STRIKE_X, cy=ANVIL_STRIKE_Y, intensity=1.1, count=55, seed=77)
    frames.append(f4)
    
    # -------------------------------------------------------------
    # FRAME 5: Nảy búa sau va chạm & Hồi thế (Rebound Recovery)
    # -------------------------------------------------------------
    f5 = np.zeros((FRAME_H, FRAME_W, 4), dtype=np.uint8)
    char_f5 = affine_transform(char_strike, angle_deg=3, scale_x=0.99, scale_y=0.98, tx=8, ty=4, pivot_x=char_strike.shape[1]//2, pivot_y=char_strike.shape[0])
    blend_fg(f5, char_f5, -5, BASELINE_Y - char_strike.shape[0] + 2)
    if anvil_img is not None:
        blend_fg(f5, anvil_img, ANVIL_STRIKE_X - 18, BASELINE_Y - anvil_img.shape[0] + 5)
    draw_smoke_rebound(f5, cx=ANVIL_STRIKE_X, cy=ANVIL_STRIKE_Y - 10, count=18)
    frames.append(f5)
    
    # Assemble into horizontal strip
    strip = np.zeros((FRAME_H, FRAME_W * 6, 4), dtype=np.uint8)
    for idx, f in enumerate(frames):
        strip[:, idx * FRAME_W : (idx + 1) * FRAME_W] = f
        # Save individual frame to brain for verification
        f_path = os.path.join(brain_dir, f'mortal_verified_frame_{idx}.png')
        cv2.imwrite(f_path, f)
        print(f"Saved frame {idx} to {f_path}")
        
    # Save Spritesheet Strip WebP to brain
    strip_p = os.path.join(brain_dir, 'mortal_blacksmith_strip_2160x480.webp')
    Image.fromarray(cv2.cvtColor(strip, cv2.COLOR_BGRA2RGBA)).save(strip_p, 'WEBP', lossless=True)
    print(f"Saved spritesheet strip to {strip_p}")
    
    # Copy to target destinations
    dests = [
        'webgame/assets/art/skins/skin_default',
        'frontend/public/assets/art/skins/skin_default'
    ]
    for d in dests:
        os.makedirs(d, exist_ok=True)
        # 1. Spritesheet strip
        target_strip = os.path.join(d, 'spritesheet_strip.webp')
        Image.fromarray(cv2.cvtColor(strip, cv2.COLOR_BGRA2RGBA)).save(target_strip, 'WEBP', lossless=True)
        print(f"Deployed strip to {target_strip}")
        
        # 2. Card art (using Frame 0)
        card_p = os.path.join(d, 'card.webp')
        Image.fromarray(cv2.cvtColor(frames[0], cv2.COLOR_BGRA2RGBA)).save(card_p, 'WEBP', lossless=True)
        print(f"Deployed card to {card_p}")

    # Also update root hero_spritesheet_strip.webp for backward-compatible fallback
    root_strip_webgame = 'webgame/assets/art/hero_spritesheet_strip.webp'
    root_strip_frontend = 'frontend/public/assets/art/hero_spritesheet_strip.webp'
    Image.fromarray(cv2.cvtColor(strip, cv2.COLOR_BGRA2RGBA)).save(root_strip_webgame, 'WEBP', lossless=True)
    Image.fromarray(cv2.cvtColor(strip, cv2.COLOR_BGRA2RGBA)).save(root_strip_frontend, 'WEBP', lossless=True)
    print("Deployed fallback hero_spritesheet_strip.webp")
    
    return strip

if __name__ == '__main__':
    build_spritesheet()
