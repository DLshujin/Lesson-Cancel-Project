# 编译未来教培管理系统

## 一、项目简介
编译未来是一款专注于教培机构/学校**消课、排课、邮件提醒**的轻量级管理系统。
核心目标：**高效管理学生、课程、排课与消课，并通过QQ邮箱自动提醒老师上课/消课。**

> **本系统不包含学生端，所有学生相关业务均为后台管理。学生无需登录和操作，所有学生相关操作均由老师或管理员在后台完成。**

---

## 二、核心功能

### 1. 学生管理
- 添加、编辑、删除学生
- 学生仅为后台管理对象，不涉及任何前台操作或自助服务
- 学生无需账号和登录，仅用于排课和消课管理

### 2. 课程管理
- 添加、编辑、删除课程

### 3. 排课管理
- 支持三种排课模式：
  1. **仅一次**：只排一次课
  2. **每天重复**：在指定日期区间内，每天同一时间排课
  3. **每周相同时间重复**：在指定日期区间内，每周指定的星期几、同一时间排课
- 新建排课时可选择排课模式，并设置起止日期、时间、星期等参数
- 排课后自动通过QQ邮箱发邮件提醒对应老师

### 4. 消课管理
- 记录每次上课消耗的课时
- 消课后自动通过QQ邮箱发邮件提醒老师

### 5. 班级管理
- 新建、编辑、删除班级
- 向班级添加/移除学生
- 查看班级学生列表

### 6. 班级排课
- 支持为整个班级排课（选择班级、课程、老师、时间、排课模式）
- 班级内所有学生自动关联排课记录

### 7. 班级点名（考勤）
- 支持对班级排课进行点名
- 记录每个学生的出勤情况（出勤/缺勤/请假等）

### 8. 邮件提醒
- 支持QQ邮箱SMTP配置
- 排课/消课后自动邮件提醒老师
- 如需通知家长，可通过后台一键发送，无需学生端配合

### 9. 登录/权限
- 管理员、老师两类角色
- 仅管理员和老师可登录系统
- 学生无需账号和登录，所有学生相关操作均由后台完成

---

## 三、技术栈

### 前端
- **Vue 3** - 现代化前端框架
- **Element Plus** - 企业级UI组件库
- **Vue Router** - 路由管理
- **Pinia** - 状态管理
- **Axios** - HTTP客户端
- **Vite** - 构建工具

### 后端
- **Flask** - Python Web框架
- **Flask-SQLAlchemy** - ORM数据库操作
- **Flask-Login** - 用户认证
- **Flask-Mail** - 邮件发送
- **Flask-CORS** - 跨域支持
- **PyMySQL** - MySQL数据库驱动

### 数据库
- **MySQL** - 关系型数据库

### 部署
- **宝塔面板** - 服务器管理
- **Nginx** - 反向代理
- **Gunicorn** - WSGI服务器

### 邮件服务
- **QQ邮箱SMTP** - 邮件提醒服务

---

## 四、项目结构

```
bianyi-weilai/
├── backend/                 # Flask后端
│   ├── app.py              # 主应用入口
│   ├── config.py           # 配置文件
│   ├── requirements.txt    # Python依赖
│   ├── Procfile           # 部署配置
│   ├── models/            # 数据模型
│   │   ├── __init__.py
│   │   ├── user.py        # 用户模型
│   │   ├── student.py     # 学生模型
│   │   ├── course.py      # 课程模型
│   │   ├── classroom.py   # 班级模型
│   │   ├── schedule.py    # 排课模型
│   │   └── record.py      # 消课记录模型
│   ├── routes/            # API路由
│   │   ├── auth.py        # 认证路由
│   │   ├── students.py    # 学生管理路由
│   │   ├── courses.py     # 课程管理路由
│   │   ├── classrooms.py  # 班级管理路由
│   │   ├── schedules.py   # 排课管理路由
│   │   └── records.py     # 消课管理路由
│   ├── utils/             # 工具函数
│   │   ├── email.py       # 邮件发送工具
│   │   └── helpers.py     # 辅助函数
│   ├── init_db.py         # 数据库初始化
│   └── clear_db.py        # 数据库清空
├── frontend/              # Vue 3前端
│   ├── index.html         # HTML模板
│   ├── package.json       # 前端依赖
│   ├── vite.config.js     # Vite配置
│   └── src/
│       ├── main.js        # 应用入口
│       ├── App.vue        # 根组件
│       ├── components/    # 公共组件
│       │   ├── Header.vue # 头部组件
│       │   ├── Sidebar.vue # 侧边栏组件
│       │   └── Table.vue  # 表格组件
│       ├── views/         # 页面组件
│       │   ├── Login.vue  # 登录页
│       │   ├── Dashboard.vue # 首页
│       │   ├── Students.vue # 学生管理
│       │   ├── Courses.vue # 课程管理
│       │   ├── Classrooms.vue # 班级管理
│       │   ├── Schedules.vue # 排课管理
│       │   ├── Records.vue # 消课管理
│       │   └── Settings.vue # 系统设置
│       ├── router/        # 路由配置
│       │   └── index.js   # 路由定义
│       ├── stores/        # 状态管理
│       │   ├── auth.js    # 认证状态
│       │   └── app.js     # 应用状态
│       └── utils/         # 工具函数
│           ├── api.js     # API请求
│           └── helpers.js # 辅助函数
└── README.md              # 项目文档
```

