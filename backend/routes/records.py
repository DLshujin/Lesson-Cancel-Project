from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models.record import Record
from models.student import Student
from models.course import Course
from models.schedule import Schedule
from models.user import db
from datetime import datetime

records_bp = Blueprint('records', __name__)

@records_bp.route('/', methods=['GET'])
@login_required
def get_records():
    """获取消课记录列表"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    student_id = request.args.get('student_id', type=int)
    course_id = request.args.get('course_id', type=int)
    schedule_id = request.args.get('schedule_id', type=int)
    attendance_status = request.args.get('attendance_status', '')
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')
    
    query = Record.query
    
    if student_id:
        query = query.filter(Record.student_id == student_id)
    if course_id:
        query = query.filter(Record.course_id == course_id)
    if schedule_id:
        query = query.filter(Record.schedule_id == schedule_id)
    if attendance_status:
        query = query.filter(Record.attendance_status == attendance_status)
    if date_from:
        try:
            date_from_obj = datetime.fromisoformat(date_from)
            query = query.filter(Record.created_at >= date_from_obj)
        except:
            pass
    if date_to:
        try:
            date_to_obj = datetime.fromisoformat(date_to)
            query = query.filter(Record.created_at <= date_to_obj)
        except:
            pass
    
    # 按创建时间倒序排列
    query = query.order_by(Record.created_at.desc())
    
    records = query.paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'records': [record.to_dict() for record in records.items],
        'total': records.total,
        'pages': records.pages,
        'current_page': records.page
    })

@records_bp.route('/<int:record_id>', methods=['GET'])
@login_required
def get_record(record_id):
    """获取单个消课记录信息"""
    record = Record.query.get_or_404(record_id)
    return jsonify(record.to_dict())

@records_bp.route('/', methods=['POST'])
@login_required
def create_record():
    """创建新消课记录"""
    data = request.get_json()
    
    # 验证必填字段
    required_fields = ['student_id', 'course_id', 'schedule_id', 'consumed_hours']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'{field}不能为空'}), 400
    
    # 验证学生是否存在
    student = Student.query.get(data['student_id'])
    if not student:
        return jsonify({'error': '学生不存在'}), 400
    
    # 验证课程是否存在
    course = Course.query.get(data['course_id'])
    if not course:
        return jsonify({'error': '课程不存在'}), 400
    
    # 验证课程安排是否存在
    schedule = Schedule.query.get(data['schedule_id'])
    if not schedule:
        return jsonify({'error': '课程安排不存在'}), 400
    
    # 验证课时消耗
    if data['consumed_hours'] <= 0:
        return jsonify({'error': '消耗课时必须大于0'}), 400
    
    # 检查是否已存在相同的消课记录
    existing_record = Record.query.filter(
        Record.student_id == data['student_id'],
        Record.schedule_id == data['schedule_id']
    ).first()
    
    if existing_record:
        return jsonify({'error': '该学生在此课程安排中已有消课记录'}), 400
    
    record = Record(
        student_id=data['student_id'],
        course_id=data['course_id'],
        schedule_id=data['schedule_id'],
        consumed_hours=data['consumed_hours'],
        attendance_status=data.get('attendance_status', 'present'),
        notes=data.get('notes'),
        created_by=current_user.id
    )
    
    try:
        db.session.add(record)
        db.session.commit()
        return jsonify({
            'message': '消课记录创建成功',
            'record': record.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': '创建失败'}), 500

@records_bp.route('/<int:record_id>', methods=['PUT'])
@login_required
def update_record(record_id):
    """更新消课记录"""
    record = Record.query.get_or_404(record_id)
    data = request.get_json()
    
    # 更新字段
    if data.get('consumed_hours') is not None:
        if data['consumed_hours'] <= 0:
            return jsonify({'error': '消耗课时必须大于0'}), 400
        record.consumed_hours = data['consumed_hours']
    
    if data.get('attendance_status') is not None:
        valid_statuses = ['present', 'absent', 'late']
        if data['attendance_status'] not in valid_statuses:
            return jsonify({'error': '无效的出勤状态'}), 400
        record.attendance_status = data['attendance_status']
    
    if data.get('notes') is not None:
        record.notes = data['notes']
    
    try:
        db.session.commit()
        return jsonify({
            'message': '消课记录更新成功',
            'record': record.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': '更新失败'}), 500

@records_bp.route('/<int:record_id>', methods=['DELETE'])
@login_required
def delete_record(record_id):
    """删除消课记录"""
    record = Record.query.get_or_404(record_id)
    
    try:
        db.session.delete(record)
        db.session.commit()
        return jsonify({'message': '消课记录删除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': '删除失败'}), 500

@records_bp.route('/student/<int:student_id>', methods=['GET'])
@login_required
def get_student_records(student_id):
    """获取指定学生的消课记录"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    query = Record.query.filter(Record.student_id == student_id)
    query = query.order_by(Record.created_at.desc())
    
    records = query.paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'records': [record.to_dict() for record in records.items],
        'total': records.total,
        'pages': records.pages,
        'current_page': records.page
    })

