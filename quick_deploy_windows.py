#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
编译未来教培管理系统 - Windows快速部署脚本
专门针对Windows系统优化，避免Unicode编码问题
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def run_command(cmd, description=""):
    """运行命令并显示结果"""
    if description:
        print(f"执行: {description}...")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='gbk')
        if result.returncode == 0:
            print(f"   成功")
            return True
        else:
            print(f"   失败: {result.stderr}")
            return False
    except Exception as e:
        print(f"   异常: {e}")
        return False

def quick_deploy_windows():
    """Windows快速部署"""
    print("编译未来教培管理系统 - Windows快速部署")
    print("=" * 50)
    
    # 获取项目路径
    project_root = Path(__file__).parent
    backend_dir = project_root / "backend"
    
    print(f"项目路径: {project_root}")
    print(f"后端路径: {backend_dir}")
    print()
    
    # 1. 检查Python
    print("检查Python环境...")
    python_version = sys.version_info
    print(f"   - Python版本: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version < (3, 7):
        print("Python版本过低，需要Python 3.7或更高版本")
        return False
    
    # 2. 安装依赖
    print("安装依赖...")
    os.chdir(backend_dir)
    
    # 安装requirements.txt
    if Path("requirements.txt").exists():
        if not run_command(f"{sys.executable} -m pip install -r requirements.txt", "安装requirements.txt"):
            return False
    
    # 安装必要包
    packages = ["pymysql", "python-dotenv", "requests"]
    for package in packages:
        run_command(f"{sys.executable} -m pip install {package}", f"安装{package}")
    
    # 3. 设置数据库
    print("设置数据库...")
    if not run_command(f"{sys.executable} direct_db_init.py", "初始化数据库"):
        print("数据库初始化失败，但继续部署...")
    
    # 4. 创建启动脚本
    print("创建启动脚本...")
    
    # Windows启动脚本
    startup_script = '''@echo off
echo 编译未来教培管理系统启动中...
cd /d "%~dp0backend"
python start_server.py
pause
'''
    with open(project_root / "start.bat", 'w', encoding='gbk') as f:
        f.write(startup_script)
    print("   Windows启动脚本: start.bat")
    
    # 5. 测试启动
    print("测试系统启动...")
    try:
        # 启动服务器（后台运行）
        process = subprocess.Popen([
            sys.executable, "start_server.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # 等待启动
        import time
        time.sleep(3)
        
        # 检查进程
        if process.poll() is None:
            print("   服务器启动成功")
            process.terminate()
        else:
            print("   服务器启动失败")
            return False
            
    except Exception as e:
        print(f"   启动测试失败: {e}")
        return False
    
    # 6. 显示结果
    print()
    print("=" * 50)
    print("快速部署完成！")
    print("=" * 50)
    print("系统信息:")
    print("   - 访问地址: http://localhost:5000")
    print("   - API文档: http://localhost:5000/api")
    print("   - 健康检查: http://localhost:5000/health")
    print("   - 管理员: admin / admin123")
    print("=" * 50)
    print("启动方式:")
    print("   - 双击: start.bat")
    print("   - 命令行: cd backend && python start_server.py")
    print("=" * 50)
    print("提示:")
    print("   - 如需安装为系统服务，请运行 python deploy.py")
    print("   - 遇到问题请查看控制台错误信息")
    print("=" * 50)
    
    return True

def main():
    """主函数"""
    try:
        success = quick_deploy_windows()
        if success:
            print("\n快速部署成功！")
            return 0
        else:
            print("\n快速部署失败")
            return 1
    except KeyboardInterrupt:
        print("\n部署被中断")
        return 1
    except Exception as e:
        print(f"\n部署异常: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main()) 