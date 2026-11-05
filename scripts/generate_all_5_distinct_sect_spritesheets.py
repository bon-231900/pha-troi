# -*- coding: utf-8 -*-
"""
Generate 5 authentic, completely distinct character spritesheets for Webgame Phá Trời:
1. skin_default: Phàm Nhân Thiết Tượng (Mortal Blacksmith)
2. skin_thunder_robe: Cửu Tiêu Lôi Bào (Thunder Sect - Lôi Đình)
3. skin_flame_robe: Hắc Diệm Minh Bào (Flame Sect - Viêm Dương)
4. skin_mountain_robe: Bất Chu Nham Giáp (Mountain Sect - Sơn Nhạc)
5. skin_mystic_robe: Thanh Mộc Tiên Y (Mystic Sect - Huyền Âm)

Each spritesheet has 6 frames (360x480 each, total 2160x480):
Frame 0: Idle stance by the anvil with ambient sect aura
Frame 1: Wind-up (drawing hammer back, energy gathering)
Frame 2: High Apex (hammer raised high, blazing elemental power)
Frame 3: Strike Slam (hammer slamming anvil at x=213, y=342 with impact explosion)
Frame 4: Recoil & Shockwave (impact rebound, spark shards flying)
Frame 5: Return to ready stance
"""
import os
import sys
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
        'spark_color': (255, 210, 110),
        'scale_h': 330,
        'waist_pct': 0.52,
        'char_x_offset': 0,
    },
    {
        'id': 'skin_thunder_robe',
        'name': 'Cửu Tiêu Lôi Bào',
        'cutout': f'{BRAIN}/clean_cutout_thunder.png',
        'anvil': 'frontend/public/assets/art/props/prop_anvil_lightning_dragon.webp',
        'anvil_type': 'lightning',
        'theme_color': (56, 189, 248),
        'spark_color': (224, 242, 254),
        'scale_h': 330,
        'waist_pct': 0.53,
        'char_x_offset': -4,
    },
    {
        'id': 'skin_flame_robe',
        'name': 'Hắc Diệm Minh Bào',
        'cutout': f'{BRAIN}/clean_cutout_fire.png',
        'anvil': 'frontend/public/assets/art/props/prop_anvil_fire_bagua.webp',
        'anvil_type': 'fire',
        'theme_color': (239, 68, 68),
        'spark_color': (254, 215, 170),
        'scale_h': 330,
        'waist_pct': 0.52,
        'char_x_offset': -2,
    },
    {
        'id': 'skin_mountain_robe',
        'name': 'Bất Chu Nham Giáp',
        'cutout': f'{BRAIN}/clean_cutout_mountain.png',
        'anvil': 'frontend/public/assets/art/props/prop_anvil_mountain_stone.webp',
        'anvil_type': 'mountain',
        'theme_color': (245, 158, 11),
        'spark_color': (253, 230, 138),
        'scale_h': 330,
        'waist_pct': 0.50,
        'char_x_offset': -6,
    },
    {
        'id': 'skin_mystic_robe',
        'name': 'Thanh Mộc Tiên Y',
        'cutout': f'{BRAIN}/clean_cutout_mystic.png',
        'anvil': f'{BRAIN}/clean_anvil_crop.png', # tinted jade
        'anvil_type': 'mystic',
        'theme_color': (16, 185, 129),
        'spark_color': (167, 243, 208),
        'scale_h': 330,
        'waist_pct': 0.53,
        'char_x_offset': -4,
    },
]

# Transformation definitions for 6 frames:
# (angle_deg, dx, dy, upper_scale_y, aura_alpha, is_strike, is_recoil)
TRANSFORMS = [
    (0,    0,   0, 1.00, 0.20, False, False), # Frame 0: Idle
    (-5,  -5,  -4, 1.02, 0.50, False, False), # Frame 1: Wind-up
    (-10, -9,  -9, 1.05, 0.90, False, False), # Frame 2: Apex
    (6,   12,   7, 0.97, 1.00, True,  False), # Frame 3: Strike Impact
    (2,    5,  -2, 1.00, 0.70, False, True),  # Frame 4: Recoil
    (-1,  -2,  -1, 1.00, 0.35, False, False), # Frame 5: Return
]

def load_and_tint_anvil(anvil_path, anvil_type):
    im = Image.open(anvil_path).convert('RGBA')
    aw, ah = im.size
    target_w = 95
    target_h = int(ah * (target_w / aw))
    scaled = im.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    if anvil_type == 'mystic':
        # Tint anvil with ethereal jade green & golden resonance veins
        arr = np.array(scaled, dtype=np.float32)
        r, g, b, a = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2], arr[:, :, 3]
        opaque = a > 30
        lum = (0.299 * r + 0.587 * g + 0.114 * b) / 255.0
        new_r = np.where(opaque, lum * 90 + 15, r)
        new_g = np.where(opaque, lum * 220 + 35, g)
        new_b = np.where(opaque, lum * 170 + 25, b)
        scaled = Image.fromarray(np.stack([new_r, new_g, new_b, a], axis=-1).astype(np.uint8))
        
    return scaled

