import sys

from rich import get_console, reconfigure


def InitializeConsole():
    reconfigure(file=sys.stdout)
    return get_console()
