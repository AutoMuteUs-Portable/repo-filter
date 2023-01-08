import os
import sys
from contextlib import contextmanager


@contextmanager
def HiddenPrints():
    stdout = sys.stdout
    with open(os.devnull, "w") as f:
        sys.stdout = f
        yield
        sys.stdout = stdout
