#!/bin/bash

echo "🌟 ===== 财经新闻爬虫系统 v2.0 ====="
echo ""

# 激活虚拟环境
source .venv/bin/activate

echo "📊 当前系统状态:"
echo "✅ RSS源配置: 8个主要源 + 15条备用新闻"
echo "✅ 成功率: ~37.5% (3/8个源稳定运行)"
echo "✅ 智能备用: 高质量财经新闻保障"
echo "✅ 热度算法: 四维度加权评分"
echo ""

echo "🚀 可用选项:"
echo "1. 运行优化RSS爬虫 (推荐)"
echo "2. 运行完整新闻显示系统"
echo "3. 查看系统状态报告"
echo "4. 退出"
echo ""

read -p "请选择操作 (1-4): " choice

case $choice in
    1)
        echo ""
        echo "🔥 启动优化RSS爬虫（含HTML生成选项）..."
        python news_module/optimized_rss_crawler.py
        ;;
    2)
        echo ""
        echo "🎨 启动完整新闻显示系统..."
        python news_module/real_news_display.py
        ;;
    3)
        echo ""
        echo "📋 显示系统状态报告..."
        cat RSS_OPTIMIZATION_REPORT.md
        ;;
    4)
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
