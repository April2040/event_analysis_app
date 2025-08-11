#!/bin/bash

# 财经事件分析系统 - 后台启动脚本
# =================================

echo "🚀 财经事件分析系统 - 后台启动"
echo "=============================="

# 检查当前目录
if [ ! -f "main_integrated.py" ]; then
    echo "❌ 错误: 请在项目根目录运行此脚本"
    exit 1
fi

# 检查虚拟环境
if [ ! -d ".venv" ]; then
    echo "❌ 错误: 虚拟环境不存在，请先创建虚拟环境"
    exit 1
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source .venv/bin/activate

# 检查端口占用
echo "🔍 检查端口占用..."
if lsof -ti:8002 >/dev/null 2>&1; then
    echo "⚠️  端口8002已被占用，正在停止占用进程..."
    lsof -ti:8002 | xargs kill -9 2>/dev/null || true
    sleep 2
fi

# 后台启动服务
echo "🌟 后台启动财经事件分析系统..."
nohup python main_integrated.py > service.log 2>&1 &
PID=$!

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 5

# 检查服务是否成功启动
if curl -s http://localhost:8002 >/dev/null 2>&1; then
    echo "✅ 服务启动成功！"
    echo ""
    echo "📊 功能: 智能分析 + 新闻爬虫"
    echo "🌐 访问: http://localhost:8002"
    echo "📰 新闻: http://localhost:8002/news"
    echo "🔍 API: http://localhost:8002/api/news"
    echo ""
    echo "📝 服务信息:"
    echo "   进程ID: $PID"
    echo "   日志文件: service.log"
    echo "   停止服务: ./stop.sh 或 kill $PID"
    echo ""
    echo "💡 提示: 可以关闭终端，服务会继续在后台运行"
else
    echo "❌ 服务启动失败，请检查日志文件: service.log"
    exit 1
fi
