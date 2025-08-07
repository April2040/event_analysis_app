from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import json
import sys
from datetime import datetime

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 导入模块
from modules.news_crawler.crawler import NewsWebCrawler
from utils_v2 import call_llm, generate_html_page

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def form_get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "result": None})

@app.post("/", response_class=HTMLResponse)
async def form_post(request: Request, user_input: str = Form(...), fast_mode: str = Form(None)):
    import time
    start_time = time.time()
    print(f"📥 收到用户输入: {user_input[:50]}...")
    print(f"📝 输入内容长度: {len(user_input)} 字符")
    print(f"⚡ 快速模式: {'是' if fast_mode else '否'}")
    
    try:
        # 第一步：生成深度事件分析（质量不妥协）
        with open("prompts/system_prompt.txt", "r", encoding="utf-8") as f:
            system_prompt = f.read()

        print("🔥 第一步：开始生成深度事件分析...")
        step1_start = time.time()
        analysis_result = call_llm(user_input, system_prompt)
        step1_time = time.time() - step1_start
        
        if "❌" in analysis_result:
            return templates.TemplateResponse("index.html", {"request": request, "result": analysis_result})
        
        print(f"✅ 深度分析完成！耗时: {step1_time:.2f}秒, 长度: {len(analysis_result)} 字符")
        
        # 保存分析结果到临时文件
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        temp_filename = f"temp_analysis_{timestamp}.txt"
        temp_filepath = os.path.join("temp", temp_filename)
        
        # 确保temp目录存在
        os.makedirs("temp", exist_ok=True)
        
        with open(temp_filepath, "w", encoding="utf-8") as f:
            f.write(analysis_result)
        
        print(f"💾 分析结果已保存到: {temp_filepath}")
        
        html_filename = None
        step2_time = 0
        
        # 根据用户选择决定是否生成HTML页面（不影响分析质量）
        if not fast_mode:  # 完整模式：包含专业HTML报告
            print("🎨 第二步：开始生成专业HTML页面...")
            step2_start = time.time()
            html_content = generate_html_page(analysis_result)
            step2_time = time.time() - step2_start
            
            if "❌" in html_content:
                return templates.TemplateResponse("index.html", {"request": request, "result": html_content})
            
            print(f"✅ HTML页面生成完成！耗时: {step2_time:.2f}秒, 长度: {len(html_content)} 字符")
            
            # 保存HTML页面到文件
            html_filename = f"analysis_report_{timestamp}.html"
            html_filepath = os.path.join("temp", html_filename)
            
            with open(html_filepath, "w", encoding="utf-8") as f:
                f.write(html_content)
            
            print(f"🌐 HTML页面已保存到: {html_filepath}")
        else:
            print("⚡ 快速模式：跳过HTML页面生成，节省时间（分析质量不变）")
        
        total_time = time.time() - start_time
        if step2_time > 0:
            print(f"🎉 任务完成！总耗时: {total_time:.2f}秒 (分析: {step1_time:.2f}s + HTML生成: {step2_time:.2f}s)")
        else:
            print(f"🎉 快速模式完成！总耗时: {total_time:.2f}秒 (仅深度分析)")
        
        # 处理HTML内容用于模板显示
        display_content = analysis_result
        
        return templates.TemplateResponse("index.html", {
            "request": request, 
            "result": display_content,
            "html_file": html_filename,
            "analysis_file": temp_filename,
            "processing_time": f"{total_time:.2f}秒"
        })
        
    except FileNotFoundError:
        error_msg = "❌ 系统提示词文件未找到"
        print(error_msg)
        return templates.TemplateResponse("index.html", {"request": request, "result": error_msg})
    except Exception as e:
        error_msg = f"❌ 处理过程中出现错误：{str(e)}"
        print(error_msg)
        return templates.TemplateResponse("index.html", {"request": request, "result": error_msg})

@app.get("/news", response_class=HTMLResponse)
async def get_news(request: Request):
    """新闻爬虫页面"""
    try:
        print("🔥 启动新闻爬虫获取热点新闻...")
        crawler = NewsWebCrawler()
        news_list = crawler.get_top_hotspots(limit=10)
        
        # 格式化新闻为可分析的文本
        news_text = "=== 今日热点财经新闻 ===\n\n"
        for i, news in enumerate(news_list, 1):
            news_text += f"{i}. 【{news.get('category', '财经')}】{news.get('title', '')}\n"
            news_text += f"   来源: {news.get('source', '')} | 热度: {news.get('heat_score', 0):.2f}\n"
            news_text += f"   摘要: {news.get('summary', news.get('description', ''))}\n"
            news_text += f"   链接: {news.get('url', '')}\n\n"
        
        return templates.TemplateResponse("index.html", {
            "request": request, 
            "result": None,
            "news_data": news_text,
            "news_count": len(news_list)
        })
        
    except Exception as e:
        error_msg = f"❌ 新闻获取失败：{str(e)}"
        print(error_msg)
        return templates.TemplateResponse("index.html", {"request": request, "result": error_msg})

@app.get("/api/news")
async def get_news_api():
    """新闻API端点 - 返回JSON格式的新闻数据"""
    try:
        print("🔥 API调用：获取热点新闻...")
        crawler = NewsWebCrawler()
        news_list = crawler.get_top_hotspots(limit=10)
        
        print(f"✅ 成功获取 {len(news_list)} 条新闻")
        return {
            "success": True,
            "news": news_list,
            "count": len(news_list),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        error_msg = f"获取新闻失败：{str(e)}"
        print(f"❌ {error_msg}")
        return {
            "success": False,
            "error": error_msg,
            "news": [],
            "count": 0
        }

@app.get("/temp/{filename}")
async def get_temp_file(filename: str):
    """获取临时文件"""
    file_path = os.path.join("temp", filename)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        if filename.endswith('.html'):
            return HTMLResponse(content=content)
        else:
            return {"content": content}
    else:
        return {"error": "文件不存在"}

if __name__ == "__main__":
    import uvicorn
    print("🚀 启动财经事件分析系统...")
    print("📊 功能: 智能分析 + 新闻爬虫")
    print("🌐 访问: http://localhost:8002")
    print("📰 新闻: http://localhost:8002/news")
    print("⚡ 快速模式: 仅生成分析，节省50%时间")
    print("💡 完整模式: 分析 + 专业HTML报告")
    uvicorn.run(app, host="0.0.0.0", port=8002)