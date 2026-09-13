# -*- coding: utf-8 -*-
import sqlite3
import datetime
from system.core.config import DB_PATH

class TelemetryEngine:
    """Hệ thống Viễn Trắc Quota Siêu Nhẹ (Lightweight Token & Cost Telemetry).
    Theo dõi lượng token tiết kiệm được, số phép toán tất định thay thế LLM và tỷ lệ nén ngữ cảnh.
    """

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._init_table()

    def _init_table(self):
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS telemetry_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            task_type TEXT NOT NULL,
            model_tier TEXT NOT NULL,
            tokens_in_est INTEGER DEFAULT 0,
            tokens_out_est INTEGER DEFAULT 0,
            tokens_saved_est INTEGER DEFAULT 0,
            deterministic_ops_count INTEGER DEFAULT 0,
            cache_hit INTEGER DEFAULT 0,
            description TEXT
        )""")
        conn.commit()
        conn.close()

    def record_event(self, task_type: str, model_tier: str = "DETERMINISTIC",
                     tokens_in_est: int = 0, tokens_out_est: int = 0,
                     tokens_saved_est: int = 0, deterministic_ops_count: int = 1,
                     cache_hit: bool = False, description: str = ""):
        """Ghi nhận một sự kiện vận hành vào bảng viễn trắc."""
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cur = conn.cursor()
        cur.execute("""INSERT INTO telemetry_events 
                       (task_type, model_tier, tokens_in_est, tokens_out_est, tokens_saved_est, deterministic_ops_count, cache_hit, description)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    (task_type, model_tier, tokens_in_est, tokens_out_est, tokens_saved_est,
                     deterministic_ops_count, 1 if cache_hit else 0, description))
        conn.commit()
        conn.close()

    def get_summary_stats(self) -> dict:
        """Tính toán các chỉ số tổng hợp về tiết kiệm quota và tài nguyên."""
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cur = conn.cursor()

        cur.execute("""SELECT 
            COUNT(*),
            SUM(tokens_in_est),
            SUM(tokens_out_est),
            SUM(tokens_saved_est),
            SUM(deterministic_ops_count),
            SUM(cache_hit)
            FROM telemetry_events""")
        row = cur.fetchone()

        total_events = row[0] or 0
        total_in = row[1] or 0
        total_out = row[2] or 0
        total_saved = row[3] or 0
        total_det_ops = row[4] or 0
        total_cache_hits = row[5] or 0

        # Ước tính chi phí tiết kiệm (Quy đổi $3 / triệu token input, $15 / triệu token output)
        estimated_dollars_saved = round((total_saved / 1_000_000) * 5.0, 4)

        # Tỷ lệ nén ngữ cảnh (%)
        naive_total = total_in + total_saved
        compression_rate = round((total_saved / naive_total * 100), 1) if naive_total > 0 else 0.0

        # Tỷ lệ Cache hit (%)
        cache_hit_rate = round((total_cache_hits / total_events * 100), 1) if total_events > 0 else 0.0

        # Breakdown theo task_type
        cur.execute("""SELECT task_type, model_tier, COUNT(*), SUM(tokens_saved_est), SUM(deterministic_ops_count)
                       FROM telemetry_events GROUP BY task_type, model_tier ORDER BY SUM(tokens_saved_est) DESC""")
        breakdown = []
        for b in cur.fetchall():
            breakdown.append({
                "task_type": b[0],
                "model_tier": b[1],
                "count": b[2] or 0,
                "saved": b[3] or 0,
                "ops": b[4] or 0
            })

        conn.close()

        return {
            "total_events": total_events,
            "total_tokens_in": total_in,
            "total_tokens_out": total_out,
            "total_tokens_saved": total_saved,
            "total_deterministic_ops": total_det_ops,
            "deterministic_ops_count": total_det_ops,
            "compression_rate_percent": compression_rate,
            "compression_percentage": compression_rate,
            "cache_hit_rate_percent": cache_hit_rate,
            "cache_hit_ratio": cache_hit_rate,
            "estimated_cost_saved_usd": estimated_dollars_saved,
            "breakdown": breakdown
        }

    def get_summary_metrics(self) -> dict:
        return self.get_summary_stats()

    def get_recent_events(self, limit: int = 8) -> list:
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cur = conn.cursor()
        cur.execute("""SELECT timestamp, task_type, model_tier, tokens_saved_est, deterministic_ops_count, description 
                       FROM telemetry_events ORDER BY id DESC LIMIT ?""", (limit,))
        events = []
        for r in cur.fetchall():
            events.append({
                "timestamp": r[0],
                "task_type": r[1],
                "model_tier": r[2],
                "tokens_saved": r[3],
                "det_ops": r[4],
                "description": r[5]
            })
        conn.close()
        return events

