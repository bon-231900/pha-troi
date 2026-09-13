# -*- coding: utf-8 -*-
import sqlite3
import json
from datetime import datetime
from system.core.config import DB_PATH

class TimelineEngine:
    START_DATE_STR = "2026-09-13T00:00:00+07:00"

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path

    def add_event(self, event_id: str, title: str, chapter_num: int, scene_num: int, absolute_time: str, location_id: str, participants: list, summary: str, outcome: str):
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cur = conn.cursor()
        cur.execute("""INSERT OR REPLACE INTO timeline_events (id, title, chapter_num, scene_num, absolute_time, location_id, participants_json, summary, outcome)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (event_id, title, chapter_num, scene_num, absolute_time, location_id, json.dumps(participants, ensure_ascii=False), summary, outcome))
        conn.commit()
        conn.close()

    def get_events(self, limit: int = 50) -> list:
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cur = conn.cursor()
        cur.execute("SELECT id, title, chapter_num, scene_num, absolute_time, location_id, participants_json, summary, outcome FROM timeline_events ORDER BY chapter_num, scene_num LIMIT ?", (limit,))
        rows = cur.fetchall()
        conn.close()
        return [{
            "id": r[0], "title": r[1], "chapter_num": r[2], "scene_num": r[3],
            "absolute_time": r[4], "location_id": r[5],
            "participants": json.loads(r[6]) if r[6] else [],
            "summary": r[7], "outcome": r[8]
        } for r in rows]

    def validate_chronology(self, chapter_num: int, event_time_str: str) -> tuple[bool, str]:
        """Kiểm tra thời gian không bị đảo lộn vô lý so với các chương trước hoặc mốc khởi đầu."""
        if not event_time_str:
            return True, "Hợp lệ."
        
        try:
            curr_dt = datetime.fromisoformat(event_time_str)
            start_dt = datetime.fromisoformat(self.START_DATE_STR)
            if curr_dt < start_dt:
                return False, f"TIMELINE_ERROR: Thời gian ({event_time_str}) trước ngày bắt đầu tác phẩm (2026-09-13) mà không gắn tag Flashback!"

            conn = sqlite3.connect(self.db_path, timeout=30.0)
            cur = conn.cursor()
            cur.execute("""SELECT chapter_num, absolute_time FROM timeline_events 
                           WHERE absolute_time IS NOT NULL AND chapter_num <= ?
                           ORDER BY chapter_num DESC, id DESC LIMIT 1""", (chapter_num,))
            prev = cur.fetchone()
            conn.close()

            if prev and prev[1]:
                prev_dt = datetime.fromisoformat(prev[1])
                if curr_dt < prev_dt and chapter_num >= prev[0]:
                    return False, f"TIMELINE_ERROR: Thời gian ({event_time_str}) sớm hơn sự kiện trước ({prev[1]}) mà không có thẻ Flashback!"
        except Exception:
            pass
        return True, "Hợp lệ."
