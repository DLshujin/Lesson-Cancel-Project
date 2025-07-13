#!/bin/bash
echo "编译未来教培管理系统启动中..."
cd "$(dirname "$0")/backend"
python3 start_server.py
