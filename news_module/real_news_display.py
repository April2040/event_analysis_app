# real_news_display.py
"""
真实新闻展示系统 - 结合真实新闻抓取与展示界面
提供从演示版本到真实版本的平滑过渡
"""

import json
import os
from datetime import datetime
from typing import List, Dict

# 导入不同的抓取器
from rss_news_crawler import RSSNewsHotspotCrawler
try:
    from real_news_crawler import RealNewsHotspotCrawler
    REAL_CRAWLER_AVAILABLE = True
except ImportError:
    REAL_CRAWLER_AVAILABLE = False

class RealNewsDisplaySystem:
    """真实新闻展示系统"""
    
    def __init__(self, crawler_type: str = "rss"):
        """
        初始化新闻展示系统
        crawler_type: "rss" | "real" | "auto"
        """
        self.output_dir = "real_news_display"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 根据类型选择抓取器
        if crawler_type == "rss":
            self.crawler = RSSNewsHotspotCrawler()
            self.crawler_name = "RSS抓取器"
        elif crawler_type == "real" and REAL_CRAWLER_AVAILABLE:
            self.crawler = RealNewsHotspotCrawler()
            self.crawler_name = "真实网站抓取器"
        else:
            # 自动选择或默认RSS
            self.crawler = RSSNewsHotspotCrawler()
            self.crawler_name = "RSS抓取器（自动选择）"
    
    def crawl_and_display(self, top_n: int = 10) -> Dict:
        """抓取并展示真实热点新闻"""
        print(f"🚀 启动真实新闻展示系统 - {self.crawler_name}")
        print("=" * 60)
        
        # Step 1: 抓取真实新闻
        print(f"📡 正在使用{self.crawler_name}抓取Top {top_n}热点财经新闻...")
        top_news = self.crawler.get_top_hotspots(limit=top_n)
        
        # Step 2: 控制台展示
        self._display_news_summary(top_news)
        
        # Step 3: 生成HTML展示页面
        html_content = self._generate_real_news_html(top_news)
        
        # Step 4: 保存结果
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # 保存HTML展示页面
        html_file = os.path.join(self.output_dir, f"real_news_{timestamp}.html")
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # 保存JSON数据
        json_file = os.path.join(self.output_dir, f"real_data_{timestamp}.json")
        news_data = {
            'timestamp': datetime.now().isoformat(),
            'crawler_type': self.crawler_name,
            'total_count': len(top_news),
            'news_list': top_news
        }
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(news_data, f, ensure_ascii=False, indent=2)
        
        result = {
            'success': True,
            'timestamp': timestamp,
            'crawler_type': self.crawler_name,
            'news_count': len(top_news),
            'html_file': html_file,
            'json_file': json_file,
            'news_list': top_news
        }
        
        print("\n✅ 真实新闻展示完成！")
        print(f"📄 HTML展示: {html_file}")
        print(f"📁 数据文件: {json_file}")
        
        return result
    
    def _display_news_summary(self, news_list: List[Dict]):
        """在控制台展示新闻摘要"""
        print("\n" + "=" * 80)
        print("📰 真实热点财经新闻榜单")
        print("=" * 80)
        print(f"📅 抓取时间: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}")
        print(f"🔧 抓取方式: {self.crawler_name}")
        print(f"📊 新闻总数: {len(news_list)}条")
        print()
        
        # 按类别统计
        categories = {}
        for news in news_list:
            cat = news['category']
            categories[cat] = categories.get(cat, 0) + 1
        
        print("📈 类别分布:")
        for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            print(f"  🔸 {cat}: {count}条")
        print()
        
        # 热度分布
        high_heat = len([n for n in news_list if n['heat_score'] >= 70])
        medium_heat = len([n for n in news_list if 50 <= n['heat_score'] < 70])
        low_heat = len([n for n in news_list if n['heat_score'] < 50])
        
        print("🔥 热度分布:")
        print(f"  🌟 高热度(≥70分): {high_heat}条")
        print(f"  🔥 中热度(50-69分): {medium_heat}条")
        print(f"  💫 低热度(<50分): {low_heat}条")
        print()
        
        print("🏆 真实热点新闻详细列表:")
        print("-" * 80)
        
        for i, news in enumerate(news_list, 1):
            print(f"【第{i}名】热度: {news['heat_score']:.1f}分")
            print(f"标题: {news['title']}")
            print(f"来源: {news['source']} | 类别: {news['category']}")
            print(f"关键词: {', '.join(news['keywords'])}")
            print(f"发布时间: {news['published_time']}")
            print(f"链接: {news['url']}")
            print("-" * 80)
    
    def _generate_real_news_html(self, news_list: List[Dict]) -> str:
        """生成真实新闻展示HTML页面"""
        
        # 计算统计数据
        categories = {}
        for news in news_list:
            cat = news['category']
            categories[cat] = categories.get(cat, 0) + 1
        
        category_stats = ""
        for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            category_stats += f'<span class="inline-block bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm mr-2 mb-2">{cat}: {count}条</span>'
        
        # 生成新闻卡片
        news_cards = ""
        for i, news in enumerate(news_list, 1):
            # 根据热度设置颜色
            if news['heat_score'] >= 70:
                heat_color = "bg-red-100 text-red-800"
                heat_icon = "🌟"
                rank_color = "bg-red-600"
            elif news['heat_score'] >= 50:
                heat_color = "bg-orange-100 text-orange-800"
                heat_icon = "🔥"
                rank_color = "bg-orange-600"
            else:
                heat_color = "bg-gray-100 text-gray-800"
                heat_icon = "💫"
                rank_color = "bg-gray-600"
            
            keywords_html = ""
            for keyword in news['keywords']:
                keywords_html += f'<span class="inline-block bg-purple-100 text-purple-800 px-2 py-1 rounded text-xs mr-1">{keyword}</span>'
            
            # 判断是否为真实链接
            is_real_link = not news['url'].startswith('https://example.com')
            link_icon = "🌐" if is_real_link else "📝"
            link_text = "查看原文" if is_real_link else "演示链接"
            
            news_cards += f"""
            <div class="bg-white rounded-lg shadow-md p-6 mb-4 hover:shadow-xl transition-all duration-300 border-l-4 border-indigo-500">
                <div class="flex justify-between items-start mb-3">
                    <div class="flex items-center">
                        <span class="{rank_color} text-white px-3 py-1 rounded-full text-sm font-bold mr-3">第{i}名</span>
                        <span class="{heat_color} px-2 py-1 rounded-full text-xs font-semibold">{heat_icon} {news['heat_score']:.1f}分</span>
                    </div>
                    <span class="bg-green-100 text-green-800 px-2 py-1 rounded text-xs font-semibold">{news['category']}</span>
                </div>
                
                <h3 class="text-lg font-bold text-gray-900 mb-3 leading-tight hover:text-indigo-600 transition-colors">
                    {news['title']}
                </h3>
                
                <div class="bg-gray-50 rounded-lg p-3 mb-3">
                    <p class="text-sm text-gray-700 leading-relaxed">{news['summary']}</p>
                </div>
                
                <div class="flex flex-wrap items-center text-sm text-gray-600 mb-3">
                    <span class="flex items-center mr-4">
                        <i class="fas fa-newspaper mr-1 text-blue-500"></i>
                        <strong>{news['source']}</strong>
                    </span>
                    <span class="flex items-center mr-4">
                        <i class="fas fa-clock mr-1 text-green-500"></i>
                        {news['published_time']}
                    </span>
                </div>
                
                <div class="mb-3">
                    <span class="text-sm text-gray-500 mr-2">热门关键词:</span>
                    {keywords_html}
                </div>
                
                <div class="border-t pt-3 flex justify-between items-center">
                    <a href="{news['url']}" target="_blank" class="text-blue-600 hover:text-blue-800 text-sm flex items-center font-medium">
                        <i class="fas fa-external-link-alt mr-1"></i>
                        {link_icon} {link_text}
                    </a>
                    <span class="text-xs text-gray-400">ID: {news['id']}</span>
                </div>
            </div>
            """
        
        html_template = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>真实热点财经新闻榜单 - {self.crawler_name}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body {{ font-family: 'Microsoft YaHei', '微软雅黑', sans-serif; }}
        .gradient-bg {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }}
        .glass-effect {{ backdrop-filter: blur(16px); background: rgba(255, 255, 255, 0.95); }}
        .pulse {{ animation: pulse 2s infinite; }}
        @keyframes pulse {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.8; }} }}
    </style>
