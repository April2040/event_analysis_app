#!/bin/bash

echo "🌟 ===== 财经新闻智能分析系统 v2.0 ====="
echo "📁 模块化架构重组完成"
echo ""

# 激活虚拟环境
source .venv/bin/activate

echo "📊 当前项目结构:"
echo "├── modules/"
echo "│   ├── news_crawler/     # 新闻爬虫模块"
echo "│   └── news_analysis/    # 智能分析模块"
echo "├── outputs/"
echo "│   ├── news_reports/     # 新闻报告输出"
echo "│   └── analysis_reports/ # 分析报告输出"
echo "├── docs/                 # 文档文件"
echo "└── scripts/              # 启动脚本"
echo ""

echo "🚀 可用功能:"
echo "1. 新闻爬虫模块 (独立运行)"
echo "2. 智能分析模块 (独立运行)"
echo "3. 完整流程 (爬虫+分析)"
echo "4. 原版系统 (FastAPI)"
echo "5. 退出"
echo ""

read -p "请选择功能 (1-5): " choice

case $choice in
    1)
        echo ""
        echo "🔥 启动新闻爬虫模块..."
        python modules/news_crawler/crawler.py
        ;;
    2)
        echo ""
        echo "🧠 启动智能分析模块..."
        echo "⚠️ 注意: 需要先运行新闻爬虫或使用备用数据"
        python main_modular.py
        ;;
    3)
        echo ""
        echo "🎯 启动完整流程..."
        python main_modular.py
        ;;
    4)
        echo ""
        echo "🌐 启动原版FastAPI系统..."
        uvicorn main:app --reload --host 0.0.0.0 --port 8000
        ;;
    5)
        echo "👋 再见!"
        exit 0
        ;;
    *)
        echo "❌ 无效选择，请重新运行脚本"
        exit 1
        ;;
esac

echo ""
echo "✅ 操作完成！"
