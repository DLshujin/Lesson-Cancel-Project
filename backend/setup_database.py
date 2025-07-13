#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
编译未来教培管理系统 - 数据库设置向导
"""

import os
import sys
import pymysql
from pathlib import Path

def check_mysql_connection(host, port, username, password):
    """检查MySQL连接"""
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=username,
            password=password,
            charset='utf8mb4'
        )
        connection.close()
        return True
    except Exception as e:
        print(f"❌ MySQL连接失败: {e}")
        return False

def create_database(host, port, username, password, database_name):
    """创建数据库"""
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=username,
            password=password,
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        
        # 创建数据库
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{database_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print(f"✅ 数据库 '{database_name}' 创建成功")
        
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ 创建数据库失败: {e}")
        return False

def update_config_file(host, port, username, password, database_name):
    """更新配置文件"""
    config_content = f'''import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \\
        'mysql+pymysql://{username}:{password}@{host}:{port}/{database_name}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 邮件配置
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'your-email@qq.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'your-smtp-password'
    
    # 分页配置
    POSTS_PER_PAGE = 20
'''
    
    try:
        with open('config.py', 'w', encoding='utf-8') as f:
            f.write(config_content)
        print("✅ 配置文件更新成功")
        return True
    except Exception as e:
        print(f"❌ 更新配置文件失败: {e}")
        return False

def test_database_connection():
    """测试数据库连接"""
    try:
        from config import Config
        from models.user import db
        from app_complete import create_app
        
        app = create_app()
        with app.app_context():
            # 测试连接
            db.engine.execute('SELECT 1')
            print("✅ 数据库连接测试成功")
            return True
    except Exception as e:
        print(f"❌ 数据库连接测试失败: {e}")
        return False

def init_database_tables():
    """初始化数据库表"""
    try:
        from app_complete import create_app, init_db
        
        app = create_app()
        with app.app_context():
            init_db()
            print("✅ 数据库表初始化成功")
            return True
    except Exception as e:
        print(f"❌ 数据库表初始化失败: {e}")
        return False

def main():
    """主函数"""
    print("🗄️  编译未来教培管理系统 - 数据库设置向导")
    print("=" * 60)
    
    # 检查PyMySQL是否安装
    try:
        import pymysql
    except ImportError:
        print("❌ 缺少PyMySQL依赖，请先安装：")
        print("pip install pymysql")
        return
    
    print("📋 请按照提示输入您的MySQL数据库信息：")
    print()
    
    # 获取数据库连接信息
    host = input("请输入MySQL主机地址 (默认: localhost): ").strip() or "localhost"
    port = input("请输入MySQL端口 (默认: 3306): ").strip() or "3306"
    username = input("请输入MySQL用户名 (默认: root): ").strip() or "root"
    password = input("请输入MySQL密码: ").strip()
    database_name = input("请输入数据库名称 (默认: lesson_cancel_db): ").strip() or "lesson_cancel_db"
    
    print()
    print("🔍 正在检查MySQL连接...")
    
    # 检查连接
    if not check_mysql_connection(host, int(port), username, password):
        print("❌ 无法连接到MySQL，请检查：")
        print("1. MySQL服务是否启动")
        print("2. 主机地址、端口是否正确")
        print("3. 用户名、密码是否正确")
        return
    
    print("✅ MySQL连接成功")
    
    # 创建数据库
    print("🗄️  正在创建数据库...")
    if not create_database(host, int(port), username, password, database_name):
        return
    
    # 更新配置文件
    print("📝 正在更新配置文件...")
    if not update_config_file(host, int(port), username, password, database_name):
        return
    
    # 测试数据库连接
    print("🧪 正在测试数据库连接...")
    if not test_database_connection():
        return
    
    # 初始化数据库表
    print("📊 正在初始化数据库表...")
    if not init_database_tables():
        return
    
    print()
    print("=" * 60)
    print("🎉 数据库设置完成！")
    print("=" * 60)
    print("📊 数据库信息:")
    print(f"   - 主机: {host}")
    print(f"   - 端口: {port}")
    print(f"   - 用户名: {username}")
    print(f"   - 数据库: {database_name}")
    print("=" * 60)
    print("🚀 现在可以启动服务器了:")
    print("   python start_server.py")
    print("=" * 60)

if __name__ == '__main__':
    main() 