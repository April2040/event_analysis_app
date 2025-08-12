# real_news_crawler.py
"""
真实新闻抓取器 - 从真实新闻网站抓取数据
基于config.py配置，实现多源新闻聚合
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import hashlib
from urllib.parse import urljoin, urlparse
import logging

# 导入配置
from config import NEWS_SOURCES, HEAT_WEIGHTS, FINANCIAL_KEYWORDS, SOURCE_AUTHORITY, CRAWLER_CONFIG

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RealNewsHotspotCrawler:
    """真实热点财经新闻抓取器"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': CRAWLER_CONFIG['user_agent']
        })
        self.timeout = CRAWLER_CONFIG['request_timeout']
        self.delay = CRAWLER_CONFIG['request_delay']
        self.max_retries = CRAWLER_CONFIG['max_retries']
    
    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """获取网页内容"""
        for attempt in range(self.max_retries):
            try:
                logger.info(f"正在抓取: {url} (尝试 {attempt + 1}/{self.max_retries})")
                
                response = self.session.get(url, timeout=self.timeout)
                response.raise_for_status()
                response.encoding = response.apparent_encoding
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 添加延迟避免频繁请求
                time.sleep(self.delay)
                return soup
                
            except requests.exceptions.RequestException as e:
                logger.warning(f"抓取失败 {url}: {str(e)}")
                if attempt < self.max_retries - 1:
                    time.sleep(2 * (attempt + 1))  # 递增延迟
                else:
                    logger.error(f"抓取彻底失败: {url}")
                    return None
    
    def extract_news_from_source(self, source_config: Dict) -> List[Dict]:
        """从单个新闻源提取新闻"""
        source_name = source_config['name']
        source_url = source_config['url']
        selectors = source_config['selectors']
        weight = source_config['weight']
        
        logger.info(f"📰 开始抓取 {source_name}...")
        
        soup = self.fetch_page(source_url)
        if not soup:
            return []
        
        news_items = []
        
        try:
            # 根据配置提取新闻标题
            title_elements = soup.select(selectors['title'])
            link_elements = soup.select(selectors['link'])
            
            # 尝试提取时间和摘要（可选）
            time_elements = soup.select(selectors.get('time', '')) if selectors.get('time') else []
            summary_elements = soup.select(selectors.get('summary', '')) if selectors.get('summary') else []
            
            logger.info(f"找到 {len(title_elements)} 个标题元素")
            
            for i, title_elem in enumerate(title_elements[:CRAWLER_CONFIG['max_items_per_source']]):
                try:
                    # 提取标题
                    title = title_elem.get_text(strip=True)
                    if not title or len(title) < 10:  # 过滤过短标题
                        continue
                    
                    # 提取链接
                    link = ""
                    if i < len(link_elements):
                        link_elem = link_elements[i]
                        href = link_elem.get('href', '')
                        if href:
                            # 处理相对链接
                            link = urljoin(source_url, href)
                    
                    # 提取发布时间
                    published_time = ""
                    if i < len(time_elements):
                        time_text = time_elements[i].get_text(strip=True)
                        published_time = self._parse_time(time_text)
                    else:
                        # 如果没有时间信息，使用当前时间
                        published_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    
                    # 提取摘要
                    summary = ""
                    if i < len(summary_elements):
                        summary = summary_elements[i].get_text(strip=True)[:200]
                    
                    # 生成内容哈希
                    content_hash = hashlib.md5(f"{title}_{link}".encode()).hexdigest()
                    
                    # 分类新闻
                    category = self._classify_news(title)
                    
                    # 提取关键词
                    keywords = self._extract_keywords(title + " " + summary)
                    
                    news_item = {
                        'id': f"{source_name}_{i}_{int(time.time())}",
                        'title': title,
                        'url': link,
                        'source': source_name,
                        'published_time': published_time,
                        'summary': summary or title[:100] + "...",
                        'category': category,
                        'keywords': keywords,
                        'content_hash': content_hash,
                        'source_weight': weight,
                        'heat_score': 0.0  # 稍后计算
                    }
                    
                    news_items.append(news_item)
                    
                except Exception as e:
                    logger.warning(f"处理新闻项失败: {str(e)}")
                    continue
            
            logger.info(f"✅ {source_name} 成功提取 {len(news_items)} 条新闻")
            
        except Exception as e:
            logger.error(f"❌ {source_name} 抓取失败: {str(e)}")
        
        return news_items
    
    def _parse_time(self, time_text: str) -> str:
        """解析时间文本"""
        now = datetime.now()
        
        # 常见时间格式
        time_patterns = [
            r'(\d{4})-(\d{2})-(\d{2})\s+(\d{2}):(\d{2})',  # 2025-08-07 12:30
            r'(\d{2})-(\d{2})\s+(\d{2}):(\d{2})',         # 08-07 12:30
            r'(\d{1,2})月(\d{1,2})日\s+(\d{2}):(\d{2})',    # 8月7日 12:30
            r'(\d{1,2})分钟前',                           # 30分钟前
            r'(\d{1,2})小时前',                           # 2小时前
            r'今天\s+(\d{2}):(\d{2})',                    # 今天 12:30
            r'昨天\s+(\d{2}):(\d{2})',                    # 昨天 12:30
        ]
        
        for pattern in time_patterns:
            match = re.search(pattern, time_text)
            if match:
                try:
                    if '分钟前' in time_text:
                        minutes = int(match.group(1))
                        time_obj = now - timedelta(minutes=minutes)
                    elif '小时前' in time_text:
                        hours = int(match.group(1))
                        time_obj = now - timedelta(hours=hours)
                    elif '今天' in time_text:
                        hour, minute = int(match.group(1)), int(match.group(2))
                        time_obj = now.replace(hour=hour, minute=minute)
                    elif '昨天' in time_text:
                        hour, minute = int(match.group(1)), int(match.group(2))
                        time_obj = (now - timedelta(days=1)).replace(hour=hour, minute=minute)
                    else:
                        # 其他格式暂时使用当前时间
                        time_obj = now
                    
                    return time_obj.strftime('%Y-%m-%d %H:%M:%S')
                except:
                    pass
        
        # 默认返回当前时间
        return now.strftime('%Y-%m-%d %H:%M:%S')
    
    def _classify_news(self, title: str) -> str:
        """新闻分类"""
        categories = {
            '货币政策': ['央行', '货币政策', '降息', '加息', '降准', '美联储', '利率'],
            '股市': ['股市', '股票', '上证', '深证', '创业板', '科创板', '涨停', '跌停'],
            '数字货币': ['比特币', '数字货币', '区块链', '加密货币', '以太坊'],
            '房地产': ['房地产', '地产', '楼市', '房价', '住房'],
            '新能源': ['新能源', '电动车', '光伏', '风电', '锂电池'],
            '科技': ['人工智能', 'AI', '芯片', '半导体', '5G', '云计算'],
            '金融': ['银行', '保险', '券商', '基金', '信托'],
            '宏观经济': ['GDP', 'CPI', 'PPI', '通胀', '失业率', '经济'],
            '贸易': ['贸易', '进出口', '关税', '制裁', '贸易战'],
            '能源': ['石油', '天然气', '煤炭', '原油', '能源'],
        }
        
        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword in title:
                    return category
        
        return '其他'
    
    def _extract_keywords(self, text: str) -> List[str]:
        """提取关键词"""
        keywords = []
        
        # 从配置的关键词中提取
        for impact_level, keyword_groups in FINANCIAL_KEYWORDS.items():
            for group_name, group_keywords in keyword_groups.items():
                for keyword in group_keywords:
                    if keyword in text and keyword not in keywords:
                        keywords.append(keyword)
        
        return keywords[:5]  # 最多返回5个关键词
    
    def calculate_heat_score(self, news_item: Dict) -> float:
        """计算新闻热度分数"""
        score = 0.0
        
        # 1. 时效性评分 (0-30分)
        time_score = self._calculate_time_score(news_item['published_time'])
        score += time_score * HEAT_WEIGHTS['time_factor'] * 100
        
        # 2. 关键词权重评分 (0-25分)
        keyword_score = self._calculate_keyword_score(news_item['title'], news_item['keywords'])
        score += keyword_score * HEAT_WEIGHTS['keyword_factor'] * 100
        
        # 3. 标题吸引力评分 (0-20分)
        title_score = self._calculate_title_score(news_item['title'])
        score += title_score * HEAT_WEIGHTS['title_factor'] * 100
        
        # 4. 来源权威性评分 (0-25分)
        source_score = self._calculate_source_score(news_item['source'])
        score += source_score * HEAT_WEIGHTS['source_factor'] * 100
        
        # 5. 来源权重加成
        score *= news_item.get('source_weight', 1.0)
        
        return min(score, 100.0)
    
    def _calculate_time_score(self, published_time: str) -> float:
        """计算时效性分数"""
        try:
            pub_time = datetime.strptime(published_time, '%Y-%m-%d %H:%M:%S')
            now = datetime.now()
            hours_diff = (now - pub_time).total_seconds() / 3600
            
            if hours_diff <= 1:
                return 1.0
            elif hours_diff <= 3:
                return 0.9
            elif hours_diff <= 6:
                return 0.8
            elif hours_diff <= 12:
                return 0.6
            elif hours_diff <= 24:
                return 0.4
            elif hours_diff <= 48:
                return 0.2
            else:
                return 0.1
        except (ValueError, TypeError):
            return 0.5
    
    def _calculate_keyword_score(self, title: str, keywords: List[str]) -> float:
        """计算关键词权重分数"""
        score = 0.0
        text = title + ' ' + ' '.join(keywords)
        
        for impact_level, keyword_groups in FINANCIAL_KEYWORDS.items():
            weight = 0.8 if impact_level == 'high_impact' else 0.5 if impact_level == 'medium_impact' else 0.2
            for group_keywords in keyword_groups.values():
                for keyword in group_keywords:
                    if keyword in text:
                        score += weight
        
        return min(score, 1.0)
    
    def _calculate_title_score(self, title: str) -> float:
        """计算标题吸引力分数"""
        score = 0.0
        
        # 数字和百分比
        if re.search(r'\d+%', title):
            score += 0.3
        if re.search(r'[0-9]+', title):
            score += 0.2
        
        # 情感词汇
        emotional_words = ['突破', '暴涨', '暴跌', '创新高', '爆发', '崩盘', '飙升', '重磅', '突发']
        for word in emotional_words:
            if word in title:
                score += 0.4
                break
        
        return min(score, 1.0)
    
    def _calculate_source_score(self, source: str) -> float:
        """计算来源权威性分数"""
        authority = SOURCE_AUTHORITY.get(source, 50)  # 默认50分
        return authority / 100.0
    
    def get_top_hotspots(self, limit: int = 10, sources: List[str] = None) -> List[Dict]:
        """获取Top热点新闻"""
        print("🚀 启动真实新闻抓取...")
        
        all_news = []
        
        # 选择要抓取的新闻源
        sources_to_crawl = []
        if sources:
            # 指定新闻源
            for source_type in ['domestic', 'international']:
                for source_config in NEWS_SOURCES[source_type]:
                    if source_config['name'] in sources:
                        sources_to_crawl.append(source_config)
        else:
            # 默认抓取所有国内源和部分国际源
            sources_to_crawl.extend(NEWS_SOURCES['domestic'])
            # 国际源可能较慢，暂时只抓取部分
            # sources_to_crawl.extend(NEWS_SOURCES['international'][:1])
        
        # 抓取各个新闻源
        for source_config in sources_to_crawl:
            try:
                news_items = self.extract_news_from_source(source_config)
                all_news.extend(news_items)
            except Exception as e:
                logger.error(f"抓取新闻源失败 {source_config['name']}: {str(e)}")
                continue
        
        print(f"📊 总共抓取到 {len(all_news)} 条新闻")
        
        # 去重（基于标题相似度）
        unique_news = self._deduplicate_news(all_news)
        print(f"🔄 去重后剩余 {len(unique_news)} 条新闻")
        
        # 计算热度分数
        for news in unique_news:
            news['heat_score'] = self.calculate_heat_score(news)
        
        # 按热度排序
        unique_news.sort(key=lambda x: x['heat_score'], reverse=True)
        
        # 返回Top N
        top_news = unique_news[:limit]
        
        print(f"✅ 成功获取Top {len(top_news)} 热点新闻")
        return top_news
    
    def _deduplicate_news(self, news_list: List[Dict]) -> List[Dict]:
        """新闻去重"""
        seen_titles = set()
        unique_news = []
        
        for news in news_list:
            title = news['title']
            # 简单的相似度检查
            is_duplicate = False
            for seen_title in seen_titles:
                # 如果标题有80%以上相似，认为是重复
                similarity = len(set(title) & set(seen_title)) / len(set(title) | set(seen_title))
                if similarity > 0.8:
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                seen_titles.add(title)
                unique_news.append(news)
        
        return unique_news

def main():
    """测试真实新闻抓取"""
    crawler = RealNewsHotspotCrawler()
    
    # 先测试抓取少量新闻源
    test_sources = ['财联社', '第一财经']  # 先测试这两个
    
    top_news = crawler.get_top_hotspots(limit=10, sources=test_sources)
    
    # 显示结果
    print("\n🏆 热点新闻榜单:")
    print("=" * 50)
    for i, news in enumerate(top_news, 1):
        print(f"{i}. [{news['source']}] {news['title']}")
        print(f"   热度: {news['heat_score']:.1f}分 | 类别: {news['category']}")
        print(f"   关键词: {', '.join(news['keywords'])}")
        print(f"   时间: {news['published_time']}")
        print()

if __name__ == "__main__":
    main()
