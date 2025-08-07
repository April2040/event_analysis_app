"""
DeepSeek AI 客户端模块
提供与DeepSeek API的交互功能
"""
import os
import json
import requests
from typing import Dict, Any, Optional
import time

class DeepSeekClient:
    """DeepSeek AI API客户端"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化DeepSeek客户端
        
        Args:
            api_key: DeepSeek API密钥，如果为None则从环境变量获取
        """
        self.api_key = api_key or os.getenv('DEEPSEEK_API_KEY')
        self.base_url = "https://api.deepseek.com/v1/chat/completions"
        self.session = requests.Session()
        
        if self.api_key:
            self.session.headers.update({
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            })
    
    def get_completion(self, prompt: str, max_tokens: int = 2000, temperature: float = 0.7) -> Dict[str, Any]:
        """
        获取AI完成响应
        
        Args:
            prompt: 输入提示
            max_tokens: 最大token数
            temperature: 温度参数
            
        Returns:
            响应字典
        """
        if not self.api_key:
            return self._get_mock_response(prompt)
        
        try:
            payload = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": max_tokens,
                "temperature": temperature
            }
            
            response = self.session.post(
                self.base_url,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"API请求失败: {response.status_code}")
                return self._get_mock_response(prompt)
                
        except Exception as e:
            print(f"API调用异常: {e}")
            return self._get_mock_response(prompt)
    
    def analyze_news(self, news_content: str, analysis_type: str = "investment") -> str:
        """
        分析新闻内容
        
        Args:
            news_content: 新闻内容
            analysis_type: 分析类型
            
        Returns:
            分析结果
        """
        if analysis_type == "investment":
            prompt = f"""
请对以下财经新闻进行投资分析，从以下角度分析：
1. 市场影响
2. 投资机会
3. 风险评估
4. 建议操作

新闻内容：
{news_content}

请提供专业的投资分析建议。
"""
        else:
            prompt = f"""
请对以下新闻进行分析：
{news_content}

请提供深入的分析见解。
"""
        
        response = self.get_completion(prompt)
        
        if response and 'choices' in response:
            return response['choices'][0]['message']['content']
        else:
            return "分析生成失败，请稍后重试"
    
    def _get_mock_response(self, prompt: str) -> Dict[str, Any]:
        """
        生成模拟响应（用于没有API密钥时的测试）
        
        Args:
            prompt: 输入提示
            
        Returns:
            模拟响应
        """
        mock_analysis = """
【模拟分析结果】

📊 市场影响分析：
- 短期内可能引起相关板块波动
- 政策导向对长期趋势影响较大
- 市场情绪指数维持中性偏谨慎

💰 投资机会识别：
- 关注受益板块的龙头企业
- 价值投资者可关注估值修复机会
- 短线交易者注意技术面配合

⚠️ 风险评估：
- 政策不确定性仍存
- 外部环境变化影响
- 流动性风险需要关注

🎯 操作建议：
- 建议采用分批建仓策略
- 严格控制仓位风险
- 密切关注后续政策动态

*注：这是模拟分析结果，仅供参考*
"""
        
        return {
            "choices": [
                {
                    "message": {
                        "content": mock_analysis
                    }
                }
            ]
        }
