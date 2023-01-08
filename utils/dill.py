from typing import List, TypedDict

from filter.filterBase import FilterBase


class FilterInDill(TypedDict):
    new_hexsha: str
    filter: FilterBase


class DillObject(TypedDict):
    appliedFilters: List[FilterInDill]
