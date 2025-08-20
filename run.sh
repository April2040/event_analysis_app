#!/bin/bash

# 财经事件分析系统 v6.0.0 - 官方启动脚本
# ==========================================
# 集成高级HTML自动生成功能
# 支持: AI分析 + 新闻爬虫 + 专业可视化

echo "🚀 财经事件分析系统 v6.0.0"
echo "=========================="
echo ""

# 检查主程序文件
if [ ! -f "main_integrated.py" ]; then
    echo "❌ 错误: 找不到主程序文件 main_integrated.py"
    echo "请确保在正确的项目目录中运行此脚本"
    exit 1
fi

# 检查虚拟环境
if [ ! -d ".venv" ]; then
    echo "❌ 错误: 找不到虚拟环境 .venv"
    echo "请先运行: python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source .venv/bin/activate

# 检查环境变量
if [ ! -f ".env" ]; then
    echo "⚠️  警告: 找不到 .env 文件"
    echo "请确保设置了 DEEPSEEK_API_KEY"
fi

echo "✅ 环境检查完成"
echo ""
echo "🎯 系统功能:"
echo "  • AI深度事件分析 (DeepSeek)"
echo "  • RSS新闻实时爬取"
echo "  • 高级HTML可视化报告"
echo "  • 四模块专业分析框架"
echo ""
echo "🌐 启动Web服务器..."
echo "📍 访问地址: http://localhost:8002"
echo "📰 新闻页面: http://localhost:8002/news"
echo ""
echo "💡 使用提示:"
echo "  • 完整模式: 生成分析 + 高级HTML报告"
echo "  • 快速模式: 仅生成分析，节省50%时间"
echo ""
echo "🚀 正在启动服务器..."
echo "按 Ctrl+C 停止服务"
echo ""

# 启动主程序
python main_integrated.py
