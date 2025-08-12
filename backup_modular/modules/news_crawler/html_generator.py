"""
HTML报告生成器
负责生成精美的新闻HTML报告
"""

from datetime import datetime
from typing import List, Dict

class HTMLReportGenerator:
    """HTML报告生成器"""
    
    def generate_html(self, news_list: List[Dict]) -> str:
        """生成HTML内容"""
        current_time = datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
        
        html_template = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>财经新闻热点 - {current_time}</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
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
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 700;
        }}
        
        .header .subtitle {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .stats {{
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-top: 20px;
            flex-wrap: wrap;
        }}
        
        .stat-item {{
            text-align: center;
        }}
        
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            display: block;
        }}
        
        .stat-label {{
            font-size: 0.9em;
            opacity: 0.8;
        }}
        
        .news-grid {{
            padding: 30px;
        }}
        
        .news-item {{
            background: white;
            border: 1px solid #e1e8ed;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 20px;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }}
        
        .news-item:hover {{
            transform: translateY(-5px);
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
            border-color: #1da1f2;
        }}
        
        .news-header {{
            display: flex;
            align-items: center;
            margin-bottom: 15px;
            flex-wrap: wrap;
            gap: 10px;
        }}
        
        .news-rank {{
            background: linear-gradient(135deg, #ff6b6b, #ee5a24);
            color: white;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 1.1em;
            flex-shrink: 0;
        }}
        
        .news-meta {{
            flex: 1;
            min-width: 0;
        }}
        
        .news-source {{
            color: #1da1f2;
            font-weight: 600;
            margin-bottom: 3px;
        }}
        
        .news-time {{
            color: #657786;
            font-size: 0.9em;
        }}
        
        .heat-score {{
            background: linear-gradient(135deg, #ffd700, #ffed4e);
            color: #333;
            padding: 5px 12px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 0.9em;
            white-space: nowrap;
        }}
        
        .news-title {{
            font-size: 1.3em;
            font-weight: 600;
            color: #14171a;
            margin-bottom: 12px;
            line-height: 1.4;
        }}
        
        .news-title a {{
            color: inherit;
            text-decoration: none;
            transition: color 0.3s ease;
        }}
        
        .news-title a:hover {{
            color: #1da1f2;
        }}
        
        .news-summary {{
            color: #657786;
            line-height: 1.5;
            margin-bottom: 15px;
        }}
        
        .news-footer {{
            display: flex;
            align-items: center;
            gap: 15px;
            flex-wrap: wrap;
        }}
        
        .category-tag {{
            background: #e1f5fe;
            color: #0277bd;
            padding: 4px 10px;
            border-radius: 15px;
            font-size: 0.85em;
            font-weight: 500;
        }}
        
        .keywords {{
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }}
        
        .keyword {{
            background: #f5f8fa;
            color: #536471;
            padding: 3px 8px;
            border-radius: 10px;
            font-size: 0.8em;
        }}
        
        .footer {{
            background: #f7f9fa;
            padding: 20px;
            text-align: center;
            color: #657786;
            border-top: 1px solid #e1e8ed;
        }}
        
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 2em;
            }}
            
            .stats {{
                gap: 20px;
            }}
            
            .news-grid {{
                padding: 20px;
            }}
            
            .news-item {{
                padding: 20px;
            }}
            
            .news-title {{
                font-size: 1.2em;
            }}
        }}
        
        .heat-high {{ border-left: 4px solid #ff4757; }}
        .heat-medium {{ border-left: 4px solid #ffa502; }}
        .heat-low {{ border-left: 4px solid #2ed573; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1><i class="fas fa-chart-line"></i> 财经新闻热点</h1>
            <div class="subtitle">基于RSS源的实时财经资讯聚合</div>
            <div class="subtitle" style="margin-top: 10px;">
                <i class="fas fa-clock"></i> 更新时间: {current_time}
            </div>
            <div class="stats">
                <div class="stat-item">
                    <span class="stat-number">{len(news_list)}</span>
                    <span class="stat-label">热点新闻</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">{len(set(item.get('category', '综合') for item in news_list))}</span>
                    <span class="stat-label">涵盖分类</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">{len(set(item.get('source', '') for item in news_list))}</span>
                    <span class="stat-label">新闻源</span>
                </div>
            </div>
        </div>
        
        <div class="news-grid">
"""
        
        # 生成新闻条目
        for i, news in enumerate(news_list, 1):
            heat_score = news.get('heat_score', 0)
            heat_class = 'heat-high' if heat_score >= 0.8 else 'heat-medium' if heat_score >= 0.5 else 'heat-low'
            
            keywords_html = ''.join([f'<span class="keyword">{kw}</span>' for kw in news.get('keywords', [])[:4]])
            
            html_template += f"""
            <div class="news-item {heat_class}">
                <div class="news-header">
                    <div class="news-rank">{i}</div>
                    <div class="news-meta">
                        <div class="news-source"><i class="fas fa-newspaper"></i> {news.get('source', '未知来源')}</div>
                        <div class="news-time"><i class="fas fa-clock"></i> {news.get('published', '')}</div>
                    </div>
                    <div class="heat-score">
                        <i class="fas fa-fire"></i> {heat_score:.2f}
                    </div>
                </div>
                
                <h3 class="news-title">
                    <a href="{news.get('link', '#')}" target="_blank">{news.get('title', '无标题')}</a>
                </h3>
                
                <p class="news-summary">{news.get('summary', '暂无摘要')}</p>
                
                <div class="news-footer">
                    <span class="category-tag">
                        <i class="fas fa-tag"></i> {news.get('category', '综合')}
                    </span>
                    <div class="keywords">
                        {keywords_html}
                    </div>
                </div>
            </div>
"""
        
        html_template += """
        </div>
        
        <div class="footer">
            <p><i class="fas fa-robot"></i> 由新闻爬虫模块自动生成</p>
            <p style="margin-top: 5px; font-size: 0.9em;">
                数据来源: 多个财经新闻网站 | 
                热度算法: 时间(30%) + 关键词(25%) + 标题(20%) + 来源(25%)
            </p>
        </div>
    </div>
    
    <script>
        // 添加平滑滚动
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({
                    behavior: 'smooth'
                });
            });
        });
        
        // 添加新闻项目动画
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, observerOptions);
        
        document.querySelectorAll('.news-item').forEach((item, index) => {
            item.style.opacity = '0';
            item.style.transform = 'translateY(20px)';
            item.style.transition = `opacity 0.6s ease ${index * 0.1}s, transform 0.6s ease ${index * 0.1}s`;
            observer.observe(item);
        });
    </script>
</body>
</html>
"""
        
        return html_template
