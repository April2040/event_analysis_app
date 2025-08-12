# utils.py
from openai import OpenAI
import os
import re
from dotenv import load_dotenv
from datetime import datetime
from typing import Dict, List, Tuple

# 加载 .env 文件
load_dotenv()

def call_llm(user_input: str, system_prompt: str, model="deepseek-chat") -> str:
    import time
    start_time = time.time()
    print(f"⏱️  开始处理LLM请求，模型: {model}")
    
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
            base_url="https://api.deepseek.com/v1",
            timeout=60  # 增加到60秒超时，处理复杂分析
        )
        
        print("🚀 正在发送请求到DeepSeek...")
        request_start = time.time()
        
        # 添加重试机制，处理超时问题
        max_retries = 2
        for attempt in range(max_retries):
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_input}
                    ],
                    temperature=0.7,
                    # 不设置max_tokens限制，确保AI能够生成完整的深度分析
                    stream=False  # 确保非流式响应以获得完整内容
                )
                break  # 成功则退出重试循环
            except Exception as retry_error:
                if attempt < max_retries - 1:
                    print(f"    ⚠️ 第{attempt + 1}次尝试失败，正在重试... ({retry_error})")
                    time.sleep(2)  # 等待2秒后重试
                    continue
                else:
                    raise retry_error  # 最后一次重试失败，抛出异常
        request_end = time.time()
        
        result = response.choices[0].message.content
        total_time = time.time() - start_time
        api_time = request_end - request_start
        
        print(f"✅ API调用成功！")
        print(f"📊 响应统计: 内容长度 {len(result)} 字符")
        print(f"⏱️  耗时详情: API请求 {api_time:.2f}秒 | 总时间 {total_time:.2f}秒")
        return result
    
    except Exception as e:
        error_msg = f"❌ API调用错误：{str(e)}"
        print(error_msg)
        return f"{error_msg}\n\n请检查：\n1. DEEPSEEK_API_KEY 是否正确设置\n2. 网络连接是否正常\n3. API密钥是否有效\n4. 是否有足够的API配额"

def generate_html_page(analysis_content: str) -> str:
    """第二步：将分析内容转换为专业的HTML页面（多层回退策略）"""
    
    # 第一层：尝试生成高级HTML（简化提示词，减少超时风险）
    advanced_prompt = """你是专业的HTML页面生成器。请将中文事件分析制作成现代化的HTML页面。

要求：
1. 中文界面，专业投资分析风格
2. 卡片布局展示分析维度
3. 现代CSS样式，响应式设计
4. 突出关键数据，易读性强
5. 适当动画效果

生成完整独立的HTML页面，可直接浏览器打开。"""

    print("🎨 第一层：尝试生成高级可视化HTML...")
    try:
        # 设置较短超时，快速尝试
        result = call_llm(analysis_content, advanced_prompt, model="deepseek-chat")
        if "❌" not in result and len(result) > 1000:  # 检查结果质量
            print("✅ 高级HTML生成成功！")
            return result
        else:
            print("⚠️ 高级HTML质量不佳，尝试中级方案...")
    except Exception as e:
        print(f"⚠️ 高级HTML生成失败: {e}")
    
    # 第二层：中级HTML模板
    print("🎨 第二层：生成中级可视化HTML...")
    try:
        medium_html = generate_medium_html(analysis_content)
        print("✅ 中级HTML生成成功！")
        return medium_html
    except Exception as e:
        print(f"⚠️ 中级HTML生成失败: {e}")
    
    # 第三层：基础HTML（原备用方案）
    print("🎨 第三层：生成基础HTML...")
    return generate_simple_html(analysis_content)

