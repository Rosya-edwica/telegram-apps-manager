from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_openedu_menu() -> InlineKeyboardMarkup:
    openedu_menu = InlineKeyboardMarkup()
    run_btn = InlineKeyboardButton(text="Запустить/Перезапустить", callback_data="openedu_run_btn")
    status_btn = InlineKeyboardButton(text="Статус", callback_data="openedu_status_btn")
    upload_btn = InlineKeyboardButton(text="Выгрузить данные", callback_data="openedu_upload_btn")
    main_menu_btn = InlineKeyboardButton(text="Главное меню", callback_data="main_menu")

    openedu_menu.add(run_btn, status_btn, upload_btn, main_menu_btn)
    return openedu_menu