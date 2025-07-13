from flask import Blueprint, request, jsonify
from flask_login import login_required
from models.classroom import Classroom
from models.user import db

classrooms_bp = Blueprint('classrooms', __name__)

@classrooms_bp.route('/', methods=['GET'])
@login_required
def get_classrooms():
    """获取教室列表"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search = request.args.get('search', '')
    status = request.args.get('status', '')
    
    query = Classroom.query
    
    if search:
        query = query.filter(Classroom.name.contains(search))
    
    if status:
        query = query.filter(Classroom.status == status)
    
    classrooms = query.paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'classrooms': [classroom.to_dict() for classroom in classrooms.items],
        'total': classrooms.total,
        'pages': classrooms.pages,
        'current_page': classrooms.page
    })

@classrooms_bp.route('/<int:classroom_id>', methods=['GET'])
@login_required
def get_classroom(classroom_id):
    """获取单个教室信息"""
    classroom = Classroom.query.get_or_404(classroom_id)
    return jsonify(classroom.to_dict())

@classrooms_bp.route('/', methods=['POST'])
@login_required
def create_classroom():
    """创建新教室"""
    data = request.get_json()
    
    if not data.get('name'):
        return jsonify({'error': '教室名称不能为空'}), 400
    
    classroom = Classroom(
        name=data.get('name'),
        capacity=data.get('capacity', 30),
        location=data.get('location'),
        equipment=data.get('equipment'),
        status=data.get('status', 'available')
    )
    
    try:
        db.session.add(classroom)
        db.session.commit()
        return jsonify({
            'message': '教室创建成功',
            'classroom': classroom.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': '创建失败'}), 500

@classrooms_bp.route('/<int:classroom_id>', methods=['PUT'])
@login_required
def update_classroom(classroom_id):
    """更新教室信息"""
    classroom = Classroom.query.get_or_404(classroom_id)
    data = request.get_json()
    
    if data.get('name'):
        classroom.name = data['name']
    if data.get('capacity') is not None:
        classroom.capacity = data['capacity']
    if data.get('location') is not None:
        classroom.location = data['location']
    if data.get('equipment') is not None:
        classroom.equipment = data['equipment']
    if data.get('status') is not None:
        classroom.status = data['status']
    
    try:
        db.session.commit()
        return jsonify({
            'message': '教室信息更新成功',
            'classroom': classroom.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': '更新失败'}), 500

@classrooms_bp.route('/<int:classroom_id>', methods=['DELETE'])
@login_required
def delete_classroom(classroom_id):
    """删除教室"""
    classroom = Classroom.query.get_or_404(classroom_id)
    
    # 检查是否有相关的课程安排
    if classroom.schedules:
        return jsonify({'error': '该教室有相关的课程安排，无法删除'}), 400
    
    try:
        db.session.delete(classroom)
        db.session.commit()
        return jsonify({'message': '教室删除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': '删除失败'}), 500

@classrooms_bp.route('/available', methods=['GET'])
@login_required
def get_available_classrooms():
    """获取可用教室列表"""
    classrooms = Classroom.query.filter(Classroom.status == 'available').all()
    return jsonify({
        'classrooms': [classroom.to_dict() for classroom in classrooms]
    }) 