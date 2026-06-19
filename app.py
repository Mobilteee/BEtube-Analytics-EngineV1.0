import streamlit as st
from core import analyze_content
from fetch_youtube import fetch_video_info
import os
import uuid
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.set_page_config(page_title="Mobiliteee 视频反向工程引擎", page_icon="📈", layout="wide")
st.title("📈 Mobiliteee 视频反向工程引擎 V2.0")
st.markdown("通过 LLM 动态抽取特征，自动生成情绪雷达图与语料词云的商业级拆解工具。")

# --- 🌟 动态雷达图函数 ---
def draw_dynamic_radar(radar_dict):
    df = pd.DataFrame({
        '情绪维度': radar_dict['dimensions'],
        '匹配指数': radar_dict['scores']
    })
    fig = px.line_polar(df, r='匹配指数', theta='情绪维度', line_close=True, color_discrete_sequence=['#FF4B4B'])
    fig.update_traces(fill='toself', fillcolor='rgba(255, 75, 75, 0.4)')
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False, height=350, margin=dict(l=30, r=30, t=30, b=30))
    return fig

# --- 🌟 动态词云函数 ---
def draw_wordcloud(keyword_dict):
    # ⚠️ 自动寻找系统中文字体，防止中文显示方块
    font_path = "simhei.ttf" if os.path.exists("simhei.ttf") else None
    
    wc = WordCloud(font_path=font_path, width=800, height=400, background_color='white', 
                   colormap='Reds', max_words=30).generate_from_frequencies(keyword_dict)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.imshow(wc, interpolation='bilinear')
    ax.axis('off')
    # 去除多余白边
    plt.tight_layout(pad=0) 
    return fig

# --- 初始化与侧边栏 ---
if 'demo_data' not in st.session_state: st.session_state.update({'demo_data': '', 'demo_transcript': '', 'demo_comments': ''})

def load_default_prompt():
    try:
        with open('prompts/system_prompt.txt', 'r', encoding='utf-8') as f: return f.read()
    except:
        return "请分析以下内容..."

with st.sidebar:
    st.header("⚙️ 引擎配置区")
    
    # 🌟 体验降级：一键看Demo按钮
    if st.button("🎁 一键查看精美示例报告 (免 API Key)", type="primary"):
        st.session_state['show_demo'] = True
    else:
        st.session_state['show_demo'] = st.session_state.get('show_demo', False)
        
    st.divider()
    
    api_provider = st.selectbox("1. 选择大模型驱动核心", ("DeepSeek (深度求索)", "Kimi (月之暗面)", "通义千问 (Qwen)", "OpenAI (GPT-4o)", "Gemini (Google)", "自定义模型 / Claude中转"))
    api_key = st.text_input(f"🔑 输入对应 API Key", type="password")
    
    custom_base_url, custom_model_name = None, None
    if api_provider == "自定义模型 / Claude中转":
        custom_base_url, custom_model_name = st.text_input("🔗 接口地址"), st.text_input("🤖 模型名称")
    elif api_provider == "OpenAI (GPT-4o)":
        if st.checkbox("使用国内反向代理直连"):
            custom_base_url = st.text_input("🔗 OpenAI 代理 URL", value="https://api.openai.com/v1")

    prompt_mode = st.selectbox("2. 选择拆解分析模板", ["👑 Mobiliteee 独家高级审计模板", "✍️ 自定义上传模板"])
    current_prompt = load_default_prompt() if prompt_mode == "👑 Mobiliteee 独家高级审计模板" else st.text_area("请粘贴自定义 Prompt", height=150)

    st.divider()
    st.info("💡 提示：为了防止被反爬，YouTube链接建议配合本地 cookies.txt 使用。B站链接可直接抓取基础播放数据。")

