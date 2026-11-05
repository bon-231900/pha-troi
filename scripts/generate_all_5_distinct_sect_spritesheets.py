# -*- coding: utf-8 -*-
"""
Generate 5 authentic, completely distinct character spritesheets for Webgame Phá Trời:
1. skin_default: Phàm Nhân Thiết Tượng (Mortal Blacksmith)
2. skin_thunder_robe: Cửu Tiêu Lôi Bào (Thunder Sect - Lôi Đình)
3. skin_flame_robe: Hắc Diệm Minh Bào (Flame Sect - Viêm Dương)
4. skin_mountain_robe: Bất Chu Nham Giáp (Mountain Sect - Sơn Nhạc)
5. skin_mystic_robe: Thanh Mộc Tiên Y (Mystic Sect - Huyền Âm)

CORE PRINCIPLE:
- The entire character is ALWAYS 100% WHOLE, SEAMLESS and INTACT in every frame.
- ZERO body cuts, ZERO horizontal seams, ZERO slicing.
- Kinematic whole-body transformation anchored at feet (CHAR_X, BASELINE_Y).
- Custom sect anvil placed firmly in front.
- Frame-by-frame hammer strike animation with elemental impact blast.
"""
import os
import sys
import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BRAIN = 'C:/Users/ADMIN/.gemini/antigravity/brain/4ac532ff-c4ae-4325-afcc-f630c6b43d10'
FRONTEND_SKINS = 'frontend/public/assets/art/skins'
WEBGAME_SKINS = 'webgame/assets/art/skins'

FRAME_W = 360
FRAME_H = 480
BASELINE_Y = 440
CHAR_X = 135

SKIN_CONFIGS = [
    {
        'id': 'skin_default',
        'name': 'Phàm Nhân Thiết Tượng',
        'cutout': f'{BRAIN}/clean_cutout_mortal.png',
        'anvil': f'{BRAIN}/clean_anvil_crop.png',
        'anvil_type': 'iron',
        'theme_color': (255, 180, 70),
        'spark_color': (255, 230, 140),
        'rim_color': (255, 200, 100),
        'scale_h': 330,
        'char_x_offset': 0,
        'lum_boost': 1.25,
    },
    {
        'id': 'skin_thunder_robe',
        'name': 'Cửu Tiêu Lôi Bào',
        'cutout': f'{BRAIN}/clean_cutout_thunder.png',
        'anvil': 'frontend/public/assets/art/props/prop_anvil_lightning_dragon.webp',
        'anvil_type': 'lightning',
        'theme_color': (56, 189, 248),
        'spark_color': (224, 242, 254),
        'rim_color': (125, 211, 252),
        'scale_h': 330,
        'char_x_offset': -4,
        'lum_boost': 1.15,
    },
    {
        'id': 'skin_flame_robe',
        'name': 'Hắc Diệm Minh Bào',
        'cutout': f'{BRAIN}/clean_cutout_fire.png',
        'anvil': 'frontend/public/assets/art/props/prop_anvil_fire_bagua.webp',
        'anvil_type': 'fire',
        'theme_color': (239, 68, 68),
        'spark_color': (254, 215, 170),
        'rim_color': (249, 115, 22),
        'scale_h': 330,
        'char_x_offset': -2,
        'lum_boost': 1.35,
    },
    {
        'id': 'skin_mountain_robe',
        'name': 'Bất Chu Nham Giáp',
        'cutout': f'{BRAIN}/clean_cutout_mountain.png',
        'anvil': 'frontend/public/assets/art/props/prop_anvil_mountain_stone.webp',
        'anvil_type': 'mountain',
        'theme_color': (245, 158, 11),
        'spark_color': (253, 230, 138),
        'rim_color': (251, 191, 36),
        'scale_h': 330,
        'char_x_offset': -6,
        'lum_boost': 1.28,
    },
    {
        'id': 'skin_mystic_robe',
        'name': 'Thanh Mộc Tiên Y',
        'cutout': f'{BRAIN}/clean_cutout_mystic.png',
        'anvil': f'{BRAIN}/clean_anvil_crop.png',
        'anvil_type': 'mystic',
        'theme_color': (16, 185, 129),
        'spark_color': (167, 243, 208),
        'rim_color': (52, 211, 153),
        'scale_h': 330,
        'char_x_offset': -4,
        'lum_boost': 1.18,
    },
]

