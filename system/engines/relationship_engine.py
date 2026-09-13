# -*- coding: utf-8 -*-
import json
import os
from system.core.config import STATE_DIR

class RelationshipEngine:
    def __init__(self):
        self.state_file = os.path.join(STATE_DIR, "relationships.json")

    def get_relationship(self, char_a: str, char_b: str) -> dict:
        if not os.path.exists(self.state_file):
            return {}
        with open(self.state_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        pairs = data.get("pairs", {})
        pair_key = f"{char_a}_x_{char_b}"
        alt_key = f"{char_b}_x_{char_a}"
        return pairs.get(pair_key) or pairs.get(alt_key) or {
            "source": char_a, "target": char_b, "trust": 0, "respect": 0,
            "affection": 0, "fear": 0, "romantic_awareness": 0, "notes": "Chưa tương tác."
        }

    def update_relationship(self, char_a: str, char_b: str, updates: dict, note: str = ""):
        os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
        data = {"pairs": {}}
        if os.path.exists(self.state_file):
            with open(self.state_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        
        pair_key = f"{char_a}_x_{char_b}"
        rel = data["pairs"].get(pair_key, {
            "source": char_a, "target": char_b, "trust": 0, "respect": 0,
            "affection": 0, "fear": 0, "romantic_awareness": 0
        })
        for k, v in updates.items():
            rel[k] = v
        if note:
            rel["notes"] = note
        data["pairs"][pair_key] = rel

        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
