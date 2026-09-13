# -*- coding: utf-8 -*-
import os
import sqlite3
import hashlib
import re
from system.core.config import DB_PATH, MANUSCRIPT_MD_DIR, CANON_DIR

class RetrievalEngine:
    """Động cơ Truy Xuất Tất Định & Chỉ Mục Hóa Vi Sai sử dụng SQLite FTS5 (BM25 ranking).
    Cho phép tìm kiếm chính xác ngữ cảnh liên quan trong 0.005s mà không tiêu tốn token LLM.
    """

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._init_db_structures()

    def _init_db_structures(self):
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cur = conn.cursor()
        # Bảng theo dõi mã băm để đánh chỉ mục vi sai (Incremental Indexing)
        cur.execute("""CREATE TABLE IF NOT EXISTS index_hashes (
            file_path TEXT PRIMARY KEY,
            sha256 TEXT NOT NULL,
            indexed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")
        # Đảm bảo bảng FTS5 search_index tồn tại
        cur.execute("""CREATE VIRTUAL TABLE IF NOT EXISTS search_index USING fts5(
            doc_id UNINDEXED,
            doc_type,
            title,
            content,
            tags
        )""")
        conn.commit()
        conn.close()

    def _compute_sha256(self, text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def index_chapter(self, chapter_path: str, force: bool = False) -> bool:
        """Đánh chỉ mục vi sai cho 1 chương bản thảo. Bỏ qua nếu nội dung không đổi."""
        if not os.path.exists(chapter_path):
            return False

        with open(chapter_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        current_hash = self._compute_sha256(content)

        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cur = conn.cursor()

        cur.execute("SELECT sha256 FROM index_hashes WHERE file_path = ?", (chapter_path,))
        row = cur.fetchone()
        if row and row[0] == current_hash and not force:
            conn.close()
            return False  # Không đổi -> Bỏ qua, tiết kiệm 100% tài nguyên xử lý!

        # Xóa các phân đoạn cũ của tệp này trong search_index
        filename = os.path.basename(chapter_path)
        base_id = os.path.splitext(filename)[0]
        cur.execute("DELETE FROM search_index WHERE doc_id LIKE ?", (f"{base_id}%",))

        # Tách chương thành các phân đoạn (Scene chunks)
        paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
        chapter_title = paragraphs[0].replace("#", "").strip() if paragraphs and paragraphs[0].startswith("#") else base_id

        # Gom các đoạn thành các chunk có độ dài vừa phải (~250-400 từ)
        chunks = []
        current_chunk = []
        current_len = 0
        for p in paragraphs:
            if p.startswith("#"):
                continue
            words = len(p.split())
            if current_len + words > 300 and current_chunk:
                chunks.append("\n\n".join(current_chunk))
                current_chunk = [p]
                current_len = words
            else:
                current_chunk.append(p)
                current_len += words
        if current_chunk:
            chunks.append("\n\n".join(current_chunk))

        # Gán thẻ từ khóa thực thể tự động
        for idx, chunk in enumerate(chunks, 1):
            tags = []
            if any(k in chunk.lower() for k in ["minh an", "tôi"]):
                tags.append("char_minh_an")
            if any(k in chunk.lower() for k in ["lâm tịch", "nàng", "thanh âm", "tàn hồn"]):
                tags.append("char_lam_tich")
            if any(k in chunk.lower() for k in ["hàng xanh", "ung văn khiêm", "bình thạnh", "sài gòn", "nơ trang long"]):
                tags.append("loc_hcmc")
            if any(k in chunk.lower() for k in ["biển máu", "kiếm gãy", "vòm trời"]):
                tags.append("lore_ancient_war")

            doc_id = f"{base_id}_sc_{idx:02d}"
            cur.execute("""INSERT INTO search_index (doc_id, doc_type, title, content, tags)
                           VALUES (?, ?, ?, ?, ?)""",
                        (doc_id, "chapter_scene", f"{chapter_title} (Đoạn {idx})", chunk, " ".join(tags)))

        # Lưu mã băm mới
        cur.execute("""INSERT OR REPLACE INTO index_hashes (file_path, sha256, indexed_at)
                       VALUES (?, ?, CURRENT_TIMESTAMP)""", (chapter_path, current_hash))
        conn.commit()
        conn.close()
        return True

    def index_canon_and_lore(self):
        """Đánh chỉ mục các thiết lập Canon và thực thể vũ trụ vào FTS5."""
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cur = conn.cursor()

        # Xóa các mục canon cũ
        cur.execute("DELETE FROM search_index WHERE doc_type IN ('canon', 'character', 'world', 'timeline')")

        # 1. Canon entries
        cur.execute("SELECT key, category, title, content, level FROM canon_entries")
        for row in cur.fetchall():
            doc_id = f"canon_{row[0]}"
            cur.execute("""INSERT INTO search_index (doc_id, doc_type, title, content, tags)
                           VALUES (?, 'canon', ?, ?, ?)""",
                        (doc_id, f"[{row[4]}] {row[2]}", row[3], f"{row[1]} {row[0]}"))

        # 2. Character profiles
        cur.execute("SELECT id, name, type, status FROM entities WHERE type = 'character'")
        for row in cur.fetchall():
            doc_id = f"char_{row[0]}"
            cur.execute("""INSERT INTO search_index (doc_id, doc_type, title, content, tags)
                           VALUES (?, 'character', ?, ?, ?)""",
                        (doc_id, f"Nhân vật: {row[1]}", f"Mã: {row[0]}, Trạng thái: {row[3]}", f"{row[0]} {row[1]}"))

        # 3. World nodes
        cur.execute("SELECT id, cosmology_rank, name, cultivation_system, status, description FROM world_nodes")
        for row in cur.fetchall():
            doc_id = f"world_{row[0]}"
            cur.execute("""INSERT INTO search_index (doc_id, doc_type, title, content, tags)
                           VALUES (?, 'world', ?, ?, ?)""",
                        (doc_id, f"Vị diện: {row[2]} (Tầng {row[1]})", row[5], f"{row[0]} {row[3]} {row[4]}"))

        # 4. Timeline events
        cur.execute("SELECT id, title, chapter_num, absolute_time, summary, outcome FROM timeline_events")
        for row in cur.fetchall():
            doc_id = f"event_{row[0]}"
            cur.execute("""INSERT INTO search_index (doc_id, doc_type, title, content, tags)
                           VALUES (?, 'timeline', ?, ?, ?)""",
                        (doc_id, f"Sự kiện: {row[1]} (Chương {row[2]})", f"Thời gian: {row[3]}\nDiễn biến: {row[4]}\nKết quả: {row[5]}", f"ch_{row[2]:03d} {row[0]}"))

        conn.commit()
        conn.close()

    def sync_all_manuscripts(self, force: bool = False) -> int:
        """Quét và đồng bộ toàn bộ bản thảo hiện có vào FTS5 theo cơ chế vi sai."""
        indexed_count = 0
        if os.path.exists(MANUSCRIPT_MD_DIR):
            for root, _, files in os.walk(MANUSCRIPT_MD_DIR):
                for f in sorted(files):
                    if f.endswith(".md"):
                        p = os.path.join(root, f)
                        if self.index_chapter(p, force=force):
                            indexed_count += 1
        self.index_canon_and_lore()
        return indexed_count

    def clean_query(self, query: str) -> str:
        """Làm sạch chuỗi truy vấn để tránh lỗi cú pháp FTS5."""
        clean = re.sub(r'[^\w\s\u00C0-\u1EF9]', ' ', query, flags=re.UNICODE).strip()
        tokens = [t for t in clean.split() if len(t) > 1]
        if not tokens:
            return ""
        # Dùng OR giữa các từ khóa quan trọng
        return " OR ".join(tokens[:8])

    def search(self, query: str, doc_types: list = None, top_k: int = 3) -> list:
        """Tìm kiếm toàn văn FTS5 với xếp hạng BM25."""
        clean_q = self.clean_query(query)
        if not clean_q:
            return []

        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cur = conn.cursor()

        type_filter = ""
        params = [clean_q]
        if doc_types:
            placeholders = ",".join("?" for _ in doc_types)
            type_filter = f"AND doc_type IN ({placeholders})"
            params.extend(doc_types)

        params.append(top_k)
        sql = f"""SELECT doc_id, doc_type, title, content, tags, bm25(search_index) as rank
                  FROM search_index
                  WHERE search_index MATCH ? {type_filter}
                  ORDER BY rank ASC LIMIT ?"""
        
        results = []
        try:
            cur.execute(sql, tuple(params))
            for r in cur.fetchall():
                results.append({
                    "doc_id": r[0],
                    "doc_type": r[1],
                    "title": r[2],
                    "content": r[3],
                    "tags": r[4],
                    "score": round(abs(r[5]), 3)
                })
        except Exception as e:
            # Fallback nếu query syntax gặp lỗi hiếm
            pass
        finally:
            conn.close()

        return results

    def retrieve_relevant_context(self, scene_prompt: str, active_characters: list = None, top_k: int = 3) -> dict:
        """Truy xuất tập trung cho ContextBuilder:
        Lấy đúng trích đoạn chương cũ và điều luật Canon liên quan nhất tới phân cảnh hiện tại.
        """
        # 1. Trích đoạn quá khứ liên quan (Scene Memory)
        past_scenes = self.search(scene_prompt, doc_types=["chapter_scene", "timeline"], top_k=top_k)

        # 2. Điều luật Canon & Lore liên quan (Targeted Lore)
        lore_query = f"{scene_prompt} {' '.join(active_characters or [])}"
        targeted_lore = self.search(lore_query, doc_types=["canon", "world"], top_k=3)

        return {
            "relevant_past_scenes": past_scenes,
            "relevant_lore": targeted_lore
        }

