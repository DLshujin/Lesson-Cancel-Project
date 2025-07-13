#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
编译未来教培管理系统 - 一键部署脚本
支持本地电脑和服务器部署
"""

import os
import sys
import subprocess
import platform
import json
import time
from pathlib import Path

class Deployer:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.backend_dir = self.project_root / "backend"
        self.frontend_dir = self.project_root / "frontend"
        self.is_windows = platform.system() == "Windows"
        self.deploy_config = {}
        
    def print_banner(self):
        """打印部署横幅"""
        print("=" * 70)
        print("🚀 编译未来教培管理系统 - 一键部署脚本")
        print("=" * 70)
        print("📋 支持功能:")
        print("   ✅ 自动检测操作系统")
        print("   ✅ 自动安装依赖")
        print("   ✅ 自动配置数据库")
        print("   ✅ 自动启动服务")
        print("   ✅ 支持本地和服务器部署")
        print("=" * 70)
    
    def detect_os(self):
        """检测操作系统"""
        print("🔍 检测操作系统...")
        os_name = platform.system()
        os_version = platform.version()
        print(f"   - 操作系统: {os_name}")
        print(f"   - 版本: {os_version}")
        print(f"   - 架构: {platform.machine()}")
        return os_name
    
    def check_python(self):
        """检查Python环境"""
        print("🐍 检查Python环境...")
        python_version = sys.version_info
        print(f"   - Python版本: {python_version.major}.{python_version.minor}.{python_version.micro}")
        
        if python_version < (3, 7):
            print("❌ Python版本过低，需要Python 3.7或更高版本")
            return False
        
        print("✅ Python版本符合要求")
        return True
    
    def install_dependencies(self):
        """安装依赖"""
        print("📦 安装Python依赖...")
        
        # 检查pip
        try:
            subprocess.run([sys.executable, "-m", "pip", "--version"], 
                         check=True, capture_output=True)
        except subprocess.CalledProcessError:
            print("❌ pip未安装或不可用")
            return False
        
        # 安装依赖
        requirements_file = self.backend_dir / "requirements.txt"
        if requirements_file.exists():
            print("   安装后端依赖...")
            try:
                subprocess.run([
                    sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
                ], check=True)
                print("   ✅ 后端依赖安装成功")
            except subprocess.CalledProcessError as e:
                print(f"   ❌ 后端依赖安装失败: {e}")
                return False
        
        # 安装额外依赖
        extra_packages = ["pymysql", "python-dotenv", "requests"]
        for package in extra_packages:
            try:
                subprocess.run([
                    sys.executable, "-m", "pip", "install", package
                ], check=True, capture_output=True)
                print(f"   ✅ {package} 安装成功")
            except subprocess.CalledProcessError:
                print(f"   ⚠️  {package} 安装失败，可能已存在")
        
        return True
    
    def setup_database(self):
        """设置数据库"""
        print("🗄️  设置数据库...")
        
        # 检查MySQL
        mysql_available = self.check_mysql()
        if not mysql_available:
            print("⚠️  MySQL未检测到，将使用SQLite作为替代")
            return self.setup_sqlite()
        
        # 尝试自动设置MySQL
        return self.setup_mysql()
    
    def check_mysql(self):
        """检查MySQL是否可用"""
        try:
            import pymysql
            # 尝试连接MySQL
            connection = pymysql.connect(
                host="localhost",
                port=3306,
                user="root",
                password="",
                connect_timeout=3
            )
            connection.close()
            return True
        except:
            try:
                connection = pymysql.connect(
                    host="localhost",
                    port=3306,
                    user="root",
                    password="123456",
                    connect_timeout=3
                )
                connection.close()
                return True
            except:
                return False
    
    def setup_mysql(self):
        """设置MySQL数据库"""
        print("   配置MySQL数据库...")
        
        # 运行数据库初始化脚本
        os.chdir(self.backend_dir)
        try:
            result = subprocess.run([
                sys.executable, "direct_db_init.py"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("   ✅ MySQL数据库设置成功")
                return True
            else:
                print(f"   ❌ MySQL数据库设置失败: {result.stderr}")
                return False
        except Exception as e:
            print(f"   ❌ MySQL数据库设置异常: {e}")
            return False
    
    def setup_sqlite(self):
        """设置SQLite数据库"""
        print("   配置SQLite数据库...")
        
        # 创建SQLite配置文件
        sqlite_config = '''import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    
    # SQLite数据库配置
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 邮件配置
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'your-email@qq.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'your-smtp-password'
    
    # 分页配置
    POSTS_PER_PAGE = 20

# 为了兼容性，添加模块级别的属性
SECRET_KEY = Config.SECRET_KEY
SQLALCHEMY_DATABASE_URI = Config.SQLALCHEMY_DATABASE_URI
SQLALCHEMY_TRACK_MODIFICATIONS = Config.SQLALCHEMY_TRACK_MODIFICATIONS
MAIL_SERVER = Config.MAIL_SERVER
MAIL_PORT = Config.MAIL_PORT
MAIL_USE_TLS = Config.MAIL_USE_TLS
MAIL_USERNAME = Config.MAIL_USERNAME
MAIL_PASSWORD = Config.MAIL_PASSWORD
POSTS_PER_PAGE = Config.POSTS_PER_PAGE
'''
        
        config_file = self.backend_dir / "config.py"
        with open(config_file, 'w', encoding='utf-8') as f:
            f.write(sqlite_config)
        
        print("   ✅ SQLite配置创建成功")
        return True
    
    def create_startup_scripts(self):
        """创建启动脚本"""
        print("📝 创建启动脚本...")
        
        # Windows启动脚本
        if self.is_windows:
            startup_script = '''@echo off
echo 编译未来教培管理系统启动中...
cd /d "%~dp0backend"
python start_server.py
pause
'''
            with open(self.project_root / "start.bat", 'w', encoding='gbk') as f:
                f.write(startup_script)
            print("   ✅ Windows启动脚本创建成功 (start.bat)")
        
        # Linux/Mac启动脚本
        startup_script = '''#!/bin/bash
echo "编译未来教培管理系统启动中..."
cd "$(dirname "$0")/backend"
python3 start_server.py
'''
        startup_file = self.project_root / "start.sh"
        with open(startup_file, 'w', encoding='utf-8') as f:
            f.write(startup_script)
        
        # 设置执行权限
        if not self.is_windows:
            os.chmod(startup_file, 0o755)
        
        print("   ✅ Linux/Mac启动脚本创建成功 (start.sh)")
    
    def create_service_files(self):
        """创建系统服务文件"""
        print("🔧 创建系统服务文件...")
        
        # systemd服务文件 (Linux)
        systemd_service = '''[Unit]
Description=编译未来教培管理系统
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/bianyi-weilai/backend
ExecStart=/usr/bin/python3 start_server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
'''
        
        service_file = self.project_root / "bianyi-weilai.service"
        with open(service_file, 'w', encoding='utf-8') as f:
            f.write(systemd_service)
        
        print("   ✅ systemd服务文件创建成功 (bianyi-weilai.service)")
        
        # Windows服务文件
        if self.is_windows:
            nssm_config = f'''Application: {sys.executable}
AppDirectory: {self.backend_dir}
AppParameters: start_server.py
DisplayName: 编译未来教培管理系统
Description: 编译未来教培管理系统服务
Start: SERVICE_AUTO_START
'''
            
            nssm_file = self.project_root / "nssm-config.txt"
            with open(nssm_file, 'w', encoding='utf-8') as f:
                f.write(nssm_config)
            
            print("   ✅ Windows服务配置创建成功 (nssm-config.txt)")
    
    def create_deployment_guide(self):
        """创建部署指南"""
        print("📚 创建部署指南...")
        
        guide_content = '''# 编译未来教培管理系统 - 部署指南

## 🚀 快速启动

### Windows
```bash
# 双击运行
start.bat

# 或命令行运行
cd backend
python start_server.py
```

### Linux/Mac
```bash
# 使用启动脚本
./start.sh

# 或直接运行
cd backend
python3 start_server.py
```

## 📊 系统信息

- **访问地址**: http://localhost:5000
- **API文档**: http://localhost:5000/api
- **健康检查**: http://localhost:5000/health
- **默认管理员**: admin / admin123

## 🔧 系统服务安装

### Linux (systemd)
```bash
# 复制服务文件
sudo cp bianyi-weilai.service /etc/systemd/system/

# 修改WorkingDirectory路径
sudo nano /etc/systemd/system/bianyi-weilai.service

# 启用并启动服务
sudo systemctl enable bianyi-weilai
sudo systemctl start bianyi-weilai

# 查看状态
sudo systemctl status bianyi-weilai
```

### Windows (NSSM)
```bash
# 安装NSSM (需要管理员权限)
# 下载: https://nssm.cc/download

# 安装服务
nssm install BianyiWeilai python.exe
nssm set BianyiWeilai AppDirectory "C:\\path\\to\\bianyi-weilai\\backend"
nssm set BianyiWeilai AppParameters start_server.py

# 启动服务
nssm start BianyiWeilai
```

## 📝 配置文件

- **数据库配置**: backend/config.py
- **环境变量**: backend/.env (可选)

## 🔍 故障排除

1. **端口被占用**: 修改 start_server.py 中的端口号
2. **数据库连接失败**: 检查数据库服务状态
3. **权限错误**: 确保有足够的文件系统权限

## 📞 技术支持

如有问题，请查看:
1. 控制台错误信息
2. 日志文件
3. 系统服务状态
'''
        
        guide_file = self.project_root / "DEPLOYMENT_GUIDE.md"
        with open(guide_file, 'w', encoding='utf-8') as f:
            f.write(guide_content)
        
        print("   ✅ 部署指南创建成功 (DEPLOYMENT_GUIDE.md)")
    
    def test_system(self):
        """测试系统"""
        print("🧪 测试系统...")
        
        # 启动测试服务器
        os.chdir(self.backend_dir)
        try:
            # 启动服务器（后台运行）
            process = subprocess.Popen([
                sys.executable, "start_server.py"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # 等待服务器启动
            time.sleep(5)
            
            # 测试健康检查
            import requests
            try:
                response = requests.get("http://localhost:5000/health", timeout=10)
                if response.status_code == 200:
                    print("   ✅ 系统测试成功")
                    process.terminate()
                    return True
                else:
                    print(f"   ❌ 系统测试失败: HTTP {response.status_code}")
                    process.terminate()
                    return False
            except Exception as e:
                print(f"   ❌ 系统测试失败: {e}")
                process.terminate()
                return False
                
        except Exception as e:
            print(f"   ❌ 系统测试异常: {e}")
            return False
    
    def create_deployment_summary(self):
        """创建部署总结"""
        print("📋 创建部署总结...")
        
        summary = {
            "deployment_time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "os": platform.system(),
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            "project_path": str(self.project_root),
            "backend_path": str(self.backend_dir),
            "frontend_path": str(self.frontend_dir),
            "startup_scripts": {
                "windows": "start.bat" if self.is_windows else None,
                "linux_mac": "start.sh"
            },
            "service_files": {
                "systemd": "bianyi-weilai.service",
                "windows": "nssm-config.txt" if self.is_windows else None
            },
            "access_info": {
                "url": "http://localhost:5000",
                "api_docs": "http://localhost:5000/api",
                "health_check": "http://localhost:5000/health",
                "admin_user": "admin",
                "admin_password": "admin123"
            }
        }
        
        summary_file = self.project_root / "deployment_summary.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print("   ✅ 部署总结创建成功 (deployment_summary.json)")
    
    def deploy(self):
        """执行完整部署"""
        self.print_banner()
        
        # 1. 检测环境
        os_name = self.detect_os()
        if not self.check_python():
            return False
        
        # 2. 安装依赖
        if not self.install_dependencies():
            print("❌ 依赖安装失败")
            return False
        
        # 3. 设置数据库
        if not self.setup_database():
            print("❌ 数据库设置失败")
            return False
        
        # 4. 创建启动脚本
        self.create_startup_scripts()
        
        # 5. 创建服务文件
        self.create_service_files()
        
        # 6. 创建部署指南
        self.create_deployment_guide()
        
        # 7. 测试系统
        if self.test_system():
            print("✅ 系统测试通过")
        else:
            print("⚠️  系统测试失败，但部署已完成")
        
        # 8. 创建部署总结
        self.create_deployment_summary()
        
        # 9. 显示部署结果
        self.show_deployment_result()
        
        return True
    
    def show_deployment_result(self):
        """显示部署结果"""
        print()
        print("=" * 70)
        print("🎉 部署完成！")
        print("=" * 70)
        print("📊 部署信息:")
        print(f"   - 操作系统: {platform.system()}")
        print(f"   - Python版本: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
        print(f"   - 项目路径: {self.project_root}")
        print("=" * 70)
        print("🚀 启动方式:")
        if self.is_windows:
            print("   - Windows: 双击 start.bat 或运行 python start_server.py")
        else:
            print("   - Linux/Mac: ./start.sh 或 python3 start_server.py")
        print("=" * 70)
        print("📋 访问信息:")
        print("   - 系统地址: http://localhost:5000")
        print("   - API文档: http://localhost:5000/api")
        print("   - 健康检查: http://localhost:5000/health")
        print("   - 管理员: admin / admin123")
        print("=" * 70)
        print("📚 相关文件:")
        print("   - 部署指南: DEPLOYMENT_GUIDE.md")
        print("   - 部署总结: deployment_summary.json")
        print("   - 系统服务: bianyi-weilai.service")
        print("=" * 70)
        print("💡 提示:")
        print("   - 查看 DEPLOYMENT_GUIDE.md 了解详细部署说明")
        print("   - 如需安装为系统服务，请参考部署指南")
        print("   - 遇到问题请查看控制台错误信息")
        print("=" * 70)

def main():
    """主函数"""
    deployer = Deployer()
    
    try:
        success = deployer.deploy()
        if success:
            print("\n🎉 一键部署成功完成！")
            return 0
        else:
            print("\n❌ 部署过程中遇到问题，请检查错误信息")
            return 1
    except KeyboardInterrupt:
        print("\n⚠️  部署被用户中断")
        return 1
    except Exception as e:
        print(f"\n❌ 部署异常: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main()) 