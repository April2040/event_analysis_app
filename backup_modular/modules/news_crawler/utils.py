"""
新闻爬虫模块 - 工具函数
"""

import json
import os
from datetime import datetime
from typing import List, Dict

def save_news_data(news_list: List[Dict], output_dir: str = "outputs/news_reports") -> str:
    """保存新闻数据为JSON文件"""
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_file = os.path.join(output_dir, f"news_data_{timestamp}.json")
    
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(news_list, f, ensure_ascii=False, indent=2)
    
    return json_file

def load_news_data(json_file: str) -> List[Dict]:
    """从JSON文件加载新闻数据"""
    with open(json_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def format_news_for_display(news_item: Dict) -> str:
    """格式化新闻条目用于显示"""
    return f"""
标题: {news_item.get('title', '无标题')}
来源: {news_item.get('source', '未知来源')}
分类: {news_item.get('category', '综合')}
热度: {news_item.get('heat_score', 0):.2f}
关键词: {', '.join(news_item.get('keywords', []))}
发布时间: {news_item.get('published', '未知时间')}
摘要: {news_item.get('summary', '暂无摘要')}
链接: {news_item.get('link', '#')}
"""

def get_news_statistics(news_list: List[Dict]) -> Dict:
    """获取新闻统计信息"""
    if not news_list:
        return {}
    
    categories = set(news.get('category', '综合') for news in news_list)
    sources = set(news.get('source', '未知') for news in news_list)
    
    avg_heat_score = sum(news.get('heat_score', 0) for news in news_list) / len(news_list)
    
    return {
        "total_news": len(news_list),
        "total_categories": len(categories),
        "total_sources": len(sources),
        "categories": list(categories),
        "sources": list(sources),
        "average_heat_score": round(avg_heat_score, 2),
        "max_heat_score": max(news.get('heat_score', 0) for news in news_list),
        "min_heat_score": min(news.get('heat_score', 0) for news in news_list)
    }
