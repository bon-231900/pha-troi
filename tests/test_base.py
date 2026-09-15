# -*- coding: utf-8 -*-
"""Base test case providing an isolated copy of the database to prevent test pollution."""

import unittest
import os
import sys
import shutil
import tempfile

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from system.core.config import DB_PATH

class IsolatedDatabaseTestCase(unittest.TestCase):
    """Base class for tests that require a full SQLite database without touching production database/novel_os.db."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.temp_dir = tempfile.mkdtemp(prefix="novel_os_test_")
        cls.isolated_db_path = os.path.join(cls.temp_dir, "isolated_novel_os.db")
        shutil.copy2(DB_PATH, cls.isolated_db_path)
        cls._orig_novel_os_db = os.environ.get("NOVEL_OS_DB")
        os.environ["NOVEL_OS_DB"] = cls.isolated_db_path
        cls.db_path = cls.isolated_db_path

    @classmethod
    def tearDownClass(cls):
        if cls._orig_novel_os_db is not None:
            os.environ["NOVEL_OS_DB"] = cls._orig_novel_os_db
        elif "NOVEL_OS_DB" in os.environ:
            del os.environ["NOVEL_OS_DB"]

        if os.path.exists(cls.temp_dir):
            shutil.rmtree(cls.temp_dir, ignore_errors=True)
        super().tearDownClass()
