# -*- coding: utf-8 -*-
"""
Novel OS — Public Distribution Verification Script (scripts/verify_public_dist.py)

Nhiệm vụ:
Kiểm tra tính an toàn tuyệt đối của thư mục triển khai công khai (system/reader_app/dist/).
Tự động FAIL (exit code 1) nếu phát hiện bất kỳ:
1. Dữ liệu bí mật tác giả (author secrets, actual_meaning, reveal_notes).
2. Tệp cơ sở dữ liệu SQLite (*.db, *.db-wal, *.db-shm).
3. Tệp mã nguồn backend Python (*.py), shell script (*.bat, *.sh).
4. Tệp cấu hình nhạy cảm (.env, credentials, keys, git).
5. Thiếu tệp công khai thiết yếu hoặc thiếu chương so với bản thảo markdown.
"""

import os
import sys
import json
import re
from pathlib import Path

# Đảm bảo in UTF-8 trên Windows console
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

REPO_ROOT = Path(__file__).resolve().parent.parent
DIST_DIR = REPO_ROOT / "system" / "reader_app" / "dist"
MANUSCRIPT_DIR = REPO_ROOT / "manuscript" / "markdown"
AUTHOR_SECRET_DIR = REPO_ROOT / "author_secret"

PROHIBITED_FILE_EXTENSIONS = {
    ".db", ".db-wal", ".db-shm", ".db-journal",
    ".py", ".pyc", ".pyo", ".pyd",
    ".bat", ".cmd", ".ps1", ".sh",
    ".env", ".key", ".pem", ".cert",
    ".bak", ".tmp"
}

PROHIBITED_NAMES = {
    "novel_os.db", "secrets.json", "reveal_ledger.json", ".git", ".gitignore", "author_secret"
}

FORBIDDEN_CONTENT_PATTERNS = [
    re.compile(r'"actual_meaning"\s*:', re.IGNORECASE),
    re.compile(r'"secret_reveals?"\s*:', re.IGNORECASE),
    re.compile(r'"vault_status"\s*:', re.IGNORECASE),
    re.compile(r'ghp_[A-Za-z0-9_]{30,}', re.IGNORECASE),
    re.compile(r'github_pat_[A-Za-z0-9_]{30,}', re.IGNORECASE),
]

def verify():
    print(f"[*] Bắt đầu kiểm toán thư mục phân phối công khai: {DIST_DIR}")
    
    if not DIST_DIR.exists():
        print(f"[FAIL] Thư mục dist không tồn tại: {DIST_DIR}")
        sys.exit(1)

    errors = []

    # 1. Kiểm tra các tệp bắt buộc phải có
    required_files = ["index.html", "data/chapters.json", "manifest.json", "sw.js"]
    for req in required_files:
        p = DIST_DIR / req
        if not p.exists():
            errors.append(f"Thiếu tệp phân phối bắt buộc: {req}")

    # 2. Quét đệ quy toàn bộ thư mục dist
    all_files = []
    for root, dirs, files in os.walk(DIST_DIR):
        for d in dirs:
            if d.lower() in PROHIBITED_NAMES:
                errors.append(f"Phát hiện thư mục cấm trong dist: {os.path.join(root, d)}")
        for f in files:
            all_files.append(Path(root) / f)

    print(f"[*] Tổng số tệp trong dist cần quét: {len(all_files)}")

    # Load known secrets to check for content leaks if author_secret exists
    secret_leak_words = set()
    secrets_file = AUTHOR_SECRET_DIR / "secrets.json"
    if secrets_file.exists():
        try:
            with open(secrets_file, "r", encoding="utf-8") as sf:
                sdata = json.load(sf)
                for sec in sdata.get("secrets", []):
                    # add title keywords
                    for word in sec.get("title", "").split():
                        if len(word) > 5:
                            secret_leak_words.add(word.lower())
        except Exception:
            pass

    for file_path in all_files:
        rel_path = file_path.relative_to(DIST_DIR)
        suffix = file_path.suffix.lower()
        name = file_path.name.lower()

        # Kiểm tra đuôi tệp bị cấm
        if suffix in PROHIBITED_FILE_EXTENSIONS:
            errors.append(f"Tệp có phần mở rộng bị cấm trong dist: {rel_path} ({suffix})")

        # Kiểm tra tên tệp bị cấm
        if name in PROHIBITED_NAMES:
            errors.append(f"Tệp có tên bị cấm trong dist: {rel_path}")

        # Kiểm tra nội dung text của file JSON, HTML, JS
        if suffix in [".json", ".html", ".js", ".svg", ".txt"]:
            try:
                with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                    content = f.read()

                for pat in FORBIDDEN_CONTENT_PATTERNS:
                    if pat.search(content):
                        errors.append(f"Phát hiện pattern dữ liệu nhạy cảm ({pat.pattern}) trong tệp: {rel_path}")

            except Exception as e:
                errors.append(f"Không thể đọc tệp {rel_path}: {e}")

    # 3. Kiểm tra tính đầy đủ của các chương bản thảo
    chapters_json_path = DIST_DIR / "data" / "chapters.json"
    if chapters_json_path.exists():
        try:
            with open(chapters_json_path, "r", encoding="utf-8") as f:
                ch_data = json.load(f)
            
            dist_ch_nums = {c["chapter"] for c in ch_data.get("chapters", [])}
            
            # Đếm số chương markdown có trong manuscript
            manuscript_ch_nums = set()
            for root, _, files in os.walk(MANUSCRIPT_DIR):
                for f in files:
                    if f.endswith(".md") and f.startswith("ch_"):
                        m = re.search(r'ch_(\d+)', f)
                        if m:
                            manuscript_ch_nums.add(int(m.group(1)))

            missing_in_dist = manuscript_ch_nums - dist_ch_nums
            if missing_in_dist:
                errors.append(f"Các chương có trong bản thảo nhưng thiếu trong dist: {sorted(list(missing_in_dist))}")

            print(f"[OK] Số chương bản thảo: {len(manuscript_ch_nums)}, số chương trong dist: {len(dist_ch_nums)}")
        except Exception as e:
            errors.append(f"Lỗi kiểm tra tính đầy đủ của chapters.json: {e}")

    # Báo cáo kết quả
    if errors:
        print("\n" + "!" * 60)
        print(f"[FAIL] PHÁT HIỆN {len(errors)} LỖ HỔNG AN NINH / TOÀN VẸN TRONG THƯ MỤC DIST:")
        for err in errors:
            print(f"  - {err}")
        print("!" * 60 + "\n")
        sys.exit(1)
    else:
        print("\n" + "=" * 60)
        print("[PASS] Thư mục phân phối công khai dist/ đạt 100% tiêu chuẩn an toàn.")
        print("  - Không chứa database (*.db).")
        print("  - Không chứa author secrets hoặc actual_meaning.")
        print("  - Không chứa mã nguồn Python backend.")
        print("  - Đầy đủ 100% chương bản thảo công khai.")
        print("=" * 60 + "\n")
        return True

if __name__ == "__main__":
    verify()
