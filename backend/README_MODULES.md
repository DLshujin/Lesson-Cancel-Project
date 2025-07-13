# 编译未来教培管理系统 - 模块开发说明

## 概述

本文档说明已开发的各个模块功能和使用方法。

## 已开发模块

### 1. 认证模块 (Auth)
- **文件**: `routes/auth.py`
- **功能**: 用户注册、登录、获取用户信息、修改密码
- **特点**: 
  - 支持JWT Token认证
  - 密码加密存储
  - 角色权限管理

### 2. 学生管理模块 (Students)
- **文件**: `routes/students.py`
- **功能**: 学生信息的增删改查
- **特点**:
  - 支持分页查询
  - 支持姓名搜索
  - 完整的CRUD操作

### 3. 课程管理模块 (Courses)
- **文件**: `routes/courses.py`
- **功能**: 课程信息的增删改查
- **特点**:
  - 支持分页和搜索
  - 课程状态管理
  - 价格和课时管理

### 4. 教室管理模块 (Classrooms)
- **文件**: `routes/classrooms.py`
- **功能**: 教室信息的增删改查
- **特点**:
  - 教室容量管理
  - 设备信息记录
  - 教室状态管理（可用/维护中/占用中）
  - 获取可用教室列表

### 5. 课程安排模块 (Schedules)
- **文件**: `routes/schedules.py`
- **功能**: 课程安排的增删改查
- **特点**:
  - 时间冲突检测
  - 教室占用检查
  - 课程状态管理
  - 今日课程安排查询
  - 支持按课程、教室、教师筛选

### 6. 消课记录模块 (Records)
- **文件**: `routes/records.py`
- **功能**: 消课记录的增删改查
- **特点**:
  - 出勤状态管理
  - 课时消耗记录
  - 批量创建功能
  - 统计信息查询
  - 支持按学生、课程、课程安排筛选

## 数据模型

### 新增模型文件

1. **教室模型** (`models/classroom.py`)
   - 教室基本信息
   - 容量和设备管理
   - 状态管理

2. **课程安排模型** (`models/schedule.py`)
   - 课程安排信息
   - 时间管理
   - 关联关系

3. **消课记录模型** (`models/record.py`)
   - 消课记录信息
   - 出勤状态
   - 关联关系

## 启动方式

### 方式1: 使用启动脚本（推荐）
```bash
cd backend
python start_server.py
```

### 方式2: 直接启动
```bash
cd backend
python app_complete.py
```

### 方式3: 使用Flask命令
```bash
cd backend
export FLASK_APP=app_complete.py
flask run --host=0.0.0.0 --port=5000
```

## 测试方法

### 1. 运行完整测试
```bash
cd backend
python test_all_modules.py
```

### 2. 测试单个模块
```bash
# 测试课程管理
python test_courses_api.py

# 测试基础功能
python test_basic.py
```

### 3. 手动测试
使用Postman或curl测试各个API接口：

```bash
# 登录获取token
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'

# 创建学生
curl -X POST http://localhost:5000/api/students \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"name": "张三", "contact": "13800138000"}'
```

## API文档

详细的API文档请查看 `API_DOCUMENTATION.md` 文件，包含：
- 所有接口的详细说明
- 请求和响应格式
- 使用示例
- 错误处理

## 功能特点

### 1. 完整的CRUD操作
每个模块都支持完整的增删改查操作，并提供适当的错误处理。

### 2. 数据验证
- 必填字段验证
- 数据格式验证
- 业务逻辑验证（如时间冲突检查）

### 3. 关联关系管理
- 外键约束
- 级联删除检查
- 关联数据查询

### 4. 分页和搜索
- 支持分页查询
- 支持关键词搜索
- 支持多条件筛选

### 5. 统计功能
- 消课记录统计
- 出勤状态统计
- 今日数据统计

## 数据库设计

### 表结构
1. **users** - 用户表
2. **students** - 学生表
3. **courses** - 课程表
4. **classrooms** - 教室表
5. **schedules** - 课程安排表
6. **records** - 消课记录表

### 关联关系
- 课程安排关联课程、教室、教师
- 消课记录关联学生、课程、课程安排
- 所有表都有创建时间和更新时间

## 安全特性

1. **认证机制**: JWT Token认证
2. **密码加密**: 使用werkzeug.security加密
3. **输入验证**: 所有输入都进行验证
4. **SQL注入防护**: 使用SQLAlchemy ORM
5. **CORS支持**: 跨域请求支持

## 部署说明

### 开发环境
```bash
# 安装依赖
pip install -r requirements.txt

# 配置数据库
# 修改 config.py 中的数据库连接信息

# 启动服务器
python start_server.py
```

### 生产环境
```bash
# 使用Gunicorn启动
gunicorn -w 4 -b 0.0.0.0:5000 app_complete:create_app()

# 或使用uWSGI
uwsgi --ini uwsgi.ini
```

## 故障排除

### 常见问题

1. **数据库连接失败**
   - 检查数据库服务是否启动
   - 检查连接字符串是否正确
   - 检查用户名密码是否正确

2. **模块导入错误**
   - 确保在backend目录下运行
   - 检查Python路径设置
   - 确保所有依赖已安装

3. **端口被占用**
   - 修改端口号
   - 关闭占用端口的程序

4. **权限错误**
   - 检查文件权限
   - 确保有数据库操作权限

### 调试方法

1. **查看日志**
   - Flask debug模式会显示详细错误信息
   - 检查控制台输出

2. **数据库调试**
   ```python
   from app_complete import create_app
   from models.user import db
   
   app = create_app()
   with app.app_context():
       # 执行数据库操作
       pass
   ```

3. **API测试**
   - 使用Postman测试接口
   - 检查请求和响应格式

## 扩展开发

### 添加新模块
1. 创建模型文件 `models/new_module.py`
2. 创建路由文件 `routes/new_module.py`
3. 在 `app_complete.py` 中注册蓝图
4. 更新 `models/__init__.py`

### 添加新功能
1. 在现有路由文件中添加新的端点
2. 更新数据模型（如需要）
3. 添加相应的测试用例

## 联系信息

如有问题或建议，请联系开发团队。 