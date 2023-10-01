from aiogram import Bot, executor, Dispatcher, types
import os
from dotenv import load_dotenv
import markups
from time import sleep
import subprocess
import status

enviroment = load_dotenv(".env")
if not enviroment:
    exit("Создайте файл с переменными окружениями .env!")

token = os.getenv("TELEGRAM_TOKEN")
bot = Bot(token)
dp = Dispatcher(bot)


async def set_default_commands(dp: Dispatcher):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Главное меню"),
    ])

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
    await message.answer(text="Главное меню", reply_markup=markups.get_main_menu())    


# MAIN MENU
@dp.callback_query_handler(text="main_menu")
async def main_menu(query: types.CallbackQuery):
    await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
    await bot.send_message(chat_id=query.from_user.id, text="Главное меню", reply_markup=markups.get_main_menu())   


# VACANCIES
@dp.callback_query_handler(text="vacancies_menu")
async def vacancies(query: types.CallbackQuery):
    await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id) 
    await bot.send_message(chat_id=query.from_user.id, text="Выбери платформу", reply_markup=markups.get_vacancies_menu())


@dp.callback_query_handler(text="vacancies_status_btn")
async def vacancies_status(query: types.CallbackQuery):
    await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id) 
    subprocess.Popen("systemctl status go_vacancies.service > status_info.txt", shell=True)
    sleep(1) # Чтобы убедиться в том, что информация успела записаться в файл перед чтением

    data = status.parse_status_info()
    await bot.send_message(
        chat_id=query.from_user.id, 
        text="\n".join([
            f"Статус выполнения: {data.ActiveStatus.Status}",
            f"Дата запуска: {data.ActiveStatus.Date}",
            f"Время запуска: {data.ActiveStatus.StartTime}\n",
            f"Последние логи:\n",
        ] + data.Logs))
    
@dp.callback_query_handler(text="vacancies_stop_btn")
async def vacancies_stop(query: types.CallbackQuery):
    await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id) 
    subprocess.Popen("systemctl stop go_vacancies.service", shell=True)
    await bot.send_message(chat_id=query.from_user.id, text="Остановили парсер")    

@dp.callback_query_handler(text="headhunter_btn")
async def vacancies_headhunter(query: types.CallbackQuery):
    await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id) 
    change_platform_for_vacancies_by_systemd("headhunter")
    subprocess.Popen("systemctl daemon-reload", shell=True)
    subprocess.Popen("systemctl restart go_vacancies.service", shell=True)
    await bot.send_message(chat_id=query.from_user.id, text="Запустили парсер Headhunter")

@dp.callback_query_handler(text="superjob_btn")
async def vacancies_superjob(query: types.CallbackQuery):
    await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id) 
    change_platform_for_vacancies_by_systemd("superjob")
    subprocess.Popen("systemctl daemon-reload", shell=True)
    subprocess.Popen("systemctl restart go_vacancies.service", shell=True)
    await bot.send_message(chat_id=query.from_user.id, text="Запустили парсер SuperJob")

@dp.callback_query_handler(text="trudvsem_btn")
async def vacancies_trudvsem(query: types.CallbackQuery):
    await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id) 
    change_platform_for_vacancies_by_systemd("trudvsem")
    subprocess.Popen("systemctl daemon-reload", shell=True)
    subprocess.Popen("systemctl restart go_vacancies.service", shell=True)
    await bot.send_message(chat_id=query.from_user.id, text="Запустили парсер Работа России")


@dp.callback_query_handler(text="geekjob_btn")
async def vacancies_geekjob(query: types.CallbackQuery):
    await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id) 
    change_platform_for_vacancies_by_systemd("geekjob")
    subprocess.Popen("systemctl daemon-reload", shell=True)
    subprocess.Popen("systemctl restart go_vacancies.service", shell=True)
    await bot.send_message(chat_id=query.from_user.id, text="Запустили парсер GeekJob")



def change_platform_for_vacancies_by_systemd(platform: str):
    systemd_config = f"""
    [Unit]
    Description=App for collection vacancies from {platform}
    After=network.target

    [Service]
    User=root
    Group=root

    WorkingDirectory=/root/go/src/github.com/Rosya-edwica/vacancies
    ExecStart=/root/go/src/github.com/Rosya-edwica/vacancies/cmd/scraper {platform}
    """
    subprocess.Popen(f"echo '{systemd_config}' > /etc/systemd/system/go_vacancies.service", shell=True)



# OPENEDU
@dp.callback_query_handler(text="openedu_menu")
async def openedu(query: types.CallbackQuery):
    await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
    await bot.send_message(chat_id=query.from_user.id, text="Выбери действие", reply_markup=markups.get_openedu_menu())

@dp.callback_query_handler(text="openedu_run_btn")
async def openedu_run(query: types.CallbackQuery):
    await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
    subprocess.Popen("systemctl restart openedu.service", shell=True)
    await bot.send_message(chat_id=query.from_user.id, text="Успешно запустили бота")

