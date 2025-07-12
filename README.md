# 编译未来开发文档

## 一、项目简介
编译未来是一款专注于教培机构/学校**消课、排课、邮件提醒**的轻量级管理系统。
核心目标：**高效管理学生、课程、排课与消课，并通过QQ邮箱自动提醒老师上课/消课。**

> **本系统不包含学生端，所有学生相关业务均为后台管理。学生无需登录和操作，所有学生相关操作均由老师或管理员在后台完成。**

---

## 二、核心功能
1. **学生管理**
   - 添加、编辑、删除学生
   - 学生仅为后台管理对象，不涉及任何前台操作或自助服务
   - 学生无需账号和登录，仅用于排课和消课管理
2. **课程管理**
   - 添加、编辑、删除课程
3. **排课管理**
   - 支持三种排课模式：
     1. 仅一次：只排一次课
     2. 每天重复：在指定日期区间内，每天同一时间排课
     3. 每周相同时间重复：在指定日期区间内，每周指定的星期几、同一时间排课
   - 新建排课时可选择排课模式，并设置起止日期、时间、星期等参数
   - 排课后自动通过QQ邮箱发邮件提醒对应老师
4. **消课管理**
   - 记录每次上课消耗的课时
   - 消课后自动通过QQ邮箱发邮件提醒老师
5. **班级管理**
   - 新建、编辑、删除班级
   - 向班级添加/移除学生
   - 查看班级学生列表
6. **班级排课**
   - 支持为整个班级排课（选择班级、课程、老师、时间、排课模式）
   - 班级内所有学生自动关联排课记录
7. **班级点名（考勤）**
   - 支持对班级排课进行点名
   - 记录每个学生的出勤情况（出勤/缺勤/请假等）
5. **邮件提醒**
   - 支持QQ邮箱SMTP配置
   - 排课/消课后自动邮件提醒老师
   - 如需通知家长，可通过后台一键发送，无需学生端配合
6. **登录/权限**
   - 管理员、老师两类角色
   - 仅管理员和老师可登录系统
   - 学生无需账号和登录，所有学生相关操作均由后台完成

---

## 三、主要页面与流程
1. **登录页**  
   - 管理员/老师登录
2. **学生管理页**  
   - 学生列表、添加/编辑/删除
   - 学生无需账号，仅信息管理，所有操作均为后台管理
3. **课程管理页**  
   - 课程列表、添加/编辑/删除
4. **排课管理页**  
   - 新建排课（选学生、课程、老师、时间、排课模式）
   - 支持“仅一次/每天/每周”三种排课模式，填写起止日期、时间、星期等参数
   - 排课列表、编辑/删除
   - 排课成功后自动发邮件
5. **消课管理页**  
   - 选择排课记录，填写消课课时、备注
   - 消课列表
   - 消课后自动发邮件
6. **班级管理页**
  - 班级列表、新建/编辑/删除班级
  - 查看和管理班级学生（添加/移除）
7. **班级排课页**
  - 选择班级进行排课，支持重复排课模式
8. **班级点名页**
  - 选择班级和排课记录，进行点名，记录每个学生的考勤状态
6. **邮箱配置页**  
   - 设置QQ邮箱账号、授权码
   - 测试邮件发送

---

## 四、数据库设计
- **student**：id, name, contact, email, remark
- **course**：id, name, total_hours
- **classroom**：id, name, remark
- **classroom_student**：id, classroom_id, student_id
- **schedule**：id, course_id, classroom_id, student_id, teacher, start_datetime, end_datetime, note, status, repeat_type（none/daily/weekly），repeat_days（如“1,3,5”），repeat_end_date
- **record**：id, schedule_id, student_id, course_id, hours_consumed, date, note
- **attendance_record**：id, schedule_id, student_id, status（出勤/缺勤/请假）, note
- **user**：id, username, password, role (admin/teacher), email

---

