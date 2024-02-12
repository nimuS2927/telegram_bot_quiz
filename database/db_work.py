import aiosqlite

from config import PATH_TO_DATABASE


async def get_info_from_db(query_get: str, *args):
    async with aiosqlite.connect(PATH_TO_DATABASE) as db:
        async with db.execute(query_get, [*args]) as cursor:
            result = await cursor.fetchall()
            return result


async def insert_info_to_db(query_insert: str, *args):
    async with aiosqlite.connect(PATH_TO_DATABASE) as db:
        result = await db.execute_insert(query_insert, [*args])
        await db.commit()
    return result


async def update_info_from_db(query_update: str, *args):
    async with aiosqlite.connect(PATH_TO_DATABASE) as db:
        await db.execute(query_update, [*args])
        await db.commit()


