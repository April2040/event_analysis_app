#!/bin/bash

echo "🚀 ===== 财经事件分析系统 ====="
echo "📊 新版架构: 新闻爬虫 + 智能分析器"
echo ""

# 激活虚拟环境
source .venv/bin/activate

echo "🎯 可用功能:"
echo "1. 启动完整系统 (FastAPI Web界面)"
echo "2. 仅新闻爬虫 (命令行)"
echo "3. 查看项目结构"
echo "4. 退出"
echo ""

read -p "请选择功能 (1-4): " choice

case $choice in
    1)
        echo ""
        echo "🌐 启动Web界面..."
        echo "📊 主页面: http://localhost:8000"
        echo "📰 新闻页面: http://localhost:8000/news"
        echo ""
        python main_integrated.py
        ;;
    2)
        echo ""
        echo "🔥 启动新闻爬虫..."
        python -c "
import sys
import os
sys.path.insert(0, '.')
from modules.news_crawler.crawler import NewsWebCrawler

print('📡 获取热点新闻...')
crawler = NewsWebCrawler()
news_list = crawler.get_top_hotspots(limit=10)

print(f'✅ 成功获取 {len(news_list)} 条新闻')
print('=' * 60)
for i, news in enumerate(news_list, 1):
    print(f'{i}. 【{news.get(\"category\", \"财经\")}】{news.get(\"title\", \"\")}')
    print(f'   来源: {news.get(\"source\", \"\")} | 热度: {news.get(\"heat_score\", 0):.2f}')
    print()
"
        ;;
    3)
        echo ""
        echo "📁 项目结构:"
        echo "├── main_integrated.py     # 整合系统入口"
        echo "├── modules/"
        echo "│   └── news_crawler/      # 新闻爬虫模块"
        echo "├── utils_v2.py           # 智能分析器(v2.0版本)"
        echo "├── templates/            # Web界面模板"
        echo "├── prompts/              # AI提示词"
        echo "└── temp/                 # 临时文件输出"
        echo ""
        ;;
    4)
        echo "👋 再见!"
        exit 0
        ;;
    *)
        echo "❌ 无效选择，请重新运行"
        exit 1
        ;;
esac

echo ""
echo "✅ 操作完成！"