# --- 主界面 ---
col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("📥 第一步：输入数据")
    uploaded_cookie = st.file_uploader("🍪 [选填] 上传目标网站 cookies.txt (用于破反爬)", type=['txt'])
    video_url = st.text_input("🔗 粘贴 YouTube / Bilibili 视频链接")
    
    if st.button("⚡ 抓取链接数据", use_container_width=True):
        if video_url:
            with st.spinner("🤖 正在突破风控并清洗高赞语料..."):
                temp_cookie_path = f"temp_{uuid.uuid4().hex}.txt" if uploaded_cookie else None
                if temp_cookie_path:
                    with open(temp_cookie_path, "wb") as f: f.write(uploaded_cookie.getbuffer())
                success, d_text, t_text, c_text = fetch_video_info(video_url, temp_cookie_path)
                if temp_cookie_path and os.path.exists(temp_cookie_path): os.remove(temp_cookie_path)
                if success:
                    st.session_state.update({'demo_data': d_text, 'demo_transcript': t_text, 'demo_comments': c_text})
                    st.success("数据抓取与清洗成功！")
                else: st.error("抓取失败，请检查链接或网络。")

    video_data = st.text_area("📊 基础数据", value=st.session_state['demo_data'], height=100)
    transcript = st.text_area("📝 视频文案/字幕 (核心必填)", value=st.session_state['demo_transcript'], height=150)
    comments = st.text_area("💬 Top 高赞语料库 (算法重排)", value=st.session_state['demo_comments'], height=150)

