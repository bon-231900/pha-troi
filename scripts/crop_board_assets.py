import os
from PIL import Image

DIR_FE = r"frontend\public\assets\art\ui\arsenal"
DIR_WG = r"webgame\assets\art\ui\arsenal"

files = [
    "board_header_plaque",
    "board_corner_bracket",
    "board_close_seal",
    "board_divider_filigree",
]

for name in files:
    png_path = os.path.join(DIR_FE, f"{name}.png")
    if not os.path.exists(png_path):
        continue
    im = Image.open(png_path).convert("RGBA")
    bbox = im.getbbox()
    if bbox:
        # Add 4px padding
        w, h = im.size
        pad_bbox = (
            max(0, bbox[0] - 4),
            max(0, bbox[1] - 4),
            min(w, bbox[2] + 4),
            min(h, bbox[3] + 4),
        )
        cropped = im.crop(pad_bbox)
        
        # Save cropped webp
        for d in [DIR_FE, DIR_WG]:
            os.makedirs(d, exist_ok=True)
            webp_out = os.path.join(d, f"{name}.webp")
            cropped.save(webp_out, "WEBP", quality=92)
            png_out = os.path.join(d, f"{name}.png")
            cropped.save(png_out, "PNG")
        print(f"[CROPPED] {name}: from {im.size} to {cropped.size}")
