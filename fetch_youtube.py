import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi
import os
import re
import requests

def fetch_video_info(url, cookie_path=None):
    data_text = ""
    comments_text = ""
    transcript_text = ""
    valid_comments = []

    # 伪装成真实的电脑浏览器
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://www.bilibili.com'
    }

    try:
        # --- 🌟 路线 1：如果是 B 站，彻底抛弃 yt-dlp，全盘接管官方 API ---
        if "bilibili.com" in url or "b23.tv" in url:
            bvid_match = re.search(r'(BV[a-zA-Z0-9]+)', url)
            if not bvid_match:
                return False, "未能识别到有效的 Bilibili BV号", "", ""
            
            bvid = bvid_match.group(1)
            
            # 1. 劫持 B站基础数据接口
            info_res = requests.get(f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}", headers=headers).json()
            if info_res.get('code') != 0:
                return False, f"B站API请求失败: {info_res.get('message')}", "", ""
                
            data = info_res['data']
            aid = data['aid']
            views = data['stat']['view']
            likes = data['stat']['like']
            comment_count = data['stat']['reply']
            description = data['desc']
            
            data_text = f"【基础数据】\n播放量：{views}次\n点赞数：{likes}\n评论总数：{comment_count}条\n\n【视频简介】\n{description}"
            transcript_text = "B站视频暂不支持自动抓取字幕，请手动粘贴文案/听译文本。"

            # 2. 劫持 B站真实热评接口
            reply_res = requests.get(f"https://api.bilibili.com/x/v2/reply/main?next=1&type=1&oid={aid}&mode=3", headers=headers).json()
            if reply_res.get('code') == 0 and reply_res.get('data', {}).get('replies'):
                for r in reply_res['data']['replies']:
                    text = r['content']['message'].replace('\n', ' ').strip()
                    like_count = r['like']
                    
                    # NLP 降噪滤网
                    if "回复 @" not in text and "回复@" not in text and len(text) >= 5:
                        valid_comments.append({'text': text, 'likes': like_count})

        # --- 🌟 路线 2：如果是 YouTube，继续使用 yt-dlp 抓取 ---
        else:
            ydl_opts = {
                'quiet': True,
                'skip_download': True,
                'extract_flat': False,
                'getcomments': True,
                'extractor_args': {'youtube': ['comment_sort=top', 'max-comments=300']},
                'ignore_no_formats_error': True,
                'no_warnings': True
            }
            if cookie_path and os.path.exists(cookie_path):
                ydl_opts['cookiefile'] = cookie_path

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
            video_id = info.get('id')
            views = info.get('view_count', 0)
            likes = info.get('like_count', 0)
            comment_count = info.get('comment_count', 0)
            description = info.get('description', '')
            
            data_text = f"【基础数据】\n播放量：{views}次\n点赞数：{likes}\n评论总数：{comment_count}条\n\n【视频简介】\n{description}"
            
            comments_list = info.get('comments', [])
            for c in comments_list:
                text = c.get('text', '').replace('\n', ' ').strip()
                like_count = c.get('like_count')
                try:
                    like_count = int(like_count) if like_count is not None else 0
                except:
                    like_count = 0
                    
                if text and "回复 @" not in text and "回复@" not in text and len(text) >= 5:
                    valid_comments.append({'text': text, 'likes': like_count})

            # 获取 YouTube 字幕
            try:
                transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'zh-Hans', 'zh-Hant', 'ko', 'ja'])
                transcript_text = "\n".join([t['text'] for t in transcript_list])
            except Exception as e:
                transcript_text = f"未找到官方自动字幕。建议将本地生成的SRT转文本后粘贴至此。\n错误参考: {str(e)}"

        # --- 🏁 终点会师：统一降序排列与输出 ---
        valid_comments.sort(key=lambda x: x['likes'], reverse=True)
        for i, c in enumerate(valid_comments[:100]):
            comments_text += f"{i+1}. [👍赞: {c['likes']}] {c['text']}\n"
            
        return True, data_text, transcript_text, comments_text

    except Exception as e:
        return False, str(e), "", ""