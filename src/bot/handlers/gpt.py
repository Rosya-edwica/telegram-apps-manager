from aiogram import Dispatcher, Bot, types
from time import sleep
import toml
from bot import markups

import systemd

bot: Bot = None
toml_data = toml.load("config.toml")


async def gpt(query: types.CallbackQuery):
    await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
    await bot.send_message(chat_id=query.from_user.id, text="Выбери направление", reply_markup=markups.get_gpt_menu())

async def gpt_positions(query: types.CallbackQuery):
    await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
    await bot.send_message(chat_id=query.from_user.id, text="Выбери действие", reply_markup=markups.get_gpt_positions_menu())

async def gpt_position_buttons(query: types.CallbackQuery):
    toml_data["gpt"]["active_program_step"] = query.data.replace("gpt_position_btn_", "")
    toml.dump(toml_data, open("config.toml", "w"))

    await bot.send_message(chat_id=query.from_user.id, text="Выбери действие", reply_markup=markups.get_gpt_tokens())

    
async def select_gpt_token(query: types.CallbackQuery):
    match query.data:
        case "gpt_token_1":
            program_path = toml_data["gpt"]["programs_path"][0]        
            working_folder = toml_data["gpt"]["working_folders"][0]
            exec_folder = toml_data["gpt"]["executable_folders"][0]
        case "gpt_token_2":
            program_path = toml_data["gpt"]["programs_path"][1]          
            working_folder = toml_data["gpt"]["working_folders"][1]
            exec_folder = toml_data["gpt"]["executable_folders"][1]
    
    current_step = toml_data["gpt"]["active_program_step"]
    systemd.update_systemd_gpt_config(action=current_step, selected_program=program_path, working_folder=working_folder, exec_folder=exec_folder)

    await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
    await bot.send_message(chat_id=query.from_user.id, text=f"Запустили обработку: {current_step}")

    toml_data["gpt"]["active_program_path"] = program_path
    toml.dump(toml_data, open("config.toml", "w"))

async def gpt_skills(query: types.CallbackQuery):
    await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
    await bot.send_message(chat_id=query.from_user.id, text="Выбери действие", reply_markup=markups.get_gpt_skills_menu())


def register_gpt_handlers(dp: Dispatcher, BOT: Bot):
    global bot
    bot = BOT

    dp.register_callback_query_handler(gpt, text="gpt_menu")
    dp.register_callback_query_handler(gpt_positions, text="gpt_position_menu")
    dp.register_callback_query_handler(gpt_position_buttons, text_contains="gpt_position_btn_")
    dp.register_callback_query_handler(select_gpt_token, text_contains="gpt_token_")
    dp.register_callback_query_handler(gpt_skills, text="gpt_skills_menu")
