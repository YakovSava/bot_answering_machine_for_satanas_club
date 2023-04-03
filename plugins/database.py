import aiosqlite
import asyncio

from os.path import join


class Database:

    def __init__(self,
                 loop: asyncio.AbstractEventLoop = asyncio.get_event_loop(),
                 filename: str = "database.db",
                 path: str = '/'
                 ):
        self._loop = loop
        self._loop.run_until_complete(self._builder(filename, path))

    async def _builder(self, filename, path) -> None:
        self._connection = await aiosqlite.connect(join(path, filename), loop=self._loop)
        self._connection.row_factory = aiosqlite.Row
        self._cursor = await self._connection.cursor()

        await self._cursor.execute('''CREATE TABLE if not exists Users (
            id TEXT,
            message TEXT
        )''')
        await self._connection.commit()

    async def get(self) -> tuple[aiosqlite.Row]:
        await self._cursor.execute('SELECT * FROM Users')
        return await self._cursor.fetchall()

    async def get_by_id(self, id: int = 505671804):
        for user in (await self.get()):
            if int(user['id']) == id:
                return user

    async def exists(self, id: int == 505671804) -> bool:
        return bool(await self.get_by_id(id))

    async def reg(self, id: int = 505671804, text: str = "") -> None:
        if not (await self.exists(id)):
            await self._cursor.execute('INSERT INTO User VALUES (?,?)', (str(id), text)
            await self._connection.commit()

    async def delete(self, id: int = 505671804) -> None:
        if (await self.exists(id)):
            await self._cursor.execute(f'DELETE FROM Users WHERE id = {id}')
            await self._connection.commit()