from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_gpt_skills_menu() -> InlineKeyboardMarkup:
    skills_menu = InlineKeyboardMarkup(row_width=2)

    duplicates_btn = InlineKeyboardButton(text="Дубликаты", callback_data="gpt_skills_duplicates_btn")
    hard_soft_btn = InlineKeyboardButton(text="Hard/Soft", callback_data="gpt_skills_hard_soft_btn")
    type_skills_btn = InlineKeyboardButton(text="Тип навыка", callback_data="gpt_skills_type_skills_btn")
    subskills_btn = InlineKeyboardButton(text="Поднавыки", callback_data="gpt_skills_subskills_btn")
    tests_btn = InlineKeyboardButton(text="Тесты", callback_data="gpt_skills_tests_btn")
    materials_btn = InlineKeyboardButton(text="Теоритический материал", callback_data="gpt_skills_materials_btn")
    main_menu_btn = InlineKeyboardButton(text="Главное меню", callback_data="main_menu")

    skills_menu.add(duplicates_btn, hard_soft_btn, type_skills_btn, subskills_btn, tests_btn, materials_btn, main_menu_btn)
    return skills_menu
