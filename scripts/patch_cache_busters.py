# -*- coding: utf-8 -*-
import re

# 1. Patch rules.ts
with open('frontend/src/game/rules.ts', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace asset paths with versioned paths
text = re.sub(r"spritesheet_strip\.webp(\?v=[^']*)?'", "spritesheet_strip.webp?v=20261105_v3'", text)
text = re.sub(r"card\.webp(\?v=[^']*)?'", "card.webp?v=20261105_v3'", text)

with open('frontend/src/game/rules.ts', 'w', encoding='utf-8') as f:
    f.write(text)
print('Updated frontend/src/game/rules.ts')

# 2. Patch CommunityPanoramicForgeCanvas.tsx
with open('frontend/src/components/CommunityPanoramicForgeCanvas.tsx', 'r', encoding='utf-8') as f:
    text = f.read()

text = re.sub(
    r"assets/art/skins/\$\{equippedSkinId\}/spritesheet_strip\.webp(\?v=[^`]*)?`",
    r"assets/art/skins/${equippedSkinId}/spritesheet_strip.webp?v=20261105_v3`",
    text
)
with open('frontend/src/components/CommunityPanoramicForgeCanvas.tsx', 'w', encoding='utf-8') as f:
    f.write(text)
print('Updated CommunityPanoramicForgeCanvas.tsx')

# 3. Patch InteractiveAltarPreview.tsx
with open('frontend/src/components/InteractiveAltarPreview.tsx', 'r', encoding='utf-8') as f:
    text = f.read()

# Check srcPath
text = text.replace(
    "${cleanBase}${skinMeta.spritesheetPath}",
    "${cleanBase}${skinMeta.spritesheetPath}" # already has ?v from rules.ts
)
with open('frontend/src/components/InteractiveAltarPreview.tsx', 'w', encoding='utf-8') as f:
    f.write(text)
print('Updated InteractiveAltarPreview.tsx')
