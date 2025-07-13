import requests

BASE_URL = "http://localhost:5000/api/courses"
LOGIN_URL = "http://localhost:5000/api/auth/login"

# 测试用账号
ADMIN = {"username": "admin", "password": "admin123"}

session = requests.Session()

def login():
    print("[1] 登录管理员账号...")
    resp = session.post(LOGIN_URL, json=ADMIN)
    print("状态码:", resp.status_code)
    print("响应:", resp.json())
    assert resp.status_code == 200

def create_course():
    print("[2] 创建新课程...")
    data = {
        "name": "Python编程",
        "total_hours": 40,
        "description": "零基础Python课程",
        "status": "active"
    }
    resp = session.post(BASE_URL + "/", json=data)
    print("状态码:", resp.status_code)
    print("响应:", resp.json())
    assert resp.status_code == 201
    return resp.json()["course"]["id"]

def get_courses():
    print("[3] 获取课程列表...")
    resp = session.get(BASE_URL + "/")
    print("状态码:", resp.status_code)
    print("响应:", resp.json())
    assert resp.status_code == 200
    return resp.json()["courses"]

def update_course(course_id):
    print("[4] 更新课程...")
    data = {
        "name": "Python进阶",
        "total_hours": 60,
        "description": "进阶Python课程",
        "status": "active"
    }
    resp = session.put(f"{BASE_URL}/{course_id}", json=data)
    print("状态码:", resp.status_code)
    print("响应:", resp.json())
    assert resp.status_code == 200

def get_course(course_id):
    print("[5] 获取单个课程...")
    resp = session.get(f"{BASE_URL}/{course_id}")
    print("状态码:", resp.status_code)
    print("响应:", resp.json())
    assert resp.status_code == 200

def delete_course(course_id):
    print("[6] 删除课程...")
    resp = session.delete(f"{BASE_URL}/{course_id}")
    print("状态码:", resp.status_code)
    print("响应:", resp.json())
    assert resp.status_code == 200

def main():
    print("\n===== 课程管理API自动化测试 =====\n")
    login()
    course_id = create_course()
    get_courses()
    update_course(course_id)
    get_course(course_id)
    delete_course(course_id)
    print("\n✅ 课程管理API测试全部通过！")

if __name__ == "__main__":
    main() 