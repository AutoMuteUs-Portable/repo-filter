import os
from fnmatch import fnmatch
from pathlib import Path
from typing import Any, Dict, List

import git_filter_repo as fr

from repofilter.utils.file import File

from .filterBase import FilterBase


class Filter(FilterBase):
    def __init__(
        self,
        filter: fr.RepoFilter,
        destination: Path,
        filesToAdd: List[File] = [],
        filesToRemove: List[str] = [],
    ):
        self._filter = filter
        self._destination = destination
        self.filesToAdd = filesToAdd
        self.filesToRemove = filesToRemove

    def __getstate__(self):
        state = self.__dict__.copy()
        if "_destination" in state:
            del state["_destination"]
        if "_filter" in state:
            del state["_filter"]
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

    def __call__(self, commit: fr.Commit, metadata: Dict[str, Any]):
        for pattern in self.filesToRemove:
            for fileChange in filter(
                lambda x: fnmatch(x.filename.decode(), pattern),
                commit.file_changes.copy(),
            ):
                commit.file_changes.remove(fileChange)

        for file in self.filesToAdd:
            blob = fr.Blob(file.contents)
            self._filter.insert(blob)

            commit.file_changes.append(
                fr.FileChange(b"M", os.fsencode(file.path), blob.id, file.mode)
            )
