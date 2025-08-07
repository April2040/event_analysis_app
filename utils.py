# utils.py
from openai import OpenAI
import os
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

def call_llm(user_input: str, system_prompt: str, model="deepseek-chat") -> str:
    print(f"开始处理LLM请求，模型: {model}")
    
    # 检查API密钥
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        print("❌ API密钥未设置")
        return "❌ 错误：请设置 DEEPSEEK_API_KEY 环境变量。\n\n请在 .env 文件中添加：\nDEEPSEEK_API_KEY=你的DeepSeek API密钥"
    
    print("✅ API密钥已设置，开始调用DeepSeek API...")
    
    try:
        # 配置 DeepSeek API
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com/v1"
        )
        
        print("🚀 正在发送请求到DeepSeek...")
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7
        )
        
        result = response.choices[0].message.content
        print(f"✅ API调用成功，返回内容长度: {len(result)} 字符")
        return result
    
    except Exception as e:
        error_msg = f"❌ API调用错误：{str(e)}"
        print(error_msg)
        return f"{error_msg}\n\n请检查：\n1. DEEPSEEK_API_KEY 是否正确设置\n2. 网络连接是否正常\n3. API密钥是否有效\n4. 是否有足够的API配额"

def generate_html_page(analysis_content: str) -> str:
    """第二步：将分析内容转换为专业的HTML页面"""
    html_generation_prompt = """你是一个专业的HTML页面创造者，任务是将用户提供的中文事件分析信息制作成一个现代化、专业的中文HTML页面。

重要要求：
- 页面必须使用中文界面和中文内容
- 所有标题、标签、按钮等界面元素都要是中文
- 保持原始分析内容的中文表达

技术要求：
- 通过CDN引入Framer Motion，实现流畅的交互动画
- 通过CDN使用Tailwind CSS进行现代化样式设计
- 通过CDN引入Font Awesome图标库
- 响应式设计，适配各种设备
- 页面语言设置为中文：<html lang="zh-CN">

设计要求：
1. 页面要有专业的投资分析报告风格
2. 使用卡片布局展示不同分析维度（事件、局面、结构、投资映射）
3. 合理使用动画效果增强用户体验
4. 色彩搭配要专业且易读
5. 适当使用图标和视觉元素
6. 页面标题和所有文本都使用中文

内容处理：
- 完整保留所有中文分析信息
- 将【🟥 事件（Event）】、【🟧 局面（Situation）】、【🟩 结构（Structure）】、【💹 投资映射（Investor Lens）】等标记转换为美观的卡片展示
- 突出关键数据和结论
- 保持专业分析的完整性
- 使用合适的中文字体

请生成一个完整的中文HTML页面，包含：
1. 完整的HTML结构
2. 所有必要的CDN引入
3. 现代化的CSS样式
4. 适当的JavaScript交互
5. 专业的中文投资分析报告布局

确保生成的页面是完全独立的，可以直接在浏览器中打开显示。"""

    print("🎨 开始生成专业中文HTML页面...")
    return call_llm(analysis_content, html_generation_prompt)
