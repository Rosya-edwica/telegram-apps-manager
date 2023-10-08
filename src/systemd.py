"""
Модуль для работы с shell-командами для редактирования и чтения конфиг-файлов systemd-программ
"""

from typing import NamedTuple
import re
import subprocess
import toml
import os
from loguru import logger

toml_data = toml.load("config.toml")

SUCCESS_EMOJI = '✅'
ERROR_EMOJI = '❌'
DIED_EMOJI = '☠️'
STATUS_FILE = toml_data["status_file_path"]


class Status(NamedTuple):
    Status: str
    StartTime: str
    Date: str


def update_systemd_vacancies_config(platform: str):
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
    reload_systemd()

def restart_systemd(program_name: str):
    subprocess.Popen(f"systemctl restart {program_name}", shell=True)

def stop_systemd(program_name):
    subprocess.Popen(f"systemctl stop {program_name}", shell=True)

def save_systemd_status_info(program_name):
    subprocess.Popen(f"systemctl status {program_name} > {STATUS_FILE}", shell=True)


def update_systemd_gpt_config(working_folder: str, exec_folder: str, action: str, selected_program: str):
    """Обновляет шаблон gpt-конфига, меняя путь программы, заголовок и этап"""

    template = f"""
        [Unit]
        Description=(GPT-processing 2) App for processing positions by GPT for {action}
        After=network.target

        [Service]
        User=root
        Group=root
        WorkingDirectory={working_folder}
        ExecStart={exec_folder} {action}

        [Install]
        WantedBy=multi-user.target
    """
    subprocess.Popen(f"echo '{template}' > {selected_program}", shell=True)
    reload_systemd()
    logger.warning(f"Обновили файл конфигурации для программы: {selected_program} + {action} в папке: {working_folder} и окружении: {exec_folder}")

def save_gpt_status_info(path: str):
    f"""Сохраняет в файл {STATUS_FILE} информацию о состоянии программы, чтобы мы могли потом этот файл распарсить"""

    program_name = path.split("/")[-1]
    subprocess.Popen(f"systemctl status {program_name} > {STATUS_FILE}", shell=True)

def get_status_info() -> str:
    """Вернет структурированный текст с инфой о состоянии программы и ее последних действиях"""

    if not os.path.exists(STATUS_FILE):
        logger.error(f"Файл {STATUS_FILE} не существует")
        return

    with open(STATUS_FILE, "r", encoding="utf-8") as f:
        text = f.read()

    try:
        status =  parse_status(text)
        logs = parse_logs(text)
    except BaseException as err:
        logger.error(f"Не удалось получить информацию о статусе: {err}")
        return 
    else:
        return "\n".join([
            f"Статус выполнения: {status.Status}",
            f"Дата запуска: {status.Date}",
            f"Время запуска: {status.StartTime}\n",
            f"Последние логи:\n",
        ] + logs)


def parse_status(text: str) -> Status:
    """Парсим основную информацию о состоянии программы"""

    active_line = re.findall("Active:.*", text)[0] # Active: failed (Result: exit-code) since Tue 2023-10-03 21:52:08 MSK; 1 day 19h ago
    status = re.sub(":|since", "", re.findall(":.*since", active_line)[0]).strip()  #  failed (Result: exit-code) 
    if "failed" in status:
        status = f"{ERROR_EMOJI} {status}" 
    elif "running" in status:
        status = f"{SUCCESS_EMOJI} {status}"
    elif "inactive" in status:
        status = f"{DIED_EMOJI} {status}"
    return Status(
        StartTime=re.sub(";", "", re.findall(";.*", active_line)[0]).strip(), # 1 day 19h ago
        Status=status,
        Date=re.sub("since", "", re.findall("since.*MSK", active_line)[0]), # Tue 2023-10-03 21:52:08 MSK
    )

def parse_logs(text: str) -> list[str]:
    """Парсим список последних действий программы, чтобы понимать на каком этапе она сейчас находится"""

    logs = re.findall("\w+ \d+ .*", text) # LIST OF: "Oct 03 21:52:08 add.edwica.ru gpt_processing_2[1898119]: 2. soft - чтобы запустить поиск soft-скиллов"
    return [i + "\n" for i in logs]

def reload_systemd():
    subprocess.Popen("systemctl daemon-reload", shell=True)


