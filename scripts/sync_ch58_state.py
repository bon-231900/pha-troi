# -*- coding: utf-8 -*-
"""Sync Chapter 58 state and build static reader app."""

import sqlite3
import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from system.core.config import DB_PATH

def sync_ch58():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # 1. Timeline event
    cur.execute("""
    INSERT OR REPLACE INTO timeline_events 
    (id, title, chapter_num, scene_num, absolute_time, relative_order, location_id, participants_json, summary, outcome)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        "EVT-CH058",
        "Ngăn chặn phá hủy cọc Trấn Thủy Lò Gốm",
        58,
        1,
        "2026-10-18T19:30:00+07:00",
        58,
        "loc_rach_lo_gom",
        json.dumps(["char_minh_an"]),
        "Minh An đột nhập xưởng Vạn Phát, dùng kình lực Thể Đạo Thiết Lương Thập Phách kết hợp Trấn Thủy Đoản Đao thuần hóa âm sát của cọc tiêu Lò Gốm.",
        "Phát hiện Thầy Cảnh và Cửu Long Group đứng sau chiến dịch thu gom Thủy Môn Thập Nhị Tiêu để phá vỡ phong ấn cướp đoạt long mạch."
    ))

    # 2. Touch active thread
    cur.execute("""
    UPDATE story_threads 
    SET last_touched_chapter = 58, 
        current_state = 'Minh An khống chế xưởng Vạn Phát, phát hiện Cửu Long Group thu gom Thủy Môn Tiêu',
        updated_at = datetime('now')
    WHERE thread_id = 'TH-001'
    """)

    conn.commit()
    conn.close()
    print("[+] DB synced for Chapter 58.")

    # 3. Update inventory.json
    inv_path = os.path.join(BASE_DIR, "state", "inventory.json")
    if os.path.exists(inv_path):
        with open(inv_path, "r", encoding="utf-8") as f:
            inv_data = json.load(f)
        inv_data["last_updated"] = "2026-10-18T20:00:00+07:00"
        for item in inv_data.get("core_weapons_and_artifacts", []):
            if "Trấn Thủy" in item.get("name", ""):
                item["condition"] = "Lộ đường chỉ hoàng kim đồng thau sau khi được kình lực Luyện Cốt thuần phục"
                item["function"] = "Bảo vật trấn thủy, có thể phong tỏa và điều khiển âm sát thủy khí của Thủy Môn Thập Nhị Tiêu"
        with open(inv_path, "w", encoding="utf-8") as f:
            json.dump(inv_data, f, ensure_ascii=False, indent=2)
        print("[+] inventory.json updated.")

if __name__ == "__main__":
    sync_ch58()
