import asyncio
import os
import sys
import types
from pathlib import Path

path, tail = os.path.split(__file__)
os.chdir(path)


def import_parents(level):
    file = Path(__file__).resolve()
    parent, top = file.parent, file.parents[level]

    sys.path.append(str(top))
    try:
        sys.path.remove(str(parent))
    except ValueError:
        pass

    __package__ = '.'.join(parent.parts[len(top.parts):])


def print_import(string):
    print(string)
    for name, val in list(globals().items()):
        if isinstance(val, types.ModuleType):
            name = val.__name__
            print("Main -", name)


import_parents(1)

from src.libs import lib
from src.gui import main_app

if __name__ == "__main__":
    from genericpath import isdir

    if not isdir(lib.resource_path("")):
        print("not exist")
        lib.create_app_files()
        lib.default_config_values()

    app = main_app.App()
    app.start()
