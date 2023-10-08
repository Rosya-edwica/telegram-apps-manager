from aiogram import Dispatcher, Bot, types
from bot import markups

import systemd
from time import sleep
import toml

toml_data = toml.load("config.toml")
PROGRAM_NAME = toml_data["openedu"]["program_name"]
RESULT_PATH = toml_data["openedu"]["result_csv_path"]

async def openedu(query: types.CallbackQuery):
    await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
    await bot.send_message(chat_id=query.from_user.id, text="Выбери действие", reply_markup=markups.get_openedu_menu())

async def openedu_run(query: types.CallbackQuery):
    systemd.restart_systemd(PROGRAM_NAME)
    await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
    await bot.send_message(chat_id=query.from_user.id, text="Успешно запустили бота")

async def openedu_status(query: types.CallbackQuery):
    systemd.save_systemd_status_info(PROGRAM_NAME)
    sleep(1) # Чтобы убедиться в том, что информация успела записаться в файл перед чтением

    status = systemd.get_status_info()
    await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
    await bot.send_message(chat_id=query.from_user.id, text=status)
    
async def openedu_upload_result(query: types.CallbackQuery):
    file = open(RESULT_PATH, "rb")
    await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
    await bot.send_document(chat_id=query.from_user.id, document=file)
    file.close()

def register_openedu_handlers(dp: Dispatcher, BOT: Bot):
    global bot
    bot = BOT

    dp.register_callback_query_handler(openedu, text="openedu_menu")
    dp.register_callback_query_handler(openedu_run, text="openedu_run_btn")
    dp.register_callback_query_handler(openedu_status, text="openedu_status_btn")
    dp.register_callback_query_handler(openedu_upload_result, text="openedu_upload_btn")