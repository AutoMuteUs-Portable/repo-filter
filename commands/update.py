import os
import subprocess
from pathlib import Path

import click
import git_filter_repo as fr
from git import Repo
from rich import get_console
from rich.padding import Padding

from filter.commitCallback.update import UpdateCommitCallback
from utils.binary import Binary
from utils.customProgress import CustomProgress
from utils.gitProgressHandler import GitProgressHandler
from utils.gitVerifyRepostiory import GitVerifyRepository
from utils.hiddenPrints import HiddenPrints
from utils.rmtree import rmtree
from utils.safechdir import Safechdir


def Update(
    binary: Binary,
    destination: str,
    input: str,
    output: str,
    upstream: str,
    force: bool,
):
    console = get_console()

    destination: Path = Path(destination).resolve()

    output: Path = Path(output).resolve()

    if input is not None:
        input: Path = Path(input).resolve()

    if os.path.exists(destination):
        rmtree(destination)
        os.mkdir(destination)

    with CustomProgress() as progress:
        task = progress.add_task("Cloning upstream repository")
        path = Path(destination).joinpath(".git").resolve()
        Repo.clone_from(
            upstream,
            destination,
            progress=GitProgressHandler(progress, task),
            multi_options=["--bare"],
        )

    with CustomProgress() as progress:
        task = progress.add_task("Finding where to start applying filter", total=None)
        args = fr.FilteringOptions.parse_args(
            ["--prune-empty", "never", "--quiet"] + (["--force"] if force else [])
        )
        updateCommitCallback = UpdateCommitCallback(binary, destination, input, output)

        filterFrom = next(
            iter(
                subprocess.check_output(
                    [
                        "git",
                        "rev-list",
                        "--reverse",
                        f"{updateCommitCallback.old_HEAD_hexsha}..HEAD",
                    ],
                    cwd=destination,
                )
                .decode()
                .splitlines()
            ),
            None,
        )
        progress.update(task, total=100, completed=100)
        if filterFrom is None:
            console.print(
                Padding.indent("No new commits to apply filter", 4),
                style="bold green",
            )
            raise click.Abort()
        updateCommitCallback.filterFrom = filterFrom

        filter = fr.RepoFilter(args, commit_callback=updateCommitCallback)
        updateCommitCallback.filter = filter

        task = progress.add_task("Applying filter", total=None)
        with Safechdir(destination), HiddenPrints():
            filter.run()
        progress.update(task, total=100, completed=100)

    updateCommitCallback.dump()
    GitVerifyRepository(destination)
