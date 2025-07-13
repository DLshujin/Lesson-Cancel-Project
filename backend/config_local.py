import os

class LocalConfig:
    SECRET_KEY = 'dev-secret-key-local'
    
    # 数据库配置 - 请根据你的MySQL设置修改
    # 格式：mysql+pymysql://用户名:密码@主机:端口/数据库名
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost/lesson_cancel_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 邮件配置
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'your-email@qq.com'
    MAIL_PASSWORD = 'your-smtp-password'
    
    # 分页配置
    POSTS_PER_PAGE = 20 