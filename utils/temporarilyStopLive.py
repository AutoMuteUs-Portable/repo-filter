from contextlib import contextmanager

from rich import get_console


@contextmanager
def TemporarilyStopLive():
    live = get_console()._live

    if live:
        transient = live.transient
        live.transient = True
        live.stop()
        live.transient = transient
        yield
        live.start()
    else:
        yield
