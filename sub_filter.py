import re
import subprocess
import sys

def process_vtt_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        vtt_content = file.read()

    # 자막 블록을 추출하는 정규 표현식 패턴
    subtitle_pattern = r'\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}([\s\S]*?)\n([\s\S]*?)\n([\s\S]*?)\n'

    subtitles = re.findall(subtitle_pattern, vtt_content)

    cleaned_subtitles = []

    for subtitle_tuple in subtitles:
        if len(subtitle_tuple[2]) >= 0:
            if len(subtitle_tuple[2].strip()) == 0:
                subtitle = subtitle_tuple[1]  # 튜플에서 자막을 추출합니다.
                cleaned_subtitles.append(subtitle.strip())
        else:
            continue
        # <.*?>를 빈 문자열로 대체하여 제거
        # cleaned_subtitle = re.sub(r'<.*?>', '', subtitle)
        # print(cleaned_subtitle)
        # align:start position:0% 문자 제거
        # cleaned_subtitle = subtitle.replace("align:start position:0%", "").strip()

        # cleaned_subtitles.append(cleaned_subtitle.strip())

    # 새로운 .srt 파일 생성
    srt_file_path = file_path[:-3] + 'txt'
    with open(srt_file_path, 'w', encoding='utf-8') as file:
        for subtitle in cleaned_subtitles:
            file.write(f'{subtitle}\n')

    return srt_file_path


def download_auto_subtitles(video_url):
    subprocess.run(['yt-dlp',
                    '--sub-lang',
                    'ko',
                    '--write-auto-sub',
                    '--output',
                    'yt-dlp.%(ext)s',
                    '--skip-download',
                    video_url])

def main(video_url):
    download_auto_subtitles(video_url)

    vtt_file_path = 'yt-dlp.ko.vtt'  # yt-dlp가 생성한 vtt 파일 경로
    srt_file_path = process_vtt_file(vtt_file_path)

    print(f'순수한 한글 자막이 생성되었습니다: {srt_file_path}')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("YouTube 동영상 URL을 입력해주세요.")
    else:
        video_url = sys.argv[1]
        main(video_url)
