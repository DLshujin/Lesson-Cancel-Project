#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
编译未来教培管理系统 - 自动数据库设置
自动连接MySQL，创建数据库和表
"""

import os
import sys
import pymysql
from urllib.parse import quote_plus

def auto_setup_database():
    """自动设置数据库"""
    print("🗄️  编译未来教培管理系统 - 自动数据库设置")
    print("=" * 60)
    
    # 默认数据库配置
    host = "localhost"
    port = 3306
    username = "root"
    password = "123456"  # 请根据您的实际密码修改
    database_name = "lesson_cancel_db"
    
    print(f"📋 使用默认配置:")
    print(f"   - 主机: {host}")
    print(f"   - 端口: {port}")
    print(f"   - 用户名: {username}")
    print(f"   - 数据库: {database_name}")
    print()
    
    # 检查PyMySQL
    try:
        import pymysql
    except ImportError:
        print("❌ 缺少PyMySQL依赖，正在安装...")
        os.system("pip install pymysql")
        import pymysql
    
    # 1. 检查MySQL连接
    print("🔍 检查MySQL连接...")
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=username,
            password=password,
            charset='utf8mb4'
        )
        connection.close()
        print("✅ MySQL连接成功")
    except Exception as e:
        print(f"❌ MySQL连接失败: {e}")
        print("请检查:")
        print("1. MySQL服务是否启动")
        print("2. 用户名密码是否正确")
        print("3. 如果密码不同，请修改脚本中的password变量")
        return False
    
    # 2. 创建数据库
    print("🗄️  创建数据库...")
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=username,
            password=password,
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{database_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print(f"✅ 数据库 '{database_name}' 创建成功")
        
        cursor.close()
        connection.close()
    except Exception as e:
        print(f"❌ 创建数据库失败: {e}")
        return False
    
    # 3. 更新配置文件
    print("📝 更新配置文件...")
    try:
        # 处理密码中的特殊字符
        encoded_password = quote_plus(password)
        
        config_content = f'''import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \\
        'mysql+pymysql://{username}:{encoded_password}@{host}:{port}/{database_name}'
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
        
        with open('config.py', 'w', encoding='utf-8') as f:
            f.write(config_content)
        print("✅ 配置文件更新成功")
    except Exception as e:
        print(f"❌ 更新配置文件失败: {e}")
        return False
    
    # 4. 测试数据库连接
    print("🧪 测试数据库连接...")
    try:
        from config import Config
        from models.user import db
        from app_complete import create_app
        
        app = create_app()
        with app.app_context():
            db.engine.execute('SELECT 1')
            print("✅ 数据库连接测试成功")
    except Exception as e:
        print(f"❌ 数据库连接测试失败: {e}")
        return False
    
    # 5. 初始化数据库表
    print("📊 初始化数据库表...")
    try:
        from app_complete import create_app, init_db
        
        app = create_app()
        with app.app_context():
            init_db()
            print("✅ 数据库表初始化成功")
    except Exception as e:
        print(f"❌ 数据库表初始化失败: {e}")
        return False
    
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
    
    return True

if __name__ == '__main__':
    auto_setup_database() 