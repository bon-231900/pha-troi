# -*- coding: utf-8 -*-
"""Regression test proving tests NEVER touch or mutate production database/novel_os.db."""

import unittest
import hashlib
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from system.core.config import DB_PATH

def compute_file_sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

class TestDatabaseIsolation(unittest.TestCase):
    """Proves that test executions and isolated engine operations never mutate production DB."""

    def test_production_db_is_never_mutated_by_test_suites(self):
        self.assertTrue(os.path.exists(DB_PATH), f"Production DB must exist at {DB_PATH}")

        # 1. Compute baseline checksum & mtime
        initial_hash = compute_file_sha256(DB_PATH)
        initial_mtime = os.path.getmtime(DB_PATH)

        # 2. Run the narrative test suite against isolated environment
        from tests.test_narrative_suite import TestNovelOSNarrativeSuite
        from tests.test_3000_upgrade_suite import Test3000UpgradeSuite
        from tests.test_optimization_suite import TestOptimizationSuite

        import io
        suite = unittest.TestSuite()
        suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestNovelOSNarrativeSuite))
        suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test3000UpgradeSuite))
        suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestOptimizationSuite))

        stream = io.StringIO()
        runner = unittest.TextTestRunner(stream=stream, verbosity=0)
        result = runner.run(suite)

        self.assertTrue(result.wasSuccessful(), f"Isolated test suites should pass cleanly: {result.errors + result.failures}")

        # 3. Verify production DB checksum and mtime are 100% UNCHANGED
        final_hash = compute_file_sha256(DB_PATH)
        final_mtime = os.path.getmtime(DB_PATH)

        self.assertEqual(
            initial_hash,
            final_hash,
            "CRITICAL VIOLATION: Production database/novel_os.db was modified during test run! SHA256 mismatch."
        )
        self.assertEqual(
            initial_mtime,
            final_mtime,
            "CRITICAL VIOLATION: Production database/novel_os.db mtime changed during test run!"
        )

if __name__ == "__main__":
    unittest.main()
