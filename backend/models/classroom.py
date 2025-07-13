from models.user import db
from datetime import datetime

class Classroom(db.Model):
    __tablename__ = 'classrooms'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, comment='教室名称')
    capacity = db.Column(db.Integer, default=30, comment='容纳人数')
    location = db.Column(db.String(200), comment='教室位置')
    equipment = db.Column(db.Text, comment='设备信息')
    status = db.Column(db.String(20), default='available', comment='状态：available-可用，maintenance-维护中，occupied-占用中')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'capacity': self.capacity,
            'location': self.location,
            'equipment': self.equipment,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        } 