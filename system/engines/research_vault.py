# -*- coding: utf-8 -*-
import json
import os
from system.core.config import RESEARCH_DIR, DB_PATH
from system.engines.telemetry_engine import TelemetryEngine

class ResearchVault:
    """Kho Lưu Trữ & Bộ Đệm Nghiên Cứu Chống Lặp (Research Deduplication Cache).
    Tránh tra cứu lặp lại cùng một thực thể ngoài đời thực, phân định rõ ràng RESEARCH != CANON.
    """

    def __init__(self, db_path: str = DB_PATH):
        self.ledger_file = os.path.join(RESEARCH_DIR, "research_ledger.json")
        self.telemetry_engine = TelemetryEngine(db_path)

    def find_cached_research(self, query: str) -> list:
        """Tra cứu nhanh xem tư liệu này đã từng được nghiên cứu chưa (0 token LLM)."""
        items = self.get_items()
        query_lower = query.lower()
        matches = []
        for it in items:
            if query_lower in it.get("topic", "").lower() or query_lower in it.get("summary", "").lower() or query_lower in it.get("source", "").lower():
                matches.append(it)

        if matches:
            self.telemetry_engine.record_event(
                task_type="RESEARCH_CACHE_HIT",
                model_tier="DETERMINISTIC",
                tokens_in_est=0,
                tokens_out_est=0,
                tokens_saved_est=1500,
                deterministic_ops_count=1,
                cache_hit=True,
                description=f"Tái sử dụng tư liệu nghiên cứu đã lưu cho '{query}' (Tiết kiệm 1.500 tokens)"
            )

        return matches

    def add_research_item(self, item_id: str, topic: str, source: str, date: str, summary: str, reliability: str = "HIGH", verified: bool = True, possible_use: str = ""):
        os.makedirs(os.path.dirname(self.ledger_file), exist_ok=True)
        data = {"items": []}
        if os.path.exists(self.ledger_file):
            with open(self.ledger_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        
        # Kiểm tra trùng lặp theo source URL hoặc topic
        for existing in data.get("items", []):
            if existing.get("source") == source and existing.get("topic") == topic:
                return existing  # Đã có trong cache, không thêm lặp

        item = {
            "id": item_id, "topic": topic, "source": source, "date": date,
            "summary": summary, "reliability": reliability, "verified": verified,
            "possible_use": possible_use,
            "canon_status": "RESEARCH_ONLY"
        }
        data["items"].append(item)
        with open(self.ledger_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return item

    def get_items(self) -> list:
        if not os.path.exists(self.ledger_file):
            return []
        with open(self.ledger_file, "r", encoding="utf-8") as f:
            return json.load(f).get("items", [])

