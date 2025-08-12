#!/bin/bash

echo "📰 ===== 交互式财经新闻爬虫 ====="
echo ""

# 激活虚拟环境
source .venv/bin/activate

echo "🚀 正在启动交互式新闻爬虫..."
echo "✨ 功能特性:"
echo "   - 实时获取财经新闻"
echo "   - 智能热度排序"
echo "   - 可选HTML网页展示"
echo "   - 自动浏览器打开"
echo ""

# 直接运行优化的RSS爬虫
python news_module/optimized_rss_crawler.py

echo ""
echo "🎉 感谢使用财经新闻爬虫系统!"
