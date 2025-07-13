from flask import Blueprint, request, jsonify
from flask_login import login_required
from models.course import Course
from models.user import db

courses_bp = Blueprint('courses', __name__)

@courses_bp.route('/', methods=['GET'])
@login_required
def get_courses():
    """获取课程列表"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search = request.args.get('search', '')
    query = Course.query
    if search:
        query = query.filter(Course.name.contains(search))
    courses = query.paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        'courses': [course.to_dict() for course in courses.items],
        'total': courses.total,
        'pages': courses.pages,
        'current_page': courses.page
    })

@courses_bp.route('/<int:course_id>', methods=['GET'])
@login_required
def get_course(course_id):
    """获取单个课程信息"""
    course = Course.query.get_or_404(course_id)
    return jsonify(course.to_dict())

@courses_bp.route('/', methods=['POST'])
@login_required
def create_course():
    """创建新课程"""
    data = request.get_json()
    if not data.get('name'):
        return jsonify({'error': '课程名称不能为空'}), 400
    course = Course(
        name=data.get('name'),
        total_hours=data.get('total_hours', 0),
        description=data.get('description'),
        status=data.get('status', 'active')
    )
    try:
        db.session.add(course)
        db.session.commit()
        return jsonify({'message': '课程创建成功', 'course': course.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': '创建失败'}), 500

@courses_bp.route('/<int:course_id>', methods=['PUT'])
@login_required
def update_course(course_id):
    """更新课程信息"""
    course = Course.query.get_or_404(course_id)
    data = request.get_json()
    if data.get('name'):
        course.name = data['name']
    if data.get('total_hours') is not None:
        course.total_hours = data['total_hours']
    if data.get('description') is not None:
        course.description = data['description']
    if data.get('status') is not None:
        course.status = data['status']
    try:
        db.session.commit()
        return jsonify({'message': '课程信息更新成功', 'course': course.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': '更新失败'}), 500

@courses_bp.route('/<int:course_id>', methods=['DELETE'])
@login_required
def delete_course(course_id):
    """删除课程"""
    course = Course.query.get_or_404(course_id)
    try:
        db.session.delete(course)
        db.session.commit()
        return jsonify({'message': '课程删除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': '删除失败'}), 500 