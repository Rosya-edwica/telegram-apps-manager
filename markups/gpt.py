from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_gpt_menu() -> InlineKeyboardMarkup:
    gpt_menu = InlineKeyboardMarkup(row_width=1)
    
    positions_menu = InlineKeyboardButton(text="Профессии", callback_data="gpt_position_menu")
    skills_menu = InlineKeyboardButton(text="Навыки", callback_data="gpt_skills_menu")
    main_menu_btn = InlineKeyboardButton(text="Главное меню", callback_data="main_menu")
    
    gpt_menu.add(positions_menu, skills_menu, main_menu_btn)
    return gpt_menu