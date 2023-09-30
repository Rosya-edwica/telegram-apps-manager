from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_postupi_menu() -> InlineKeyboardMarkup:
    postupi_menu = InlineKeyboardMarkup(row_width=1)

    vuz_menu = InlineKeyboardButton(text="ВУЗ", callback_data="postupi_vuz_menu")
    college_menu = InlineKeyboardButton(text="Колледж", callback_data="postupi_college_menu")
    main_menu_btn = InlineKeyboardButton(text="Главное меню", callback_data="main_menu")

    postupi_menu.add(vuz_menu, college_menu, main_menu_btn)
    return postupi_menu


def get_postupi_vuz_menu() -> InlineKeyboardMarkup:
    vuz_menu = InlineKeyboardMarkup()

    run_btn = InlineKeyboardButton(text="Запустить/Перезапустить", callback_data="postupi_vuz_run_btn")
    status_btn = InlineKeyboardButton(text="Статус", callback_data="postupi_vuz_status_btn")
    upload_btn = InlineKeyboardButton(text="Выгрузить данные", callback_data="postupi_vuz_upload_btn")
    main_menu_btn = InlineKeyboardButton(text="Главное меню", callback_data="main_menu")

    vuz_menu.add(run_btn, status_btn, upload_btn, main_menu_btn)
    return vuz_menu


def get_postupi_college_menu() -> InlineKeyboardMarkup:
    college_menu = InlineKeyboardMarkup()

    run_btn = InlineKeyboardButton(text="Запустить/Перезапустить", callback_data="postupi_college_run_btn")
    status_btn = InlineKeyboardButton(text="Статус", callback_data="postupi_college_status_btn")
    upload_btn = InlineKeyboardButton(text="Выгрузить данные", callback_data="postupi_college_upload_btn")
    main_menu_btn = InlineKeyboardButton(text="Главное меню", callback_data="main_menu")

    college_menu.add(run_btn, status_btn, upload_btn, main_menu_btn)
    return college_menu