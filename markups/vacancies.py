from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_vacancies_menu() -> InlineKeyboardMarkup:
    vacancies_menu = InlineKeyboardMarkup(row_width=2)
    headhunter_btn = InlineKeyboardButton(text="HeadHunter", callback_data="headhunter_btn")
    superjob_btn = InlineKeyboardButton(text="SuperJob", callback_data="superjob_btn")
    trudvsem_btn = InlineKeyboardButton(text="Работа России", callback_data="trudvsem_btn")
    geekjob_btn = InlineKeyboardButton(text="GeekJob", callback_data="geekjob_btn")
    main_menu_btn = InlineKeyboardButton(text="Главное меню", callback_data="main_menu")

    vacancies_menu.add(headhunter_btn, superjob_btn, trudvsem_btn, geekjob_btn, main_menu_btn)
    return vacancies_menu

