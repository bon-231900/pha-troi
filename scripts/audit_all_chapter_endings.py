# -*- coding: utf-8 -*-
"""
Auditing all 96 chapter endings in Phá Trời:
Detecting tacked-on artificial cliffhangers, dangling tokens, dropped threads,
and disconnected transitions to the next chapter.
"""
import os
import sys
import glob
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE_DIR = r"d:\tieu-thuyet"

def parse_simple_frontmatter(yaml_str):
    meta = {}
    for line in yaml_str.split("\n"):
        line = line.strip()
        if ":" in line and not line.startswith("#"):
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip('"\'')
    return meta

def load_chapter(ch_num):
    matches = glob.glob(os.path.join(BASE_DIR, "manuscript", "markdown", "**", f"ch_{ch_num:03d}.md"), recursive=True)
    if not matches:
        return None
    fpath = matches[0]
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    
    meta = {}
    body = content
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            meta = parse_simple_frontmatter(parts[1])
            body = parts[2]
            
    paras = [p.strip() for p in body.split("\n\n") if p.strip() and not p.strip().startswith("#")]
    return {
        "ch": ch_num,
        "path": fpath,
        "meta": meta,
        "body": body,
        "paras": paras,
        "first_paras": paras[:2] if paras else [],
        "last_paras": paras[-2:] if paras else [],
    }

def audit_endings():
    chapters = {}
    for ch in range(1, 97):
        data = load_chapter(ch)
        if data:
            chapters[ch] = data

    print("=" * 80)
    print("        RÀ SOÁT TẤT CẢ 96 KẾT CHƯƠNG VÀ ĐẦU CHƯƠNG TIẾP THEO")
    print("=" * 80)

    # Patterns of artificial tacked-on endings:
    # "Đột nhiên", "Bỗng nhiên", "Bất thần", "Nhưng ngay khi", "Ngay khoảnh khắc", "Một tiếng", "Một bóng", "Một vệt", "Ai đó"
    CLIFF_STARTERS = [
        "đột nhiên", "bỗng nhiên", "bất thần", "nhưng ngay khi", "ngay khoảnh khắc",
        "nhưng đúng vào", "ai đó đã", "một âm thanh", "một bóng người", "một đốm sáng",
        "một tiếng", "một vệt", "một chiếc", "một cánh"
    ]

    suspicious_endings = []

    for ch in range(1, 96):
        c1 = chapters.get(ch)
        c2 = chapters.get(ch + 1)
        if not c1 or not c2:
            continue

        last_p = c1["last_paras"][-1] if c1["last_paras"] else ""
        prev_to_last_p = c1["last_paras"][-2] if len(c1["last_paras"]) >= 2 else ""
        end_text = prev_to_last_p + "\n\n" + last_p

        first_p = c2["first_paras"][0] if c2["first_paras"] else ""
        second_p = c2["first_paras"][1] if len(c2["first_paras"]) >= 2 else ""
        start_text = first_p + "\n\n" + second_p

        # Check if ending has a sudden tacked-on cliffhanger
        has_sudden_cliff = False
        found_starter = ""
        for cs in CLIFF_STARTERS:
            if cs in last_p.lower() or cs in prev_to_last_p.lower():
                has_sudden_cliff = True
                found_starter = cs
                break

        # Check if the object/event in last_p is mentioned in start_text of c2
        # Extract potential nouns/objects in last_p
        # e.g., words in quotes, capitalized proper nouns, or distinct keywords
        quoted_items = re.findall(r'["“\‘\*]([^"”\’\*]{3,40})["”\’\*]', last_p)
        
        # Check connection
        resolved_in_next = False
        for qi in quoted_items:
            # check if qi or significant words of qi are in start_text
            words = [w for w in re.split(r'\W+', qi) if len(w) > 3]
            if any(w.lower() in start_text.lower() for w in words):
                resolved_in_next = True
                break

        # Check if c2 starts with something completely unrelated
        suspicious_endings.append({
            "ch": ch,
            "next_ch": ch + 1,
            "title1": c1["meta"].get("title", ""),
            "title2": c2["meta"].get("title", ""),
            "last_p": last_p,
            "first_p": first_p,
            "has_sudden_cliff": has_sudden_cliff,
            "starter": found_starter,
            "quoted_items": quoted_items,
            "resolved": resolved_in_next
        })

    # Print summary
    print(f"\n[+] Tổng số kết chương đã phân tích: {len(suspicious_endings)}")
    
    # Filter those with sudden cliffhanger
    sudden_cliffs = [s for s in suspicious_endings if s["has_sudden_cliff"]]
    print(f"[!] Phát hiện {len(sudden_cliffs)} kết chương có dấu hiệu 'Đột nhiên / Bỗng nhiên / Nhồi đồ vật bí ẩn ở đoạn cuối':")

    for s in sudden_cliffs:
        print(f"\n--- Chương {s['ch']:02d} ({s['title1']}) -> Chương {s['next_ch']:02d} ({s['title2']}) ---")
        print(f"  [Dấu hiệu]: '{s['starter']}' | Đối tượng nổi bật: {s['quoted_items']}")
        print(f"  CUỐI {s['ch']:02d}:\n    {s['last_p'][:250]}...")
        print(f"  ĐẦU {s['next_ch']:02d}:\n    {s['first_p'][:250]}...")

if __name__ == "__main__":
    audit_endings()
