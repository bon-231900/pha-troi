# -*- coding: utf-8 -*-
"""
NovelOS — Script tự động đồng bộ bản thảo lên GitHub Pages
Chạy lệnh: python scripts/sync_to_github.py
"""
import os
import subprocess
import sys
import json

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE_DIR = r"d:\tieu-thuyet"
BUILD_SCRIPT = os.path.join(BASE_DIR, "system", "reader_app", "generate_static_site.py")
DIST_DIR = os.path.join(BASE_DIR, "system", "reader_app", "dist")

def get_github_token():
    # 1. Environment variable
    token = os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token:
        return token

    # 2. Local Gemini MCP configuration
    mcp_config = os.path.expanduser(r"~\.gemini\config\mcp_config.json")
    if os.path.exists(mcp_config):
        try:
            with open(mcp_config, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("mcpServers", {}).get("github-mcp-server", {}).get("env", {}).get("GITHUB_PERSONAL_ACCESS_TOKEN", "")
        except Exception:
            pass
    return ""

def sync():
    token = get_github_token()
    if not token:
        print("[Lỗi] Không tìm thấy GitHub Access Token. Vui lòng thiết lập biến môi trường GITHUB_TOKEN.")
        return

    repo_remote = f"https://bon-231900:{token}@github.com/bon-231900/pha-troi.git"

    print("[1/3] Đang biên dịch bản thảo thành Web App tĩnh...")
    res = subprocess.run([sys.executable, BUILD_SCRIPT], cwd=BASE_DIR, capture_output=True, text=True, encoding="utf-8")
    print(res.stdout)
    if res.returncode != 0:
        print("[Lỗi biên dịch]", res.stderr)
        return

    print("[2/3] Đang đóng gói và đẩy dữ liệu lên nhánh gh-pages của GitHub...")
    commands = [
        "git init",
        'git config user.name "NovelOS Architect"',
        'git config user.email "novelos@pha-troi.local"',
        f"git remote add origin {repo_remote}",
        "git checkout -B gh-pages",
        "git add -A",
        'git commit -m "[NovelOS] Cap nhat chuong moi va dong bo Web Reader App"',
        "git push -u origin gh-pages --force"
    ]
    full_cmd = " && ".join(commands)
    push_res = subprocess.run(full_cmd, shell=True, cwd=DIST_DIR, capture_output=True, text=True)
    
    # Dọn dẹp .git trong dist
    git_folder = os.path.join(DIST_DIR, ".git")
    if os.path.exists(git_folder):
        subprocess.run(f'rd /s /q "{git_folder}"', shell=True)

    if push_res.returncode == 0:
        print("\n" + "="*60)
        print("  ĐỒNG BỘ LÊN GITHUB PAGES THÀNH CÔNG RỰC RỠ!")
        print("="*60)
        print("-> Đọc online 24/7 (Tắt laptop vẫn đọc tốt):")
        print("   https://phatroi.com/ (Tên miền chính)")
        print("   https://bon-231900.github.io/pha-troi/ (Tự động chuyển hướng)\n")
        print("="*60)
    else:
        print("[Lỗi Push]", push_res.stderr)

if __name__ == "__main__":
    sync()
