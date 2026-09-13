import os
import sqlite3
import json
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional

from system.core.config import ROOT_DIR, DB_PATH, MANUSCRIPT_MD_DIR, MANUSCRIPT_WORD_DIR, ASSETS_DIR
from system.core.lock import verify_novel_lock
from system.core.git_manager import GitManager
from system.engines.coauthor_engine import CoAuthorEngine
from system.engines.critique_engine import CritiqueEngine
from system.engines.docx_pipeline import DocxPipeline
from system.engines.canon_engine import CanonEngine
from system.engines.character_engine import CharacterEngine
from system.engines.world_engine import WorldEngine
from system.engines.timeline_engine import TimelineEngine
from system.engines.foreshadowing_engine import ForeshadowingEngine
from system.engines.proposal_manager import ProposalManager
from system.engines.test_runner import run_all_narrative_tests

app = FastAPI(title="Novel OS ? Ph? Tr?i Studio")

# Static assets
os.makedirs(os.path.join(ROOT_DIR, "system", "web", "static"), exist_ok=True)
app.mount("/static", StaticFiles(directory=os.path.join(ROOT_DIR, "system", "web", "static")), name="static")

@app.get("/assets/world-map")
def get_world_map():
    map_path = os.path.join(ASSETS_DIR, "WORLD_MAP_MASTER.jpg")
    if os.path.exists(map_path):
        return FileResponse(map_path, media_type="image/jpeg")
    raise HTTPException(status_code=404, detail="World map image not found")

@app.get("/api/status")
def get_system_status():
    verify_novel_lock()
    gm = GitManager()
    
    # Word count across all markdown manuscripts
    total_words = 0
    chapter_count = 0
    if os.path.exists(MANUSCRIPT_MD_DIR):
        for root, _, files in os.walk(MANUSCRIPT_MD_DIR):
            for f in files:
                if f.endswith(".md"):
                    chapter_count += 1
                    with open(os.path.join(root, f), "r", encoding="utf-8") as fl:
                        total_words += len(fl.read().split())

    return {
        "project": "Ph? Tr?i (PHA_TROI)",
        "author_authority": "ABSOLUTE",
        "chapter_count": chapter_count,
        "total_words": total_words,
        "git_status": gm.status().strip(),
        "recent_commit": gm.log(1).strip()
    }

@app.get("/api/chapter/{chapter_num}")
def get_chapter(chapter_num: int):
    md_file = os.path.join(MANUSCRIPT_MD_DIR, "volume_01", "arc_01", f"ch_{chapter_num:03d}.md")
    if not os.path.exists(md_file):
        raise HTTPException(status_code=404, detail=f"Ch??ng {chapter_num} ch?a ???c kh?i t?o.")
    with open(md_file, "r", encoding="utf-8") as f:
        content = f.read()
    return {
        "chapter_num": chapter_num,
        "content": content,
        "word_count": len(content.split()),
        "has_docx": os.path.exists(os.path.join(MANUSCRIPT_WORD_DIR, "volume_01", f"ch_{chapter_num:03d}.docx"))
    }

class WriteRequest(BaseModel):
    chapter_num: int = 1
    pov: str = "Nguy?n Minh An (First Person)"
    custom_text: Optional[str] = None

@app.post("/api/write-next")
def write_next(req: WriteRequest):
    coauthor = CoAuthorEngine()
    res = coauthor.write_next_chapter(target_chapter_num=req.chapter_num, pov=req.pov, custom_draft_prose=req.custom_text)
    return res

@app.get("/api/audit")
def run_audit():
    return run_all_narrative_tests()

@app.get("/api/canon")
def get_canon():
    c_eng = CanonEngine()
    return c_eng.list_all_canon()

@app.get("/api/characters")
def get_characters():
    char_eng = CharacterEngine()
    result = []
    for cid in ["char_minh_an", "char_lam_tich"]:
        c = char_eng.get_character(cid)
        if c:
            result.append(c)
    return result

@app.get("/api/world")
def get_world():
    w_eng = WorldEngine()
    return w_eng.list_nodes()

@app.get("/api/timeline")
def get_timeline():
    t_eng = TimelineEngine()
    return t_eng.get_events()

@app.get("/api/foreshadowing")
def get_foreshadowing():
    f_eng = ForeshadowingEngine()
    return f_eng.list_seeds()

@app.get("/api/proposals")
def get_proposals():
    p_mgr = ProposalManager()
    return p_mgr.list_proposals()

@app.post("/api/proposals/{prop_id}/approve")
def approve_prop(prop_id: str):
    p_mgr = ProposalManager()
    p_mgr.approve_proposal(prop_id)
    return {"success": True, "id": prop_id, "status": "APPROVED"}

@app.post("/api/proposals/{prop_id}/reject")
def reject_prop(prop_id: str):
    p_mgr = ProposalManager()
    p_mgr.reject_proposal(prop_id)
    return {"success": True, "id": prop_id, "status": "REJECTED"}

@app.get("/api/export-docx/{chapter_num}")
def export_docx(chapter_num: int):
    docx_file = os.path.join(MANUSCRIPT_WORD_DIR, "volume_01", f"ch_{chapter_num:03d}.docx")
    if not os.path.exists(docx_file):
        raise HTTPException(status_code=404, detail="File DOCX ch?a ???c bi?n d?ch.")
    return FileResponse(docx_file, filename=f"Pha_Troi_Ch_{chapter_num:03d}.docx", media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

@app.get("/", response_class=HTMLResponse)
def index_page():
    html_path = os.path.join(ROOT_DIR, "system", "web", "static", "index.html")
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Novel OS Web Studio is loading...</h1>"

def run_server(port: int = 8765):
    import uvicorn
    print(f"[*] Kh?i ch?y Novel OS Web Studio t?i http://127.0.0.1:{port}")
    uvicorn.run("system.web.app:app", host="127.0.0.1", port=port, reload=False)

if __name__ == "__main__":
    run_server()
