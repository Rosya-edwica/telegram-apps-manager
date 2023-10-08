from aiogram import types, Dispatcher, Bot
import systemd
from bot import markups

from time import sleep
import toml

bot: Bot = None
toml_data = toml.load("config.toml")

PROGRAM_NAME = toml_data["vacancies"]["program_name"]

async def vacancies_menu(query: types.CallbackQuery):
    await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id) 
    await bot.send_message(chat_id=query.from_user.id, text="Выбери платформу", reply_markup=markups.get_vacancies_menu())


async def vacancies_status(query: types.CallbackQuery):
    systemd.save_systemd_status_info(PROGRAM_NAME)
    sleep(1) # Чтобы убедиться в том, что информация успела записаться в файл перед чтением
    status = systemd.get_status_info()
    if status is None:
        status = "Не удалось узнать статус программы"

    await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id) 
    await bot.send_message(chat_id=query.from_user.id, text=status)

async def vacancies_stop(query: types.CallbackQuery):
    systemd.stop_systemd(PROGRAM_NAME)
    await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id) 
    await bot.send_message(chat_id=query.from_user.id, text="Остановили парсер")    

async def vacancies_platforms(query: types.CallbackQuery):
    platform = query.data.split("_")[-1]
    systemd.update_systemd_vacancies_config(platform)
    systemd.restart_systemd(PROGRAM_NAME)
    
    await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id) 
    await bot.send_message(chat_id=query.from_user.id, text=f"Запустили парсер {platform}")


def register_vacancies_handlers(dp: Dispatcher, BOT: bot):
    global bot
    bot = BOT

    dp.register_callback_query_handler(vacancies_menu, text="vacancies_menu")
    dp.register_callback_query_handler(vacancies_status, text="vacancies_status_btn")
    dp.register_callback_query_handler(vacancies_stop, text="vacancies_stop_btn")
    dp.register_callback_query_handler(vacancies_platforms, text_contains="vacancies_platform_")
