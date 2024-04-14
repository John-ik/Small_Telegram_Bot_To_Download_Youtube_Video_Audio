import yt_dlp
import asyncio
import os


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
    return audio_file


if __name__ == '__main__':
    setting = "Не выбран"
    run = True
    while run:
        # os.system("clear")
        print("Режим скачивания:", setting)
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