# 6 Frame Keyframes (whole-body kinematic motion around feet anchor (CHAR_X, BASELINE_Y)):
# (angle_deg, scale_x, scale_y, dx, dy, aura_alpha, is_strike, is_recoil)
KEYFRAMES = [
    (0,   1.00, 1.00,  0,  0, 0.25, False, False), # 0: Ready Idle (hammer resting near anvil)
    (-4,  0.98, 1.02, -3, -4, 0.55, False, False), # 1: Wind-up (drawing hammer back, lifting body)
    (-7,  0.97, 1.04, -6, -8, 0.95, False, False), # 2: High Apex (hammer poised at peak, fully charged)
    (5,   1.04, 0.95, 10,  5, 1.00, True,  False), # 3: Heavy Strike Slam (surging forward into anvil)
    (2,   1.01, 0.98,  3, -2, 0.75, False, True),  # 4: Recoil Rebound (bouncing off anvil, sparks flying)
    (-1,  0.99, 1.01, -1, -1, 0.40, False, False), # 5: Recovery (settling smoothly back to idle)
]

def enhance_sprite_clarity(img, lum_boost, rim_color):
    """Enhance visibility against dark backgrounds with shadow lifting & luminous cel-shaded rim light"""
    arr = np.array(img, dtype=np.float32)
    r, g, b, a = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2], arr[:, :, 3]
    opaque = a > 25
    
    # Lift shadows so dark armor and robes are crisp and readable
    lum = (0.299 * r + 0.587 * g + 0.114 * b) / 255.0
    shadow_curve = np.where(opaque, np.clip(lum_boost - lum * 0.35, 1.0, 1.5), 1.0)
    
    r = np.clip(r * shadow_curve * 1.10, 0, 255)
    g = np.clip(g * shadow_curve * 1.08, 0, 255)
    b = np.clip(b * shadow_curve * 1.06, 0, 255)
    
    # Calculate silhouette rim light mask
    mask = (a > 60).astype(np.uint8) * 255
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    eroded = cv2.erode(mask, kernel, iterations=1)
    rim_mask = (mask > 0) & (eroded == 0)
    
    rr, rg, rb = rim_color
    r[rim_mask] = np.clip(r[rim_mask] * 0.35 + rr * 0.65, 0, 255)
    g[rim_mask] = np.clip(g[rim_mask] * 0.35 + rg * 0.65, 0, 255)
    b[rim_mask] = np.clip(b[rim_mask] * 0.35 + rb * 0.65, 0, 255)
    
    out_arr = np.stack([r, g, b, a], axis=-1).astype(np.uint8)
    return Image.fromarray(out_arr)

def transform_whole_body(img, angle_deg, scale_x, scale_y, dx, dy, anchor_x, anchor_y):
    """Transform the whole character image around the feet anchor with ZERO cuts"""
    arr = np.array(img)
    rad = np.radians(angle_deg)
    cos_a = np.cos(rad) * scale_x
    sin_a = np.sin(rad) * scale_y
    M = np.float32([
        [cos_a, -sin_a, (1 - cos_a) * anchor_x + sin_a * anchor_y + dx],
        [sin_a,  cos_a, -sin_a * anchor_x + (1 - cos_a) * anchor_y + dy]
    ])
    transformed = cv2.warpAffine(arr, M, (FRAME_W, FRAME_H), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_CONSTANT, borderValue=(0,0,0,0))
    return Image.fromarray(transformed)

def load_and_tint_anvil(anvil_path, anvil_type):
    im = Image.open(anvil_path).convert('RGBA')
    aw, ah = im.size
    target_w = 95
    target_h = int(ah * (target_w / aw))
    scaled = im.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    if anvil_type == 'mystic':
        arr = np.array(scaled, dtype=np.float32)
        r, g, b, a = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2], arr[:, :, 3]
        opaque = a > 30
        lum = (0.299 * r + 0.587 * g + 0.114 * b) / 255.0
        new_r = np.where(opaque, lum * 90 + 20, r)
        new_g = np.where(opaque, lum * 230 + 40, g)
        new_b = np.where(opaque, lum * 180 + 30, b)
        scaled = Image.fromarray(np.stack([new_r, new_g, new_b, a], axis=-1).astype(np.uint8))
        
    return scaled

