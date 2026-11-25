with open(r'frontend\src\game\characterSlots.ts', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = [l for l in lines if l.strip() != 'ensureAllEquippedSlots,']

with open(r'frontend\src\game\characterSlots.ts', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Cleaned stray line")
