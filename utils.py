# utils.py
from openai import OpenAI
import os
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

def call_llm(user_input: str, system_prompt: str, model="deepseek-chat") -> str:
    print(f"开始处理LLM请求，模型: {model}")
    
    # 检查API密钥
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        print("❌ API密钥未设置")
        return "❌ 错误：请设置 DEEPSEEK_API_KEY 环境变量。\n\n请在 .env 文件中添加：\nDEEPSEEK_API_KEY=你的DeepSeek API密钥"
    
    print("✅ API密钥已设置，开始调用DeepSeek API...")
    
    try:
        # 配置 DeepSeek API
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com/v1"
        )
        
        print("🚀 正在发送请求到DeepSeek...")
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7
        )
        
        result = response.choices[0].message.content
        print(f"✅ API调用成功，返回内容长度: {len(result)} 字符")
        return result
    
    except Exception as e:
        error_msg = f"❌ API调用错误：{str(e)}"
        print(error_msg)
        return f"{error_msg}\n\n请检查：\n1. DEEPSEEK_API_KEY 是否正确设置\n2. 网络连接是否正常\n3. API密钥是否有效\n4. 是否有足够的API配额"
