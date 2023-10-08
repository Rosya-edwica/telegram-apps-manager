import csv
from loguru import logger
import aiomysql
import toml

data_toml = toml.load("config.toml")

async def connect_to_mysql():
    connection = await aiomysql.connect(
        host=data_toml["database"]["host"],
        port=data_toml["database"]["port"],
        user=data_toml["database"]["user"],
        password=data_toml["database"]["password"],
        db=data_toml["database"]["name"],
    )
    return connection


def save_rows_to_csv(path: str, rows: list[list[str]]):
    with open(path, encoding="utf-8", newline="", mode="w") as f:
        writer = csv.writer(f) 
        writer.writerows(rows)
        logger.info(f"Экспортировали данные из MySQL в файл {path}")

