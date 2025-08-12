# config.py
"""新闻抓取器配置文件"""

# 新闻源配置
NEWS_SOURCES = {
    "domestic": [
        {
            "name": "第一财经",
            "url": "https://www.yicai.com/",
            "weight": 0.9,
            "selectors": {
                "title": ".m-news-list .f-arial .black",
                "link": ".m-news-list a",
                "time": ".time",
                "summary": ".m-news-list .gray"
            }
        },
        {
            "name": "财新网",
            "url": "https://www.caixin.com/",
            "weight": 0.95,
            "selectors": {
                "title": ".news_item h3",
                "link": ".news_item a",
                "time": ".time",
                "summary": ".news_item .desc"
            }
        },
        {
            "name": "财联社",
            "url": "https://www.cls.cn/",
            "weight": 0.85,
            "selectors": {
                "title": ".telegraph-list .title",
                "link": ".telegraph-list a",
                "time": ".time",
                "summary": ".content"
            }
        },
        {
            "name": "新华财经",
            "url": "http://www.xinhua08.com/",
            "weight": 0.88,
            "selectors": {
                "title": ".content h3",
                "link": ".content a",
                "time": ".time",
                "summary": ".desc"
            }
        },
        {
            "name": "中新经纬",
            "url": "https://www.jwview.com/",
            "weight": 0.82,
            "selectors": {
                "title": ".news-list .title",
                "link": ".news-list a",
                "time": ".time",
                "summary": ".abstract"
            }
        }
    ],
    "international": [
        {
            "name": "彭博社中文",
            "url": "https://www.bloomberg.com/asia",
            "weight": 1.0,
            "selectors": {
                "title": ".story-package-module__story-headline",
                "link": ".story-package-module__story a",
                "time": ".timestamp",
                "summary": ".summary"
            }
        },
        {
            "name": "路透中文",
            "url": "https://cn.reuters.com/",
            "weight": 1.0,
            "selectors": {
                "title": ".story-title",
                "link": ".story a",
                "time": ".timestamp",
                "summary": ".summary"
            }
        }
    ]
}

# 热度计算权重配置
HEAT_WEIGHTS = {
    "time_factor": 0.3,      # 时效性权重
    "keyword_factor": 0.25,  # 关键词权重
    "title_factor": 0.2,     # 标题吸引力权重
    "source_factor": 0.25    # 来源权威性权重
}

# 财经关键词配置
FINANCIAL_KEYWORDS = {
    "high_impact": {  # 高影响力关键词 (权重4-5)
        "市场类": ["股市", "股灾", "牛市", "熊市", "涨停", "跌停", "暴涨", "暴跌", "熔断"],
        "政策类": ["央行", "货币政策", "降息", "加息", "降准", "QE", "量化宽松"],
        "经济类": ["GDP", "通胀", "通缩", "CPI", "PPI", "失业率", "贸易战", "制裁"],
        "机构类": ["美联储", "欧央行", "人民银行", "证监会", "银保监会"],
        "科技类": ["比特币", "数字货币", "区块链", "人工智能", "AI", "芯片", "半导体"]
    },
    "medium_impact": {  # 中等影响力关键词 (权重2-3)
        "行业类": ["房地产", "地产", "楼市", "新能源", "汽车", "医药", "消费"],
        "金融类": ["银行", "保险", "券商", "基金", "信托", "P2P", "理财"],
        "投资类": ["IPO", "并购", "重组", "退市", "分红", "配股", "增发"],
        "数据类": ["财报", "业绩", "营收", "利润", "亏损", "净利", "毛利"]
    },
    "low_impact": {   # 低影响力关键词 (权重1)
        "一般类": ["企业", "公司", "发布", "公告", "声明", "报告", "分析"]
    }
}

# 新闻源权威性评分
SOURCE_AUTHORITY = {
    "彭博社": 100, "Bloomberg": 100,
    "路透社": 100, "Reuters": 100,
    "华尔街日报": 95, "Wall Street Journal": 95,
    "金融时报": 95, "Financial Times": 95,
    "财新": 90, "财新网": 90,
    "第一财经": 88,
    "财联社": 85,
    "新华财经": 85,
    "中新经纬": 80,
    "每日经济新闻": 78,
    "证券时报": 78,
    "21世纪经济报道": 75,
    "经济观察报": 70,
    "CNBC": 85,
    "MarketWatch": 80,
    "雅虎财经": 70,
    "Yahoo Finance": 70
}

# 抓取配置
CRAWLER_CONFIG = {
    "max_items_per_source": 20,
    "request_timeout": 10,
    "request_delay": 1,  # 请求间隔(秒)
    "max_retries": 3,
    "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# 文件保存配置
FILE_CONFIG = {
    "output_dir": "news_data",
    "filename_format": "hotspot_news_{timestamp}.json",
    "backup_days": 7  # 保留7天的历史数据
}
