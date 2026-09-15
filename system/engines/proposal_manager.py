# -*- coding: utf-8 -*-
"""
Novel OS — ProposalManager (Quản lý Đề xuất & Chuyển đổi Đột biến Canon)
Đảm bảo AI chỉ tạo đề xuất (PENDING), chỉ khi Tác giả phê duyệt thì đề xuất mới được chuyển đổi
thành đột biến trạng thái chính thức (APPLIED) có kiểm toán và khả năng hoàn tác (ROLLED_BACK).
"""
import sqlite3
import json
from datetime import datetime
from system.core.config import DB_PATH

class ProposalManager:
    STATUSES = ["PENDING", "APPROVED", "APPLYING", "APPLIED", "FAILED", "REJECTED", "ROLLED_BACK"]

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path

    def create_proposal(self, prop_id: str, title: str, description: str, why_it_matters: str,
                        affected_canon: str, affected_characters: str, affected_plot: str,
                        alternatives: list, recommended_option: str, risk: str) -> str:
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cur = conn.cursor()
        cur.execute("""INSERT OR REPLACE INTO proposals (
            id, title, description, why_it_matters, affected_canon, affected_characters,
            affected_plot, alternatives_json, recommended_option, risk, status, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'PENDING', CURRENT_TIMESTAMP)""",
        (prop_id, title, description, why_it_matters, affected_canon, affected_characters,
         affected_plot, json.dumps(alternatives, ensure_ascii=False), recommended_option, risk))
        conn.commit()
        conn.close()
        return prop_id

    def get_proposal(self, prop_id: str) -> dict:
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cur = conn.cursor()
        cur.execute("""SELECT id, title, description, why_it_matters, affected_canon,
                              affected_characters, affected_plot, alternatives_json,
                              recommended_option, risk, status, created_at, reviewed_at
                       FROM proposals WHERE id = ?""", (prop_id,))
        r = cur.fetchone()
        conn.close()
        if not r:
            return None
        return {
            "id": r[0], "title": r[1], "description": r[2], "why_it_matters": r[3],
            "affected_canon": r[4], "affected_characters": r[5], "affected_plot": r[6],
            "alternatives": json.loads(r[7]) if r[7] else [],
            "recommended_option": r[8], "risk": r[9], "status": r[10],
            "created_at": r[11], "reviewed_at": r[12]
        }

    def list_proposals(self, status: str = None) -> list:
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cur = conn.cursor()
        if status:
            cur.execute("""SELECT id, title, description, why_it_matters, affected_canon,
                                  affected_characters, affected_plot, recommended_option, risk, status
                           FROM proposals WHERE status = ? ORDER BY created_at DESC""", (status,))
        else:
            cur.execute("""SELECT id, title, description, why_it_matters, affected_canon,
                                  affected_characters, affected_plot, recommended_option, risk, status
                           FROM proposals ORDER BY created_at DESC""")
        rows = cur.fetchall()
        conn.close()
        return [{
            "id": r[0], "title": r[1], "description": r[2], "why_it_matters": r[3],
            "affected_canon": r[4], "affected_characters": r[5], "affected_plot": r[6],
            "recommended_option": r[7], "risk": r[8], "status": r[9]
        } for r in rows]

    def approve_proposal(self, prop_id: str, reviewer: str = "Author"):
        """Tác giả phê duyệt đề xuất, chuyển trạng thái sang APPROVED."""
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cur = conn.cursor()
        cur.execute("UPDATE proposals SET status = 'APPROVED', reviewed_at = CURRENT_TIMESTAMP WHERE id = ?", (prop_id,))
        cur.execute("""INSERT INTO audit_log (action_type, description, author, details_json)
                       VALUES ('PROPOSAL_APPROVED', ?, ?, ?)""",
                    (f"Đề xuất {prop_id} đã được phê duyệt", reviewer, json.dumps({"prop_id": prop_id}, ensure_ascii=False)))
        conn.commit()
        conn.close()

    def reject_proposal(self, prop_id: str, reason: str = "", reviewer: str = "Author"):
        """Tác giả từ chối đề xuất, chuyển trạng thái sang REJECTED."""
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cur = conn.cursor()
        cur.execute("UPDATE proposals SET status = 'REJECTED', reviewed_at = CURRENT_TIMESTAMP WHERE id = ?", (prop_id,))
        cur.execute("""INSERT INTO audit_log (action_type, description, author, details_json)
                       VALUES ('PROPOSAL_REJECTED', ?, ?, ?)""",
                    (f"Đề xuất {prop_id} bị từ chối: {reason}", reviewer, json.dumps({"prop_id": prop_id, "reason": reason}, ensure_ascii=False)))
        conn.commit()
        conn.close()

    def apply_proposal(self, prop_id: str, reviewer: str = "Author") -> dict:
        """Thực thi đột biến trạng thái chính thức từ đề xuất đã được duyệt.
        Chuyển trạng thái sang APPLIED và ghi nhận Audit log."""
        prop = self.get_proposal(prop_id)
        if not prop:
            return {"success": False, "error": f"Không tìm thấy đề xuất {prop_id}"}

        if prop["status"] not in ("APPROVED", "PENDING"):
            return {"success": False, "error": f"Đề xuất đang ở trạng thái '{prop['status']}', không thể áp dụng!"}

        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cur = conn.cursor()
        try:
            # 1. Đặt trạng thái APPLYING
            cur.execute("UPDATE proposals SET status = 'APPLYING' WHERE id = ?", (prop_id,))

            # 2. Nếu đề xuất tác động đến Canon, cập nhật hoặc tạo canon entry tương ứng
            if prop.get("affected_canon") and prop["affected_canon"] != "NONE":
                canon_key = prop["affected_canon"].strip()
                cur.execute("""INSERT OR REPLACE INTO canon_entries (id, category, key, title, content, level, approved_by, approved_at)
                               VALUES (?, 'proposal_applied', ?, ?, ?, 'CONFIRMED', ?, CURRENT_TIMESTAMP)""",
                            (f"CANON-{prop_id}", canon_key, prop["title"], prop["description"], reviewer))

            # 3. Đặt trạng thái APPLIED
            cur.execute("UPDATE proposals SET status = 'APPLIED', reviewed_at = CURRENT_TIMESTAMP WHERE id = ?", (prop_id,))

            # 4. Ghi Audit Log
            cur.execute("""INSERT INTO audit_log (action_type, description, author, details_json)
                           VALUES ('PROPOSAL_APPLIED', ?, ?, ?)""",
                        (f"Đề xuất {prop_id} đã được áp dụng vào Canon", reviewer, json.dumps(prop, ensure_ascii=False)))

            conn.commit()
            return {"success": True, "prop_id": prop_id, "status": "APPLIED"}
        except Exception as e:
            conn.rollback()
            cur.execute("UPDATE proposals SET status = 'FAILED' WHERE id = ?", (prop_id,))
            conn.commit()
            return {"success": False, "error": str(e), "status": "FAILED"}
        finally:
            conn.close()

    def rollback_proposal(self, prop_id: str, reason: str = "", reviewer: str = "Author") -> dict:
        """Hoàn tác đề xuất đã áp dụng, chuyển trạng thái sang ROLLED_BACK."""
        prop = self.get_proposal(prop_id)
        if not prop:
            return {"success": False, "error": f"Không tìm thấy đề xuất {prop_id}"}

        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cur = conn.cursor()
        try:
            # Thu hồi canon entry nếu có
            cur.execute("DELETE FROM canon_entries WHERE id = ?", (f"CANON-{prop_id}",))
            cur.execute("UPDATE proposals SET status = 'ROLLED_BACK', reviewed_at = CURRENT_TIMESTAMP WHERE id = ?", (prop_id,))
            cur.execute("""INSERT INTO audit_log (action_type, description, author, details_json)
                           VALUES ('PROPOSAL_ROLLED_BACK', ?, ?, ?)""",
                        (f"Đề xuất {prop_id} đã hoàn tác: {reason}", reviewer, json.dumps({"prop_id": prop_id, "reason": reason}, ensure_ascii=False)))
            conn.commit()
            return {"success": True, "prop_id": prop_id, "status": "ROLLED_BACK"}
        except Exception as e:
            conn.rollback()
            return {"success": False, "error": str(e)}
        finally:
            conn.close()
