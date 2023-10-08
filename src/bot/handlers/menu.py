from aiogram import Dispatcher, types, Bot
from bot import markups


bot: Bot = None
async def main_menu(query: types.CallbackQuery):
    await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
    await bot.send_message(chat_id=query.from_user.id, text="Главное меню", reply_markup=markups.get_main_menu())   


def register_main_menu(dp: Dispatcher, BOT: Bot):
    global bot
    bot = BOT
    dp.register_callback_query_handler(main_menu, text="main_menu")