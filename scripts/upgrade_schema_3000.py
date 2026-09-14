# -*- coding: utf-8 -*-
"""Script nâng cấp schema database novel_os.db cho quy mô 3.000+ chương."""

import sqlite3
import json
import os
import sys
from datetime import datetime

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

DB_PATH = r"d:\tieu-thuyet\database\novel_os.db"

def upgrade_schema():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    print("[1/5] Đang tạo bảng story_hierarchy...")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS story_hierarchy (
        id TEXT PRIMARY KEY,
        level TEXT NOT NULL, -- 'saga', 'era', 'volume', 'arc', 'mini_arc', 'chapter', 'scene', 'beat'
        parent_id TEXT,
        order_index INTEGER NOT NULL,
        title TEXT NOT NULL,
        summary TEXT,
        objective TEXT,
        stakes TEXT,
        pov TEXT,
        word_count INTEGER DEFAULT 0,
        status TEXT DEFAULT 'PLANNED', -- 'PLANNED', 'IN_PROGRESS', 'DRAFTED', 'REVISED', 'LOCKED', 'COMPLETED'
        metadata_json TEXT,
        created_at TEXT,
        updated_at TEXT,
        FOREIGN KEY (parent_id) REFERENCES story_hierarchy(id)
    )
    """)

    cur.execute("CREATE INDEX IF NOT EXISTS idx_hierarchy_parent ON story_hierarchy(parent_id, order_index)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_hierarchy_level ON story_hierarchy(level, status)")

    print("[2/5] Đang tạo bảng story_threads...")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS story_threads (
        thread_id TEXT PRIMARY KEY,
        thread_type TEXT NOT NULL, -- 'MAIN_PLOT', 'SUBPLOT', 'CHARACTER_ARC', 'MYSTERY', 'RELATIONSHIP', 'WORLDBUILDING', 'FACTION'
        title TEXT NOT NULL,
        description TEXT,
        origin_chapter INTEGER NOT NULL,
        target_resolution_chapter INTEGER,
        status TEXT NOT NULL DEFAULT 'ACTIVE', -- 'OPEN', 'ACTIVE', 'DORMANT', 'RESOLVING', 'RESOLVED', 'ABANDONED'
        current_state TEXT,
        known_info TEXT, -- Thông tin nhân vật đã biết
        hidden_info TEXT, -- Bí mật của tác giả
        reader_knowledge TEXT, -- Những gì độc giả đã biết
        last_touched_chapter INTEGER DEFAULT 0,
        revisit_window_chapters INTEGER DEFAULT 15,
        urgency TEXT DEFAULT 'MEDIUM', -- 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL'
        importance TEXT DEFAULT 'MAJOR', -- 'CORE', 'MAJOR', 'MINOR', 'BACKGROUND'
        created_at TEXT,
        updated_at TEXT
    )
    """)

    cur.execute("CREATE INDEX IF NOT EXISTS idx_threads_status ON story_threads(status, urgency)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_threads_type ON story_threads(thread_type)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_threads_last_touched ON story_threads(last_touched_chapter)")

    print("[3/5] Đang tạo bảng escalation_budgets...")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS escalation_budgets (
        budget_id TEXT PRIMARY KEY,
        scope_type TEXT NOT NULL, -- 'SAGA', 'VOLUME', 'ARC'
        scope_id TEXT NOT NULL,
        axis TEXT NOT NULL, -- 'POWER_CEILING', 'GEOGRAPHY_SCALE', 'COSMOLOGY_DEPTH', 'STAKES_LEVEL', 'MYSTERY_REVEAL', 'EMOTIONAL_INTIMACY'
        current_level REAL NOT NULL DEFAULT 0.0,
        allowed_ceiling REAL NOT NULL DEFAULT 1.0,
        cooldown_chapters INTEGER DEFAULT 5,
        last_escalated_chapter INTEGER DEFAULT 0,
        description TEXT,
        status TEXT DEFAULT 'ACTIVE',
        created_at TEXT,
        updated_at TEXT
    )
    """)

    cur.execute("CREATE INDEX IF NOT EXISTS idx_escalation_scope ON escalation_budgets(scope_id, axis)")

    print("[4/5] Đang tạo bảng mystery_depth...")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS mystery_depth (
        mystery_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        surface_explanation TEXT,
        intermediate_explanation TEXT,
        deep_explanation TEXT,
        ultimate_truth TEXT,
        false_theories TEXT,
        reveal_schedule TEXT, -- JSON mapping scope/chapter to allowed layer
        current_revealed_layer INTEGER DEFAULT 1,
        status TEXT DEFAULT 'UNRESOLVED',
        created_at TEXT,
        updated_at TEXT
    )
    """)

    print("[5/5] Đang tạo bảng thread_fatigue_logs...")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS thread_fatigue_logs (
        log_id TEXT PRIMARY KEY,
        chapter_num INTEGER NOT NULL,
        pattern_type TEXT NOT NULL, -- 'ENDING_CLIFFHANGER_REPETITION', 'ANOMALY_CYCLE', 'EXPOSITION_DUMP', 'CULTIVATION_BREAKTHROUGH_LOOP', 'ROMANCE_STAGNATION', 'VOCABULARY_REPETITION'
        pattern_signature TEXT,
        occurrences_window INTEGER DEFAULT 1,
        severity TEXT DEFAULT 'INFO', -- 'INFO', 'WARNING', 'CRITICAL'
        details TEXT,
        detected_at TEXT
    )
    """)

    cur.execute("CREATE INDEX IF NOT EXISTS idx_fatigue_chapter ON thread_fatigue_logs(chapter_num)")

    conn.commit()
    print("[+] Toàn bộ 5 bảng mới và các index đã được thiết lập thành công!")
    conn.close()

if __name__ == "__main__":
    upgrade_schema()
