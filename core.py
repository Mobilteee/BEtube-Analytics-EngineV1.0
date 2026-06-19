from openai import OpenAI
import json
import re

def analyze_content(api_key, api_provider, video_data, transcript, comments, system_prompt, custom_base_url=None, custom_model_name=None):
    
    user_content = f"【视频数据】: {video_data}\n【视频文案/字幕】: {transcript}\n【评论区高赞】: {comments}\n请根据以上信息，执行拆解。"
    
    # 动态路由配置
    if api_provider == "DeepSeek (深度求索)":
        client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com/v1")
        model_name = "deepseek-chat"
    elif api_provider == "Kimi (月之暗面)":
        client = OpenAI(api_key=api_key, base_url="https://api.moonshot.cn/v1")
        model_name = "moonshot-v1-8k"
    elif api_provider == "通义千问 (Qwen)":
        client = OpenAI(api_key=api_key, base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")
        model_name = "qwen-plus"
    elif api_provider == "OpenAI (GPT-4o)":
        base_url = custom_base_url if custom_base_url else "https://api.openai.com/v1"
        client = OpenAI(api_key=api_key, base_url=base_url) 
        model_name = "gpt-4o"
    elif api_provider == "Gemini (Google)":
        client = OpenAI(api_key=api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
        model_name = "gemini-1.5-pro"
    elif api_provider == "自定义模型 / Claude中转":
        client = OpenAI(api_key=api_key, base_url=custom_base_url)
        model_name = custom_model_name
    else:
        raise ValueError("未知的模型供应商")

    # 调用大模型
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ],
        temperature=0.7
    )
    
    full_response = response.choices[0].message.content
    
    # --- 🌟 核心算法：提取 JSON 与 文字分离 ---
    json_data = None
    text_report = full_response
    
    # 使用正则表达式寻找 ```json ... ``` 块
    json_match = re.search(r'```json\n(.*?)\n```', full_response, re.DOTALL)
    if json_match:
        try:
            json_str = json_match.group(1)
            json_data = json.loads(json_str)
            # 在文字报告中把 JSON 块剔除，保持前端整洁
            text_report = full_response.replace(json_match.group(0), '').strip()
        except Exception as e:
            print(f"JSON 解析失败: {e}")
            
    # 返回：清理后的文字报告, 解析好的 JSON 字典
    return text_report, json_data