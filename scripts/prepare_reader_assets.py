# -*- coding: utf-8 -*-
"""Prepare and optimize image assets for Phá Trời Web Reader."""

import os
import shutil
from PIL import Image

SRC_LOGO = r"C:/Users/ADMIN/.gemini/antigravity/brain/27f361fe-4c12-45ac-8f78-bc13847be80a/.user_uploaded/media_1789466559985.jpg"
SRC_VERTICAL = r"C:/Users/ADMIN/.gemini/antigravity/brain/27f361fe-4c12-45ac-8f78-bc13847be80a/.user_uploaded/media_1789466560022.jpg"
SRC_HORIZONTAL = r"C:/Users/ADMIN/.gemini/antigravity/brain/27f361fe-4c12-45ac-8f78-bc13847be80a/.user_uploaded/media_1789466560052.jpg"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_ASSETS_DIR = os.path.join(BASE_DIR, "system", "reader_app", "static", "assets")
DIST_ASSETS_DIR = os.path.join(BASE_DIR, "system", "reader_app", "dist", "assets")

def process_assets():
    os.makedirs(STATIC_ASSETS_DIR, exist_ok=True)
    os.makedirs(DIST_ASSETS_DIR, exist_ok=True)

    assets_map = [
        ("logo", SRC_LOGO),
        ("cover_vertical", SRC_VERTICAL),
        ("hero_horizontal", SRC_HORIZONTAL),
    ]

    for name, src_path in assets_map:
        if not os.path.exists(src_path):
            print(f"[-] Source not found: {src_path}")
            continue

        jpg_dst = os.path.join(STATIC_ASSETS_DIR, f"{name}.jpg")
        webp_dst = os.path.join(STATIC_ASSETS_DIR, f"{name}.webp")
        shutil.copy2(src_path, jpg_dst)

        with Image.open(src_path) as img:
            print(f"[+] {name}: size={img.size}, mode={img.mode}")
            img.save(webp_dst, "WEBP", quality=90, method=6)

        # Copy to dist as well
        shutil.copy2(jpg_dst, os.path.join(DIST_ASSETS_DIR, f"{name}.jpg"))
        shutil.copy2(webp_dst, os.path.join(DIST_ASSETS_DIR, f"{name}.webp"))
        print(f"  [+] Saved {name}.jpg ({os.path.getsize(jpg_dst):,} B) & {name}.webp ({os.path.getsize(webp_dst):,} B)")

if __name__ == "__main__":
    process_assets()
