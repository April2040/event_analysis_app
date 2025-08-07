"""
新闻爬虫模块初始化文件
"""

from .crawler import NewsWebCrawler
from .html_generator import HTMLReportGenerator
from .utils import save_news_data, load_news_data, format_news_for_display, get_news_statistics

__all__ = [
    'NewsWebCrawler',
    'HTMLReportGenerator', 
    'save_news_data',
    'load_news_data',
    'format_news_for_display',
    'get_news_statistics'
]
