from abc import abstractmethod
from pathlib import Path

from restrun.core import http


class RestrunException(Exception):
    @property
    @abstractmethod
    def message(self) -> str:
        ...

    def __str__(self) -> str:
        return self.message


class RestrunError(RestrunException):
    pass


class MockResponseNotFoundError(RestrunError, KeyError):
    @property
    def message(self) -> str:
        return (
            "Mock response data does not found."
            " Please set use `MockClient.inject_*` methods."
        )


class MockResponseTypeError(RestrunError, KeyError):
    def __init__(
        self,
        method: http.Method,
        url: http.URL,
        expected_method: http.Method,
        expected_url: http.URL,
    ) -> None:
        self.method = method
        self.url = url
        self.expected_method = expected_method
        self.expected_url = expected_url

    @property
    def message(self) -> str:
        return "Mock response type is wrong."


class FileExtensionError(RestrunError, ValueError):
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


class PythonFileExecutionError(RestrunError, ValueError):
    def __init__(self, filepath: Path, error: Exception) -> None:
        self.filepath = filepath
        self.error = error

    @property
    def message(self) -> str:
        return f'"{self.filepath}" execution failed: {self.error}'


class ResponseJsonBodyParseError(RestrunError, ValueError):
    def __init__(self, method: http.Method, url: http.URL, content: bytes) -> None:
        self.method = method
        self.url = url
        self.content = content

    @property
    def message(self) -> str:
        return (
            f'Failed to parse the response json body of {self.method} "{self.url}":'
            f" {self.content}"
        )


class ResponseStatusCodeError(RestrunError, ValueError):
    def __init__(
        self,
        method: http.Method,
        url: http.URL,
        status_code: int,
        response_body: bytes,
    ) -> None:
        self.method = method
        self.url = url
        self.status_code = status_code
        self.response_body = response_body

    @property
    def message(self) -> str:
        return (
            f'Response to {self.method} "{self.url}" was not successful.'
            f" Status code: {self.status_code}, Response body: {self.response_body}"
        )


class ResponseJsonBodyValidationError(RestrunError, ValueError):
    def __init__(
        self,
        method: http.Method,
        url: http.URL,
        response_body: dict | list,
        error: Exception,
    ) -> None:
        self.method = method
        self.url = url
        self.response_body = response_body
        self.error = error

    @property
    def message(self) -> str:
        return (
            f'Failed to validate the response json body of {self.method} "{self.url}":'
            f" Error: {self.error}, Response body: {self.response_body}"
        )
