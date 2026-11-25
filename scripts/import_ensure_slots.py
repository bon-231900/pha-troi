with open(r'frontend\src\game\characterSlots.ts', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace(
    "INITIAL_EQUIPPED_SLOTS,\n",
    "INITIAL_EQUIPPED_SLOTS,\n  ensureAllEquippedSlots,\n"
)

with open(r'frontend\src\game\characterSlots.ts', 'w', encoding='utf-8') as f:
    f.write(c)

print("Imported ensureAllEquippedSlots into characterSlots.ts")
