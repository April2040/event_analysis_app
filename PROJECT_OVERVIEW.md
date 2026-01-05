# 财经事件分析系统 - 项目结构总览

## 🎯 项目简介
财经事件分析系统是一个基于AI的智能财经新闻分析工具，能够自动抓取热点新闻、进行深度分析，并生成专业的HTML报告。

## 📂 核心文件结构

### 🚀 主要程序入口
```
├── main_integrated.py          # 主程序（FastAPI Web应用）
├── run.sh                      # 官方启动脚本 ⭐
└── stop.sh                     # 停止服务脚本
```

### 🎨 HTML渲染引擎
```
├── standardized_renderer.py    # 标准化HTML渲染器（最新）
├── generate_advanced_html.py   # 高级HTML生成器
└── convert_to_html.py          # 基础HTML转换工具
```

### 🛠️ 工具库
```
├── utils_v2.py                 # 核心工具库（AI分析 + HTML生成）
└── utils.py                    # 旧版工具库（兼容性保留）
```

### 📁 模块化组件
```
├── modules/
│   ├── news_analysis/          # 新闻分析模块
│   │   ├── analyzer.py         # 分析引擎
│   │   ├── deepseek_client.py  # AI客户端
│   │   ├── prompts.py          # 提示词管理
│   │   └── report_generator.py # 报告生成器
│   └── news_crawler/           # 新闻爬虫模块
│       ├── crawler.py          # 爬虫引擎
│       ├── config.py           # 配置管理
│       ├── html_generator.py   # HTML生成
│       └── utils.py            # 工具函数
```

### 📰 新闻模块
```
├── news_module/                # 新闻处理模块
│   ├── optimized_rss_crawler.py # RSS爬虫
│   ├── demo_reports/           # 演示报告
│   ├── news_data/              # 新闻数据
│   └── real_news_display/      # 实时新闻展示
```

### 🎨 前端资源
```
├── templates/                  # HTML模板
├── static/                     # 静态资源（CSS、JS）
└── prompts/
    └── system_prompt.txt       # 系统提示词
```

### 📊 输出目录
```
├── temp/                       # 临时文件（分析结果、HTML报告）
└── outputs/                    # 正式输出
    ├── analysis_reports/       # 分析报告
    └── news_reports/           # 新闻报告
```

### 📚 文档与配置
```
├── docs/                       # 项目文档
├── .env                        # 环境变量
├── .gitignore                  # Git忽略规则
└── venv/                       # Python虚拟环境
```

## 🔧 核心技术栈

### 后端框架
- **FastAPI** - 现代高性能Web框架
- **Uvicorn** - ASGI服务器
- **Python 3.13** - 主要编程语言

### AI与数据处理
- **OpenAI API** - AI分析引擎
- **BeautifulSoup4** - HTML解析
- **Requests** - HTTP请求
- **Jieba** - 中文分词

### 前端技术
- **HTML5/CSS3** - 现代Web标准
- **JavaScript** - 交互功能
- **响应式设计** - 适配各种设备

## 🎯 主要功能模块

### 1. 新闻抓取模块
- RSS源自动抓取
- 多源新闻聚合
- 实时热点监控

### 2. AI分析引擎
- 事件梳理
- 局面解读
- 底层逻辑分析
- 投资机会发现

### 3. HTML报告生成
- 标准化模板渲染
- 动态内容提取
- 专业视觉设计
- 响应式布局

### 4. Web界面
- 交互式分析界面
- 实时新闻展示
- 一键报告生成
- 文件下载功能

## 🚀 快速启动

### 1. 环境准备
```bash
cd /Users/qiyi/coding/event_analysis_app
source venv/bin/activate  # 激活虚拟环境
```

### 2. 启动服务
```bash
./run.sh
```

### 3. 访问地址
- **主页面**: http://localhost:8002
- **新闻页面**: http://localhost:8002/news

## 📈 版本历史

### v6.0.0+ (当前)
- ✅ 标准化HTML渲染器
- ✅ 动态内容提取
- ✅ 优化的样式系统
- ✅ 模块化架构

### v6.0.0 (2025-08-12)
- 🎨 高级HTML自动生成
- 📊 四模块卡片展示
- 🔄 自动化工作流

### v5.2.0 (2025-08-11)
- ⚡ 性能优化
- 📰 RSS缓存机制
- 🚀 响应时间提升

## 🔄 开发工作流

### 日常开发
1. 修改代码文件
2. 使用 `./run.sh` 重启服务
3. 访问界面测试功能
4. 提交到Git仓库

### 新功能开发
1. 在对应模块添加功能
2. 更新 `standardized_renderer.py` 模板
3. 测试HTML输出效果
4. 更新文档

## 🎨 设计哲学

### 模块化设计
- 清晰的功能分离
- 松耦合的组件架构
- 易于扩展和维护

### 用户体验
- 简洁直观的界面
- 快速响应的交互
- 专业的视觉呈现

### 技术优先
- 现代Web技术
- 高性能架构
- 可扩展设计

---

*最后更新: 2025年8月20日*
