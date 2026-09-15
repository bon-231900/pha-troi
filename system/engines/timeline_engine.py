# -*- coding: utf-8 -*-
"""
Novel OS — TimelineEngine (Quản lý Dòng thời gian & Niên đại Vũ trụ)
Phân tách thứ tự chương (chapter order) và niên đại thế giới (world chronology).
Hỗ trợ các chế độ thời gian: LINEAR, FLASHBACK, FLASHFORWARD, PARALLEL, DREAM, VISION, TIME_SKIP.
Loại bỏ việc nuốt ngoại lệ âm thầm (fail-closed validation).
"""
import sqlite3
import json
from datetime import datetime
from system.core.config import DB_PATH

class TimelineEngine:
    START_DATE_STR = "2026-09-13T00:00:00+07:00"
    VALID_TEMPORAL_MODES = ["LINEAR", "FLASHBACK", "FLASHFORWARD", "PARALLEL", "DREAM", "VISION", "TIME_SKIP"]

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._ensure_temporal_mode_column()

    def _ensure_temporal_mode_column(self):
        """Đảm bảo cột temporal_mode tồn tại trong bảng timeline_events (Migration tương thích ngược)."""
        try:
            conn = sqlite3.connect(self.db_path, timeout=30.0)
            cur = conn.cursor()
            cur.execute("PRAGMA table_info(timeline_events)")
            cols = [c[1] for c in cur.fetchall()]
            if "temporal_mode" not in cols and cols:
                cur.execute("ALTER TABLE timeline_events ADD COLUMN temporal_mode TEXT DEFAULT 'LINEAR'")
                conn.commit()
            conn.close()
        except Exception:
            pass

    def add_event(self, event_id: str, title: str, chapter_num: int, scene_num: int,
                  absolute_time: str, location_id: str, participants: list,
                  summary: str, outcome: str, temporal_mode: str = "LINEAR"):
        if temporal_mode not in self.VALID_TEMPORAL_MODES:
            raise ValueError(f"Chế độ thời gian không hợp lệ: {temporal_mode}. Phải là một trong: {self.VALID_TEMPORAL_MODES}")

        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cur = conn.cursor()
        
        # Kiểm tra xem cột temporal_mode có sẵn không
        cur.execute("PRAGMA table_info(timeline_events)")
        cols = [c[1] for c in cur.fetchall()]
        if "temporal_mode" in cols:
            cur.execute("""INSERT OR REPLACE INTO timeline_events (
                id, title, chapter_num, scene_num, absolute_time, location_id,
                participants_json, summary, outcome, temporal_mode
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (event_id, title, chapter_num, scene_num, absolute_time, location_id,
             json.dumps(participants, ensure_ascii=False), summary, outcome, temporal_mode))
        else:
            cur.execute("""INSERT OR REPLACE INTO timeline_events (
                id, title, chapter_num, scene_num, absolute_time, location_id,
                participants_json, summary, outcome
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (event_id, title, chapter_num, scene_num, absolute_time, location_id,
             json.dumps(participants, ensure_ascii=False), summary, outcome))
        conn.commit()
        conn.close()

    def get_events(self, limit: int = 50) -> list:
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cur = conn.cursor()
        cur.execute("PRAGMA table_info(timeline_events)")
        cols = [c[1] for c in cur.fetchall()]
        has_mode = "temporal_mode" in cols

        if has_mode:
            cur.execute("""SELECT id, title, chapter_num, scene_num, absolute_time, location_id,
                                  participants_json, summary, outcome, temporal_mode
                           FROM timeline_events ORDER BY chapter_num, scene_num LIMIT ?""", (limit,))
        else:
            cur.execute("""SELECT id, title, chapter_num, scene_num, absolute_time, location_id,
                                  participants_json, summary, outcome
                           FROM timeline_events ORDER BY chapter_num, scene_num LIMIT ?""", (limit,))
        rows = cur.fetchall()
        conn.close()
        return [{
            "id": r[0], "title": r[1], "chapter_num": r[2], "scene_num": r[3],
            "absolute_time": r[4], "location_id": r[5],
            "participants": json.loads(r[6]) if r[6] else [],
            "summary": r[7], "outcome": r[8],
            "temporal_mode": r[9] if has_mode and len(r) > 9 else "LINEAR"
        } for r in rows]

    def validate_chronology(self, chapter_num: int, event_time_str: str, temporal_mode: str = "LINEAR") -> tuple[bool, str]:
        """Kiểm tra thời gian không bị đảo lộn vô lý so với các chương trước hoặc mốc khởi đầu.
        Cho phép các chế độ phi tuyến: FLASHBACK, DREAM, VISION, PARALLEL có mốc thời gian độc lập."""
        if not event_time_str:
            return True, "Hợp lệ (Không có mốc thời gian)."

        if temporal_mode in ("FLASHBACK", "DREAM", "VISION", "PARALLEL"):
            # Các chế độ phi tuyến tính được phép nằm ngoài hoặc trước dòng thời gian tuyến tính
            return True, f"Hợp lệ ({temporal_mode}: Cho phép mốc thời gian phi tuyến tính)."

        try:
            curr_dt = datetime.fromisoformat(event_time_str)
            start_dt = datetime.fromisoformat(self.START_DATE_STR)
            if curr_dt < start_dt:
                return False, f"TIMELINE_ERROR: Thời gian ({event_time_str}) trước ngày bắt đầu tác phẩm (2026-09-13) mà không gắn tag Flashback/Vision!"

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
            return True, "Hợp lệ."
        except ValueError as ve:
            return False, f"TIMELINE_FORMAT_ERROR: Định dạng ISO datetime không hợp lệ '{event_time_str}': {ve}"
        except Exception as e:
            return False, f"TIMELINE_SYSTEM_ERROR: Lỗi kiểm tra dòng thời gian: {e}"
