import contextlib
from typing import Any

from git import Repo

from .customProgress import CustomProgress


def GitVerifyRepository(path: Any):
    with contextlib.closing(Repo(path)) as repo:
        with CustomProgress() as progress:
            task = progress.add_task("Verifying repository", total=None)
            repo.git.fsck("--full")
            progress.update(task, total=100, completed=100)
