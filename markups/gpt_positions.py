from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from markups.menu import get_status_menu


POSITION_BUTTONS = (
    {
        "text": "Краткое описание",
        "callback_data": "gpt_position_btn_about"
    },
    {
        "text": "Подробное описание",
        "callback_data": "gpt_position_btn_descr"
    },
    {
        "text": "Функции",
        "callback_data": "gpt_position_btn_functions"
    },
    {
        "text": "Образование",
        "callback_data": "gpt_position_btn_education"
    },
    {
        "text": "Уровни",
        "callback_data": "gpt_position_btn_levels"
    },
    {
        "text": "Рабочие места",
        "callback_data": "gpt_position_btn_work_places"
    },
    {
        "text": "Другие наименования",
        "callback_data": "gpt_position_btn_other_names"
    },
    
    
)

def get_gpt_positions_menu() -> InlineKeyboardMarkup:
    positions_menu = InlineKeyboardMarkup(row_width=2)

    for item in POSITION_BUTTONS:
        btn = InlineKeyboardButton(text=item["text"], callback_data=item["callback_data"])
        positions_menu.insert(btn)

    main_menu_btn = InlineKeyboardButton(text="Главное меню", callback_data="main_menu")
    positions_menu.insert(main_menu_btn)
    return positions_menu


def get_gpt_positions_1_menu() -> InlineKeyboardMarkup:
    return get_status_menu(
        run_callback_data_name="gpt_positions_1_run_btn", 
        status_callback_data_name="gpt_positions_1_status_btn")


def get_gpt_positions_2_menu() -> InlineKeyboardMarkup:
    return get_status_menu(
        run_callback_data_name="gpt_positions_2_run_btn", 
        status_callback_data_name="gpt_positions_2_status_btn")