---

## 五、数据库设计

### 核心数据表
- **user**：id, username, password, role (admin/teacher), email
- **student**：id, name, contact, email, remark
- **course**：id, name, total_hours
- **classroom**：id, name, remark
- **classroom_student**：id, classroom_id, student_id
- **schedule**：id, course_id, classroom_id, student_id, teacher, start_datetime, end_datetime, note, status, repeat_type（none/daily/weekly），repeat_days（如"1,3,5"），repeat_end_date
- **record**：id, schedule_id, student_id, course_id, hours_consumed, date, note
- **attendance_record**：id, schedule_id, student_id, status（出勤/缺勤/请假）, note

---

## 六、主要页面与流程

### 1. 登录页
- 管理员/老师登录

### 2. 学生管理页
- 学生列表、添加/编辑/删除
- 学生无需账号，仅信息管理，所有操作均为后台管理

### 3. 课程管理页
- 课程列表、添加/编辑/删除

### 4. 排课管理页
- 新建排课（选学生、课程、老师、时间、排课模式）
- 支持"仅一次/每天/每周"三种排课模式，填写起止日期、时间、星期等参数
- 排课列表、编辑/删除
- 排课成功后自动发邮件

### 5. 消课管理页
- 选择排课记录，填写消课课时、备注
- 消课列表
- 消课后自动发邮件

### 6. 班级管理页
- 班级列表、新建/编辑/删除班级
- 查看和管理班级学生（添加/移除）

### 7. 班级排课页
- 选择班级进行排课，支持重复排课模式

### 8. 班级点名页
- 选择班级和排课记录，进行点名，记录每个学生的考勤状态

### 9. 邮箱配置页
- 设置QQ邮箱账号、授权码
- 测试邮件发送

---

## 七、邮件提醒逻辑

### 排课后自动发邮件
- 自动发送邮件给老师，内容包含课程、学生、时间等

### 消课后自动发邮件
- 自动发送邮件给老师，内容包含消课详情

### 邮箱配置
- 支持QQ邮箱（SMTP）

### 邮件内容示例

#### 排课提醒
```
主题：【排课提醒】您有新的课程安排

老师您好，您有新的排课：
课程：Python编程
学生：张三
时间：2024-06-20 14:00 - 16:00
请及时查看。
```

#### 消课提醒
```
主题：【消课提醒】课程已消课

老师您好，课程已消课：
课程：Python编程
学生：张三
消课课时：2
时间：2024-06-20
备注：正常上课
```

---

## 八、快速开始

### 环境要求
- Python 3.8+
- Node.js 16+
- MySQL 5.7+

### 后端安装

1. **克隆项目**
```bash
git clone https://github.com/DLshujin/Lesson-Cancel-Project.git
cd Lesson-Cancel-Project/backend
```

2. **创建虚拟环境**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **配置环境变量**
创建 `.env` 文件：
```env
SECRET_KEY=your-secret-key
DATABASE_URL=mysql+pymysql://username:password@localhost/lesson_cancel_db
MAIL_USERNAME=your-email@qq.com
MAIL_PASSWORD=your-smtp-password
```

