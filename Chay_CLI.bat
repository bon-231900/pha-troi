@echo off
chcp 65001 > nul
set PYTHONIOENCODING=utf-8
title Novel OS - Bảng Điều Khiển CLI
echo ============================================================
echo   NOVEL OS — TIỂU THUYẾT "PHÁ TRỜI" (PHA_TROI)
echo   Bảng điều khiển dòng lệnh CLI (100%% Tiếng Việt)
echo ============================================================
python -m system.cli --help
cmd /k