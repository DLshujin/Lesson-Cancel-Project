# 编译未来主后端入口
from flask import Flask

app = Flask(__name__)

# 后续将添加路由和业务逻辑

if __name__ == '__main__':
    app.run(debug=True) 