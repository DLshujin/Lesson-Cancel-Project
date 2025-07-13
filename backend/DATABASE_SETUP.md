# 数据库设置指南

## 🗄️ 数据库配置步骤

### 方法一：使用自动设置向导（推荐）

1. **运行设置向导**
   ```bash
   cd backend
   python setup_database.py
   ```

2. **按提示输入信息**
   - MySQL主机地址（默认：localhost）
   - MySQL端口（默认：3306）
   - MySQL用户名（默认：root）
   - MySQL密码
   - 数据库名称（默认：lesson_cancel_db）

3. **等待自动完成**
   - 检查MySQL连接
   - 创建数据库
   - 更新配置文件
   - 初始化数据表

### 方法二：手动配置

#### 1. 确保MySQL已安装并运行

**Windows:**
```bash
# 检查MySQL服务状态
net start mysql

# 或启动MySQL服务
net start mysql
```

**macOS/Linux:**
```bash
# 检查MySQL服务状态
sudo systemctl status mysql

# 启动MySQL服务
sudo systemctl start mysql
```

#### 2. 创建数据库

连接到MySQL并创建数据库：
```sql
mysql -u root -p

CREATE DATABASE lesson_cancel_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

#### 3. 修改配置文件

编辑 `backend/config.py` 文件：
```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    
    # 数据库配置 - 请修改为您的实际配置
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://用户名:密码@localhost:3306/lesson_cancel_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 邮件配置
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'your-email@qq.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'your-smtp-password'
    
    # 分页配置
    POSTS_PER_PAGE = 20
```

**重要：** 将 `用户名:密码` 替换为您的实际MySQL用户名和密码。

#### 4. 初始化数据库表

```bash
cd backend
python -c "
from app_complete import create_app, init_db
app = create_app()
with app.app_context():
    init_db()
    print('数据库表初始化成功')
"
```

## 🔧 常见问题解决

### 1. MySQL连接失败

**错误信息：** `Can't connect to MySQL server`

**解决方案：**
- 检查MySQL服务是否启动
- 确认主机地址和端口正确
- 验证用户名和密码

### 2. 权限错误

**错误信息：** `Access denied for user`

**解决方案：**
```sql
-- 登录MySQL
mysql -u root -p

-- 创建用户并授权
CREATE USER 'your_username'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON lesson_cancel_db.* TO 'your_username'@'localhost';
FLUSH PRIVILEGES;
```

### 3. 字符集问题

**错误信息：** `Incorrect string value`

**解决方案：**
确保数据库使用utf8mb4字符集：
```sql
ALTER DATABASE lesson_cancel_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 4. 密码包含特殊字符

如果MySQL密码包含特殊字符，需要进行URL编码：
```python
import urllib.parse

password = "your@password#123"
encoded_password = urllib.parse.quote_plus(password)
# 结果: your%40password%23123
```

## 📊 数据库表结构

系统会自动创建以下表：

1. **users** - 用户表
   - id, username, password_hash, name, email, role, created_at

2. **students** - 学生表
   - id, name, contact, email, remark, created_at

3. **courses** - 课程表
   - id, name, description, price, total_hours, status, created_at

4. **classrooms** - 教室表
   - id, name, capacity, location, equipment, status, created_at

5. **schedules** - 课程安排表
   - id, course_id, classroom_id, teacher_id, start_time, end_time, max_students, current_students, status, notes, created_at

6. **records** - 消课记录表
   - id, student_id, course_id, schedule_id, consumed_hours, attendance_status, notes, created_by, created_at

## 🧪 测试数据库连接

运行以下命令测试数据库连接：

```bash
cd backend
python -c "
from config import Config
from models.user import db
from app_complete import create_app

app = create_app()
with app.app_context():
    try:
        db.engine.execute('SELECT 1')
        print('✅ 数据库连接成功')
    except Exception as e:
        print(f'❌ 数据库连接失败: {e}')
"
```

## 🚀 启动系统

数据库配置完成后，启动系统：

```bash
cd backend
python start_server.py
```

访问 http://localhost:5000 查看系统是否正常运行。

## 📞 技术支持

如果遇到问题，请检查：

1. **MySQL服务状态**
2. **连接字符串格式**
3. **用户权限设置**
4. **字符集配置**
5. **防火墙设置**

---

**配置完成后，您就可以使用完整的教培管理系统了！** 🎉 