#!/bin/bash

# 财经事件分析系统 - 停止服务脚本
# =================================

echo "🛑 财经事件分析系统 - 停止服务"
echo "=============================="

# 查找并停止占用8002端口的进程
if lsof -ti:8002 >/dev/null 2>&1; then
    echo "🔍 发现占用端口8002的进程..."
    PIDS=$(lsof -ti:8002)
    echo "📋 进程ID: $PIDS"
    
    echo "⏳ 正在停止服务..."
    lsof -ti:8002 | xargs kill -9 2>/dev/null || true
    
    sleep 2
    
    # 再次检查
    if lsof -ti:8002 >/dev/null 2>&1; then
        echo "❌ 服务停止失败，请手动停止"
        echo "💡 手动停止命令: lsof -ti:8002 | xargs kill -9"
    else
        echo "✅ 服务已成功停止"
    fi
else
    echo "ℹ️  没有发现运行在端口8002的服务"
fi

# 查找可能的Python进程
echo ""
echo "🔍 检查相关Python进程..."
PYTHON_PIDS=$(ps aux | grep main_integrated.py | grep -v grep | awk '{print $2}' 2>/dev/null || true)

if [ -n "$PYTHON_PIDS" ]; then
    echo "📋 发现相关Python进程: $PYTHON_PIDS"
    echo "⏳ 正在停止Python进程..."
    echo "$PYTHON_PIDS" | xargs kill -9 2>/dev/null || true
    echo "✅ Python进程已停止"
else
    echo "ℹ️  没有发现相关Python进程"
fi

echo ""
echo "🎉 停止操作完成！"
