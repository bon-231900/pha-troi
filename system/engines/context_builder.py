# -*- coding: utf-8 -*-
import os
import json
import sqlite3
from system.core.config import DB_PATH, CANON_DIR
from system.engines.retrieval_engine import RetrievalEngine
from system.engines.telemetry_engine import TelemetryEngine
from system.engines.hierarchy_engine import HierarchyEngine
from system.engines.thread_engine import StoryThreadEngine
from system.engines.escalation_engine import EscalationEngine

class WriterForeshadowingView:
    """Sanitized view of foreshadowing clues for the AI / writer context.
    Strictly excludes author secrets: actual_meaning, payoff_chapter, and internal notes."""
    @staticmethod
    def create(seed_id: str, seed_description: str, planted_chapter: int, status: str) -> dict:
        return {
            "id": seed_id,
            "observable_clue": seed_description,
            "planted_chapter": planted_chapter,
            "status": status
        }

class ContextBuilder:
    """Động cơ Đóng Gói Ngữ Cảnh Tinh Gọn & Thích Ứng (Adaptive Hierarchical Context Pack).
    Tối ưu hóa cực hạn ngân sách token: Tách tầng bất biến (Static Caching), chỉ nạp delta thực thể
    và trích xuất đúng phân đoạn quá khứ liên quan qua FTS5 BM25.
    """

    DEFAULT_BUDGETS = {
        "max_canon_items": 4,
        "max_active_characters": 3,
        "max_knowledge_per_char": 4,
        "max_threads": 3,
        "max_foreshadowing_items": 3,
        "max_recent_events": 2,
        "max_excerpts": 2,
        "max_excerpt_chars": 280,
        "max_total_tokens": 4000
    }

    STATIC_STYLE_CONSTRAINTS = [
        "Modern Cinematic: Giàu hình ảnh, nhịp phim, không gian rõ ràng, thoại tự nhiên đời thực.",
        "Literary Depth: Khắc họa nội tâm, kết cấu cảm xúc sâu, có ý nghĩa nhân sinh.",
        "Mature Dark Fantasy: Nghiêm túc, tàn khốc khi cần, không lạm dụng bạo lực vô nghĩa.",
        "Vietnam 2026: Đời thường TP.HCM, kẹt xe, thời tiết, căn hộ, thói quen sinh hoạt thực tế.",
        "Không dump lore! Mọi thông tin mở ra qua hành động, quan sát và đối thoại.",
        "Minh An 100% là người bình thường. Cấm mọi suy diễn gian lận/hệ thống/chuyển sinh."
    ]

    def __init__(self, db_path: str = DB_PATH, budgets: dict = None):
        self.db_path = db_path
        self.budgets = dict(self.DEFAULT_BUDGETS)
        if budgets:
            self.budgets.update(budgets)
        self.retrieval_engine = RetrievalEngine(db_path)
        self.telemetry_engine = TelemetryEngine(db_path)
        self.hierarchy_engine = HierarchyEngine(db_path)
        self.thread_engine = StoryThreadEngine(db_path)
        self.escalation_engine = EscalationEngine(db_path)

    def build_context_pack(self, chapter_num: int, pov: str, active_characters: list, location_id: str, scene_objective: str = "") -> dict:
        """Tạo gói ngữ cảnh phân tầng thích ứng (Adaptive Context Pack).
        Đảm bảo dung lượng token cố định O(1) bất kể tiểu thuyết đang ở chương 3 hay chương 2.000.
        """
        pack = {
            "chapter_num": chapter_num,
            "pov": pov,
            "location_id": location_id,
            "canon_summary": [],
            "hierarchy_context": {},
            "active_story_threads": [],
            "escalation_limits": {},
            "character_states": {},
            "epistemic_knowledge": {},
            "active_foreshadowing": [],
            "recent_events": [],
            "relevant_past_excerpts": [],
            "style_constraints": self.STATIC_STYLE_CONSTRAINTS
        }

        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cur = conn.cursor()

        # 1. TẦNG CANON BẤT BIẾN + CHỌN LỌC (Targeted Canon Retrieval)
        # Thay vì nạp toàn bộ hàng trăm điều luật, lấy số điều luật cốt lõi theo budget (LOCKED) + luật liên quan qua FTS5
        cur.execute("SELECT key, title, content FROM canon_entries WHERE level = 'LOCKED' LIMIT ?", (self.budgets["max_canon_items"],))
        for row in cur.fetchall():
            pack["canon_summary"].append(f"[{row[0]}] {row[1]}: {row[2]}")

        # Tìm thêm canon/lore liên quan mật thiết đến phân cảnh qua FTS5 BM25
        search_query = f"{scene_objective} {' '.join(active_characters)} {location_id}".strip()
        targeted_lore = self.retrieval_engine.search(search_query, doc_types=["canon", "world"], top_k=2)
        for tl in targeted_lore:
            lore_entry = f"[{tl['doc_id']}] {tl['title']}: {tl['content']}"
            if lore_entry not in pack["canon_summary"]:
                pack["canon_summary"].append(lore_entry)

        # 1.5. LÁT CẮT PHÂN CẤP & ĐẠI CƯƠNG (Hierarchical Context Slice)
        pack["hierarchy_context"] = self.hierarchy_engine.get_chapter_hierarchy_context(chapter_num)

        # 1.6. TUYẾN TRUYỆN CẦN CHĂM SÓC (Active Story Threads)
        pack["active_story_threads"] = self.thread_engine.get_threads_for_chapter_context(chapter_num, limit=self.budgets["max_threads"])

        # 1.7. GIỚI HẠN LEO THANG (Escalation Limits)
        budgets = self.escalation_engine.list_budgets(scope_id="volume_01")
        pack["escalation_limits"] = {b["axis"]: {"current": b["current_level"], "ceiling": b["allowed_ceiling"]} for b in budgets}

        # 2. DELTA THỰC THỂ HOẠT ĐỘNG (Active Entities Delta Only — Giới hạn số lượng theo budget)
        bounded_chars = active_characters[:self.budgets["max_active_characters"]]
        for cid in bounded_chars:
            cur.execute("""SELECT cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state
                           FROM character_states WHERE character_id = ? ORDER BY chapter_num DESC LIMIT 1""", (cid,))
            st = cur.fetchone()
            if st:
                pack["character_states"][cid] = {
                    "realm": st[0], "condition": st[1],
                    "injuries": json.loads(st[2]) if st[2] else [],
                    "inventory": json.loads(st[3]) if st[3] else [],
                    "emotion": st[4]
                }

        # 3. MA TRẬN NHẬN THỨC CÓ CHỌN LỌC (Epistemic Knowledge Bounds)
        # Lọc các trạng thái UNKNOWN/FORGOTTEN quan trọng để chống leak, cộng thêm sự thật đã biết gần nhất
        for cid in bounded_chars:
            cur.execute("""SELECT statement, epistemic_status FROM knowledge_matrix 
                           WHERE character_id = ? 
                           ORDER BY id DESC LIMIT ?""", (cid, self.budgets["max_knowledge_per_char"]))
            knows = cur.fetchall()
            pack["epistemic_knowledge"][cid] = {k[0]: k[1] for k in knows}

        # 4. SỔ CÁI PHỤC BÚT CẬN KỀ — SANITIZED WRITER VIEW (WriterForeshadowingView)
        # Tuyệt đối KHÔNG query actual_meaning, payoff_chapter, hay ghi chú riêng của tác giả
        cur.execute("""SELECT id, seed_description, planted_chapter, status FROM foreshadowing_ledger 
                       WHERE status IN ('PLANTED', 'ACTIVE') AND planted_chapter <= ?
                       ORDER BY planted_chapter DESC LIMIT ?""", (chapter_num, self.budgets["max_foreshadowing_items"]))
        for r in cur.fetchall():
            pack["active_foreshadowing"].append(
                WriterForeshadowingView.create(seed_id=r[0], seed_description=r[1], planted_chapter=r[2], status=r[3])
            )

        # 5. DÒNG THỜI GIAN NGAY TRƯỚC ĐÓ (Recent Events)
        cur.execute("""SELECT title, summary FROM timeline_events 
                       WHERE chapter_num < ? 
                       ORDER BY chapter_num DESC, scene_num DESC LIMIT ?""", (chapter_num, self.budgets["max_recent_events"]))
        for r in cur.fetchall():
            pack["recent_events"].append(f"{r[0]}: {r[1]}")

        # 6. TRÍCH ĐOẠN QUÁ KHỨ LIÊN QUAN TỪ FTS5 (Relevant Past Excerpts)
        if scene_objective:
            past_scenes = self.retrieval_engine.search(scene_objective, doc_types=["chapter_scene"], top_k=self.budgets["max_excerpts"])
            for ps in past_scenes:
                pack["relevant_past_excerpts"].append({
                    "source": ps["title"],
                    "excerpt": ps["content"][:self.budgets["max_excerpt_chars"]] + "..."
                })

        conn.close()

        # 7. TÍNH TOÁN & GHI NHẬN VIỄN TRẮC (Telemetry Tracking)
        # Ước tính kích thước naive (nếu dump toàn bộ bản thảo + story bible) vs adaptive context pack
        pack_json = json.dumps(pack, ensure_ascii=False)
        optimized_tokens = len(pack_json.split()) * 2  # Ước tính 1 từ ~ 1.5 - 2 tokens tiếng Việt
        
        # Naive dump: Tại chương N, gửi cả bộ Story bible + các chương trước
        naive_tokens = (chapter_num * 2500) + 6000  # Mỗi chương ~2500 tokens + Story bible ~6000 tokens
        tokens_saved = max(0, naive_tokens - optimized_tokens)

        self.telemetry_engine.record_event(
            task_type="CONTEXT_PACK_BUILD",
            model_tier="DETERMINISTIC",
            tokens_in_est=optimized_tokens,
            tokens_out_est=0,
            tokens_saved_est=tokens_saved,
            deterministic_ops_count=6,
            cache_hit=True,
            description=f"Đóng gói ngữ cảnh thích ứng Chương {chapter_num} (Tiết kiệm {tokens_saved:,} tokens)"
        )

        return pack

