import csv
import os

import aiomysql
from dotenv import load_dotenv


enviroment = load_dotenv(".env")
if not enviroment:
    exit("Создайте файл с переменными окружениями .env!")

async def connect_to_mysql():
    connection = await aiomysql.connect(
        host=os.getenv("HOST_MYSQL"),
        port=int(os.getenv("PORT_MYSQL")),
        user=os.getenv("USER_MYSQL"),
        password=os.getenv("PASSWORD_MYSQL"),
        db=os.getenv("DATABASE_MYSQL"),
    )
    return connection


def save_rows_to_csv(rows: list[list[str]]):
    with open("postupi.csv", encoding="utf-8", newline="", mode="w") as f:
        writer = csv.writer(f) 
        writer.writerows(rows)

