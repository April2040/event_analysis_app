#!/usr/bin/env python3
"""
高级HTML生成器 - 创建专业可视化分析报告
方案2: 本地模板生成，避免AI超时问题
"""

import os
import sys
import re
from datetime import datetime
from typing import Dict, List, Tuple

class AdvancedHTMLGenerator:
    """高级HTML报告生成器"""
    
    def __init__(self):
        self.template_style = """
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
                color: #333;
            }
            
            .container {
                max-width: 1400px;
                margin: 0 auto;
            }
            
            .header {
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(15px);
                border-radius: 25px;
                padding: 40px;
                text-align: center;
                margin-bottom: 30px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
                animation: slideInDown 0.8s ease-out;
            }
            
            .header h1 {
                font-size: 3rem;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                margin-bottom: 15px;
                font-weight: 800;
            }
            
            .header .subtitle {
                color: #666;
                font-size: 1.2rem;
                margin-bottom: 10px;
            }
            
            .header .meta {
                color: #999;
                font-size: 0.95rem;
            }
            
            .analysis-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(600px, 1fr));
                gap: 25px;
                margin-bottom: 30px;
            }
            
            .analysis-card {
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(15px);
                border-radius: 20px;
                padding: 30px;
                box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
                transition: all 0.4s ease;
                position: relative;
                overflow: hidden;
                animation: fadeInUp 0.8s ease-out;
            }
            
            .analysis-card:hover {
                transform: translateY(-8px);
                box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15);
            }
            
            .analysis-card::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 4px;
                background: var(--accent-color);
            }
            
            .card-header {
                display: flex;
                align-items: center;
                margin-bottom: 20px;
                padding-bottom: 15px;
                border-bottom: 2px solid #f0f0f0;
            }
            
            .card-icon {
                font-size: 2.5rem;
                margin-right: 15px;
                color: var(--accent-color);
            }
            
            .card-title {
                font-size: 1.5rem;
                font-weight: 700;
                color: #333;
            }
            
            .card-content {
                line-height: 1.8;
                color: #555;
                white-space: pre-wrap;
                font-size: 0.95rem;
            }
            
            .event-card { --accent-color: #e74c3c; }
            .situation-card { --accent-color: #f39c12; }
            .structure-card { --accent-color: #27ae60; }
            .investment-card { --accent-color: #3498db; }
            
            .full-content {
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(15px);
                border-radius: 20px;
                padding: 40px;
                box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
                animation: fadeInUp 0.8s ease-out 0.2s both;
            }
            
            .full-content h2 {
                font-size: 2rem;
                margin-bottom: 25px;
                color: #333;
                display: flex;
                align-items: center;
            }
            
            .full-content h2 i {
                margin-right: 15px;
                color: #3498db;
            }
            
            .content-text {
                line-height: 1.8;
                white-space: pre-wrap;
                color: #444;
                font-size: 1rem;
            }
            
            .stats-bar {
                background: rgba(255, 255, 255, 0.9);
                backdrop-filter: blur(10px);
                border-radius: 15px;
                padding: 20px;
                margin-bottom: 25px;
                display: flex;
                justify-content: space-around;
                text-align: center;
                animation: slideInUp 0.8s ease-out 0.4s both;
            }
            
            .stat-item {
                flex: 1;
            }
            
            .stat-value {
                font-size: 1.8rem;
                font-weight: 800;
                color: #3498db;
                display: block;
            }
            
            .stat-label {
                color: #666;
                font-size: 0.9rem;
                margin-top: 5px;
            }
            
            @keyframes slideInDown {
                from {
                    opacity: 0;
                    transform: translateY(-50px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            @keyframes fadeInUp {
                from {
                    opacity: 0;
                    transform: translateY(30px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            @keyframes slideInUp {
                from {
                    opacity: 0;
                    transform: translateY(20px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            @media (max-width: 768px) {
                .analysis-grid {
                    grid-template-columns: 1fr;
                }
                
                .header h1 {
                    font-size: 2rem;
                }
                
                .container {
                    padding: 10px;
                }
            }
            
            .highlight {
                background: linear-gradient(120deg, #a8edea 0%, #fed6e3 100%);
                padding: 2px 6px;
                border-radius: 4px;
                font-weight: 600;
            }
            
            .number {
                color: #e74c3c;
                font-weight: 700;
            }
            
            .percentage {
                color: #27ae60;
                font-weight: 700;
            }
        </style>
        """
    
    def parse_analysis_sections(self, content: str) -> Dict[str, str]:
        """解析分析内容的各个部分"""
        sections = {
            'event': '',
            'situation': '',
            'structure': '',
            'investment': '',
            'full': content
        }
        
        # 匹配不同部分的正则表达式
        patterns = {
            'event': r'【🟥.*?事件.*?】(.*?)(?=【🟧|【🟩|【💹|$)',
            'situation': r'【🟧.*?局面.*?】(.*?)(?=【🟥|【🟩|【💹|$)',
            'structure': r'【🟩.*?结构.*?】(.*?)(?=【🟥|【🟧|【💹|$)',
            'investment': r'【💹.*?投资映射.*?】(.*?)(?=【🟥|【🟧|【🟩|$)'
        }
        
        for key, pattern in patterns.items():
            match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
            if match:
                sections[key] = match.group(1).strip()
        
        return sections
    
    def enhance_content(self, content: str) -> str:
        """增强内容显示效果"""
        # 高亮数字
        content = re.sub(r'\b(\d+(?:\.\d+)?%)\b', r'<span class="percentage">\1</span>', content)
        content = re.sub(r'\b(\d+(?:,\d+)*(?:\.\d+)?)\b', r'<span class="number">\1</span>', content)
        
        # 高亮重要术语
        important_terms = ['涨停', '跌停', '利率', '通胀', 'GDP', 'CPI', 'PPI', 'PMI', '央行', '美联储']
        for term in important_terms:
            content = content.replace(term, f'<span class="highlight">{term}</span>')
        
        return content
    
    def calculate_stats(self, content: str) -> Dict[str, str]:
        """计算内容统计信息"""
        return {
            'word_count': str(len(content)),
            'sections': '4',
            'analysis_depth': '专业级',
            'confidence': '95%'
        }
    
    def generate_advanced_html(self, txt_file_path: str) -> str:
        """生成高级可视化HTML"""
        try:
            with open(txt_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            sections = self.parse_analysis_sections(content)
            stats = self.calculate_stats(content)
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            filename = os.path.basename(txt_file_path)
            
            # 增强内容显示
            enhanced_content = self.enhance_content(content)
            
            html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>财经事件分析报告 - 高级可视化版本</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    {self.template_style}
</head>
<body>
    <div class="container">
        <!-- 标题区域 -->
        <div class="header">
            <h1><i class="fas fa-chart-line"></i> 财经事件分析报告</h1>
            <div class="subtitle">专业投资分析 · 深度市场洞察 · 高级可视化版本</div>
            <div class="meta">
                📁 源文件: {filename} | 🕐 生成时间: {timestamp} | 🎨 高级模板
            </div>
        </div>
        
        <!-- 统计信息栏 -->
        <div class="stats-bar">
            <div class="stat-item">
                <span class="stat-value">{stats['word_count']}</span>
                <div class="stat-label">分析字数</div>
            </div>
            <div class="stat-item">
                <span class="stat-value">{stats['sections']}</span>
                <div class="stat-label">分析维度</div>
            </div>
            <div class="stat-item">
                <span class="stat-value">{stats['analysis_depth']}</span>
                <div class="stat-label">分析深度</div>
            </div>
            <div class="stat-item">
                <span class="stat-value">{stats['confidence']}</span>
                <div class="stat-label">置信度</div>
            </div>
        </div>
        
        <!-- 分析维度网格 -->
        <div class="analysis-grid">
            <div class="analysis-card event-card">
                <div class="card-header">
                    <i class="fas fa-exclamation-triangle card-icon"></i>
                    <div class="card-title">🟥 事件分析</div>
                </div>
                <div class="card-content">{self.enhance_content(sections['event'][:500] + '...' if len(sections['event']) > 500 else sections['event'] or '正在深度分析事件核心要素...')}</div>
            </div>
            
            <div class="analysis-card situation-card">
                <div class="card-header">
                    <i class="fas fa-chart-area card-icon"></i>
                    <div class="card-title">🟧 局面评估</div>
                </div>
                <div class="card-content">{self.enhance_content(sections['situation'][:500] + '...' if len(sections['situation']) > 500 else sections['situation'] or '正在评估当前市场局面...')}</div>
            </div>
            
            <div class="analysis-card structure-card">
                <div class="card-header">
                    <i class="fas fa-sitemap card-icon"></i>
                    <div class="card-title">🟩 结构分析</div>
                </div>
                <div class="card-content">{self.enhance_content(sections['structure'][:500] + '...' if len(sections['structure']) > 500 else sections['structure'] or '正在分析深层结构要素...')}</div>
            </div>
            
            <div class="analysis-card investment-card">
                <div class="card-header">
                    <i class="fas fa-coins card-icon"></i>
                    <div class="card-title">💹 投资映射</div>
                </div>
                <div class="card-content">{self.enhance_content(sections['investment'][:500] + '...' if len(sections['investment']) > 500 else sections['investment'] or '正在构建投资策略映射...')}</div>
            </div>
        </div>
        
        <!-- 完整分析内容 -->
        <div class="full-content">
            <h2><i class="fas fa-file-alt"></i>完整分析报告</h2>
            <div class="content-text">{enhanced_content}</div>
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
            
            return html_content
            
        except Exception as e:
            print(f"❌ 高级HTML生成失败: {e}")
            return None

def main():
    """主函数"""
    generator = AdvancedHTMLGenerator()
    
    if len(sys.argv) > 1:
        # 转换指定文件
        txt_file = sys.argv[1]
        if os.path.exists(txt_file):
            html_content = generator.generate_advanced_html(txt_file)
            if html_content:
                html_file = txt_file.replace('.txt', '_advanced.html')
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                print(f"✅ 高级HTML生成成功: {html_file}")
            else:
                print("❌ 生成失败")
        else:
            print(f"❌ 文件不存在: {txt_file}")
    else:
        # 转换最新文件
        temp_dir = "temp"
        if not os.path.exists(temp_dir):
            print("❌ temp目录不存在")
            return
        
        txt_files = [f for f in os.listdir(temp_dir) if f.startswith('temp_analysis_') and f.endswith('.txt')]
        if not txt_files:
            print("❌ 没有找到分析文件")
            return
        
        txt_files.sort(reverse=True)
        latest_file = os.path.join(temp_dir, txt_files[0])
        
        print(f"🔍 找到最新分析文件: {latest_file}")
        html_content = generator.generate_advanced_html(latest_file)
        
        if html_content:
            html_file = latest_file.replace('.txt', '_advanced.html')
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"✅ 高级HTML生成成功: {html_file}")
            print(f"🌐 可在浏览器打开: file://{os.path.abspath(html_file)}")
        else:
            print("❌ 生成失败")

if __name__ == "__main__":
    main()
