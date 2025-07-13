#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的数据库初始化脚本
"""

import os
import sys

def init_database():
    """初始化数据库"""
    print("🗄️  初始化数据库...")
    
    try:
        # 导入必要的模块
        from app_complete import create_app, init_db
        
        # 创建应用
        app = create_app()
        
        # 在应用上下文中初始化数据库
        with app.app_context():
            print("   创建数据库表...")
            init_db()
            print("✅ 数据库初始化成功！")
            
            # 显示数据库信息
            from config import Config
            print(f"📊 数据库连接: {Config.SQLALCHEMY_DATABASE_URI}")
            
            return True
            
    except Exception as e:
        print(f"❌ 数据库初始化失败: {e}")
        print("请检查:")
        print("1. MySQL服务是否启动")
        print("2. 数据库连接配置是否正确")
        print("3. 用户名密码是否正确")
        return False

if __name__ == '__main__':
    init_database() 