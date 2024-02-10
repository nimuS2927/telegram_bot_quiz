import aiosqlite

from config import PATH_TO_DATABASE


async def get_info_from_db(query_get: str, *args):
    async with aiosqlite.connect(PATH_TO_DATABASE) as db:
        async with db.execute(query_get, [*args]) as cursor:
            result = await cursor.fetchall()
            return result

