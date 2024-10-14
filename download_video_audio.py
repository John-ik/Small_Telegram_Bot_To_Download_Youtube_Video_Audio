from mp3_metadata_setter import set_mp3_image

import yt_dlp
import asyncio
import os
import subprocess


async def download_video(url):
    ydl_opts = {
        'format': 'mp4',
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        ydl.process_info(info_dict)
        video_file = ydl.prepare_filename(info_dict)
    return video_file


async def download_audio(url):
    ydl_opts = {
        'format': 'mp3/bestaudio/best',
        'writethumbnail': True,
        'outtmpl': 'music/%(title)s.%(ext)s',
        'quiet': True,
        # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
        'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        ydl.process_info(info_dict)
        audio_file = ydl.prepare_filename(info_dict)
    set_mp3_image(audio_file)

    return audio_file


async def search(req):
    result = subprocess.getoutput(f'yt-dlp "ytsearch1:{req}" --write-thumbnail --skip-download -o "temp" --no-simulate -O "%(channel)s - %(title)s"')
    print(result)
    return result


if __name__ == '__main__':
    setting = "Не выбран"
    run = True
    while run:
        # os.system("clear")
        print("Режим скачивания:", setting)
        print("Введите ссылку видео или выберите действие:")
        print("1. Скачать видео")
        print("2. Скачать аудио")
        print("3. Закончить сеанс")
        key = str(input("Ввод: "))
        if key == "1":
            setting = "Видео"
        elif key == "2":
            setting = "Аудио"
        elif key == "3":
            run = False
            break

        elif setting == "Видео":
            asyncio.run(download_video(key))

        elif setting == "Аудио":
            asyncio.run(download_audio(key))

        else:
            print("Сначала выберите режим скачивания")

