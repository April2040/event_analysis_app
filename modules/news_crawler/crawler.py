"""
新闻爬虫模块 - 主爬虫类
整合了RSS源抓取、热度评分、HTML生成等功能
"""

import requests
import json
import random
import os
import subprocess
import platform
from datetime import datetime, timedelta
from typing import List, Dict, Any
import time

from .config import (
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
    
    def get_top_hotspots(self, limit: int = 10, use_backup: bool = True) -> List[Dict]:
        """获取热点新闻"""
        print("🌟 开始获取热点财经新闻...")
        
        # 尝试从RSS源获取新闻
        news_list = self.get_news_from_rss_sources()
        
        # 如果RSS源新闻不足且允许使用备用数据
        if len(news_list) < limit // 2 and use_backup:
            backup_news = self.get_backup_news()
            news_list.extend(backup_news)
            print(f"📰 合并备用新闻，当前共 {len(news_list)} 条")
        
        # 按热度分数排序
        news_list.sort(key=lambda x: x.get("heat_score", 0), reverse=True)
        
        # 返回指定数量的热点新闻
        top_news = news_list[:limit]
        
        print(f"✨ 成功获取 {len(top_news)} 条热点新闻")
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
        import re
        
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
