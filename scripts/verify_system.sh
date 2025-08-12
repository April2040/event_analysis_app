#!/bin/bash

echo "🚀 启动事件分析器功能验证"
echo "================================="

# 检查服务器状态
echo "📡 检查服务器状态..."
if curl -s http://127.0.0.1:8001/ > /dev/null; then
    echo "✅ 主页面正常访问"
else
    echo "❌ 主页面无法访问"
    exit 1
fi

# 检查报告API
echo "📊 检查报告API..."
REPORTS=$(curl -s http://127.0.0.1:8001/reports)
if echo "$REPORTS" | grep -q "reports"; then
    echo "✅ 报告API正常工作"
    REPORT_COUNT=$(echo "$REPORTS" | grep -o "filename" | wc -l)
    echo "📈 当前有 $REPORT_COUNT 个历史报告"
else
    echo "❌ 报告API异常"
fi

# 检查报告页面
echo "🌐 检查报告页面..."
if curl -s http://127.0.0.1:8001/reports/view > /dev/null; then
    echo "✅ 报告页面正常访问"
else
    echo "❌ 报告页面无法访问"
fi

# 检查temp目录
echo "📁 检查temp目录..."
if [ -d "temp" ]; then
    HTML_FILES=$(ls temp/*.html 2>/dev/null | wc -l)
    TXT_FILES=$(ls temp/*.txt 2>/dev/null | wc -l)
    echo "✅ temp目录存在"
    echo "   📄 HTML报告: $HTML_FILES 个"
    echo "   📝 文本分析: $TXT_FILES 个"
else
    echo "❌ temp目录不存在"
fi

echo ""
echo "🎯 功能测试完成！"
echo ""
echo "📱 访问方式："
echo "   主页面: http://127.0.0.1:8001"
echo "   历史报告: http://127.0.0.1:8001/reports/view"
echo "   报告API: http://127.0.0.1:8001/reports"
echo ""
echo "💡 使用提示："
echo "   1. 在主页面输入事件描述进行分析"
echo "   2. 等待两步AI处理完成（30-60秒）"
echo "   3. 查看生成的专业HTML报告"
echo "   4. 通过历史报告页面查看过往分析"
