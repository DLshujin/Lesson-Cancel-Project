#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
编译未来教培管理系统 - 服务器启动脚本
"""

import os
import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """检查依赖是否安装"""
    print("检查依赖...")
    
    required_packages = [
        'flask',
        'flask-sqlalchemy',
        'flask-login',
        'flask-cors',
        'pymysql',
        'requests'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"缺少依赖包: {', '.join(missing_packages)}")
        print("请运行: pip install -r requirements.txt")
        return False
    
    print("依赖检查通过")
    return True

def check_database():
    """检查数据库连接"""
    print("检查数据库连接...")
    
    try:
        from config import SQLALCHEMY_DATABASE_URI
        from models.user import db
        from app_complete import create_app
        
        app = create_app()
        with app.app_context():
            # 尝试连接数据库
            db.engine.execute('SELECT 1')
            print("数据库连接正常")
            return True
    except Exception as e:
        print(f"数据库连接失败: {e}")
        print("请检查数据库配置和连接")
        return False

def init_database():
    """初始化数据库"""
    print("初始化数据库...")
    
    try:
        from app_complete import create_app, init_db
        
        app = create_app()
        with app.app_context():
            init_db()
            print("数据库初始化完成")
            return True
    except Exception as e:
        print(f"数据库初始化失败: {e}")
        return False

def start_server():
    """启动服务器"""
    print("启动编译未来教培管理系统...")
    
    try:
        from app_complete import create_app
        
        app = create_app()
        
        print("=" * 60)
        print("编译未来教培管理系统启动成功！")
        print("=" * 60)
        print("系统信息:")
        print("   - API地址: http://localhost:5000")
        print("   - API文档: http://localhost:5000/api")
        print("   - 健康检查: http://localhost:5000/health")
        print("=" * 60)
        print("默认管理员账户:")
        print("   - 用户名: admin")
        print("   - 密码: admin123")
        print("=" * 60)
        print("可用模块:")
        print("   - 认证管理: /api/auth")
        print("   - 学生管理: /api/students")
        print("   - 课程管理: /api/courses")
        print("   - 教室管理: /api/classrooms")
        print("   - 课程安排: /api/schedules")
        print("   - 消课记录: /api/records")
        print("=" * 60)
        print("提示:")
        print("   - 按 Ctrl+C 停止服务器")
        print("   - 查看 API_DOCUMENTATION.md 了解详细接口")
        print("   - 运行 test_all_modules.py 进行功能测试")
        print("=" * 60)
        
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except KeyboardInterrupt:
        print("\n服务器已停止")
    except Exception as e:
        print(f"服务器启动失败: {e}")

def main():
    """主函数"""
    print("编译未来教培管理系统 - 服务器启动器")
    print("=" * 50)
    
    # 检查Python版本
    if sys.version_info < (3, 7):
        print("需要Python 3.7或更高版本")
        return
    
    # 检查依赖
    if not check_dependencies():
        return
    
    # 检查数据库
    if not check_database():
        print("数据库连接失败，是否继续启动？(y/n): ", end="")
        if input().lower() != 'y':
            return
    
    # 初始化数据库
    if not init_database():
        print("数据库初始化失败，是否继续启动？(y/n): ", end="")
        if input().lower() != 'y':
            return
    
    # 启动服务器
    start_server()

if __name__ == '__main__':
    main() 