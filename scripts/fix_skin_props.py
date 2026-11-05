with open('frontend/src/components/StatusModal.tsx', 'r', encoding='utf-8') as f:
    c = f.read()

old_props = """  playerClass?: PlayerClassMeta;
  activeCharacterName?: string;
}"""

new_props = """  playerClass?: PlayerClassMeta;
  activeCharacterName?: string;
  equippedSkinId?: string;
  onEquipSkin?: (skinId: string) => void;
}"""

if old_props in c:
    c = c.replace(old_props, new_props, 1)

old_destruct = """  playerClass,
  activeCharacterName,
}) => {"""

new_destruct = """  playerClass,
  activeCharacterName,
  equippedSkinId = 'skin_default',
  onEquipSkin,
}) => {"""

if old_destruct in c:
    c = c.replace(old_destruct, new_destruct, 1)

c = c.replace('src={`$' + '{import.meta.env', 'src={`' + '{import.meta.env')

with open('frontend/src/components/StatusModal.tsx', 'w', encoding='utf-8') as f:
    f.write(c)

print('StatusModal.tsx patched successfully')

# Also fix CharacterCreationModal.tsx and CharacterSelectionModal.tsx
for path in ['frontend/src/components/CharacterCreationModal.tsx', 'frontend/src/components/CharacterSelectionModal.tsx']:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace('src={`$' + '{import.meta.env', 'src={`' + '{import.meta.env')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'{path} image src patched successfully')
