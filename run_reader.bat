@echo off
title PHÁ TRỜI — Reader Server
chcp 65001 > nul
cd /d "d:\tieu-thuyet"
echo Dang khoi dong may chu doc truyen noi bo...
python system/reader_app/server.py
pause
