import subprocess
from time import sleep

from aiogram import Bot, executor, Dispatcher, types

from bot import handlers
import toml


toml_data = toml.load("config.toml")
bot = Bot(toml_data["telegram"]["token"])
dp = Dispatcher(bot)


handlers.register_commands(dp, bot)
handlers.register_main_menu(dp, bot)
handlers.register_vacancies_handlers(dp, bot)
handlers.register_postupi_handlers(dp, bot)
handlers.register_openedu_handlers(dp, bot)
handlers.register_gpt_handlers(dp, bot)


async def set_default_commands(dp: Dispatcher):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Главное меню"),
        types.BotCommand("status_gpt_1", "Статус программы с токеном GPT-1"),
        types.BotCommand("status_gpt_2", "Статус программы с токеном GPT-2"),
    ])


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=set_default_commands)
