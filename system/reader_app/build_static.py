# -*- coding: utf-8 -*-
"""
NovelOS — Trình đóng gói Reader Web tĩnh an toàn
Gọi trực tiếp pipeline generate_static_site để biên dịch toàn bộ Arc/Chương ra dist/
"""
import os
import sys
from pathlib import Path

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE_DIR = os.getenv("NOVEL_OS_ROOT", str(Path(__file__).resolve().parent.parent.parent))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from system.reader_app.generate_static_site import build as generate_build

def build():
    return generate_build()

if __name__ == "__main__":
    build()
