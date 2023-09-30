from aiogram import Bot, executor, Dispatcher, types
import os
from dotenv import load_dotenv
import subprocess
import status


enviroment = load_dotenv(".env")
if not enviroment:
    exit("Создайте файл с переменными окружениями .env!")

token = os.getenv("TELEGRAM_TOKEN")
bot = Bot(token)
dp = Dispatcher(bot)

async def set_default_commands(dp: Dispatcher):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить бота"),
        types.BotCommand("restart_gpt_functions", "Перезапустить: поиск функций для профессии"),
        types.BotCommand("restart_gpt_description", "Перезапустить: поиск описаний для профессии"),
        types.BotCommand("status_gpt_functions", "Статус: поиск функций для профессии"),
        types.BotCommand("status_gpt_description", "Статус: поиск описаний для профессии"),
    ])


@dp.message_handler(commands="start")
async def run_bot(message: types.Message):
    await message.answer("Hello, World!")


@dp.message_handler(commands="restart_gpt_functions")
async def restart_gpt_functions(message: types.Message):
    subprocess.Popen("systemctl restart gpt_processing_functions.service", shell=True)
    await message.answer("Перезапустили программу для поиска функций")

@dp.message_handler(commands="restart_gpt_description")
async def restart_gpt_description(message: types.Message):
    subprocess.Popen("systemctl restart gpt_processing_description.service", shell=True)
    await message.answer("Перезапустили программу для поиска описаний")


@dp.message_handler(commands="status_gpt_functions")
async def get_status_gpt_functions(message: types.Message):
    subprocess.Popen("systemctl restart gpt_processing_functions.service > status_info.txt")

    data = status.parse_status_info()
    await message.answer("\n".join([
        f"Статус выполнения: {data.ActiveStatus.Status}",
        f"Дата запуска: {data.ActiveStatus.Date}",
        f"Время запуска: {data.ActiveStatus.StartTime}\n",
        f"Последние логи:\n",
    ] + data.Logs))

@dp.message_handler(commands="status_gpt_description")
async def get_status_gpt_description(message: types.Message):
    subprocess.Popen("systemctl restart gpt_processing_description.service > status_info.txt")

    data = status.parse_status_info()
    
    await message.answer("\n".join([
        f"Статус выполнения: {data.ActiveStatus.Status}",
        f"Дата запуска: {data.ActiveStatus.Date}",
        f"Время запуска: {data.ActiveStatus.StartTime}\n",
        f"Последние логи:\n",
    ] + data.Logs))



if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=set_default_commands)
