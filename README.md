# BEtube-Analytics-EngineV1.0
Automating YouTube/Bilibili content analysis and localized remodeling via LLM.
# 内容增长引擎 (BEtube Content Analyzer) v1.0

> 一个为出海新媒体团队打造的 AI Native 短视频数据审计与情绪反向工程系统。

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](#) *(这里未来可以换成你的真实公网链接)*

## 💡 项目背景 (Background)

在过往的 B站/YouTube 内容运营经验中，我们发现传统的爆款复盘存在两大痛点：
1. **耗时极长**：运营人员需要手动统计数据、阅读海量评论、提炼字幕，一篇深度复盘耗时往往在 2 小时以上。
2. **缺乏标准**：主观性太强，往往忽略了“高赞评论池”中蕴含的真实受众心理（如：OG养成系自豪感、明星特质代偿等）。

为了打破跨境数据分发的认知错位，我开发了这套**轻量级 AI 内容审计系统**，将复杂的“数据抓取-语料清洗-大模型分析”链路浓缩为一键式的 SaaS 工具。

## 🚀 核心特性 (Core Features)

- **🔗 全自动无头抓取 (Headless Fetching)**
  - 深度集成 `yt-dlp`，仅需一个视频链接，自动提取播放量、点赞数及视频简介。
  - **核心语料清洗**：自动抓取最多 200 条最新/最热评论，并在后台采用**冒泡重排逻辑**，强制清洗出 Top 100 高赞情绪语料，确保大模型输入的纯净度（Garbage In, Garbage Out 防御）。

- **🧠 情绪反向工程与本土化重构 (Sentiment Reverse Engineering)**
  - 内置独家的高级 Prompt 审计模板。
  - 自动输出四大维度报告：【流量漏斗诊断】、【评论区情绪画像提取】、【跨境数据错位风险】、【AI 切片矩阵二创 Hook 提取】。

- **🤖 动态模型路由引擎 (Dynamic Model Routing)**
  - 后端未硬编码任何特定厂商，支持万物兼容的 OpenAI 接口格式。
  - 原生内置对 **DeepSeek (深度求索)**、**Kimi (月之暗面)**、**通义千问**、**GPT-4o** 及 **Gemini** 的多模型一键切换。
  - 开放自定义接口，支持用户填入第三方代理或本地私有化部署模型。

- **🛡️ 绝对的隐私与风控 (Privacy & Security First)**
  - 突破 YouTube 反爬限制，支持用户在前端临时上传 `cookies.txt` 通行证。
  - **并发安全机制**：采用 `UUID` 动态生成临时文件隔离并发冲突，并在数据抓取完毕后瞬间进行物理级 `os.remove` 销毁，绝对不保存用户任何私钥与会话状态。

## 🛠️ 技术栈 (Tech Stack)

- **前端交互**: Streamlit
- **大模型接口**: OpenAI Python SDK 
- **爬虫引擎**: yt-dlp, youtube-transcript-api
- **架构**: Python 3.10+, 纯函数式路由

## 👨‍💻 开发者 (Author)

**Mobiliteee** 
*资深新媒体增长策略师 / AI 内容产品探索者*
*致力于将“好内容的网感”抽象为可复用的“AI 自动化流水线”。
