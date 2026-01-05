# 🚀 部署指南

## 📌 GitHub vs 在线部署的区别

### GitHub仓库的作用
- ✅ **代码托管**：存储和版本控制
- ✅ **协作开发**：团队协作、代码审查
- ✅ **文档展示**：README、项目介绍
- ✅ **CI/CD自动化**：自动测试、构建
- ❌ **不能运行应用**：GitHub不是服务器

### 实现在线访问的方法
需要将应用部署到云平台，才能像本地一样访问完整功能。

---

## 🌐 部署方案对比

| 平台 | 免费额度 | 复杂度 | 推荐度 | 特点 |
|------|---------|--------|--------|------|
| **Railway** | ✅ $5/月 | ⭐ 简单 | ⭐⭐⭐⭐⭐ | 最简单，一键部署 |
| **Render** | ✅ 750h/月 | ⭐⭐ 中等 | ⭐⭐⭐⭐ | 稳定，文档完善 |
| **Fly.io** | ✅ 有限制 | ⭐⭐ 中等 | ⭐⭐⭐⭐ | 性能好，全球部署 |
| **Heroku** | ❌ 无免费 | ⭐⭐ 中等 | ⭐⭐⭐ | 老牌平台，需付费 |
| **Vercel** | ✅ 慷慨 | ⭐⭐⭐ 复杂 | ⭐⭐⭐ | 适合前端，后端受限 |
| **Docker+VPS** | ❌ 需付费 | ⭐⭐⭐⭐ 复杂 | ⭐⭐⭐⭐⭐ | 完全控制，需运维 |

---

## 🎯 推荐方案：Railway部署（最简单）

### 步骤1：准备工作
1. 确保代码已推送到GitHub
2. 注册Railway账号：https://railway.app
3. 准备DeepSeek API密钥

### 步骤2：一键部署
1. 登录Railway
2. 点击 "New Project" → "Deploy from GitHub repo"
3. 选择 `event_analysis_app` 仓库
4. Railway会自动检测Python项目并部署

### 步骤3：配置环境变量
在Railway项目设置中添加：
```
DEEPSEEK_API_KEY=你的API密钥
PORT=8002
```

### 步骤4：访问应用
部署完成后，Railway会提供一个公开URL，如：
```
https://event-analysis-app.up.railway.app
```

---

## 🐳 方案2：Docker部署

### 本地测试
```bash
# 1. 构建镜像
docker build -t event-analysis-app .

# 2. 运行容器
docker run -d \
  -p 8002:8002 \
  -e DEEPSEEK_API_KEY="your_api_key" \
  --name event-analysis \
  event-analysis-app

# 3. 访问应用
open http://localhost:8002
```

### Docker Compose（推荐）
```bash
# 1. 设置环境变量
cp .env.example .env
# 编辑 .env 填入API密钥

# 2. 启动服务
docker-compose up -d

# 3. 查看日志
docker-compose logs -f

# 4. 停止服务
docker-compose down
```

---

## 🔧 方案3：Render部署

### 步骤1：准备
1. 注册Render账号：https://render.com
2. 连接GitHub仓库

### 步骤2：创建Web Service
1. 点击 "New" → "Web Service"
2. 选择 `event_analysis_app` 仓库
3. 配置如下：
   - **Name**: event-analysis-app
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main_integrated:app --host 0.0.0.0 --port $PORT`

### 步骤3：添加环境变量
在Render控制台添加：
```
DEEPSEEK_API_KEY=你的API密钥
```

### 步骤4：部署
点击 "Create Web Service"，等待部署完成。

---

## ⚙️ GitHub Actions自动化（已配置）

### 自动化功能
项目已配置GitHub Actions，每次推送代码会自动：
1. ✅ 运行代码质量检查
2. ✅ 验证项目结构
3. ✅ 测试模块导入
4. ✅ 检查依赖完整性

### 查看运行结果
访问：https://github.com/April2040/event_analysis_app/actions

---

## 🔐 安全注意事项

### 1. 保护API密钥
```bash
# ❌ 错误：直接写在代码里
api_key = "sk-d7155044d7bd426ba0307ae7eb67c8bd"

# ✅ 正确：使用环境变量
import os
api_key = os.getenv('DEEPSEEK_API_KEY')
```

### 2. 更新.gitignore
确保敏感文件不被提交：
```gitignore
.env
*.log
__pycache__/
.venv/
```

### 3. 使用Secret管理
- GitHub: Settings → Secrets → Actions
- Railway: Variables → Add Variable
- Render: Environment → Add Environment Variable

---

## 📊 部署后验证

### 健康检查
```bash
# 检查服务是否运行
curl https://your-app-url.com/

# 检查API响应
curl https://your-app-url.com/api/news
```

### 性能监控
- Railway提供内置监控面板
- Render提供日志和指标
- 可集成第三方监控（如Sentry、DataDog）

---

## 🐛 常见问题

### Q1: 部署后无法访问？
**A**: 检查端口配置，云平台通常使用 `$PORT` 环境变量。

### Q2: API密钥不生效？
**A**: 确认环境变量名称正确，重启服务。

### Q3: 部署超时？
**A**: 检查依赖安装是否卡住，可以减少不必要的依赖。

### Q4: 内存不足？
**A**: 升级到付费计划或优化代码内存使用。

---

## 📈 成本估算

### 免费方案
- **Railway**: $5免费额度/月（约5美元）
- **Render**: 750小时/月免费（够用）
- **Fly.io**: 3个共享CPU免费

### 付费方案（如需更高性能）
- **Railway**: $10-20/月
- **Render**: $7-25/月
- **AWS/GCP**: $5-50/月（按需）

---

## 🎓 学习资源

- [Railway文档](https://docs.railway.app/)
- [Render文档](https://render.com/docs)
- [Docker教程](https://docs.docker.com/get-started/)
- [FastAPI部署指南](https://fastapi.tiangolo.com/deployment/)

---

## 💡 推荐流程

1. **开发阶段**：本地运行测试
2. **测试阶段**：Docker容器化测试
3. **部署阶段**：Railway/Render一键部署
4. **生产阶段**：根据流量选择合适方案

**对于个人项目，推荐直接使用Railway，3分钟即可完成部署！**
