from openai import OpenAI

def analyze_content(api_key, api_provider, video_data, transcript, comments, system_prompt, custom_base_url=None, custom_model_name=None):
    
    # 1. 组装用户的输入
    user_content = f"""
    【视频数据】: {video_data}
    【视频文案/字幕】: {transcript}
    【评论区高赞】: {comments}
    
    请根据以上信息，执行拆解。
    """
    
    # 2. 动态路由配置 (万物兼容 OpenAI 协议)
    if api_provider == "DeepSeek (深度求索)":
        client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com/v1")
        model_name = "deepseek-chat"
        
    elif api_provider == "Kimi (月之暗面)":
        client = OpenAI(api_key=api_key, base_url="https://api.moonshot.cn/v1")
        model_name = "moonshot-v1-8k"
        
    elif api_provider == "通义千问 (Qwen)":
        # 阿里千问的 OpenAI 兼容接口
        client = OpenAI(api_key=api_key, base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")
        model_name = "qwen-plus"
        
    elif api_provider == "OpenAI (GPT-4o)":
        # 考虑到国内直连可能会断，允许读取用户填写的代理 URL
        base_url = custom_base_url if custom_base_url else "https://api.openai.com/v1"
        client = OpenAI(api_key=api_key, base_url=base_url) 
        model_name = "gpt-4o"
        
    elif api_provider == "Gemini (Google)":
        # 谷歌最新推出的原生 OpenAI 兼容接口
        client = OpenAI(api_key=api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
        model_name = "gemini-1.5-pro"
        
    elif api_provider == "自定义模型 / Claude中转":
        if not custom_base_url or not custom_model_name:
            raise ValueError("请在左侧侧边栏填入自定义的 Base URL 和 模型名称！")
        client = OpenAI(api_key=api_key, base_url=custom_base_url)
        model_name = custom_model_name
        
    else:
        raise ValueError("未知的模型供应商")

    # 3. 调用大模型
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content