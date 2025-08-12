#!/bin/bash

echo "🚀 安装新闻抓取模块依赖..."

# 激活虚拟环境
if [ -f "../.venv/bin/activate" ]; then
    source ../.venv/bin/activate
    echo "✅ 虚拟环境已激活"
else
    echo "❌ 未找到虚拟环境，请先在主目录创建虚拟环境"
    exit 1
fi

# 安装依赖
pip install -r requirements.txt

echo "✅ 依赖安装完成"

# 创建数据目录
mkdir -p news_data
echo "✅ 数据目录已创建"

# 测试导入
python -c "
try:
    import requests
    import bs4
    import jieba
    print('✅ 所有依赖导入成功')
except ImportError as e:
    print(f'❌ 导入失败: {e}')
"

echo "🎯 新闻抓取模块安装完成！"
