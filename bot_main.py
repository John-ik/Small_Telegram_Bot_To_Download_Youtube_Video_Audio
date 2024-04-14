from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from download_video_audio import download_video, download_audio
from config import bot_token
import os

bot = Bot(token=bot_token)
dp = Dispatcher(bot, storage=MemoryStorage())


class States:
    video = "видео"
    audio = "аудио"


@dp.message_handler(state="*", commands=["start"])
async def start_command(message: types.Message):
    keyboard = [[types.KeyboardButton(text='/video')], [types.KeyboardButton(text='/audio')]]
    video_audio_kb = types.ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)
    await message.reply("Перед отправлением ссылки выберите:\n"
                        "Скачать видео: /video\n"
                        "Скачать аудио из видео: /audio\n"
                        "[GitHub проекта](https://github.com/Ifanfomin/Small-Telegram-Bot-To-Download-Youtube-Video-Aoudio)",
                        reply_markup=video_audio_kb,
                        parse_mode="MarkdownV2")


@dp.message_handler(state="*", commands=["video"])
async def user_set_state(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(States.video)
    await message.reply("Я готов скачивать видео", reply=False)


@dp.message_handler(state="*", commands=["audio"])
async def user_set_state(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(States.audio)
    await message.reply("Я готов скачивать аудио", reply=False)


@dp.message_handler(state=States.video)
async def bot_download_video(message: types.Message):
    msg = await message.reply("Скачиваем...", reply=False)
    try:
        video_file = await download_video(message.text)
        with open(video_file, "rb") as file:
            await message.reply_video(file, reply=False)
        os.remove(video_file)
    except:
        await msg.edit_text("Проверьте введёную ссылку")


@dp.message_handler(state=States.audio)
async def bot_download_audio(message: types.Message):
    msg = await message.reply("Скачиваем...", reply=False)
    try:
        audio_file = await download_audio(message.text)
        print(audio_file)
        with open(audio_file, "rb") as file:
            await message.reply_audio(file, reply=False, title=" ".join(audio_file.split("_")))
        os.remove(audio_file)
    except:
        await msg.edit_text("Проверьте введёную ссылку")


@dp.message_handler()
async def please_send_start(message: types.Message):
    await message.reply("Для начала работы введите /start", reply=False)


if __name__ == '__main__':
    executor.start_polling(dp)
