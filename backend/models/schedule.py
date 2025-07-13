from models.user import db
from datetime import datetime

class Schedule(db.Model):
    __tablename__ = 'schedules'
    
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False, comment='课程ID')
    classroom_id = db.Column(db.Integer, db.ForeignKey('classrooms.id'), nullable=False, comment='教室ID')
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, comment='教师ID')
    start_time = db.Column(db.DateTime, nullable=False, comment='开始时间')
    end_time = db.Column(db.DateTime, nullable=False, comment='结束时间')
    max_students = db.Column(db.Integer, default=30, comment='最大学生数')
    current_students = db.Column(db.Integer, default=0, comment='当前学生数')
    status = db.Column(db.String(20), default='scheduled', comment='状态：scheduled-已安排，ongoing-进行中，completed-已完成，cancelled-已取消')
    notes = db.Column(db.Text, comment='备注')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联关系
    course = db.relationship('Course', backref='schedules')
    classroom = db.relationship('Classroom', backref='schedules')
    teacher = db.relationship('User', backref='teaching_schedules')
    
    def to_dict(self):
        return {
            'id': self.id,
            'course_id': self.course_id,
            'course_name': self.course.name if self.course else None,
            'classroom_id': self.classroom_id,
            'classroom_name': self.classroom.name if self.classroom else None,
            'teacher_id': self.teacher_id,
            'teacher_name': self.teacher.name if self.teacher else None,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'max_students': self.max_students,
            'current_students': self.current_students,
            'status': self.status,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        } 