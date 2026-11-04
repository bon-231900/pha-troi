# -*- coding: utf-8 -*-
import os
import sys
from PIL import Image, ImageOps, ImageEnhance

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE_ART_DIR = r"D:\tieu-thuyet\frontend\public\assets\art"
WEBGAME_ART_DIR = r"D:\tieu-thuyet\webgame\assets\art"

os.makedirs(BASE_ART_DIR, exist_ok=True)
os.makedirs(WEBGAME_ART_DIR, exist_ok=True)

def key_out_black_background(img, threshold=20, softness=30):
    """
    Luminance-based alpha keying for pure black background
    """
    img = img.convert("RGBA")
    gray = ImageOps.grayscale(img)
    
    def map_alpha(val):
        if val <= threshold:
            return 0
        elif val >= threshold + softness:
            return 255
        else:
            return int(((val - threshold) / softness) * 255)
            
    alpha_mask = gray.point(map_alpha)
    img.putalpha(alpha_mask)
    return img

def process_file(src_path, out_name, key_black=True, max_width=1920, threshold=22, softness=32):
    if not os.path.exists(src_path):
        print(f"[-] Không tìm thấy: {src_path}")
        return False
        
    print(f"[+] Đang xử lý: {os.path.basename(src_path)} -> {out_name}...")
    img = Image.open(src_path)
    
    if key_black:
        img = key_out_black_background(img, threshold=threshold, softness=softness)
    else:
        img = img.convert("RGBA")
        
    if img.width > max_width:
        ratio = max_width / img.width
        new_size = (max_width, int(img.height * ratio))
        img = img.resize(new_size, Image.Resampling.LANCZOS)
        
    out1 = os.path.join(BASE_ART_DIR, out_name)
    out2 = os.path.join(WEBGAME_ART_DIR, out_name)
    
    img.save(out1, "WEBP", quality=90, method=6)
    img.save(out2, "WEBP", quality=90, method=6)
    
    kb = os.path.getsize(out1) / 1024
    print(f"    -> Thành công: {out_name} ({img.width}x{img.height}, {kb:.1f} KB)")
    return True

if __name__ == "__main__":
    artifacts = [
        (
            r"C:\Users\ADMIN\.gemini\antigravity\brain\4ac532ff-c4ae-4325-afcc-f630c6b43d10\altar_platform_raw_1793785173359.jpg",
            "altar_platform.webp",
            True,
            1400,
            24,
            35
        ),
        (
            r"C:\Users\ADMIN\.gemini\antigravity\brain\4ac532ff-c4ae-4325-afcc-f630c6b43d10\celestial_furnace_raw_1793785184654.jpg",
            "celestial_furnace.webp",
            True,
            900,
            22,
            30
        ),
        (
            r"C:\Users\ADMIN\.gemini\antigravity\brain\4ac532ff-c4ae-4325-afcc-f630c6b43d10\mountain_backdrop_raw_1793785186777.jpg",
            "mountain_backdrop.webp",
            False,
            1920,
            0,
            0
        ),
        (
            r"C:\Users\ADMIN\.gemini\antigravity\brain\4ac532ff-c4ae-4325-afcc-f630c6b43d10\foreground_pillars_raw_1793785189001.jpg",
            "foreground_pillars.webp",
            True,
            1920,
            22,
            32
        ),
    ]
    
    for src, out, kb, mw, th, sf in artifacts:
        process_file(src, out, key_black=kb, max_width=mw, threshold=th, softness=sf)
