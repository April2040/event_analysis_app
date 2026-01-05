#!/usr/bin/env python3
"""
创建财经事件分析应用的图标
生成一个包含图表和趋势线的专业财经主题图标
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont
import numpy as np

def create_financial_icon(size=512):
    """创建财经分析主题的图标"""
    # 创建画布 - 使用现代的渐变背景
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 绘制圆角矩形背景 - 深蓝到浅蓝渐变
    margin = size // 16
    corner_radius = size // 8
    
    # 创建渐变背景
    for y in range(size):
        color_ratio = y / size
        r = int(30 + (70 - 30) * color_ratio)  # 深蓝到浅蓝
        g = int(80 + (130 - 80) * color_ratio)
        b = int(180 + (220 - 180) * color_ratio)
        draw.rectangle([0, y, size, y+1], fill=(r, g, b, 255))
    
    # 绘制圆角遮罩
    mask = Image.new('L', (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([margin, margin, size-margin, size-margin], 
                               radius=corner_radius, fill=255)
    
    # 应用遮罩
    img.putalpha(mask)
    
    # 重新创建draw对象
    draw = ImageDraw.Draw(img)
    
    # 绘制图表区域
    chart_left = size // 4
    chart_right = size * 3 // 4
    chart_top = size // 3
    chart_bottom = size * 2 // 3
    
    # 绘制网格线
    grid_color = (255, 255, 255, 100)
    for i in range(3):
        y = chart_top + (chart_bottom - chart_top) * i // 2
        draw.line([chart_left, y, chart_right, y], fill=grid_color, width=1)
    
    for i in range(4):
        x = chart_left + (chart_right - chart_left) * i // 3
        draw.line([x, chart_top, x, chart_bottom], fill=grid_color, width=1)
    
    # 生成上升趋势的数据点
    points = []
    x_step = (chart_right - chart_left) // 8
    base_y = chart_bottom - size // 20
    
    for i in range(9):
        x = chart_left + i * x_step
        # 添加一些随机波动但整体上升的趋势
        noise = np.sin(i * 0.5) * size // 40
        trend = -i * size // 60  # 上升趋势
        y = base_y + trend + noise
        points.append((x, int(y)))
    
    # 绘制趋势线 - 绿色表示上涨
    line_color = (0, 255, 100, 255)
    line_width = max(2, size // 128)
    
    for i in range(len(points) - 1):
        draw.line([points[i], points[i+1]], fill=line_color, width=line_width)
    
    # 绘制数据点
    point_radius = max(2, size // 100)
    for point in points:
        draw.ellipse([point[0]-point_radius, point[1]-point_radius,
                     point[0]+point_radius, point[1]+point_radius],
                    fill=(255, 255, 255, 255))
    
    # 绘制柱状图
    bar_width = size // 40
    bar_colors = [(255, 100, 100, 200), (100, 255, 100, 200), (100, 100, 255, 200)]
    
    for i in range(3):
        x = chart_left + size // 12 + i * size // 8
        height = size // 20 + (i + 1) * size // 30
        y = chart_bottom - height
        
        draw.rectangle([x, y, x + bar_width, chart_bottom],
                      fill=bar_colors[i % len(bar_colors)])
    
    # 添加"AI"标识
    try:
        # 尝试使用系统字体
        font_size = size // 12
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
    except:
        # 如果没有找到字体，使用默认字体
        font = ImageFont.load_default()
    
    ai_text = "AI"
    text_color = (255, 255, 255, 255)
    
    # 计算文本位置
    bbox = draw.textbbox((0, 0), ai_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    text_x = size - text_width - size // 20
    text_y = size // 20
    
    # 绘制AI标识背景
    padding = size // 60
    draw.rounded_rectangle([text_x - padding, text_y - padding,
                           text_x + text_width + padding, text_y + text_height + padding],
                          radius=size // 40, fill=(0, 0, 0, 150))
    
    # 绘制AI文本
    draw.text((text_x, text_y), ai_text, fill=text_color, font=font)
    
    return img

def create_icns_file(png_path, icns_path):
    """将PNG转换为ICNS文件"""
    try:
        # 使用macOS的iconutil命令创建icns
        import subprocess
        import tempfile
        import shutil
        
        # 创建临时目录
        with tempfile.TemporaryDirectory() as temp_dir:
            iconset_dir = os.path.join(temp_dir, "icon.iconset")
            os.makedirs(iconset_dir)
            
            # 创建各种尺寸的图标
            base_img = Image.open(png_path)
            sizes = [16, 32, 64, 128, 256, 512, 1024]
            
            for size in sizes:
                # 标准分辨率
                resized = base_img.resize((size, size), Image.Resampling.LANCZOS)
                resized.save(os.path.join(iconset_dir, f"icon_{size}x{size}.png"))
                
                # 高分辨率 (除了1024，因为没有2048x2048)
                if size <= 512:
                    resized_2x = base_img.resize((size*2, size*2), Image.Resampling.LANCZOS)
                    resized_2x.save(os.path.join(iconset_dir, f"icon_{size}x{size}@2x.png"))
            
            # 使用iconutil创建icns文件
            result = subprocess.run(['iconutil', '-c', 'icns', iconset_dir, '-o', icns_path],
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                return True
            else:
                print(f"iconutil错误: {result.stderr}")
                return False
                
    except Exception as e:
        print(f"创建icns文件时出错: {e}")
        return False

def main():
    # 创建图标
    icon = create_financial_icon(512)
    
    # 保存为PNG
    png_path = "/Users/qiyi/coding/event_analysis_app/macOS/app_icon.png"
    icon.save(png_path, "PNG")
    print(f"已创建PNG图标: {png_path}")
    
    # 转换为ICNS
    icns_path = "/Users/qiyi/coding/event_analysis_app/macOS/EventAnalysis.app/Contents/Resources/app.icns"
    
    # 确保Resources目录存在
    os.makedirs(os.path.dirname(icns_path), exist_ok=True)
    
    if create_icns_file(png_path, icns_path):
        print(f"已创建ICNS图标: {icns_path}")
        return True
    else:
        print("ICNS创建失败，尝试直接复制PNG作为临时方案")
        # 作为备选方案，直接复制PNG到Resources目录
        import shutil
        backup_path = icns_path.replace('.icns', '.png')
        shutil.copy(png_path, backup_path)
        print(f"已创建备选PNG图标: {backup_path}")
        return False

if __name__ == "__main__":
    main()