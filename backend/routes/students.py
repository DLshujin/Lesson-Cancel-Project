from flask import Blueprint, request, jsonify
from flask_login import login_required
from models.student import Student
from models.user import db

students_bp = Blueprint('students', __name__)

@students_bp.route('/', methods=['GET'])
@login_required
def get_students():
    """获取学生列表"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search = request.args.get('search', '')
    
    query = Student.query
    
    if search:
        query = query.filter(Student.name.contains(search))
    
    students = query.paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'students': [student.to_dict() for student in students.items],
        'total': students.total,
        'pages': students.pages,
        'current_page': students.page
    })

@students_bp.route('/<int:student_id>', methods=['GET'])
@login_required
def get_student(student_id):
    """获取单个学生信息"""
    student = Student.query.get_or_404(student_id)
    return jsonify(student.to_dict())

@students_bp.route('/', methods=['POST'])
@login_required
def create_student():
    """创建新学生"""
    data = request.get_json()
    
    if not data.get('name'):
        return jsonify({'error': '学生姓名不能为空'}), 400
    
    student = Student(
        name=data.get('name'),
        contact=data.get('contact'),
        email=data.get('email'),
        remark=data.get('remark')
    )
    
    try:
        db.session.add(student)
        db.session.commit()
        return jsonify({
            'message': '学生创建成功',
            'student': student.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': '创建失败'}), 500

@students_bp.route('/<int:student_id>', methods=['PUT'])
@login_required
def update_student(student_id):
    """更新学生信息"""
    student = Student.query.get_or_404(student_id)
    data = request.get_json()
    
    if data.get('name'):
        student.name = data['name']
    if data.get('contact') is not None:
        student.contact = data['contact']
    if data.get('email') is not None:
        student.email = data['email']
    if data.get('remark') is not None:
        student.remark = data['remark']
    
    try:
        db.session.commit()
        return jsonify({
            'message': '学生信息更新成功',
            'student': student.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': '更新失败'}), 500

@students_bp.route('/<int:student_id>', methods=['DELETE'])
@login_required
def delete_student(student_id):
    """删除学生"""
    student = Student.query.get_or_404(student_id)
    
    try:
        db.session.delete(student)
        db.session.commit()
        return jsonify({'message': '学生删除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': '删除失败'}), 500 