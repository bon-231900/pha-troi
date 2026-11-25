import os
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import numpy as np

BRAIN_DIR = r"C:\Users\ADMIN\.gemini\antigravity\brain\73b9c58f-058c-426a-b43f-d34ec4624adc"

def save_webp_dual(im, filename, size, subfolder):
    p1 = os.path.join("frontend", "public", "assets", "art", subfolder, filename)
    p2 = os.path.join("webgame", "assets", "art", subfolder, filename)
    
    if im.size != size:
        im = im.resize(size, Image.Resampling.LANCZOS)
        
    os.makedirs(os.path.dirname(p1), exist_ok=True)
    os.makedirs(os.path.dirname(p2), exist_ok=True)
    
    im.save(p1, "WEBP", quality=90)
    im.save(p2, "WEBP", quality=90)
    print(f"[OK] Generated & saved: {filename} ({size[0]}x{size[1]})")

def make_fortune_rune():
    # Base from gem_rune_thunder or mystic, turn into radiant golden solar diamond
    src = os.path.join(BRAIN_DIR, "gem_rune_thunder_1794018140059.jpg")
    if not os.path.exists(src):
        return
    im = Image.open(src).convert("RGB")
    arr = np.array(im, dtype=np.float32)
    
    # Cyan has high G and B. Turn it into Golden Sun (High R and G, lower B)
    r = arr[:, :, 0]
    g = arr[:, :, 1]
    b = arr[:, :, 2]
    
    # Calculate luminance
    lum = (r * 0.299 + g * 0.587 + b * 0.114)
    
    new_r = np.clip(lum * 1.35 + 20, 0, 255)
    new_g = np.clip(lum * 1.05 + 5, 0, 255)
    new_b = np.clip(lum * 0.25, 0, 255)
    
    gold_arr = np.dstack([new_r, new_g, new_b]).astype(np.uint8)
    gold_im = Image.fromarray(gold_arr)
    
    # Add brightness & contrast punch
    enh = ImageEnhance.Color(gold_im).enhance(1.4)
    enh = ImageEnhance.Contrast(enh).enhance(1.25)
    
    save_webp_dual(enh, "gem_rune_fortune.webp", (256, 256), "runes")

def make_apron():
    src = os.path.join("frontend", "public", "assets", "art", "items", "item_apron.webp")
    if os.path.exists(src):
        im = Image.open(src).convert("RGBA")
        enh = ImageEnhance.Contrast(im).enhance(1.2)
        enh = ImageEnhance.Brightness(enh).enhance(1.1)
        save_webp_dual(enh, "item_apron_celestial_mail.webp", (512, 512), "items")

def make_relic():
    src = os.path.join("frontend", "public", "assets", "art", "items", "item_relic.webp")
    if os.path.exists(src):
        im = Image.open(src).convert("RGBA")
        enh = ImageEnhance.Contrast(im).enhance(1.25)
        enh = ImageEnhance.Color(enh).enhance(1.3)
        save_webp_dual(enh, "item_relic_bagua_core.webp", (512, 512), "items")

def make_sigil_pen():
    # Armor Pen (Golden Amber / Pierce) from sigil_stat_str
    src = os.path.join(BRAIN_DIR, "sigil_stat_str_1794018165717.jpg")
    if os.path.exists(src):
        im = Image.open(src).convert("RGB")
        arr = np.array(im, dtype=np.float32)
        r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
        lum = r * 0.299 + g * 0.587 + b * 0.114
        
        # Golden amber pierce hue
        new_r = np.clip(lum * 1.3 + 15, 0, 255)
        new_g = np.clip(lum * 0.95 + 5, 0, 255)
        new_b = np.clip(lum * 0.2, 0, 255)
        
        pen_im = Image.fromarray(np.dstack([new_r, new_g, new_b]).astype(np.uint8))
        pen_im = ImageEnhance.Contrast(pen_im).enhance(1.3)
        save_webp_dual(pen_im, "sigil_stat_pen.webp", (128, 128), "sigils")

def make_sigil_spr():
    # Spirit Lotus (Amethyst Violet) from sigil_stat_agi
    src = os.path.join(BRAIN_DIR, "sigil_stat_agi_1794018193782.jpg")
    if os.path.exists(src):
        im = Image.open(src).convert("RGB")
        arr = np.array(im, dtype=np.float32)
        r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
        lum = r * 0.299 + g * 0.587 + b * 0.114
        
        # Royal purple / amethyst hue
        new_r = np.clip(lum * 1.15 + 20, 0, 255)
        new_g = np.clip(lum * 0.5, 0, 255)
        new_b = np.clip(lum * 1.35 + 30, 0, 255)
        
        spr_im = Image.fromarray(np.dstack([new_r, new_g, new_b]).astype(np.uint8))
        spr_im = ImageEnhance.Contrast(spr_im).enhance(1.25)
        save_webp_dual(spr_im, "sigil_stat_spr.webp", (128, 128), "sigils")

if __name__ == "__main__":
    make_fortune_rune()
    make_apron()
    make_relic()
    make_sigil_pen()
    make_sigil_spr()
    print("All supplementary assets generated successfully!")
