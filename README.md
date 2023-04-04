# What is it?

This is a bot for answering machine in a group dedicated to Satanism, but you can use this bot for something else. It
has flexible configuration of everything from *configuration* files to *C++* code replacement.

## How to change something?

Configuration:

```toml
token = 'Enter your VK API group token'
group_id = 'Enter your group ID'
admin = ['Enter your IDs']
```

C++ files:

```C++
string read(string filename) {
    string line, lines = "", endline = "\n";
    ifstream file;
    file.open(filename.c_str());
    if (file.is_open()) {
        while (getline(line, file)) lines = lines + line + endline;
    }
    return lines;
}

void write(string filename, string all_lines) {
    ofstream file;
    file.open(filename.c_str());
    if (file.is_open()) {
        file << all_lines.c_str() << endl;
    }
}
```

<blockquote> C/C++ files should implement the methods read(string filename) and write(string filename, string all_lines) </blockquote>

You can also customize:

- A folder for the binder with files (*binder.py*), configuration file (*config.conf*) or downoloader type (*cpp.py*)

```python
from plugins.binder import Binder
from custom.plugins.cpp import CppCustomDownoloader

...
binder = Binder(
    path='/your/path',
    config='your_config_filename.txt',
    cpp=CppCustomDownoloader()
)
```

- Folder with C++ files

```python
from plugins.cpp import Downoloader

...
downoloader = Downoloader(path='/your/c-plus-plus/path')
```

- Database file

```python
from plugins.database import Database

...
db = Database(
    path='/your/database/path',
    filename='your_filename.db'  # And or binary files type (.db, .bin)
)
```

- C++ downoloader (**asynchronous only, please!**)

```python
import asyncio
import cppyy  # For C - cffi

from os import listdir
from os.path import join


class Downoloader(cppyy.dbl.example_c_plus_plus_class_for_inheritance):

    def __init__(self, path: str = 'cxx', loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()):
        self._loop = loop
        for file in (listdir(path)):
            if file.endswith((
                    '.cc', '.cxx', '.cpp',
                    '.c++', '.h', '.hpp',
                    '.hh', '.hxx', '.h++'
            )):
                cppyy.include(join(path, file))

    def __getattr__(self, name: str) -> Any:
        async def wrapper(*args) -> Any:
            function = getattr(cppyy.gbl, name)
            return await self._loop.run_in_executor(None, function, *args)

        return wrapper
```