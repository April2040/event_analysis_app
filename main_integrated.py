from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import json
import sys
from datetime import datetime
from pathlib import Path

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 导入模块
from modules.news_crawler.crawler import NewsWebCrawler
from utils_v2 import call_llm, generate_html_page

# 新闻缓存配置
import time
from typing import Dict, Any, Optional

class NewsCache:
    def __init__(self, cache_duration: int = 300):  # 5分钟缓存
        self.cache_duration = cache_duration
        self.cache: Dict[str, Any] = {}
        self.last_update: Optional[float] = None
    
    def is_valid(self) -> bool:
        if self.last_update is None:
            return False
        return time.time() - self.last_update < self.cache_duration
    
    def get_news(self) -> Optional[list]:
        if self.is_valid():
            return self.cache.get('news')
        return None
    
    def set_news(self, news_list: list) -> None:
        self.cache['news'] = news_list
        self.last_update = time.time()

# 全局新闻缓存实例
news_cache = NewsCache()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/temp", StaticFiles(directory="temp"), name="temp")
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
        
        # ✨ 新增：自动生成标准化HTML报告（基于认可的standalone版本）
        advanced_html_filepath = None
        try:
            from standardized_renderer import StandardizedRenderer
            renderer = StandardizedRenderer()
            advanced_html_filepath = renderer.render_to_html(temp_filepath)
            if advanced_html_filepath and Path(advanced_html_filepath).exists():
                print(f"🎨 标准化HTML报告已生成: {advanced_html_filepath}")
            else:
                print("⚠️ 标准化HTML生成失败")
        except Exception as e:
            print(f"⚠️ 标准化HTML生成失败: {e}")
        
        html_filename = None
        step2_time = 0
        
        # 根据用户选择决定是否生成HTML页面（不影响分析质量）
        if not fast_mode:  # 完整模式：包含专业HTML报告
            print("🎨 第二步：开始生成标准化HTML页面...")
            step2_start = time.time()
            
            # 使用标准化渲染器生成HTML（基于认可的standalone版本）
            try:
                from standardized_renderer import StandardizedRenderer
                renderer = StandardizedRenderer()
                # 直接使用已保存的TXT文件路径
                html_filepath = renderer.render_to_html(temp_filepath)
                step2_time = time.time() - step2_start
                
                if html_filepath and Path(html_filepath).exists():
                    # 读取生成的HTML内容用于返回
                    with open(html_filepath, "r", encoding="utf-8") as f:
                        html_content = f.read()
                    
                    print(f"✅ 标准化HTML页面生成完成！耗时: {step2_time:.2f}秒")
                    print(f"🌐 HTML页面已保存到: {html_filepath}")
                    
                    # 设置html_filename用于后续处理
                    html_filename = Path(html_filepath).name
                else:
                    print("❌ 标准化HTML生成失败，使用文本内容")
                    html_content = f"<pre>{analysis_result}</pre>"
                    step2_time = time.time() - step2_start
            except Exception as e:
                print(f"❌ 标准化HTML生成失败: {e}，使用文本内容")
                html_content = f"<pre>{analysis_result}</pre>"
                step2_time = time.time() - step2_start
        else:
            print("⚡ 快速模式：跳过HTML页面生成，节省时间（分析质量不变）")
        
        total_time = time.time() - start_time
        if step2_time > 0:
            print(f"🎉 任务完成！总耗时: {total_time:.2f}秒 (分析: {step1_time:.2f}s + HTML生成: {step2_time:.2f}s)")
        else:
            print(f"🎉 快速模式完成！总耗时: {total_time:.2f}秒 (仅深度分析)")
        
        # 处理HTML内容用于模板显示
        display_content = analysis_result
        
        # 准备返回数据，包含高级HTML信息
        template_data = {
            "request": request, 
            "result": display_content,
            "html_file": html_filename,
            "analysis_file": temp_filename,
            "processing_time": f"{total_time:.2f}秒"
        }
        
        # 如果生成了高级HTML，添加相关信息
        if advanced_html_filepath:
            advanced_html_filename = os.path.basename(advanced_html_filepath)
            template_data["advanced_html_file"] = advanced_html_filename
            template_data["has_advanced_html"] = True
            print(f"📊 高级可视化报告可用: {advanced_html_filename}")
        
        return templates.TemplateResponse("index.html", template_data)
        
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
    """新闻爬虫页面（带缓存优化）"""
    try:
        # 首先检查缓存
        cached_news = news_cache.get_news()
        if cached_news:
            print(f"🚀 使用缓存数据显示新闻页面：{len(cached_news)} 条新闻")
            # 格式化缓存的新闻为可分析的文本
            news_text = "=== 今日热点财经新闻（缓存数据，快速加载）===\n\n"
            for i, news in enumerate(cached_news, 1):
                news_text += f"{i}. 【{news.get('category', '财经')}】{news.get('title', '')}\n"
                news_text += f"   来源: {news.get('source', '')} | 热度: {news.get('heat_score', 0):.2f}\n"
                news_text += f"   摘要: {news.get('summary', news.get('description', ''))}\n"
                news_text += f"   链接: {news.get('url', '')}\n\n"
            
            return templates.TemplateResponse("index.html", {
                "request": request, 
                "result": None,
                "news_data": news_text,
                "news_count": len(cached_news)
            })
        
        print("🔥 启动新闻爬虫获取热点新闻...")
        start_time = time.time()
        crawler = NewsWebCrawler()
        news_list = crawler.get_top_hotspots(limit=10)
        fetch_time = time.time() - start_time
        
        # 更新缓存
        news_cache.set_news(news_list)
        
        print(f"✅ 成功获取并缓存 {len(news_list)} 条新闻（耗时: {fetch_time:.2f}秒）")
        
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
    """新闻API端点 - 返回JSON格式的新闻数据（带缓存优化）"""
    try:
        # 首先检查缓存
        cached_news = news_cache.get_news()
        if cached_news:
            print(f"� 使用缓存数据：{len(cached_news)} 条新闻（节省RSS请求时间）")
            return {
                "success": True,
                "news": cached_news,
                "count": len(cached_news),
                "timestamp": datetime.now().isoformat(),
                "cached": True
            }
        
        print("�🔥 API调用：获取热点新闻...")
        start_time = time.time()
        crawler = NewsWebCrawler()
        news_list = crawler.get_top_hotspots(limit=10)
        fetch_time = time.time() - start_time
        
        # 更新缓存
        news_cache.set_news(news_list)
        
        print(f"✅ 成功获取 {len(news_list)} 条新闻（耗时: {fetch_time:.2f}秒）")
        return {
            "success": True,
            "news": news_list,
            "count": len(news_list),
            "timestamp": datetime.now().isoformat(),
            "cached": False,
            "fetch_time": fetch_time
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
    print("🚀 性能优化:")
    print("  • RSS超时: 5秒（之前15秒）")
    print("  • AI API超时: 30秒")
    print("  • 新闻缓存: 5分钟")
    print("  • 缓存命中时响应时间 < 100ms")
    uvicorn.run(app, host="0.0.0.0", port=8002)