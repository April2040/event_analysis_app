# news_integration.py
"""
新闻抓取与事件分析集成模块
将热点新闻自动输入到主分析流程
"""

import json
import os
import sys
from datetime import datetime
from typing import List, Dict

# 添加父目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simple_news_crawler import SimpleNewsHotspotCrawler
from utils import call_llm, generate_html_page

class NewsAnalysisIntegration:
    """新闻分析集成器"""
    
    def __init__(self):
        self.crawler = SimpleNewsHotspotCrawler()
        self.output_dir = "reports"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def crawl_and_analyze(self, top_n: int = 10) -> Dict:
        """抓取热点新闻并进行分析"""
        print("🔄 启动自动化新闻抓取与分析流程...")
        
        # Step 1: 抓取热点新闻
        print(f"📡 正在抓取Top {top_n}热点财经新闻...")
        top_news = self.crawler.get_top_hotspots(limit=top_n)
        
        # Step 2: 格式化新闻内容用于分析
        news_content = self._format_news_for_analysis(top_news)
        
        # Step 3: 第一次AI调用 - 事件分析
        print("🤖 正在进行AI事件分析...")
        system_prompt = "你是一个专业的财经分析师，请对提供的热点新闻进行深度分析。"
        analysis_result = call_llm(news_content, system_prompt)
        
        # Step 4: 第二次AI调用 - 生成HTML报告
        print("📄 正在生成HTML分析报告...")
        html_content = generate_html_page(analysis_result)
        
        # Step 5: 保存结果
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # 保存分析结果
        analysis_file = os.path.join(self.output_dir, f"news_analysis_{timestamp}.txt")
        with open(analysis_file, 'w', encoding='utf-8') as f:
            f.write(analysis_result)
        
        # 保存HTML报告
        html_file = os.path.join(self.output_dir, f"news_report_{timestamp}.html")
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # 保存原始新闻数据
        news_file = os.path.join(self.output_dir, f"news_data_{timestamp}.json")
        news_data = {
            'timestamp': datetime.now().isoformat(),
            'analysis_method': 'automated_news_crawl',
            'news_count': len(top_news),
            'news_list': top_news
        }
        with open(news_file, 'w', encoding='utf-8') as f:
            json.dump(news_data, f, ensure_ascii=False, indent=2)
        
        result = {
            'success': True,
            'timestamp': timestamp,
            'news_count': len(top_news),
            'analysis_file': analysis_file,
            'html_file': html_file,
            'news_file': news_file,
            'analysis_preview': analysis_result[:500] + '...' if len(analysis_result) > 500 else analysis_result
        }
        
        print("✅ 自动化分析完成！")
        print(f"📊 分析报告: {html_file}")
        print(f"📝 文本结果: {analysis_file}")
        print(f"📁 新闻数据: {news_file}")
        
        return result
    
    def _format_news_for_analysis(self, news_list: List[Dict]) -> str:
        """格式化新闻内容用于AI分析"""
        content_parts = []
        content_parts.append("=== 当前热点财经新闻汇总 ===")
        content_parts.append(f"数据时间: {datetime.now().strftime('%Y年%m月%d日 %H:%M')}")
        content_parts.append(f"新闻数量: {len(news_list)}条")
        content_parts.append("")
        
        for i, news in enumerate(news_list, 1):
            content_parts.append(f"【新闻{i}】")
            content_parts.append(f"标题: {news['title']}")
            content_parts.append(f"来源: {news['source']}")
            content_parts.append(f"类别: {news['category']}")
            content_parts.append(f"热度评分: {news['heat_score']:.1f}/100")
            content_parts.append(f"关键词: {', '.join(news['keywords'])}")
            content_parts.append(f"发布时间: {news['published_time']}")
            content_parts.append("")
        
        content_parts.append("=== 分析要求 ===")
        content_parts.append("请基于以上热点财经新闻，进行深度事件分析，包括：")
        content_parts.append("1. 市场趋势分析")
        content_parts.append("2. 投资机会识别")
        content_parts.append("3. 风险点提示")
        content_parts.append("4. 政策影响评估")
        content_parts.append("5. 未来展望预测")
        
        return "\n".join(content_parts)
    
    def batch_analyze_historical_news(self, days: int = 7) -> List[Dict]:
        """批量分析历史新闻（模拟多天数据）"""
        print(f"🔄 开始批量分析最近{days}天的新闻...")
        
        results = []
        for day in range(days):
            print(f"📅 分析第{day+1}天的新闻...")
            result = self.crawl_and_analyze(top_n=5)  # 每天5条新闻
            results.append(result)
        
        print(f"✅ 批量分析完成！共生成{len(results)}份报告")
        return results
    
    def generate_trend_summary(self, results: List[Dict]) -> str:
        """生成趋势总结报告"""
        summary_content = []
        summary_content.append("📈 多日趋势分析总结")
        summary_content.append("=" * 50)
        summary_content.append(f"分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        summary_content.append(f"分析天数: {len(results)}天")
        summary_content.append("")
        
        for i, result in enumerate(results, 1):
            summary_content.append(f"第{i}天 ({result['timestamp']}):")
            summary_content.append(f"  新闻数量: {result['news_count']}条")
            summary_content.append(f"  分析预览: {result['analysis_preview']}")
            summary_content.append("")
        
        # 保存趋势总结
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        summary_file = os.path.join(self.output_dir, f"trend_summary_{timestamp}.txt")
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(summary_content))
        
        print(f"📊 趋势总结已保存: {summary_file}")
        return summary_file

def main():
    """主函数 - 演示自动化新闻分析"""
    print("🚀 启动自动化新闻分析系统")
    print("=" * 50)
    
    integration = NewsAnalysisIntegration()
    
    # 单次分析演示
    result = integration.crawl_and_analyze(top_n=10)
    
    print("\n" + "=" * 50)
    print("📋 分析结果摘要:")
    print(f"🕐 时间戳: {result['timestamp']}")
    print(f"📰 新闻数量: {result['news_count']}条")
    print(f"📄 HTML报告: {result['html_file']}")
    print(f"📝 文本分析: {result['analysis_file']}")
    print("\n预览:")
    print(result['analysis_preview'])
    
    print("\n✅ 自动化新闻分析演示完成！")
    print("💡 提示: 可以将生成的HTML文件在浏览器中打开查看完整报告")

if __name__ == "__main__":
    main()
