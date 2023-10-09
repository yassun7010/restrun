from abc import ABC, abstractmethod
from pathlib import Path


class Linter(ABC):
    @abstractmethod
    def lint(self, target_dir: Path, *args: str) -> None:
        ...
