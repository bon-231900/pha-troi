# -*- coding: utf-8 -*-
with open('frontend/src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

target = "    return null;\n  });\n\n  const [skillCooldowns"
replacement = "    return null;\n  });\n\n  const [equippedSkinId, setEquippedSkinId] = useState<string>(() => {\n    return safeStorage.getItem('phatroi_equipped_skin') || 'skin_default';\n  });\n\n  const [skillCooldowns"

if target not in content:
    target = target.replace("\n", "\r\n")
    replacement = replacement.replace("\n", "\r\n")

if target in content:
    content = content.replace(target, replacement, 1)
    with open('frontend/src/App.tsx', 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS: equippedSkinId state added to App.tsx!")
else:
    print("ERROR: target not found!")
