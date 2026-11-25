with open(r'frontend\src\game\characterSlots.ts', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace(
    "  SECT_DEFAULT_SKIN,\n",
    "  SECT_DEFAULT_SKIN,\n  ensureAllEquippedSlots,\n"
)

with open(r'frontend\src\game\characterSlots.ts', 'w', encoding='utf-8') as f:
    f.write(c)

print("Added import to characterSlots.ts")
