from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import json
from datetime import datetime
from utils import call_llm, generate_html_page
from modules.news_crawler.crawler import NewsWebCrawler

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# 创建新闻爬虫实例
news_crawler = NewsWebCrawler()

@app.get("/api/news")
async def get_news():
    """获取新闻数据API端点"""
    try:
        # 首先尝试从RSS Feed获取新闻
        news_list = news_crawler.get_news_from_rss_feeds()
        
        # 如果RSS Feed获取失败，尝试RSS Sources
        if not news_list:
            news_list = news_crawler.get_news_from_rss_sources()
        
        # 检查获取到的新闻质量 - 如果标题只是网站名称，则使用备用新闻
        if not news_list or all(
            news.get("title", "") in ["腾讯网", "网易财经-有态度的财经门户", "财经", "新浪财经", "东方财富网"] or
            any(site in news.get("title", "") for site in ["腾讯", "网易", "搜狐", "新浪", "东方财富"])
            for news in news_list
        ):
            print("📰 RSS源质量不佳，使用今日热点财经新闻...")
            news_list = news_crawler.get_enhanced_backup_news()
        
        return {
            "success": True,
            "news": news_list[:20],  # 返回前20条新闻
            "total": len(news_list),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        # 出错时也使用备用新闻
        try:
            news_list = news_crawler.get_enhanced_backup_news()
            return {
                "success": True,
                "news": news_list[:20],
                "total": len(news_list),
                "timestamp": datetime.now().isoformat(),
                "fallback": True
            }
        except:
            return {
                "success": False,
                "error": str(e),
                "news": [],
                "timestamp": datetime.now().isoformat()
            }

@app.get("/", response_class=HTMLResponse)
async def form_get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "result": None})

@app.post("/", response_class=HTMLResponse)
async def form_post(request: Request, user_input: str = Form(...)):
    print(f"收到用户输入: {user_input[:50]}...")
    
    try:
        # 第一步：生成事件分析内容
        with open("prompts/system_prompt.txt", "r", encoding="utf-8") as f:
            system_prompt = f.read()

        print("📊 第一步：开始生成事件分析...")
        analysis_result = call_llm(user_input, system_prompt)
        
        if "❌" in analysis_result:
            return templates.TemplateResponse("index.html", {"request": request, "result": analysis_result})
        
        print(f"✅ 事件分析完成，长度: {len(analysis_result)} 字符")
        
        # 保存分析结果到临时文件
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        temp_filename = f"temp_analysis_{timestamp}.txt"
        temp_filepath = os.path.join("temp", temp_filename)
        
        # 确保temp目录存在
        os.makedirs("temp", exist_ok=True)
        
        with open(temp_filepath, "w", encoding="utf-8") as f:
            f.write(analysis_result)
        
        print(f"📝 分析结果已保存到: {temp_filepath}")
        
        # 第二步：生成专业HTML页面
        print("🎨 第二步：开始生成专业HTML页面...")
        html_content = generate_html_page(analysis_result)
        
        if "❌" in html_content:
            return templates.TemplateResponse("index.html", {"request": request, "result": f"分析完成，但HTML生成失败：\n{html_content}"})
        
        print(f"✅ HTML页面生成完成，长度: {len(html_content)} 字符")
        
        # 保存生成的HTML
        html_filename = f"generated_report_{timestamp}.html"
        html_filepath = os.path.join("temp", html_filename)
        
        with open(html_filepath, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        print(f"🌐 HTML报告已保存到: {html_filepath}")
        
        # 创建元数据
        metadata = {
            "timestamp": timestamp,
            "user_input": user_input,
            "analysis_file": temp_filename,
            "html_file": html_filename,
            "analysis_length": len(analysis_result),
            "html_length": len(html_content)
        }
        
        # 返回生成的HTML内容
        return HTMLResponse(content=html_content)
        
    except Exception as e:
        error_msg = f"❌ 处理过程中发生错误: {str(e)}"
        print(error_msg)
        return templates.TemplateResponse("index.html", {"request": request, "result": error_msg})

@app.get("/reports")
async def list_reports():
    """列出所有生成的报告"""
    try:
        if not os.path.exists("temp"):
            return {"reports": []}
        
        files = os.listdir("temp")
        html_files = [f for f in files if f.endswith('.html')]
        html_files.sort(reverse=True)  # 最新的在前面
        
        reports = []
        for html_file in html_files:
            timestamp = html_file.replace('generated_report_', '').replace('.html', '')
            reports.append({
                "filename": html_file,
                "timestamp": timestamp,
                "url": f"/report/{html_file}"
            })
        
        return {"reports": reports}
    except Exception as e:
        return {"error": str(e)}

@app.get("/reports/view", response_class=HTMLResponse)
async def reports_page(request: Request):
    """报告列表页面"""
    return templates.TemplateResponse("reports.html", {"request": request})

@app.get("/report/{filename}")
async def get_report(filename: str):
    """获取指定的报告"""
    try:
        filepath = os.path.join("temp", filename)
        if not os.path.exists(filepath):
            return HTMLResponse(content="<h1>报告未找到</h1>", status_code=404)
        
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        return HTMLResponse(content=content)
    except Exception as e:
        return HTMLResponse(content=f"<h1>错误: {str(e)}</h1>", status_code=500)
