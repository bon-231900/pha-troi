import os
import shutil
from PIL import Image

# 1. Source strip: temp_orig_strip.webp
src_strip = 'temp_orig_strip.webp'
assert os.path.exists(src_strip), f"{src_strip} not found!"

target_skin_strip = 'frontend/public/assets/art/skins/skin_default/spritesheet_strip.webp'
target_hero_strip = 'frontend/public/assets/art/hero_spritesheet_strip.webp'
target_skin_card = 'frontend/public/assets/art/skins/skin_default/card.webp'

# Copy strip
shutil.copy2(src_strip, target_skin_strip)
shutil.copy2(src_strip, target_hero_strip)
print(f"Copied {src_strip} -> {target_skin_strip} ({os.path.getsize(target_skin_strip)} bytes)")
print(f"Copied {src_strip} -> {target_hero_strip} ({os.path.getsize(target_hero_strip)} bytes)")

# Generate card from frame 0
im = Image.open(src_strip)
f0 = im.crop((0, 0, 360, 480))
f0.save(target_skin_card, 'WEBP', quality=95)
print(f"Generated {target_skin_card} ({os.path.getsize(target_skin_card)} bytes, size={f0.size})")

# Also copy to webgame directly so local dev is in sync
webgame_skin_strip = 'webgame/assets/art/skins/skin_default/spritesheet_strip.webp'
webgame_hero_strip = 'webgame/assets/art/hero_spritesheet_strip.webp'
webgame_skin_card = 'webgame/assets/art/skins/skin_default/card.webp'

os.makedirs(os.path.dirname(webgame_skin_strip), exist_ok=True)
shutil.copy2(target_skin_strip, webgame_skin_strip)
shutil.copy2(target_hero_strip, webgame_hero_strip)
shutil.copy2(target_skin_card, webgame_skin_card)
print("Synced to webgame/assets/art successfully!")
