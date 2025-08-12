# news_crawler.py
import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime, timedelta
import re
from typing import List, Dict, Optional
from dataclasses import dataclass
import hashlib
from urllib.parse import urljoin, urlparse
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class NewsItem:
    """新闻项数据结构"""
    title: str
    url: str
    source: str
    published_time: str
    summary: str
    heat_score: float
    category: str
    keywords: List[str]
    content_hash: str

class NewsSource:
    """新闻源配置"""
    def __init__(self, name: str, url: str, selectors: Dict[str, str], encoding: str = 'utf-8'):
        self.name = name
        self.url = url
        self.selectors = selectors
        self.encoding = encoding

class HeatCalculator:
    """热度计算器"""
    
    @staticmethod
    def calculate_heat_score(news_item: Dict) -> float:
        """
        计算新闻热度分数
        考虑因素：时效性、关键词权重、标题吸引力、来源权威性
        """
        score = 0.0
        
        # 1. 时效性评分 (0-30分)
        time_score = HeatCalculator._calculate_time_score(news_item.get('published_time', ''))
        score += time_score
        
        # 2. 关键词权重评分 (0-25分)
        keyword_score = HeatCalculator._calculate_keyword_score(news_item.get('title', '') + ' ' + news_item.get('summary', ''))
        score += keyword_score
        
        # 3. 标题吸引力评分 (0-20分)
        title_score = HeatCalculator._calculate_title_score(news_item.get('title', ''))
        score += title_score
        
        # 4. 来源权威性评分 (0-25分)
        source_score = HeatCalculator._calculate_source_score(news_item.get('source', ''))
        score += source_score
        
        return min(score, 100.0)  # 最高100分
    
    @staticmethod
    def _calculate_time_score(published_time: str) -> float:
        """计算时效性分数"""
        try:
            if not published_time:
                return 10.0
            
            # 假设时间格式已标准化
            now = datetime.now()
            # 这里需要根据实际时间格式进行解析
            # 简化处理：越新的新闻分数越高
            return 25.0  # 暂时给固定分数
        except:
            return 10.0
    
    @staticmethod
    def _calculate_keyword_score(text: str) -> float:
        """计算关键词权重分数"""
        # 财经热词列表
        hot_keywords = {
            '股市': 3, '涨停': 4, '跌停': 4, '牛市': 3, '熊市': 3,
            '央行': 4, '降息': 4, '加息': 4, '货币政策': 3, 'GDP': 3,
            '通胀': 3, 'CPI': 2, 'PPI': 2, '失业率': 2,
            '美联储': 4, '欧央行': 3, '人民银行': 3,
            '比特币': 3, '加密货币': 2, '区块链': 2,
            '新能源': 3, '芯片': 3, '人工智能': 3, 'AI': 3,
            '房地产': 3, '地产': 2, '楼市': 3,
            '贸易战': 4, '制裁': 3, '关税': 2,
            'IPO': 3, '并购': 2, '重组': 2, '退市': 3,
            '财报': 2, '业绩': 2, '营收': 2, '利润': 2
        }
        
        score = 0.0
        text_lower = text.lower()
        
        for keyword, weight in hot_keywords.items():
            if keyword in text:
                score += weight
        
        return min(score, 25.0)
    
    @staticmethod
    def _calculate_title_score(title: str) -> float:
        """计算标题吸引力分数"""
        score = 0.0
        
        # 数字和百分比
        if re.search(r'\d+%', title):
            score += 5
        if re.search(r'[0-9]+', title):
            score += 2
            
        # 情感词汇
        positive_words = ['突破', '大涨', '飙升', '创新高', '利好', '增长']
        negative_words = ['暴跌', '崩盘', '危机', '下跌', '亏损', '风险']
        
        for word in positive_words + negative_words:
            if word in title:
                score += 3
                break
        
        # 紧急性词汇
        urgent_words = ['紧急', '突发', '重磅', '独家', '最新']
        for word in urgent_words:
            if word in title:
                score += 4
                break
        
        return min(score, 20.0)
    
    @staticmethod
    def _calculate_source_score(source: str) -> float:
        """计算来源权威性分数"""
        authority_scores = {
            '彭博社': 25, 'Bloomberg': 25,
            '路透社': 25, 'Reuters': 25,
            '华尔街日报': 25, 'Wall Street Journal': 25,
            '金融时报': 24, 'Financial Times': 24,
            '第一财经': 23, '财新': 23, '财联社': 22,
            '新华财经': 22, '中新经纬': 21,
            '每日经济新闻': 20, '证券时报': 20,
            '21世纪经济报道': 19, '经济观察报': 18,
            'CNBC': 22, 'MarketWatch': 20,
            '雅虎财经': 18, 'Yahoo Finance': 18
        }
        
        for source_name, score in authority_scores.items():
            if source_name in source:
                return score
        
        return 15.0  # 默认分数

