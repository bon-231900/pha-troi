with open('frontend/src/game/rules.ts', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace(
    "spritesheetPath: 'assets/art/skins/skin_mystic_fairy/spritesheet_strip.webp?v=20261106_v1',",
    "spritesheetPath: 'assets/art/skins/skin_mystic_fairy/spritesheet_strip.webp?v=20261107_lotus_v2',"
)
text = text.replace(
    "cardPath: 'assets/art/skins/skin_mystic_fairy/card.webp?v=20261106_v1',",
    "cardPath: 'assets/art/skins/skin_mystic_fairy/card.webp?v=20261107_lotus_v2',"
)

with open('frontend/src/game/rules.ts', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated fairy cache busters in rules.ts!')
