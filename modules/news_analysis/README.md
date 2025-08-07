# 智能新闻分析模块

这个模块负责基于DeepSeek AI的新闻分析和洞察生成。

## 功能特性

- DeepSeek AI集成
- 新闻事件智能分析
- 投资建议生成
- 多维度洞察报告
- HTML可视化分析

## 核心文件

- `analyzer.py`: 主要分析引擎
- `deepseek_client.py`: DeepSeek API客户端
- `report_generator.py`: 分析报告生成器
- `prompts.py`: 分析提示词模板

## 使用方法

```python
from modules.news_analysis.analyzer import NewsAnalyzer

analyzer = NewsAnalyzer()
analysis_result = analyzer.analyze_news_list(news_list)
html_report = analyzer.generate_analysis_report(analysis_result)
```

## 输出

分析报告保存在: `outputs/analysis_reports/`
