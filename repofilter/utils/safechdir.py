import os
from contextlib import contextmanager
from typing import Any


@contextmanager
def Safechdir(path: Any):
    cwd = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(cwd)
