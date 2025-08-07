"""
分析提示词模板
"""

def get_analysis_prompt(news_item: dict) -> str:
    """获取新闻分析提示词"""
    title = news_item.get('title', '')
    summary = news_item.get('summary', '')
    category = news_item.get('category', '')
    source = news_item.get('source', '')
    
    prompt = f"""
请对以下财经新闻进行专业分析：

标题：{title}
分类：{category}
来源：{source}
摘要：{summary}

请从以下角度进行分析：
1. 事件核心要点提炼
2. 市场影响评估（短期和长期）
3. 投资机会识别
4. 风险因素分析
5. 相关行业影响
6. 后续发展预判

请保持分析的客观性和专业性，字数控制在300-500字。
"""
    
    return prompt

def get_summary_prompt(news_list: list) -> str:
    """获取新闻总结提示词"""
    news_titles = "\n".join([f"- {news.get('title', '')}" for news in news_list[:10]])
    
    prompt = f"""
基于以下财经新闻标题，请生成今日财经要闻摘要：

{news_titles}

请提供：
1. 市场整体态势概括（2-3句话）
2. 主要热点事件总结（3-5个要点）
3. 重点关注领域（2-3个行业或政策方向）

要求简洁明了，突出重点。
"""
    
    return prompt

def get_investment_analysis_prompt() -> str:
    """获取投资分析提示词"""
    return """
基于当前财经新闻热点，请提供投资分析建议：

1. 市场趋势判断
2. 热点板块识别
3. 投资机会评估
4. 风险提示
5. 投资策略建议

请保持客观、专业的投资建议，不构成具体投资指导。
"""
