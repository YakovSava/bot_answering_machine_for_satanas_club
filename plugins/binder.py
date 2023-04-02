import asyncio

from os import mkdir
from os.path import join, exists, isdir
from aiofiles import open as aiopen
from plugins.cpp import Downoloader
from plugins.annotations import NotNone, BinderError


async def _touch(filename: str = "", binary: bool = False) -> None:
    async with aiopen(
            filename,
            ('xb' if binary else 'xt'),
            encoding='utf-8'
    ) as file: pass


class Binder:

    def __init__(
            self,
            cpp: Downoloader = NotNone,
            path: str = "/",
            config: str = "config.conf",
            loop: asyncio.AbstractEventLoop = loop.get_event_loop()
    ):
        if cpp is NotNone:
            self._c = True
        else:
            self._c = False
            self._cpp = cpp

        self._path = path
        self._config = config
        self._loop = loop

    async def read(self, filename: str = "") -> str:
