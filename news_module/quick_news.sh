#!/bin/bash
# quick_news.sh - 快速新闻展示脚本

echo "📰 快速新闻榜单生成器"
echo "===================="
echo ""

# 检查是否在正确目录
if [ ! -f "news_display.py" ]; then
    echo "❌ 请在news_module目录下运行此脚本"
    exit 1
fi

echo "🔄 正在生成最新热点新闻榜单..."
python3 news_display.py

echo ""
echo "✅ 完成！新闻榜单已生成"
echo ""
echo "📂 查看文件:"
echo "  HTML榜单: news_display/ 目录下的 .html 文件"
echo "  JSON数据: news_display/ 目录下的 .json 文件"
echo ""
echo "💡 提示: 在浏览器中打开HTML文件查看精美的新闻榜单界面"
