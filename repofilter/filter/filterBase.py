from typing import Any, Dict

import git_filter_repo as fr


class FilterBase:
    def __call__(self, commit: fr.Commit, metadata: Dict[str, Any]):
        raise NotImplementedError(
            "This function must be implemented by the derived class"
        )
