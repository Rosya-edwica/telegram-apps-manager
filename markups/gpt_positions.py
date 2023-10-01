from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from markups.menu import get_status_menu

def get_gpt_positions_menu() -> InlineKeyboardMarkup:
    positions_menu = InlineKeyboardMarkup(row_width=2)

    short_descr_btn = InlineKeyboardButton(text="Краткое описание", callback_data="gpt_position_short_descr_menu")
    descr_btn = InlineKeyboardButton(text="Подробное описание", callback_data="gpt_position_description_menu")
    functions_btn = InlineKeyboardButton(text="Функции", callback_data="gpt_position_functions_menu")
    other_names_btn = InlineKeyboardButton(text="Другие наименования", callback_data="gpt_position_other_names_menu")
    work_places_btn = InlineKeyboardButton(text="Рабочие места", callback_data="gpt_position_work_places_menu")
    levels_btn = InlineKeyboardButton(text="Уровни", callback_data="gpt_position_levels_menu")
    main_menu_btn = InlineKeyboardButton(text="Главное меню", callback_data="main_menu")

    positions_menu.add(short_descr_btn, descr_btn, functions_btn, other_names_btn, work_places_btn, levels_btn, main_menu_btn)
    return positions_menu


def get_gpt_positions_functions_menu() -> InlineKeyboardMarkup:
    return get_status_menu(
        run_callback_data_name="gpt_positions_functions_run_btn", 
        status_callback_data_name="gpt_positions_functions_status_btn")


def get_gpt_positions_description_menu() -> InlineKeyboardMarkup:
    return get_status_menu(
        run_callback_data_name="gpt_positions_description_run_btn", 
        status_callback_data_name="gpt_positions_description_status_btn")