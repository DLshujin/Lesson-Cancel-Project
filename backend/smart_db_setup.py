#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
编译未来教培管理系统 - 智能数据库设置
自动尝试多种MySQL配置并设置数据库
"""

import os
import sys
import pymysql
from urllib.parse import quote_plus

def try_mysql_connection(host, port, username, password):
    """尝试MySQL连接"""
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=username,
            password=password,
            charset='utf8mb4',
            connect_timeout=5
        )
        connection.close()
        return True
    except Exception:
        return False

def find_mysql_config():
    """查找可用的MySQL配置"""
    print("🔍 正在查找MySQL配置...")
    
    # 常见的MySQL配置组合
    configs = [
        # (host, port, username, password)
        ("localhost", 3306, "root", ""),  # 无密码
        ("localhost", 3306, "root", "root"),  # 密码为root
        ("localhost", 3306, "root", "123456"),  # 密码为123456
        ("localhost", 3306, "root", "password"),  # 密码为password
        ("localhost", 3306, "root", "A123bc!@"),  # 密码为A123bc!@"
        ("127.0.0.1", 3306, "root", ""),  # 使用IP地址
        ("127.0.0.1", 3306, "root", "root"),
        ("127.0.0.1", 3306, "root", "123456"),
    ]
    
    for host, port, username, password in configs:
        print(f"   尝试: {username}@{host}:{port} (密码: {'*' * len(password) if password else '无密码'})")
        if try_mysql_connection(host, port, username, password):
            print(f"✅ 找到可用配置: {username}@{host}:{port}")
            return host, port, username, password
    
    return None

def setup_database_with_config(host, port, username, password, database_name="lesson_cancel_db"):
    """使用指定配置设置数据库"""
    print(f"🗄️  使用配置: {username}@{host}:{port}")
    
    # 1. 创建数据库
    print("   创建数据库...")
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
        print(f"   ✅ 数据库 '{database_name}' 创建成功")
        
        cursor.close()
        connection.close()
    except Exception as e:
        print(f"   ❌ 创建数据库失败: {e}")
        return False
    
    # 2. 更新配置文件
    print("   更新配置文件...")
    try:
        # 处理密码中的特殊字符
        encoded_password = quote_plus(password) if password else ""
        
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
        print("   ✅ 配置文件更新成功")
    except Exception as e:
        print(f"   ❌ 更新配置文件失败: {e}")
        return False
    
    # 3. 测试数据库连接
    print("   测试数据库连接...")
    try:
        from config import Config
        from models.user import db
        from app_complete import create_app
        
        app = create_app()
        with app.app_context():
            db.engine.execute('SELECT 1')
            print("   ✅ 数据库连接测试成功")
    except Exception as e:
        print(f"   ❌ 数据库连接测试失败: {e}")
        return False
    
    # 4. 初始化数据库表
    print("   初始化数据库表...")
    try:
        from app_complete import create_app, init_db
        
        app = create_app()
        with app.app_context():
            init_db()
            print("   ✅ 数据库表初始化成功")
    except Exception as e:
        print(f"   ❌ 数据库表初始化失败: {e}")
        return False
    
    return True

def main():
    """主函数"""
    print("🗄️  编译未来教培管理系统 - 智能数据库设置")
    print("=" * 60)
    
    # 检查PyMySQL
    try:
        import pymysql
    except ImportError:
        print("❌ 缺少PyMySQL依赖，正在安装...")
        os.system("pip install pymysql")
        import pymysql
    
    # 查找MySQL配置
    config = find_mysql_config()
    
    if not config:
        print("❌ 未找到可用的MySQL配置")
        print("请手动配置MySQL连接信息:")
        print("1. 确保MySQL服务已启动")
        print("2. 检查用户名和密码")
        print("3. 或者手动修改 auto_setup_db.py 中的密码")
        return False
    
    host, port, username, password = config
    
    # 设置数据库
    if setup_database_with_config(host, port, username, password):
        print()
        print("=" * 60)
        print("🎉 数据库设置完成！")
        print("=" * 60)
        print("📊 数据库信息:")
        print(f"   - 主机: {host}")
        print(f"   - 端口: {port}")
        print(f"   - 用户名: {username}")
        print(f"   - 密码: {'*' * len(password) if password else '无密码'}")
        print(f"   - 数据库: lesson_cancel_db")
        print("=" * 60)
        print("🚀 现在可以启动服务器了:")
        print("   python start_server.py")
        print("=" * 60)
        return True
    else:
        print("❌ 数据库设置失败")
        return False

if __name__ == '__main__':
    main() 