from pathlib import Path
from typing import Dict


def ParseCommitMap(destination: Path) -> Dict[str, str]:
    path = Path(destination).joinpath("filter-repo/commit-map").resolve()

    commitMap: Dict[str, str] = {}
    with open(path, "r") as f:
        for line in f.readlines():
            if len(line) != 81:
                continue
            else:
                commitMap[line[:40]] = line[41:]

    return commitMap
