from abc import ABC, abstractmethod


class BaseLinter(ABC):
    @abstractmethod
    def lint(self) -> None:
        ...
