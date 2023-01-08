from typing import Any, Dict

import git_filter_repo as fr

from filter.commitCallback.commitCallbackBase import CommitCallbackBase
from filter.filter import Filter


class InitCommitCallback(CommitCallbackBase):
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
