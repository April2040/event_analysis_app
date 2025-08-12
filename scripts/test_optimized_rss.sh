#!/bin/bash

echo "🚀 启动优化RSS新闻爬虫测试..."

# 激活虚拟环境
source .venv/bin/activate

# 测试RSS爬虫
echo "📡 测试RSS新闻爬虫..."
python news_module/optimized_rss_crawler.py

echo "✅ 测试完成"
