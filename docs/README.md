# 🧠 热点事件分析器

基于DeepSeek AI的智能事件分析工具，能够对热点事件进行多维度深度分析。

## 📋 功能特点

- **事件分析**：对热点事件进行全面分析
- **局面解读**：分析当前态势和影响
- **结构洞察**：揭示深层制度和经济结构
- **投资建议**：提供专业的投资映射和风险分析

## 🚀 快速开始

### 1. 安装依赖

```bash
# 激活虚拟环境
source .venv/bin/activate

# 安装依赖包
pip install fastapi uvicorn jinja2 python-multipart openai python-dotenv
```

### 2. 配置API密钥

创建 `.env` 文件并添加你的DeepSeek API密钥：

```bash
DEEPSEEK_API_KEY=你的DeepSeek API密钥
```

### 3. 启动应用

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### 4. 访问应用

打开浏览器访问：http://127.0.0.1:8000

## 📁 项目结构

```
event_analysis_app/
├── main.py              # FastAPI主应用
├── utils.py             # LLM调用工具
├── .env                 # 环境变量配置
├── .gitignore          # Git忽略文件
├── README.md           # 项目说明
├── prompts/
│   └── system_prompt.txt  # 系统提示词
├── templates/
│   └── index.html         # 前端模板
└── static/
    └── style.css          # 样式文件
```

## 🛠️ 技术栈

- **后端**: FastAPI
- **前端**: HTML + Jinja2 模板
- **AI模型**: DeepSeek API
- **部署**: Uvicorn

## 📝 使用说明

1. 在输入框中描述一个热点事件
2. 点击"🔍 开始分析"按钮
3. 等待AI分析完成（通常10-30秒）
4. 查看详细的分析结果

## 🔧 开发

```bash
# 开发模式启动
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

## 📄 许可证

MIT License
