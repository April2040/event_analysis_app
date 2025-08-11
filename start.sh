#!/bin/bash

# 财经事件分析系统 - 一键启动脚本
# =================================

echo "🚀 财经事件分析系统 - 一键启动"
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

# 启动服务
echo "🌟 启动财经事件分析系统..."
echo ""
echo "📊 功能: 智能分析 + 新闻爬虫"
echo "🌐 访问: http://localhost:8002"
echo "📰 新闻: http://localhost:8002/news"
echo "⚡ 快速模式: 仅生成分析，节省50%时间"
echo "💡 完整模式: 分析 + 专业HTML报告"
echo ""
echo "🔥 正在启动服务，请稍候..."
echo "📝 提示: 按 Ctrl+C 停止服务"
echo ""

# 启动主程序
python main_integrated.py