## 五、技术选型
- **后端**：Flask（Python 3.9+）
- **前端**：Bootstrap 5 + Jinja2模板
- **数据库**：SQLite（可扩展MySQL/PostgreSQL）
- **邮件**：smtplib（QQ邮箱SMTP）
- **定时任务**：APScheduler（如需定时提醒）
- **依赖管理**：requirements.txt

---

## 六、开发步骤
1. **环境准备**
   - 安装Python 3.9+、pip
   - pip install -r requirements.txt
2. **数据库初始化**
   - 运行 `python init_db.py` 创建表和初始账号
3. **功能开发**
   - 学生、课程、排课、消课、邮件、登录等模块
   - 邮件发送函数集成QQ邮箱SMTP
4. **前端页面**
   - 使用Bootstrap 5组件开发所有页面
   - 弹窗表单、表格、分页、AJAX交互
5. **邮箱配置与测试**
   - 邮箱配置页，保存SMTP信息
   - 邮件发送测试接口
6. **邮件提醒**
   - 排课/消课成功后自动调用邮件发送
7. **部署上线**
   - 本地：python app.py
   - 云端：gunicorn/Procfile/Nginx

---

## 七、生产环境部署说明

### 1. 推荐部署环境
- **操作系统**：Linux（如 Ubuntu 20.04+），也可在 Windows Server 上运行
- **Web服务器**：Nginx（推荐，做反向代理和静态资源服务）
- **应用服务器**：Gunicorn（Linux）或 Waitress（Windows）
- **Python环境**：Python 3.8+
- **依赖管理**：pip + requirements.txt
- **数据库**：SQLite（开发/小型生产），可扩展为MySQL/PostgreSQL
- **邮件服务**：QQ邮箱 SMTP

### 2. 服务器准备
- 购买云服务器（如阿里云、腾讯云、华为云、AWS、Azure等）
- 配置安全组，开放 80（HTTP）、443（HTTPS）、22（SSH）端口

### 3. 部署步骤（以Linux为例）

