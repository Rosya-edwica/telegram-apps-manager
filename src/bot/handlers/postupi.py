from aiogram import types, Bot, Dispatcher
from bot import markups
import db
import systemd
from time import sleep
import toml


bot: Bot = None
toml_data = toml.load("config.toml")
PROGRAM_NAME = toml_data["postupi"]["program_name"]
DATA_PATH = toml_data["postupi"]["upload_file"]

async def postupi(query: types.CallbackQuery):
    await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
    await bot.send_message(chat_id=query.from_user.id, text="Поступи-онлайн: Выбери действие", reply_markup=markups.get_postupi_menu())

async def postupi_vuz(query: types.CallbackQuery):
    await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
    await bot.send_message(chat_id=query.from_user.id, text="ВУЗ: Выбери действие", reply_markup=markups.get_postupi_vuz_menu())

async def postupi_college(query: types.CallbackQuery):
    await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
    await bot.send_message(chat_id=query.from_user.id, text="Колледж: Выбери действие", reply_markup=markups.get_postupi_college_menu())


async def postupi_vuz_upload(query: types.CallbackQuery):
    msg = await bot.send_message(query.from_user.id, "⏳ Подготовка ответа...", reply_to_message_id=query.message.message_id)

    data = await db.get_postupi_vuzes()
    msg = await bot.edit_message_text(chat_id=query.from_user.id, text="⏳ Сохраняем данные в файл...", message_id=msg.message_id)
    db.save_rows_to_csv(path=DATA_PATH, rows=data)
    sleep(1) # Чтобы убедиться в том, что информация успела записаться в файл перед чтением
    
    file = open(DATA_PATH, mode="rb")

    await bot.edit_message_text(chat_id=query.from_user.id, text="⏳ Загружаем файл...", message_id=msg.message_id)
    await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
    await bot.delete_message(chat_id=query.from_user.id, message_id=msg.message_id)    
    await bot.send_document(chat_id=query.from_user.id, document=file)
    file.close()

async def postupi_vuz_run(query: types.CallbackQuery):
    systemd.restart_systemd(PROGRAM_NAME)
    await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
    await bot.send_message(chat_id=query.from_user.id, text="Перезапустили парсер вузов Postupi-online")

async def postupi_vuz_status(query: types.CallbackQuery):
    systemd.save_systemd_status_info(PROGRAM_NAME)
    sleep(1) # Чтобы убедиться в том, что информация успела записаться в файл перед чтением
    status = systemd.get_status_info()
    await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
    await bot.send_message(chat_id=query.from_user.id, text=status)


async def postupi_vuz_stop(query: types.CallbackQuery):
    systemd.stop_systemd(PROGRAM_NAME)

    await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id) 
    await bot.send_message(chat_id=query.from_user.id, text="Остановили парсер вузов")


def register_postupi_handlers(dp: Dispatcher, BOT: bot):
    global bot
    bot = BOT
    dp.register_callback_query_handler(postupi, text="postupi_menu")
    dp.register_callback_query_handler(postupi_vuz, text="postupi_vuz_menu")
    dp.register_callback_query_handler(postupi_college, text="postupi_college_menu")
    dp.register_callback_query_handler(postupi_vuz_upload, text="postupi_vuz_upload_btn")
    dp.register_callback_query_handler(postupi_vuz_run, text="postupi_vuz_run_btn")
    dp.register_callback_query_handler(postupi_vuz_status, text="postupi_vuz_status_btn")
    dp.register_callback_query_handler(postupi_vuz_stop, text="postupi_vuz_stop_btn")
