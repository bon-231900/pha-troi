# -*- coding: utf-8 -*-
path = r"frontend/src/components/TopBossHeader.tsx"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

# Normalize and replace
dup = ') : null}\n      <div className="pointer-events-auto flex items-center gap-1.5">'
dup_crlf = ') : null}\r\n      <div className="pointer-events-auto flex items-center gap-1.5">'

if dup in text:
    text = text.replace(dup, ") : null}")
    print("Replaced dup LF")
elif dup_crlf in text:
    text = text.replace(dup_crlf, ") : null}")
    print("Replaced dup CRLF")
else:
    print("Not found, checking...")

with open(path, "w", encoding="utf-8") as f:
    f.write(text)
