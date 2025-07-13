import pymysql
from config import Config

def create_database():
    """创建数据库"""
    try:
        # 连接MySQL服务器（不指定数据库）
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='A123bc!@',  # 请修改为你的MySQL密码
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        
        # 创建数据库
        cursor.execute("CREATE DATABASE IF NOT EXISTS lesson_cancel_db DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print("✅ 数据库 lesson_cancel_db 创建成功")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ 创建数据库失败: {e}")
        print("\n请检查：")
        print("1. MySQL服务是否已启动")
        print("2. 用户名和密码是否正确")
        print("3. 用户是否有创建数据库的权限")

def test_connection():
    """测试数据库连接"""
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='A123bc!@',  # 你的MySQL密码
            database='lesson_cancel_db',
            charset='utf8mb4'
        )
        print("✅ 数据库连接测试成功")
        connection.close()
        return True
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        return False

if __name__ == "__main__":
    print("🚀 初始化本地数据库...")
    print("=" * 50)
    
    # 创建数据库
    create_database()
    
    # 测试连接
    if test_connection():
        print("\n✅ 数据库初始化完成！")
        print("现在可以运行: python app.py")
    else:
        print("\n❌ 数据库初始化失败，请检查配置") 