#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
编译未来教培管理系统 - 完整模块测试脚本
测试所有模块的API功能
"""

import requests
import json
import time
from datetime import datetime, timedelta

# 配置
BASE_URL = 'http://localhost:5000/api'
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin123'

class APITester:
    def __init__(self):
        self.session = requests.Session()
        self.token = None
        self.test_data = {}
    
    def login(self):
        """登录获取token"""
        print("🔐 正在登录...")
        try:
            response = self.session.post(f'{BASE_URL}/auth/login', json={
                'username': ADMIN_USERNAME,
                'password': ADMIN_PASSWORD
            })
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get('token')
                print(f"✅ 登录成功，用户: {data.get('user', {}).get('name')}")
                return True
            else:
                print(f"❌ 登录失败: {response.text}")
                return False
        except Exception as e:
            print(f"❌ 登录异常: {e}")
            return False
    
    def test_auth(self):
        """测试认证模块"""
        print("\n🔐 测试认证模块...")
        
        # 测试注册
        print("  - 测试用户注册...")
        response = self.session.post(f'{BASE_URL}/auth/register', json={
            'username': 'testuser',
            'password': 'test123',
            'name': '测试用户',
            'email': 'test@example.com',
            'role': 'teacher'
        })
        print(f"    注册结果: {response.status_code} - {response.json()}")
        
        # 测试登录
        print("  - 测试用户登录...")
        response = self.session.post(f'{BASE_URL}/auth/login', json={
            'username': 'testuser',
            'password': 'test123'
        })
        print(f"    登录结果: {response.status_code} - {response.json()}")
        
        # 测试获取用户信息
        if self.token:
            print("  - 测试获取用户信息...")
            headers = {'Authorization': f'Bearer {self.token}'}
            response = self.session.get(f'{BASE_URL}/auth/profile', headers=headers)
            print(f"    用户信息: {response.status_code} - {response.json()}")
    
    def test_students(self):
        """测试学生管理模块"""
        print("\n👨‍🎓 测试学生管理模块...")
        
        headers = {'Authorization': f'Bearer {self.token}'} if self.token else {}
        
        # 创建学生
        print("  - 创建学生...")
        student_data = {
            'name': '张三',
            'contact': '13800138000',
            'email': 'zhangsan@example.com',
            'remark': '测试学生'
        }
        response = self.session.post(f'{BASE_URL}/students', json=student_data, headers=headers)
        if response.status_code == 201:
            student = response.json()['student']
            self.test_data['student_id'] = student['id']
            print(f"    ✅ 学生创建成功: {student['name']}")
        else:
            print(f"    ❌ 学生创建失败: {response.text}")
        
        # 获取学生列表
        print("  - 获取学生列表...")
        response = self.session.get(f'{BASE_URL}/students', headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"    ✅ 获取到 {data['total']} 个学生")
        else:
            print(f"    ❌ 获取学生列表失败: {response.text}")
        
        # 获取单个学生
        if self.test_data.get('student_id'):
            print("  - 获取单个学生信息...")
            response = self.session.get(f'{BASE_URL}/students/{self.test_data["student_id"]}', headers=headers)
            if response.status_code == 200:
                student = response.json()
                print(f"    ✅ 学生信息: {student['name']}")
            else:
                print(f"    ❌ 获取学生信息失败: {response.text}")
    
    def test_courses(self):
        """测试课程管理模块"""
        print("\n📚 测试课程管理模块...")
        
        headers = {'Authorization': f'Bearer {self.token}'} if self.token else {}
        
        # 创建课程
        print("  - 创建课程...")
        course_data = {
            'name': 'Python编程基础',
            'description': 'Python编程入门课程',
            'price': 299.00,
            'total_hours': 20,
            'status': 'active'
        }
        response = self.session.post(f'{BASE_URL}/courses', json=course_data, headers=headers)
        if response.status_code == 201:
            course = response.json()['course']
            self.test_data['course_id'] = course['id']
            print(f"    ✅ 课程创建成功: {course['name']}")
        else:
            print(f"    ❌ 课程创建失败: {response.text}")
        
        # 获取课程列表
        print("  - 获取课程列表...")
        response = self.session.get(f'{BASE_URL}/courses', headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"    ✅ 获取到 {data['total']} 个课程")
        else:
            print(f"    ❌ 获取课程列表失败: {response.text}")
    
    def test_classrooms(self):
        """测试教室管理模块"""
        print("\n🏫 测试教室管理模块...")
        
        headers = {'Authorization': f'Bearer {self.token}'} if self.token else {}
        
        # 创建教室
        print("  - 创建教室...")
        classroom_data = {
            'name': 'A101',
            'capacity': 30,
            'location': '一楼A区',
            'equipment': '投影仪、白板、空调',
            'status': 'available'
        }
        response = self.session.post(f'{BASE_URL}/classrooms', json=classroom_data, headers=headers)
        if response.status_code == 201:
            classroom = response.json()['classroom']
            self.test_data['classroom_id'] = classroom['id']
            print(f"    ✅ 教室创建成功: {classroom['name']}")
        else:
            print(f"    ❌ 教室创建失败: {response.text}")
        
        # 获取可用教室
        print("  - 获取可用教室...")
        response = self.session.get(f'{BASE_URL}/classrooms/available', headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"    ✅ 获取到 {len(data['classrooms'])} 个可用教室")
        else:
            print(f"    ❌ 获取可用教室失败: {response.text}")
    
    def test_schedules(self):
        """测试课程安排模块"""
        print("\n📅 测试课程安排模块...")
        
        headers = {'Authorization': f'Bearer {self.token}'} if self.token else {}
        
        if not all(key in self.test_data for key in ['course_id', 'classroom_id']):
            print("    ⚠️  跳过课程安排测试，缺少必要数据")
            return
        
        # 创建课程安排
        print("  - 创建课程安排...")
        start_time = datetime.now() + timedelta(days=1)
        end_time = start_time + timedelta(hours=2)
        
        schedule_data = {
            'course_id': self.test_data['course_id'],
            'classroom_id': self.test_data['classroom_id'],
            'teacher_id': 1,  # 假设管理员是教师
            'start_time': start_time.isoformat(),
            'end_time': end_time.isoformat(),
            'max_students': 25,
            'notes': '测试课程安排'
        }
        response = self.session.post(f'{BASE_URL}/schedules', json=schedule_data, headers=headers)
        if response.status_code == 201:
            schedule = response.json()['schedule']
            self.test_data['schedule_id'] = schedule['id']
            print(f"    ✅ 课程安排创建成功: {schedule['id']}")
        else:
            print(f"    ❌ 课程安排创建失败: {response.text}")
        
        # 获取今日课程安排
        print("  - 获取今日课程安排...")
        response = self.session.get(f'{BASE_URL}/schedules/today', headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"    ✅ 今日有 {len(data['schedules'])} 个课程安排")
        else:
            print(f"    ❌ 获取今日课程安排失败: {response.text}")
    
    def test_records(self):
        """测试消课记录模块"""
        print("\n📝 测试消课记录模块...")
        
        headers = {'Authorization': f'Bearer {self.token}'} if self.token else {}
        
        if not all(key in self.test_data for key in ['student_id', 'course_id', 'schedule_id']):
            print("    ⚠️  跳过消课记录测试，缺少必要数据")
            return
        
        # 创建消课记录
        print("  - 创建消课记录...")
        record_data = {
            'student_id': self.test_data['student_id'],
            'course_id': self.test_data['course_id'],
            'schedule_id': self.test_data['schedule_id'],
            'consumed_hours': 2.0,
            'attendance_status': 'present',
            'notes': '测试消课记录'
        }
        response = self.session.post(f'{BASE_URL}/records', json=record_data, headers=headers)
        if response.status_code == 201:
            record = response.json()['record']
            self.test_data['record_id'] = record['id']
            print(f"    ✅ 消课记录创建成功: {record['id']}")
        else:
            print(f"    ❌ 消课记录创建失败: {response.text}")
        
        # 获取消课记录统计
        print("  - 获取消课记录统计...")
        response = self.session.get(f'{BASE_URL}/records/statistics', headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"    ✅ 统计信息: 总记录{data['total_records']}条，总课时{data['total_hours']}小时")
        else:
            print(f"    ❌ 获取统计信息失败: {response.text}")
    
    def run_all_tests(self):
        """运行所有测试"""
        print("🚀 开始测试编译未来教培管理系统所有模块...")
        print("=" * 60)
        
        # 登录
        if not self.login():
            print("❌ 登录失败，无法继续测试")
            return
        
        # 测试各个模块
        self.test_auth()
        self.test_students()
        self.test_courses()
        self.test_classrooms()
        self.test_schedules()
        self.test_records()
        
        print("\n" + "=" * 60)
        print("🎉 所有模块测试完成！")
        print(f"📊 测试数据: {json.dumps(self.test_data, indent=2, ensure_ascii=False)}")

def main():
    """主函数"""
    print("编译未来教培管理系统 - 完整模块测试")
    print("请确保后端服务器正在运行: python app_complete.py")
    
    # 检查服务器是否运行
    try:
        response = requests.get('http://localhost:5000/health', timeout=5)
        if response.status_code != 200:
            print("❌ 服务器未正常运行，请先启动后端服务器")
            return
    except:
        print("❌ 无法连接到服务器，请确保后端服务器正在运行")
        print("启动命令: python app_complete.py")
        return
    
    # 运行测试
    tester = APITester()
    tester.run_all_tests()

if __name__ == '__main__':
    main() 