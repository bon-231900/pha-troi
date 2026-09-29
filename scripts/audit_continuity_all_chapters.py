# -*- coding: utf-8 -*-
"""
Auditing continuity, transitions, and narrative seams across all 96 chapters of Phá Trời.
"""
import os
import sys
import glob
import re
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE_DIR = r"d:\tieu-thuyet"

FORBIDDEN_WORDS = [
    "huyết mạch",
    "chương này",
    "hồi sau",
    "nhân vật chính",
    "tác giả",
    "cốt truyện",
    "bản thảo",
    "hệ thống",
    "canon",
    "database",
    "plot",
    "foreshadowing",
]

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
    
    # parse frontmatter
    meta = {}
    body = content
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            meta = parse_simple_frontmatter(parts[1])
            body = parts[2]
            
    # get clean paragraphs
    paras = [p.strip() for p in body.split("\n\n") if p.strip() and not p.strip().startswith("#")]
    return {
        "ch": ch_num,
        "path": fpath,
        "meta": meta,
        "body": body,
        "paras": paras,
        "first_paras": paras[:3] if paras else [],
        "last_paras": paras[-3:] if paras else [],
    }

def main():
    chapters = {}
    for ch in range(1, 97):
        data = load_chapter(ch)
        if data:
            chapters[ch] = data
            
    print(f"[*] Đã tải thành công {len(chapters)} chương để kiểm tra tính liên tục toàn diện.")
    
    issues = []
    
    # 1. Check forbidden words across all chapters
    print("\n--- 1. KIỂM TRA TỪ CẤM & META-WORDS TRÊN TOÀN BỘ 96 CHƯƠNG ---")
    forbidden_hits = {}
    for ch, data in chapters.items():
        body_lower = data["body"].lower()
        for fw in FORBIDDEN_WORDS:
            # check word boundary
            found = re.findall(rf"\b{re.escape(fw)}\b", body_lower)
            if found:
                if ch not in forbidden_hits:
                    forbidden_hits[ch] = []
                forbidden_hits[ch].append((fw, len(found)))
                
    if forbidden_hits:
        print(f"[-] Phát hiện {len(forbidden_hits)} chương có từ cấm / meta-words:")
        for ch, hits in forbidden_hits.items():
            print(f"    Chương {ch:03d}: {hits}")
    else:
        print("[+] 100% Sạch: Không có từ cấm hoặc meta-words nào trong toàn bộ 96 chương!")
        
    # 2. Check Transitions Between Chapter N and Chapter N+1
    print("\n--- 2. KIỂM TRA MẮT XÍCH CHUYỂN TIẾP (SEAMS) GIỮA TỪNG CẶP CHƯƠNG (N -> N+1) ---")
    seam_reports = []
    
    for ch in range(1, 96):
        c1 = chapters.get(ch)
        c2 = chapters.get(ch + 1)
        if not c1 or not c2:
            continue
            
        loc1 = c1["meta"].get("location", "")
        loc2 = c2["meta"].get("location", "")
        date1 = str(c1["meta"].get("date", ""))
        date2 = str(c2["meta"].get("date", ""))
        
        last_p = c1["last_paras"][-1] if c1["last_paras"] else ""
        first_p = c2["first_paras"][0] if c2["first_paras"] else ""
        
        # Check repeated phrases across the seam (potential loops)
        # e.g., sentences with length > 25 chars appearing in both
        s1 = set([re.sub(r'[^\w\s]', '', s.strip().lower()) for s in re.split(r'[\.\?\!\n]', last_p) if len(s.strip()) > 25])
        s2 = set([re.sub(r'[^\w\s]', '', s.strip().lower()) for s in re.split(r'[\.\?\!\n]', first_p) if len(s.strip()) > 25])
        repeats = s1.intersection(s2)
        
        # Check if last paragraph ends with a question, dialogue or cliffhanger
        is_cliffhanger = last_p.endswith("?") or last_p.endswith("!") or last_p.endswith("...") or "—" in last_p
        
        # Location change without mention
        loc_change = False
        if loc1 and loc2 and loc1 != loc2:
            # Check if loc2 is mentioned in first paragraphs of c2 or last paragraphs of c1
            main_loc2 = loc2.split(",")[0].strip()
            loc_in_c1 = any(main_loc2.lower() in p.lower() for p in c1["last_paras"])
            loc_in_c2 = any(main_loc2.lower() in p.lower() for p in c2["first_paras"])
            if not loc_in_c1 and not loc_in_c2:
                loc_change = True
                
        seam_reports.append({
            "pair": f"{ch:03d} -> {ch+1:03d}",
            "ch1_title": c1["meta"].get("title", ""),
            "ch2_title": c2["meta"].get("title", ""),
            "loc1": loc1,
            "loc2": loc2,
            "date1": date1,
            "date2": date2,
            "last_p": last_p,
            "first_p": first_p,
            "repeats": list(repeats),
            "loc_change": loc_change,
            "is_cliff": is_cliffhanger
        })
        
    print(f"[*] Đã quét qua {len(seam_reports)} mối nối giữa các chương.")
    
    # Analyze and print suspicious seams
    suspicious = []
    for s in seam_reports:
        warnings = []
        if s["repeats"]:
            warnings.append(f"Trùng lặp câu giữa 2 chương: {s['repeats']}")
        if s["loc_change"]:
            warnings.append(f"Chuyển địa điểm lớn nhưng chưa thấy cầu nối ở đầu chương: '{s['loc1']}' -> '{s['loc2']}'")
            
        if warnings:
            suspicious.append((s, warnings))
            
    print(f"\n[!] Tìm thấy {len(suspicious)} mối nối cần kiểm tra sâu về tính liên tục.")
    for s, warns in suspicious:
        print(f"\n=== MỐI NỐI {s['pair']}: [{s['ch1_title']}] -> [{s['ch2_title']}] ===")
        for w in warns:
            print(f"  [CẢNH BÁO] {w}")
        print(f"  CUỐI CHƯƠNG {s['pair'][:3]}: {s['last_p'][:150]}...")
        print(f"  ĐẦU CHƯƠNG {s['pair'][7:]}: {s['first_p'][:150]}...")

if __name__ == "__main__":
    main()
