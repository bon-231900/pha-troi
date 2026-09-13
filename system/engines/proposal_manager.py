import sqlite3
import json
from system.core.config import DB_PATH

class ProposalManager:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path

    def create_proposal(self, prop_id: str, title: str, description: str, why_it_matters: str, affected_canon: str, affected_characters: str, affected_plot: str, alternatives: list, recommended_option: str, risk: str) -> str:
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("""INSERT OR REPLACE INTO proposals (id, title, description, why_it_matters, affected_canon, affected_characters, affected_plot, alternatives_json, recommended_option, risk, status)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'PENDING')""",
                    (prop_id, title, description, why_it_matters, affected_canon, affected_characters, affected_plot, json.dumps(alternatives, ensure_ascii=False), recommended_option, risk))
        conn.commit()
        conn.close()
        return prop_id

    def list_proposals(self, status: str = None) -> list:
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        if status:
            cur.execute("SELECT id, title, description, why_it_matters, affected_canon, affected_characters, affected_plot, recommended_option, risk, status FROM proposals WHERE status = ?", (status,))
        else:
            cur.execute("SELECT id, title, description, why_it_matters, affected_canon, affected_characters, affected_plot, recommended_option, risk, status FROM proposals ORDER BY created_at DESC")
        rows = cur.fetchall()
        conn.close()
        return [{
            "id": r[0], "title": r[1], "description": r[2], "why_it_matters": r[3],
            "affected_canon": r[4], "affected_characters": r[5], "affected_plot": r[6],
            "recommended_option": r[7], "risk": r[8], "status": r[9]
        } for r in rows]

    def approve_proposal(self, prop_id: str):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("UPDATE proposals SET status = 'APPROVED', reviewed_at = CURRENT_TIMESTAMP WHERE id = ?", (prop_id,))
        conn.commit()
        conn.close()

    def reject_proposal(self, prop_id: str):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("UPDATE proposals SET status = 'REJECTED', reviewed_at = CURRENT_TIMESTAMP WHERE id = ?", (prop_id,))
        conn.commit()
        conn.close()
