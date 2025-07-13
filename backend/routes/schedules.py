from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models.schedule import Schedule
from models.course import Course
from models.classroom import Classroom
from models.user import db
from datetime import datetime

schedules_bp = Blueprint('schedules', __name__)

@schedules_bp.route('/', methods=['GET'])
@login_required
def get_schedules():
    """获取课程安排列表"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    course_id = request.args.get('course_id', type=int)
    classroom_id = request.args.get('classroom_id', type=int)
    teacher_id = request.args.get('teacher_id', type=int)
    status = request.args.get('status', '')
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')
    
    query = Schedule.query
    
    if course_id:
        query = query.filter(Schedule.course_id == course_id)
    if classroom_id:
        query = query.filter(Schedule.classroom_id == classroom_id)
    if teacher_id:
        query = query.filter(Schedule.teacher_id == teacher_id)
    if status:
        query = query.filter(Schedule.status == status)
    if date_from:
        try:
            date_from_obj = datetime.fromisoformat(date_from)
            query = query.filter(Schedule.start_time >= date_from_obj)
        except:
            pass
    if date_to:
        try:
            date_to_obj = datetime.fromisoformat(date_to)
            query = query.filter(Schedule.end_time <= date_to_obj)
        except:
            pass
    
    # 按开始时间排序
    query = query.order_by(Schedule.start_time.desc())
    
    schedules = query.paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'schedules': [schedule.to_dict() for schedule in schedules.items],
        'total': schedules.total,
        'pages': schedules.pages,
        'current_page': schedules.page
    })

@schedules_bp.route('/<int:schedule_id>', methods=['GET'])
@login_required
def get_schedule(schedule_id):
    """获取单个课程安排信息"""
    schedule = Schedule.query.get_or_404(schedule_id)
    return jsonify(schedule.to_dict())

@schedules_bp.route('/', methods=['POST'])
@login_required
def create_schedule():
    """创建新课程安排"""
    data = request.get_json()
    
    # 验证必填字段
    required_fields = ['course_id', 'classroom_id', 'teacher_id', 'start_time', 'end_time']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'{field}不能为空'}), 400
    
    # 验证时间格式
    try:
        start_time = datetime.fromisoformat(data['start_time'])
        end_time = datetime.fromisoformat(data['end_time'])
    except:
        return jsonify({'error': '时间格式错误'}), 400
    
    # 验证时间逻辑
    if start_time >= end_time:
        return jsonify({'error': '开始时间必须早于结束时间'}), 400
    
    # 检查教室是否可用
    classroom = Classroom.query.get(data['classroom_id'])
    if not classroom or classroom.status != 'available':
        return jsonify({'error': '教室不可用'}), 400
    
    # 检查时间冲突
    conflict = Schedule.query.filter(
        Schedule.classroom_id == data['classroom_id'],
        Schedule.status.in_(['scheduled', 'ongoing']),
        ((Schedule.start_time <= start_time) & (Schedule.end_time > start_time)) |
        ((Schedule.start_time < end_time) & (Schedule.end_time >= end_time)) |
        ((Schedule.start_time >= start_time) & (Schedule.end_time <= end_time))
    ).first()
    
    if conflict:
        return jsonify({'error': '该时间段教室已被占用'}), 400
    
    schedule = Schedule(
        course_id=data['course_id'],
        classroom_id=data['classroom_id'],
        teacher_id=data['teacher_id'],
        start_time=start_time,
        end_time=end_time,
        max_students=data.get('max_students', 30),
        notes=data.get('notes')
    )
    
    try:
        db.session.add(schedule)
        db.session.commit()
        return jsonify({
            'message': '课程安排创建成功',
            'schedule': schedule.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': '创建失败'}), 500

@schedules_bp.route('/<int:schedule_id>', methods=['PUT'])
@login_required
def update_schedule(schedule_id):
    """更新课程安排"""
    schedule = Schedule.query.get_or_404(schedule_id)
    data = request.get_json()
    
    # 如果修改了时间，需要检查冲突
    if data.get('start_time') or data.get('end_time'):
        start_time = datetime.fromisoformat(data['start_time']) if data.get('start_time') else schedule.start_time
        end_time = datetime.fromisoformat(data['end_time']) if data.get('end_time') else schedule.end_time
        
        if start_time >= end_time:
            return jsonify({'error': '开始时间必须早于结束时间'}), 400
        
        # 检查时间冲突（排除自己）
        conflict = Schedule.query.filter(
            Schedule.id != schedule_id,
            Schedule.classroom_id == (data.get('classroom_id') or schedule.classroom_id),
            Schedule.status.in_(['scheduled', 'ongoing']),
            ((Schedule.start_time <= start_time) & (Schedule.end_time > start_time)) |
            ((Schedule.start_time < end_time) & (Schedule.end_time >= end_time)) |
            ((Schedule.start_time >= start_time) & (Schedule.end_time <= end_time))
        ).first()
        
        if conflict:
            return jsonify({'error': '该时间段教室已被占用'}), 400
    
    # 更新字段
    if data.get('course_id'):
        schedule.course_id = data['course_id']
    if data.get('classroom_id'):
        schedule.classroom_id = data['classroom_id']
    if data.get('teacher_id'):
        schedule.teacher_id = data['teacher_id']
    if data.get('start_time'):
        schedule.start_time = datetime.fromisoformat(data['start_time'])
    if data.get('end_time'):
        schedule.end_time = datetime.fromisoformat(data['end_time'])
    if data.get('max_students') is not None:
        schedule.max_students = data['max_students']
    if data.get('status') is not None:
        schedule.status = data['status']
    if data.get('notes') is not None:
        schedule.notes = data['notes']
    
    try:
        db.session.commit()
        return jsonify({
            'message': '课程安排更新成功',
            'schedule': schedule.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': '更新失败'}), 500

@schedules_bp.route('/<int:schedule_id>', methods=['DELETE'])
@login_required
def delete_schedule(schedule_id):
    """删除课程安排"""
    schedule = Schedule.query.get_or_404(schedule_id)
    
    # 检查是否可以删除
    if schedule.status in ['ongoing', 'completed']:
        return jsonify({'error': '进行中或已完成的课程安排无法删除'}), 400
    
    try:
        db.session.delete(schedule)
        db.session.commit()
        return jsonify({'message': '课程安排删除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': '删除失败'}), 500

@schedules_bp.route('/today', methods=['GET'])
@login_required
def get_today_schedules():
    """获取今日课程安排"""
    today = datetime.now().date()
    schedules = Schedule.query.filter(
        db.func.date(Schedule.start_time) == today
    ).order_by(Schedule.start_time).all()
    
    return jsonify({
        'schedules': [schedule.to_dict() for schedule in schedules]
    })

@schedules_bp.route('/<int:schedule_id>/status', methods=['PUT'])
@login_required
def update_schedule_status(schedule_id):
    """更新课程安排状态"""
    schedule = Schedule.query.get_or_404(schedule_id)
    data = request.get_json()
    
    if not data.get('status'):
        return jsonify({'error': '状态不能为空'}), 400
    
    valid_statuses = ['scheduled', 'ongoing', 'completed', 'cancelled']
    if data['status'] not in valid_statuses:
        return jsonify({'error': '无效的状态'}), 400
    
    schedule.status = data['status']
    
    try:
        db.session.commit()
        return jsonify({
            'message': '状态更新成功',
            'schedule': schedule.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': '更新失败'}), 500 