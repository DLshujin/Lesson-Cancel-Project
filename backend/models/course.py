from .user import db
from datetime import datetime

class Course(db.Model):
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, comment='课程名称')
    total_hours = db.Column(db.Integer, default=0, comment='总课时')
    description = db.Column(db.Text, comment='课程描述')
    status = db.Column(db.String(20), default='active', comment='状态：active/inactive')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联关系
    schedules = db.relationship('Schedule', backref='course', lazy=True)
    records = db.relationship('Record', backref='course', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'total_hours': self.total_hours,
            'description': self.description,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Course {self.name}>' 