@records_bp.route('/course/<int:course_id>', methods=['GET'])
@login_required
def get_course_records(course_id):
    """获取指定课程的消课记录"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    query = Record.query.filter(Record.course_id == course_id)
    query = query.order_by(Record.created_at.desc())
    
    records = query.paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'records': [record.to_dict() for record in records.items],
        'total': records.total,
        'pages': records.pages,
        'current_page': records.page
    })

@records_bp.route('/schedule/<int:schedule_id>', methods=['GET'])
@login_required
def get_schedule_records(schedule_id):
    """获取指定课程安排的消课记录"""
    records = Record.query.filter(Record.schedule_id == schedule_id).all()
    
    return jsonify({
        'records': [record.to_dict() for record in records]
    })

@records_bp.route('/batch', methods=['POST'])
@login_required
def create_batch_records():
    """批量创建消课记录"""
    data = request.get_json()
    
    if not data.get('records') or not isinstance(data['records'], list):
        return jsonify({'error': 'records字段必须是数组'}), 400
    
    created_records = []
    errors = []
    
    for i, record_data in enumerate(data['records']):
        try:
            # 验证必填字段
            required_fields = ['student_id', 'course_id', 'schedule_id', 'consumed_hours']
            for field in required_fields:
                if not record_data.get(field):
                    errors.append(f'第{i+1}条记录: {field}不能为空')
                    continue
            
            # 检查是否已存在相同的消课记录
            existing_record = Record.query.filter(
                Record.student_id == record_data['student_id'],
                Record.schedule_id == record_data['schedule_id']
            ).first()
            
            if existing_record:
                errors.append(f'第{i+1}条记录: 该学生在此课程安排中已有消课记录')
                continue
            
            record = Record(
                student_id=record_data['student_id'],
                course_id=record_data['course_id'],
                schedule_id=record_data['schedule_id'],
                consumed_hours=record_data['consumed_hours'],
                attendance_status=record_data.get('attendance_status', 'present'),
                notes=record_data.get('notes'),
                created_by=current_user.id
            )
            
            db.session.add(record)
            created_records.append(record)
            
        except Exception as e:
            errors.append(f'第{i+1}条记录: {str(e)}')
    
    if errors:
        db.session.rollback()
        return jsonify({'error': '批量创建失败', 'details': errors}), 400
    
    try:
        db.session.commit()
        return jsonify({
            'message': f'成功创建{len(created_records)}条消课记录',
            'records': [record.to_dict() for record in created_records]
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': '批量创建失败'}), 500

@records_bp.route('/statistics', methods=['GET'])
@login_required
def get_records_statistics():
    """获取消课记录统计信息"""
    # 总消课记录数
    total_records = Record.query.count()
    
    # 今日消课记录数
    today = datetime.now().date()
    today_records = Record.query.filter(
        db.func.date(Record.created_at) == today
    ).count()
    
    # 各出勤状态统计
    attendance_stats = db.session.query(
        Record.attendance_status,
        db.func.count(Record.id)
    ).group_by(Record.attendance_status).all()
    
    # 总消耗课时
    total_hours = db.session.query(db.func.sum(Record.consumed_hours)).scalar() or 0
    
    return jsonify({
        'total_records': total_records,
        'today_records': today_records,
        'total_hours': float(total_hours),
        'attendance_stats': dict(attendance_stats)
    }) 