from typing import Any, Dict

import git_filter_repo as fr

from repofilter.filter.filter import Filter
from repofilter.utils.dill import FilterInDill

from .commitCallbackBase import CommitCallbackBase


class InitCommitCallback(CommitCallbackBase):
    def __call__(self, commit: fr.Commit, metadata: Dict[str, Any]):
        old_hexsha: str = commit.original_id.decode()

        if self.input is not None and old_hexsha in self.appliedFilters:
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

            self.newlyAppliedFilters[old_hexsha] = FilterInDill(filter=filter)

        filter(commit, metadata)
