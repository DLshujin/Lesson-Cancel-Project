# 编译未来教培管理系统 API 文档

## 概述

编译未来教培管理系统是一个轻量级的教培机构管理系统，提供课程管理、学生管理、教室管理、课程安排和消课记录等功能。

## 基础信息

- **基础URL**: `http://localhost:5000/api`
- **认证方式**: Bearer Token
- **数据格式**: JSON
- **字符编码**: UTF-8

## 认证模块 (Auth)

### 用户注册
- **POST** `/api/auth/register`
- **描述**: 注册新用户
- **请求体**:
```json
{
    "username": "string",
    "password": "string",
    "name": "string",
    "email": "string",
    "role": "admin|teacher|staff"
}
```
- **响应**: 201 Created

### 用户登录
- **POST** `/api/auth/login`
- **描述**: 用户登录获取token
- **请求体**:
```json
{
    "username": "string",
    "password": "string"
}
```
- **响应**: 200 OK
```json
{
    "token": "string",
    "user": {
        "id": 1,
        "username": "string",
        "name": "string",
        "email": "string",
        "role": "string"
    }
}
```

### 获取用户信息
- **GET** `/api/auth/profile`
- **描述**: 获取当前登录用户信息
- **认证**: 需要
- **响应**: 200 OK

### 修改密码
- **PUT** `/api/auth/password`
- **描述**: 修改用户密码
- **认证**: 需要
- **请求体**:
```json
{
    "old_password": "string",
    "new_password": "string"
}
```

## 学生管理模块 (Students)

### 获取学生列表
- **GET** `/api/students`
- **描述**: 获取学生列表，支持分页和搜索
- **认证**: 需要
- **查询参数**:
  - `page`: 页码 (默认: 1)
  - `per_page`: 每页数量 (默认: 10)
  - `search`: 搜索关键词
- **响应**: 200 OK
```json
{
    "students": [...],
    "total": 100,
    "pages": 10,
    "current_page": 1
}
```

### 获取单个学生
- **GET** `/api/students/{id}`
- **描述**: 获取指定学生信息
- **认证**: 需要

### 创建学生
- **POST** `/api/students`
- **描述**: 创建新学生
- **认证**: 需要
- **请求体**:
```json
{
    "name": "string",
    "contact": "string",
    "email": "string",
    "remark": "string"
}
```

### 更新学生
- **PUT** `/api/students/{id}`
- **描述**: 更新学生信息
- **认证**: 需要

### 删除学生
- **DELETE** `/api/students/{id}`
- **描述**: 删除学生
- **认证**: 需要

## 课程管理模块 (Courses)

### 获取课程列表
- **GET** `/api/courses`
- **描述**: 获取课程列表，支持分页和搜索
- **认证**: 需要
- **查询参数**:
  - `page`: 页码
  - `per_page`: 每页数量
  - `search`: 搜索关键词
  - `status`: 课程状态

### 获取单个课程
- **GET** `/api/courses/{id}`
- **描述**: 获取指定课程信息
- **认证**: 需要

### 创建课程
- **POST** `/api/courses`
- **描述**: 创建新课程
- **认证**: 需要
- **请求体**:
```json
{
    "name": "string",
    "description": "string",
    "price": 299.00,
    "total_hours": 20,
    "status": "active|inactive"
}
```

### 更新课程
- **PUT** `/api/courses/{id}`
- **描述**: 更新课程信息
- **认证**: 需要

### 删除课程
- **DELETE** `/api/courses/{id}`
- **描述**: 删除课程
- **认证**: 需要

## 教室管理模块 (Classrooms)

### 获取教室列表
- **GET** `/api/classrooms`
- **描述**: 获取教室列表
- **认证**: 需要
- **查询参数**:
  - `page`: 页码
  - `per_page`: 每页数量
  - `search`: 搜索关键词
  - `status`: 教室状态

### 获取可用教室
- **GET** `/api/classrooms/available`
- **描述**: 获取所有可用教室
- **认证**: 需要

### 获取单个教室
- **GET** `/api/classrooms/{id}`
- **描述**: 获取指定教室信息
- **认证**: 需要

