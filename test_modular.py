"""
测试模块化系统的导入功能
"""
import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from modules.news_crawler.crawler import NewsWebCrawler
    print("✅ 新闻爬虫模块导入成功")
except ImportError as e:
    print(f"❌ 新闻爬虫模块导入失败: {e}")

try:
    from modules.news_analysis.analyzer import NewsAnalyzer
    print("✅ 智能分析模块导入成功")
except ImportError as e:
    print(f"❌ 智能分析模块导入失败: {e}")

try:
    from modules.news_crawler.config import SIMPLE_RSS_SOURCES
    print(f"✅ 配置文件导入成功，RSS源数量: {len(SIMPLE_RSS_SOURCES)}")
except ImportError as e:
    print(f"❌ 配置文件导入失败: {e}")

print("\n🎯 模块化系统导入测试完成")
