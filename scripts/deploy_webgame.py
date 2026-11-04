# -*- coding: utf-8 -*-
"""
Script tự động đẩy Webgame "Toàn Dân Phá Trời: The Celestial Forge" lên GitHub Pages (phatroi.com)
Chạy lệnh: py scripts/deploy_webgame.py
"""
import os
import subprocess
import sys
import json

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE_DIR = r"d:\tieu-thuyet"
GAME_DIR = os.path.join(BASE_DIR, "webgame")

def get_github_token():
    token = os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token:
        return token

    mcp_config = os.path.expanduser(r"~\.gemini\config\mcp_config.json")
    if os.path.exists(mcp_config):
        try:
            with open(mcp_config, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("mcpServers", {}).get("github-mcp-server", {}).get("env", {}).get("GITHUB_PERSONAL_ACCESS_TOKEN", "")
        except Exception:
            pass
    return ""

def deploy():
    token = get_github_token()
    if not token:
        print("[Lỗi] Không tìm thấy GitHub Token.")
        return False

    repo_remote = f"https://bon-231900:{token}@github.com/bon-231900/pha-troi.git"

    print("[1/2] Đang dọn dẹp và chuẩn bị đóng gói Webgame...")
    git_dir = os.path.join(GAME_DIR, ".git")
    if os.path.exists(git_dir):
        subprocess.run(f'rd /s /q "{git_dir}"', shell=True)

    # Cache buster trên index.html để Cloudflare không cache nhầm 404
    index_html = os.path.join(GAME_DIR, "index.html")
    if os.path.exists(index_html):
        with open(index_html, "r", encoding="utf-8") as f:
            content = f.read()
        import time, re
        ts = int(time.time())
        content = re.sub(r'(\./assets/[^"?]+\.(?:js|css))(?:\?v=\d+)?', rf'\1?v={ts}', content)
        with open(index_html, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"    -> Đã đánh dấu Cache Buster: ?v={ts} vào index.html")

    print("[2/2] Đang đẩy lên nhánh gh-pages của GitHub (phatroi.com)...")
    commands = [
        "git init",
        'git config user.name "Skybreaker Studio"',
        'git config user.email "admin@phatroi.com"',
        f"git remote add origin {repo_remote}",
        "git checkout -B gh-pages",
        "git add -A",
        'git commit -m "feat(mobile): AAA Mobile UI/UX for iOS & Android - Safe Area, Adaptive Canvas, Thumb Dock, Haptics & PWA"',
        "git push -u origin gh-pages --force"
    ]
    full_cmd = " && ".join(commands)
    res = subprocess.run(full_cmd, shell=True, cwd=GAME_DIR, capture_output=True, text=True, encoding='utf-8', errors='replace')

    # Dọn dẹp .git trong webgame
    if os.path.exists(git_dir):
        subprocess.run(f'rd /s /q "{git_dir}"', shell=True)

    print("STDOUT:", res.stdout)
    if res.returncode == 0:
        print("\n" + "="*60)
        print("  XUẤT BẢN GIAO DIỆN MỞ ĐẦU THƯ PHÁP CỔ PHONG LÊN PHATROI.COM THÀNH CÔNG RỰC RỠ!")
        print("="*60)
        print("-> Truy cập ngay:")
        print("   https://phatroi.com/")
        print("   https://bon-231900.github.io/pha-troi/\n")
        print("="*60)
        return True
    else:
        print("[Lỗi deploy]:", res.stderr)
        return False

if __name__ == "__main__":
    deploy()
