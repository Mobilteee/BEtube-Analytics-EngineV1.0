# BEtube-Analytics-EngineV1.0
Automating YouTube/Bilibili content analysis and localized remodeling via LLM.
# 📈 Mobiliteee 内容增长引擎 (BEtube Content Analyzer) v2.0

> 一个为出海新媒体团队打造的 AI Native 短视频数据审计与情绪反向工程系统。

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](#)
 https://betube-analytics-engine.streamlit.app/
## 💡 项目背景 (Background)

在过往的 B站/YouTube 内容运营实践中，我发现传统的爆款复盘存在两大痛点：
1. **耗时极长**：运营人员需要手动统计数据、阅读海量评论、提炼字幕，一篇深度复盘耗时往往在 2 小时以上。
2. **缺乏标准**：人工复盘主观性较强，容易忽略“高赞评论池”中蕴含的受众真实心理（如：OG养成系自豪感、明星特质代偿等核心痛点）。

为了打破这种效率瓶颈与认知错位，我开发了这套**轻量级 AI 内容审计系统**，将复杂的“数据抓取-语料清洗-大模型分析”链路浓缩为一键式的 SaaS 工具。

## 🚀 核心特性 (Core Features)

- **🔗 全自动无头抓取 (Headless Fetching)**
  - 深度集成 `yt-dlp`，仅需一个视频链接，自动提取播放量、点赞数及视频简介。
  - **核心语料清洗**：自动抓取最多 200 条最新/最热评论，并在后台采用冒泡重排逻辑，强制清洗出 Top 100 高赞情绪语料，从源头切断 LLM 的 Garbage In 缺陷。

- **🧠 情绪反向工程与本土化重构 (Sentiment Reverse Engineering)**
  - 内置独家的高级 Prompt 审计模板，自动生成多维度商业报告。
  - **可视化呈现**：基于 Plotly 动态生成受众情绪分布雷达图，直观洞察用户共鸣点。

- **🤖 动态模型路由引擎 (Dynamic Model Routing)**
  - 后端架构兼容所有 OpenAI API 格式。原生支持一键切换 DeepSeek、Kimi、通义千问等国内高性价比模型，及 GPT-4o、Gemini 等海外生态，并开放自定义代理接口。

- **🛡️ 隐私风控设计 (Privacy & Security)**
  - 突破反爬限制，支持前台动态注入临时 `cookies` 通行证。
  - 采用 `UUID` 隔离并发访问，并在抓取完成后执行物理级销毁 (`os.remove`)，零信任架构保障用户私钥安全。

## 🛠️ 技术栈 (Tech Stack)
- **Frontend**: Streamlit, Plotly (数据可视化)
- **Backend**: Python 3.10, OpenAI Python SDK
- **Crawler**: yt-dlp, youtube-transcript-api

## 👨‍💻 关于作者 (About)
**Mobiliteee** 
`AI 内容工具独立开发者` | `新媒体运营实践者`
- 致力于将“好内容的网感”与“受众心理学”抽象为可复用的 AI 自动化工作流。
