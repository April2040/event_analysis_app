"""
项目主入口 - 模块化版本
"""

import sys
import os

# 添加模块路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

from news_crawler.crawler import NewsWebCrawler
from news_analysis.analyzer import NewsAnalyzer

def main():
    """主程序入口"""
    print("🌟 ===== 财经新闻智能分析系统 v2.0 =====")
    print("📊 模块化架构:")
    print("   1. 新闻爬虫模块 - RSS源抓取与HTML报告")
    print("   2. 智能分析模块 - DeepSeek AI分析与洞察")
    print("")
    
    print("🚀 可用功能:")
    print("1. 仅新闻抓取 (生成新闻列表)")
    print("2. 仅智能分析 (基于已有新闻)")
    print("3. 完整流程 (抓取 + 分析)")
    print("4. 退出")
    print("")
    
    try:
        choice = input("请选择功能 (1-4): ").strip()
        
        if choice == "1":
            run_news_crawler_only()
        elif choice == "2":
            run_analysis_only()
        elif choice == "3":
            run_full_pipeline()
        elif choice == "4":
            print("👋 再见!")
            return
        else:
            print("❌ 无效选择")
            
    except KeyboardInterrupt:
        print("\n\n👋 用户取消操作")
    except Exception as e:
        print(f"❌ 程序执行出错: {e}")

def run_news_crawler_only():
    """仅运行新闻爬虫"""
    print("\n🔥 启动新闻爬虫模块...")
    
    crawler = NewsWebCrawler()
    html_path = crawler.crawl_with_html_option(limit=10)
    
    if html_path:
        print(f"\n✅ 新闻爬虫完成! HTML文件: {html_path}")
    else:
        print("\n✅ 新闻爬虫完成!")

def run_analysis_only():
    """仅运行智能分析"""
    print("\n🧠 启动智能分析模块...")
    print("⚠️ 此功能需要先有新闻数据")
    
    # 先获取新闻数据
    crawler = NewsWebCrawler()
    news_list = crawler.get_top_hotspots(limit=5, use_backup=True)
    
    if not news_list:
        print("❌ 无法获取新闻数据，分析终止")
        return
    
    # 运行分析
    analyzer = NewsAnalyzer()
    analysis_result = analyzer.analyze_news_list(news_list)
    
    if analysis_result:
        html_path = analyzer.generate_analysis_report(analysis_result)
        print(f"\n✅ 智能分析完成! 报告文件: {html_path}")
    else:
        print("\n❌ 智能分析失败")

def run_full_pipeline():
    """运行完整流程"""
    print("\n🎯 启动完整分析流程...")
    
    # Step 1: 新闻爬取
    print("\n📡 第一步: 新闻抓取...")
    crawler = NewsWebCrawler()
    news_list = crawler.get_top_hotspots(limit=10, use_backup=True)
    
    if not news_list:
        print("❌ 新闻抓取失败，流程终止")
        return
    
    # 生成新闻HTML
    news_html = crawler.generate_html_report(news_list)
    print(f"✅ 新闻报告已生成: {news_html}")
    
    # Step 2: 智能分析
    print("\n🧠 第二步: 智能分析...")
    analyzer = NewsAnalyzer()
    analysis_result = analyzer.analyze_news_list(news_list[:5])  # 分析前5条
    
    if analysis_result:
        analysis_html = analyzer.generate_analysis_report(analysis_result)
        print(f"✅ 分析报告已生成: {analysis_html}")
        
        print(f"\n🎉 完整流程完成!")
        print(f"📄 新闻报告: {news_html}")
        print(f"📊 分析报告: {analysis_html}")
    else:
        print("⚠️ 智能分析失败，但新闻抓取成功")

if __name__ == "__main__":
    main()
