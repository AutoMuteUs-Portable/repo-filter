import os
import tempfile
from pathlib import Path
from shutil import copy
from typing import Optional

import click
import git_filter_repo as fr
import questionary
from git import Repo

from filter.commitCallback.init import InitCommitCallback
from utils.customProgress import CustomProgress
from utils.customQuestionary import CustomQuestionary
from utils.gitProgressHandler import GitProgressHandler
from utils.gitVerifyRepostiory import GitVerifyRepository
from utils.hiddenPrints import HiddenPrints
from utils.remote import Remote
from utils.rmtree import rmtree
from utils.safechdir import Safechdir


def Init(
    destination: str,
    input: Optional[str],
    output: str,
    upstream: Remote,
):
    with tempfile.TemporaryDirectory() as tempDir:
        destination: Path = Path(destination).resolve()

        output: Path = Path(output).resolve()
        tempOutput = Path(tempDir).joinpath("output.dill").resolve()

        tempInput = None
        if input is not None:
            input: Path = Path(input).resolve()
            tempInput = Path(tempDir).joinpath("input.dill").resolve()
            copy(input, tempInput)

        if os.path.exists(destination):
            if CustomQuestionary(
                0,
                questionary.confirm,
                "Destination already exists. Do you want to overwrite it?",
                default=False,
            ):
                rmtree(destination)
                os.mkdir(destination)
            else:
                raise click.Abort()
        else:
            os.mkdir(destination)

        with CustomProgress() as progress:
            task = progress.add_task("Cloning upstream repository")
            path = Path(destination).joinpath(".git").resolve()
            Repo.clone_from(
                upstream["url"],
                destination,
                progress=GitProgressHandler(progress, task),
                multi_options=["--bare"],
            )

        with CustomProgress() as progress:
            task = progress.add_task("Applying filter", total=None)
            args = fr.FilteringOptions.parse_args(["--prune-empty", "never", "--quiet"])
            initCommitCallback = InitCommitCallback(destination, tempInput, tempOutput)
            filter = fr.RepoFilter(args, commit_callback=initCommitCallback)
            initCommitCallback.filter = filter
            with Safechdir(destination), HiddenPrints():
                filter.run()
            progress.update(task, total=100, completed=100)

        initCommitCallback.dump()
        GitVerifyRepository(destination)

        if input is not None:
            copy(tempInput, input)

        copy(tempOutput, output)
