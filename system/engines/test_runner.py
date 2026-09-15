import unittest
import io
import os
import sys

from system.core.config import ROOT_DIR

def run_all_narrative_tests() -> dict:
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=os.path.join(ROOT_DIR, "tests"), pattern="test_*.py")
    stream = io.StringIO()
    runner = unittest.TextTestRunner(stream=stream, verbosity=2)
    result = runner.run(suite)
    
    return {
        "total": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "passed": result.wasSuccessful(),
        "output": stream.getvalue()
    }

if __name__ == "__main__":
    res = run_all_narrative_tests()
    print(res["output"])
    print(f"Passed: {res['passed']} (Ran {res['total']} tests)")
