import os
from pathlib import Path

_DEFAULT_ROOT = Path(__file__).resolve().parent.parent.parent
ROOT_DIR = os.getenv("NOVEL_OS_ROOT", str(_DEFAULT_ROOT))
DB_PATH = os.getenv("NOVEL_OS_DB", os.path.join(ROOT_DIR, "database", "novel_os.db"))
CANON_DIR = os.path.join(ROOT_DIR, "canon")
AUTHOR_SECRET_DIR = os.path.join(ROOT_DIR, "author_secret")
MANUSCRIPT_MD_DIR = os.path.join(ROOT_DIR, "manuscript", "markdown")
MANUSCRIPT_WORD_DIR = os.path.join(ROOT_DIR, "manuscript", "word")
STATE_DIR = os.path.join(ROOT_DIR, "state")
RESEARCH_DIR = os.path.join(ROOT_DIR, "research")
PROPOSALS_DIR = os.path.join(ROOT_DIR, "proposals")
ASSETS_DIR = os.path.join(ROOT_DIR, "assets")

PROJECT_ID = "PHA_TROI"
PROJECT_NAME = "Phá Trời"
AUTHOR_AUTHORITY = "ABSOLUTE"
DEFAULT_POV = "Nguyễn Minh An (Ngôi thứ nhất)"
TARGET_CHAPTERS = 3000
