from aiogram import types, Bot
import markups

async def postupi(bot: Bot, query: types.CallbackQuery):
    await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
    await bot.send_message(chat_id=query.from_user.id, text="Поступи-онлайн: Выбери действие", reply_markup=markups.get_postupi_menu())

async def postupi_vuz(bot: Bot, query: types.CallbackQuery):
    await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
    await bot.send_message(chat_id=query.from_user.id, text="ВУЗ: Выбери действие", reply_markup=markups.get_postupi_vuz_menu())

async def postupi_college(bot: Bot, query: types.CallbackQuery):
    await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
    await bot.send_message(chat_id=query.from_user.id, text="Колледж: Выбери действие", reply_markup=markups.get_postupi_college_menu())
