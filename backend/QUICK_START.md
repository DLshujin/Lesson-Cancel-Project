# 编译未来教培管理系统 - 快速启动指南

## 🚀 5分钟快速启动

### 1. 环境准备
确保已安装Python 3.7+和MySQL数据库

### 2. 安装依赖
```bash
cd backend
pip install -r requirements.txt
```

### 3. 配置数据库
编辑 `config.py` 文件，修改数据库连接信息：
```python
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://用户名:密码@localhost:3306/数据库名'
```

### 4. 启动服务器
```bash
python start_server.py
```

### 5. 访问系统
- 系统地址: http://localhost:5000
- 默认管理员: admin / admin123

## 📋 功能模块

| 模块 | 功能 | API路径 |
|------|------|---------|
| 认证管理 | 用户登录、注册 | `/api/auth` |
| 学生管理 | 学生信息管理 | `/api/students` |
| 课程管理 | 课程信息管理 | `/api/courses` |
| 教室管理 | 教室信息管理 | `/api/classrooms` |
| 课程安排 | 课程排期管理 | `/api/schedules` |
| 消课记录 | 课时消耗记录 | `/api/records` |

## 🧪 测试功能

### 运行完整测试
```bash
python test_all_modules.py
```

### 测试单个模块
```bash
# 测试课程管理
python test_courses_api.py

# 测试基础功能
python test_basic.py
```

## 📖 详细文档

- [API文档](API_DOCUMENTATION.md) - 完整的API接口说明
- [模块说明](README_MODULES.md) - 各模块详细功能说明
- [项目README](../README.md) - 项目整体说明

## 🔧 常见问题

### Q: 数据库连接失败怎么办？
A: 检查MySQL服务是否启动，确认连接字符串中的用户名、密码、数据库名是否正确。

### Q: 端口5000被占用怎么办？
A: 修改 `app_complete.py` 中的端口号，或关闭占用端口的程序。

### Q: 模块导入错误怎么办？
A: 确保在backend目录下运行，检查Python路径和依赖安装。

### Q: 如何添加新功能？
A: 参考 `README_MODULES.md` 中的扩展开发说明。

## 📞 技术支持

如遇问题，请查看：
1. 控制台错误信息
2. 相关文档说明
3. 联系开发团队

---

**祝您使用愉快！** 🎉 