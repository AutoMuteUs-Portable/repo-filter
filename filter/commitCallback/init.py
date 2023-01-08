import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import dill
import git_filter_repo as fr

from filter.filter import Filter
from utils.create_ce_mode import create_ce_mode
from utils.customProgress import CustomProgress
from utils.dill import DillObject, FilterInDill
from utils.file import File
from utils.stat import _wstat64

from .parseCommitMap import ParseCommitMap


class InitCommitCallback:
    def __init__(
        self,
        destination: Path,
        input: Optional[Path],
        output: Path,
    ):
        self.filter: Union[fr.RepoFilter, None] = None
        self.destination = destination
        self.input = input
        self.output = output

        self.newlyAppliedFilters: Dict[str, FilterInDill] = {}

        self.appliedFilters: Dict[str, FilterInDill] = {}
        if self.input is not None:
            with open(self.input, "rb") as f:
                obj: DillObject = dill.load(f, ignore=True)

            self.appliedFilters = obj["appliedFilters"]

        self.filesToRemove = [".github/*", ".github/**/*", "README.md", "LICENSE"]

        self.filesToAdd: List[File] = []
        root_dir = (
            Path(os.path.dirname(__file__))
            .joinpath("../../")
            .joinpath("automuteus")
            .resolve()
        )
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
                ).encode("utf-8")

                file = File(filename, contents, mode)
                self.filesToAdd.append(file)

    def __call__(self, commit: fr.Commit, metadata: Dict[str, Any]):
        old_hexsha: str = commit.original_id.decode("utf-8")

        if old_hexsha in self.appliedFilters:
            filter = self.appliedFilters[old_hexsha]["filter"]
            filter._destination = self.destination
            filter._filter = self.filter
        else:
            if len(commit.parents) == 0:
                filter = Filter(
                    self.filter, self.destination, self.filesToAdd, self.filesToRemove
                )
            else:
                filter = Filter(
                    self.filter, self.destination, filesToRemove=self.filesToRemove
                )

            self.newlyAppliedFilters[old_hexsha] = {"filter": filter}

        filter(commit, metadata)

    def dump(self):
        with CustomProgress() as progress:
            task = progress.add_task("Dumping applied filters")

            self._parseCommitMap()

            appliedFilters = self.appliedFilters.copy()
            appliedFilters.update(self.newlyAppliedFilters)

            obj = DillObject(appliedFilters=appliedFilters)

            with open(self.output, "wb") as f:
                dill.dump(obj, f)

            progress.update(task, total=100, completed=100)

    def _parseCommitMap(self):
        commitMap = ParseCommitMap(self.destination)
        for old_hexsha, new_hexsha in commitMap.items():
            if old_hexsha in self.newlyAppliedFilters:
                self.newlyAppliedFilters[old_hexsha]["new_hexsha"] = new_hexsha