5. **初始化数据库**
```bash
python init_db.py
```

6. **启动后端服务**
```bash
python app.py
```

### 前端安装

1. **进入前端目录**
```bash
cd ../frontend
```

2. **安装依赖**
```bash
npm install
```

3. **启动开发服务器**
```bash
npm run dev
```

4. **构建生产版本**
```bash
npm run build
```

---

## 九、部署指南

### 宝塔面板部署

1. **安装宝塔面板**
```bash
# CentOS
yum install -y wget && wget -O install.sh http://download.bt.cn/install/install_6.0.sh && sh install.sh

# Ubuntu/Debian
wget -O install.sh http://download.bt.cn/install/install-ubuntu_6.0.sh && sudo bash install.sh
```

2. **安装必要软件**
- Nginx
- MySQL
- Python项目管理器

3. **上传项目文件**
- 将项目文件上传到服务器
- 配置Python项目

4. **配置Nginx**
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    # 前端静态文件
    location / {
        root /path/to/frontend/dist;
        try_files $uri $uri/ /index.html;
    }
    
    # 后端API代理
    location /api {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

5. **配置Gunicorn**
```bash
# 启动命令
gunicorn -w 4 -b 127.0.0.1:5000 app:app
```

---

## 十、邮件配置

### QQ邮箱SMTP配置

1. **获取授权码**
- 登录QQ邮箱
- 设置 → 账户 → POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务
- 开启SMTP服务
- 获取授权码

2. **配置环境变量**
```env
MAIL_USERNAME=your-email@qq.com
MAIL_PASSWORD=your-smtp-authorization-code
```

---

## 十一、功能权限矩阵

| 功能模块   | 管理员 | 老师 |
|------------|--------|------|
| 学生管理   | √      | 只读/可编辑（可配置） |
| 班级管理   | √      | √    |
| 排课       | √      | √    |
| 调课/补课  | √      | √    |
| 消课/考勤  | √      | √    |
| 数据导出   | √      | √    |
| 系统配置   | √      | ×    |
| 操作日志   | √      | 只读 |

---

## 十二、重要功能优化与行业最佳实践

### 排课模块
- **排课冲突检测**：自动检测老师、教室、班级时间冲突，排课时实时提示
- **调课/补课/请假**：支持对已排课程的调课、补课、请假、取消等操作，并自动通知老师
- **课程表视图**：提供日历/周视图，支持拖拽调整课程
- **排课通知**：排课、调课、取消等自动邮件/短信/微信通知老师

### 消课/考勤模块
- **多状态考勤**：支持出勤、迟到、早退、请假、旷课等多种状态
- **消课与课时自动关联**：消课自动扣减课时，课时不足自动提醒
- **考勤统计报表**：支持按班级、学生、老师、课程等多维度统计与导出
- **考勤补录与修改**：支持历史考勤补录、修改，自动记录操作日志

### 班级与数据管理
- **班级历史记录**：记录班级的历史学生、课程、考勤等变更日志
- **批量操作**：支持学生、排课、考勤等批量导入导出
- **班级课表导出**：支持班级课表、考勤表一键导出
- **操作日志**：所有关键操作自动记录日志，便于追溯

---

## 十三、常见问题与运维建议

- **如何恢复误删数据？** 建议定期备份数据库，支持一键恢复
- **如何追溯关键操作？** 所有关键操作自动记录日志，支持按用户、时间、功能模块检索
- **如何批量导入数据？** 支持Excel模板批量导入学生、排课、考勤等
- **课时不足如何提醒？** 系统自动检测课时余额，课时不足时自动提醒老师/家长
- **如何导出报表？** 支持一键导出班级课表、考勤表、消课统计等
- **本系统不支持学生自助登录与操作，所有学生相关业务均由老师或管理员后台完成**

---

## 十四、关键代码模板

### 邮件发送函数（QQ邮箱SMTP）
```python
import smtplib
from email.mime.text import MIMEText

def send_mail(to_addr, subject, content, smtp_user, smtp_pass, smtp_server='smtp.qq.com', smtp_port=465):
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['From'] = smtp_user
    msg['To'] = to_addr
    msg['Subject'] = subject
    try:
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(smtp_user, smtp_pass)
        server.sendmail(smtp_user, [to_addr], msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print('邮件发送失败:', e)
        return False
```

### 排课/消课后自动发邮件
```python
# 排课后
send_mail(
    to_addr=teacher_email,
    subject="【排课提醒】您有新的课程安排",
    content=f"老师您好，您有新的排课：\n课程：{course_name}\n学生：{student_name}\n时间：{start_time} - {end_time}\n请及时查看。",
    smtp_user=smtp_user, smtp_pass=smtp_pass
)

# 消课后
send_mail(
    to_addr=teacher_email,
    subject="【消课提醒】课程已消课",
    content=f"老师您好，课程已消课：\n课程：{course_name}\n学生：{student_name}\n消课课时：{hours}\n时间：{date}\n备注：{note}",
    smtp_user=smtp_user, smtp_pass=smtp_pass
)
```

---

## 十五、API文档

### 认证相关
- `POST /api/login` - 用户登录
- `POST /api/logout` - 用户登出
- `GET /api/user` - 获取当前用户信息

### 学生管理
- `GET /api/students` - 获取学生列表
- `POST /api/students` - 创建学生
- `PUT /api/students/:id` - 更新学生信息
- `DELETE /api/students/:id` - 删除学生

### 课程管理
- `GET /api/courses` - 获取课程列表
- `POST /api/courses` - 创建课程
- `PUT /api/courses/:id` - 更新课程信息
- `DELETE /api/courses/:id` - 删除课程

### 班级管理
- `GET /api/classrooms` - 获取班级列表
- `POST /api/classrooms` - 创建班级
- `PUT /api/classrooms/:id` - 更新班级信息
- `DELETE /api/classrooms/:id` - 删除班级

### 排课管理
- `GET /api/schedules` - 获取排课列表
- `POST /api/schedules` - 创建排课
- `PUT /api/schedules/:id` - 更新排课信息
- `DELETE /api/schedules/:id` - 删除排课

### 消课管理
- `GET /api/records` - 获取消课记录
- `POST /api/records` - 创建消课记录
- `PUT /api/records/:id` - 更新消课记录
- `DELETE /api/records/:id` - 删除消课记录

---

## 十六、开发指南

### 后端开发

1. **添加新的API路由**
```python
# backend/routes/example.py
from flask import Blueprint, jsonify

api = Blueprint('api', __name__)

@api.route('/example')
def example():
    return jsonify({'message': 'Hello World'})
```

2. **创建数据模型**
```python
# backend/models/example.py
from .user import db

class Example(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
```

### 前端开发

1. **添加新页面**
```vue
<!-- frontend/src/views/Example.vue -->
<template>
  <div class="example-page">
    <h1>示例页面</h1>
  </div>
</template>

<script>
export default {
  name: 'Example'
}
</script>
```

2. **配置路由**
```javascript
// frontend/src/router/index.js
import Example from '../views/Example.vue'

const routes = [
  {
    path: '/example',
    name: 'Example',
    component: Example
  }
]
```

---

## 十七、后续可扩展方向

- 消课统计报表
- 多校区/多角色权限
- 微信/钉钉/短信通知
- 移动端适配/小程序（如有学生端需求可后续开发，当前不包含学生端）

---

## 十八、详细开发任务分解

- 环境与基础搭建
- 登录与权限
- 学生管理
- 课程管理
- 排课管理
- 消课管理
- 班级管理模块开发
- 班级与学生的关联管理
- 班级排课功能开发
- 班级点名（考勤）功能开发
- 邮箱配置与邮件提醒
- 其它（操作日志、导入导出、页面美化）

---

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证（含专利保护条款）- 查看 [LICENSE](LICENSE) 文件了解详情

### 专利保护说明
- 本项目可能涉及相关技术专利
- 商业使用需要单独专利授权
- 教育和非商业使用免费
- 专利许可咨询请联系：adilei.shujin@gmail.com

## 📞 联系方式

- 项目地址：[https://github.com/DLshujin/Lesson-Cancel-Project](https://github.com/DLshujin/Lesson-Cancel-Project)
- 邮箱：adilei.shujin@gmail.com

## 🙏 致谢

感谢所有为这个项目做出贡献的开发者！