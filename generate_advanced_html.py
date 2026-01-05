#!/usr/bin/env python3
"""
高级HTML生成器 - 创建专业可视化分析报告
优化版本: 四模块分析 + 新闻简介 + 展开功能 + 完善的标题层级识别
"""

import os
import sys
import re
from datetime import datetime
from typing import Dict

class AdvancedHTMLGenerator:
    """高级HTML报告生成器"""
    
    def __init__(self):
        pass
        
    def extract_news_summary(self, content: str) -> str:
        """从分析内容中智能提取新闻简介"""
        try:
            surface_pattern = r'【🟥[^】]*表层事件[^】]*】(.*?)(?=【|$)'
            surface_match = re.search(surface_pattern, content, re.DOTALL)
            
            if surface_match:
                surface_content = surface_match.group(1).strip()
                
                time_pattern = r'[*-]*\s*时间线[*：:](.*?)(?=[*-]*\s*(?:核心行动者|行动者|直接结果|争议焦点)|$)'
                actors_pattern = r'[*-]*\s*(?:核心行动者|行动者)[*：:](.*?)(?=[*-]*\s*(?:直接结果|争议焦点|时间线)|$)'
                results_pattern = r'[*-]*\s*直接结果[*：:](.*?)(?=[*-]*\s*(?:争议焦点|核心行动者|时间线)|$)'
                
                time_match = re.search(time_pattern, surface_content, re.DOTALL | re.IGNORECASE)
                actors_match = re.search(actors_pattern, surface_content, re.DOTALL | re.IGNORECASE)
                results_match = re.search(results_pattern, surface_content, re.DOTALL | re.IGNORECASE)
                
                summary_parts = []
                
                if time_match:
                    time_info = time_match.group(1).strip()
                    time_clean = re.sub(r'[*\s]+', ' ', time_info)
                    time_clean = re.sub(r'^\s*[：:]\s*', '', time_clean)
                    summary_parts.append(time_clean.split('。')[0].split('，')[0])
                
                if actors_match:
                    actors_info = actors_match.group(1).strip()
                    actors_clean = re.sub(r'[*\s]+', ' ', actors_info)
                    actors_clean = re.sub(r'^\s*[：:]\s*', '', actors_clean)
                    if '（' in actors_clean:
                        actors_clean = actors_clean.split('（')[0]
                    summary_parts.append(actors_clean.split('。')[0].split('、')[0])
                
                if results_match:
                    results_info = results_match.group(1).strip()
                    results_clean = re.sub(r'[*\s]+', ' ', results_info)
                    results_clean = re.sub(r'^\s*[：:]\s*', '', results_clean)
                    summary_parts.append(results_clean.split('。')[0])
                
                if summary_parts:
                    news_summary = '，'.join(summary_parts[:3])
                    if not news_summary.endswith('。'):
                        news_summary += '。'
                    return news_summary
            
            return "财经事件深度分析：市场动态与投资机会解读。"
            
        except Exception as e:
            print(f"新闻简介提取失败: {e}")
            return "财经事件深度分析：市场动态与投资机会解读。"

    def parse_analysis_sections(self, content: str) -> Dict[str, str]:
        """解析分析内容的各个部分"""
        sections = {}
        
        patterns = {
            '表层事件': [
                r'【🟥[^】]*表层事件[^】]*】(.*?)(?=【|$)',
                r'🟥[^】]*表层事件[^】]*(.*?)(?=🟧|🟩|💹|$)',
            ],
            '博弈局面': [
                r'【🟧[^】]*博弈局面[^】]*】(.*?)(?=【|$)',
                r'🟧[^】]*博弈局面[^】]*(.*?)(?=🟥|🟩|💹|$)',
            ],
            '底层逻辑': [
                r'【🟩[^】]*(?:底层逻辑|结构分析)[^】]*】(.*?)(?=【|$)',
                r'🟩[^】]*(?:底层逻辑|结构分析)[^】]*(.*?)(?=🟥|🟧|💹|$)',
            ],
            '投资映射': [
                r'【💹[^】]*投资映射[^】]*】(.*?)(?=【|$)',
                r'💹[^】]*投资映射[^】]*(.*?)(?=🟥|🟧|🟩|$)',
            ]
        }
        
        for section_name, section_patterns in patterns.items():
            for pattern in section_patterns:
                match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
                if match:
                    sections[section_name] = match.group(1).strip()
                    break
        
        return sections

    def enhance_content(self, content: str) -> str:
        """增强内容格式，处理列表、表格和格式化"""
        if not content:
            return ""
        
        # 处理顺序很重要：先处理标题，再处理列表
        content = self._process_section_headers(content)
        content = self._process_markdown(content)
        content = self._process_lists(content)
        content = self.render_tables(content)
        
        return content

    def _process_markdown(self, text: str) -> str:
        """处理Markdown格式转HTML"""
        text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
        text = re.sub(r'__([^_]+)__', r'<strong>\1</strong>', text)
        text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
        text = re.sub(r'_([^_]+)_', r'<em>\1</em>', text)
        return text

    def _process_section_headers(self, content: str) -> str:
        """处理章节标题 - 专门优化博弈局面等复杂结构"""
        
        # 第一步：处理一级标题 - **标题**： 格式（列表项）
        content = re.sub(
            r'^- \*\*([^*]+)\*\*[：:]\s*$',
            r'<div class="section-header level-1">\1</div>',
            content,
            flags=re.MULTILINE
        )
        
        # 第二步：处理二级标题 - 带缩进的 **标题**： 格式
        content = re.sub(
            r'^  - \*\*([^*]+)\*\*[：:]\s*(.*)$',
            r'<div class="section-header level-2">\1</div>\n\2',
            content,
            flags=re.MULTILINE
        )
        
        # 第三步：处理数字编号标题
        content = re.sub(
            r'^(\d+)\.\s*(.+)$',
            r'<div class="section-header level-1">\1. \2</div>',
            content,
            flags=re.MULTILINE
        )
        
        # 第四步：处理其他粗体标题（兜底）
        content = re.sub(
            r'^\*\*([^*]+)\*\*[：:]\s*$',
            r'<div class="section-header level-1">\1</div>',
            content,
            flags=re.MULTILINE
        )
        
        return content

    def _process_lists(self, content: str) -> str:
        """处理列表结构 - 跳过已处理的标题"""
        lines = content.split('\n')
        processed_lines = []
        
        for line in lines:
            original_line = line
            stripped_line = line.strip()
            
            if not stripped_line:
                continue
            
            # 跳过已经处理过的标题
            if '<div class="section-header' in line:
                processed_lines.append(original_line)
                continue
                
            # 处理列表项
            if re.match(r'^- ', stripped_line):
                # 第一级列表项
                text = re.sub(r'^- ', '', stripped_line)
                processed_lines.append(f'<li class="list-item level-1">{text}</li>')
            elif re.match(r'^  - ', line):  # 保持原始缩进检测
                # 第二级列表项
                text = re.sub(r'^  - ', '', line).strip()
                processed_lines.append(f'<li class="list-item level-2">{text}</li>')
            elif re.match(r'^\s{4,}- ', line):
                # 第三级列表项
                text = re.sub(r'^\s*- ', '', line).strip()
                processed_lines.append(f'<li class="list-item level-3">{text}</li>')
            elif re.match(r'^\d+\.\s+', stripped_line):
                # 数字列表
                text = re.sub(r'^\d+\.\s+', '', stripped_line)
                processed_lines.append(f'<li class="list-item level-1">{text}</li>')
            else:
                # 普通文本行
                processed_lines.append(stripped_line)
        
        return '\n'.join(processed_lines)

    def render_tables(self, content: str) -> str:
        """渲染表格内容"""
        table_pattern = r'\|[^|]*\|[^|]*\|[^|]*\|?[^\n]*\n(?:\|[^|]*\|[^|]*\|[^|]*\|?[^\n]*\n?)+'
        
        def process_table(match):
            table_text = match.group(0)
            lines = [line.strip() for line in table_text.split('\n') if line.strip()]
            
            if len(lines) < 2:
                return table_text
            
            rows = []
            for line in lines:
                if '|' in line:
                    cells = [cell.strip() for cell in line.split('|') if cell.strip()]
                    if cells:
                        rows.append(cells)
            
            if not rows:
                return table_text
            
            html = '<div class="table-container">\\n<table class="analysis-table">\\n'
            
            if rows:
                html += '<thead>\\n<tr>\\n'
                for cell in rows[0]:
                    html += f'<th>{cell}</th>\\n'
                html += '</tr>\\n</thead>\\n'
            
            if len(rows) > 1:
                html += '<tbody>\\n'
                for row in rows[1:]:
                    html += '<tr>\\n'
                    for cell in row:
                        if '⬆️' in cell or '积极' in cell:
                            cell = f'<span style="color: #27ae60;">{cell}</span>'
                        elif '⬇️' in cell or '消极' in cell:
                            cell = f'<span style="color: #e74c3c;">{cell}</span>'
                        elif '➡️' in cell or '分化' in cell:
                            cell = f'<span style="color: #f39c12;">{cell}</span>'
                        
                        html += f'<td>{cell}</td>\\n'
                    html += '</tr>\\n'
                html += '</tbody>\\n'
            
            html += '</table>\\n</div>'
            return html
        
        content = re.sub(table_pattern, process_table, content, flags=re.MULTILINE)
        return content

    def _truncate_content(self, content: str, max_length: int = 300) -> str:
        """智能截断内容，避免破坏HTML标签"""
        if len(content) <= max_length:
            return content
        
        truncated = content[:max_length]
        
        last_open = truncated.rfind('<')
        last_close = truncated.rfind('>')
        
        if last_open > last_close:
            truncated = content[:last_open]
        
        if truncated != content:
            truncated += '...'
        
        return truncated

    def generate_advanced_html(self, file_path: str) -> str:
        """生成高级HTML报告"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            news_summary = self.extract_news_summary(content)
            sections = self.parse_analysis_sections(content)
            
            html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>金融事件深度分析报告</title>
    <style>
        :root {{
            --primary-color: #2c3e50;
            --accent-color: #3498db;
            --success-color: #27ae60;
            --warning-color: #f39c12;
            --danger-color: #e74c3c;
            --text-color: #2c3e50;
            --bg-color: #ecf0f1;
            --card-bg: #ffffff;
            --border-color: #bdc3c7;
            --shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            --gradient-bg: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
            line-height: 1.6;
            color: var(--text-color);
            background: var(--gradient-bg);
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 30px;
            background: rgba(255, 255, 255, 0.95);
            padding: 30px;
            border-radius: 15px;
            box-shadow: var(--shadow);
        }}
        
        .header h1 {{
            color: var(--primary-color);
            font-size: 2.5rem;
            margin-bottom: 10px;
            font-weight: 700;
        }}
        
        .header p {{
            color: #7f8c8d;
            font-size: 1.1rem;
        }}
        
        .news-summary {{
            background: rgba(255, 255, 255, 0.95);
            padding: 25px;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: var(--shadow);
        }}
        
        .news-summary h2 {{
            color: var(--primary-color);
            font-size: 1.8rem;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
        }}
        
        .news-summary p {{
            font-size: 1.1rem;
            line-height: 1.8;
            color: #2c3e50;
        }}
        
        .analysis-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(600px, 1fr));
            gap: 25px;
            margin-bottom: 30px;
        }}
        
        .analysis-card {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            box-shadow: var(--shadow);
            overflow: hidden;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        
        .analysis-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
        }}
        
        .card-title {{
            background: linear-gradient(135deg, var(--accent-color), #2980b9);
            color: white;
            padding: 20px;
            font-size: 1.3rem;
            font-weight: 600;
        }}
        
        .card-content {{
            padding: 0;
        }}
        
        .content-preview {{
            padding: 20px;
            max-height: 200px;
            overflow: hidden;
            position: relative;
        }}
        
        .content-full {{
            padding: 20px;
            max-height: 600px;
            overflow-y: auto;
        }}
        
        .expand-controls {{
            padding: 15px 20px;
            background: #f8f9fa;
            border-top: 1px solid #e9ecef;
        }}
        
        .expand-btn {{
            background: var(--accent-color);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 0.9rem;
            font-weight: 500;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .expand-btn:hover {{
            background: #2980b9;
            transform: translateY(-2px);
        }}
        
        .expand-icon {{
            font-size: 0.8rem;
            transition: transform 0.3s ease;
        }}
        
        .list-item {{
            margin: 10px 0;
            padding: 8px 0;
            border-bottom: 1px solid #f0f0f0;
            line-height: 1.7;
        }}
        
        .list-item:last-child {{
            border-bottom: none;
        }}
        
        .list-item.level-1 {{
            margin-left: 0;
            font-size: 1rem;
        }}
        
        .list-item.level-2 {{
            margin: 6px 0 6px 20px;
            font-size: 0.95rem;
        }}
        
        .list-item.level-3 {{
            margin: 6px 0 6px 40px;
            font-size: 0.9rem;
        }}
        
        .section-header {{
            margin: 20px 0 15px 0;
            padding: 12px 20px;
            border-radius: 8px;
            font-weight: 600;
        }}
        
        .section-header.level-1 {{
            background: linear-gradient(135deg, rgba(52, 152, 219, 0.15), rgba(52, 152, 219, 0.05));
            border-left: 4px solid var(--accent-color);
            font-size: 1.1rem;
            color: var(--primary-color);
        }}
        
        .section-header.level-2 {{
            background: linear-gradient(135deg, rgba(46, 204, 113, 0.12), rgba(46, 204, 113, 0.03));
            border-left: 3px solid var(--success-color);
            font-size: 1rem;
            color: var(--success-color);
            margin: 15px 0 10px 0;
            padding: 8px 15px;
        }}
        
        .table-container {{
            margin: 20px 0;
            overflow-x: auto;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            background: rgba(255, 255, 255, 0.95);
        }}
        
        .analysis-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.9rem;
            line-height: 1.6;
        }}
        
        .analysis-table th {{
            background: linear-gradient(135deg, var(--accent-color, #3498db), rgba(var(--accent-color-rgb, 52, 152, 219), 0.8));
            color: white;
            font-weight: 600;
            padding: 12px 15px;
            text-align: left;
            border: none;
            font-size: 0.95rem;
        }}
        
        .analysis-table td {{
            padding: 12px 15px;
            border-bottom: 1px solid #ecf0f1;
            background: rgba(255, 255, 255, 0.8);
        }}
        
        .analysis-table tr:hover td {{
            background: rgba(52, 152, 219, 0.05);
        }}
        
        .analysis-table tr:last-child td {{
            border-bottom: none;
        }}
        
        @media (max-width: 768px) {{
            .analysis-grid {{
                grid-template-columns: 1fr;
            }}
            
            .header h1 {{
                font-size: 2rem;
            }}
            
            .container {{
                padding: 15px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 金融事件深度分析报告</h1>
            <p>基于AI智能分析的专业财经事件解读</p>
        </div>
        
        <div class="news-summary">
            <h2>📰 事件概要</h2>
            <p>{news_summary}</p>
        </div>
        
        <div class="analysis-grid">"""
            
            card_configs = [
                {'key': '表层事件', 'title': '🟥 事件分析', 'icon': '🟥'},
                {'key': '博弈局面', 'title': '🟧 局面评估', 'icon': '🟧'},
                {'key': '底层逻辑', 'title': '🟩 结构分析', 'icon': '🟩'},
                {'key': '投资映射', 'title': '💹 投资映射', 'icon': '💹'}
            ]
            
            for config in card_configs:
                section_content = sections.get(config['key'], f"{config['title']}部分暂无内容")
                enhanced_content = self.enhance_content(section_content)
                
                # 投资映射模块需要更长的预览长度，因为有表格和详细内容
                if config['key'] == '投资映射':
                    preview_content = self._truncate_content(enhanced_content, 1650)
                else:
                    preview_content = self._truncate_content(enhanced_content, 300)
                
                html_content += f"""
            <div class="analysis-card">
                <div class="card-title">{config['title']}</div>
                <div class="card-content">
                    <div class="content-preview">
                        {preview_content}
                    </div>
                    <div class="content-full" style="display: none;">
                        {enhanced_content}
                    </div>
                    <div class="expand-controls">
                        <button class="expand-btn" onclick="toggleExpand(this)">
                            <span class="expand-icon">▼</span>
                            <span>展开更多内容</span>
                        </button>
                    </div>
                </div>
            </div>"""
            
            html_content += """
        </div>
    </div>

    <script>
        function toggleExpand(button) {
            const card = button.closest('.analysis-card');
            const preview = card.querySelector('.content-preview');
            const full = card.querySelector('.content-full');
            const icon = button.querySelector('.expand-icon');
            const text = button.querySelector('span:last-child');
            
            if (full.style.display === 'none') {
                preview.style.display = 'none';
                full.style.display = 'block';
                icon.textContent = '▲';
                text.textContent = '收起内容';
                
                card.scrollIntoView({ behavior: 'smooth', block: 'start' });
            } else {
                preview.style.display = 'block';
                full.style.display = 'none';
                icon.textContent = '▼';
                text.textContent = '展开更多内容';
            }
        }
    </script>
</body>
</html>"""
            
            return html_content
            
        except Exception as e:
            print(f"生成HTML失败: {e}")
            return None

def main():
    """主函数"""
    if len(sys.argv) != 2:
        print("使用方法: python generate_advanced_html.py <分析文件路径>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        print(f"文件不存在: {file_path}")
        sys.exit(1)
    
    generator = AdvancedHTMLGenerator()
    html_content = generator.generate_advanced_html(file_path)
    
    if html_content:
        base_name = os.path.splitext(file_path)[0]
        output_file = f"{base_name}_advanced.html"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ 高级HTML报告已生成: {output_file}")
        
        # 添加简单的验证
        level1_headers = len(re.findall(r'<div class="section-header level-1">', html_content))
        level2_headers = len(re.findall(r'<div class="section-header level-2">', html_content))
        print(f"📊 结构验证: 一级标题{level1_headers}个, 二级标题{level2_headers}个")
    else:
        print("❌ HTML生成失败")

if __name__ == "__main__":
    main()
