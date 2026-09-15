# -*- coding: utf-8 -*-
import unittest
import json
import os

class TestInventoryIntegrity(unittest.TestCase):
    def setUp(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.inventory_json = os.path.join(self.base_dir, "state", "inventory.json")
        self.inventory_md = os.path.join(self.base_dir, "canon", "items", "inventory.md")

    def test_inventory_files_exist(self):
        self.assertTrue(os.path.exists(self.inventory_json), "inventory.json must exist")
        self.assertTrue(os.path.exists(self.inventory_md), "inventory.md must exist")

    def test_inventory_json_structure(self):
        with open(self.inventory_json, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertIn("holder", data)
        self.assertIn("cultivation_realm", data)
        self.assertIn("core_weapons_and_artifacts", data)
        self.assertIn("core_skills", data)
        
        # Pacing verification: Realm must NOT exceed Luyện Cốt
        self.assertIn("Luyện Cốt", data["cultivation_realm"], "Realm should be firmly anchored in Luyện Cốt")

        # Every core weapon/artifact must have name, location, condition, function
        for item in data["core_weapons_and_artifacts"]:
            self.assertTrue(item.get("name"), "Item must have name")
            self.assertTrue(item.get("location"), "Item must have location")
            self.assertTrue(item.get("condition"), "Item must have condition")
            self.assertTrue(item.get("function"), "Item must have function")

if __name__ == "__main__":
    unittest.main()