### 创建教室
- **POST** `/api/classrooms`
- **描述**: 创建新教室
- **认证**: 需要
- **请求体**:
```json
{
    "name": "string",
    "capacity": 30,
    "location": "string",
    "equipment": "string",
    "status": "available|maintenance|occupied"
}
```

### 更新教室
- **PUT** `/api/classrooms/{id}`
- **描述**: 更新教室信息
- **认证**: 需要

### 删除教室
- **DELETE** `/api/classrooms/{id}`
- **描述**: 删除教室
- **认证**: 需要

## 课程安排模块 (Schedules)

### 获取课程安排列表
- **GET** `/api/schedules`
- **描述**: 获取课程安排列表
- **认证**: 需要
- **查询参数**:
  - `page`: 页码
  - `per_page`: 每页数量
  - `course_id`: 课程ID
  - `classroom_id`: 教室ID
  - `teacher_id`: 教师ID
  - `status`: 状态
  - `date_from`: 开始日期
  - `date_to`: 结束日期

### 获取今日课程安排
- **GET** `/api/schedules/today`
- **描述**: 获取今日的课程安排
- **认证**: 需要

### 获取单个课程安排
- **GET** `/api/schedules/{id}`
- **描述**: 获取指定课程安排信息
- **认证**: 需要

### 创建课程安排
- **POST** `/api/schedules`
- **描述**: 创建新课程安排
- **认证**: 需要
- **请求体**:
```json
{
    "course_id": 1,
    "classroom_id": 1,
    "teacher_id": 1,
    "start_time": "2024-01-15T09:00:00",
    "end_time": "2024-01-15T11:00:00",
    "max_students": 25,
    "notes": "string"
}
```

### 更新课程安排
- **PUT** `/api/schedules/{id}`
- **描述**: 更新课程安排
- **认证**: 需要

### 更新课程安排状态
- **PUT** `/api/schedules/{id}/status`
- **描述**: 更新课程安排状态
- **认证**: 需要
- **请求体**:
```json
{
    "status": "scheduled|ongoing|completed|cancelled"
}
```

### 删除课程安排
- **DELETE** `/api/schedules/{id}`
- **描述**: 删除课程安排
- **认证**: 需要

## 消课记录模块 (Records)

### 获取消课记录列表
- **GET** `/api/records`
- **描述**: 获取消课记录列表
- **认证**: 需要
- **查询参数**:
  - `page`: 页码
  - `per_page`: 每页数量
  - `student_id`: 学生ID
  - `course_id`: 课程ID
  - `schedule_id`: 课程安排ID
  - `attendance_status`: 出勤状态
  - `date_from`: 开始日期
  - `date_to`: 结束日期

### 获取单个消课记录
- **GET** `/api/records/{id}`
- **描述**: 获取指定消课记录信息
- **认证**: 需要

### 创建消课记录
- **POST** `/api/records`
- **描述**: 创建新消课记录
- **认证**: 需要
- **请求体**:
```json
{
    "student_id": 1,
    "course_id": 1,
    "schedule_id": 1,
    "consumed_hours": 2.0,
    "attendance_status": "present|absent|late",
    "notes": "string"
}
```

### 批量创建消课记录
- **POST** `/api/records/batch`
- **描述**: 批量创建消课记录
- **认证**: 需要
- **请求体**:
```json
{
    "records": [
        {
            "student_id": 1,
            "course_id": 1,
            "schedule_id": 1,
            "consumed_hours": 2.0,
            "attendance_status": "present"
        }
    ]
}
```

### 更新消课记录
- **PUT** `/api/records/{id}`
- **描述**: 更新消课记录
- **认证**: 需要

### 删除消课记录
- **DELETE** `/api/records/{id}`
- **描述**: 删除消课记录
- **认证**: 需要

### 获取学生消课记录
- **GET** `/api/records/student/{student_id}`
- **描述**: 获取指定学生的消课记录
- **认证**: 需要

### 获取课程消课记录
- **GET** `/api/records/course/{course_id}`
- **描述**: 获取指定课程的消课记录
- **认证**: 需要

### 获取课程安排消课记录
- **GET** `/api/records/schedule/{schedule_id}`
- **描述**: 获取指定课程安排的消课记录
- **认证**: 需要

