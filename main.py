from aiogram import Bot, executor, Dispatcher, types
import os
from dotenv import load_dotenv
import subprocess

enviroment = load_dotenv(".env")
if not enviroment:
    exit("Создайте файл с переменными окружениями .env!")

token = os.getenv("TELEGRAM_TOKEN")
bot = Bot(token)
dp = Dispatcher(bot)

async def set_default_commands(dp: Dispatcher):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить бота"),
        types.BotCommand("restart_gpt_functions", "Перезапустить поиск функций для профессии"),
        types.BotCommand("restart_gpt_description", "Перезапустить поиск описаний для профессии"),
    ])


@dp.message_handler(commands="start")
async def run_bot(message: types.Message):
    await message.answer("Hello, World!")


@dp.message_handler(commands="restart_gpt_functions")
async def restart_gpt_functions(message: types.Message):
    subprocess.Popen("systemctl restart gpt_processing_functions.service")
    await message.answer("Перезапустили программу для поиска функций")

@dp.message_handler(commands="restart_gpt_description")
async def restart_gpt_description(message: types.Message):
    subprocess.Popen("systemctl restart gpt_processing_description.service")
    await message.answer("Перезапустили программу для поиска описаний")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=set_default_commands)
