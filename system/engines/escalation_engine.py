# -*- coding: utf-8 -*-
"""Động cơ Kiểm Soát Ngân Sách Leo Thang (Escalation Budget Controller).
Quản lý và thực thi nghiêm ngặt ngân sách mở rộng theo 6 trục:
1. POWER_CEILING: Trần sức mạnh tu luyện / chiến đấu
2. GEOGRAPHY_SCALE: Bán kính mở rộng địa lý
3. COSMOLOGY_DEPTH: Chiều sâu hé lộ cấu trúc vũ trụ 7 Đạo
4. STAKES_LEVEL: Tầm mức nguy cơ và cổ phần được mất
5. MYSTERY_REVEAL: Tầng bí mật được phép vén màn
6. EMOTIONAL_INTIMACY: Tốc độ phát triển tình cảm Minh An & Lâm Tịch (Extremely Slow Burn)
"""

import sqlite3
from datetime import datetime
from system.core.config import DB_PATH

class EscalationEngine:
    VALID_AXES = [
        "POWER_CEILING", "GEOGRAPHY_SCALE", "COSMOLOGY_DEPTH",
        "STAKES_LEVEL", "MYSTERY_REVEAL", "EMOTIONAL_INTIMACY"
    ]

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path

    def get_budget(self, scope_id: str, axis: str) -> dict:
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cur = conn.cursor()
        cur.execute("""
        SELECT budget_id, scope_type, scope_id, axis, current_level, allowed_ceiling, cooldown_chapters,
               last_escalated_chapter, description, status
        FROM escalation_budgets
        WHERE scope_id = ? AND axis = ?
        """, (scope_id, axis))
        row = cur.fetchone()
        conn.close()
        if not row:
            return None
        return {
            "budget_id": row[0], "scope_type": row[1], "scope_id": row[2], "axis": row[3],
            "current_level": row[4], "allowed_ceiling": row[5], "cooldown_chapters": row[6],
            "last_escalated_chapter": row[7], "description": row[8], "status": row[9]
        }

    def list_budgets(self, scope_id: str = None) -> list:
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cur = conn.cursor()
        if scope_id:
            cur.execute("""
            SELECT budget_id, scope_type, scope_id, axis, current_level, allowed_ceiling, cooldown_chapters,
                   last_escalated_chapter, description, status
            FROM escalation_budgets WHERE scope_id = ?
            """, (scope_id,))
        else:
            cur.execute("""
            SELECT budget_id, scope_type, scope_id, axis, current_level, allowed_ceiling, cooldown_chapters,
                   last_escalated_chapter, description, status
            FROM escalation_budgets
            """)
        rows = cur.fetchall()
        conn.close()
        return [{
            "budget_id": r[0], "scope_type": r[1], "scope_id": r[2], "axis": r[3],
            "current_level": r[4], "allowed_ceiling": r[5], "cooldown_chapters": r[6],
            "last_escalated_chapter": r[7], "description": r[8], "status": r[9]
        } for r in rows]

    def validate_escalation(self, scope_id: str, axis: str, proposed_level: float, chapter_num: int) -> tuple:
        """Kiểm tra xem đề xuất tăng cấp có vi phạm trần (ceiling) hoặc thời gian hồi (cooldown) hay không."""
        b = self.get_budget(scope_id, axis)
        if not b:
            return True, "Không có ngân sách giới hạn cụ thể cho phạm vi này."

        # 1. Kiểm tra trần tối đa cho phép
        if proposed_level > b["allowed_ceiling"]:
            return False, (f"VI PHẠM TRẦN LEO THANG: Trục '{axis}' tại {scope_id} có mức trần là "
                           f"{b['allowed_ceiling']}, đề xuất mức {proposed_level} bị cấm vượt qua!")

        # 2. Kiểm tra thời gian hồi nếu tăng cấp
        if proposed_level > b["current_level"]:
            gap = chapter_num - b["last_escalated_chapter"]
            if gap < b["cooldown_chapters"]:
                return False, (f"VI PHẠM COOLDOWN: Trục '{axis}' vừa tăng cấp ở chương {b['last_escalated_chapter']} "
                               f"(mới qua {gap}/{b['cooldown_chapters']} chương làm nguội). Cần giữ nhịp ổn định!")

        return True, "Hợp lệ trong ngân sách cho phép."

    def bump_escalation(self, scope_id: str, axis: str, new_level: float, chapter_num: int, reason: str = "") -> dict:
        """Thực hiện tăng cấp ngân sách sau khi đã xác thực."""
        valid, msg = self.validate_escalation(scope_id, axis, new_level, chapter_num)
        if not valid:
            raise ValueError(msg)

        now_iso = datetime.now().isoformat()
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cur = conn.cursor()
        cur.execute("""
        UPDATE escalation_budgets
        SET current_level = ?, last_escalated_chapter = ?, updated_at = ?
        WHERE scope_id = ? AND axis = ?
        """, (new_level, chapter_num, now_iso, scope_id, axis))
        conn.commit()
        conn.close()
        return self.get_budget(scope_id, axis)

    def audit_chapter_escalations(self, scope_id: str, chapter_num: int, chapter_claims: dict) -> list:
        """Kiểm tra toàn diện các yếu tố dự kiến của chương đối chiếu với các trục ngân sách.
        chapter_claims có thể chứa:
          - power_level: float
          - geo_level: float
          - cosmology_level: float
          - stakes_level: float
          - mystery_level: float
          - intimacy_level: float
        """
        violations = []
        axis_mapping = {
            "power_level": "POWER_CEILING",
            "geo_level": "GEOGRAPHY_SCALE",
            "cosmology_level": "COSMOLOGY_DEPTH",
            "stakes_level": "STAKES_LEVEL",
            "mystery_level": "MYSTERY_REVEAL",
            "intimacy_level": "EMOTIONAL_INTIMACY"
        }

        for claim_key, axis_name in axis_mapping.items():
            if claim_key in chapter_claims:
                val = chapter_claims[claim_key]
                valid, msg = self.validate_escalation(scope_id, axis_name, val, chapter_num)
                if not valid:
                    violations.append({
                        "axis": axis_name,
                        "proposed": val,
                        "reason": msg
                    })

        return violations
