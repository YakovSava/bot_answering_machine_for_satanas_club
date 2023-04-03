import asyncio

import aiosqlite3

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
        self._connection = await aiosqlite3.connect(join(path, filename), loop=self._loop)
        self._connection.row_factory = aiosqlite3.Row
        self._cursor = await self._connection.cursor()
