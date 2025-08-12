"""
智能新闻分析模块初始化文件
"""

from .analyzer import NewsAnalyzer
from .deepseek_client import DeepSeekClient
from .report_generator import AnalysisReportGenerator
from .prompts import get_analysis_prompt, get_summary_prompt, get_investment_analysis_prompt

__all__ = [
    'NewsAnalyzer',
    'DeepSeekClient',
    'AnalysisReportGenerator',
    'get_analysis_prompt',
    'get_summary_prompt', 
    'get_investment_analysis_prompt'
]
