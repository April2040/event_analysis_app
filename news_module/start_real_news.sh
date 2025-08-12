#!/bin/bash
# start_real_news.sh - 真实新闻系统启动脚本

echo "🚀 真实新闻抓取系统"
echo "==================="
echo ""

# 检查Python环境
PYTHON_CMD="/Users/qiyi/coding/event_analysis_app/.venv/bin/python"

if [ ! -f "$PYTHON_CMD" ]; then
    echo "❌ Python虚拟环境未找到"
    echo "请先运行: python3 -m venv .venv && source .venv/bin/activate"
    exit 1
fi

# 检查依赖
echo "🔍 检查依赖..."
$PYTHON_CMD -c "import requests, bs4" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅ 依赖检查通过"
else
    echo "❌ 缺少依赖，正在安装..."
    $PYTHON_CMD -m pip install requests beautifulsoup4 lxml
fi

echo ""
echo "📡 启动真实新闻抓取系统..."
echo "请选择抓取模式:"
echo "1) RSS抓取模式 (推荐，稳定)"
echo "2) 网站抓取模式 (实验性)"
echo "3) 演示模式 (兜底方案)"
echo ""

read -p "请输入选择 (1-3): " choice

case $choice in
    1)
        echo "🔄 启动RSS抓取模式..."
        $PYTHON_CMD real_news_display.py
        ;;
    2)
        echo "🔄 启动网站抓取模式..."
        $PYTHON_CMD real_news_crawler.py
        ;;
    3)
        echo "🔄 启动演示模式..."
        $PYTHON_CMD news_display.py
        ;;
    *)
        echo "❌ 无效选择，启动默认RSS模式..."
        $PYTHON_CMD real_news_display.py
        ;;
esac

echo ""
echo "✅ 运行完成！"
echo "💡 提示: 在浏览器中打开生成的HTML文件查看完整报告"
