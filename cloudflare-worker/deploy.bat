@echo off
chcp 65001 >nul
echo ==============================================================================
echo    1-CLICK DEPLOY CLOUDFLARE WORKER API (PHATROI.COM)
echo ==============================================================================
cd /d "%~dp0"
py deploy_worker.py
pause
