#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直接数据库初始化脚本
"""

import os
import sys
import pymysql
from urllib.parse import quote_plus

def create_database_direct():
    """直接创建数据库"""
    print("数据库初始化")
    print("=" * 50)
    
    # 数据库配置
    host = "localhost"
    port = 3306
    username = "root"
    password = "A123bc!@"  # 从配置文件中的密码
    database_name = "lesson_cancel_db"
    
    print(f"使用配置:")
    print(f"   - 主机: {host}")
    print(f"   - 端口: {port}")
    print(f"   - 用户名: {username}")
    print(f"   - 数据库: {database_name}")
    print()
    
    try:
        # 1. 连接MySQL（不指定数据库）
        print("连接MySQL...")
        connection = pymysql.connect(
            host=host,
            port=port,
            user=username,
            password=password,
            charset='utf8mb4'
        )
        print("MySQL连接成功")
        
        # 2. 创建数据库
        print("创建数据库...")
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{database_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print(f"数据库 '{database_name}' 创建成功")
        
        # 3. 切换到新创建的数据库
        cursor.execute(f"USE `{database_name}`")
        print(f"切换到数据库 '{database_name}'")
        
        # 4. 创建表结构
        print("创建数据表...")
        
        # 用户表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS `users` (
            `id` int NOT NULL AUTO_INCREMENT,
            `username` varchar(80) NOT NULL UNIQUE,
            `password_hash` varchar(255) NOT NULL,
            `name` varchar(100) NOT NULL,
            `email` varchar(120) UNIQUE,
            `role` varchar(20) DEFAULT 'staff',
            `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("   用户表创建成功")
        
        # 学生表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS `students` (
            `id` int NOT NULL AUTO_INCREMENT,
            `name` varchar(100) NOT NULL,
            `contact` varchar(50),
            `email` varchar(120),
            `remark` text,
            `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
            `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("   学生表创建成功")
        
        # 课程表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS `courses` (
            `id` int NOT NULL AUTO_INCREMENT,
            `name` varchar(100) NOT NULL,
            `description` text,
            `price` decimal(10,2) DEFAULT 0.00,
            `total_hours` int DEFAULT 0,
            `status` varchar(20) DEFAULT 'active',
            `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
            `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("   课程表创建成功")
        
        # 教室表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS `classrooms` (
            `id` int NOT NULL AUTO_INCREMENT,
            `name` varchar(100) NOT NULL,
            `capacity` int DEFAULT 30,
            `location` varchar(200),
            `equipment` text,
            `status` varchar(20) DEFAULT 'available',
            `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
            `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("   教室表创建成功")
        
        # 课程安排表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS `schedules` (
            `id` int NOT NULL AUTO_INCREMENT,
            `course_id` int NOT NULL,
            `classroom_id` int NOT NULL,
            `teacher_id` int NOT NULL,
            `start_time` datetime NOT NULL,
            `end_time` datetime NOT NULL,
            `max_students` int DEFAULT 30,
            `current_students` int DEFAULT 0,
            `status` varchar(20) DEFAULT 'scheduled',
            `notes` text,
            `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
            `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            PRIMARY KEY (`id`),
            FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`),
            FOREIGN KEY (`classroom_id`) REFERENCES `classrooms` (`id`),
            FOREIGN KEY (`teacher_id`) REFERENCES `users` (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("   课程安排表创建成功")
        
        # 消课记录表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS `records` (
            `id` int NOT NULL AUTO_INCREMENT,
            `student_id` int NOT NULL,
            `course_id` int NOT NULL,
            `schedule_id` int NOT NULL,
            `consumed_hours` float NOT NULL,
            `attendance_status` varchar(20) DEFAULT 'present',
            `notes` text,
            `created_by` int NOT NULL,
            `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
            `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            PRIMARY KEY (`id`),
            FOREIGN KEY (`student_id`) REFERENCES `students` (`id`),
            FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`),
            FOREIGN KEY (`schedule_id`) REFERENCES `schedules` (`id`),
            FOREIGN KEY (`created_by`) REFERENCES `users` (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("   消课记录表创建成功")
        
        # 5. 创建默认管理员用户
        print("创建默认管理员用户...")
        from werkzeug.security import generate_password_hash
        
        admin_password_hash = generate_password_hash('admin123')
        cursor.execute("""
        INSERT IGNORE INTO `users` (`username`, `password_hash`, `name`, `email`, `role`) 
        VALUES ('admin', %s, '系统管理员', 'admin@example.com', 'admin')
        """, (admin_password_hash,))
        
        if cursor.rowcount > 0:
            print("   默认管理员用户创建成功 (admin/admin123)")
        else:
            print("   默认管理员用户已存在")
        
        # 提交更改
        connection.commit()
        cursor.close()
        connection.close()
        
        print()
        print("=" * 50)
        print("数据库初始化完成！")
        print("=" * 50)
        print("数据库信息:")
        print(f"   - 数据库名: {database_name}")
        print(f"   - 字符集: utf8mb4")
        print(f"   - 表数量: 6个")
        print("=" * 50)
        print("默认用户:")
        print("   - 管理员: admin / admin123")
        print("=" * 50)
        print("现在可以启动服务器了:")
        print("   python start_server.py")
        print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"数据库初始化失败: {e}")
        return False

if __name__ == '__main__':
    create_database_direct() 