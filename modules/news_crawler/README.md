# 新闻爬虫模块

这个模块负责财经新闻的抓取、处理和HTML报告生成。

## 功能特性

- RSS源新闻抓取
- 智能热度评分算法
- HTML可视化报告生成  
- 多源备用机制
- 交互式用户界面

## 核心文件

- `crawler.py`: 优化的RSS新闻爬虫
- `config.py`: RSS源和评分配置
- `html_generator.py`: HTML报告生成器
- `utils.py`: 工具函数

## 使用方法

```python
from modules.news_crawler.crawler import NewsWebCrawler

crawler = NewsWebCrawler()
news_list = crawler.get_top_hotspots(limit=10)
html_path = crawler.generate_html_report(news_list)
```

## 输出

HTML报告保存在: `outputs/news_reports/`
