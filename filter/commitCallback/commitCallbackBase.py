import os
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import dill
import git_filter_repo as fr

from utils.binary import Binary
from utils.create_ce_mode import create_ce_mode
from utils.customProgress import CustomProgress
from utils.dill import DillObject, FilterInDill
from utils.file import File
from utils.stat import _wstat64

from .parseCommitMap import ParseCommitMap


class CommitCallbackBase:
    def __init__(
        self,
        binary: Binary,
        destination: Path,
        input: Optional[Path],
        output: Path,
    ):
        self.binary = binary
        self.filter: Union[fr.RepoFilter, None] = None
        self.destination = destination
        self.input = input
        self.output = output

        self.newlyAppliedFilters: Dict[str, FilterInDill] = {}

        self.appliedFilters: Dict[str, FilterInDill] = {}
        if self.input is not None:
            with open(self.input, "rb") as f:
                obj: DillObject = dill.load(f, ignore=True)

            self.old_HEAD_hexsha = obj["old_HEAD_hexsha"]
            self.appliedFilters = obj["appliedFilters"]

        self.filesToRemove = [".github/*", ".github/**/*", "README.md", "LICENSE"]

        self.filesToAdd: List[File] = []

        filesDir = Path(os.path.dirname(__file__)).joinpath("../files").resolve()
        root_dir = filesDir.joinpath(binary.value).resolve()
        patterns = ["*", "**/*"]

        for pattern in patterns:
            for path in root_dir.glob(pattern):
                if path.is_dir():
                    continue

                filename = path.relative_to(root_dir).as_posix()

                if (
                    len(list(filter(lambda x: x.path == filename, self.filesToAdd)))
                    != 0
                ):
                    continue

                with open(path, "rb") as f:
                    contents = f.read()
                mode = format(
                    create_ce_mode(_wstat64(path.as_posix()).st_mode), "o"
                ).encode()

                file = File(filename, contents, mode)
                self.filesToAdd.append(file)

    def __call__(self, commit: fr.Commit, metadata: Dict[str, Any]):
        raise NotImplementedError(
            "This function must be implemented by the derived class"
        )

    def dump(self):
        with CustomProgress() as progress:
            task = progress.add_task("Dumping applied filters")

            self._parseCommitMap()

            appliedFilters = self.appliedFilters.copy()
            appliedFilters.update(self.newlyAppliedFilters)

            new_HEAD_hexsha = (
                subprocess.check_output(
                    ["git", "rev-list", "--max-count", "1", "HEAD"],
                    cwd=self.destination,
                )
                .decode()
                .strip()
            )
            for key, val in appliedFilters.items():
                if val["new_hexsha"] == new_HEAD_hexsha:
                    old_HEAD_hexsha = key
                    break

            obj = DillObject(
                old_HEAD_hexsha=old_HEAD_hexsha, appliedFilters=appliedFilters
            )

            with open(self.output, "wb") as f:
                dill.dump(obj, f)

            progress.update(task, total=100, completed=100)

    def _parseCommitMap(self):
        commitMap = ParseCommitMap(self.destination)
        for old_hexsha, new_hexsha in commitMap.items():
            if old_hexsha in self.newlyAppliedFilters:
                self.newlyAppliedFilters[old_hexsha]["new_hexsha"] = new_hexsha
