# 🔧 财经事件分析应用 - 故障排除指南

## ✅ 问题已解决！

**问题**: 点击图标后显示"无法访问网站"  
**原因**: 启动器脚本路径错误 + 浏览器打开时机过早  
**解决方案**: 修复路径并增加服务就绪检测  

## 🎯 现在的工作流程

### 1. 点击图标后的执行过程
```
1. 启动器打开终端
2. 在终端中执行 ./start_optimized.sh
3. 后台等待服务启动完成 (最多60秒)
4. 检测到端口8002可访问后自动打开浏览器
5. 如果超时，会在日志中记录提示信息
```

### 2. 验证启动成功
```bash
# 检查服务是否运行
lsof -i :8002

# 测试网页访问
curl http://localhost:8002

# 查看启动日志
cat ~/coding/event_analysis_app/logs/app_launcher_*.log | tail -5
```

## 🚀 使用方式

### 方法1: Launchpad点击 (推荐)
1. 四指捏合打开Launchpad
2. 搜索"财经事件分析"
3. 点击图标启动

### 方法2: Spotlight快速启动
1. `⌘ + 空格`
2. 输入"财经事件分析"
3. 回车启动

### 方法3: Dock固定启动
1. 右键Dock中的图标
2. 选择"选项" → "在程序坞中保留"
3. 以后直接点击Dock图标

## 🔍 可能的问题与解决

### 问题1: 终端打开但没有启动服务
**解决**: 在终端手动运行
```bash
cd /Users/qiyi/coding/event_analysis_app
./start_optimized.sh
```

### 问题2: 服务启动但浏览器没打开
**解决**: 手动访问 `http://localhost:8002`

### 问题3: 图标仍为白板
**解决**: 重启macOS或运行
```bash
cd /Users/qiyi/coding/event_analysis_app
./refresh_icon.sh
```

### 问题4: 权限被拒绝
**解决**: 重新赋予权限
```bash
xattr -rc ~/Applications/EventAnalysis.app
chmod +x ~/Applications/EventAnalysis.app/Contents/MacOS/launcher
```

## 📱 服务管理命令

```bash
# 进入项目目录
cd /Users/qiyi/coding/event_analysis_app

# 启动服务
./start_optimized.sh

# 检查状态
./status.sh

# 快速重启
./restart.sh

# 停止服务
./stop_optimized.sh
```

## 🎉 成功标志

启动成功后您会看到：
- ✅ 终端显示启动信息
- ✅ 浏览器自动打开到 `http://localhost:8002`
- ✅ 网页显示"财经事件分析系统"界面
- ✅ 日志文件记录"服务已启动，打开浏览器..."

---

**现在您的财经事件分析应用已经完全配置好，可以像使用任何原生macOS应用一样一键启动！** 🚀