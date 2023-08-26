from abc import abstractmethod
from pathlib import Path


class RestrunException(Exception):
    @property
    @abstractmethod
    def message(self) -> str:
        ...

    def __str__(self) -> str:
        return self.message


class RestrunError(RestrunException):
    pass


class MockResponseNotFoundError(RestrunError):
    @property
    def message(self) -> str:
        return (
            "Mock response data does not found."
            " Please set use `MockClient.inject_*` methods."
        )


class FileExtensionError(RestrunError):
    def __init__(self, file: str, extension: str) -> None:
        self._file = file
        self._extension = extension

    @property
    def message(self) -> str:
        return f'file extension "{self._extension}" of "{self._file}" is not supported.'


class FileNotFoundError(RestrunError, FileNotFoundError):
    def __init__(self, filepath: str | Path) -> None:
        self.filepath = Path(filepath) if isinstance(filepath, str) else filepath

    @property
    def message(self) -> str:
        return f'"{self.filepath}" not found.'
