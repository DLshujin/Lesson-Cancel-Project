# 编译未来主后端入口
from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from models.user import db, User
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 初始化扩展
    db.init_app(app)
    CORS(app)
    
    # 初始化登录管理器
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # 注册蓝图
    from routes.auth import auth_bp
    from routes.students import students_bp
    from routes.courses import courses_bp
    from routes.classrooms import classrooms_bp
    from routes.schedules import schedules_bp
    from routes.records import records_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(students_bp, url_prefix='/api/students')
    app.register_blueprint(courses_bp, url_prefix='/api/courses')
    app.register_blueprint(classrooms_bp, url_prefix='/api/classrooms')
    app.register_blueprint(schedules_bp, url_prefix='/api/schedules')
    app.register_blueprint(records_bp, url_prefix='/api/records')
    
    # 根路由
    @app.route('/')
    def index():
        return {'message': '编译未来教培管理系统API'}
    
    return app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000) 