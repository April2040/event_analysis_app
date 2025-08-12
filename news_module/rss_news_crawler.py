# rss_news_crawler.py
"""
RSS新闻抓取器 - 通过RSS源抓取新闻
更稳定可靠的新闻获取方式
"""

import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import re
from typing import List, Dict
import hashlib
import time
import logging

# 导入配置
from config import FINANCIAL_KEYWORDS, SOURCE_AUTHORITY, HEAT_WEIGHTS

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RSSNewsHotspotCrawler:
    """基于RSS的新闻抓取器"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        
        import requests
import json
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any
import time
import sys
import os

# 导入配置文件
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from rss_sources_config import (
    PRIMARY_RSS_SOURCES, 
    BACKUP_RSS_SOURCES, 
    INTERNATIONAL_RSS_SOURCES,
    SIMPLE_RSS_SOURCES,
    ENHANCED_BACKUP_NEWS,
    RSS_SOURCE_WEIGHTS
)
        
        # 备用测试新闻（如果RSS不可用）
        self.backup_news = [
            {
                "title": "央行宣布降准0.5个百分点，释放长期资金约1万亿元",
                "source": "人民银行",
                "category": "货币政策",
                "keywords": ["央行", "降准", "流动性"],
                "summary": "中国人民银行决定于2025年8月15日降准0.5个百分点，此次降准将释放长期资金约1万亿元。"
            },
            {
                "title": "A股三大指数集体收涨，创业板指涨超2%，新能源板块领涨",
                "source": "上海证券报",
                "category": "股市",
                "keywords": ["A股", "创业板", "新能源"],
                "summary": "今日A股市场表现强劲，三大指数全线上涨，创业板指数涨幅超过2%。"
            },
            {
                "title": "美联储会议纪要显示对通胀担忧加剧，加息预期升温",
                "source": "华尔街日报",
                "category": "货币政策", 
                "keywords": ["美联储", "通胀", "加息"],
                "summary": "美联储最新会议纪要显示，多数委员对通胀持续高位表示担忧。"
            },
            {
                "title": "比特币突破4.3万美元，加密货币市场重现活力",
                "source": "Coindesk",
                "category": "数字货币",
                "keywords": ["比特币", "加密货币", "突破"],
                "summary": "比特币价格突破4.3万美元关口，带动整个加密货币市场上涨。"
            },
            {
                "title": "特斯拉Q3财报超预期，新能源汽车销量创历史新高",
                "source": "财联社",
                "category": "新能源",
                "keywords": ["特斯拉", "财报", "新能源汽车"],
                "summary": "特斯拉第三季度财报显示，营收和净利润均超出市场预期。"
            },
            {
                "title": "人工智能芯片需求激增，英伟达股价再创新高",
                "source": "彭博社",
                "category": "科技",
                "keywords": ["人工智能", "芯片", "英伟达"],
                "summary": "AI芯片需求持续旺盛，推动英伟达股价连续上涨。"
            },
            {
                "title": "房地产政策现边际宽松迹象，多城市放松限购政策",
                "source": "中国证券报",
                "category": "房地产",
                "keywords": ["房地产", "政策", "限购"],
                "summary": "近期多个城市陆续调整房地产调控政策，市场预期政策将进一步宽松。"
            },
            {
                "title": "原油价格大幅波动，地缘政治风险推高能源价格",
                "source": "路透社",
                "category": "能源",
                "keywords": ["原油", "地缘政治", "能源"],
                "summary": "受地缘政治因素影响，国际原油价格出现大幅波动。"
            },
            {
                "title": "银行板块估值修复行情启动，资金回流金融股",
                "source": "证券时报",
                "category": "金融",
                "keywords": ["银行", "估值", "金融股"],
                "summary": "随着经济预期改善，银行板块估值修复行情正在启动。"
            },
            {
                "title": "消费板块逐步复苏，白酒食品股表现亮眼",
                "source": "第一财经",
                "category": "消费",
                "keywords": ["消费", "白酒", "食品"],
                "summary": "消费复苏迹象明显，白酒、食品等消费股表现突出。"
            }
        ]
    
    def get_news_from_rss(self, url: str, source_name: str) -> List[Dict]:
        """从RSS源获取新闻"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            # 解析XML
            root = ET.fromstring(response.content)
            
            news_items = []
            # 查找所有新闻项
            items = root.findall('.//item')
            
            for i, item in enumerate(items[:20]):  # 最多20条
                try:
                    title_elem = item.find('title')
                    link_elem = item.find('link')
                    desc_elem = item.find('description')
                    date_elem = item.find('pubDate')
                    
                    if title_elem is not None:
                        title = title_elem.text or ""
                        link = link_elem.text if link_elem is not None else ""
                        description = desc_elem.text if desc_elem is not None else ""
                        pub_date = date_elem.text if date_elem is not None else ""
                        
                        # 过滤财经相关新闻
                        if self._is_financial_news(title + " " + description):
                            news_item = self._create_news_item(title, link, source_name, description, pub_date, i)
                            news_items.append(news_item)
                
                except Exception as e:
                    logger.warning(f"解析RSS项目失败: {str(e)}")
                    continue
            
            logger.info(f"从 {source_name} RSS 获取 {len(news_items)} 条财经新闻")
            return news_items
            
        except Exception as e:
            logger.error(f"RSS抓取失败 {source_name}: {str(e)}")
            return []
    
    def _is_financial_news(self, text: str) -> bool:
        """判断是否为财经新闻"""
        financial_words = [
            '股市', '股票', '基金', '银行', '保险', '证券', '投资', '理财',
            '经济', '金融', '财政', '货币', '央行', '利率', '通胀', 'GDP',
            '房地产', '楼市', '房价', '新能源', '科技股', '芯片',
            '比特币', '数字货币', '区块链', '原油', '黄金', '外汇'
        ]
        
        return any(word in text for word in financial_words)
    
    def _create_news_item(self, title: str, link: str, source: str, description: str, pub_date: str, index: int) -> Dict:
        """创建新闻项"""
        # 解析发布时间
        published_time = self._parse_rss_time(pub_date)
        
        # 分类新闻
        category = self._classify_news(title + " " + description)
        
        # 提取关键词
        keywords = self._extract_keywords(title + " " + description)
        
        # 生成ID和哈希
        news_id = f"{source}_{index}_{int(time.time())}"
        content_hash = hashlib.md5(f"{title}_{link}".encode()).hexdigest()
        
        return {
            'id': news_id,
            'title': title.strip(),
            'url': link.strip(),
            'source': source,
            'published_time': published_time,
            'summary': description.strip()[:200] + "..." if len(description) > 200 else description.strip(),
            'category': category,
            'keywords': keywords,
            'content_hash': content_hash,
            'heat_score': 0.0
        }
    
    def _parse_rss_time(self, time_str: str) -> str:
        """解析RSS时间格式"""
        if not time_str:
            return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 尝试解析常见的RSS时间格式
        try:
            # RFC 2822 format: Wed, 02 Oct 2002 08:00:00 EST
            time_obj = datetime.strptime(time_str[:25], '%a, %d %b %Y %H:%M:%S')
            return time_obj.strftime('%Y-%m-%d %H:%M:%S')
        except:
            try:
                # ISO format
                time_obj = datetime.fromisoformat(time_str.replace('Z', '+00:00'))
                return time_obj.strftime('%Y-%m-%d %H:%M:%S')
            except:
                # 默认当前时间
                return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def _classify_news(self, text: str) -> str:
        """新闻分类"""
        categories = {
            '货币政策': ['央行', '货币政策', '降息', '加息', '降准', '美联储', '利率', '通胀'],
            '股市': ['股市', '股票', '上证', '深证', '创业板', '科创板', '涨停', '跌停', 'A股'],
            '数字货币': ['比特币', '数字货币', '区块链', '加密货币', '以太坊'],
            '房地产': ['房地产', '地产', '楼市', '房价', '住房', '限购'],
            '新能源': ['新能源', '电动车', '光伏', '风电', '锂电池', '特斯拉'],
            '科技': ['人工智能', 'AI', '芯片', '半导体', '5G', '云计算', '英伟达'],
            '金融': ['银行', '保险', '券商', '基金', '信托'],
            '能源': ['石油', '天然气', '煤炭', '原油', '能源'],
            '消费': ['消费', '零售', '白酒', '食品', '餐饮'],
        }
        
        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword in text:
                    return category
        
        return '财经'
    
    def _extract_keywords(self, text: str) -> List[str]:
        """提取关键词"""
        keywords = []
        
        # 从配置的关键词中提取
        for keyword_groups in FINANCIAL_KEYWORDS.values():
            for group_keywords in keyword_groups.values():
                for keyword in group_keywords:
                    if keyword in text and keyword not in keywords:
                        keywords.append(keyword)
        
        # 补充一些常见财经词汇
        common_words = ['股市', '投资', '经济', '金融', '市场', '政策', '增长', '下跌', '上涨']
        for word in common_words:
            if word in text and word not in keywords:
                keywords.append(word)
        
        return keywords[:5]  # 最多5个关键词
    
    def calculate_heat_score(self, news_item: Dict) -> float:
        """计算新闻热度分数"""
        score = 0.0
        
        # 1. 时效性评分
        time_score = self._calculate_time_score(news_item['published_time'])
        score += time_score * 30
        
        # 2. 关键词权重评分
        keyword_score = self._calculate_keyword_score(news_item['title'], news_item['keywords'])
        score += keyword_score * 25
        
        # 3. 标题吸引力评分
        title_score = self._calculate_title_score(news_item['title'])
        score += title_score * 20
        
        # 4. 来源权威性评分
        source_score = self._calculate_source_score(news_item['source'])
        score += source_score * 25
        
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
        except:
            return 15.0
    
    def _calculate_keyword_score(self, title: str, keywords: List[str]) -> float:
        """计算关键词权重分数"""
        high_impact_words = ['暴涨', '暴跌', '突破', '创新高', '央行', '美联储', '降准', '加息', 'GDP', '比特币']
        
        score = 0.0
        text = title + ' ' + ' '.join(keywords)
        
        for word in high_impact_words:
            if word in text:
                score += 3
        
        return min(score, 25.0)
    
    def _calculate_title_score(self, title: str) -> float:
        """计算标题吸引力分数"""
        score = 0.0
        
        # 数字和百分比
        if re.search(r'\d+%', title):
            score += 8
        if re.search(r'[0-9]+', title):
            score += 5
        
        # 情感词汇
        emotional_words = ['突破', '暴涨', '暴跌', '创新高', '爆发', '重磅', '突发']
        for word in emotional_words:
            if word in title:
                score += 7
                break
        
        return min(score, 20.0)
    
    def _calculate_source_score(self, source: str) -> float:
        """计算来源权威性分数"""
        return SOURCE_AUTHORITY.get(source, 15.0)
    
    def get_top_hotspots(self, limit: int = 10, use_backup: bool = True) -> List[Dict]:
        """获取Top热点新闻"""
        print("📡 启动RSS新闻抓取...")
        
        all_news = []
        
        # 尝试从RSS获取新闻
        for source_name, rss_url in self.rss_sources.items():
            try:
                news_items = self.get_news_from_rss(rss_url, source_name)
                all_news.extend(news_items)
                if len(news_items) > 0:
                    break  # 只要有一个源成功就够了
            except Exception as e:
                logger.error(f"RSS源 {source_name} 失败: {str(e)}")
                continue
        
        # 如果RSS失败，使用备用新闻
        if len(all_news) == 0 and use_backup:
            print("🔄 RSS抓取失败，使用备用新闻数据...")
            for i, backup in enumerate(self.backup_news):
                news_item = {
                    'id': f"backup_{i}",
                    'title': backup['title'],
                    'url': f"https://example.com/news/{i}",
                    'source': backup['source'],
                    'published_time': (datetime.now() - timedelta(hours=i)).strftime('%Y-%m-%d %H:%M:%S'),
                    'summary': backup['summary'],
                    'category': backup['category'],
                    'keywords': backup['keywords'],
                    'content_hash': hashlib.md5(f"{backup['title']}_{i}".encode()).hexdigest(),
                    'heat_score': 0.0
                }
                all_news.append(news_item)
        
        print(f"📊 总共获取 {len(all_news)} 条新闻")
        
        # 计算热度分数
        for news in all_news:
            news['heat_score'] = self.calculate_heat_score(news)
        
        # 按热度排序
        all_news.sort(key=lambda x: x['heat_score'], reverse=True)
        
        # 返回Top N
        top_news = all_news[:limit]
        
        print(f"✅ 成功获取Top {len(top_news)} 热点新闻")
        return top_news

def main():
    """测试RSS新闻抓取"""
    crawler = RSSNewsHotspotCrawler()
    
    top_news = crawler.get_top_hotspots(limit=10)
    
    # 显示结果
    print("\n🏆 RSS热点新闻榜单:")
    print("=" * 60)
    for i, news in enumerate(top_news, 1):
        print(f"{i}. [{news['source']}] {news['title']}")
        print(f"   热度: {news['heat_score']:.1f}分 | 类别: {news['category']}")
        print(f"   关键词: {', '.join(news['keywords'])}")
        print(f"   时间: {news['published_time']}")
        print()

if __name__ == "__main__":
    main()