</head>
<body class="gradient-bg min-h-screen">
    <div class="container mx-auto px-4 py-8">
        <!-- 头部标题 -->
        <div class="text-center mb-8">
            <h1 class="text-5xl font-bold text-white mb-4">
                <i class="fas fa-satellite-dish mr-3 pulse"></i>真实热点财经新闻
            </h1>
            <p class="text-xl text-blue-100">实时抓取 · 智能评分 · 专业展示</p>
            <div class="mt-4 text-blue-200">
                <i class="fas fa-clock mr-2"></i>抓取时间: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}
                <span class="mx-4">|</span>
                <i class="fas fa-robot mr-2"></i>抓取方式: {self.crawler_name}
            </div>
        </div>
        
        <!-- 状态指示 -->
        <div class="text-center mb-6">
            <div class="inline-flex items-center bg-green-100 text-green-800 px-4 py-2 rounded-full border border-green-200">
                <div class="w-3 h-3 bg-green-500 rounded-full mr-2 pulse"></div>
                <span class="font-semibold">实时抓取系统已激活</span>
            </div>
        </div>
        
        <!-- 统计概览 -->
        <div class="glass-effect rounded-2xl p-6 mb-8 shadow-2xl">
            <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6">
                <div class="text-center">
                    <div class="text-3xl font-bold text-indigo-600">{len(news_list)}</div>
                    <div class="text-gray-600">实时新闻</div>
                </div>
                <div class="text-center">
                    <div class="text-3xl font-bold text-purple-600">{len(categories)}</div>
                    <div class="text-gray-600">新闻类别</div>
                </div>
                <div class="text-center">
                    <div class="text-3xl font-bold text-green-600">{max([n['heat_score'] for n in news_list]):.1f}</div>
                    <div class="text-gray-600">最高热度</div>
                </div>
                <div class="text-center">
                    <div class="text-3xl font-bold text-red-600">{self.crawler_name.split('抓取器')[0]}</div>
                    <div class="text-gray-600">数据来源</div>
                </div>
            </div>
            
            <div>
                <h3 class="text-lg font-semibold text-gray-800 mb-3">📊 实时类别分布</h3>
                <div class="flex flex-wrap">
                    {category_stats}
                </div>
            </div>
        </div>
        
        <!-- 新闻列表 -->
        <div class="glass-effect rounded-2xl p-6 shadow-2xl">
            <h2 class="text-2xl font-bold text-gray-800 mb-6 flex items-center">
                <i class="fas fa-trophy mr-3 text-yellow-500"></i>
                实时热点新闻排行榜
                <span class="ml-3 text-sm text-gray-500 font-normal">基于多维度热度算法实时排序</span>
            </h2>
            
            <div class="space-y-4">
                {news_cards}
            </div>
        </div>
        
        <!-- 底部信息 -->
        <div class="text-center mt-8">
            <div class="inline-flex items-center bg-green-500 text-white px-6 py-3 rounded-full shadow-lg">
                <i class="fas fa-check-circle mr-2"></i>
                真实新闻抓取完成 · 共{len(news_list)}条热点 · 数据实时更新
            </div>
            <div class="mt-4 text-blue-200 text-sm">
                <i class="fas fa-info-circle mr-1"></i>
                本系统采用{self.crawler_name}进行数据抓取，热度评分基于时效性、关键词、标题吸引力和来源权威性综合计算
            </div>
        </div>
    </div>
    
    <script>
        // 添加渐入动画
        document.addEventListener('DOMContentLoaded', function() {{
            const cards = document.querySelectorAll('.bg-white');
            cards.forEach((card, index) => {{
                card.style.opacity = '0';
                card.style.transform = 'translateY(20px)';
                
                setTimeout(() => {{
                    card.style.transition = 'all 0.8s ease-out';
                    card.style.opacity = '1';
                    card.style.transform = 'translateY(0)';
                }}, 150 * index);
            }});
            
            // 添加悬停效果
            cards.forEach(card => {{
                card.addEventListener('mouseenter', function() {{
                    this.style.transform = 'translateY(-5px)';
                }});
                card.addEventListener('mouseleave', function() {{
                    this.style.transform = 'translateY(0)';
                }});
            }});
        }});
    </script>
</body>
</html>"""
        return html_template

def main():
    """主函数"""
    print("🚀 真实新闻展示系统启动")
    print("=" * 50)
    
    # 可以选择不同的抓取器类型
    display_system = RealNewsDisplaySystem(crawler_type="rss")  # 或 "real" 或 "auto"
    result = display_system.crawl_and_display(top_n=10)
    
    print("\n🎯 系统运行总结:")
    print(f"📊 抓取方式: {result['crawler_type']}")
    print(f"📰 抓取新闻: {result['news_count']}条")
    print(f"📄 HTML展示: {result['html_file']}")
    print(f"📁 JSON数据: {result['json_file']}")
    print("\n💡 提示: 在浏览器中打开HTML文件查看专业的真实新闻榜单")

if __name__ == "__main__":
    main()
