from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_main_menu() -> InlineKeyboardMarkup:
    main_menu = InlineKeyboardMarkup(row_width=2)
    gpt_menu = InlineKeyboardButton(text="GPT", callback_data="gpt_menu")
    vacancies_menu = InlineKeyboardButton(text="Вакансии", callback_data="vacancies_menu")
    openedu_menu = InlineKeyboardButton(text="Открытое образование", callback_data="openedu_menu")
    postupi_menu = InlineKeyboardButton(text="Поступи Онлайн", callback_data="postupi_menu")

    main_menu.add(gpt_menu, vacancies_menu, openedu_menu, postupi_menu)
    return main_menu


def get_status_menu(run_callback_data_name: str, status_callback_data_name: str) -> InlineKeyboardMarkup:
    status_menu = InlineKeyboardMarkup(row_width=1)
    run_btn = InlineKeyboardButton(text="Запустить/Перезапустить", callback_data=run_callback_data_name)
    status_btn = InlineKeyboardButton(text="Статус", callback_data=status_callback_data_name)
    main_menu_btn = InlineKeyboardButton(text="Главное меню", callback_data="main_menu")
    
    status_menu.add(run_btn, status_btn, main_menu_btn)
    return status_menu