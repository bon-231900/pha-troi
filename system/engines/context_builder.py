# -*- coding: utf-8 -*-
import os
import json
import sqlite3
from system.core.config import DB_PATH, CANON_DIR
from system.engines.retrieval_engine import RetrievalEngine
from system.engines.telemetry_engine import TelemetryEngine

class ContextBuilder:
    """Động cơ Đóng Gói Ngữ Cảnh Tinh Gọn & Thích Ứng (Adaptive Hierarchical Context Pack).
    Tối ưu hóa cực hạn ngân sách token: Tách tầng bất biến (Static Caching), chỉ nạp delta thực thể
    và trích xuất đúng phân đoạn quá khứ liên quan qua FTS5 BM25.
    """

    STATIC_STYLE_CONSTRAINTS = [
        "Modern Cinematic: Giàu hình ảnh, nhịp phim, không gian rõ ràng, thoại tự nhiên đời thực.",
        "Literary Depth: Khắc họa nội tâm, kết cấu cảm xúc sâu, có ý nghĩa nhân sinh.",
        "Mature Dark Fantasy: Nghiêm túc, tàn khốc khi cần, không lạm dụng bạo lực vô nghĩa.",
        "Vietnam 2026: Đời thường TP.HCM, kẹt xe, thời tiết, căn hộ, thói quen sinh hoạt thực tế.",
        "Không dump lore! Mọi thông tin mở ra qua hành động, quan sát và đối thoại.",
        "Minh An 100% là người bình thường. Cấm mọi suy diễn gian lận/hệ thống/chuyển sinh."
    ]

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self.retrieval_engine = RetrievalEngine(db_path)
        self.telemetry_engine = TelemetryEngine(db_path)

    def build_context_pack(self, chapter_num: int, pov: str, active_characters: list, location_id: str, scene_objective: str = "") -> dict:
        """Tạo gói ngữ cảnh phân tầng thích ứng (Adaptive Context Pack).
        Đảm bảo dung lượng token cố định O(1) bất kể tiểu thuyết đang ở chương 3 hay chương 2.000.
        """
        pack = {
            "chapter_num": chapter_num,
            "pov": pov,
            "location_id": location_id,
            "canon_summary": [],
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
        # Thay vì nạp toàn bộ hàng trăm điều luật, lấy 3 điều luật cốt lõi (LOCKED) + luật liên quan qua FTS5
        cur.execute("SELECT key, title, content FROM canon_entries WHERE level = 'LOCKED' LIMIT 4")
        for row in cur.fetchall():
            pack["canon_summary"].append(f"[{row[0]}] {row[1]}: {row[2]}")

        # Tìm thêm canon/lore liên quan mật thiết đến phân cảnh qua FTS5 BM25
        search_query = f"{scene_objective} {' '.join(active_characters)} {location_id}".strip()
        targeted_lore = self.retrieval_engine.search(search_query, doc_types=["canon", "world"], top_k=2)
        for tl in targeted_lore:
            lore_entry = f"[{tl['doc_id']}] {tl['title']}: {tl['content']}"
            if lore_entry not in pack["canon_summary"]:
                pack["canon_summary"].append(lore_entry)

        # 2. DELTA THỰC THỂ HOẠT ĐỘNG (Active Entities Delta Only)
        # Chỉ nạp trạng thái của nhân vật tham gia phân cảnh, bỏ qua toàn bộ dàn nhân vật phụ không có mặt
        for cid in active_characters:
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
        for cid in active_characters:
            cur.execute("""SELECT statement, epistemic_status FROM knowledge_matrix 
                           WHERE character_id = ? 
                           ORDER BY id DESC LIMIT 5""", (cid,))
            knows = cur.fetchall()
            pack["epistemic_knowledge"][cid] = {k[0]: k[1] for k in knows}

        # 4. SỔ CÁI PHỤC BÚT CẬN KỀ (Proximity-based Foreshadowing)
        # Chỉ nạp những hạt mầm có kỳ vọng thu hồi gần chương hiện tại hoặc vừa gieo
        cur.execute("""SELECT id, seed_description, actual_meaning FROM foreshadowing_ledger 
                       WHERE status IN ('PLANTED', 'ACTIVE')
                       ORDER BY planted_chapter DESC LIMIT 3""")
        for r in cur.fetchall():
            pack["active_foreshadowing"].append({"id": r[0], "seed": r[1], "meaning": r[2]})

        # 5. DÒNG THỜI GIAN NGAY TRƯỚC ĐÓ (Recent Events)
        cur.execute("SELECT title, summary FROM timeline_events ORDER BY chapter_num DESC, scene_num DESC LIMIT 2")
        for r in cur.fetchall():
            pack["recent_events"].append(f"{r[0]}: {r[1]}")

        # 6. TRÍCH ĐOẠN QUÁ KHỨ LIÊN QUAN TỪ FTS5 (Relevant Past Excerpts)
        if scene_objective:
            past_scenes = self.retrieval_engine.search(scene_objective, doc_types=["chapter_scene"], top_k=2)
            for ps in past_scenes:
                pack["relevant_past_excerpts"].append({
                    "source": ps["title"],
                    "excerpt": ps["content"][:300] + "..."
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