### 获取消课记录统计
- **GET** `/api/records/statistics`
- **描述**: 获取消课记录统计信息
- **认证**: 需要
- **响应**:
```json
{
    "total_records": 100,
    "today_records": 5,
    "total_hours": 200.5,
    "attendance_stats": {
        "present": 80,
        "absent": 15,
        "late": 5
    }
}
```

## 通用响应格式

### 成功响应
```json
{
    "message": "操作成功",
    "data": {...}
}
```

### 错误响应
```json
{
    "error": "错误信息",
    "details": "详细错误信息"
}
```

## 状态码说明

- **200**: 成功
- **201**: 创建成功
- **400**: 请求参数错误
- **401**: 未认证
- **403**: 权限不足
- **404**: 资源不存在
- **500**: 服务器内部错误

## 数据模型

### 用户 (User)
```json
{
    "id": 1,
    "username": "string",
    "name": "string",
    "email": "string",
    "role": "admin|teacher|staff",
    "created_at": "2024-01-01T00:00:00"
}
```

### 学生 (Student)
```json
{
    "id": 1,
    "name": "string",
    "contact": "string",
    "email": "string",
    "remark": "string",
    "created_at": "2024-01-01T00:00:00"
}
```

### 课程 (Course)
```json
{
    "id": 1,
    "name": "string",
    "description": "string",
    "price": 299.00,
    "total_hours": 20,
    "status": "active|inactive",
    "created_at": "2024-01-01T00:00:00"
}
```

### 教室 (Classroom)
```json
{
    "id": 1,
    "name": "string",
    "capacity": 30,
    "location": "string",
    "equipment": "string",
    "status": "available|maintenance|occupied",
    "created_at": "2024-01-01T00:00:00"
}
```

### 课程安排 (Schedule)
```json
{
    "id": 1,
    "course_id": 1,
    "course_name": "string",
    "classroom_id": 1,
    "classroom_name": "string",
    "teacher_id": 1,
    "teacher_name": "string",
    "start_time": "2024-01-15T09:00:00",
    "end_time": "2024-01-15T11:00:00",
    "max_students": 25,
    "current_students": 20,
    "status": "scheduled|ongoing|completed|cancelled",
    "notes": "string",
    "created_at": "2024-01-01T00:00:00"
}
```

### 消课记录 (Record)
```json
{
    "id": 1,
    "student_id": 1,
    "student_name": "string",
    "course_id": 1,
    "course_name": "string",
    "schedule_id": 1,
    "schedule_info": "2024-01-15 09:00 - 11:00",
    "consumed_hours": 2.0,
    "attendance_status": "present|absent|late",
    "notes": "string",
    "created_by": 1,
    "creator_name": "string",
    "created_at": "2024-01-01T00:00:00"
}
```

## 使用示例

### 1. 登录获取token
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

### 2. 创建学生
```bash
curl -X POST http://localhost:5000/api/students \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"name": "张三", "contact": "13800138000", "email": "zhangsan@example.com"}'
```

### 3. 创建课程
```bash
curl -X POST http://localhost:5000/api/courses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"name": "Python编程基础", "description": "Python入门课程", "price": 299.00, "total_hours": 20}'
```

### 4. 创建课程安排
```bash
curl -X POST http://localhost:5000/api/schedules \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"course_id": 1, "classroom_id": 1, "teacher_id": 1, "start_time": "2024-01-15T09:00:00", "end_time": "2024-01-15T11:00:00"}'
```

### 5. 创建消课记录
```bash
curl -X POST http://localhost:5000/api/records \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"student_id": 1, "course_id": 1, "schedule_id": 1, "consumed_hours": 2.0, "attendance_status": "present"}'
```

## 注意事项

1. 所有需要认证的接口都需要在请求头中包含 `Authorization: Bearer YOUR_TOKEN`
2. 时间格式统一使用 ISO 8601 格式：`YYYY-MM-DDTHH:MM:SS`
3. 分页参数 `page` 从 1 开始
4. 删除操作会进行关联性检查，有相关数据的记录可能无法删除
5. 课程安排会检查时间冲突，避免同一教室在同一时间段被重复安排
6. 消课记录会检查重复性，同一学生在同一课程安排中只能有一条记录 