with col2:
    st.subheader("📤 第二步：动态可视化分析")
    
    # 🌟 核心：展示免密 Demo 逻辑
    if st.session_state.get('show_demo'):
        
        # --- 🌟 新增：头部栏与关闭按钮 ---
        head_c1, head_c2 = st.columns([8, 2])
        with head_c1:
            st.success("✅ 示例报告已加载 (分析源：Bilibili《铁拳教育》P1 解说)")
        with head_c2:
            if st.button("❌ 关掉示例", use_container_width=True):
                st.session_state['show_demo'] = False
                st.rerun()  # 瞬间刷新网页状态，清空Demo
        
        # 构建 Demo 专用的可视化数据
        demo_radar = {
            "dimensions": ["爽感冲击力", "社会议题共鸣", "主角人设魅力", "叙事节奏掌控", "本土化改编潜力"],
            "scores": [95, 90, 85, 80, 95]
        }
        demo_words = {
            "爽": 100, "霸凌": 90, "羡慕": 80, "铁拳教育": 75, "马东锡": 70, 
            "老师": 65, "以暴制暴": 60, "无力感": 55, "反抗": 50, "保护": 45,
            "现实": 40, "规矩": 35, "酸了": 30, "正义": 25, "幻想": 20
        }
        
        # --- 🌟 新增：左右大屏看板布局 ---
        demo_left, demo_right = st.columns([1, 1.2])
        
        with demo_left:
            # 左侧：渲染 Demo 图表
            tab1, tab2 = st.tabs(["🎯 情绪多边形雷达", "☁️ 受众语料词云"])
            with tab1:
                st.plotly_chart(draw_dynamic_radar(demo_radar), use_container_width=True)
            with tab2:
                st.pyplot(draw_wordcloud(demo_words))
                
        with demo_right:
            # 右侧：渲染 Demo 文字报告 (🌟 加入高度为 450px 的滚动容器)
            with st.container(height=450):
                st.markdown("""
### 📊 01 核心算法指标与长视频留存诊断 (Algorithm & Retention Audit)
- **流量漏斗分析**：该视频播放量（494万）与点赞数（10.1万）形成的点赞率约为2.04%，这在长视频生态中属于中等偏上水平，说明内容成功触达了核心爽剧受众。然而，207条评论与494万播放量形成的互动率（0.004%）极低。这种“高播放、高点赞、低评论”的漏斗形态，通常意味着流量主要来源于推荐流的被动分发，缺乏引发观众“必须说点什么”的强争议点。
- **长视频前置护城河 (First 30s Hook)**：开篇以“杀人后抛尸的完美地点——校园”为Hook，瞬间制造了强悬念和猎奇感。但随后迅速进入了对原漫画、剧集背景的科普，对于纯粹追求“爽感”的泛娱乐用户来说，可能导致部分不耐受的观众跳出。
- **高能时间戳预测 (AVD Boosters)**：
  - **03:20 - 04:10**：新老师登场，一巴掌扇飞校霸。这是全片第一个情绪爆发点，AVD必然在此处拉升。
  - **18:30 - 20:00**：罗华镇以近乎“审判”的方式惩罚黑化后的校霸，这是全片最极致、最具争议性的爽点。

### 🧠 02 评论区情绪反向工程 (Sentiment Reverse Engineering)
- **模型 C：技术流共鸣创作欲（主导）**：评论区大量用户聚焦于“爽感”本身，如“前段讲霸凌后段解决，真的太爽了”，表明受众在主动识别“爽剧”的叙事节奏。
- **模型 B：明星气质的精神寄托（辅助）**：部分评论将主角与马东锡等韩国顶流演员进行类比，表明主角形象成功承载了观众对“理想守护者”的精神投射。
- **受众画像与核心痛点**：主要为18-35岁泛娱乐用户，核心痛点是对现实社会中“正义无法伸张”的深层无力感。他们需要的不是说教，而是一场酣畅淋漓、突破规则的“正义幻想”。

### ⚠️ 03 跨境数据错位风险 (Cross-border Risk)
- **本土化冷启动陷阱**：国内用户对“教权保护局”等核心设定缺乏前置认知。直接打上“韩剧”标签，容易被算法判定为“小众圈层内容”，难以突破至大众流量池。

### 🔄 04 AI Native 矩阵分发与切片重构 (Matrix & Shorts Pivot)
- **切片矩阵“黄金 3 秒”提取**：切片前置应直接展示极具视觉冲击力的“打脸”慢镜头，配文：“别跟我说什么未成年保护法，今天教教你什么叫铁拳教育！” 这种“去符号化”的Hook，能瞬间抓住对“霸凌”话题有共鸣的泛人群。
- **本土爆款标题重构**：
  1. 【社会学议题型】：“当老师拥有‘无限开火权’：校园霸凌的终极解法，是让正义比拳头更硬！” 
  2. 【强冲突型】：“全网最硬核的老师：校长不管？我管！这剧看得我乳腺都通了！” 
- **AIGC 放大策略**：“AI 换脸 + 本土化二创”。使用 AI 工具将主角的脸替换为国内观众更熟悉的“硬汉”演员（如吴京、张译），重新混剪短片。这种操作能最大程度消除“韩剧”带来的隔阂感，利用本土演员的国民度实现流量“洗白”。
                """)
        
    else:
        submit_btn = st.button("🚀 启动 AI 极客拆解", type="primary", use_container_width=True)
        if submit_btn:
            if not api_key or not transcript:
                st.warning("⚠️ 请输入 API Key 及视频文案！")
            else:
                with st.spinner(f"🧠 模型正在提取特征并绘制可视化矩阵，预计 15-20 秒..."):
                    try:
                        text_report, json_data = analyze_content(api_key, api_provider, video_data, transcript, comments, current_prompt, custom_base_url, custom_model_name)
                        st.success("✅ 报告生成完毕！")
                        
                        if json_data:
                            # 真实调用也采用左右分栏大屏设计
                            res_left, res_right = st.columns([1, 1.2])
                            with res_left:
                                tab1, tab2 = st.tabs(["🎯 情绪多边形雷达", "☁️ 受众语料词云"])
                                with tab1:
                                    if "radar_chart" in json_data:
                                        st.plotly_chart(draw_dynamic_radar(json_data["radar_chart"]), use_container_width=True)
                                with tab2:
                                    if "word_cloud" in json_data:
                                        st.pyplot(draw_wordcloud(json_data["word_cloud"]["keywords"]))
                            with res_right:
                                # 右侧分析报告加滚动条
                                with st.container(height=450):
                                    st.markdown(text_report)
                        else:
                            st.warning("大模型未按严格格式返回 JSON，图表渲染失败，仅展示文本。")
                            st.markdown(text_report)
                            
                    except Exception as e:
                        st.error(f"分析失败: {e}")