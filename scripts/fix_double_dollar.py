files = [
    'frontend/src/components/CharacterCreationModal.tsx',
    'frontend/src/components/CharacterSelectionModal.tsx',
    'frontend/src/components/StatusModal.tsx'
]
target = chr(115) + chr(114) + chr(99) + chr(61) + chr(123) + chr(96) + chr(36) + chr(36) + chr(123)
replacement = chr(115) + chr(114) + chr(99) + chr(61) + chr(123) + chr(96) + chr(36) + chr(123)

for p in files:
    with open(p, 'r', encoding='utf-8') as f:
        c = f.read()
    if target in c:
        c = c.replace(target, replacement)
        with open(p, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f'Fixed {p}')
    else:
        print(f'Target not found in {p}')
