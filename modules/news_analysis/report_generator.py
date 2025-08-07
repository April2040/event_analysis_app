"""
分析报告生成器
生成专业的HTML分析报告
"""

from datetime import datetime
from typing import Dict, Any, List

class AnalysisReportGenerator:
    """分析报告生成器"""
    
    def generate_html(self, analysis_result: Dict[str, Any]) -> str:
        """生成HTML分析报告"""
        current_time = datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
        
        html_template = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>智能新闻分析报告 - {current_time}</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
            min-height: 100vh;
            padding: 20px;
            color: #333;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #1a252f 0%, #2c3e50 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.8em;
            margin-bottom: 15px;
            font-weight: 700;
        }}
        
        .header .subtitle {{
            font-size: 1.2em;
            opacity: 0.9;
            margin-bottom: 20px;
        }}
        
        .analysis-stats {{
            display: flex;
            justify-content: center;
            gap: 40px;
            margin-top: 25px;
            flex-wrap: wrap;
        }}
        
        .stat-item {{
            text-align: center;
            background: rgba(255, 255, 255, 0.1);
            padding: 15px 25px;
            border-radius: 15px;
        }}
        
        .stat-number {{
            font-size: 2.2em;
            font-weight: bold;
            display: block;
            color: #3498db;
        }}
        
        .stat-label {{
            font-size: 0.95em;
            opacity: 0.8;
            margin-top: 5px;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .section {{
            margin-bottom: 40px;
            background: #f8fafc;
            border-radius: 15px;
            padding: 30px;
            border-left: 5px solid #3498db;
        }}
        
        .section h2 {{
            color: #2c3e50;
            font-size: 1.8em;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .section h3 {{
            color: #34495e;
            font-size: 1.4em;
            margin: 20px 0 15px 0;
            padding-bottom: 8px;
            border-bottom: 2px solid #ecf0f1;
        }}
        
        .overall-analysis {{
            background: #fff;
            border: 1px solid #e1e8ed;
            border-radius: 12px;
            padding: 25px;
            line-height: 1.8;
            font-size: 1.05em;
            color: #2c3e50;
        }}
        
        .news-analysis-item {{
            background: white;
            border: 1px solid #e1e8ed;
            border-radius: 12px;
            padding: 25px;
            margin-bottom: 20px;
            transition: all 0.3s ease;
        }}
        
        .news-analysis-item:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        }}
        
        .news-title {{
            font-size: 1.3em;
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 10px;
            line-height: 1.4;
        }}
        
        .news-meta {{
            display: flex;
            gap: 20px;
            margin-bottom: 15px;
            flex-wrap: wrap;
        }}
        
        .meta-item {{
            background: #ecf0f1;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.9em;
            color: #7f8c8d;
        }}
        
        .news-analysis-content {{
            line-height: 1.7;
            color: #34495e;
        }}
        
        .insights-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        
        .insight-card {{
            background: white;
            border: 1px solid #e1e8ed;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
        }}
        
        .insight-icon {{
            font-size: 2.5em;
            color: #3498db;
            margin-bottom: 15px;
        }}
        
        .insight-text {{
            font-weight: 600;
            color: #2c3e50;
        }}
        
        .categories-chart {{
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            margin-top: 20px;
        }}
        
        .category-item {{
            background: #3498db;
            color: white;
            padding: 8px 16px;
            border-radius: 25px;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .risk-assessment {{
            text-align: center;
            padding: 25px;
            background: white;
            border-radius: 12px;
            border: 1px solid #e1e8ed;
        }}
        
        .risk-level {{
            font-size: 2em;
            font-weight: bold;
            margin: 15px 0;
        }}
        
        .risk-neutral {{ color: #f39c12; }}
        .risk-positive {{ color: #27ae60; }}
        .risk-negative {{ color: #e74c3c; }}
        
        .footer {{
            background: #34495e;
            color: white;
            padding: 30px;
            text-align: center;
            border-top: 1px solid #e1e8ed;
        }}
        
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 2.2em;
            }}
            
            .analysis-stats {{
                gap: 20px;
            }}
            
            .content {{
                padding: 25px;
            }}
            
            .section {{
                padding: 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1><i class="fas fa-brain"></i> 智能新闻分析报告</h1>
            <div class="subtitle">基于DeepSeek AI的深度财经新闻分析</div>
            <div class="subtitle" style="margin-top: 10px;">
                <i class="fas fa-clock"></i> 分析时间: {current_time}
            </div>
            <div class="analysis-stats">
                <div class="stat-item">
                    <span class="stat-number">{analysis_result.get('total_news', 0)}</span>
                    <span class="stat-label">新闻总数</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">{analysis_result.get('analyzed_news', 0)}</span>
                    <span class="stat-label">深度分析</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">{len(analysis_result.get('categories_distribution', {}))}</span>
                    <span class="stat-label">涵盖分类</span>
                </div>
            </div>
        </div>
        
        <div class="content">
            <!-- 新闻概览 -->
            <div class="section">
                <h2><i class="fas fa-newspaper"></i> 新闻概览</h2>
                <div class="overall-analysis">
                    {analysis_result.get('news_summary', '暂无概览')}
                </div>
            </div>
            
            <!-- 整体分析 -->
            <div class="section">
                <h2><i class="fas fa-chart-line"></i> 整体市场分析</h2>
                <div class="overall-analysis">
                    {analysis_result.get('overall_analysis', '暂无整体分析')}
                </div>
            </div>
            
            <!-- 投资洞察 -->
            <div class="section">
                <h2><i class="fas fa-lightbulb"></i> 投资洞察</h2>
                <div class="insights-grid">
"""
        
        # 添加投资洞察卡片
        insights = analysis_result.get('investment_insights', [])
        if insights:
            for insight in insights:
                html_template += f"""
                    <div class="insight-card">
                        <div class="insight-icon"><i class="fas fa-star"></i></div>
                        <div class="insight-text">{insight}</div>
                    </div>
"""
        else:
            html_template += """
                    <div class="insight-card">
                        <div class="insight-icon"><i class="fas fa-info-circle"></i></div>
                        <div class="insight-text">暂无特定投资洞察</div>
                    </div>
"""
        
        html_template += """
                </div>
            </div>
            
            <!-- 风险评估 -->
            <div class="section">
                <h2><i class="fas fa-shield-alt"></i> 风险评估</h2>
                <div class="risk-assessment">
                    <div>市场情绪评估</div>
"""
        
        # 添加风险评估
        risk_level = analysis_result.get('risk_assessment', '中性')
        risk_class = 'risk-neutral'
        if '乐观' in risk_level:
            risk_class = 'risk-positive'
        elif '谨慎' in risk_level:
            risk_class = 'risk-negative'
        
        html_template += f"""
                    <div class="risk-level {risk_class}">{risk_level}</div>
                    <div>基于当前新闻热点的综合评估</div>
                </div>
            </div>
            
            <!-- 分类分布 -->
            <div class="section">
                <h2><i class="fas fa-tags"></i> 新闻分类分布</h2>
                <div class="categories-chart">
"""
        
        # 添加分类分布
        categories = analysis_result.get('categories_distribution', {})
        for category, count in categories.items():
            html_template += f"""
                    <div class="category-item">
                        <i class="fas fa-tag"></i>
                        <span>{category} ({count})</span>
                    </div>
"""
        
        html_template += """
                </div>
            </div>
            
            <!-- 个别新闻分析 -->
            <div class="section">
                <h2><i class="fas fa-microscope"></i> 重点新闻深度分析</h2>
"""
        
        # 添加个别新闻分析
        individual_analyses = analysis_result.get('individual_analyses', [])
        if individual_analyses:
            for i, analysis in enumerate(individual_analyses, 1):
                html_template += f"""
                <div class="news-analysis-item">
                    <div class="news-title">{i}. {analysis.get('news_title', '无标题')}</div>
                    <div class="news-meta">
                        <span class="meta-item"><i class="fas fa-newspaper"></i> {analysis.get('news_source', '未知来源')}</span>
                        <span class="meta-item"><i class="fas fa-tag"></i> {analysis.get('news_category', '综合')}</span>
                        <span class="meta-item"><i class="fas fa-fire"></i> 热度: {analysis.get('heat_score', 0):.2f}</span>
                    </div>
                    <div class="news-analysis-content">
                        {analysis.get('analysis', '暂无分析')}
                    </div>
                </div>
"""
        else:
            html_template += """
                <div class="news-analysis-item">
                    <div class="news-analysis-content">暂无深度分析内容</div>
                </div>
"""
        
        html_template += f"""
            </div>
        </div>
        
        <div class="footer">
            <p><i class="fas fa-robot"></i> 由智能新闻分析系统自动生成</p>
            <p style="margin-top: 8px; font-size: 0.9em; opacity: 0.8;">
                基于DeepSeek AI技术 | 分析时间: {analysis_result.get('timestamp', current_time)}
            </p>
        </div>
    </div>
    
    <script>
        // 添加页面加载动画
        document.addEventListener('DOMContentLoaded', function() {{
            const sections = document.querySelectorAll('.section');
            sections.forEach((section, index) => {{
                section.style.opacity = '0';
                section.style.transform = 'translateY(30px)';
                section.style.transition = `opacity 0.6s ease ${{index * 0.1}}s, transform 0.6s ease ${{index * 0.1}}s`;
                
                setTimeout(() => {{
                    section.style.opacity = '1';
                    section.style.transform = 'translateY(0)';
                }}, index * 100);
            }});
        }});
    </script>
</body>
</html>
"""
        
        return html_template
