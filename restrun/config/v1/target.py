from enum import Enum
from typing import Iterable


class GenerateTarget(Enum):
    ALL = "all"
    CLIENT = "client"
    RESOURCE = "resource"

    def __str__(self) -> str:
        return self.value


def get_targets(
    targets: Iterable[GenerateTarget],
) -> set[GenerateTarget]:
    for target in targets:
        if target == GenerateTarget.ALL:
            return set([t for t in GenerateTarget if t != GenerateTarget.ALL])

    return set(targets)
