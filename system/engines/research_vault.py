import json
import os
from system.core.config import RESEARCH_DIR

class ResearchVault:
    def __init__(self):
        self.ledger_file = os.path.join(RESEARCH_DIR, "research_ledger.json")

    def add_research_item(self, item_id: str, topic: str, source: str, date: str, summary: str, reliability: str = "HIGH", verified: bool = True, possible_use: str = ""):
        os.makedirs(os.path.dirname(self.ledger_file), exist_ok=True)
        data = {"items": []}
        if os.path.exists(self.ledger_file):
            with open(self.ledger_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        
        item = {
            "id": item_id, "topic": topic, "source": source, "date": date,
            "summary": summary, "reliability": reliability, "verified": verified,
            "possible_use": possible_use,
            "canon_status": "RESEARCH_ONLY" # Kh?ng t? ??ng th?nh canon!
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
