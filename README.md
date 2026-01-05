# 📊 财经事件分析系统

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

**基于DeepSeek AI的智能财经新闻分析工具**

[快速开始](#-快速开始) • [功能特性](#-核心功能) • [在线部署](#-在线部署) • [文档](#-项目文档)

</div>

---

## 🎯 项目简介

财经事件分析系统是一个**AI驱动的智能财经分析工具**，能够：
- 🤖 自动抓取财经热点新闻
- 🧠 进行深度AI分析（四维度分析）
- 📊 生成专业HTML可视化报告
- 💹 发现投资机会和风险提示

### ✨ 核心特性
- **AI分析引擎**：基于DeepSeek Reasoner模型
- **四模块分析**：事件梳理 → 局面评估 → 底层逻辑 → 投资映射
- **新闻聚合**：整合10+主流财经媒体RSS源
- **专业报告**：标准化HTML渲染，可复制、下载、打印
- **响应式设计**：适配桌面和移动设备

---

## 🖥️ 界面预览

```
主页面：http://localhost:8002/
├── 事件分析输入框
├── 快速模式 / 标准模式切换
└── 实时新闻页面入口

分析报告：
┌─────────────────────────────────────┐
│  🟥 事件梳理                        │
│  - 时间线、关键数据、相关方          │
├─────────────────────────────────────┤
│  🟧 局面评估                        │
│  - 市场影响、行业态势、机会风险      │
├─────────────────────────────────────┤
│  🟩 底层逻辑                        │
│  - 因果关系、政策逻辑、趋势判断      │
├─────────────────────────────────────┤
│  💹 投资映射                        │
│  - 相关标的、投资逻辑、风险提示      │
└─────────────────────────────────────┘
```

---

## 🚀 快速开始

### 方案1：本地运行（推荐用于开发）

#### 环境要求
- Python 3.11+
- macOS / Linux / Windows

#### 安装步骤
```bash
# 1. 克隆项目
git clone https://github.com/April2040/event_analysis_app.git
cd event_analysis_app

# 2. 创建虚拟环境
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置环境变量
cp .env.example .env
# 编辑.env文件，填入DeepSeek API密钥

# 5. 启动服务
python main_integrated.py
# 或使用uvicorn: uvicorn main_integrated:app --reload --port 8002
```

#### 访问应用
- **主页**：http://localhost:8002
- **新闻页**：http://localhost:8002/news

---

### 方案2：Docker部署（推荐用于生产）

```bash
# 使用Docker Compose（最简单）
docker-compose up -d

# 或使用Docker命令
docker build -t event-analysis-app .
docker run -d -p 8002:8002 \
  -e DEEPSEEK_API_KEY="your_api_key" \
  --name event-analysis \
  event-analysis-app
```

---

### 方案3：一键部署到云平台

#### Railway部署（3分钟完成）
1. 访问 [Railway](https://railway.app)
2. 选择 "Deploy from GitHub repo"
3. 选择此项目仓库
4. 添加环境变量 `DEEPSEEK_API_KEY`
5. 自动部署完成 ✅

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template)

#### Render部署
1. 访问 [Render](https://render.com)
2. 创建Web Service，连接此仓库
3. 配置启动命令：`uvicorn main_integrated:app --host 0.0.0.0 --port $PORT`
4. 添加环境变量，点击部署

详细部署指南：[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

---

## 📋 核心功能

### 1. 智能新闻抓取
- **多源聚合**：整合新浪财经、凤凰财经、华尔街日报等
- **智能过滤**：基于关键词库自动识别财经内容
- **热度评分**：自动评估新闻重要性
- **分类管理**：10+类别（股市、货币、宏观、科技等）

### 2. AI深度分析
#### 四大分析维度
| 模块 | 功能 | 输出 |
|------|------|------|
| 🟥 **事件梳理** | 事实信息提取 | 时间线、数据、相关方 |
| 🟧 **局面评估** | 当前态势分析 | 影响范围、机会风险 |
| 🟩 **底层逻辑** | 深层机制解读 | 因果关系、趋势判断 |
| 💹 **投资映射** | 投资机会发现 | 相关标的、投资逻辑 |

### 3. 专业报告生成
- **标准化模板**：基于认可的设计规范
- **动态渲染**：自动提取和格式化内容
- **交互功能**：一键复制、下载、打印
- **响应式布局**：完美适配各种设备

### 4. Web交互界面
- **简洁输入**：支持文本/URL输入
- **双模式**：快速模式(纯文本) / 标准模式(HTML)
- **实时反馈**：处理状态实时显示
- **历史记录**：自动保存分析结果

---

## 🛠️ 技术架构

### 技术栈
```
├── Backend
│   ├── FastAPI (Web框架)
│   ├── Uvicorn (ASGI服务器)
│   ├── Python 3.11+
│   └── DeepSeek API (AI引擎)
│
├── Frontend
│   ├── HTML5/CSS3
│   ├── JavaScript
│   └── Jinja2模板
│
├── Data Processing
│   ├── BeautifulSoup4 (HTML解析)
│   ├── Jieba (中文分词)
│   └── Requests (HTTP客户端)
│
└── Deployment
    ├── Docker
    ├── GitHub Actions (CI/CD)
    └── Railway/Render (云平台)
```

### 项目结构
```
event_analysis_app/
├── main_integrated.py          # FastAPI主应用
├── standardized_renderer.py    # HTML渲染器
├── utils_v2.py                 # 核心工具库
├── modules/
│   ├── news_analysis/          # AI分析模块
│   │   ├── analyzer.py
│   │   ├── deepseek_client.py
│   │   └── report_generator.py
│   └── news_crawler/           # 新闻爬虫模块
│       ├── crawler.py
│       ├── config.py
│       └── html_generator.py
├── templates/                  # HTML模板
├── static/                     # 静态资源
├── outputs/                    # 分析报告输出
└── temp/                       # 临时文件
```

---

## 📖 项目文档

| 文档 | 说明 |
|------|------|
| [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) | 项目架构详解 |
| [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) | 部署完整指南 |
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | 问题排查手册 |
| [CHANGELOG.md](CHANGELOG.md) | 版本更新日志 |

---

## 🔧 配置说明

### 环境变量
```bash
# .env文件配置
DEEPSEEK_API_KEY=your_api_key_here  # DeepSeek API密钥（必需）
HOST=0.0.0.0                        # 服务器地址
PORT=8002                           # 服务器端口
DEBUG=False                         # 调试模式
NEWS_CACHE_DURATION=300            # 新闻缓存时间（秒）
```

### API密钥获取
1. 访问 [DeepSeek开放平台](https://platform.deepseek.com/)
2. 注册并登录账号
3. 创建API密钥
4. 复制密钥到.env文件

---

## 🎯 使用示例

### 命令行启动
```bash
# 激活虚拟环境
source .venv/bin/activate

# 方式1：直接运行主程序
python main_integrated.py

# 方式2：使用uvicorn（支持热重载）
uvicorn main_integrated:app --reload --port 8002

# 方式3：生产环境部署
uvicorn main_integrated:app --host 0.0.0.0 --port 8002 --workers 4
```

### API调用示例
```python
import requests

# 提交分析任务
response = requests.post('http://localhost:8002/', 
    data={'user_input': '分析美联储加息对A股的影响'})

# 获取新闻数据
news = requests.get('http://localhost:8002/api/news')
print(news.json())
```

---

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

### 开发流程
1. Fork本仓库
2. 创建特性分支：`git checkout -b feature/AmazingFeature`
3. 提交更改：`git commit -m 'Add some AmazingFeature'`
4. 推送分支：`git push origin feature/AmazingFeature`
5. 提交Pull Request

### 代码规范
- 遵循PEP 8 Python代码规范
- 添加必要的注释和文档字符串
- 提交前运行代码检查：`flake8 .`

---

## 📊 性能指标

| 指标 | 数值 |
|------|------|
| 分析速度 | 10-15秒/次 |
| 新闻缓存 | 5分钟 |
| 并发支持 | 100+ 用户 |
| 报告生成 | 1-2秒 |
| 内存占用 | ~200MB |

---

## 🔐 安全说明

- ⚠️ **API密钥保护**：确保.env文件不被提交到Git
- ⚠️ **生产部署**：使用HTTPS和环境变量管理
- ⚠️ **访问控制**：根据需要添加身份验证
- ⚠️ **数据备份**：定期备份分析报告

---

## 📝 许可证

本项目采用 [MIT License](LICENSE) 开源协议。

---

## 📮 联系方式

- **GitHub**: [@April2040](https://github.com/April2040)
- **项目主页**: https://github.com/April2040/event_analysis_app
- **问题反馈**: [Issues](https://github.com/April2040/event_analysis_app/issues)

---

## 🙏 致谢

- [DeepSeek AI](https://www.deepseek.com/) - 提供强大的AI分析能力
- [FastAPI](https://fastapi.tiangolo.com/) - 现代化的Web框架
- 所有开源贡献者和用户

---

## ⭐ Star History

如果这个项目对您有帮助，请给个Star支持一下！

[![Star History Chart](https://api.star-history.com/svg?repos=April2040/event_analysis_app&type=Date)](https://star-history.com/#April2040/event_analysis_app&Date)

---

<div align="center">

**[⬆ 返回顶部](#-财经事件分析系统)**

Made with ❤️ by April2040

</div>
