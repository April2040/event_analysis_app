#!/bin/bash

echo "🔧 强制刷新财经事件分析应用图标"
echo "================================="

# 确保应用在正确位置
if [ ! -d ~/Applications/EventAnalysis.app ]; then
    echo "❌ 应用未找到，正在复制..."
    cp -R /Users/qiyi/coding/event_analysis_app/macOS/EventAnalysis.app ~/Applications/
fi

# 验证图标文件
ICON_PATH=~/Applications/EventAnalysis.app/Contents/Resources/app.icns
if [ -f "$ICON_PATH" ]; then
    echo "✅ 图标文件存在: $(ls -lh "$ICON_PATH" | awk '{print $5}')"
else
    echo "❌ 图标文件缺失，正在创建..."
    cd /Users/qiyi/coding/event_analysis_app
    source venv/bin/activate
    python create_icon.py
fi

# 清除扩展属性（隔离标记）
echo "🧹 清除隔离属性..."
xattr -rc ~/Applications/EventAnalysis.app

# 强制系统重新扫描图标
echo "🔄 清除图标缓存..."
sudo rm -rf /Library/Caches/com.apple.iconservices.store 2>/dev/null || true
sudo find /private/var/folders/ -name com.apple.iconservices -exec rm -rf {} \; 2>/dev/null || true

# 重建 Launch Services 数据库
echo "🗃️ 重建 Launch Services 数据库..."
/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister \
    -kill -r -domain local -domain system -domain user

# 重启系统UI组件
echo "🔄 重启 Dock 和 Finder..."
killall Dock 2>/dev/null || true
killall Finder 2>/dev/null || true

# 触发应用重新注册
echo "📱 触发应用重新注册..."
touch ~/Applications/EventAnalysis.app
sleep 1

echo ""
echo "✅ 图标刷新完成！"
echo ""
echo "📌 验证步骤："
echo "1. 打开 Launchpad (四指捏合)"
echo "2. 搜索「财经事件分析」或「EventAnalysis」"
echo "3. 如仍为白板图标，请重启 macOS"
echo ""
echo "🚀 如果图标正确显示，可以将应用固定到 Dock："
echo "   右键点击 Dock 中的图标 → 选项 → 在程序坞中保留"

# 打开 Applications 文件夹供查看
open ~/Applications/

echo ""
echo "📂 已打开应用程序文件夹供您验证"