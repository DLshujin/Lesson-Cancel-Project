import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    
    # 数据库配置 - 开发环境使用本地配置
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://root:A123bc%21%40@localhost/lesson_cancel_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 邮件配置
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'your-email@qq.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'your-smtp-password'
    
    # 分页配置
    POSTS_PER_PAGE = 20

# 为了兼容性，添加模块级别的属性
SECRET_KEY = Config.SECRET_KEY
SQLALCHEMY_DATABASE_URI = Config.SQLALCHEMY_DATABASE_URI
SQLALCHEMY_TRACK_MODIFICATIONS = Config.SQLALCHEMY_TRACK_MODIFICATIONS
MAIL_SERVER = Config.MAIL_SERVER
MAIL_PORT = Config.MAIL_PORT
MAIL_USE_TLS = Config.MAIL_USE_TLS
MAIL_USERNAME = Config.MAIL_USERNAME
MAIL_PASSWORD = Config.MAIL_PASSWORD
POSTS_PER_PAGE = Config.POSTS_PER_PAGE 