from models.user import db
from datetime import datetime

class Record(db.Model):
    __tablename__ = 'records'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False, comment='学生ID')
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False, comment='课程ID')
    schedule_id = db.Column(db.Integer, db.ForeignKey('schedules.id'), nullable=False, comment='课程安排ID')
    consumed_hours = db.Column(db.Float, nullable=False, comment='消耗课时')
    attendance_status = db.Column(db.String(20), default='present', comment='出勤状态：present-出席，absent-缺席，late-迟到')
    notes = db.Column(db.Text, comment='备注')
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, comment='创建人ID')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联关系
    student = db.relationship('Student', backref='records')
    course = db.relationship('Course', backref='records')
    schedule = db.relationship('Schedule', backref='records')
    creator = db.relationship('User', backref='created_records')
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'student_name': self.student.name if self.student else None,
            'course_id': self.course_id,
            'course_name': self.course.name if self.course else None,
            'schedule_id': self.schedule_id,
            'schedule_info': f"{self.schedule.start_time.strftime('%Y-%m-%d %H:%M')} - {self.schedule.end_time.strftime('%H:%M')}" if self.schedule else None,
            'consumed_hours': self.consumed_hours,
            'attendance_status': self.attendance_status,
            'notes': self.notes,
            'created_by': self.created_by,
            'creator_name': self.creator.name if self.creator else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        } 