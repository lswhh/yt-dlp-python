import re
import subprocess
import sys
import webvtt

def process_vtt_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        vtt_content = file.read()

    # 자막 블록을 추출하는 정규 표현식 패턴
    subtitle_pattern = r'\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}([\s\S]*?)\n([\s\S]*?)\n([\s\S]*?)\n'

    subtitles = re.findall(subtitle_pattern, vtt_content, re.DOTALL)

    cleaned_subtitles = []

    for subtitle_tuple in subtitles:
        # if len(subtitle_tuple[2]) >= 1:
        #     if len(subtitle_tuple[2].strip()) == 0:
        #         subtitle = subtitle_tuple[1]  # 튜플에서 자막을 추출합니다.
        #         cleaned_subtitles.append(subtitle)
        # else:
        #     continue
        if len(subtitle_tuple[2].strip()) == 0:
            continue
        subtitle = subtitle_tuple[1]
        # <.*?>를 빈 문자열로 대체하여 제거
        cleaned_subtitle = re.sub(r'<.*?>', '', subtitle)
        #print(cleaned_subtitle)
        # align:start position:0% 문자 제거
        # cleaned_subtitle = subtitle.replace("align:start position:0%", "").strip()

        cleaned_subtitles.append(cleaned_subtitle.strip())


    # 새로운 .txt 파일 생성
    srt_file_path = file_path[:-3] + 'txt'
    with open(srt_file_path, 'w', encoding='utf-8') as file:
        for subtitle in cleaned_subtitles:
            file.write(f'{subtitle}\n')

    return srt_file_path

def vtt_to_text(vtt_filename, output_filename):
    captions = webvtt.read(vtt_filename)
    unique_lines = []

    for caption in captions:
        line = caption.text.strip()
        num_of_lines = len(line.split('\n'))  # 줄 개수 확인

        if num_of_lines <= 1: 
            # 중복 line 검사를 위해 unique_lines의 마지막 3개 요소를 검사
            recent_lines = unique_lines[-3:]
            if line not in recent_lines:
                unique_lines.append(line)

    with open(output_filename, 'w', encoding='utf-8') as output_file:
        for line in unique_lines:
            output_file.write(line + '\n')
            
def download_auto_subtitles(video_url):
    subprocess.run(['yt-dlp',
                    '--sub-lang',
                    'ko',
                    '--write-auto-sub',
                    # '--write-sub',
                    '--output',
                    'yt-dlp',
                    '--skip-download',
                    video_url])

def main(video_url):
    download_auto_subtitles(video_url)

    vtt_file_path = 'yt-dlp.ko.vtt'  # yt-dlp가 생성한 vtt 파일 경로
    srt_file_path = process_vtt_file(vtt_file_path)
    vtt_to_text(vtt_file_path,"vtt_to_text.text")
    print(f'순수한 한글 자막이 생성되었습니다: {srt_file_path}')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("YouTube 동영상 URL을 입력해주세요.")
    else:
        video_url = sys.argv[1]
        main(video_url)