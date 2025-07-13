from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 模拟数据
users = [
    {'id': 1, 'username': 'admin', 'email': 'admin@example.com', 'role': 'admin'},
    {'id': 2, 'username': 'teacher', 'email': 'teacher@example.com', 'role': 'teacher'}
]

students = [
    {'id': 1, 'name': '张三', 'contact': '13800138001', 'email': 'zhangsan@example.com'},
    {'id': 2, 'name': '李四', 'contact': '13800138002', 'email': 'lisi@example.com'}
]

@app.route('/')
def index():
    return jsonify({'message': '编译未来教培管理系统API - 测试版本'})

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': '用户名和密码不能为空'}), 400
    
    # 简单的用户验证（测试用）
    if username == 'admin' and password == 'admin123':
        return jsonify({
            'message': '登录成功',
            'user': {'id': 1, 'username': 'admin', 'role': 'admin'}
        })
    elif username == 'teacher' and password == 'teacher123':
        return jsonify({
            'message': '登录成功',
            'user': {'id': 2, 'username': 'teacher', 'role': 'teacher'}
        })
    else:
        return jsonify({'error': '用户名或密码错误'}), 401

@app.route('/api/students', methods=['GET'])
def get_students():
    return jsonify({
        'students': students,
        'total': len(students),
        'message': '获取学生列表成功'
    })

@app.route('/api/students', methods=['POST'])
def create_student():
    data = request.get_json()
    if not data.get('name'):
        return jsonify({'error': '学生姓名不能为空'}), 400
    
    new_student = {
        'id': len(students) + 1,
        'name': data.get('name'),
        'contact': data.get('contact', ''),
        'email': data.get('email', '')
    }
    students.append(new_student)
    
    return jsonify({
        'message': '学生创建成功',
        'student': new_student
    }), 201

@app.route('/api/test')
def test():
    return jsonify({
        'status': 'success',
        'message': '后端API测试成功',
        'timestamp': '2024-01-01 12:00:00'
    })

if __name__ == '__main__':
    print("🚀 启动编译未来教培管理系统测试服务器...")
    print("📝 测试账号:")
    print("   管理员: admin / admin123")
    print("   老师: teacher / teacher123")
    print("🌐 服务器地址: http://localhost:5000")
    print("📋 API测试地址: http://localhost:5000/api/test")
    app.run(debug=True, host='0.0.0.0', port=5000) 