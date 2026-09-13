import os
from system.core.config import ROOT_DIR, PROJECT_ID

def verify_novel_lock() -> bool:
    lock_file = os.path.join(ROOT_DIR, "NOVEL_LOCK.md")
    if not os.path.exists(lock_file):
        raise RuntimeError("CRITICAL ERROR: NOVEL_LOCK.md not found! System must be hard-locked to PHA_TROI.")
    with open(lock_file, "r", encoding="utf-8") as f:
        content = f.read()
    if f'project_id: "{PROJECT_ID}"' not in content:
        raise RuntimeError(f"CRITICAL ERROR: Project ID mismatch in NOVEL_LOCK.md! Must be {PROJECT_ID}.")
    return True
