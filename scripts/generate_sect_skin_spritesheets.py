# -*- coding: utf-8 -*-
"""
Script tạo 4 bộ Assets Art Trang Phục Môn Phái (Sect Outfits) cho game Phá Trời:
1. skin_thunder_robe: Cửu Tiêu Lôi Bào (Lôi Đình - Lam Lôi & Bạc Điện)
2. skin_flame_robe: Hắc Diệm Minh Bào (Viêm Dương - Hắc Diệm & Xích Hỏa)
3. skin_mountain_robe: Bất Chu Nham Giáp (Sơn Nhạc - Huyền Nham & Hoàng Kim)
4. skin_mystic_robe: Thanh Mộc Tiên Y (Huyền Âm - Bích Ngọc & Linh Khí)
5. skin_default: Phàm Nhân Thiết Tượng (Gốc)
"""
import os
import sys
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np

BASE_DIR = 'frontend/public/assets/art'
WEBGAME_DIR = 'webgame/assets/art'

source_sheet_path = os.path.join(BASE_DIR, 'hero_spritesheet_strip.webp')
src_img = Image.open(source_sheet_path).convert('RGBA')
w, h = src_img.size
print(f"Source spritesheet size: {w}x{h}")

# Define 4 Sect Transformations
# Each transformation targets the robe/fabric while preserving human skin and hair
def is_skin_or_face(r, g, b):
    # Skin tone: R > 150, G > 115, B > 90, R > G > B, (R - G) in [15, 60]
    is_skin = (r > 155) & (g > 120) & (b > 90) & (r >= g) & (g >= b) & ((r - g) >= 15) & ((r - g) <= 75)
    return is_skin

def is_hair(r, g, b):
    # Silver-white hair: high brightness and low saturation (r ~= g ~= b > 140)
    diff = np.maximum(np.maximum(np.abs(r - g), np.abs(g - b)), np.abs(r - b))
    is_silver = (r > 130) & (g > 130) & (b > 130) & (diff < 25)
    return is_silver

def transform_robe(img, sect_type):
    arr = np.array(img, dtype=np.float32)
    r, g, b, a = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2], arr[:, :, 3]
    
    opaque = a > 40
    skin = is_skin_or_face(r, g, b) & opaque
    hair = is_hair(r, g, b) & opaque
    
    # Robe / Outfit / Hammer pixels to transform
    robe_mask = opaque & (~skin) & (~hair)
    
    # Calculate luminance of the original pixels to maintain shading/creases
    lum = 0.299 * r + 0.587 * g + 0.114 * b
    norm_lum = lum / 255.0  # 0.0 to 1.0
    
    new_r = np.copy(r)
    new_g = np.copy(g)
    new_b = np.copy(b)
    
    if sect_type == 'thunder':
        # Cửu Tiêu Lôi Bào: Sapphire blue to cyan-white highlight with electric sparks
        # Deep shadows: #081B38, Mids: #1E40AF, Highs: #38BDF8 & #E0F2FE
        tr_r = np.where(norm_lum < 0.45, norm_lum * 28 + 6, norm_lum * 180 + 40)
        tr_g = np.where(norm_lum < 0.45, norm_lum * 80 + 16, norm_lum * 220 + 35)
        tr_b = np.where(norm_lum < 0.45, norm_lum * 190 + 50, norm_lum * 255 + 20)
        
        # Give silver hair a subtle ethereal azure gloss
        hair_mask = hair & (norm_lum > 0.6)
        new_b[hair_mask] = np.clip(new_b[hair_mask] * 1.15, 0, 255)
        
    elif sect_type == 'flame':
        # Hắc Diệm Minh Bào: Obsidian black with burning vermilion-gold edges
        # Deep shadows: #150505, Mids: #7F1D1D to #DC2626, Highs: #F59E0B & #FDE68A
        tr_r = np.where(norm_lum < 0.4, norm_lum * 110 + 20, norm_lum * 255 + 40)
        tr_g = np.where(norm_lum < 0.4, norm_lum * 20 + 4, norm_lum * 120 + 10)
        tr_b = np.where(norm_lum < 0.4, norm_lum * 15 + 2, norm_lum * 40 + 5)
        
    elif sect_type == 'mountain':
        # Bất Chu Nham Giáp: Deep amethyst basalt rock with gold ore and rune veins
        # Deep shadows: #1E0E38, Mids: #581C87 to #7E22CE, Highs: #D97706 & #FCD34D
        tr_r = np.where(norm_lum < 0.45, norm_lum * 60 + 22, norm_lum * 210 + 45)
        tr_g = np.where(norm_lum < 0.45, norm_lum * 35 + 10, norm_lum * 130 + 20)
        tr_b = np.where(norm_lum < 0.45, norm_lum * 110 + 40, norm_lum * 160 + 30)
        
    elif sect_type == 'mystic':
        # Thanh Mộc Tiên Y: Emerald jade with celadon silk and mint-gold silk sashes
        # Deep shadows: #052E2B, Mids: #065F46 to #059669, Highs: #6EE7B7 & #F0FDF4
        tr_r = np.where(norm_lum < 0.45, norm_lum * 30 + 8, norm_lum * 140 + 30)
        tr_g = np.where(norm_lum < 0.45, norm_lum * 120 + 35, norm_lum * 255 + 30)
        tr_b = np.where(norm_lum < 0.45, norm_lum * 80 + 24, norm_lum * 190 + 35)

    new_r[robe_mask] = np.clip(tr_r[robe_mask], 0, 255)
    new_g[robe_mask] = np.clip(tr_g[robe_mask], 0, 255)
    new_b[robe_mask] = np.clip(tr_b[robe_mask], 0, 255)
    
    out_arr = np.stack([new_r, new_g, new_b, a], axis=-1).astype(np.uint8)
    return Image.fromarray(out_arr)

