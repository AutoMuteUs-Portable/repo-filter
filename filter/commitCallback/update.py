from pathlib import Path
from typing import Any, Dict, Union

import git_filter_repo as fr

from filter.filter import Filter
from utils.binary import Binary
from utils.dill import FilterInDill

from .commitCallbackBase import CommitCallbackBase


class UpdateCommitCallback(CommitCallbackBase):
    def __init__(
        self,
        binary: Binary,
        destination: Path,
        input: Path,
        output: Path,
    ):
        super().__init__(binary, destination, input, output)

        self.filterFrom: Union[str, None] = None

    def __call__(self, commit: fr.Commit, metadata: Dict[str, Any]):
        old_hexsha: str = commit.original_id.decode()

        if old_hexsha in self.appliedFilters:
            filter = self.appliedFilters[old_hexsha]["filter"]
            filter._destination = self.destination
            filter._filter = self.filter
        else:
            if commit.original_id.decode() == self.filterFrom:
                filter = Filter(
                    self.filter, self.destination, self.filesToAdd, self.filesToRemove
                )
            else:
                filter = Filter(
                    self.filter, self.destination, filesToRemove=self.filesToRemove
                )

            self.newlyAppliedFilters[old_hexsha] = FilterInDill(filter=filter)

        filter(commit, metadata)
