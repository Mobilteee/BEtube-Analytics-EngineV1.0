import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi
import os # 确保顶部导入了 os

# 🌟 新增了一个参数 cookie_path，默认为 None
def fetch_video_info(url, cookie_path=None):
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'extract_flat': False,
        'getcomments': True,
        'extractor_args': {'youtube': ['comment_sort=top', 'max-comments=200']},
        'ignore_no_formats_error': True,
        'no_warnings': True
    }
    
    # 🌟 动态判断：如果传了 cookie_path 且文件存在，才带上 cookie 配置
    if cookie_path and os.path.exists(cookie_path):
        ydl_opts['cookiefile'] = cookie_path

    data_text = ""
    comments_text = ""
    transcript_text = ""


    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
        video_id = info.get('id')
        views = info.get('view_count', 0)
        likes = info.get('like_count', 0)
        comment_count = info.get('comment_count', 0)
        description = info.get('description', '')
        
        data_text = f"【基础数据】\n播放量：{views}次\n点赞数：{likes}\n评论总数：{comment_count}条\n\n【视频简介】\n{description}"
        
        # --- 🌟 核心数据清洗区：强制按点赞数重排 ---
        comments_list = info.get('comments', [])
        
        # 优化点 2：无论平台怎么乱序，我们在本地强制按 like_count 从大到小降序排列
        sorted_comments = sorted(comments_list, key=lambda x: x.get('like_count', 0) if x.get('like_count') else 0, reverse=True)
        
        # 优化点 3：精准截取排名前 100 条最精华的评论
        for i, c in enumerate(sorted_comments[:100]):
            text = c.get('text', '').replace('\n', ' ')
            like_count = c.get('like_count', 0)
            if like_count is None:  # 防止有些平台抓不到赞数报错
                like_count = 0
            comments_text += f"{i+1}. [👍赞: {like_count}] {text}\n"
            
        # 尝试获取字幕 (主要针对YouTube)
        if "youtube.com" in url or "youtu.be" in url:
            try:
                transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'zh-Hans', 'zh-Hant', 'ko', 'ja'])
                transcript_text = "\n".join([t['text'] for t in transcript_list])
            except Exception as e:
                transcript_text = f"未找到官方自动字幕。建议将本地生成的SRT转文本后粘贴至此。\n错误参考: {str(e)}"
        else:
            transcript_text = "检测到非 YouTube 链接。请手动粘贴视频文案/听译文本。"

        return True, data_text, transcript_text, comments_text

    except Exception as e:
        return False, str(e), "", ""