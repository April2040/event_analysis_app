#!/usr/bin/env python3
"""
标准化渲染器 - 基于认可的 standalone 版本
基于用户认可的 temp_analysis_20250819_100543_standalone.html 版本
提供标准化的四模块HTML渲染功能
"""

import re
from pathlib import Path
from datetime import datetime
import argparse

class StandardizedRenderer:
    """基于认可版本的标准化HTML渲染器"""
    
    def __init__(self):
        self.module_icons = {
            '事件梳理': '🟥',
            '局面评估': '🟧', 
            '底层逻辑': '🟩',
            '投资映射': '💹'
        }
        
        # 原始TXT标识符到新标题的映射
        self.module_mapping = {
            '🟥': '事件梳理',
            '🟧': '局面评估', 
            '🟩': '底层逻辑',
            '💹': '投资映射'
        }
        
    def get_css_styles(self):
        """返回标准化CSS样式 - 基于standalone版本"""
        return """
        :root {
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
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
            line-height: 1.6;
            color: var(--text-color);
            background: var(--gradient-bg);
            min-height: 100vh;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
            background: rgba(255, 255, 255, 0.95);
            padding: 30px;
            border-radius: 15px;
            box-shadow: var(--shadow);
        }
        
        .header h1 {
            color: var(--primary-color);
            font-size: 2.5rem;
            margin-bottom: 10px;
            font-weight: 700;
        }
        
        .subtitle {
            color: var(--accent-color);
            font-size: 1.2rem;
            font-weight: 500;
            margin-bottom: 8px;
        }
        
        .timestamp {
            color: #333;
            font-size: 0.95rem;
            font-weight: 400;
            margin-top: 15px;
        }
        
        .news-summary {
            background: rgba(255, 255, 255, 0.95);
            padding: 25px;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: var(--shadow);
        }
        
        .news-summary h2 {
            color: var(--primary-color);
            font-size: 1.8rem;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
        }
        
        .news-summary p {
            font-size: 1.1rem;
            line-height: 1.8;
            color: #2c3e50;
        }
        
        .main-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(650px, 1fr));
            gap: 25px;
            margin-bottom: 30px;
        }
        
        .module {
            background: var(--card-bg);
            border-radius: 12px;
            padding: 25px;
            box-shadow: var(--shadow);
            border-left: 5px solid var(--accent-color);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        
        .module:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 15px rgba(0, 0, 0, 0.15);
        }
        
        .module-title {
            font-size: 1.6rem;
            font-weight: 700;
            margin-bottom: 15px;
            color: var(--primary-color);
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .module-content {
            color: var(--text-color);
            line-height: 1.8;
        }
        
        .list-item {
            margin-bottom: 8px;
            padding-left: 15px;
            position: relative;
        }
        
        .list-item.level-1 {
            font-weight: 600;
            color: var(--primary-color);
            border-left: 3px solid var(--accent-color);
            padding-left: 12px;
        }
        
        .list-item.level-2 {
            font-weight: 500;
            color: var(--text-color);
            margin-left: 20px;
            border-left: 2px solid var(--success-color);
            padding-left: 10px;
        }
        
        .list-item strong {
            color: var(--primary-color);
        }
        
        .section-header {
            font-size: 1.3rem;
            font-weight: 700;
            margin: 20px 0 15px 0;
            padding: 12px 20px;
            border-radius: 8px;
            border-left: 4px solid;
        }
        
        .section-header.level-1 {
            background: linear-gradient(135deg, #3498db, #2980b9);
            color: white;
            border-left-color: #2c3e50;
            border-width: 4px;
        }
        
        .section-header.level-2 {
            background: linear-gradient(135deg, #27ae60, #229954);
            color: white;
            border-left-color: #1e8449;
            border-width: 3px;
            margin-left: 15px;
            font-size: 1.1rem;
        }
        
        .preview-note {
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 6px;
            padding: 15px;
            margin-top: 15px;
            font-style: italic;
            color: #6c757d;
        }
        
        .table-container {
            overflow-x: auto;
            margin: 15px 0;
        }
        
        .analysis-table {
            width: 100%;
            border-collapse: collapse;
            margin: 10px 0;
            font-size: 0.95rem;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .analysis-table th {
            background: linear-gradient(135deg, #3498db, #2980b9);
            color: white;
            font-weight: 600;
            padding: 12px 15px;
            text-align: center;
            border-bottom: 2px solid #2c3e50;
        }
        
        .analysis-table td {
            padding: 12px 15px;
            text-align: center;
            border-bottom: 1px solid #ecf0f1;
            vertical-align: middle;
        }
        
        .analysis-table tbody tr:hover {
            background-color: #f8f9fa;
        }
        
        .analysis-table tbody tr:last-child td {
            border-bottom: none;
        }
        
        .content-preview {
            display: block;
        }
        
        .content-full {
            display: none;
        }
        
        .expand-controls {
            text-align: center;
            margin-top: 20px;
        }
        
        .expand-btn {
            background: linear-gradient(135deg, #3498db, #2980b9);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 0.9rem;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 8px;
            margin: 0 auto;
        }
        
        .expand-btn:hover {
            background: linear-gradient(135deg, #2980b9, #3498db);
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(52, 152, 219, 0.3);
        }
        
        .expand-icon {
            transition: transform 0.3s ease;
        }
        
        .expand-btn.expanded .expand-icon {
            transform: rotate(180deg);
        }
        
        .footer {
            text-align: center;
            margin-top: 40px;
            padding: 20px;
            background: rgba(255, 255, 255, 0.9);
            border-radius: 10px;
            color: var(--text-color);
        }
        
        @media (max-width: 768px) {
            .main-grid {
                grid-template-columns: 1fr;
            }
            
            .header h1 {
                font-size: 2rem;
            }
            
            .container {
                padding: 15px;
            }
        }
        """
    
    def extract_event_summary(self, content):
        """从内容中提取事件概要 - 基于第一个事件的核心信息"""
        lines = content.split('\n')
        
        # 查找第一行有效内容（通常包含核心事件信息）
        for line in lines:
            line = line.strip()
            if line and not line.startswith('【') and not line.startswith('#'):
                # 移除开头的 "- " 如果存在
                if line.startswith('- '):
                    line = line[2:]
                
                # 如果内容太长，截取前100个字符并添加省略号
                if len(line) > 100:
                    summary = line[:100] + "..."
                else:
                    summary = line
                
                return summary
        
        # 如果没找到合适的内容，返回通用描述
        return "重要财经事件分析报告，详细解读事件背景、影响及投资机会。"
    
    def extract_additional_investment_content(self, content):
        """提取投资映射模块中表格前后的所有额外内容"""
        lines = content.split('\n')
        additional_content = []
        in_investment_section = False
        table_started = False
        table_ended = False
        
        for line in lines:
            # 开始投资映射部分
            if '【💹 投资映射' in line:
                in_investment_section = True
                continue
            
            if not in_investment_section:
                continue
                
            # 检测表格开始
            if '| 资产类别' in line:
                table_started = True
                continue
            
            # 检测表格结束
            if table_started and not table_ended:
                if line.strip() == '' or (not line.strip().startswith('|') and line.strip()):
                    table_ended = True
                    if line.strip():
                        additional_content.append(line)
                continue
            
            # 收集表格前和表格后的内容
            if (not table_started or table_ended) and line.strip():
                additional_content.append(line)
        
        if not additional_content:
            return ""
        
        # 处理提取的内容，转换为HTML
        html_parts = []
        current_section = ""
        
        for line in additional_content:
            line = line.strip()
            if not line or line.startswith('⚠️'):
                continue
                
            # 检测数字开头的主要部分 (如: 1. **宏观信号解码**)
            if re.match(r'^\d+\.\s*\*\*.*?\*\*', line):
                if current_section:
                    html_parts.append(current_section)
                current_section = f'<div class="section-header level-1">{line}</div>'
            # 检测缩进的子项 (如: - 关键指标)
            elif line.startswith('   - ') or line.startswith('- '):
                item_text = line.replace('   - ', '').replace('- ', '')
                current_section += f'<li class="list-item level-1">{item_text}</li>'
            # 检测其他内容
            elif line and not line.startswith('#'):
                current_section += f'<div class="text-content">{line}</div>'
        
        if current_section:
            html_parts.append(current_section)
        
        return ''.join(html_parts)
    
    def process_investment_mapping(self, content):
        """特殊处理投资映射模块 - 基于standalone版本的表格结构"""
        
        # 检查是否包含表格格式
        if '| 资产类别' in content and '|-------' in content:
            # 解析表格数据
            lines = content.split('\n')
            table_data = []
            in_table = False
            
            for line in lines:
                if '| 资产类别' in line:
                    in_table = True
                    continue
                elif '|-------' in line or '|--------' in line:
                    continue
                elif in_table and line.strip().startswith('|') and line.strip().endswith('|'):
                    # 解析表格行
                    cells = [cell.strip() for cell in line.split('|')[1:-1]]
                    if len(cells) >= 3:
                        table_data.append(cells)
                elif in_table and line.strip() and not line.strip().startswith('|'):
                    break
            
            # 生成投资映射专用HTML结构 - 基于standalone版本
            html_content = '''
                    <div class="content-preview">
                        <div class="table-container">
                            <table class="analysis-table">
                                <thead>
                                    <tr>
                                        <th>投资标的</th>
                                        <th>影响方向</th>
                                        <th>时间周期</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td><strong>消费相关股权</strong></td>
                                        <td style="color: #27ae60;">⬆️ 积极正面</td>
                                        <td>短期&中期</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                    <div class="content-full" style="display: none;">
                        <div class="table-container">
                            <table class="analysis-table">
                                <thead>
                                    <tr>
                                        <th>资产类别</th>
                                        <th>逻辑链条</th>
                                        <th>具体标的/指数</th>
                                        <th>风险收益评级</th>
                                    </tr>
                                </thead>
                                <tbody>'''
            
            # 动态添加表格数据
            for row in table_data:
                asset_type = row[0] if len(row) > 0 else ""
                logic = row[1] if len(row) > 1 else ""
                target = row[2] if len(row) > 2 else ""
                
                # 根据资产类别设置影响方向颜色
                if "股权" in asset_type or "消费" in logic:
                    impact_color = "#27ae60"
                    impact_text = "⬆️ 积极正面"
                    rating = "★★★★☆"
                elif "固收" in asset_type or "利率债" in logic:
                    impact_color = "#f39c12"
                    impact_text = "➡️ 分化影响"
                    rating = "★★★☆☆"
                else:
                    impact_color = "#e74c3c"
                    impact_text = "⬇️ 中性偏弱"
                    rating = "★★☆☆☆"
                
                html_content += f'''
                                    <tr>
                                        <td><strong>{asset_type}</strong></td>
                                        <td>{logic}</td>
                                        <td>{target}</td>
                                        <td>{rating}</td>
                                    </tr>'''
            
            html_content += '''
                                </tbody>
                            </table>
                        </div>
                        
                        ''' + self.extract_additional_investment_content(content) + '''
                    </div>
                    <div class="expand-controls">
                        <button class="expand-btn" onclick="toggleExpand(this)">
                            <span class="expand-icon">▼</span>
                            <span>展开更多内容</span>
                        </button>
                    </div>'''
            
            return html_content
        else:
            # 如果没有表格格式，使用普通处理
            return self.process_section_headers(content)
    
    def get_investment_mapping_css(self):
        """返回投资映射模块专用CSS - 基于standalone版本"""
        return """
        .table-container {
            overflow-x: auto;
            margin: 15px 0;
        }
        
        .analysis-table {
            width: 100%;
            border-collapse: collapse;
            margin: 10px 0;
            font-size: 0.95rem;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .analysis-table th {
            background: linear-gradient(135deg, #3498db, #2980b9);
            color: white;
            font-weight: 600;
            padding: 12px 15px;
            text-align: center;
            border-bottom: 2px solid #2c3e50;
        }
        
        .analysis-table td {
            padding: 12px 15px;
            text-align: center;
            border-bottom: 1px solid #ecf0f1;
            vertical-align: middle;
        }
        
        .analysis-table tbody tr:hover {
            background-color: #f8f9fa;
        }
        
        .analysis-table tbody tr:last-child td {
            border-bottom: none;
        }
        
        .content-preview {
            display: block;
        }
        
        .content-full {
            display: none;
        }
        
        .expand-controls {
            text-align: center;
            margin-top: 20px;
        }
        
        .expand-btn {
            background: linear-gradient(135deg, #3498db, #2980b9);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 0.9rem;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 8px;
            margin: 0 auto;
        }
        
        .expand-btn:hover {
            background: linear-gradient(135deg, #2980b9, #3498db);
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(52, 152, 219, 0.3);
        }
        
        .expand-icon {
            transition: transform 0.3s ease;
        }
        
        .expand-btn.expanded .expand-icon {
            transform: rotate(180deg);
        }
        """
    
    def get_investment_mapping_js(self):
        """返回投资映射交互JavaScript - 基于standalone版本"""
        return """
        function toggleExpand(button) {
            const card = button.closest('.module');
            const preview = card.querySelector('.content-preview');
            const full = card.querySelector('.content-full');
            const icon = button.querySelector('.expand-icon');
            const text = button.querySelector('span:last-child');
            
            if (full.style.display === 'none') {
                full.style.display = 'block';
                preview.style.display = 'none';
                icon.textContent = '▲';
                text.textContent = '收起内容';
                button.classList.add('expanded');
            } else {
                full.style.display = 'none';
                preview.style.display = 'block';
                icon.textContent = '▼';
                text.textContent = '展开更多内容';
                button.classList.remove('expanded');
            }
        }
        """
    def process_section_headers(self, content):
        """处理标题层级 - 基于认可的standalone版本逻辑"""
        lines = content.split('\n')
        processed_lines = []
        
        for line in lines:
            # 检测一级标题: - **标题**:
            level1_match = re.match(r'^- \*\*([^*]+)\*\*[：:]\s*$', line.strip())
            if level1_match:
                title = level1_match.group(1)
                processed_lines.append(f'                        <div class="section-header level-1">{title}</div>')
                continue
                
            # 检测二级标题: 空格空格- **标题**:
            level2_match = re.match(r'^  - \*\*([^*]+)\*\*[：:]\s*', line.strip())
            if level2_match:
                title = level2_match.group(1)
                processed_lines.append(f'                        <div class="section-header level-2">{title}</div>')
                continue
            
            # 检测一级列表项: - **粗体**：内容
            level1_list = re.match(r'^- \*\*([^*]+)\*\*[：:](.+)$', line.strip())
            if level1_list:
                bold_text = level1_list.group(1)
                content_text = level1_list.group(2).strip()
                processed_lines.append(f'                        <li class="list-item level-1"><strong>{bold_text}</strong>：{content_text}</li>')
                continue
                
            # 检测二级列表项: 空格空格- **粗体**：内容
            level2_list = re.match(r'^  - \*\*([^*]+)\*\*[：:](.+)$', line.strip())
            if level2_list:
                bold_text = level2_list.group(1)
                content_text = level2_list.group(2).strip()
                processed_lines.append(f'                        <li class="list-item level-2"><strong>{bold_text}</strong>：{content_text}</li>')
                continue
            
            # 普通行处理
            if line.strip():
                processed_lines.append(f'                        <p>{line.strip()}</p>')
            else:
                processed_lines.append('')
        
        return '\n'.join(processed_lines)
    
    def render_to_html(self, txt_file_path, output_file_path=None):
        """将TXT文件渲染为标准化HTML"""
        
        # 读取源文件
        with open(txt_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 分析四大模块
        modules = {}
        current_module = None
        current_content = []
        
        lines = content.split('\n')
        for line in lines:
            # 检测模块标题 - 使用新的映射逻辑
            if any(icon in line for icon in self.module_mapping.keys()):
                if current_module and current_content:
                    modules[current_module] = '\n'.join(current_content)
                
                for icon, name in self.module_mapping.items():
                    if icon in line:
                        current_module = name
                        current_content = []
                        break
            else:
                if current_module:
                    current_content.append(line)
        
        # 添加最后一个模块
        if current_module and current_content:
            modules[current_module] = '\n'.join(current_content)
        
        # 提取事件概要
        event_summary = self.extract_event_summary(content)
        
        # 生成HTML
        timestamp = datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
        
        html_template = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>财经新闻AI深度解读报告</title>
    <style>
        {self.get_css_styles()}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 财经新闻AI深度解读报告</h1>
            <p class="subtitle">穿透"热闹"看"门道"，洞察事件底层逻辑，把握投资机会</p>
            <p class="timestamp">生成时间：{timestamp}</p>
        </div>
        
        <div class="news-summary">
            <h2>📰 新闻简介</h2>
            <p>{event_summary}</p>
        </div>
        
        <div class="main-grid">"""
        
        # 按指定顺序渲染模块
        module_order = ['事件梳理', '局面评估', '底层逻辑', '投资映射']
        
        for module_name in module_order:
            if module_name in modules:
                icon = self.module_icons[module_name]
                content = modules[module_name]
                
                # 投资映射模块使用特殊处理
                if module_name == '投资映射':
                    processed_content = self.process_investment_mapping(content)
                    show_preview_note = False
                else:
                    # 其他模块使用普通处理
                    processed_content = self.process_section_headers(content)
                    show_preview_note = False
                
                html_template += f"""
            <div class="module">
                <div class="module-title">
                    <span>{icon}</span>
                    <span>{module_name}</span>
                </div>
                <div class="module-content">"""
                
                if module_name == '投资映射':
                    # 投资映射模块直接插入处理后的HTML
                    html_template += processed_content
                else:
                    # 其他模块使用列表包装
                    html_template += f"""
                    <ul style="list-style: none; padding: 0;">
{processed_content}
                    </ul>"""
                
                if show_preview_note:
                    html_template += """
                    <div class="preview-note">
                        注：此模块内容较长，以上为预览部分
                    </div>"""
                
                html_template += """
                </div>
            </div>"""
        
        html_template += """
        </div>
        
        <div class="footer">
            <p>© 2025 金融事件分析系统 | 基于标准化模板生成</p>
        </div>
    </div>

    <script>
        function toggleExpand(button) {
            const card = button.closest('.module');
            const preview = card.querySelector('.content-preview');
            const full = card.querySelector('.content-full');
            const icon = button.querySelector('.expand-icon');
            const text = button.querySelector('span:last-child');
            
            if (full.style.display === 'none') {
                full.style.display = 'block';
                preview.style.display = 'none';
                icon.textContent = '▲';
                text.textContent = '收起内容';
                button.classList.add('expanded');
            } else {
                full.style.display = 'none';
                preview.style.display = 'block';
                icon.textContent = '▼';
                text.textContent = '展开更多内容';
                button.classList.remove('expanded');
            }
        }
    </script>
</body>
</html>"""
        
        # 保存文件
        if not output_file_path:
            base_name = Path(txt_file_path).stem
            output_file_path = f"temp/{base_name}_standardized.html"
        
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(html_template)
        
        print(f"✅ 标准化渲染完成: {output_file_path}")
        return output_file_path

def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description='标准化HTML渲染器')
    parser.add_argument('txt_file', help='源TXT文件路径')
    parser.add_argument('-o', '--output', help='输出HTML文件路径')
    
    args = parser.parse_args()
    
    renderer = StandardizedRenderer()
    output_file = renderer.render_to_html(args.txt_file, args.output)
    
    print(f"🎉 渲染完成，请查看: {output_file}")

if __name__ == "__main__":
    main()
