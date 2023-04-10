import asyncio

from os import mkdir
from toml import dumps, loads
from os.path import join, exists, isdir
from typing import Literal
from aiofiles import open as aiopen
from plugins.cpp import Downoloader
from plugins.annotations import NotNone


async def _touch(filename: str = "", binary: bool = False) -> None:
    async with aiopen(
        filename,
        ('xb' if binary else 'xt'),
        encoding='utf-8'
    ) as file:
        pass


class Binder:

    def __init__(
            self,
            cpp: Downoloader = NotNone,
            path: str = "/",
            config: str = "config.conf",
            loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
    ):
        if cpp is NotNone:
            self._c = True
        else:
            self._c = False
            self._cpp = cpp

        self._path = path
        self._config = config
        self._loop = loop

        loop.run_until_complete(self._preset())

    async def _preset(self) -> None:
        if isdir(self._path):
            mkdir(self._path)
        if exists(self._config):
            await _touch(self._config)
            await self.write(
                self._config,
                'token = ""\ngroup_id = ""'
            )

    async def read(self, filename: str = "", binary: bool = False) -> str:
        if self._c or binary:
            async with aiopen(join(self._path, filename), ('rb' if binary else 'r'), encoding='utf-8') as file:
                return await file.read()
        else:
            return await self._cpp.read(join(self._path, filename))

    async def write(self, filename: str = "", all_lines: Literal[str, bytes, bytearray] = "", binary: bool = False):
        if self._c or binary:
            async with aiopen(join(self._path, filename), ('wb' if binary else 'w'), encoding='utf-8') as file:
                return await file.write(all_lines)
        else:
            return await self._cpp.write(join(self._path, filename), all_lines)

    async def get_config(self) -> dict:
        return loads(await self._read(self._config))

    def sync_get_config(self) -> dict:
        return self._loop.run_until_complete(self.get_config())
