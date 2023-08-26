from abc import ABC, abstractmethod


class Linter(ABC):
    @abstractmethod
    def lint(self) -> None:
        ...
