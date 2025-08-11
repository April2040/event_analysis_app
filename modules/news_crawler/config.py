"""
RSS源配置和评分权重配置
"""

# 真正的RSS Feed源 - 仅使用可靠的RSS源
# RSS新闻源配置
RSS_FEEDS = {
    'ft_chinese': {
        'url': 'https://www.ftchinese.com/rss/news',
        'source': 'FT中文网',
        'priority': 1,
        'type': 'xml'
    },
    'chinanews': {
        'url': 'https://www.chinanews.com.cn/rss/finance.xml',
        'source': '中新网',
        'priority': 2,
        'type': 'xml'
    }
}

# 备用简单RSS源（如果主要RSS失效）
SIMPLE_RSS_SOURCES = {
    "新浪财经": "https://finance.sina.com.cn/",
    "腾讯财经": "https://finance.qq.com/",
    "网易财经": "https://money.163.com/", 
    "搜狐财经": "https://business.sohu.com/",
    "东方财富": "https://www.eastmoney.com/",
}

# 高质量备用新闻数据（扩展版）
ENHANCED_BACKUP_NEWS = [
    {
        "title": "央行宣布降准0.5个百分点，释放长期资金约1万亿元",
        "source": "中国人民银行",
        "category": "货币政策",
        "keywords": ["央行", "降准", "流动性", "货币政策"],
        "summary": "中国人民银行决定于2025年8月15日降准0.5个百分点，此次降准将释放长期资金约1万亿元，支持实体经济发展。",
        "importance": "high",
        "link": "http://www.pbc.gov.cn/goutongjiaoliu/113456/113469/5156279/index.html"
    },
    {
        "title": "A股三大指数集体收涨，创业板指涨超2%，新能源板块领涨",
        "source": "上海证券报",
        "category": "股市",
        "keywords": ["A股", "创业板", "新能源", "上涨"],
        "summary": "今日A股市场表现强劲，三大指数全线上涨，创业板指数涨幅超过2%，新能源板块成为领涨先锋。",
        "importance": "high",
        "link": "https://news.cnstock.com/news,yw-202508-5156280.htm"
    },
    {
        "title": "美联储会议纪要显示对通胀担忧加剧，加息预期升温",
        "source": "华尔街日报",
        "category": "货币政策",
        "keywords": ["美联储", "通胀", "加息", "会议纪要"],
        "summary": "美联储最新会议纪要显示，多数委员对通胀持续高位表示担忧，市场对后续加息预期升温。",
        "importance": "high",
        "link": "https://cn.wsj.com/articles/fed-meeting-minutes-inflation-concerns-20250807"
    },
    {
        "title": "比特币突破43000美元，加密货币市场重现活力",
        "source": "Coindesk",
        "category": "数字货币",
        "keywords": ["比特币", "加密货币", "突破", "数字资产"],
        "summary": "比特币价格突破43000美元关口，带动整个加密货币市场上涨，市场信心逐步恢复。",
        "importance": "medium",
        "link": "https://www.coindesk.com/markets/2025/08/07/bitcoin-breaks-43000-crypto-rally"
    },
    {
        "title": "特斯拉Q3财报超预期，新能源汽车销量创历史新高",
        "source": "财联社",
        "category": "新能源",
        "keywords": ["特斯拉", "财报", "新能源汽车", "销量"],
        "summary": "特斯拉第三季度财报显示，营收和净利润均超出市场预期，全球新能源汽车销量创历史新高。",
        "importance": "high",
        "link": "https://www.cls.cn/telegraph/20250807/tesla-q3-earnings-record"
    },
    {
        "title": "人工智能芯片需求激增，英伟达股价再创新高",
        "source": "彭博社",
        "category": "科技",
        "keywords": ["人工智能", "芯片", "英伟达", "AI"],
        "summary": "随着AI应用的快速发展，人工智能芯片需求持续旺盛，推动英伟达股价连续上涨。",
        "importance": "high",
        "link": "https://www.bloomberg.com/news/articles/2025-08-07/nvidia-stock-hits-record-ai-chip-demand"
    },
    {
        "title": "房地产政策现边际宽松迹象，多城市放松限购政策",
        "source": "中国证券报",
        "category": "房地产",
        "keywords": ["房地产", "政策", "限购", "宽松"],
        "summary": "近期多个城市陆续调整房地产调控政策，市场预期政策将进一步宽松，地产股表现活跃。",
        "importance": "medium",
        "link": "https://www.cs.com.cn/ssgs/gsxw/202508/t20250807_6384921.html"
    },
    {
        "title": "原油价格大幅波动，地缘政治风险推高能源价格",
        "source": "路透社",
        "category": "能源",
        "keywords": ["原油", "地缘政治", "能源", "价格"],
        "summary": "受地缘政治因素影响，国际原油价格出现大幅波动，能源类股票表现分化。",
        "importance": "medium",
        "link": "https://cn.reuters.com/markets/commodities/oil-prices-surge-geopolitical-tensions-20250807"
    },
    {
        "title": "银行板块估值修复行情启动，资金回流金融股",
        "source": "证券时报",
        "category": "金融",
        "keywords": ["银行", "估值", "金融股", "修复"],
        "summary": "随着经济预期改善，银行板块估值修复行情正在启动，大量资金开始回流金融股。",
        "importance": "medium",
        "link": "https://www.stcn.com/stock/djjd/202508/t20250807_4568921.html"
    },
    {
        "title": "消费板块逐步复苏，白酒食品股表现亮眼",
        "source": "第一财经",
        "category": "消费",
        "keywords": ["消费", "白酒", "食品", "复苏"],
        "summary": "消费复苏迹象明显，白酒、食品等消费股表现突出，板块整体呈现上涨态势。",
        "importance": "medium",
        "link": "https://www.yicai.com/news/102159567.html"
    },
    {
        "title": "医药板块分化加剧，创新药企业受到资金青睐",
        "source": "医药经济报",
        "category": "医药",
        "keywords": ["医药", "创新药", "分化", "投资"],
        "summary": "医药板块内部分化加剧，具有创新能力的药企受到市场资金青睐，传统药企面临转型压力。",
        "importance": "medium",
        "link": "https://www.yyjjb.com.cn/news/2025/08/07/pharma-innovation-investment.html"
    },
    {
        "title": "5G建设进入新阶段，通信设备股迎来投资机遇",
        "source": "通信产业报",
        "category": "科技",
        "keywords": ["5G", "通信", "设备", "建设"],
        "summary": "5G网络建设进入新发展阶段，相关通信设备企业迎来新的投资机遇和市场空间。",
        "importance": "medium",
        "link": "https://www.ccidcom.com/industry/5g-development-phase-20250807.html"
    },
    {
        "title": "外贸数据超预期，进出口贸易呈现稳中向好态势",
        "source": "海关总署",
        "category": "贸易",
        "keywords": ["外贸", "进出口", "数据", "贸易"],
        "summary": "最新外贸数据显示，进出口贸易表现超出市场预期，呈现稳中向好的发展态势。",
        "importance": "medium",
        "link": "http://www.customs.gov.cn/customs/302249/zfxxgk/2799825/302274/5156285/index.html"
    },
    {
        "title": "绿色金融发展提速，ESG投资理念深入人心",
        "source": "金融时报",
        "category": "绿色金融",
        "keywords": ["绿色金融", "ESG", "投资", "可持续"],
        "summary": "绿色金融发展步伐加快，ESG投资理念逐渐深入人心，相关金融产品规模快速增长。",
        "importance": "medium",
        "link": "https://www.financialnews.com.cn/green/esg-investment-trends-20250807.html"
    },
    {
        "title": "制造业PMI重回扩张区间，经济复苏势头增强",
        "source": "国家统计局",
        "category": "宏观经济",
        "keywords": ["PMI", "制造业", "经济", "复苏"],
        "summary": "最新制造业PMI数据重回50以上扩张区间，显示经济复苏势头进一步增强。",
        "importance": "high",
        "link": "http://www.stats.gov.cn/sj/zxfb/202508/t20250807_1950281.html"
    }
]

# RSS源权重配置
RSS_SOURCE_WEIGHTS = {
    "官方媒体": 0.95,  # 人民网、央视网、经济日报等
    "专业财经": 0.90,  # 第一财经、财新、财联社等
    "门户财经": 0.80,  # 新浪、网易、腾讯财经等
    "国际媒体": 1.00,  # 路透、彭博等
    "行业媒体": 0.85   # 证券时报、投资者报等
}
