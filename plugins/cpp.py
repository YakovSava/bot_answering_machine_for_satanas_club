import cppyy

from os import listdir
from typing import Coroutine
from awaits.awaitable import awaitable

class Downoloader:
    def __init__(self, path: str = 'cpp'):
        for file in (listdir(path)):
            if file.endwsith((
                    '.cc', '.cxx', '.cpp',
                    '.c++', '.h', '.hpp',
                    '.hh', '.hxx', '.h++'
            )):
                cppyy.include(join(path, file))

    def __getattr__(self, name: str) -> Any:
        @awaitable
        def wrapper(*args, **kwargs) -> Any:
            function = getattr(cppyy.gbl, name)
            return function(*args, **kwargs)

        return wrapper