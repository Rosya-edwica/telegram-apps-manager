from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_vacancies_menu() -> InlineKeyboardMarkup:
    vacancies_menu = InlineKeyboardMarkup(row_width=2)
    headhunter_btn = InlineKeyboardButton(text="HeadHunter", callback_data="vacancies_platform_headhunter")
    superjob_btn = InlineKeyboardButton(text="SuperJob", callback_data="vacancies_platform_superjob")
    trudvsem_btn = InlineKeyboardButton(text="Работа России", callback_data="vacancies_platform_trudvsem")
    geekjob_btn = InlineKeyboardButton(text="GeekJob", callback_data="vacancies_platform_geekjob")
    status_btn = InlineKeyboardButton(text="Статус", callback_data="vacancies_status_btn")
    stop_btn = InlineKeyboardButton(text="Остановить",  callback_data="vacancies_stop_btn")
    main_menu_btn = InlineKeyboardButton(text="Главное меню", callback_data="main_menu")

    vacancies_menu.add(headhunter_btn, superjob_btn, trudvsem_btn, geekjob_btn, status_btn, stop_btn, main_menu_btn)
    return vacancies_menu

