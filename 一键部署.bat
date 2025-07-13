@echo off
chcp 65001 >nul
echo 编译未来教培管理系统 - 一键部署
echo ================================================
echo.
echo 正在检查Python环境...
python --version
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python 3.7+
    pause
    exit /b 1
)

echo.
echo 开始部署...
python quick_deploy_windows.py

if errorlevel 1 (
    echo.
    echo 部署失败，请检查错误信息
    pause
    exit /b 1
)

echo.
echo 部署完成！按任意键启动系统...
pause

echo.
echo 启动系统...
cd backend
python start_server.py

pause 