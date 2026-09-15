# -*- coding: utf-8 -*-
"""
Test Suite: Bức Tường Thứ Tư & Thuật Ngữ Hậu Trường
Đảm bảo toàn bộ 100% các chương trong bản thảo không chứa bất kỳ từ ngữ meta hay hậu trường sáng tác nào.
"""
import unittest
import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANUSCRIPT_DIR = os.path.join(BASE_DIR, "manuscript", "markdown")

FORBIDDEN_META_PATTERNS = [
    (r'(?<!^#\s)(?<!title:\s")(?<!title:\s)Chương\s+\d+', 'Tham chiếu số chương trong văn bản (vd: Chương 44)'),
    (r'(?<!^#\s)(?<!arc:\s)Hồi\s+\d+', 'Tham chiếu số hồi trong văn bản'),
    (r'(?<!^#\s)(?<!volume:\s)Quyển\s+\d+', 'Tham chiếu số quyển trong văn bản'),
    (r'\btác giả\b', 'Từ ngữ hậu trường: tác giả'),
    (r'\bcốt truyện\b', 'Từ ngữ hậu trường: cốt truyện'),
    (r'\bhậu trường\b', 'Từ ngữ hậu trường: hậu trường'),
    (r'\bbản thảo\b', 'Từ ngữ hậu trường: bản thảo'),
    (r'\bđộc giả\b', 'Từ ngữ hậu trường: độc giả'),
    (r'\bngười đọc\b', 'Từ ngữ hậu trường: người đọc'),
    (r'\bcanon\b', 'Từ ngữ hậu trường: canon'),
    (r'\bplot\b', 'Từ ngữ hậu trường: plot'),
    (r'\bforeshadow', 'Từ ngữ hậu trường: foreshadow'),
    (r'\bbức tường thứ tư\b', 'Từ ngữ hậu trường: bức tường thứ tư'),
    (r'\bfourth wall\b', 'Từ ngữ hậu trường: fourth wall')
]

class TestNoMetaInManuscript(unittest.TestCase):

    def test_all_chapters_free_of_meta_terms(self):
        violations = []
        for root, _, files in os.walk(MANUSCRIPT_DIR):
            for f in sorted(files):
                if f.endswith(".md") and f.startswith("ch_"):
                    filepath = os.path.join(root, f)
                    with open(filepath, "r", encoding="utf-8") as file:
                        lines = file.readlines()
                    
                    in_frontmatter = False
                    for idx, line in enumerate(lines):
                        sline = line.strip()
                        if idx == 0 and sline == "---":
                            in_frontmatter = True
                            continue
                        if in_frontmatter:
                            if sline == "---":
                                in_frontmatter = False
                            continue
                        
                        if sline.startswith("#"):
                            continue
                        
                        for pattern, desc in FORBIDDEN_META_PATTERNS:
                            m = re.search(pattern, line, re.IGNORECASE)
                            if m:
                                violations.append(
                                    f"[{f}:L{idx+1}] Vi phạm: '{m.group(0)}' ({desc}) -> \"{line.strip()[:80]}\""
                                )

        self.assertEqual(len(violations), 0, "\nPhát hiện từ ngữ hậu trường / phá vỡ bức tường thứ tư trong bản thảo:\n" + "\n".join(violations))

if __name__ == "__main__":
    unittest.main()
