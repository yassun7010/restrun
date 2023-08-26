from abc import ABC, abstractmethod
from pathlib import Path


class Formatter(ABC):
    @abstractmethod
    def format(self, target_dir: Path, *args: str) -> None:
        ...
