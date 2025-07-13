from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 模拟数据
users = [
    {'id': 1, 'username': 'admin', 'email': 'admin@example.com', 'role': 'admin'},
    {'id': 2, 'username': 'teacher', 'email': 'teacher@example.com', 'role': 'teacher'}
]

courses = [
    {'id': 1, 'name': 'Python编程', 'total_hours': 40, 'description': '零基础Python课程', 'status': 'active'},
    {'id': 2, 'name': 'Java开发', 'total_hours': 60, 'description': 'Java企业级开发', 'status': 'active'}
]

students = [
    {'id': 1, 'name': '张三', 'contact': '13800138001', 'email': 'zhangsan@example.com'},
    {'id': 2, 'name': '李四', 'contact': '13800138002', 'email': 'lisi@example.com'}
]

@app.route('/')
def index():
    return jsonify({'message': '编译未来教培管理系统API - 简化版本'})

@app.route('/api/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': '编译未来教培管理系统',
        'version': '1.0.0'
    })

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'error': '无效的请求数据'}), 400
    
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

@app.route('/api/courses', methods=['GET'])
def get_courses():
    return jsonify({
        'courses': courses,
        'total': len(courses),
        'message': '获取课程列表成功'
    })

@app.route('/api/courses', methods=['POST'])
def create_course():
    data = request.get_json()
    if not data:
        return jsonify({'error': '无效的请求数据'}), 400
    
    if not data.get('name'):
        return jsonify({'error': '课程名称不能为空'}), 400
    
    new_course = {
        'id': len(courses) + 1,
        'name': data.get('name'),
        'total_hours': data.get('total_hours', 0),
        'description': data.get('description', ''),
        'status': data.get('status', 'active')
    }
    courses.append(new_course)
    
    return jsonify({
        'message': '课程创建成功',
        'course': new_course
    }), 201

@app.route('/api/courses/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    course = next((c for c in courses if c['id'] == course_id), None)
    if not course:
        return jsonify({'error': '课程不存在'}), 404
    
    data = request.get_json()
    if data.get('name'):
        course['name'] = data['name']
    if data.get('total_hours') is not None:
        course['total_hours'] = data['total_hours']
    if data.get('description') is not None:
        course['description'] = data['description']
    if data.get('status') is not None:
        course['status'] = data['status']
    
    return jsonify({
        'message': '课程更新成功',
        'course': course
    })

@app.route('/api/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    global courses
    course = next((c for c in courses if c['id'] == course_id), None)
    if not course:
        return jsonify({'error': '课程不存在'}), 404
    
    courses = [c for c in courses if c['id'] != course_id]
    return jsonify({'message': '课程删除成功'})

@app.route('/api/students', methods=['GET'])
def get_students():
    return jsonify({
        'students': students,
        'total': len(students),
        'message': '获取学生列表成功'
    })

if __name__ == '__main__':
    print("=" * 50)
    print("🚀 编译未来教培管理系统 - 简化测试服务器")
    print("=" * 50)
    print("📝 测试账号:")
    print("   管理员: admin / admin123")
    print("   老师: teacher / teacher123")
    print("=" * 50)
    print("🌐 服务器地址: http://localhost:5000")
    print("📋 健康检查: http://localhost:5000/api/health")
    print("📋 课程列表: http://localhost:5000/api/courses")
    print("📋 学生列表: http://localhost:5000/api/students")
    print("=" * 50)
    print("🔄 启动服务器...")
    app.run(debug=True, host='0.0.0.0', port=5000) 