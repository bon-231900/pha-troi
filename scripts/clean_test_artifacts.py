# -*- coding: utf-8 -*-
"""Clean any residual test artifacts from production database."""

import sqlite3
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from system.core.config import DB_PATH

def clean_test_artifacts(db_path: str = DB_PATH):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    print(f"[*] Cleaning residual test data from {db_path}...")

    # Entities
    cur.execute("DELETE FROM entities WHERE id IN ('char_dead_npc', 'char_ally_d') OR id LIKE 'TEST-%'")
    print(f"  [-] Removed test entities: {cur.rowcount} rows")

    # Character states
    cur.execute("DELETE FROM character_states WHERE character_id IN ('char_dead_npc', 'char_ally_d')")
    print(f"  [-] Removed test character states: {cur.rowcount} rows")

    # Knowledge matrix
    cur.execute("DELETE FROM knowledge_matrix WHERE character_id IN ('char_antagonist_c', 'char_dead_npc', 'char_ally_d') OR fact_key IN ('fact_lam_tich_name', 'fact_ancient_jade', 'fact_earth_prison_origin')")
    print(f"  [-] Removed test knowledge matrix: {cur.rowcount} rows")

    # Foreshadowing ledger
    cur.execute("DELETE FROM foreshadowing_ledger WHERE id IN ('FSH-TEST-DORMANT', 'FSH-SIM-A') OR id LIKE '%TEST%'")
    print(f"  [-] Removed test foreshadowing: {cur.rowcount} rows")

    # Story threads
    cur.execute("DELETE FROM story_threads WHERE thread_id IN ('TH-TEST-DORMANT') OR thread_id LIKE '%TEST%'")
    print(f"  [-] Removed test threads: {cur.rowcount} rows")

    # Timeline events
    cur.execute("DELETE FROM timeline_events WHERE id IN ('EVT-CH100') OR id LIKE '%TEST%'")
    print(f"  [-] Removed test timeline events: {cur.rowcount} rows")

    # Continuity errors
    cur.execute("DELETE FROM continuity_errors WHERE id LIKE '%ERR-10-%' OR id LIKE '%ERR-999-%'")
    print(f"  [-] Removed test continuity errors: {cur.rowcount} rows")

    # Telemetry events
    cur.execute("DELETE FROM telemetry_events WHERE task_type LIKE '%TEST%' OR task_type = 'UNIT_TEST_OPTIMIZATION'")
    print(f"  [-] Removed test telemetry events: {cur.rowcount} rows")

    conn.commit()
    conn.execute("VACUUM")
    conn.close()
    print("[+] Production DB cleaned and vacuumed successfully.")

if __name__ == "__main__":
    clean_test_artifacts()
