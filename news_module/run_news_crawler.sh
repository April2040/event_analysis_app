#!/bin/bash
# run_news_crawler.sh - 运行新闻抓取器

echo "🚀 启动热点财经新闻抓取器..."
echo "======================================"

# 进入新闻模块目录
cd /Users/qiyi/coding/event_analysis_app/news_module

# 运行简化版新闻抓取器
python3 simple_news_crawler.py

echo "======================================"
echo "✅ 新闻抓取完成！"
echo "📁 数据文件保存在 news_data/ 目录下"
echo "🔄 可以将此数据用于后续的事件分析"
