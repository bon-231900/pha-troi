import os
from PIL import Image

SRC_DIR = r"d:\tieu-thuyet\frontend\public\assets\art\ui\arsenal"
DEST_WEB = r"d:\tieu-thuyet\webgame\assets\art\ui\arsenal"
os.makedirs(DEST_WEB, exist_ok=True)

files = [
    "board_header_plaque.png",
    "board_corner_bracket.png",
    "board_close_seal.png",
    "board_divider_filigree.png",
    "board_forge_texture.png",
]

for f in files:
    src_path = os.path.join(SRC_DIR, f)
    if os.path.exists(src_path):
        im = Image.open(src_path)
        base_name = os.path.splitext(f)[0]
        webp_name = base_name + ".webp"
        
        # Save as webp in frontend
        fe_webp = os.path.join(SRC_DIR, webp_name)
        im.save(fe_webp, "WEBP", quality=90)
        
        # Save as webp in webgame
        wg_webp = os.path.join(DEST_WEB, webp_name)
        im.save(wg_webp, "WEBP", quality=90)
        
        print(f"[OK] Converted {f} -> {webp_name}")
