from flask import Flask, jsonify
from flask_login import LoginManager, login_required
from flask_cors import CORS
from models.user import db, User
from routes.auth import auth_bp
from routes.students import students_bp
from routes.courses import courses_bp
from routes.classrooms import classrooms_bp
from routes.schedules import schedules_bp
from routes.records import records_bp
import config

def create_app():
    app = Flask(__name__)
    
    # 配置
    app.config['SECRET_KEY'] = config.SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
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
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(students_bp, url_prefix='/api/students')
    app.register_blueprint(courses_bp, url_prefix='/api/courses')
    app.register_blueprint(classrooms_bp, url_prefix='/api/classrooms')
    app.register_blueprint(schedules_bp, url_prefix='/api/schedules')
    app.register_blueprint(records_bp, url_prefix='/api/records')
    
    # 根路由
    @app.route('/')
    def index():
        return jsonify({
            'message': '编译未来教培管理系统API',
            'version': '1.0.0',
            'endpoints': {
                'auth': '/api/auth',
                'students': '/api/students',
                'courses': '/api/courses',
                'classrooms': '/api/classrooms',
                'schedules': '/api/schedules',
                'records': '/api/records'
            }
        })
    
    # 健康检查
    @app.route('/health')
    def health():
        return jsonify({'status': 'healthy'})
    
    # 错误处理
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': '接口不存在'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': '服务器内部错误'}), 500
    
    return app

def init_db():
    """初始化数据库"""
    app = create_app()
    with app.app_context():
        db.create_all()
        print("数据库表创建成功")
        
        # 创建默认管理员用户
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                name='系统管理员',
                email='admin@example.com',
                role='admin'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("默认管理员用户创建成功: admin/admin123")

if __name__ == '__main__':
    app = create_app()
    
    # 初始化数据库
    with app.app_context():
        db.create_all()
    
    print("编译未来教培管理系统启动中...")
    print("API地址: http://localhost:5000")
    print("默认管理员: admin/admin123")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 