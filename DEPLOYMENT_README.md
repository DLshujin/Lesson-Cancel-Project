# 编译未来教培管理系统 - 一键部署说明

## 🚀 快速部署

### 方法一：快速部署（推荐）
```bash
# 运行快速部署脚本
python quick_deploy.py
```

### 方法二：完整部署
```bash
# 运行完整部署脚本
python deploy.py
```

## 📋 部署脚本说明

### 1. quick_deploy.py - 快速部署脚本
**特点：**
- ⚡ 快速部署，适合开发环境
- 🔧 自动安装依赖
- 🗄️ 自动配置数据库
- 📝 创建启动脚本
- 🧪 测试系统启动

**适用场景：**
- 本地开发环境
- 快速测试部署
- 临时服务器部署

### 2. deploy.py - 完整部署脚本
**特点：**
- 🔍 自动检测操作系统
- 📦 完整依赖管理
- 🗄️ 智能数据库配置（MySQL/SQLite）
- 🔧 创建系统服务文件
- 📚 生成部署文档
- 🧪 完整系统测试

**适用场景：**
- 生产环境部署
- 服务器长期运行
- 需要系统服务

## 🖥️ 支持的操作系统

### Windows
- Windows 10/11
- Windows Server 2016+
- 支持批处理脚本启动

### Linux
- Ubuntu 18.04+
- CentOS 7+
- Debian 9+
- 支持systemd服务

### macOS
- macOS 10.14+
- 支持shell脚本启动

## 📦 系统要求

### 最低要求
- Python 3.7+
- 512MB RAM
- 1GB 磁盘空间

### 推荐配置
- Python 3.8+
- 2GB RAM
- 5GB 磁盘空间
- MySQL 5.7+ (可选)

## 🗄️ 数据库支持

### MySQL (推荐)
- 自动检测MySQL服务
- 自动创建数据库和表
- 支持密码自动配置

### SQLite (备用)
- 无需额外安装
- 适合轻量级部署
- 自动配置

## 📁 部署后文件结构

```
bianyi-weilai/
├── deploy.py              # 完整部署脚本
├── quick_deploy.py        # 快速部署脚本
├── start.bat              # Windows启动脚本
├── start.sh               # Linux/Mac启动脚本
├── bianyi-weilai.service  # Linux系统服务文件
├── nssm-config.txt        # Windows服务配置
├── DEPLOYMENT_GUIDE.md    # 详细部署指南
├── deployment_summary.json # 部署总结
├── backend/               # 后端代码
└── frontend/              # 前端代码
```

## 🚀 启动方式

### Windows
```bash
# 双击启动
start.bat

# 命令行启动
cd backend
python start_server.py
```

### Linux/Mac
```bash
# 脚本启动
./start.sh

# 命令行启动
cd backend
python3 start_server.py
```

## 🔧 系统服务安装

### Linux (systemd)
```bash
# 复制服务文件
sudo cp bianyi-weilai.service /etc/systemd/system/

# 修改工作目录
sudo nano /etc/systemd/system/bianyi-weilai.service

# 启用并启动服务
sudo systemctl enable bianyi-weilai
sudo systemctl start bianyi-weilai

# 查看状态
sudo systemctl status bianyi-weilai
```

### Windows (NSSM)
```bash
# 安装NSSM
# 下载: https://nssm.cc/download

# 安装服务
nssm install BianyiWeilai python.exe
nssm set BianyiWeilai AppDirectory "C:\path\to\bianyi-weilai\backend"
nssm set BianyiWeilai AppParameters start_server.py

# 启动服务
nssm start BianyiWeilai
```

## 📊 访问信息

部署完成后，可以通过以下地址访问系统：

- **系统地址**: http://localhost:5000
- **API文档**: http://localhost:5000/api
- **健康检查**: http://localhost:5000/health
- **默认管理员**: admin / admin123

## 🔍 故障排除

### 常见问题

1. **Python版本过低**
   ```bash
   # 检查Python版本
   python --version
   
   # 需要Python 3.7+
   ```

2. **依赖安装失败**
   ```bash
   # 升级pip
   python -m pip install --upgrade pip
   
   # 手动安装依赖
   pip install -r backend/requirements.txt
   ```

3. **数据库连接失败**
   ```bash
   # 检查MySQL服务
   # Windows: net start mysql
   # Linux: sudo systemctl status mysql
   
   # 或使用SQLite
   # 修改 backend/config.py 中的数据库配置
   ```

4. **端口被占用**
   ```bash
   # 修改端口
   # 编辑 backend/start_server.py 中的端口号
   ```

5. **权限错误**
   ```bash
   # Linux/Mac设置执行权限
   chmod +x start.sh
   
   # Windows以管理员身份运行
   ```

### 日志查看

1. **控制台输出**: 查看启动时的错误信息
2. **系统日志**: 
   - Linux: `sudo journalctl -u bianyi-weilai`
   - Windows: 事件查看器

## 📞 技术支持

### 获取帮助

1. **查看部署总结**: `deployment_summary.json`
2. **查看详细指南**: `DEPLOYMENT_GUIDE.md`
3. **检查错误日志**: 控制台输出
4. **测试系统状态**: http://localhost:5000/health

### 联系支持

如遇到问题，请提供：
- 操作系统信息
- Python版本
- 错误日志
- 部署脚本输出

---

**祝您部署顺利！** 🎉 