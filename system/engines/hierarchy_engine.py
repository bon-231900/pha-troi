# -*- coding: utf-8 -*-
"""Động cơ Phân Cấp Cốt Truyện 8 Tầng & Tóm Tắt Cuộn (Hierarchical Plot & Roll-up Engine).
Quản lý cây phân cấp: Saga -> Era -> Volume -> Arc -> Mini-Arc -> Chapter -> Scene -> Beat.
Cung cấp lát cắt ngữ cảnh phân tầng (Hierarchical Context Slice) cho từng chương,
giúp LLM nắm vững mục tiêu vĩ mô mà không bị bão hòa token.
"""

import sqlite3
import json
from datetime import datetime
from system.core.config import DB_PATH

class HierarchyEngine:
    LEVELS = ["saga", "era", "volume", "arc", "mini_arc", "chapter", "scene", "beat"]

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path

    def get_node(self, node_id: str) -> dict:
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cur = conn.cursor()
        cur.execute("""
        SELECT id, level, parent_id, order_index, title, summary, objective, stakes, pov, word_count, status
        FROM story_hierarchy WHERE id = ?
        """, (node_id,))
        row = cur.fetchone()
        conn.close()
        if not row:
            return None
        return {
            "id": row[0], "level": row[1], "parent_id": row[2], "order_index": row[3],
            "title": row[4], "summary": row[5], "objective": row[6], "stakes": row[7],
            "pov": row[8], "word_count": row[9], "status": row[10]
        }

    def get_children(self, parent_id: str) -> list:
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cur = conn.cursor()
        cur.execute("""
        SELECT id, level, parent_id, order_index, title, summary, word_count, status
        FROM story_hierarchy WHERE parent_id = ? ORDER BY order_index ASC
        """, (parent_id,))
        rows = cur.fetchall()
        conn.close()
        return [{
            "id": r[0], "level": r[1], "parent_id": r[2], "order_index": r[3],
            "title": r[4], "summary": r[5], "word_count": r[6], "status": r[7]
        } for r in rows]

    def get_ancestors(self, node_id: str) -> list:
        """Truy ngược toàn bộ chuỗi phả hệ từ lá lên gốc (Chapter -> MiniArc -> Arc -> Volume -> Era -> Saga)."""
        ancestors = []
        curr = self.get_node(node_id)
        while curr and curr.get("parent_id"):
            parent = self.get_node(curr["parent_id"])
            if parent:
                ancestors.append(parent)
                curr = parent
            else:
                break
        return ancestors

    def get_chapter_hierarchy_context(self, chapter_num: int) -> dict:
        """Trích xuất lát cắt phân cấp chặt chẽ cho một chương cụ thể để đưa vào Context Pack."""
        cid = f"ch_{chapter_num:03d}"
        ch_node = self.get_node(cid)
        ancestors = self.get_ancestors(cid) if ch_node else []

        context_slice = {
            "chapter_id": cid,
            "chapter_title": ch_node["title"] if ch_node else f"Chương {chapter_num}",
            "saga": None,
            "volume": None,
            "arc": None,
            "mini_arc": None
        }

        for anc in ancestors:
            lvl = anc["level"]
            if lvl == "mini_arc" and not context_slice["mini_arc"]:
                context_slice["mini_arc"] = {"id": anc["id"], "title": anc["title"], "summary": anc["summary"]}
            elif lvl == "arc" and not context_slice["arc"]:
                context_slice["arc"] = {"id": anc["id"], "title": anc["title"], "objective": anc["objective"], "summary": anc["summary"]}
            elif lvl == "volume" and not context_slice["volume"]:
                context_slice["volume"] = {"id": anc["id"], "title": anc["title"], "objective": anc["objective"]}
            elif lvl == "saga" and not context_slice["saga"]:
                context_slice["saga"] = {"id": anc["id"], "title": anc["title"]}

        return context_slice

    def roll_up_word_counts(self, parent_id: str) -> int:
        """Tính tổng số từ lũy tiến của một nút cha dựa trên toàn bộ các nút con."""
        children = self.get_children(parent_id)
        total_words = 0
        for child in children:
            if child["level"] == "chapter":
                total_words += child["word_count"] or 0
            else:
                total_words += self.roll_up_word_counts(child["id"])

        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cur = conn.cursor()
        cur.execute("UPDATE story_hierarchy SET word_count = ? WHERE id = ?", (total_words, parent_id))
        conn.commit()
        conn.close()
        return total_words
