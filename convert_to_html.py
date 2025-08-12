#!/usr/bin/env python3
"""
HTML转换工具 - 将分析TXT文件转换为HTML页面
解决AI HTML生成超时问题的备用方案
"""

import os
import sys
from datetime import datetime

def convert_txt_to_html(txt_file_path):
    """将分析TXT文件转换为简洁的HTML页面"""
    try:
        # 读取TXT文件内容
        with open(txt_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 获取文件名信息
        filename = os.path.basename(txt_file_path)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 生成HTML模板
        html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>财经事件分析报告 - {filename}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.7;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
        }}
        .container {{
            background: white;
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            margin: 20px 0;
        }}
        h1 {{
            color: #2c3e50;
            text-align: center;
            border-bottom: 4px solid #3498db;
            padding-bottom: 15px;
            margin-bottom: 30px;
            font-size: 2.2em;
        }}
        .content {{
            white-space: pre-wrap;
            font-size: 16px;
            line-height: 1.8;
            color: #34495e;
        }}
        .timestamp {{
            text-align: center;
            color: #7f8c8d;
            margin-top: 30px;
            font-size: 14px;
            padding-top: 20px;
            border-top: 1px solid #ecf0f1;
        }}
        .header-info {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 25px;
            border-left: 4px solid #3498db;
        }}
        .highlight {{
            background: linear-gradient(120deg, #a8edea 0%, #fed6e3 100%);
            padding: 2px 6px;
            border-radius: 3px;
        }}
        @media (max-width: 768px) {{
            body {{ padding: 10px; }}
            .container {{ padding: 20px; }}
            h1 {{ font-size: 1.8em; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🧠 财经事件分析报告</h1>
        
        <div class="header-info">
            <strong>📁 文件:</strong> {filename}<br>
            <strong>🕐 转换时间:</strong> {timestamp}<br>
            <strong>⚡ 生成方式:</strong> 本地HTML转换（解决AI超时问题）
        </div>
        
        <div class="content">{content}</div>
        
        <div class="timestamp">
            <p>📝 本报告由财经事件分析系统生成</p>
            <p>🔄 HTML转换时间: {timestamp}</p>
        </div>
    </div>
</body>
</html>"""
        
        # 生成HTML文件路径
        html_file_path = txt_file_path.replace('.txt', '.html')
        
        # 保存HTML文件
        with open(html_file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ 成功转换: {txt_file_path} → {html_file_path}")
        return html_file_path
        
    except Exception as e:
        print(f"❌ 转换失败: {e}")
        return None

def convert_latest_analysis():
    """转换最新的分析文件"""
    temp_dir = "temp"
    if not os.path.exists(temp_dir):
        print("❌ temp目录不存在")
        return
    
    # 找到最新的分析文件
    txt_files = [f for f in os.listdir(temp_dir) if f.startswith('temp_analysis_') and f.endswith('.txt')]
    if not txt_files:
        print("❌ 没有找到分析文件")
        return
    
    # 按时间排序，获取最新文件
    txt_files.sort(reverse=True)
    latest_file = os.path.join(temp_dir, txt_files[0])
    
    print(f"🔍 找到最新分析文件: {latest_file}")
    html_file = convert_txt_to_html(latest_file)
    
    if html_file:
        print(f"🌐 HTML文件已生成: {html_file}")
        print(f"📂 您可以在浏览器中打开: file://{os.path.abspath(html_file)}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # 转换指定文件
        txt_file = sys.argv[1]
        if os.path.exists(txt_file):
            convert_txt_to_html(txt_file)
        else:
            print(f"❌ 文件不存在: {txt_file}")
    else:
        # 转换最新文件
        convert_latest_analysis()
