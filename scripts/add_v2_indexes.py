# -*- coding: utf-8 -*-
"""Script to add performance indexes to novel_os.db for 3,000+ chapter scaling."""

import sqlite3
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from system.core.config import DB_PATH

def add_indexes(db_path: str = DB_PATH):
    if not os.path.exists(db_path):
        print(f"[-] Database not found at {db_path}")
        return False

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    indexes = [
        ("idx_char_states_cid_ch", "CREATE INDEX IF NOT EXISTS idx_char_states_cid_ch ON character_states(character_id, chapter_num DESC)"),
        ("idx_knowledge_cid_key_ch", "CREATE INDEX IF NOT EXISTS idx_knowledge_cid_key_ch ON knowledge_matrix(character_id, fact_key, chapter_num DESC)"),
        ("idx_timeline_ch_scene", "CREATE INDEX IF NOT EXISTS idx_timeline_ch_scene ON timeline_events(chapter_num, scene_num)"),
        ("idx_timeline_abs_time", "CREATE INDEX IF NOT EXISTS idx_timeline_abs_time ON timeline_events(absolute_time)"),
        ("idx_foreshadow_status_planted", "CREATE INDEX IF NOT EXISTS idx_foreshadow_status_planted ON foreshadowing_ledger(status, planted_chapter)"),
        ("idx_story_threads_status_urg", "CREATE INDEX IF NOT EXISTS idx_story_threads_status_urg ON story_threads(status, urgency)"),
        ("idx_canon_entries_cat_level", "CREATE INDEX IF NOT EXISTS idx_canon_entries_cat_level ON canon_entries(category, level)"),
        ("idx_canon_entries_cat_key", "CREATE INDEX IF NOT EXISTS idx_canon_entries_cat_key ON canon_entries(category, key)"),
        ("idx_continuity_errors_ch_status", "CREATE INDEX IF NOT EXISTS idx_continuity_errors_ch_status ON continuity_errors(chapter_num, status)"),
        ("idx_proposals_status_created", "CREATE INDEX IF NOT EXISTS idx_proposals_status_created ON proposals(status, created_at)"),
    ]

    print(f"[*] Applying {len(indexes)} indexes on {db_path}...")
    for name, sql in indexes:
        try:
            cur.execute(sql)
            print(f"  [+] Index {name} created / verified.")
        except sqlite3.OperationalError as e:
            print(f"  [!] Notice for {name}: {e}")

    conn.commit()
    conn.close()
    print("[+] All v2 performance indexes verified successfully.")
    return True

if __name__ == "__main__":
    add_indexes()