def add_elemental_aura(frame, char_x, char_y, target_w, target_h, theme_color, aura_alpha, sect_type):
    aura_layer = Image.new('RGBA', (FRAME_W, FRAME_H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(aura_layer)
    cx = char_x + target_w // 2
    cy = char_y + int(target_h * 0.4)
    tr, tg, tb = theme_color
    
    if sect_type == 'thunder':
        for _ in range(int(8 * aura_alpha)):
            start_x = cx + np.random.randint(-40, 40)
            start_y = cy + np.random.randint(-60, 60)
            end_x = start_x + np.random.randint(-25, 25)
            end_y = start_y + np.random.randint(-25, 25)
            mid_x = (start_x + end_x) // 2 + np.random.randint(-12, 12)
            mid_y = (start_y + end_y) // 2 + np.random.randint(-12, 12)
            alpha = int(190 * aura_alpha)
            draw.line([(start_x, start_y), (mid_x, mid_y), (end_x, end_y)], fill=(tr, tg, tb, alpha), width=2)
            draw.ellipse([mid_x-2, mid_y-2, mid_x+2, mid_y+2], fill=(240, 250, 255, alpha))
            
    elif sect_type == 'fire':
        for _ in range(int(14 * aura_alpha)):
            ex = cx + np.random.randint(-50, 50)
            ey = cy + np.random.randint(-60, 80)
            rad = np.random.randint(2, 4)
            alpha = int(220 * aura_alpha)
            draw.ellipse([ex - rad, ey - rad, ex + rad, ey + rad], fill=(255, np.random.randint(120, 220), 30, alpha))
            
    elif sect_type == 'mountain':
        for _ in range(int(8 * aura_alpha)):
            mx = cx + np.random.randint(-45, 45)
            my = cy + np.random.randint(-60, 60)
            sz = np.random.randint(3, 6)
            alpha = int(200 * aura_alpha)
            draw.rectangle([mx, my, mx + sz, my + sz], fill=(245, 180, 30, alpha))
            
    elif sect_type == 'mystic':
        for _ in range(int(10 * aura_alpha)):
            wx = cx + np.random.randint(-50, 50)
            wy = cy + np.random.randint(-60, 60)
            alpha = int(190 * aura_alpha)
            draw.ellipse([wx - 3, wy - 6, wx + 3, wy + 6], fill=(110, 240, 180, alpha))
            
    return Image.alpha_composite(frame, aura_layer)

def add_impact_blast(frame, impact_x, impact_y, theme_color, spark_color, sect_type):
    fx_layer = Image.new('RGBA', (FRAME_W, FRAME_H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(fx_layer)
    tr, tg, tb = theme_color
    sr, sg, sb = spark_color
    
    for r in range(36, 4, -4):
        alpha = int(180 * (1.0 - r / 36.0))
        draw.ellipse([impact_x - r, impact_y - int(r * 0.5), impact_x + r, impact_y + int(r * 0.5)], fill=(tr, tg, tb, alpha))
    draw.ellipse([impact_x - 16, impact_y - 8, impact_x + 16, impact_y + 8], fill=(sr, sg, sb, 255))
    
    np.random.seed(1337)
    num_sparks = 36 if sect_type in ['fire', 'thunder'] else 28
    for _ in range(num_sparks):
        ang = np.random.uniform(np.pi * 0.85, np.pi * 2.15)
        dist = np.random.uniform(18, 80)
        ex = int(impact_x + np.cos(ang) * dist)
        ey = int(impact_y + np.sin(ang) * dist * 0.6)
        width = np.random.randint(2, 4)
        alpha = np.random.randint(190, 255)
        draw.line([(impact_x, impact_y), (ex, ey)], fill=(sr, sg, sb, alpha), width=width)
        draw.ellipse([ex - 2, ey - 2, ex + 2, ey + 2], fill=(255, 255, 255, alpha))
        
    for ring_r in [28, 40]:
        draw.ellipse([impact_x - ring_r, impact_y - int(ring_r * 0.45), impact_x + ring_r, impact_y + int(ring_r * 0.45)], outline=(sr, sg, sb, 180), width=2)
        
    return Image.alpha_composite(frame, fx_layer)

def add_recoil_sparks(frame, impact_x, impact_y, spark_color):
    fx_layer = Image.new('RGBA', (FRAME_W, FRAME_H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(fx_layer)
    sr, sg, sb = spark_color
    np.random.seed(999)
    for _ in range(18):
        ang = np.random.uniform(np.pi * 0.7, np.pi * 2.3)
        dist = np.random.uniform(35, 90)
        ex = int(impact_x + np.cos(ang) * dist)
        ey = int(impact_y + np.sin(ang) * dist * 0.65)
        rad = np.random.randint(2, 4)
        draw.ellipse([ex - rad, ey - rad, ex + rad, ey + rad], fill=(sr, sg, sb, 200))
    return Image.alpha_composite(frame, fx_layer)

def generate_skin_spritesheet(cfg):
    print(f"\n==========================================")
    print(f"Generating Whole-Body Spritesheet (ZERO CUTS) for: {cfg['name']} ({cfg['id']})")
    print(f"==========================================")
    
    # 1. Load and enhance cutout
    cutout = Image.open(cfg['cutout']).convert('RGBA')
    cutout = enhance_sprite_clarity(cutout, cfg['lum_boost'], cfg['rim_color'])
    
    cw, ch = cutout.size
    target_h = cfg['scale_h']
    target_w = int(cw * (target_h / ch))
    c_scaled = cutout.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    # Base character frame (placed on 360x480 canvas, feet at BASELINE_Y)
    char_base_x = CHAR_X + cfg['char_x_offset']
    base_frame = Image.new('RGBA', (FRAME_W, FRAME_H), (0, 0, 0, 0))
    base_px = char_base_x - target_w // 2
    base_py = BASELINE_Y - target_h
    base_frame.paste(c_scaled, (base_px, base_py), c_scaled)
    
    # Feet anchor for whole-body transformation
    anchor_x = char_base_x
    anchor_y = BASELINE_Y
    
    # 2. Load Sect Anvil
    anvil_scaled = load_and_tint_anvil(cfg['anvil'], cfg['anvil_type'])
    an_w, an_h = anvil_scaled.size
    an_px = 213 - an_w // 2
    an_py = BASELINE_Y - an_h
    impact_x = 213
    impact_y = 342
    
    # 3. Create 6 Frames with Whole-Body Transformation (ZERO CUTS)
    sheet = Image.new('RGBA', (FRAME_W * 6, FRAME_H), (0, 0, 0, 0))
    sect_type = cfg['id'].replace('skin_', '').replace('_robe', '')
    if sect_type == 'default':
        sect_type = 'mortal'
        
    for f_idx, (angle, sx, sy, dx, dy, aura_a, is_strike, is_recoil) in enumerate(KEYFRAMES):
        # Transform the WHOLE character around feet anchor with zero slicing
        frame = transform_whole_body(base_frame, angle, sx, sy, dx, dy, anchor_x, anchor_y)
        
        # Anvil placed firmly in front on dais
        frame.paste(anvil_scaled, (an_px, an_py), anvil_scaled)
        
        # Elemental Aura
        if aura_a > 0:
            frame = add_elemental_aura(frame, base_px, base_py, target_w, target_h, cfg['theme_color'], aura_a, sect_type)
            
        # Impact Blast FX
        if is_strike:
            frame = add_impact_blast(frame, impact_x, impact_y, cfg['theme_color'], cfg['spark_color'], sect_type)
        elif is_recoil:
            frame = add_recoil_sparks(frame, impact_x, impact_y, cfg['spark_color'])
            
        sheet.paste(frame, (f_idx * FRAME_W, 0))
        
    # Save to both frontend and webgame
    out_dirs = [
        os.path.join(FRONTEND_SKINS, cfg['id']),
        os.path.join(WEBGAME_SKINS, cfg['id'])
    ]
    for d in out_dirs:
        os.makedirs(d, exist_ok=True)
        out_webp = os.path.join(d, 'spritesheet_strip.webp')
        sheet.save(out_webp, 'WEBP', quality=95, method=6)
        print(f"-> Saved: {out_webp} ({sheet.size[0]}x{sheet.size[1]})")

def main():
    print("Starting generation of 5 completely distinct, UNBROKEN character spritesheets...")
    for cfg in SKIN_CONFIGS:
        generate_skin_spritesheet(cfg)
    print("\n[SUCCESS] All 5 distinct sect spritesheets generated successfully with ZERO cuts!")

if __name__ == '__main__':
    main()