# Generate and save each skin
SKINS = [
    {
        'id': 'skin_default',
        'name': 'Phàm Nhân Thiết Tượng',
        'type': 'default',
        'palette': '#94A3B8',
        'img': src_img
    },
    {
        'id': 'skin_thunder_robe',
        'name': 'Cửu Tiêu Lôi Bào',
        'type': 'thunder',
        'palette': '#00F0FF',
        'img': transform_robe(src_img, 'thunder')
    },
    {
        'id': 'skin_flame_robe',
        'name': 'Hắc Diệm Minh Bào',
        'type': 'flame',
        'palette': '#FF5500',
        'img': transform_robe(src_img, 'flame')
    },
    {
        'id': 'skin_mountain_robe',
        'name': 'Bất Chu Nham Giáp',
        'type': 'mountain',
        'palette': '#A855F7',
        'img': transform_robe(src_img, 'mountain')
    },
    {
        'id': 'skin_mystic_robe',
        'name': 'Thanh Mộc Tiên Y',
        'type': 'mystic',
        'palette': '#10B981',
        'img': transform_robe(src_img, 'mystic')
    }
]

for sk in SKINS:
    # 1. Save in frontend
    out_dir_fe = os.path.join(BASE_DIR, 'skins', sk['id'])
    os.makedirs(out_dir_fe, exist_ok=True)
    out_path_fe = os.path.join(out_dir_fe, 'spritesheet_strip.webp')
    sk['img'].save(out_path_fe, 'WEBP', quality=92, method=6)
    
    # 2. Save in webgame
    out_dir_wg = os.path.join(WEBGAME_DIR, 'skins', sk['id'])
    os.makedirs(out_dir_wg, exist_ok=True)
    out_path_wg = os.path.join(out_dir_wg, 'spritesheet_strip.webp')
    sk['img'].save(out_path_wg, 'WEBP', quality=92, method=6)
    
    # 3. Create Avatar Card (Frame 0 crop centered)
    # Frame 0 is (0, 0, 360, 480)
    card_img = sk['img'].crop((0, 0, 360, 480))
    # Resize to clean thumbnail 270x360
    card_thumb = card_img.resize((270, 360), Image.Resampling.LANCZOS)
    card_path_fe = os.path.join(out_dir_fe, 'card.webp')
    card_path_wg = os.path.join(out_dir_wg, 'card.webp')
    card_thumb.save(card_path_fe, 'WEBP', quality=92, method=6)
    card_thumb.save(card_path_wg, 'WEBP', quality=92, method=6)
    
    print(f"Generated skin: {sk['id']} ({sk['name']}) -> {out_path_fe} ({os.path.getsize(out_path_fe)} bytes)")

print("\nALL 5 SECT SKINS & OUTFIT CARDS GENERATED SUCCESSFULLY!")
