# -*- coding: utf-8 -*-
import subprocess
import os
import shutil
from system.core.config import ROOT_DIR

class GitManager:
    def __init__(self, root_dir: str = ROOT_DIR):
        self.root_dir = root_dir
        self.git_bin = self._resolve_git()

    def _resolve_git(self) -> str:
        g = shutil.which("git")
        if g:
            return g
        candidates = [
            r"C:\Program Files\Git\cmd\git.exe",
            r"C:\Program Files\Git\bin\git.exe",
            r"C:\Program Files (x86)\Git\cmd\git.exe"
        ]
        for c in candidates:
            if os.path.exists(c):
                return c
        return "git"

    def _run_git(self, args: list) -> tuple[int, str]:
        cmd = [self.git_bin] + args
        try:
            res = subprocess.run(cmd, cwd=self.root_dir, capture_output=True, text=True, encoding="utf-8")
            return res.returncode, res.stdout + res.stderr
        except Exception as e:
            return -1, str(e)

    def is_git_repo(self) -> bool:
        code, _ = self._run_git(["rev-parse", "--is-inside-work-tree"])
        return code == 0

    def commit_minor(self, message: str, files: list = None) -> tuple[bool, str]:
        """Tự động commit cho các thay đổi nhỏ (state update, metadata, formatting, index).
        Bắt buộc phải có danh sách tệp tường minh (file manifest). Tuyệt đối không stage toàn repo."""
        if not files:
            return False, "FAIL_CLOSED: git commit_minor yêu cầu danh sách tệp (manifest) tường minh. 'git add .' bị cấm tuyệt đối!"
        
        for f in files:
            self._run_git(["add", str(f)])
        
        full_msg = f"[NovelOS-Minor] {message}"
        code, out = self._run_git(["commit", "-m", full_msg])
        return (code == 0, out)

    def commit_major(self, message: str, files: list = None) -> tuple[bool, str]:
        """Tự động commit cho các mốc kiến trúc hoặc sáng tác chương lớn.
        Bắt buộc phải có danh sách tệp tường minh (file manifest). Tuyệt đối không stage toàn repo."""
        if not files:
            return False, "FAIL_CLOSED: git commit_major yêu cầu danh sách tệp (manifest) tường minh. 'git add .' bị cấm tuyệt đối!"
        
        for f in files:
            self._run_git(["add", str(f)])
        
        full_msg = f"[NovelOS-Major] {message}"
        code, out = self._run_git(["commit", "-m", full_msg])
        return (code == 0, out)

    def status(self) -> str:
        _, out = self._run_git(["status", "--short"])
        return out

    def log(self, n: int = 5) -> str:
        _, out = self._run_git(["log", f"-n{n}", "--oneline"])
        return out
