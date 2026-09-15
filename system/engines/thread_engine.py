# -*- coding: utf-8 -*-
"""Động cơ Quản Lý Tuyến Truyện (Story Thread Engine) cho Novel OS 3.000+ chương.
Theo dõi vòng đời độc lập của các mạch truyện: MAIN_PLOT, SUBPLOT, CHARACTER_ARC, MYSTERY, RELATIONSHIP, WORLDBUILDING.
Cảnh báo tuyến ngủ quên (dormant threads) và đề xuất tuyến cần giải quyết cho từng chương.
"""

import sqlite3
import json
from datetime import datetime
from system.core.config import DB_PATH

class StoryThreadEngine:
    VALID_TYPES = ["MAIN_PLOT", "SUBPLOT", "CHARACTER_ARC", "MYSTERY", "RELATIONSHIP", "WORLDBUILDING", "FACTION"]
    VALID_STATUSES = ["OPEN", "ACTIVE", "DORMANT", "RESOLVING", "RESOLVED", "ABANDONED"]
    VALID_URGENCIES = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    VALID_IMPORTANCES = ["CORE", "MAJOR", "MINOR", "BACKGROUND"]

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path

    def create_thread(self, thread_id: str, thread_type: str, title: str, description: str,
                      origin_chapter: int, target_resolution_chapter: int = None,
                      status: str = "ACTIVE", current_state: str = "",
                      known_info: str = "", hidden_info: str = "", reader_knowledge: str = "",
                      revisit_window_chapters: int = 15, urgency: str = "MEDIUM",
                      importance: str = "MAJOR") -> dict:
        if thread_type not in self.VALID_TYPES:
            raise ValueError(f"Loại tuyến truyện không hợp lệ: {thread_type}")
        if status not in self.VALID_STATUSES:
            raise ValueError(f"Trạng thái không hợp lệ: {status}")

        now_iso = datetime.now().isoformat()
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cur = conn.cursor()
        cur.execute("""
        INSERT OR REPLACE INTO story_threads (
            thread_id, thread_type, title, description, origin_chapter, target_resolution_chapter,
            status, current_state, known_info, hidden_info, reader_knowledge,
            last_touched_chapter, revisit_window_chapters, urgency, importance, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (thread_id, thread_type, title, description, origin_chapter, target_resolution_chapter,
              status, current_state, known_info, hidden_info, reader_knowledge,
              origin_chapter, revisit_window_chapters, urgency, importance, now_iso, now_iso))
        conn.commit()
        conn.close()
        return self.get_thread(thread_id)

    def get_thread(self, thread_id: str) -> dict:
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cur = conn.cursor()
        cur.execute("""
        SELECT thread_id, thread_type, title, description, origin_chapter, target_resolution_chapter,
               status, current_state, known_info, hidden_info, reader_knowledge,
               last_touched_chapter, revisit_window_chapters, urgency, importance, created_at, updated_at
        FROM story_threads WHERE thread_id = ?
        """, (thread_id,))
        row = cur.fetchone()
        conn.close()
        if not row:
            return None
        return {
            "thread_id": row[0], "thread_type": row[1], "title": row[2], "description": row[3],
            "origin_chapter": row[4], "target_resolution_chapter": row[5], "status": row[6],
            "current_state": row[7], "known_info": row[8], "hidden_info": row[9],
            "reader_knowledge": row[10], "last_touched_chapter": row[11],
            "revisit_window_chapters": row[12], "urgency": row[13], "importance": row[14],
            "created_at": row[15], "updated_at": row[16]
        }

    def update_thread(self, thread_id: str, **kwargs) -> dict:
        now_iso = datetime.now().isoformat()
        fields = []
        values = []
        for k, v in kwargs.items():
            fields.append(f"{k} = ?")
            values.append(v)
        fields.append("updated_at = ?")
        values.append(now_iso)
        values.append(thread_id)

        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cur = conn.cursor()
        cur.execute(f"UPDATE story_threads SET {', '.join(fields)} WHERE thread_id = ?", values)
        conn.commit()
        conn.close()
        return self.get_thread(thread_id)

    def touch_thread(self, thread_id: str, chapter_num: int, new_state: str = None) -> dict:
        """Cập nhật tiến trình của tuyến truyện tại một chương cụ thể."""
        kwargs = {"last_touched_chapter": chapter_num}
        if new_state:
            kwargs["current_state"] = new_state
        return self.update_thread(thread_id, **kwargs)

    def resolve_thread(self, thread_id: str, chapter_num: int, resolution_summary: str = "") -> dict:
        return self.update_thread(
            thread_id,
            status="RESOLVED",
            last_touched_chapter=chapter_num,
            current_state=f"[RESOLVED tại Ch {chapter_num}] {resolution_summary}"
        )

    def list_threads(self, status: str = None, thread_type: str = None) -> list:
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cur = conn.cursor()
        query = "SELECT thread_id, thread_type, title, status, last_touched_chapter, revisit_window_chapters, urgency, importance FROM story_threads WHERE 1=1"
        params = []
        if status:
            query += " AND status = ?"
            params.append(status)
        if thread_type:
            query += " AND thread_type = ?"
            params.append(thread_type)
        query += """ ORDER BY 
            (CASE urgency WHEN 'CRITICAL' THEN 4 WHEN 'HIGH' THEN 3 WHEN 'MEDIUM' THEN 2 ELSE 1 END) DESC,
            (CASE importance WHEN 'CORE' THEN 4 WHEN 'MAJOR' THEN 3 WHEN 'MINOR' THEN 2 ELSE 1 END) DESC,
            last_touched_chapter ASC"""
        cur.execute(query, params)
        rows = cur.fetchall()
        conn.close()
        return [{
            "thread_id": r[0], "thread_type": r[1], "title": r[2], "status": r[3],
            "last_touched_chapter": r[4], "revisit_window_chapters": r[5],
            "urgency": r[6], "importance": r[7]
        } for r in rows]

    def audit_dormant_threads(self, current_chapter: int) -> list:
        """Phát hiện các tuyến truyện đang ACTIVE hoặc OPEN nhưng đã quá hạn revisit_window_chapters mà chưa được đụng tới."""
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cur = conn.cursor()
        cur.execute("""
        SELECT thread_id, thread_type, title, last_touched_chapter, revisit_window_chapters, urgency, importance
        FROM story_threads
        WHERE status IN ('ACTIVE', 'OPEN', 'RESOLVING')
        """)
        rows = cur.fetchall()
        conn.close()

        dormant = []
        for r in rows:
            tid, ttype, title, last_ch, window, urg, imp = r
            gap = current_chapter - last_ch
            if gap > window:
                dormant.append({
                    "thread_id": tid,
                    "thread_type": ttype,
                    "title": title,
                    "last_touched_chapter": last_ch,
                    "gap_chapters": gap,
                    "allowed_window": window,
                    "urgency": urg,
                    "importance": imp,
                    "alert": f"Tuyến '{title}' [{tid}] bị bỏ quên {gap} chương (ngưỡng tối đa: {window} chương)!"
                })
        return sorted(dormant, key=lambda x: x["gap_chapters"], reverse=True)

    def get_threads_for_chapter_context(self, chapter_num: int, limit: int = 4) -> list:
        """Trích xuất danh sách tuyến truyện ưu tiên cần xuất hiện/phát triển trong gói ngữ cảnh của chương."""
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cur = conn.cursor()
        cur.execute("""
        SELECT thread_id, thread_type, title, current_state, known_info, reader_knowledge, last_touched_chapter, revisit_window_chapters
        FROM story_threads
        WHERE status IN ('ACTIVE', 'OPEN', 'RESOLVING')
        ORDER BY (CASE urgency WHEN 'CRITICAL' THEN 1 WHEN 'HIGH' THEN 2 WHEN 'MEDIUM' THEN 3 ELSE 4 END) ASC,
                 (?-last_touched_chapter) DESC
        LIMIT ?
        """, (chapter_num, limit))
        rows = cur.fetchall()
        conn.close()
        return [{
            "thread_id": r[0],
            "type": r[1],
            "title": r[2],
            "state": r[3],
            "known": r[4],
            "reader_view": r[5],
            "gap": chapter_num - r[6],
            "needs_touch": (chapter_num - r[6]) >= r[7]
        } for r in rows]
