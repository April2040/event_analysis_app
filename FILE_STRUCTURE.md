# 财经事件分析系统 - 文件结构说明

## 🚀 启动方式

**主启动脚本**: `./run.sh`
```bash
cd /Users/qiyi/coding/event_analysis_app
./run.sh
```

## 📁 核心文件结构

### 🎯 主程序文件
- **main_integrated.py** - 主程序 (v6.0.0，集成高级HTML生成)
- **utils_v2.py** - 核心工具库 (AI分析 + HTML生成)
- **run.sh** - 官方启动脚本 ⭐

### 🎨 HTML生成工具
- **generate_advanced_html.py** - 独立高级HTML生成器
- **convert_to_html.py** - 基础HTML转换工具

### 🗂️ 其他重要文件
- **stop.sh** - 停止服务脚本
- **utils.py** - 旧版工具库 (兼容性保留)
- **verify_system.sh** - 系统验证脚本

## ✅ 已清理的文件

以下过时/重复文件已删除：
- ❌ `start_news_system.sh` (空文件)
- ❌ `quick_news_interactive.sh` (空文件)  
- ❌ `test_optimized_rss.sh` (空文件)
- ❌ `start_background.sh` (功能重复)
- ❌ `main_modular.py` (过时版本)
- ❌ `launch_modular.sh` (过时版本)
- ❌ `launch_integrated.sh` (端口配置过时)
- ❌ `main.py` (旧版本，使用utils而非utils_v2)
- ❌ `start.sh` (功能重复)

## 🎯 使用指南

### 启动系统
```bash
./run.sh
```

### 访问地址
- **主页面**: http://localhost:8002
- **新闻页面**: http://localhost:8002/news

### 停止服务
```bash
./stop.sh
# 或者在终端按 Ctrl+C
```

## 📋 功能特性

✅ **AI深度分析** - DeepSeek驱动的财经事件分析
✅ **RSS新闻爬取** - 实时热点财经新闻
✅ **高级HTML报告** - 专业可视化报告自动生成
✅ **四模块分析** - 事件/局面/结构/投资完整框架
✅ **性能优化** - 缓存系统、超时控制
✅ **响应式设计** - 现代Web界面

## 🔧 维护说明

- **核心逻辑**: main_integrated.py + utils_v2.py
- **前端模板**: templates/index.html
- **静态资源**: static/ + temp/
- **配置文件**: .env (需要DEEPSEEK_API_KEY)
- **虚拟环境**: .venv/

---

**版本**: v6.0.0
**最后更新**: 2025年8月17日
**状态**: 生产就绪 ✅
