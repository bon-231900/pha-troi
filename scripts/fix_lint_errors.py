with open(r'frontend\src\game\characterSlots.ts', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace('  ensureAllEquippedSlots,\n', '')
with open(r'frontend\src\game\characterSlots.ts', 'w', encoding='utf-8') as f:
    f.write(c)

with open(r'frontend\src\App.tsx', 'r', encoding='utf-8') as f:
    a = f.read()

a = a.replace(
    "const [equippedItems, setEquippedItems] = useState<Record<EquipmentSlotKey, EquipmentItem>>(",
    "const [equippedItems, setEquippedItems] = useState<Record<EquipmentSlotKey, EquipmentItem | null>>("
)

with open(r'frontend\src\App.tsx', 'w', encoding='utf-8') as f:
    f.write(a)

print("Fixed typing in characterSlots.ts and App.tsx")