class NewsHotspotCrawler:
    """热点财经新闻抓取器"""
    
    def __init__(self):
        self.news_sources = self._init_news_sources()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def _init_news_sources(self) -> List[NewsSource]:
        """初始化新闻源配置"""
        sources = [
            # 示例配置 - 实际使用时需要根据具体网站调整
            NewsSource(
                name="第一财经",
                url="https://www.yicai.com/",
                selectors={
                    'title': '.title, h1, h2',
                    'link': 'a[href]',
                    'time': '.time, .date',
                    'summary': '.summary, .desc'
                }
            ),
            NewsSource(
                name="财新网",
                url="https://www.caixin.com/",
                selectors={
                    'title': '.title, h1, h2',
                    'link': 'a[href]',
                    'time': '.time, .date',
                    'summary': '.summary, .desc'
                }
            ),
            NewsSource(
                name="财联社",
                url="https://www.cls.cn/",
                selectors={
                    'title': '.title, h1, h2',
                    'link': 'a[href]',
                    'time': '.time, .date',
                    'summary': '.summary, .desc'
                }
            )
        ]
        return sources
    
    def crawl_news_from_source(self, source: NewsSource, max_items: int = 20) -> List[Dict]:
        """从单个新闻源抓取新闻"""
        try:
            logger.info(f"正在抓取 {source.name} 的新闻...")
            
            response = self.session.get(source.url, timeout=10)
            response.encoding = source.encoding
            soup = BeautifulSoup(response.text, 'html.parser')
            
            news_items = []
            
            # 查找新闻标题链接
            title_elements = soup.select(source.selectors['title'])[:max_items]
            
            for element in title_elements:
                try:
                    # 提取标题
                    title = element.get_text(strip=True)
                    if len(title) < 10:  # 过滤太短的标题
                        continue
                    
                    # 提取链接
                    link_element = element.find('a') or element.find_parent('a')
                    if not link_element:
                        continue
                    
                    url = link_element.get('href', '')
                    if url.startswith('/'):
                        url = urljoin(source.url, url)
                    
                    # 生成内容哈希
                    content_hash = hashlib.md5((title + url).encode()).hexdigest()
                    
                    news_item = {
                        'title': title,
                        'url': url,
                        'source': source.name,
                        'published_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'summary': title[:100] + '...' if len(title) > 100 else title,
                        'category': '财经',
                        'keywords': self._extract_keywords(title),
                        'content_hash': content_hash
                    }
                    
                    news_items.append(news_item)
                    
                except Exception as e:
                    logger.warning(f"处理新闻项时出错: {e}")
                    continue
            
            logger.info(f"从 {source.name} 抓取到 {len(news_items)} 条新闻")
            return news_items
            
        except Exception as e:
            logger.error(f"抓取 {source.name} 时出错: {e}")
            return []
    
    def _extract_keywords(self, text: str) -> List[str]:
        """提取关键词"""
        keywords = []
        
        # 简单的关键词提取
        financial_terms = [
            '股市', '股票', '基金', '债券', '期货', '外汇',
            '银行', '保险', '证券', '投资', '理财',
            '经济', '金融', '财政', '货币', '央行',
            '上市', 'IPO', '并购', '重组', '退市',
            '涨停', '跌停', '牛市', '熊市'
        ]
        
        for term in financial_terms:
            if term in text:
                keywords.append(term)
        
        return keywords[:5]  # 最多返回5个关键词
    
    def get_all_news(self, max_per_source: int = 20) -> List[Dict]:
        """从所有新闻源抓取新闻"""
        all_news = []
        
        for source in self.news_sources:
            news_items = self.crawl_news_from_source(source, max_per_source)
            all_news.extend(news_items)
            time.sleep(1)  # 避免过于频繁的请求
        
        return all_news
    
    def calculate_heat_scores(self, news_list: List[Dict]) -> List[Dict]:
        """计算所有新闻的热度分数"""
        for news in news_list:
            news['heat_score'] = HeatCalculator.calculate_heat_score(news)
        return news_list
    
    def get_top_hotspots(self, limit: int = 10) -> List[Dict]:
        """获取Top热点新闻"""
        logger.info("开始抓取热点财经新闻...")
        
        # 1. 抓取所有新闻
        all_news = self.get_all_news()
        
        # 2. 去重（基于内容哈希）
        unique_news = {}
        for news in all_news:
            hash_key = news['content_hash']
            if hash_key not in unique_news:
                unique_news[hash_key] = news
        
        news_list = list(unique_news.values())
        logger.info(f"去重后共 {len(news_list)} 条新闻")
        
        # 3. 计算热度分数
        news_list = self.calculate_heat_scores(news_list)
        
        # 4. 按热度排序
        news_list.sort(key=lambda x: x['heat_score'], reverse=True)
        
        # 5. 返回Top N
        top_news = news_list[:limit]
        
        logger.info(f"筛选出Top {len(top_news)} 热点新闻")
        
        return top_news
    
    def save_to_file(self, news_list: List[Dict], filename: str = None):
        """保存新闻到文件"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"hotspot_news_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'total_count': len(news_list),
                'news_list': news_list
            }, f, ensure_ascii=False, indent=2)
        
        logger.info(f"新闻数据已保存到 {filename}")
        return filename

def main():
    """主函数 - 示例用法"""
    crawler = NewsHotspotCrawler()
    
    # 获取Top10热点新闻
    top_news = crawler.get_top_hotspots(limit=10)
    
    # 打印结果
    print("🔥 Top 10 热点财经新闻")
    print("=" * 50)
    
    for i, news in enumerate(top_news, 1):
        print(f"{i}. 【{news['source']}】{news['title']}")
        print(f"   热度: {news['heat_score']:.1f} | 关键词: {', '.join(news['keywords'])}")
        print(f"   链接: {news['url']}")
        print()
    
    # 保存到文件
    filename = crawler.save_to_file(top_news)
    print(f"📁 数据已保存到: {filename}")

if __name__ == "__main__":
    main()