@dp.callback_query_handler(text="openedu_status_btn")
async def openedu_status(query: types.CallbackQuery):
    await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
    subprocess.Popen("systemctl status openedu.service > status_info.txt", shell=True)
    sleep(1) # Чтобы убедиться в том, что информация успела записаться в файл перед чтением

    data = status.parse_status_info()
    await bot.send_message(
        chat_id=query.from_user.id, 
        text="\n".join([
            f"Статус выполнения: {data.ActiveStatus.Status}",
            f"Дата запуска: {data.ActiveStatus.Date}",
            f"Время запуска: {data.ActiveStatus.StartTime}\n",
            f"Последние логи:\n",
        ] + data.Logs))
    
@dp.callback_query_handler(text="openedu_upload_btn")
async def openedu_upload_result(query: types.CallbackQuery):
    await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
    file = open("/root/parsers/py-openedu-scraper/courses.csv", "rb")
    await bot.send_document(chat_id=query.from_user.id, document=file)
    file.close()

# POSTUPI ONLINE
@dp.callback_query_handler(text="postupi_menu")
async def postupi(query: types.CallbackQuery):
    await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
    await bot.send_message(chat_id=query.from_user.id, text="Поступи-онлайн: Выбери действие", reply_markup=markups.get_postupi_menu())

@dp.callback_query_handler(text="postupi_vuz_menu")
async def postupi_vuz(query: types.CallbackQuery):
    await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
    await bot.send_message(chat_id=query.from_user.id, text="ВУЗ: Выбери действие", reply_markup=markups.get_postupi_vuz_menu())

@dp.callback_query_handler(text="postupi_college_menu")
async def postupi_college(query: types.CallbackQuery):
    await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
    await bot.send_message(chat_id=query.from_user.id, text="Колледж: Выбери действие", reply_markup=markups.get_postupi_college_menu())

    
# GPT
@dp.callback_query_handler(text="gpt_menu")
async def gpt(query: types.CallbackQuery):
    await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
    await bot.send_message(chat_id=query.from_user.id, text="Выбери направление", reply_markup=markups.get_gpt_menu())

@dp.callback_query_handler(text="gpt_position_menu")
async def gpt_positions(query: types.CallbackQuery):
    await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
    await bot.send_message(chat_id=query.from_user.id, text="Выбери действие", reply_markup=markups.get_gpt_positions_menu())

@dp.callback_query_handler(text="gpt_skills_menu")
async def gpt_skills(query: types.CallbackQuery):
    await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
    await bot.send_message(chat_id=query.from_user.id, text="Выбери действие", reply_markup=markups.get_gpt_skills_menu())


@dp.callback_query_handler(text="gpt_position_functions_menu")
async def gpt_positions_functions(query: types.CallbackQuery):
    await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
    await bot.send_message(chat_id=query.from_user.id, text="Подбор описаний профессий: Выбери действие", reply_markup=markups.get_gpt_positions_functions_menu())

@dp.callback_query_handler(text="gpt_position_description_menu")
async def gpt_positions_description(query: types.CallbackQuery):
    await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
    await bot.send_message(chat_id=query.from_user.id, text="Подбор функций профессий: Выбери действие", reply_markup=markups.get_gpt_positions_description_menu())


@dp.callback_query_handler(text="gpt_positions_functions_status_btn")
async def gpt_positions_functions_status(query: types.CallbackQuery):
    await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
    subprocess.Popen("systemctl status gpt_processing_functions.service > status_info.txt", shell=True)
    sleep(1) # Чтобы убедиться в том, что информация успела записаться в файл перед чтением

    data = status.parse_status_info()
    await bot.send_message(
        chat_id=query.from_user.id, 
        text="\n".join([
            f"Статус выполнения: {data.ActiveStatus.Status}",
            f"Дата запуска: {data.ActiveStatus.Date}",
            f"Время запуска: {data.ActiveStatus.StartTime}\n",
            f"Последние логи:\n",
        ] + data.Logs))

@dp.callback_query_handler(text="gpt_positions_functions_run_btn")
async def gpt_positions_functions_run(query: types.CallbackQuery):
    await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
    subprocess.Popen("systemctl restart gpt_processing_functions.service", shell=True)
    await bot.send_message(chat_id=query.from_user.id, text="Перезапустили программу для поиска функций")


@dp.callback_query_handler(text="gpt_positions_description_run_btn")
async def gpt_positions_description_run(query: types.CallbackQuery):
    await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
    subprocess.Popen("systemctl restart gpt_processing_description.service", shell=True)
    await bot.send_message(chat_id=query.from_user.id, text="Перезапустили программу для поиска описаний")

@dp.callback_query_handler(text="gpt_positions_description_status_btn")
async def gpt_positions_description_status(query: types.CallbackQuery):
    await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
    subprocess.Popen("systemctl status gpt_processing_description.service > status_info.txt", shell=True)
    sleep(1) # Чтобы убедиться в том, что информация успела записаться в файл перед чтением

    data = status.parse_status_info()
    await bot.send_message(
        chat_id=query.from_user.id, 
        text="\n".join([
            f"Статус выполнения: {data.ActiveStatus.Status}",
            f"Дата запуска: {data.ActiveStatus.Date}",
            f"Время запуска: {data.ActiveStatus.StartTime}\n",
            f"Последние логи:\n",
        ] + data.Logs))
    
if __name__ == "__main__":

    executor.start_polling(dp, skip_updates=True, on_startup=set_default_commands)
