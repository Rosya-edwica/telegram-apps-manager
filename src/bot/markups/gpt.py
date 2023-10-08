from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_gpt_menu() -> InlineKeyboardMarkup:
    gpt_menu = InlineKeyboardMarkup(row_width=1)
    
    positions_menu = InlineKeyboardButton(text="Профессии", callback_data="gpt_position_menu")
    skills_menu = InlineKeyboardButton(text="Навыки", callback_data="gpt_skills_menu")
    main_menu_btn = InlineKeyboardButton(text="Главное меню", callback_data="main_menu")
    
    gpt_menu.add(positions_menu, skills_menu, main_menu_btn)
    return gpt_menu


def get_gpt_tokens() -> InlineKeyboardMarkup:
    tokens_menu = InlineKeyboardMarkup(row_width=1)

    token_1 = InlineKeyboardButton(text="TOKEN 1", callback_data="gpt_token_1")
    token_2 = InlineKeyboardButton(text="TOKEN 2", callback_data="gpt_token_2")
    main_menu = InlineKeyboardButton(text="Главное меню", callback_data="main_menu")

    tokens_menu.add(token_1, token_2, main_menu)
    return tokens_menu