def generate_medium_html(analysis_content: str) -> str:
    """生成中级可视化HTML页面"""
    # 解析分析内容，提取关键部分
    sections = parse_analysis_content(analysis_content)
    
    html_template = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>财经事件分析报告</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }}
        .card {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        .card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 30px 60px rgba(0, 0, 0, 0.15);
        }}
        .section-icon {{
            font-size: 2rem;
            margin-bottom: 1rem;
        }}
        .event {{ color: #e74c3c; }}
        .situation {{ color: #f39c12; }}
        .structure {{ color: #27ae60; }}
        .investment {{ color: #3498db; }}
        .gradient-text {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        .fade-in {{
            animation: fadeIn 0.6s ease-in-out;
        }}
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
    </style>
</head>
<body class="p-4">
    <div class="max-w-7xl mx-auto">
        <!-- 标题区域 -->
        <div class="card p-8 mb-8 text-center fade-in">
            <h1 class="text-4xl font-bold gradient-text mb-4">
                <i class="fas fa-chart-line mr-3"></i>财经事件分析报告
            </h1>
            <p class="text-gray-600">专业投资分析 · 深度市场洞察</p>
            <div class="text-sm text-gray-500 mt-2">
                生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            </div>
        </div>

        <!-- 分析内容网格 -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {generate_section_cards(sections)}
        </div>

        <!-- 完整内容区域 -->
        <div class="card p-8 mt-8 fade-in">
            <h2 class="text-2xl font-bold mb-6 flex items-center">
                <i class="fas fa-file-alt mr-3 text-blue-500"></i>完整分析内容
            </h2>
            <div class="prose max-w-none">
                <pre class="whitespace-pre-wrap font-sans leading-relaxed text-gray-700">{analysis_content}</pre>
            </div>
        </div>
    </div>

    <script>
        // 添加滚动动画
        const observer = new IntersectionObserver((entries) => {{
            entries.forEach(entry => {{
                if (entry.isIntersecting) {{
                    entry.target.classList.add('fade-in');
                }}
            }});
        }});

        document.querySelectorAll('.card').forEach(card => {{
            observer.observe(card);
        }});
    </script>
</body>
</html>"""
    
    return html_template

def parse_analysis_content(content: str) -> dict:
    """解析分析内容，提取各个部分"""
    sections = {{
        'event': '',
        'situation': '', 
        'structure': '',
        'investment': ''
    }}
    
    # 简单的内容解析逻辑
    lines = content.split('\n')
    current_section = None
    
    for line in lines:
        if '事件' in line and '🟥' in line:
            current_section = 'event'
        elif '局面' in line and '🟧' in line:
            current_section = 'situation'
        elif '结构' in line and '🟩' in line:
            current_section = 'structure'
        elif '投资映射' in line and '💹' in line:
            current_section = 'investment'
        elif current_section and line.strip():
            sections[current_section] += line + '\n'
    
    return sections

def generate_section_cards(sections: dict) -> str:
    """生成分析部分的卡片"""
    card_configs = [
        ('event', '🟥 事件分析', 'event', 'fas fa-exclamation-triangle'),
        ('situation', '🟧 局面评估', 'situation', 'fas fa-chart-area'),
        ('structure', '🟩 结构分析', 'structure', 'fas fa-sitemap'),
        ('investment', '💹 投资映射', 'investment', 'fas fa-coins')
    ]
    
    cards_html = ""
    for key, title, css_class, icon in card_configs:
        content = sections.get(key, '数据分析中...')[:300] + '...' if len(sections.get(key, '')) > 300 else sections.get(key, '数据分析中...')
        
        cards_html += f'''
        <div class="card p-6 fade-in">
            <div class="text-center mb-4">
                <i class="{icon} section-icon {css_class}"></i>
                <h3 class="text-xl font-bold text-gray-800">{title}</h3>
            </div>
            <div class="text-gray-600 leading-relaxed">
                <pre class="whitespace-pre-wrap font-sans text-sm">{content}</pre>
            </div>
        </div>
        '''
    
    return cards_html

def generate_simple_html(analysis_content: str) -> str:
    """生成简单的HTML页面作为备用方案"""
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>财经事件分析报告</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f8f9fa;
        }}
        .container {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            text-align: center;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        .content {{
            white-space: pre-wrap;
            font-size: 16px;
            line-height: 1.8;
        }}
        .timestamp {{
            text-align: center;
            color: #7f8c8d;
            margin-top: 20px;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🧠 财经事件分析报告</h1>
        <div class="content">{analysis_content}</div>
        <div class="timestamp">生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
    </div>
</body>
</html>"""


class AdvancedHTMLGenerator:
    """高级HTML报告生成器 - 集成到主程序"""
    
    def __init__(self):
        pass
    
    def parse_analysis_content_advanced(self, content: str) -> Dict[str, str]:
        """智能解析分析内容"""
        sections = {
            'title': '财经事件深度分析报告',
            'event': '',
            'situation': '',
            'structure': '',
            'investment': '',
            'full_content': content
        }
        
        # 提取标题
        lines = content.split('\n')
        for line in lines[:5]:
            if line.strip() and ('分析' in line or '报告' in line):
                sections['title'] = line.strip()
                break
        
        # 解析各个部分 - 优化匹配逻辑
        current_section = None
        section_content = []
        
        for line in lines:
            line_stripped = line.strip()
            if not line_stripped:
                continue
                
            # 识别章节标题 - 支持多种格式
            if any(pattern in line_stripped for pattern in ['### 【🟥', '🟥 事件', '事件（Event）', '【事件']):
                if current_section and section_content:
                    sections[current_section] = '\n'.join(section_content)
                current_section = 'event'
                section_content = [line]
            elif any(pattern in line_stripped for pattern in ['### 【🟧', '� 局面', '局面（Situation）', '【局面']):
                if current_section and section_content:
                    sections[current_section] = '\n'.join(section_content)
                current_section = 'situation'
                section_content = [line]
            elif any(pattern in line_stripped for pattern in ['### 【🟩', '� 结构', '结构（Structure）', '【结构']):
                if current_section and section_content:
                    sections[current_section] = '\n'.join(section_content)
                current_section = 'structure'
                section_content = [line]
            elif any(pattern in line_stripped for pattern in ['### 【💹', '� 投资', '投资映射', '【投资']):
                if current_section and section_content:
                    sections[current_section] = '\n'.join(section_content)
                current_section = 'investment'
                section_content = [line]
            elif line_stripped.startswith('---') or line_stripped.startswith('⚠️'):
                # 分隔线或免责声明，结束当前section
                if current_section and section_content:
                    sections[current_section] = '\n'.join(section_content)
                    current_section = None
                    section_content = []
            else:
                if current_section:
                    section_content.append(line)
        
        # 处理最后一个section
        if current_section and section_content:
            sections[current_section] = '\n'.join(section_content)
        
        # 确保每个部分都有内容（如果解析失败，从完整内容中提取）
        for key in ['event', 'situation', 'structure', 'investment']:
            if not sections[key].strip():
                # 使用正则表达式更精确地提取
                import re
                pattern_map = {
                    'event': r'### 【🟥.*?】(.*?)(?=### 【🟧|$)',
                    'situation': r'### 【🟧.*?】(.*?)(?=### 【🟩|$)',
                    'structure': r'### 【🟩.*?】(.*?)(?=### 【💹|$)',
                    'investment': r'### 【💹.*?】(.*?)(?=---|\Z)'
                }
                if key in pattern_map:
                    match = re.search(pattern_map[key], content, re.DOTALL)
                    if match:
                        sections[key] = match.group(1).strip()
        
        return sections
    
    def generate_advanced_html_from_content(self, content: str) -> str:
        """从分析内容生成高级HTML"""
        sections = self.parse_analysis_content_advanced(content)
        
        html_template = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{sections['title']}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            color: #333;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        .header {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(15px);
            border-radius: 25px;
            padding: 40px;
            text-align: center;
            margin-bottom: 30px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
            animation: slideInDown 0.8s ease-out;
        }}
        
        .header h1 {{
            font-size: 3rem;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea, #764ba2);
            background-clip: text;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }}
        
        .subtitle {{
            font-size: 1.2rem;
            color: #666;
            font-weight: 300;
        }}
        
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(600px, 1fr));
            gap: 25px;
            margin-bottom: 30px;
        }}
        
        .analysis-card {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(15px);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.1);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: pointer;
            opacity: 0;
            transform: translateY(30px);
            animation: slideInUp 0.8s ease-out forwards;
        }}
        
        .analysis-card:hover {{
            transform: translateY(-10px);
            box-shadow: 0 25px 60px rgba(0, 0, 0, 0.15);
        }}
        
        .card-header {{
            display: flex;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid #f0f0f0;
        }}
        
        .card-icon {{
            font-size: 2.5rem;
            margin-right: 15px;
        }}
        
        .card-title {{
            font-size: 1.8rem;
            font-weight: 600;
            color: #333;
        }}
        
        .card-content {{
            line-height: 1.8;
            color: #555;
            font-size: 1rem;
            white-space: pre-wrap;
            max-height: 200px;
            overflow: hidden;
            transition: max-height 0.4s ease-out;
        }}
        
        .analysis-card.expanded .card-content {{
            max-height: none;
        }}
        
        .expand-hint {{
            text-align: center;
            margin-top: 15px;
            color: #888;
            font-size: 0.9rem;
            font-style: italic;
        }}
        
        .full-content {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(15px);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.1);
            opacity: 0;
            transform: translateY(30px);
            animation: slideInUp 0.8s ease-out 0.4s forwards;
        }}
        
        .full-content h2 {{
            font-size: 2rem;
            margin-bottom: 20px;
            color: #333;
            text-align: center;
        }}
        
        .full-content .content {{
            line-height: 1.8;
            color: #444;
            white-space: pre-wrap;
            font-size: 1rem;
        }}
        
        .timestamp {{
            text-align: center;
            margin-top: 30px;
            color: rgba(255, 255, 255, 0.8);
            font-style: italic;
        }}
        
        /* 动画定义 */
        @keyframes slideInDown {{
            from {{
                opacity: 0;
                transform: translateY(-50px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        @keyframes slideInUp {{
            from {{
                opacity: 0;
                transform: translateY(30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        /* 颜色主题 */
        .event {{ --theme-color: #e74c3c; }}
        .situation {{ --theme-color: #f39c12; }}
        .structure {{ --theme-color: #27ae60; }}
        .investment {{ --theme-color: #3498db; }}
        
        .event .card-icon {{ color: #e74c3c; }}
        .situation .card-icon {{ color: #f39c12; }}
        .structure .card-icon {{ color: #27ae60; }}
        .investment .card-icon {{ color: #3498db; }}
        
        /* 响应式设计 */
        @media (max-width: 768px) {{
            .grid {{
                grid-template-columns: 1fr;
            }}
            
            .header h1 {{
                font-size: 2rem;
            }}
            
            .container {{
                padding: 10px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{sections['title']}</h1>
            <div class="subtitle">智能分析 · 专业洞察 · 投资指导</div>
        </div>
        
        <div class="grid">"""
        
        # 生成各个分析卡片
        cards_config = [
            ('event', '🟥 事件分析', 'fas fa-exclamation-triangle', 'event'),
            ('situation', '🟧 局面评估', 'fas fa-chart-area', 'situation'),
            ('structure', '🟩 结构分析', 'fas fa-sitemap', 'structure'),
            ('investment', '💹 投资映射', 'fas fa-coins', 'investment')
        ]
        
        for key, title, icon, css_class in cards_config:
            if sections[key].strip():
                html_template += f"""
            <div class="analysis-card {css_class}">
                <div class="card-header">
                    <div class="card-icon">{title.split()[0]}</div>
                    <div class="card-title">{title}</div>
                </div>
                <div class="card-content">{sections[key]}</div>
                <div class="expand-hint">点击展开完整内容</div>
            </div>"""
        
        html_template += f"""
        </div>
        
        <div class="full-content">
            <h2>📊 完整分析报告</h2>
            <div class="content">{sections['full_content']}</div>
        </div>
        
        <div class="timestamp">
            📅 生成时间: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}
        </div>
    </div>
    
    <script>
        // 滚动动画观察器
        const observerOptions = {{
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        }};
        
        const observer = new IntersectionObserver((entries) => {{
            entries.forEach(entry => {{
                if (entry.isIntersecting) {{
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }}
            }});
        }}, observerOptions);
        
        // 观察所有卡片
        document.querySelectorAll('.analysis-card, .full-content').forEach(card => {{
            observer.observe(card);
        }});
        
        // 点击卡片展开/收缩
        document.querySelectorAll('.analysis-card').forEach(card => {{
            card.addEventListener('click', function() {{
                this.classList.toggle('expanded');
            }});
        }});
    </script>
</body>
</html>"""
        
        return html_template
    
    def save_advanced_html(self, content: str, txt_filepath: str) -> str:
        """保存高级HTML文件并返回文件路径"""
        try:
            html_content = self.generate_advanced_html_from_content(content)
            html_filepath = txt_filepath.replace('.txt', '_advanced.html')
            
            with open(html_filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"✅ 高级HTML报告已生成: {html_filepath}")
            return html_filepath
            
        except Exception as e:
            print(f"❌ 高级HTML生成失败: {e}")
            return None


def generate_advanced_html_auto(analysis_content: str, txt_filepath: str) -> str:
    """自动生成高级HTML版本（集成到主程序流程中）"""
    try:
        print("🎨 正在生成高级HTML可视化报告...")
        generator = AdvancedHTMLGenerator()
        html_filepath = generator.save_advanced_html(analysis_content, txt_filepath)
        
        if html_filepath:
            return html_filepath
        else:
            print("⚠️ 高级HTML生成失败，将使用标准HTML备用方案")
            return None
            
    except Exception as e:
        print(f"⚠️ 高级HTML生成过程出错: {e}")
        return None
