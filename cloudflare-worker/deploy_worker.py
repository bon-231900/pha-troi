# -*- coding: utf-8 -*-
"""
Script 1-Click Tự động Triển khai Cloudflare Worker API cho Webgame "Phá Trời" (phatroi.com)
Chạy lệnh: py cloudflare-worker/deploy_worker.py
"""
import subprocess
import sys
import os

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

WORKER_DIR = os.path.dirname(os.path.abspath(__file__))

def run_cmd(cmd, cwd=WORKER_DIR):
    print(f"\n[EXEC] {cmd}...")
    res = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if res.stdout:
        print(res.stdout)
    if res.stderr and res.returncode != 0:
        print("[STDERR]", res.stderr)
    return res.returncode == 0

def main():
    print("=" * 65)
    print("   TRIỂN KHAI CLOUDFLARE WORKER API (PHATROI.COM)")
    print("=" * 65)

    print("\n[1/3] Kiểm tra công cụ Cloudflare Wrangler...")
    has_wrangler = run_cmd("npx wrangler --version")
    if not has_wrangler:
        print("[!] Đang cài đặt Wrangler...")
        run_cmd("npm install")

    print("\n[2/3] Triển khai Cloudflare Worker lên mạng toàn cầu...")
    success = run_cmd("npx wrangler deploy")

    if success:
        print("\n" + "=" * 65)
        print("  🎉 XUẤT BẢN CLOUDFLARE WORKER API THÀNH CÔNG RỰC RỠ!")
        print("=" * 65)
        print("Các endpoint hoạt động ngay:")
        print("  - GET  https://phatroi.com/api/boss")
        print("  - POST https://phatroi.com/api/boss/strike")
        print("  - GET  https://phatroi.com/api/leaderboard")
        print("=" * 65)
    else:
        print("\n[!] Nếu Cloudflare yêu cầu đăng nhập lần đầu, vui lòng chạy lệnh:")
        print("    cd cloudflare-worker && npx wrangler login")
        print("    sau đó chạy lại: py deploy_worker.py")

if __name__ == "__main__":
    main()
