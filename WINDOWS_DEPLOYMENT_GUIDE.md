# Windows 一键部署指南

## 🚀 最简单的部署方式

### 方法一：双击部署（推荐）
1. 双击运行 `一键部署.bat`
2. 等待部署完成
3. 系统自动启动

### 方法二：命令行部署
```cmd
# 运行Windows专用部署脚本
python quick_deploy_windows.py

# 启动系统
cd backend
python start_server.py
```

## 📋 部署脚本说明

### 1. 一键部署.bat
- **功能**: 最简单的部署方式，双击即可
- **特点**: 自动检查Python环境，自动部署，自动启动
- **适用**: 新手用户，快速部署

### 2. quick_deploy_windows.py
- **功能**: Windows专用快速部署脚本
- **特点**: 避免Unicode编码问题，专门针对Windows优化
- **适用**: 有经验的用户，需要更多控制

### 3. quick_deploy.py
- **功能**: 通用快速部署脚本
- **特点**: 支持多平台，但可能有编码问题
- **适用**: 跨平台部署

### 4. deploy.py
- **功能**: 完整部署脚本
- **特点**: 功能最全面，包含系统服务配置
- **适用**: 生产环境部署

## 🖥️ 系统要求

### 最低配置
- Windows 10/11
- Python 3.7+
- 512MB RAM
- 1GB 磁盘空间

### 推荐配置
- Windows 10/11
- Python 3.8+
- 2GB RAM
- 5GB 磁盘空间
- MySQL 5.7+ (可选)

## 📦 安装步骤

### 1. 安装Python
1. 访问 https://www.python.org/downloads/
2. 下载Python 3.7或更高版本
3. 安装时勾选"Add Python to PATH"
4. 验证安装: `python --version`

### 2. 下载项目
1. 下载项目文件到本地
2. 解压到任意目录
3. 进入项目目录

### 3. 运行部署
```cmd
# 方法一：双击部署
一键部署.bat

# 方法二：命令行部署
python quick_deploy_windows.py
```

## 🗄️ 数据库配置

### MySQL (推荐)
- 自动检测MySQL服务
- 自动创建数据库和表
- 默认配置: localhost:3306, root/A123bc!@

### SQLite (备用)
- 无需额外安装
- 自动配置
- 适合轻量级使用

## 🚀 启动方式

### 自动启动
- 部署完成后自动启动
- 或双击 `start.bat`

### 手动启动
```cmd
cd backend
python start_server.py
```

## 📊 访问信息

部署完成后，可以通过以下地址访问：

- **系统地址**: http://localhost:5000
- **API文档**: http://localhost:5000/api
- **健康检查**: http://localhost:5000/health
- **默认管理员**: admin / admin123

## 🔍 故障排除

### 常见问题

1. **Python未找到**
   ```cmd
   # 检查Python安装
   python --version
   
   # 如果未找到，重新安装Python并勾选"Add to PATH"
   ```

2. **依赖安装失败**
   ```cmd
   # 升级pip
   python -m pip install --upgrade pip
   
   # 手动安装依赖
   pip install -r backend/requirements.txt
   ```

3. **数据库连接失败**
   ```cmd
   # 检查MySQL服务
   net start mysql
   
   # 或使用SQLite
   # 修改 backend/config.py
   ```

4. **端口被占用**
   ```cmd
   # 查看端口占用
   netstat -ano | findstr :5000
   
   # 修改端口
   # 编辑 backend/start_server.py
   ```

5. **编码错误**
   ```cmd
   # 设置控制台编码
   chcp 65001
   
   # 使用Windows专用脚本
   python quick_deploy_windows.py
   ```

### 错误日志

1. **控制台输出**: 查看启动时的错误信息
2. **Python错误**: 检查Python版本和依赖
3. **数据库错误**: 检查数据库连接配置

## 📁 部署后文件

```
bianyi-weilai/
├── 一键部署.bat              # 一键部署脚本
├── quick_deploy_windows.py   # Windows专用部署脚本
├── quick_deploy.py           # 通用快速部署脚本
├── deploy.py                 # 完整部署脚本
├── start.bat                 # Windows启动脚本
├── start.sh                  # Linux/Mac启动脚本
├── backend/                  # 后端代码
└── frontend/                 # 前端代码
```

## 🔧 高级配置

### 修改端口
编辑 `backend/start_server.py`:
```python
app.run(debug=True, host='0.0.0.0', port=8080)  # 修改端口号
```

### 修改数据库
编辑 `backend/config.py`:
```python
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:pass@host:port/db'
```

### 安装为Windows服务
```cmd
# 使用NSSM安装服务
nssm install BianyiWeilai python.exe
nssm set BianyiWeilai AppDirectory "C:\path\to\bianyi-weilai\backend"
nssm set BianyiWeilai AppParameters start_server.py
nssm start BianyiWeilai
```

## 📞 技术支持

### 获取帮助
1. 查看控制台错误信息
2. 检查Python版本和依赖
3. 验证数据库连接
4. 查看部署日志

### 联系支持
如遇到问题，请提供：
- Windows版本
- Python版本
- 错误日志
- 部署脚本输出

---

**祝您部署顺利！** 🎉 