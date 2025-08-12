"""
简化的智能分析模块测试
"""
import sys
import os
sys.path.insert(0, '.')

def test_analysis_module():
    """测试分析模块的基本功能"""
    print("🧠 开始智能分析模块快速测试...")
    
    try:
        from modules.news_analysis.deepseek_client import DeepSeekClient
        print("✅ DeepSeek客户端导入成功")
        
        # 创建客户端实例（使用模拟模式）
        client = DeepSeekClient()
        print("✅ 客户端实例创建成功")
        
        # 测试分析功能
        test_content = "央行宣布降准0.5个百分点，释放流动性约1万亿元"
        print("📊 开始测试分析功能...")
        
        result = client.analyze_news(test_content)
        print("✅ 分析完成")
        print("📄 分析结果预览:")
        print(result[:300] + "...")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_analysis_module()
