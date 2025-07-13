# 数据库模型包
from .user import User
from .student import Student
from .course import Course
from .classroom import Classroom
from .schedule import Schedule
from .record import Record

__all__ = ['User', 'Student', 'Course', 'Classroom', 'Schedule', 'Record'] 