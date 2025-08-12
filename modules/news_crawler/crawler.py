"""
新闻爬虫模块 - 主爬虫类
整合了RSS源抓取、热度评分、HTML生成等功能
"""

import requests
import json
import random
import re
import os
import subprocess
import platform
from datetime import datetime, timedelta
from typing import List, Dict, Any
from urllib.parse import urljoin, urlparse
import time
from bs4 import BeautifulSoup

from .config import (
    RSS_FEEDS,
    SIMPLE_RSS_SOURCES,
    ENHANCED_BACKUP_NEWS,
    RSS_SOURCE_WEIGHTS
)
from .html_generator import HTMLReportGenerator

class NewsWebCrawler:
    """新闻网站爬虫 - 主要爬虫类"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        
        # 财经关键词分类
        self.financial_keywords = {
            "股市": ["股票", "A股", "港股", "美股", "股市", "大盘", "指数", "上证", "深证", "创业板", "科创板", "涨停", "跌停"],
            "货币政策": ["央行", "利率", "降准", "加息", "货币政策", "流动性", "M2", "存款准备金", "基准利率"],
            "宏观经济": ["GDP", "CPI", "PPI", "PMI", "经济增长", "通胀", "通缩", "失业率", "经济数据"],
            "金融": ["银行", "保险", "证券", "基金", "信托", "债券", "理财", "金融监管", "资管"],
            "房地产": ["房价", "楼市", "地产", "土地", "住房", "商品房", "二手房", "房贷", "限购"],
            "科技": ["人工智能", "AI", "芯片", "5G", "新能源", "电动车", "科技股", "互联网", "数字化"],
            "能源": ["原油", "天然气", "煤炭", "电力", "新能源", "光伏", "风电", "石油", "能源"],
            "消费": ["消费", "零售", "电商", "白酒", "食品", "服装", "汽车", "家电", "消费升级"],
            "国际": ["美联储", "美元", "汇率", "贸易", "关税", "进出口", "国际经济", "全球"],
            "政策": ["政策", "改革", "税收", "财政", "监管", "法规", "国务院", "发改委"]
        }
        
        # 合并所有关键词
        self.all_keywords = []
        for category_keywords in self.financial_keywords.values():
            self.all_keywords.extend(category_keywords)
        
        # HTML生成器
        self.html_generator = HTMLReportGenerator()
    
    def _is_finance_related(self, text: str) -> bool:
        """判断文本是否与财经相关"""
        text_lower = text.lower()
        
        # 检查是否包含财经关键词
        keyword_count = 0
        for keyword in self.all_keywords:
            if keyword in text_lower:
                keyword_count += 1
                if keyword_count >= 1:  # 包含至少1个财经关键词就认为相关
                    return True
        
        # 检查是否包含基础财经词汇
        basic_finance_words = [
            "财经", "经济", "金融", "股票", "投资", "市场", "银行", "证券", "基金", "汇率", "GDP",
            "税收", "税法", "增值税", "所得税", "关税", "财政", "预算", "货币", "通胀", "通缩",
            "利率", "债券", "期货", "外汇", "保险", "房地产", "贸易", "进出口", "消费", "零售",
            "制造业", "工业", "服务业", "农业", "能源", "石油", "黄金", "大宗商品", "供应链",
            "企业", "公司", "集团", "上市", "IPO", "并购", "重组", "破产", "融资", "借贷",
            "央行", "美联储", "欧央行", "人民银行", "监管", "政策", "改革", "开放", "发展"
        ]
        for word in basic_finance_words:
            if word in text_lower:
                return True
                
        return False
    
    def get_news_from_rss_feeds(self) -> List[Dict]:
        """从RSS Feed获取新闻（优化版本 - 快速重试机制）"""
        print("📰 开始从RSS Feed获取新闻...")
        all_news = []
        successful_sources = 0
        
        for source, config in RSS_FEEDS.items():
            try:
                print(f"  正在访问RSS: {source}")
                start_time = time.time()
                
                # 快速重试机制 - 最多尝试2次，每次超时5秒
                response = None
                for attempt in range(2):
                    try:
                        response = self.session.get(config["url"], timeout=5)
                        response.raise_for_status()
                        break
                    except Exception as e:
                        if attempt == 0:
                            print(f"    ⚠️ 第1次尝试失败，快速重试... ({e})")
                            continue
                        else:
                            raise e
                
                if not response:
                    continue
                
                fetch_time = time.time() - start_time
                
                # 确保正确的中文编码
                if response.encoding.lower() in ['iso-8859-1', 'ascii']:
                    response.encoding = 'utf-8'
                
                # 根据类型解析内容
                if config["type"] == "xml":
                    news_items = self._parse_xml_feed(response.text, source)
                elif config["type"] == "json":
                    news_items = self._parse_json_feed(response.text, source)
                else:
                    news_items = self._parse_html_feed(response.text, source)
                
                if news_items:
                    print(f"  ✅ {source} - 获取到 {len(news_items)} 条新闻 (耗时: {fetch_time:.2f}s)")
                    all_news.extend(news_items)
                    successful_sources += 1
                else:
                    print(f"  ⚠️ {source} - 未获取到有效新闻 (耗时: {fetch_time:.2f}s)")
                    
            except Exception as e:
                print(f"  ❌ {source} - 访问失败: {e}")
                continue
                
        print(f"✅ RSS Feed扫描完成: {successful_sources}/{len(RSS_FEEDS)} 个源成功")
        
        # 按热度分数排序
        all_news.sort(key=lambda x: x.get("heat_score", 0), reverse=True)
        return all_news[:50]  # 返回前50条
    
    def _parse_xml_feed(self, content: str, source: str) -> List[Dict]:
        """解析XML RSS内容"""
        news_items = []
        try:
            soup = BeautifulSoup(content, 'xml')
            
            # 查找所有item元素
            items = soup.find_all('item')
            
            for item in items[:20]:  # 限制数量
                try:
                    title_elem = item.find('title')
                    link_elem = item.find('link')
                    description_elem = item.find('description')
                    pub_date_elem = item.find('pubDate')
                    
                    if title_elem and link_elem:
                        title = title_elem.get_text(strip=True)
                        link = link_elem.get_text(strip=True)
                        
                        # 过滤财经相关新闻
                        if self._is_finance_related(title):
                            description = description_elem.get_text(strip=True) if description_elem else ""
                            pub_date = pub_date_elem.get_text(strip=True) if pub_date_elem else ""
                            
                            # 转换发布时间格式
                            published = self._parse_publish_date(pub_date)
                            
                            category = self._classify_news(title)
                            keywords = self._extract_keywords(title)
                            
                            news_item = {
                                "title": title,
                                "link": link,
                                "source": source,
                                "published": published,
                                "category": category,
                                "keywords": keywords,
                                "summary": description[:200] + "..." if len(description) > 200 else description,
                                "heat_score": 0.0
                            }
                            
                            news_item["heat_score"] = self.calculate_heat_score(news_item)
                            news_items.append(news_item)
                            
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"  ⚠️ 解析XML RSS失败: {e}")
            
        return news_items
    
    def _parse_publish_date(self, date_str: str) -> str:
        """解析RSS发布时间"""
        if not date_str:
            return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
        try:
            # 处理常见的RSS时间格式
            # RFC 2822格式: Mon, 05 Jun 2023 14:30:00 +0800
            
            # 简化处理：提取日期部分
            date_match = re.search(r'(\d{1,2})\s+(\w{3})\s+(\d{4})\s+(\d{1,2}):(\d{2}):(\d{2})', date_str)
            if date_match:
                day, month_abbr, year, hour, minute, second = date_match.groups()
                
                # 月份映射
                month_map = {
                    'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
                    'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
                    'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
                }
                
                month = month_map.get(month_abbr, '01')
                return f"{year}-{month}-{day.zfill(2)} {hour.zfill(2)}:{minute}:{second}"
            
            # 如果解析失败，返回当前时间
            return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
        except Exception:
            return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def _parse_json_feed(self, content: str, source: str) -> List[Dict]:
        """解析JSON格式的新闻源"""
        news_items = []
        try:
            data = json.loads(content)
            
            # 根据不同源的JSON结构进行解析
            if isinstance(data, dict) and 'data' in data:
                items = data['data']
            elif isinstance(data, list):
                items = data
            else:
                return news_items
                
            for item in items[:20]:
                try:
                    title = item.get('title', '')
                    link = item.get('url', '') or item.get('link', '')
                    
                    if title and link and self._is_finance_related(title):
                        published = item.get('time', '') or item.get('publish_time', '')
                        if not published:
                            published = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        
                        category = self._classify_news(title)
                        keywords = self._extract_keywords(title)
                        
                        news_item = {
                            "title": title,
                            "link": link,
                            "source": source,
                            "published": published,
                            "category": category,
                            "keywords": keywords,
                            "summary": item.get('summary', '')[:200] + "..." if item.get('summary') else "",
                            "heat_score": 0.0
                        }
                        
                        news_item["heat_score"] = self.calculate_heat_score(news_item)
                        news_items.append(news_item)
                        
                except Exception:
                    continue
                    
        except Exception as e:
            print(f"  ⚠️ 解析JSON失败: {e}")
            
        return news_items
    
    def _parse_html_feed(self, content: str, source: str) -> List[Dict]:
        """解析HTML内容提取新闻"""
        news_items = []
        try:
            soup = BeautifulSoup(content, 'html.parser')
            
            # 根据不同源的HTML结构提取新闻
            if "新浪" in source:
                news_items = self._parse_sina_html(soup, source)
            elif "东方财富" in source:
                news_items = self._parse_eastmoney_html(soup, source)
            elif "金融界" in source:
                news_items = self._parse_jrj_html(soup, source)
            else:
                # 通用HTML解析
                news_items = self._parse_generic_html(soup, source)
                
        except Exception as e:
            print(f"  ⚠️ 解析HTML失败: {e}")
            
        return news_items
    
    def _parse_sina_html(self, soup: BeautifulSoup, source: str) -> List[Dict]:
        """解析新浪财经HTML"""
        return []  # 简化实现，返回空列表
    
    def _parse_eastmoney_html(self, soup: BeautifulSoup, source: str) -> List[Dict]:
        """解析东方财富HTML"""
        return []  # 简化实现，返回空列表
    
    def _parse_jrj_html(self, soup: BeautifulSoup, source: str) -> List[Dict]:
        """解析金融界HTML"""
        return []  # 简化实现，返回空列表
    
    def _parse_generic_html(self, soup: BeautifulSoup, source: str) -> List[Dict]:
        """通用HTML解析"""
        return []  # 简化实现，返回空列表

    def get_news_from_rss_sources(self) -> List[Dict]:
        """从RSS源获取新闻"""
        all_news = []
        successful_sources = 0
        
        print("🔍 开始从RSS源获取新闻...")
        
        for source_name, url in SIMPLE_RSS_SOURCES.items():
            try:
                print(f"  正在访问: {source_name}")
                response = self.session.get(url, timeout=10)
                
                if response.status_code == 200:
                    content = response.text
                    if self._contains_financial_content(content):
                        news_item = self._create_news_from_content(content, source_name, url)
                        if news_item:
                            all_news.append(news_item)
                            successful_sources += 1
                            print(f"  ✅ {source_name} - 成功获取新闻")
                    else:
                        print(f"  ⚠️ {source_name} - 无相关财经内容")
                else:
                    print(f"  ❌ {source_name} - HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"  ❌ {source_name} - 错误: {str(e)[:50]}")
                continue
            
            time.sleep(1)  # 避免被屏蔽
        
        print(f"✅ RSS源扫描完成: {successful_sources}/{len(SIMPLE_RSS_SOURCES)} 个源成功")
        return all_news
    
    def get_enhanced_backup_news(self) -> List[Dict]:
        """获取增强版备用新闻 - 真实的热点财经新闻"""
        print("📰 使用今日热点财经新闻数据...")
        
        backup_news = []
        current_time = datetime.now()
        
        for i, news_data in enumerate(ENHANCED_BACKUP_NEWS):
            # 生成今天的随机时间
            hours_ago = random.randint(1, 12)  # 1-12小时前
            minutes_ago = random.randint(0, 59)
            pub_time = current_time - timedelta(hours=hours_ago, minutes=minutes_ago)
            
            news_item = {
                "title": news_data["title"],  # 使用真实的新闻标题
                "link": news_data.get("link", f"https://finance.example.com/news/{i+1}"),
                "source": news_data["source"],
                "published": pub_time.strftime("%Y-%m-%d %H:%M:%S"),
                "category": news_data["category"],
                "keywords": news_data["keywords"],
                "summary": news_data["summary"],
                "heat_score": 0.0
            }
            
            # 计算热度分数
            news_item["heat_score"] = self.calculate_heat_score(news_item)
            
            # 根据重要性调整热度分数
            importance_bonus = {
                "high": 0.3,
                "medium": 0.15,
                "low": 0.0
            }.get(news_data.get("importance", "medium"), 0.15)
            
            news_item["heat_score"] += importance_bonus
            news_item["heat_score"] = min(news_item["heat_score"], 1.0)
            
            backup_news.append(news_item)
        
        # 按热度分数排序
        backup_news.sort(key=lambda x: x["heat_score"], reverse=True)
        
        print(f"✅ 加载了 {len(backup_news)} 条今日热点财经新闻")
        return backup_news
    
    def get_backup_news(self) -> List[Dict]:
        """获取高质量备用新闻"""
        print("📰 使用高质量备用新闻数据...")
        
        backup_news = []
        for i, news_data in enumerate(ENHANCED_BACKUP_NEWS):
            base_time = datetime.now() - timedelta(hours=random.randint(1, 6))
            
            news_item = {
                "title": news_data["title"],
                "link": f"https://finance.example.com/news/{i+1}",
                "source": news_data["source"],
                "published": base_time.strftime("%Y-%m-%d %H:%M:%S"),
                "category": news_data["category"],
                "keywords": news_data["keywords"],
                "summary": news_data["summary"],
                "heat_score": 0.0
            }
            
            # 根据重要性调整基础分数
            importance_bonus = {
                "high": 0.3,
                "medium": 0.15,
                "low": 0.0
            }.get(news_data.get("importance", "medium"), 0.15)
            
            news_item["heat_score"] = self.calculate_heat_score(news_item) + importance_bonus
            backup_news.append(news_item)
        
        return backup_news
    
    def get_top_hotspots(self, limit: int = 10) -> List[Dict]:
        """获取热点新闻 - 仅真实RSS新闻，不混合备用数据"""
        print("🌟 开始获取真实RSS热点财经新闻...")
        
        # 首先尝试从RSS Feed获取新闻
        news_list = self.get_news_from_rss_feeds()
        
        # 如果RSS Feed获取失败，尝试RSS Sources
        if not news_list:
            print("🔄 RSS Feed获取失败，尝试RSS Sources...")
            news_list = self.get_news_from_rss_sources()
        
        # 只检查是否有有效的真实新闻
        if not news_list:
            print("❌ 未能获取到真实RSS新闻")
            return []
        
        # 过滤掉低质量新闻（只是网站名称的）
        filtered_news = []
        for news in news_list:
            title = news.get("title", "").strip()
            if title and title not in ["腾讯网", "网易财经-有态度的财经门户", "财经", "新浪财经", "东方财富网"]:
                # 检查标题是否包含实际内容而不只是网站名
                if not any(site in title for site in ["腾讯", "网易", "搜狐", "新浪", "东方财富"]) or len(title) > 10:
                    filtered_news.append(news)
        
        # 为真实新闻设置优先级权重
        for news in filtered_news:
            base_score = news.get("heat_score", 0)
            link = news.get("link", "")
            
            # FT中文网优先级最高
            if "ftchinese.com" in link:
                news["priority_score"] = base_score + 1000
            # 中新网次优先级
            elif "chinanews.com" in link:
                news["priority_score"] = base_score + 800
            # 其他真实RSS来源
            else:
                news["priority_score"] = base_score + 500
        
        # 按优先级分数排序（真实新闻内部排序）
        filtered_news.sort(key=lambda x: x.get("priority_score", 0), reverse=True)
        
        # 返回指定数量的真实热点新闻
        top_news = filtered_news[:limit]
        
        print(f"✨ 成功获取 {len(top_news)} 条真实RSS热点新闻")
        if top_news:
            print(f"📑 新闻来源: {', '.join(set(news.get('source', '未知') for news in top_news))}")
        
        return top_news
    
    def generate_html_report(self, news_list: List[Dict]) -> str:
        """生成HTML新闻报告"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 确保输出目录存在
        output_dir = "outputs/news_reports"
        os.makedirs(output_dir, exist_ok=True)
        
        html_content = self.html_generator.generate_html(news_list)
        html_file = os.path.join(output_dir, f"news_report_{timestamp}.html")
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return html_file
    
    def crawl_with_html_option(self, limit: int = 10) -> str:
        """抓取新闻并提供HTML查看选项"""
        # 获取新闻
        hot_news = self.get_top_hotspots(limit=limit)
        
        if not hot_news:
            print("❌ 未能获取到新闻")
            return ""
        
        # 显示新闻列表
        self._display_news_list(hot_news)
        
        # 询问是否生成HTML
        return self._handle_html_generation(hot_news)
    
    def _display_news_list(self, news_list: List[Dict]):
        """显示新闻列表"""
        print(f"\n📊 获取到 {len(news_list)} 条热点新闻:")
        print("=" * 60)
        
        for i, news in enumerate(news_list, 1):
            print(f"{i}. 【{news['category']}】{news['title']}")
            print(f"   来源: {news['source']} | 热度: {news['heat_score']}")
            print(f"   关键词: {', '.join(news['keywords'][:3])}")
            print(f"   发布: {news['published']}")
            print()
    
    def _handle_html_generation(self, news_list: List[Dict]) -> str:
        """处理HTML生成选项"""
        print("🌐 是否需要生成HTML网页查看新闻？")
        print("1. 是，生成HTML网页")
        print("2. 否，仅查看终端输出")
        
        try:
            choice = input("\n请选择 (1-2，默认为1): ").strip()
            if choice == "2":
                print("✅ 已完成新闻展示")
                return ""
            
            # 生成HTML报告
            print("\n🎨 正在生成HTML网页...")
            html_file = self.generate_html_report(news_list)
            
            # 获取绝对路径
            abs_path = os.path.abspath(html_file)
            file_url = f"file://{abs_path}"
            
            print("✅ HTML网页已生成!")
            print(f"📄 文件位置: {abs_path}")
            print(f"🌐 浏览器链接: {file_url}")
            print("💡 您可以复制上面的链接到浏览器中查看，或直接双击文件打开")
            
            # 询问是否自动打开
            self._handle_browser_opening(abs_path)
            
            return abs_path
            
        except KeyboardInterrupt:
            print("\n\n👋 用户取消操作")
            return ""
        except Exception as e:
            print(f"⚠️ 输入处理出错: {e}")
            # 默认生成HTML
            html_file = self.generate_html_report(news_list)
            abs_path = os.path.abspath(html_file)
            print(f"✅ 已自动生成HTML网页: {abs_path}")
            return abs_path
    
    def _handle_browser_opening(self, abs_path: str):
        """处理浏览器打开选项"""
        try:
            open_choice = input("\n是否自动在浏览器中打开？(y/n，默认为y): ").strip().lower()
            if open_choice != 'n':
                system = platform.system()
                if system == "Darwin":  # macOS
                    subprocess.run(["open", abs_path], check=False)
                elif system == "Windows":
                    subprocess.run(["start", abs_path], shell=True, check=False)
                else:  # Linux
                    subprocess.run(["xdg-open", abs_path], check=False)
                
                print("🚀 已在浏览器中打开HTML网页!")
            else:
                print("📋 您可以手动打开文件查看")
                
        except Exception as e:
            print(f"⚠️ 无法自动打开浏览器: {e}")
            print("📋 请手动复制链接到浏览器中查看")
    
    def _contains_financial_content(self, content: str) -> bool:
        """检查内容是否包含财经相关信息"""
        content_lower = content.lower()
        keyword_count = 0
        
        for keyword in self.all_keywords[:20]:
            if keyword in content_lower:
                keyword_count += 1
                if keyword_count >= 3:
                    return True
        return False
    
    def _create_news_from_content(self, content: str, source: str, url: str) -> Dict:
        """从网页内容创建新闻条目"""
        # 简单的标题提取（寻找title标签或h1标签）
        
        title_match = re.search(r'<title[^>]*>([^<]+)</title>', content, re.IGNORECASE)
        if title_match:
            title = title_match.group(1).strip()
        else:
            title = f"{source}财经资讯"
        
        category = self._classify_news(title)
        keywords = self._extract_keywords(title)
        
        news_item = {
            "title": title,
            "link": url,
            "source": source,
            "published": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "category": category,
            "keywords": keywords,
            "summary": f"来自{source}的最新财经资讯",
            "heat_score": 0.0
        }
        
        news_item["heat_score"] = self.calculate_heat_score(news_item)
        return news_item
    
    def _classify_news(self, text: str) -> str:
        """对新闻进行分类"""
        text_lower = text.lower()
        
        category_scores = {}
        for category, keywords in self.financial_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                category_scores[category] = score
        
        if category_scores:
            return max(category_scores, key=category_scores.get)
        else:
            return "综合"
    
    def _extract_keywords(self, text: str) -> List[str]:
        """提取关键词"""
        text_lower = text.lower()
        found_keywords = []
        
        for keyword in self.all_keywords:
            if keyword in text_lower and keyword not in found_keywords:
                found_keywords.append(keyword)
                
        return found_keywords[:5]
    
    def calculate_heat_score(self, news_item: Dict) -> float:
        """计算新闻热度分数"""
        try:
            # 时间因子 (30%)
            time_score = self._calculate_time_score(news_item.get("published", ""))
            
            # 关键词因子 (25%)
            keyword_score = self._calculate_keyword_score(news_item.get("keywords", []))
            
            # 标题因子 (20%)
            title_score = self._calculate_title_score(news_item.get("title", ""))
            
            # 来源权威性因子 (25%)
            source_score = self._calculate_source_score(news_item.get("source", ""))
            
            # 加权计算总分
            total_score = (
                time_score * 0.30 +
                keyword_score * 0.25 +
                title_score * 0.20 +
                source_score * 0.25
            )
            
            return round(total_score, 2)
            
        except Exception as e:
            print(f"计算热度分数时出错: {e}")
            return 0.5
    
    def _calculate_time_score(self, published_time: str) -> float:
        """计算时间分数"""
        try:
            if not published_time:
                return 0.3
                
            pub_dt = datetime.strptime(published_time, "%Y-%m-%d %H:%M:%S")
            now = datetime.now()
            hours_diff = (now - pub_dt).total_seconds() / 3600
            
            if hours_diff <= 1:
                return 1.0
            elif hours_diff <= 6:
                return 0.9
            elif hours_diff <= 24:
                return 0.7
            else:
                return 0.4
        except Exception:
            return 0.3
    
    def _calculate_keyword_score(self, keywords: List[str]) -> float:
        """计算关键词分数"""
        if not keywords:
            return 0.3
            
        high_impact_keywords = ["央行", "降准", "加息", "IPO", "重组", "涨停", "跌停", "突破"]
        
        score = len(keywords) * 0.1
        for keyword in keywords:
            if keyword in high_impact_keywords:
                score += 0.3
        
        return min(score, 1.0)
    
    def _calculate_title_score(self, title: str) -> float:
        """计算标题分数"""
        if not title:
            return 0.3
            
        impact_words = ["突破", "暴涨", "暴跌", "创新高", "创新低", "重大", "紧急", "突发"]
        
        score = 0.3
        for word in impact_words:
            if word in title:
                score += 0.2
                
        return min(score, 1.0)
    
    def _calculate_source_score(self, source: str) -> float:
        """计算来源权威性分数"""
        source_lower = source.lower()
        
        if any(official in source_lower for official in ["人民", "央视", "经济日报", "新华"]):
            return RSS_SOURCE_WEIGHTS["官方媒体"]
        elif any(prof in source_lower for prof in ["财联社", "财新", "第一财经"]):
            return RSS_SOURCE_WEIGHTS["专业财经"]
        elif any(portal in source_lower for portal in ["新浪", "网易", "腾讯"]):
            return RSS_SOURCE_WEIGHTS["门户财经"]
        elif any(intl in source_lower for intl in ["路透", "彭博", "华尔街"]):
            return RSS_SOURCE_WEIGHTS["国际媒体"]
        else:
            return RSS_SOURCE_WEIGHTS["行业媒体"]
