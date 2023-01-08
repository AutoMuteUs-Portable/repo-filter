from typing import List, TypedDict

from repofilter.filter.filterBase import FilterBase


class FilterInDill(TypedDict):
    new_hexsha: str
    filter: FilterBase


class DillObject(TypedDict):
    old_HEAD_hexsha: str
    appliedFilters: List[FilterInDill]
