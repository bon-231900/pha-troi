@echo off
chcp 65001 > nul
set PYTHONIOENCODING=utf-8
title Novel OS - Xưởng Sáng Tác Phá Trời
echo ============================================================
echo   NOVEL OS — TIỂU THUYẾT "PHÁ TRỜI" (PHA_TROI)
echo   Đang khởi chạy Xưởng Sáng Tác Web Studio...
echo   Giao diện sẽ tự động mở tại: http://127.0.0.1:8765
echo ============================================================
start http://127.0.0.1:8765
python -m system.cli studio
pause