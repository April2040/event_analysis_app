# 热点财经新闻抓取器

基于权威财经媒体的自动化新闻抓取与热度评估系统

## 功能特性

- 🌐 多源新闻抓取：集成多个权威财经媒体
- 🔥 热度评估算法：基于多维度指标评估新闻热度
- 📊 Top10排行：自动筛选最热门的10条财经新闻
- ⏰ 实时更新：定时抓取最新财经资讯
- 📱 结构化输出：标准化的新闻数据格式

## 技术架构

- **新闻源**：彭博社、路透社、华尔街日报、金融时报等
- **抓取引擎**：基于requests + BeautifulSoup
- **热度算法**：阅读量、传播力、时效性综合评估
- **数据存储**：JSON格式结构化存储
- **API接口**：RESTful API提供数据访问

## 使用方式

```python
from news_crawler import NewsHotspotCrawler

crawler = NewsHotspotCrawler()
top_news = crawler.get_top_hotspots(limit=10)
```
