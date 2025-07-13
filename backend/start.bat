@echo off
echo 编译未来教培管理系统启动中...
cd /d "%~dp0backend"
python start_server.py
pause