1. **代码上传**
```bash
scp -r ./bianyi-weilai user@your_server_ip:/home/user/
```
2. **安装依赖**
```bash
cd /home/user/bianyi-weilai
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
3. **配置环境变量（如有）**
- 可在`.env`或`config.py`中配置数据库、邮箱等敏感信息
4. **数据库初始化**
```bash
python init_db.py
```
5. **启动应用（Gunicorn）**
```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```
6. **配置Nginx反向代理**
```nginx
server {
    listen 80;
    server_name your_domain.com;
    location /static/ {
        alias /home/user/bianyi-weilai/static/;
    }
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```
重载Nginx：
```bash
sudo systemctl reload nginx
```
7. **设置守护进程（可选）**
- 推荐用 Supervisor、systemd 管理 Gunicorn 进程，保证服务自动重启

### 4. Windows 部署补充
- 可用 `waitress-serve` 启动 Flask 项目：
```bash
pip install waitress
waitress-serve --listen=0.0.0.0:8000 app:app
```
- 也可用 IIS 或 Nginx for Windows 做反向代理

### 5. 常见运维建议
- 定期备份数据库（如 school.db）
- 定期更新依赖，修复安全漏洞
- 配置日志记录，便于排查问题
- 设置防火墙和安全组，防止未授权访问
- 邮件服务配置：确保QQ邮箱开启SMTP服务，授权码正确

---

## 七、邮件提醒逻辑
- **排课后**：自动发送邮件给老师，内容包含课程、学生、时间等
- **消课后**：自动发送邮件给老师，内容包含消课详情
- **邮箱配置**：支持QQ邮箱（SMTP）

---

## 八、项目结构推荐
```
your_project/
├── app.py
├── init_db.py
├── clear_db.py
├── requirements.txt
├── Procfile
├── school.db
├── static/
│   └── custom.css
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── students.html
│   ├── courses.html
│   ├── schedule_attendance.html
│   ├── users.html
│   └── classrooms.html
```

---

## 九、上线与维护建议
- 管理员定期备份数据库
- 邮箱授权码妥善保管
- 密码建议加密存储（生产环境）
- 可扩展导入导出、统计报表等功能
- 本系统不支持学生自助登录与操作，所有学生相关业务均由老师或管理员后台完成

---

## 十、后续可扩展方向
- 消课统计报表
- 多校区/多角色权限
- 微信/钉钉/短信通知
- 移动端适配/小程序（如有学生端需求可后续开发，当前不包含学生端）

---

## 十一、详细开发任务分解
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

## 十二、关键代码模板
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

### 邮箱配置表单（users.html）
```html
<form id="email-config-form" method="post">
  <div class="mb-3">
    <label class="form-label">QQ邮箱账号</label>
    <input type="email" class="form-control" name="smtp_user" required>
  </div>
  <div class="mb-3">
    <label class="form-label">QQ邮箱授权码</label>
    <input type="password" class="form-control" name="smtp_pass" required>
    <div class="form-text">请在QQ邮箱设置-账户-开启SMTP服务后获取授权码。</div>
  </div>
  <button type="submit" class="btn btn-primary">保存配置</button>
</form>
```

---

## 十三、邮件内容示例
### 排课提醒
```
主题：【排课提醒】您有新的课程安排

老师您好，您有新的排课：
课程：Python编程
学生：张三
时间：2024-06-20 14:00 - 16:00
请及时查看。
```

### 消课提醒
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

## 十四、页面美化建议（Bootstrap 5）
- 使用 `.container`, `.row`, `.col` 布局，保证响应式
- 表格加 `.table-hover .align-middle .table-bordered`
- 按钮用 `.btn .btn-primary/.btn-success/.btn-danger`
- 弹窗用 `.modal .modal-dialog .modal-content`
- 表单用 `.form-label .form-control .form-select`
- 用 `.badge`, `.alert`, `.card` 增强视觉层次
- 在 `static/custom.css` 中自定义主色、圆角、阴影
- 移动端适配：用 Bootstrap 5 的栅格系统和媒体查询

---

如需某一模块的详细代码实现、页面结构或美化CSS示例，请直接指定模块或页面！ 

## 重要功能优化与行业最佳实践补充

### 排课模块
- **排课冲突检测**：自动检测老师、教室、班级时间冲突，排课时实时提示。
- **调课/补课/请假**：支持对已排课程的调课、补课、请假、取消等操作，并自动通知老师。
- **课程表视图**：提供日历/周视图，支持拖拽调整课程。
- **排课通知**：排课、调课、取消等自动邮件/短信/微信通知老师。

### 消课/考勤模块
- **多状态考勤**：支持出勤、迟到、早退、请假、旷课等多种状态。
- **消课与课时自动关联**：消课自动扣减课时，课时不足自动提醒。
- **考勤统计报表**：支持按班级、学生、老师、课程等多维度统计与导出。
- **考勤补录与修改**：支持历史考勤补录、修改，自动记录操作日志。

### 班级与数据管理
- **班级历史记录**：记录班级的历史学生、课程、考勤等变更日志。
- **批量操作**：支持学生、排课、考勤等批量导入导出。
- **班级课表导出**：支持班级课表、考勤表一键导出。
- **操作日志**：所有关键操作自动记录日志，便于追溯。

---

## 功能权限矩阵（示例）
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

## 常见问题与运维建议
- 如何恢复误删数据？建议定期备份数据库，支持一键恢复。
- 如何追溯关键操作？所有关键操作自动记录日志，支持按用户、时间、功能模块检索。
- 如何批量导入数据？支持Excel模板批量导入学生、排课、考勤等。
- 课时不足如何提醒？系统自动检测课时余额，课时不足时自动提醒老师/家长。
- 如何导出报表？支持一键导出班级课表、考勤表、消课统计等。
- 本系统不支持学生自助登录与操作，所有学生相关业务均由老师或管理员后台完成

---

## 模块设计建议
每个核心模块建议包含：
- **功能说明**：简要描述模块核心功能和业务目标。
- **操作流程**：用流程图或文字描述典型操作流程。
- **界面示意**：可插入页面结构草图或主要交互说明。
- **数据结构**：列出主要表结构及关键字段。 