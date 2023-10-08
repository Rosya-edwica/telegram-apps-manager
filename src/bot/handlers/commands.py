from aiogram import Dispatcher, types, Bot
from bot import markups
import systemd
import toml


bot: Bot = None
toml_data = toml.load("config.toml")

async def start_command(message: types.Message):
    await message.answer(text="Главное меню", reply_markup=markups.get_main_menu())    

async def status_gpt_programs_commands(message: types.Message):
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
    match message.text:
        case "/status_gpt_1":
            program_path = toml_data["gpt"]["programs_path"][0]
        case "/status_gpt_2":
            program_path = toml_data["gpt"]["programs_path"][1]

    systemd.save_systemd_status_info(program_path)
    status = systemd.get_status_info()
    if status is None:
        status = "Не удалось узнать статус программы"
    await message.answer(text=status, reply_markup=markups.get_main_menu())


def register_commands(dp: Dispatcher, BOT: bot):
    global bot
    bot = BOT
    dp.register_message_handler(start_command, commands=["start"])
    dp.register_message_handler(status_gpt_programs_commands, commands=["status_gpt_1", "status_gpt_2"])