import os.path

import aiosqlite
import asyncio

from json import load
from core.utils.excel_to_json import PATH_TO_FIXTURES

from config import PATH_TO_DIR_DATABASE, PATH_TO_DATABASE
from database.querysets import GET_ALL_QUESTIONS, INSERT_NEW_QUESTION

PATH_TO_SCRIPTS = os.path.join(PATH_TO_DIR_DATABASE, 'queries_to_create_db.sql')


async def create_table(path_to_db: str, path_to_scripts: str):
    with open(path_to_scripts, 'r') as f:
        sql_script: str = f.read()

    # Создаем соединение с базой данных (если она не существует, то она будет создана)
    async with aiosqlite.connect(path_to_db) as db:
        # Выполняем SQL-запрос к базе данных
        await db.executescript(sql_script)
        # Сохраняем изменения
        await db.commit()


async def create_question(path_to_file: str, path_to_db: str, query_get: str, query_insert: str):
    with open(path_to_file, 'r', encoding='utf-8') as f:
        data = load(f)

    async with aiosqlite.connect(path_to_db) as db:
        async with db.execute(query_get) as cursor:
            result = await cursor.fetchall()
        if len(result) == 0:
            for key, value in data.items():
                await db.execute(query_insert, [value['question'], value['answer_options'], value['true_answer']])

        await db.commit()


async def main_db_create():
    await create_table(PATH_TO_DATABASE, PATH_TO_SCRIPTS)
    await create_question(PATH_TO_FIXTURES, PATH_TO_DATABASE, GET_ALL_QUESTIONS, INSERT_NEW_QUESTION)


if __name__ == '__main__':
    asyncio.run(main_db_create())
