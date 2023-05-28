import yt_dlp
import sys
def download_mp3(video_url, output_path=""):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            },
            {'key': 'FFmpegMetadata'},
        ],
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("YouTube 동영상 URL을 입력해주세요.")
    else:
        output_path = "." # 여기에 저장할 디렉터리 경로를 입력하세요
        video_url = sys.argv[1]
        download_mp3(video_url, output_path)
