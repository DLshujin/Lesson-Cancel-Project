import requests
import json

# 服务器地址
BASE_URL = "http://localhost:5000"

def test_health_check():
    """测试健康检查接口"""
    print("🔍 测试健康检查接口...")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ 健康检查失败: {e}")
        return False

def test_login():
    """测试登录接口"""
    print("\n🔍 测试登录接口...")
    
    # 测试管理员登录
    print("测试管理员登录...")
    admin_data = {
        "username": "admin",
        "password": "admin123"
    }
    try:
        response = requests.post(f"{BASE_URL}/api/auth/login", json=admin_data)
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
    except Exception as e:
        print(f"❌ 管理员登录失败: {e}")
    
    # 测试老师登录
    print("\n测试老师登录...")
    teacher_data = {
        "username": "teacher",
        "password": "teacher123"
    }
    try:
        response = requests.post(f"{BASE_URL}/api/auth/login", json=teacher_data)
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
    except Exception as e:
        print(f"❌ 老师登录失败: {e}")

def test_students():
    """测试学生管理接口"""
    print("\n🔍 测试学生管理接口...")
    
    # 获取学生列表
    print("获取学生列表...")
    try:
        response = requests.get(f"{BASE_URL}/api/students")
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
    except Exception as e:
        print(f"❌ 获取学生列表失败: {e}")
    
    # 创建新学生
    print("\n创建新学生...")
    new_student = {
        "name": "王五",
        "contact": "13800138003",
        "email": "wangwu@example.com"
    }
    try:
        response = requests.post(f"{BASE_URL}/api/students", json=new_student)
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
    except Exception as e:
        print(f"❌ 创建学生失败: {e}")

def test_root():
    """测试根路径"""
    print("\n🔍 测试根路径...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
    except Exception as e:
        print(f"❌ 根路径测试失败: {e}")

def main():
    print("=" * 60)
    print("🧪 编译未来教培管理系统 - API测试")
    print("=" * 60)
    
    # 测试各个接口
    test_root()
    test_health_check()
    test_login()
    test_students()
    
    print("\n" + "=" * 60)
    print("✅ API测试完成")
    print("=" * 60)

if __name__ == "__main__":
    main() 