import os, glob, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

for ch in range(80, 97):
    fn = f"manuscript/markdown/volume_01/arc_02/ch_{ch:03d}.md"
    if not os.path.exists(fn):
        continue
    with open(fn, "r", encoding="utf-8") as f:
        lines = f.readlines()
    title = ""
    desc = ""
    for l in lines:
        if l.startswith("title:"):
            title = l.replace("title:", "").strip().strip('"\'')
        if l.startswith("description:"):
            desc = l.replace("description:", "").strip().strip('"\'')
    
    # get last paragraph and first paragraph of body
    body_lines = [l for l in lines if not l.startswith("---") and not l.startswith("#")]
    text = "".join(body_lines)
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    first_p = paragraphs[0] if paragraphs else ""
    last_p = paragraphs[-1] if paragraphs else ""
    
    print(f"=== CH {ch:03d}: {title} ===")
    print(f"DESC: {desc[:100]}...")
    print(f"FIRST: {first_p[:100]}...")
    print(f"LAST:  {last_p[:100]}...\n")