def add_elemental_aura(frame, char_x, char_y, target_w, target_h, theme_color, aura_alpha, sect_type):
    """Draw ambient elemental energy around character"""
    aura_layer = Image.new('RGBA', (FRAME_W, FRAME_H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(aura_layer)
    cx = char_x + target_w // 2
    cy = char_y + int(target_h * 0.4)
    
    tr, tg, tb = theme_color
    
    if sect_type == 'thunder':
        # Electric lightning arcs
        for _ in range(int(8 * aura_alpha)):
            start_x = cx + np.random.randint(-40, 40)
            start_y = cy + np.random.randint(-60, 60)
            end_x = start_x + np.random.randint(-25, 25)
            end_y = start_y + np.random.randint(-25, 25)
            mid_x = (start_x + end_x) // 2 + np.random.randint(-12, 12)
            mid_y = (start_y + end_y) // 2 + np.random.randint(-12, 12)
            alpha = int(180 * aura_alpha)
            draw.line([(start_x, start_y), (mid_x, mid_y), (end_x, end_y)], fill=(tr, tg, tb, alpha), width=2)
            draw.ellipse([mid_x-2, mid_y-2, mid_x+2, mid_y+2], fill=(240, 250, 255, alpha))
            
    elif sect_type == 'fire':
        # Molten ember motes floating up
        for _ in range(int(12 * aura_alpha)):
            ex = cx + np.random.randint(-50, 50)
            ey = cy + np.random.randint(-60, 80)
            rad = np.random.randint(2, 4)
            alpha = int(210 * aura_alpha)
            draw.ellipse([ex - rad, ey - rad, ex + rad, ey + rad], fill=(255, np.random.randint(120, 220), 30, alpha))
            
    elif sect_type == 'mountain':
        # Floating golden basalt rune fragments
        for _ in range(int(7 * aura_alpha)):
            mx = cx + np.random.randint(-45, 45)
            my = cy + np.random.randint(-60, 60)
            sz = np.random.randint(3, 6)
            alpha = int(190 * aura_alpha)
            draw.rectangle([mx, my, mx + sz, my + sz], fill=(245, 180, 30, alpha))
            
    elif sect_type == 'mystic':
        # Floating jade wind ribbons & spirit petals
        for _ in range(int(9 * aura_alpha)):
            wx = cx + np.random.randint(-50, 50)
            wy = cy + np.random.randint(-60, 60)
            alpha = int(180 * aura_alpha)
            draw.ellipse([wx - 3, wy - 6, wx + 3, wy + 6], fill=(110, 240, 180, alpha))
            
    return Image.alpha_composite(frame, aura_layer)

def add_impact_blast(frame, impact_x, impact_y, theme_color, spark_color, sect_type):
    """Draw dramatic impact blast on anvil at (impact_x, impact_y)"""
    fx_layer = Image.new('RGBA', (FRAME_W, FRAME_H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(fx_layer)
    tr, tg, tb = theme_color
    sr, sg, sb = spark_color
    
    # 1. Radiant central flash
    for r in range(32, 4, -4):
        alpha = int(160 * (1.0 - r / 32.0))
        draw.ellipse([impact_x - r, impact_y - int(r * 0.5), impact_x + r, impact_y + int(r * 0.5)], fill=(tr, tg, tb, alpha))
    draw.ellipse([impact_x - 14, impact_y - 7, impact_x + 14, impact_y + 7], fill=(sr, sg, sb, 255))
    
    # 2. Explosive sparks / debris fountain
    np.random.seed(1337)
    num_sparks = 36 if sect_type in ['fire', 'thunder'] else 26
    for _ in range(num_sparks):
        # Angle pointing mostly upward and outwards (-160 deg to -20 deg)
        ang = np.random.uniform(np.pi * 0.85, np.pi * 2.15)
        dist = np.random.uniform(18, 75)
        ex = int(impact_x + np.cos(ang) * dist)
        ey = int(impact_y + np.sin(ang) * dist * 0.6)
        width = np.random.randint(2, 4)
        alpha = np.random.randint(180, 255)
        draw.line([(impact_x, impact_y), (ex, ey)], fill=(sr, sg, sb, alpha), width=width)
        # Spark tip
        draw.ellipse([ex - 2, ey - 2, ex + 2, ey + 2], fill=(255, 255, 255, alpha))
        
    # 3. Expanding Qi Shockwave Ring
    for ring_r in [26, 36]:
        draw.ellipse([impact_x - ring_r, impact_y - int(ring_r * 0.45), impact_x + ring_r, impact_y + int(ring_r * 0.45)], outline=(sr, sg, sb, 160), width=2)
        
    return Image.alpha_composite(frame, fx_layer)

def add_recoil_sparks(frame, impact_x, impact_y, spark_color):
    """Draw dissipating spark shards for recoil frame"""
    fx_layer = Image.new('RGBA', (FRAME_W, FRAME_H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(fx_layer)
    sr, sg, sb = spark_color
    np.random.seed(999)
    for _ in range(16):
        ang = np.random.uniform(np.pi * 0.7, np.pi * 2.3)
        dist = np.random.uniform(35, 85)
        ex = int(impact_x + np.cos(ang) * dist)
        ey = int(impact_y + np.sin(ang) * dist * 0.65)
        rad = np.random.randint(2, 4)
        draw.ellipse([ex - rad, ey - rad, ex + rad, ey + rad], fill=(sr, sg, sb, 180))
    return Image.alpha_composite(frame, fx_layer)

def generate_skin_spritesheet(cfg):
    print(f"\n==========================================")
    print(f"Generating Spritesheet for: {cfg['name']} ({cfg['id']})")
    print(f"==========================================")
    
    # 1. Load Character Cutout
    cutout = Image.open(cfg['cutout']).convert('RGBA')
    cw, ch = cutout.size
    target_h = cfg['scale_h']
    target_w = int(cw * (target_h / ch))
    c_scaled = cutout.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    # Placement
    char_base_x = CHAR_X + cfg['char_x_offset']
    base_px = char_base_x - target_w // 2
    base_py = BASELINE_Y - target_h
    waist_rel_y = int(target_h * cfg['waist_pct'])
    
    # Split into lower and upper body with feathering
    c_arr = np.array(c_scaled)
    upper_arr = c_arr.copy()
    upper_arr[waist_rel_y:, :, :] = 0
    blend_px = 12
    for i in range(blend_px):
        factor = 1.0 - (i / float(blend_px))
        upper_arr[waist_rel_y - blend_px + i, :, 3] = (upper_arr[waist_rel_y - blend_px + i, :, 3] * factor).astype(np.uint8)
        
    lower_arr = c_arr.copy()
    lower_arr[:waist_rel_y - blend_px, :, :] = 0
    for i in range(blend_px):
        factor = i / float(blend_px)
        lower_arr[waist_rel_y - blend_px + i, :, 3] = (lower_arr[waist_rel_y - blend_px + i, :, 3] * factor).astype(np.uint8)
        
    upper_img = Image.fromarray(upper_arr)
    lower_img = Image.fromarray(lower_arr)
    
    # 2. Load Sect Anvil
    anvil_scaled = load_and_tint_anvil(cfg['anvil'], cfg['anvil_type'])
    an_w, an_h = anvil_scaled.size
    an_px = 213 - an_w // 2
    an_py = BASELINE_Y - an_h
    impact_x = 213
    impact_y = 342
    
    # 3. Create 6 Frames
    sheet = Image.new('RGBA', (FRAME_W * 6, FRAME_H), (0, 0, 0, 0))
    
    sect_type = cfg['id'].replace('skin_', '').replace('_robe', '')
    if sect_type == 'default':
        sect_type = 'mortal'
        
    for f_idx, (angle, dx, dy, sy, aura_a, is_strike, is_recoil) in enumerate(TRANSFORMS):
        frame = Image.new('RGBA', (FRAME_W, FRAME_H), (0, 0, 0, 0))
        
        # A. Lower body (anchored)
        frame.paste(lower_img, (base_px, base_py), lower_img)
        
        # B. Upper body transformed
        u_w, u_h = upper_img.size
        u_scaled = upper_img.resize((u_w, int(u_h * sy)), Image.Resampling.LANCZOS)
        u_rot = u_scaled.rotate(angle, resample=Image.Resampling.BICUBIC, expand=True)
        rot_w, rot_h = u_rot.size
        up_x = base_px + (u_w - rot_w) // 2 + dx
        up_y = base_py + (u_h - rot_h) // 2 + dy - int((sy - 1.0) * u_h * 0.5)
        
        frame.paste(u_rot, (up_x, up_y), u_rot)
        
        # C. Anvil in front
        frame.paste(anvil_scaled, (an_px, an_py), anvil_scaled)
        
        # D. Elemental Aura
        if aura_a > 0:
            frame = add_elemental_aura(frame, base_px, base_py, target_w, target_h, cfg['theme_color'], aura_a, sect_type)
            
        # E. Impact FX
        if is_strike:
            frame = add_impact_blast(frame, impact_x, impact_y, cfg['theme_color'], cfg['spark_color'], sect_type)
        elif is_recoil:
            frame = add_recoil_sparks(frame, impact_x, impact_y, cfg['spark_color'])
            
        sheet.paste(frame, (f_idx * FRAME_W, 0))
        
    # Save Spritesheet
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
    print("Starting generation of 5 completely distinct character spritesheets...")
    for cfg in SKIN_CONFIGS:
        generate_skin_spritesheet(cfg)
    print("\n[SUCCESS] All 5 distinct sect spritesheets generated successfully!")

if __name__ == '__main__':
    main()
