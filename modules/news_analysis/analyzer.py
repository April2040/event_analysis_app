"""
智能新闻分析模块 - 主分析引擎
集成DeepSeek AI进行新闻事件分析
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any

from .deepseek_client import DeepSeekClient
from .report_generator import AnalysisReportGenerator
from .prompts import get_analysis_prompt, get_summary_prompt

class NewsAnalyzer:
    """新闻智能分析器"""
    
    def __init__(self, api_key: str = None):
        """初始化分析器"""
        self.deepseek_client = DeepSeekClient(api_key)
        self.report_generator = AnalysisReportGenerator()
    
    def analyze_news_list(self, news_list: List[Dict]) -> Dict[str, Any]:
        """分析新闻列表"""
        print("🧠 开始智能新闻分析...")
        
        if not news_list:
            print("❌ 新闻列表为空，无法进行分析")
            return {}
        
        # 准备分析数据
        analysis_data = self._prepare_analysis_data(news_list)
        
        # 分析各个新闻事件
        individual_analyses = []
        for i, news in enumerate(news_list[:5], 1):  # 分析前5条热点新闻
            print(f"  分析第{i}条新闻: {news.get('title', '')[:30]}...")
            analysis = self._analyze_single_news(news)
            if analysis:
                individual_analyses.append(analysis)
        
        # 生成整体总结和洞察
        print("  生成整体分析和投资洞察...")
        overall_analysis = self._generate_overall_analysis(news_list, individual_analyses)
        
        # 构建完整分析结果
        result = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_news": len(news_list),
            "analyzed_news": len(individual_analyses),
            "news_summary": self._generate_news_summary(news_list),
            "individual_analyses": individual_analyses,
            "overall_analysis": overall_analysis,
            "investment_insights": self._extract_investment_insights(overall_analysis),
            "risk_assessment": self._assess_market_risks(news_list),
            "categories_distribution": self._get_categories_distribution(news_list)
        }
        
        print(f"✅ 分析完成，共分析 {len(individual_analyses)} 条新闻")
        return result
    
    def generate_analysis_report(self, analysis_result: Dict[str, Any]) -> str:
        """生成分析报告HTML"""
        if not analysis_result:
            print("❌ 分析结果为空，无法生成报告")
            return ""
        
        print("📊 生成分析报告...")
        
        # 确保输出目录存在
        output_dir = "outputs/analysis_reports"
        os.makedirs(output_dir, exist_ok=True)
        
        # 生成HTML报告
        html_content = self.report_generator.generate_html(analysis_result)
        
        # 保存文件
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        html_file = os.path.join(output_dir, f"analysis_report_{timestamp}.html")
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # 同时保存JSON数据
        json_file = os.path.join(output_dir, f"analysis_data_{timestamp}.json")
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(analysis_result, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 分析报告已生成: {html_file}")
        return html_file
    
    def _prepare_analysis_data(self, news_list: List[Dict]) -> Dict:
        """准备分析数据"""
        return {
            "news_count": len(news_list),
            "categories": list(set(news.get('category', '综合') for news in news_list)),
            "sources": list(set(news.get('source', '未知') for news in news_list)),
            "time_range": {
                "start": min(news.get('published', '') for news in news_list if news.get('published')),
                "end": max(news.get('published', '') for news in news_list if news.get('published'))
            }
        }
    
    def _analyze_single_news(self, news: Dict) -> Dict:
        """分析单条新闻"""
        try:
            prompt = get_analysis_prompt(news)
            response = self.deepseek_client.get_completion(prompt)
            
            if response:
                return {
                    "news_title": news.get('title', ''),
                    "news_source": news.get('source', ''),
                    "news_category": news.get('category', ''),
                    "heat_score": news.get('heat_score', 0),
                    "analysis": response,
                    "keywords": news.get('keywords', []),
                    "published": news.get('published', '')
                }
        except Exception as e:
            print(f"    ⚠️ 分析失败: {e}")
        
        return None
    
    def _generate_overall_analysis(self, news_list: List[Dict], individual_analyses: List[Dict]) -> str:
        """生成整体分析"""
        try:
            # 构建整体分析提示词
            news_summary = "\n".join([
                f"- {news.get('title', '')[:100]} (来源: {news.get('source', '')}, 热度: {news.get('heat_score', 0)})"
                for news in news_list[:10]
            ])
            
            prompt = f"""
基于以下财经新闻热点，请进行整体市场分析和投资洞察：

新闻摘要：
{news_summary}

请从以下角度进行分析：
1. 市场整体趋势判断
2. 主要投资机会识别
3. 潜在风险提示
4. 行业轮动特征
5. 政策影响分析
6. 投资策略建议

请提供深度、专业的分析，字数控制在800字左右。
"""
            
            response = self.deepseek_client.get_completion(prompt)
            return response if response else "整体分析生成失败"
            
        except Exception as e:
            print(f"    ⚠️ 整体分析失败: {e}")
            return "整体分析暂时无法生成"
    
    def _generate_news_summary(self, news_list: List[Dict]) -> str:
        """生成新闻摘要"""
        if not news_list:
            return "暂无新闻"
        
        top_categories = self._get_top_categories(news_list, 3)
        category_text = "、".join(top_categories)
        
        return f"今日共获取{len(news_list)}条财经热点新闻，主要集中在{category_text}等领域，平均热度{self._get_average_heat_score(news_list):.2f}。"
    
    def _extract_investment_insights(self, overall_analysis: str) -> List[str]:
        """提取投资洞察要点"""
        # 简单的关键词提取，实际项目中可以使用更复杂的NLP技术
        insights = []
        
        if "投资机会" in overall_analysis:
            insights.append("发现潜在投资机会")
        if "风险" in overall_analysis:
            insights.append("需要关注市场风险")
        if "政策" in overall_analysis:
            insights.append("政策变化值得关注")
        if "趋势" in overall_analysis:
            insights.append("市场趋势明确")
        
        return insights if insights else ["需要进一步分析"]
    
    def _assess_market_risks(self, news_list: List[Dict]) -> str:
        """评估市场风险"""
        risk_keywords = ["风险", "下跌", "担忧", "危机", "冲突", "制裁"]
        positive_keywords = ["上涨", "利好", "增长", "突破", "复苏"]
        
        risk_count = 0
        positive_count = 0
        
        for news in news_list:
            title = news.get('title', '').lower()
            for keyword in risk_keywords:
                if keyword in title:
                    risk_count += 1
                    break
            for keyword in positive_keywords:
                if keyword in title:
                    positive_count += 1
                    break
        
        if risk_count > positive_count:
            return "偏谨慎"
        elif positive_count > risk_count:
            return "偏乐观"
        else:
            return "中性"
    
    def _get_categories_distribution(self, news_list: List[Dict]) -> Dict[str, int]:
        """获取分类分布"""
        categories = {}
        for news in news_list:
            category = news.get('category', '综合')
            categories[category] = categories.get(category, 0) + 1
        
        return dict(sorted(categories.items(), key=lambda x: x[1], reverse=True))
    
    def _get_top_categories(self, news_list: List[Dict], limit: int = 3) -> List[str]:
        """获取热门分类"""
        distribution = self._get_categories_distribution(news_list)
        return list(distribution.keys())[:limit]
    
    def _get_average_heat_score(self, news_list: List[Dict]) -> float:
        """获取平均热度分数"""
        if not news_list:
            return 0.0
        
        total_score = sum(news.get('heat_score', 0) for news in news_list)
        return total_score / len(news_list)
