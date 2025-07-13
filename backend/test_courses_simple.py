import requests
import json

BASE_URL = "http://localhost:5000/api/courses"
LOGIN_URL = "http://localhost:5000/api/auth/login"

# 测试用账号
ADMIN = {"username": "admin", "password": "admin123"}

session = requests.Session()

def test_health():
    """测试服务器健康状态"""
    print("🔍 测试服务器健康状态...")
    try:
        response = requests.get("http://localhost:5000/api/health")
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ 服务器连接失败: {e}")
        return False

def test_login():
    """测试登录接口"""
    print("\n🔍 测试登录接口...")
    try:
        response = session.post(LOGIN_URL, json=ADMIN)
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ 登录失败: {e}")
        return False

def test_courses_endpoint():
    """测试课程接口"""
    print("\n🔍 测试课程接口...")
    try:
        response = session.get(BASE_URL + "/")
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ 课程接口测试失败: {e}")
        return False

def main():
    print("=" * 60)
    print("🧪 课程管理API简化测试")
    print("=" * 60)
    
    # 测试服务器状态
    if not test_health():
        print("\n❌ 服务器未启动或无法连接")
        print("请确保运行了: python app.py")
        return
    
    # 测试登录
    if not test_login():
        print("\n❌ 登录失败")
        return
    
    # 测试课程接口
    if not test_courses_endpoint():
        print("\n❌ 课程接口测试失败")
        return
    
    print("\n✅ 基础API测试通过！")
    print("服务器运行正常，可以进行进一步开发")

if __name__ == "__main__":
    main() 