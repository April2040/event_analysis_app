# simple_news_crawler.py
"""
简化版新闻抓取器 - 可以立即运行的版本
使用模拟数据演示功能，后续可替换为真实抓取
"""

import json
import time
from datetime import datetime, timedelta
from typing import List, Dict
import random
import hashlib

class SimpleNewsHotspotCrawler:
    """简化版热点财经新闻抓取器"""
    
    def __init__(self):
        self.mock_news_pool = self._generate_mock_news()
        
    def _generate_mock_news(self) -> List[Dict]:
        """生成模拟新闻数据"""
        news_templates = [
            {
                "title": "美股三大指数集体收涨，科技股领涨纳斯达克指数上涨2.1%",
                "source": "第一财经",
                "category": "股市",
                "keywords": ["美股", "科技股", "纳斯达克"]
            },
            {
                "title": "央行决定下调存款准备金率0.5个百分点，释放流动性约1万亿元",
                "source": "新华财经", 
                "category": "货币政策",
                "keywords": ["央行", "降准", "流动性"]
            },
            {
                "title": "比特币突破6万美元关口，加密货币市场总市值创历史新高",
                "source": "财联社",
                "category": "数字货币", 
                "keywords": ["比特币", "加密货币", "新高"]
            },
            {
                "title": "新能源汽车销量同比增长156%，产业链上市公司业绩亮眼",
                "source": "证券时报",
                "category": "新能源",
                "keywords": ["新能源汽车", "销量", "产业链"]
            },
            {
                "title": "人工智能芯片龙头企业发布新一代产品，算力提升300%",
                "source": "21世纪经济报道",
                "category": "科技",
                "keywords": ["人工智能", "芯片", "算力"]
            },
            {
                "title": "房地产政策现边际宽松信号，一线城市楼市成交量回暖",
                "source": "经济观察报",
                "category": "房地产",
                "keywords": ["房地产", "政策", "楼市"]
            },
            {
                "title": "美联储主席重申渐进式加息立场，市场预期年内再加息两次",
                "source": "华尔街日报",
                "category": "货币政策",
                "keywords": ["美联储", "加息", "政策"]
            },
            {
                "title": "中美贸易数据超预期，双边贸易额创历史同期新高",
                "source": "路透社",
                "category": "贸易",
                "keywords": ["中美贸易", "贸易额", "新高"]
            },
            {
                "title": "三季度GDP同比增长4.9%，经济复苏态势持续巩固",
                "source": "人民日报",
                "category": "宏观经济",
                "keywords": ["GDP", "经济复苏", "增长"]
            },
            {
                "title": "医药板块集体爆发，创新药企业估值修复行情启动",
                "source": "每日经济新闻",
                "category": "医药",
                "keywords": ["医药", "创新药", "估值"]
            },
            {
                "title": "ESG投资理念深入人心，绿色金融产品规模突破10万亿",
                "source": "金融时报",
                "category": "绿色金融",
                "keywords": ["ESG", "绿色金融", "投资"]
            },
            {
                "title": "短视频平台广告收入暴增，数字营销产业迎来黄金期",
                "source": "财新",
                "category": "数字经济",
                "keywords": ["短视频", "广告", "数字营销"]
            }
        ]
        
        mock_news = []
        for i, template in enumerate(news_templates):
            # 生成多个变体
            for j in range(2):
                news_item = {
                    "id": f"news_{i}_{j}",
                    "title": template["title"],
                    "url": f"https://example.com/news/{i}_{j}",
                    "source": template["source"],
                    "published_time": self._random_recent_time(),
                    "summary": template["title"][:50] + "...",
                    "category": template["category"],
                    "keywords": template["keywords"],
                    "content_hash": hashlib.md5(f"{template['title']}_{j}".encode()).hexdigest(),
                    "heat_score": 0.0
                }
                mock_news.append(news_item)
        
        return mock_news
    
    def _random_recent_time(self) -> str:
        """生成随机的近期时间"""
        now = datetime.now()
        hours_ago = random.randint(1, 72)  # 1-72小时前
        random_time = now - timedelta(hours=hours_ago)
        return random_time.strftime('%Y-%m-%d %H:%M:%S')
    
    def calculate_heat_score(self, news_item: Dict) -> float:
        """计算新闻热度分数"""
        score = 0.0
        
        # 1. 时效性评分 (0-30分)
        time_score = self._calculate_time_score(news_item['published_time'])
        score += time_score
        
        # 2. 关键词权重评分 (0-25分)
        keyword_score = self._calculate_keyword_score(news_item['title'], news_item['keywords'])
        score += keyword_score
        
        # 3. 标题吸引力评分 (0-20分)
        title_score = self._calculate_title_score(news_item['title'])
        score += title_score
        
        # 4. 来源权威性评分 (0-25分)
        source_score = self._calculate_source_score(news_item['source'])
        score += source_score
        
        return min(score, 100.0)
    
    def _calculate_time_score(self, published_time: str) -> float:
        """计算时效性分数"""
        try:
            pub_time = datetime.strptime(published_time, '%Y-%m-%d %H:%M:%S')
            now = datetime.now()
            hours_diff = (now - pub_time).total_seconds() / 3600
            
            if hours_diff <= 2:
                return 30.0
            elif hours_diff <= 6:
                return 25.0
            elif hours_diff <= 12:
                return 20.0
            elif hours_diff <= 24:
                return 15.0
            elif hours_diff <= 48:
                return 10.0
            else:
                return 5.0
        except (ValueError, TypeError):
            return 10.0
    
    def _calculate_keyword_score(self, title: str, keywords: List[str]) -> float:
        """计算关键词权重分数"""
        high_impact_words = {
            '暴涨': 5, '暴跌': 5, '突破': 4, '创新高': 4, '涨停': 4, '跌停': 4,
            '央行': 4, '美联储': 4, '降准': 4, '加息': 4, '降息': 4,
            'GDP': 3, 'CPI': 3, '比特币': 3, '人工智能': 3, '新能源': 3,
            '政策': 2, '增长': 2, '投资': 2, '市场': 2
        }
        
        score = 0.0
        text = title + ' ' + ' '.join(keywords)
        
        for word, weight in high_impact_words.items():
            if word in text:
                score += weight
        
        return min(score, 25.0)
    
    def _calculate_title_score(self, title: str) -> float:
        """计算标题吸引力分数"""
        score = 0.0
        
        # 数字和百分比
        import re
        if re.search(r'\d+%', title):
            score += 5
        if re.search(r'[0-9]+', title):
            score += 2
        
        # 情感词汇
        emotional_words = ['突破', '暴涨', '暴跌', '创新高', '爆发', '崩盘', '飙升']
        for word in emotional_words:
            if word in title:
                score += 4
                break
        
        # 紧急性词汇
        urgent_words = ['重磅', '突发', '最新', '独家', '首次']
        for word in urgent_words:
            if word in title:
                score += 3
                break
        
        return min(score, 20.0)
    
    def _calculate_source_score(self, source: str) -> float:
        """计算来源权威性分数"""
        authority_scores = {
            '彭博社': 25, '路透社': 25, '华尔街日报': 25, '金融时报': 24,
            '第一财经': 23, '财新': 23, '财联社': 22, '新华财经': 22,
            '证券时报': 20, '21世纪经济报道': 19, '经济观察报': 18,
            '每日经济新闻': 20, '人民日报': 21
        }
        
        return authority_scores.get(source, 15.0)
    
    def get_top_hotspots(self, limit: int = 10) -> List[Dict]:
        """获取Top热点新闻"""
        print("🔄 正在模拟抓取热点财经新闻...")
        
        # 模拟网络延迟
        time.sleep(1)
        
        # 随机选择一部分新闻作为"抓取"结果
        selected_news = random.sample(self.mock_news_pool, min(len(self.mock_news_pool), 20))
        
        # 计算热度分数
        for news in selected_news:
            news['heat_score'] = self.calculate_heat_score(news)
        
        # 按热度排序
        selected_news.sort(key=lambda x: x['heat_score'], reverse=True)
        
        # 返回Top N
        top_news = selected_news[:limit]
        
        print(f"✅ 成功获取Top {len(top_news)} 热点新闻")
        return top_news
    
    def save_to_file(self, news_list: List[Dict], filename: str = None) -> str:
        """保存新闻到文件"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"news_data/hotspot_news_{timestamp}.json"
        
        # 确保目录存在
        import os
        os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)
        
        data = {
            'timestamp': datetime.now().isoformat(),
            'total_count': len(news_list),
            'crawl_method': 'mock_simulation',
            'news_list': news_list
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"📁 新闻数据已保存到: {filename}")
        return filename
    
    def generate_summary_report(self, news_list: List[Dict]) -> str:
        """生成热点新闻摘要报告"""
        report = []
        report.append("📊 热点财经新闻摘要报告")
        report.append("=" * 40)
        report.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"新闻总数: {len(news_list)}")
        report.append("")
        
        # 按类别统计
        categories = {}
        for news in news_list:
            cat = news['category']
            categories[cat] = categories.get(cat, 0) + 1
        
        report.append("📈 热点类别分布:")
        for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            report.append(f"  {cat}: {count}条")
        report.append("")
        
        # 热度分布
        high_heat = len([n for n in news_list if n['heat_score'] >= 70])
        medium_heat = len([n for n in news_list if 50 <= n['heat_score'] < 70])
        low_heat = len([n for n in news_list if n['heat_score'] < 50])
        
        report.append("🔥 热度分布:")
        report.append(f"  高热度(≥70分): {high_heat}条")
        report.append(f"  中热度(50-69分): {medium_heat}条")
        report.append(f"  低热度(<50分): {low_heat}条")
        report.append("")
        
        # Top 5 新闻标题
        report.append("🏆 Top 5 热点新闻:")
        for i, news in enumerate(news_list[:5], 1):
            report.append(f"{i}. [{news['source']}] {news['title']}")
            report.append(f"   热度: {news['heat_score']:.1f}分 | 类别: {news['category']}")
        
        return "\n".join(report)

def main():
    """主函数 - 演示使用"""
    print("🚀 启动简化版热点财经新闻抓取器")
    print("=" * 50)
    
    crawler = SimpleNewsHotspotCrawler()
    
    # 获取Top10热点新闻
    top_news = crawler.get_top_hotspots(limit=10)
    
    # 生成摘要报告
    summary = crawler.generate_summary_report(top_news)
    print(summary)
    print()
    
    # 详细新闻列表
    print("📰 详细新闻列表:")
    print("-" * 40)
    for i, news in enumerate(top_news, 1):
        print(f"{i}. 【{news['source']}】{news['title']}")
        print(f"   热度: {news['heat_score']:.1f}分 | 类别: {news['category']}")
        print(f"   关键词: {', '.join(news['keywords'])}")
        print(f"   发布: {news['published_time']}")
        print(f"   链接: {news['url']}")
        print()
    
    # 保存到文件
    filename = crawler.save_to_file(top_news)
    
    print("✅ 新闻抓取演示完成！")
    print(f"📄 完整数据已保存到: {filename}")

if __name__ == "__main__":
    main()
