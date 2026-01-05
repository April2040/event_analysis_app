
import uvicorn
import asyncio
import json
import os
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from deepseek_client import get_completion
from standardized_renderer import render_report
from utils import get_news

app = FastAPI()

# 挂载静态文件目录
app.mount("/static", StaticFiles(directory="static"), name="static")

# 设置模板目录
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/", response_class=HTMLResponse)
async def analyze_event(request: Request, user_input: str = Form(...), fast_mode: bool = Form(False)):
    try:
        # 调用模型进行分析
        analysis_result = get_completion(user_input)
        
        if fast_mode:
            # 快速模式：直接返回纯文本结果
            return HTMLResponse(f"<pre>{analysis_result}</pre>")
            
        # 标准模式：生成并渲染HTML报告
        report_path = await render_report(analysis_result)
        return RedirectResponse(url=f"/report/{os.path.basename(report_path)}", status_code=303)

    except Exception as e:
        # 异常处理：返回错误信息
        error_html = f"""
        <html>
            <head><title>分析失败</title></head>
            <body>
                <h1>分析过程中发生错误</h1>
                <p><strong>错误详情:</strong></p>
                <pre>{str(e)}</pre>
                <a href="/">返回重试</a>
            </body>
        </html>
        """
        return HTMLResponse(content=error_html, status_code=500)

@app.get("/report/{report_name}", response_class=HTMLResponse)
async def view_report(report_name: str):
    report_path = os.path.join("reports", report_name)
    if os.path.exists(report_path):
        with open(report_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse("<h1>报告未找到</h1>", status_code=404)

@app.get("/api/news")
async def api_news():
    try:
        news_data = await get_news()
        return {"success": True, "news": news_data}
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    # 确保 reports 目录存在
    if not os.path.exists("reports"):
        os.makedirs("reports")
        
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8002, 
        reload=True,
        log_level="info"
    )
