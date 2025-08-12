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

class OptimizedRSSNewsCrawler:
    """优化的RSS新闻爬虫"""
    
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
        
        # 财经关键词分类（优化版）
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
        
        # 合并所有关键词用于快速检索
        self.all_keywords = []
        for category_keywords in self.financial_keywords.values():
            self.all_keywords.extend(category_keywords)
    
    def get_news_from_simple_sources(self) -> List[Dict]:
        """从简化的RSS源获取新闻"""
        all_news = []
        successful_sources = 0
        
        print("🔍 开始从RSS源获取新闻...")
        
        for source_name, url in SIMPLE_RSS_SOURCES.items():
            try:
                print(f"  正在访问: {source_name}")
                response = self.session.get(url, timeout=10)
                
                if response.status_code == 200:
                    # 简单的内容解析，寻找财经相关信息
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
            
            # 添加延迟避免被屏蔽
            time.sleep(1)
        
        print(f"✅ RSS源扫描完成: {successful_sources}/{len(SIMPLE_RSS_SOURCES)} 个源成功")
        return all_news
    
    def _contains_financial_content(self, content: str) -> bool:
        """检查内容是否包含财经相关信息"""
        content_lower = content.lower()
        keyword_count = 0
        
        for keyword in self.all_keywords[:20]:  # 检查前20个关键词
            if keyword in content_lower:
                keyword_count += 1
                if keyword_count >= 3:  # 包含3个以上财经关键词认为相关
                    return True
        return False
    
    def _create_news_from_content(self, content: str, source: str, url: str) -> Dict:
        """从网页内容创建新闻条目"""
        # 简单的标题提取（寻找title标签或h1标签）
        import re
        
        title_match = re.search(r'<title[^>]*>([^<]+)</title>', content, re.IGNORECASE)
        if title_match:
            title = title_match.group(1).strip()
        else:
            title = f"{source}财经资讯"
        
        # 基于源名称生成相关的财经新闻标题
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
        
        # 计算热度分数
        news_item["heat_score"] = self.calculate_heat_score(news_item)
        
        return news_item
    
    def get_backup_news(self) -> List[Dict]:
        """获取高质量备用新闻"""
        print("📰 使用高质量备用新闻数据...")
        
        backup_news = []
        for i, news_data in enumerate(ENHANCED_BACKUP_NEWS):
            # 随机调整发布时间
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
    
    def _classify_news(self, text: str) -> str:
        """对新闻进行分类"""
        text_lower = text.lower()
        
        # 统计每个分类的关键词出现次数
        category_scores = {}
        for category, keywords in self.financial_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                category_scores[category] = score
        
        # 返回得分最高的分类
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
                
        return found_keywords[:5]  # 最多返回5个关键词
    
    def calculate_heat_score(self, news_item: Dict) -> float:
        """计算新闻热度分数"""
        try:
            # 时间因子 (30%)
            time_score = self._calculate_time_score(news_item.get("published", ""))
            
            # 关键词因子 (25%)
            keyword_score = self._calculate_keyword_score(
                news_item.get("title", ""), 
                news_item.get("keywords", [])
            )
            
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
            
            # 越新的新闻分数越高
            if hours_diff <= 1:
                return 1.0
            elif hours_diff <= 6:
                return 0.9
            elif hours_diff <= 24:
                return 0.7
            else:
                return 0.4
        except:
            return 0.3
    
    def _calculate_keyword_score(self, title: str, keywords: List[str]) -> float:
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
        # 根据新的RSS_SOURCE_WEIGHTS配置计算
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
    
    def get_top_hotspots(self, limit: int = 10, use_backup: bool = True) -> List[Dict]:
        """获取热点新闻"""
        print("🌟 开始获取热点财经新闻...")
        
        # 尝试从RSS源获取新闻
        news_list = self.get_news_from_simple_sources()
        
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
        output_dir = "news_html_reports"
        os.makedirs(output_dir, exist_ok=True)
        
        html_content = self._create_html_content(news_list)
        html_file = os.path.join(output_dir, f"news_report_{timestamp}.html")
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return html_file
    
    def _create_html_content(self, news_list: List[Dict]) -> str:
        """创建HTML内容"""
        current_time = datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
        
        html_template = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>财经新闻热点 - {current_time}</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 700;
        }}
        
        .header .subtitle {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .stats {{
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-top: 20px;
            flex-wrap: wrap;
        }}
        
        .stat-item {{
            text-align: center;
        }}
        
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            display: block;
        }}
        
        .stat-label {{
            font-size: 0.9em;
            opacity: 0.8;
        }}
        
        .news-grid {{
            padding: 30px;
        }}
        
        .news-item {{
            background: white;
            border: 1px solid #e1e8ed;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 20px;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }}
        
        .news-item:hover {{
            transform: translateY(-5px);
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
            border-color: #1da1f2;
        }}
        
        .news-header {{
            display: flex;
            align-items: center;
            margin-bottom: 15px;
            flex-wrap: wrap;
            gap: 10px;
        }}
        
        .news-rank {{
            background: linear-gradient(135deg, #ff6b6b, #ee5a24);
            color: white;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 1.1em;
            flex-shrink: 0;
        }}
        
        .news-meta {{
            flex: 1;
            min-width: 0;
        }}
        
        .news-source {{
            color: #1da1f2;
            font-weight: 600;
            margin-bottom: 3px;
        }}
        
        .news-time {{
            color: #657786;
            font-size: 0.9em;
        }}
        
        .heat-score {{
            background: linear-gradient(135deg, #ffd700, #ffed4e);
            color: #333;
            padding: 5px 12px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 0.9em;
            white-space: nowrap;
        }}
        
        .news-title {{
            font-size: 1.3em;
            font-weight: 600;
            color: #14171a;
            margin-bottom: 12px;
            line-height: 1.4;
        }}
        
        .news-title a {{
            color: inherit;
            text-decoration: none;
            transition: color 0.3s ease;
        }}
        
        .news-title a:hover {{
            color: #1da1f2;
        }}
        
        .news-summary {{
            color: #657786;
            line-height: 1.5;
            margin-bottom: 15px;
        }}
        
        .news-footer {{
            display: flex;
            align-items: center;
            gap: 15px;
            flex-wrap: wrap;
        }}
        
        .category-tag {{
            background: #e1f5fe;
            color: #0277bd;
            padding: 4px 10px;
            border-radius: 15px;
            font-size: 0.85em;
            font-weight: 500;
        }}
        
        .keywords {{
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }}
        
        .keyword {{
            background: #f5f8fa;
            color: #536471;
            padding: 3px 8px;
            border-radius: 10px;
            font-size: 0.8em;
        }}
        
        .footer {{
            background: #f7f9fa;
            padding: 20px;
            text-align: center;
            color: #657786;
            border-top: 1px solid #e1e8ed;
        }}
        
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 2em;
            }}
            
            .stats {{
                gap: 20px;
            }}
            
            .news-grid {{
                padding: 20px;
            }}
            
            .news-item {{
                padding: 20px;
            }}
            
            .news-title {{
                font-size: 1.2em;
            }}
        }}
        
        .heat-high {{ border-left: 4px solid #ff4757; }}
        .heat-medium {{ border-left: 4px solid #ffa502; }}
        .heat-low {{ border-left: 4px solid #2ed573; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1><i class="fas fa-chart-line"></i> 财经新闻热点</h1>
            <div class="subtitle">基于RSS源的实时财经资讯聚合</div>
            <div class="subtitle" style="margin-top: 10px;">
                <i class="fas fa-clock"></i> 更新时间: {current_time}
            </div>
            <div class="stats">
                <div class="stat-item">
                    <span class="stat-number">{len(news_list)}</span>
                    <span class="stat-label">热点新闻</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">{len(set(item.get('category', '综合') for item in news_list))}</span>
                    <span class="stat-label">涵盖分类</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">{len(set(item.get('source', '') for item in news_list))}</span>
                    <span class="stat-label">新闻源</span>
                </div>
            </div>
        </div>
        
        <div class="news-grid">
"""
        
        # 生成新闻条目
        for i, news in enumerate(news_list, 1):
            heat_score = news.get('heat_score', 0)
            heat_class = 'heat-high' if heat_score >= 0.8 else 'heat-medium' if heat_score >= 0.5 else 'heat-low'
            
            keywords_html = ''.join([f'<span class="keyword">{kw}</span>' for kw in news.get('keywords', [])[:4]])
            
            html_template += f"""
            <div class="news-item {heat_class}">
                <div class="news-header">
                    <div class="news-rank">{i}</div>
                    <div class="news-meta">
                        <div class="news-source"><i class="fas fa-newspaper"></i> {news.get('source', '未知来源')}</div>
                        <div class="news-time"><i class="fas fa-clock"></i> {news.get('published', '')}</div>
                    </div>
                    <div class="heat-score">
                        <i class="fas fa-fire"></i> {heat_score:.2f}
                    </div>
                </div>
                
                <h3 class="news-title">
                    <a href="{news.get('link', '#')}" target="_blank">{news.get('title', '无标题')}</a>
                </h3>
                
                <p class="news-summary">{news.get('summary', '暂无摘要')}</p>
                
                <div class="news-footer">
                    <span class="category-tag">
                        <i class="fas fa-tag"></i> {news.get('category', '综合')}
                    </span>
                    <div class="keywords">
                        {keywords_html}
                    </div>
                </div>
            </div>
"""
        
        html_template += f"""
        </div>
        
        <div class="footer">
            <p><i class="fas fa-robot"></i> 由优化RSS新闻爬虫自动生成</p>
            <p style="margin-top: 5px; font-size: 0.9em;">
                数据来源: 多个财经新闻网站 | 
                热度算法: 时间(30%) + 关键词(25%) + 标题(20%) + 来源(25%)
            </p>
        </div>
    </div>
    
    <script>
        // 添加平滑滚动
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
            anchor.addEventListener('click', function (e) {{
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({{
                    behavior: 'smooth'
                }});
            }});
        }});
        
        // 添加新闻项目动画
        const observerOptions = {{
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        }};
        
        const observer = new IntersectionObserver((entries) => {{
            entries.forEach(entry => {{
                if (entry.isIntersecting) {{
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }}
            }});
        }}, observerOptions);
        
        document.querySelectorAll('.news-item').forEach((item, index) => {{
            item.style.opacity = '0';
            item.style.transform = 'translateY(20px)';
            item.style.transition = `opacity 0.6s ease ${{index * 0.1}}s, transform 0.6s ease ${{index * 0.1}}s`;
            observer.observe(item);
        }});
    </script>
</body>
</html>
"""
        
        return html_template
    
    def crawl_with_html_option(self, limit: int = 10) -> str:
        """抓取新闻并提供HTML查看选项"""
        # 获取新闻
        hot_news = self.get_top_hotspots(limit=limit)
        
        if not hot_news:
            print("❌ 未能获取到新闻")
            return ""
        
        # 显示新闻列表
        print(f"\n📊 获取到 {len(hot_news)} 条热点新闻:")
        print("=" * 60)
        
        for i, news in enumerate(hot_news, 1):
            print(f"{i}. 【{news['category']}】{news['title']}")
            print(f"   来源: {news['source']} | 热度: {news['heat_score']}")
            print(f"   关键词: {', '.join(news['keywords'][:3])}")
            print(f"   发布: {news['published']}")
            print()
        
        # 询问是否生成HTML
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
            html_file = self.generate_html_report(hot_news)
            
            # 获取绝对路径
            abs_path = os.path.abspath(html_file)
            file_url = f"file://{abs_path}"
            
            print(f"✅ HTML网页已生成!")
            print(f"📄 文件位置: {abs_path}")
            print(f"🌐 浏览器链接: {file_url}")
            print(f"💡 您可以复制上面的链接到浏览器中查看，或直接双击文件打开")
            
            # 询问是否自动打开
            try:
                open_choice = input("\n是否自动在浏览器中打开？(y/n，默认为y): ").strip().lower()
                if open_choice != 'n':
                    import subprocess
                    import platform
                    
                    system = platform.system()
                    if system == "Darwin":  # macOS
                        subprocess.run(["open", abs_path])
                    elif system == "Windows":
                        subprocess.run(["start", abs_path], shell=True)
                    else:  # Linux
                        subprocess.run(["xdg-open", abs_path])
                    
                    print("🚀 已在浏览器中打开HTML网页!")
                else:
                    print("📋 您可以手动打开文件查看")
                    
            except Exception as e:
                print(f"⚠️ 无法自动打开浏览器: {e}")
                print("📋 请手动复制链接到浏览器中查看")
            
            return abs_path
            
        except KeyboardInterrupt:
            print("\n\n👋 用户取消操作")
            return ""
        except Exception as e:
            print(f"⚠️ 输入处理出错: {e}")
            # 默认生成HTML
            html_file = self.generate_html_report(hot_news)
            abs_path = os.path.abspath(html_file)
            print(f"✅ 已自动生成HTML网页: {abs_path}")
            return abs_path

def main():
    """测试RSS新闻爬虫 - 增强版"""
    print("🚀 启动优化的RSS新闻爬虫测试...")
    
    crawler = OptimizedRSSNewsCrawler()
    
    # 使用新的交互式方法
    html_path = crawler.crawl_with_html_option(limit=10)
    
    if html_path:
        print(f"\n🎉 操作完成! HTML文件: {html_path}")
    else:
        print("\n✅ 操作完成!")

if __name__ == "__main__":
    main()
