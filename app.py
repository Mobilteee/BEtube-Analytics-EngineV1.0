import uuid  # 🌟 新增：用于生成随机文件名
import streamlit as st
from core import analyze_content
from fetch_youtube import fetch_video_info
import os

# --- 1. 页面基本设置 ---
st.set_page_config(page_title="BEtube 分析引擎", page_icon="📈", layout="wide")

st.title("📈 Mobiliteee 视频反向工程引擎 V2.0")
st.markdown("只需一个链接，AI 自动抓取 YouTube/B站 数据并输出商业级爆款拆解报告。")

# --- 2. 初始化 session_state ---
if 'demo_data' not in st.session_state:
    st.session_state['demo_data'] = ""
if 'demo_transcript' not in st.session_state:
    st.session_state['demo_transcript'] = ""
if 'demo_comments' not in st.session_state:
    st.session_state['demo_comments'] = ""

# 加载默认 Prompt 模板
def load_default_prompt():
    try:
        with open('prompts/system_prompt.txt', 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return "你是资深分析师..." # 兜底提示词

# --- 3. 侧边栏：核心控制台 ---
with st.sidebar:
    st.header("⚙️ 引擎配置区")
    
    # 1. 动态大模型选择矩阵
    api_provider = st.selectbox(
        "1. 选择大模型驱动核心", 
        (
            "DeepSeek (深度求索)", 
            "Kimi (月之暗面)", 
            "通义千问 (Qwen)", 
            "OpenAI (GPT-4o)", 
            "Gemini (Google)",
            "自定义模型 / Claude中转"
        )
    )
    
    api_key = st.text_input(f"🔑 输入对应 API Key", type="password")
    
    # 初始化自定义变量
    custom_base_url = None
    custom_model_name = None
    
    # 动态显示自定义输入框
    if api_provider == "自定义模型 / Claude中转":
        st.caption("👇 请填入兼容 OpenAI 格式的中转代理接口")
        custom_base_url = st.text_input("🔗 接口地址 (Base URL)", placeholder="例如: https://api.api2d.com/v1")
        custom_model_name = st.text_input("🤖 模型名称", placeholder="例如: claude-3-5-sonnet-20240620")
    elif api_provider == "OpenAI (GPT-4o)":
        show_proxy = st.checkbox("使用国内反向代理直连 (必勾)")
        if show_proxy:
            custom_base_url = st.text_input("🔗 OpenAI 代理 URL", placeholder="如无需代理请清空", value="https://api.openai.com/v1")

    st.divider()
    
    # 2. Prompt 模板选择
    prompt_mode = st.selectbox("2. 选择拆解分析模板", ["👑 Mobiliteee 独家高级审计模板", "✍️ 自定义上传模板"])
    
    if prompt_mode == "👑 Mobiliteee 独家高级审计模板":
        current_prompt = load_default_prompt()
        st.success("已加载系统默认【情绪反向工程】模板")
    else:
        current_prompt = st.text_area("请在此粘贴你的自定义 Prompt", value="你是一个短视频分析专家，请帮我分析...", height=150)
        
    st.divider()
    st.info("💡 提示：为了防止网页被反爬，YouTube链接建议配合本地 cookies.txt 使用。B站链接可直接抓取基础播放数据。")

# --- 4. 主界面：工作流 ---
col1, col2 = st.columns([1, 1])

# 左半部分：链接抓取与数据展示
with col1:
    st.subheader("📥 第一步：输入数据")
    
    # 🌟 增加文件上传组件
    uploaded_cookie = st.file_uploader("🍪 [选填] 上传你的 YouTube cookies.txt (用于突破反爬)", type=['txt'])
    
    video_url = st.text_input("🔗 粘贴 YouTube 或 Bilibili 视频链接")
    
    if st.button("⚡ 一键抓取链接数据", use_container_width=True):
        if not video_url:
            st.warning("请先粘贴视频链接！")
        else:
            with st.spinner("🤖 正在绕过反爬机制并提取数据，请稍候..."):
                
                # 🌟 处理用户上传的 Cookie 文件
                temp_cookie_path = None
                if uploaded_cookie is not None:
                    unique_id = uuid.uuid4().hex 
                    temp_cookie_path = f"temp_cookies_{unique_id}.txt"
                    with open(temp_cookie_path, "wb") as f:
                        f.write(uploaded_cookie.getbuffer())
                
                # 🌟 把 cookie 路径传给后台抓取函数
                success, d_text, t_text, c_text = fetch_video_info(video_url, temp_cookie_path)
                
                # 抓取完后，安全起见，立刻删掉刚才保存的临时 cookie 文件
                if temp_cookie_path and os.path.exists(temp_cookie_path):
                    os.remove(temp_cookie_path)
                    
                if success:
                    st.session_state['demo_data'] = d_text
                    st.session_state['demo_transcript'] = t_text
                    st.session_state['demo_comments'] = c_text
                    st.success("数据抓取成功！已自动填充至下方。")
                else:
                    st.error(f"抓取失败，请检查链接或确保上传了有效的 cookies.txt。报错: {d_text}")

    # 数据展示区（支持用户二次手动修改）
    video_data = st.text_area("📊 基础数据", value=st.session_state['demo_data'], height=100)
    transcript = st.text_area("📝 视频文案/字幕 (核心必填)", value=st.session_state['demo_transcript'], height=150)
    comments = st.text_area("💬 评论区语料 (用于情绪反推)", value=st.session_state['demo_comments'], height=150)

# 右半部分：生成报告
with col2:
    st.subheader("📤 第二步：生成洞察")
    
    submit_btn = st.button("🚀 启动 AI 极客拆解", type="primary", use_container_width=True)
    
    if submit_btn:
        if not api_key:
            st.error("⚠️ 请先在左侧配置 API Key！")
        elif not transcript:
            st.warning("⚠️ 必须包含视频文案/字幕才能进行拆解！")
        else:
            with st.spinner(f"🧠 {api_provider.split(' ')[0]} 正在执行极客分析，预计 15-20 秒..."):
                try:
                    # 将拿到的各项参数全部传给后端（包括自定义的 URL 和 模型名）
                    result = analyze_content(
                        api_key=api_key, 
                        api_provider=api_provider, 
                        video_data=video_data, 
                        transcript=transcript, 
                        comments=comments, 
                        system_prompt=current_prompt,
                        custom_base_url=custom_base_url,
                        custom_model_name=custom_model_name
                    )
                    st.success("✅ 报告生成完毕！")
                    st.markdown("---")
                    st.markdown(result)
                except Exception as e:
                    st.error(f"API 调用失败: {e}")