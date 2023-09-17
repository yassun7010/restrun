from abc import abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING, Never, Type

import jinja2

if TYPE_CHECKING:
    import pydantic

    from restrun.core import http
    from restrun.core.client import Response
    from restrun.core.operation import Operation
    from restrun.generator import ClassInfo


class RestrunException(Exception):
    @property
    @abstractmethod
    def message(self) -> str:
        ...

    def __str__(self) -> str:
        return self.message


class RestrunError(RestrunException):
    pass


class NeverReachError(RestrunError, ValueError):
    def __init__(self, type: Never) -> None:
        self.type = type

    @property
    def message(self) -> str:
        return f"Never reach {self.type}."


class RestrunConfigNotFoundError(RestrunError, FileNotFoundError):
    def __init__(self, config_path: Path) -> None:
        self.config_path = config_path

    @property
    def message(self) -> str:
        return f'"{self.config_path}" file not found.'


class MockResponseNotFoundError(RestrunError, KeyError):
    @property
    def message(self) -> str:
        return (
            "Mock response data does not found."
            " Please set use `MockClient.inject_*` methods."
        )


class MockRequestError(RestrunError, KeyError):
    def __init__(
        self,
        method: "http.Method",
        url: "http.URL",
        expected_method: "http.Method",
        expected_url: "http.URL",
    ) -> None:
        self.method = method
        self.url = url
        self.expected_method = expected_method
        self.expected_url = expected_url

    @property
    def message(self) -> str:
        return "Mock request method and url are wrong."


class MockResponseError(RestrunError, KeyError):
    def __init__(
        self,
        method: "http.Method",
        url: "http.URL",
        response_body: "Response",
        expected_type: "Type[Response]",
    ) -> None:
        self.method = method
        self.url = url
        self.response_body = response_body
        self.expected_type = expected_type

    @property
    def message(self) -> str:
        return (
            f'Mock response type is expected "{self.expected_type.__name__}",'
            f' but "{self.response_body.__class__.__name__}".'
        )


class MockResponseBodyRemainsError(RestrunError, KeyError):
    @property
    def message(self) -> str:
        return "Mock response body remains."


class URLNotSupportedError(RestrunError, ValueError):
    def __init__(self, url: "http.URL") -> None:
        self.url = url

    @property
    def message(self) -> str:
        return f'"{self.url}" is not supported.'


class JinjaTemplateSyntaxError(jinja2.TemplateSyntaxError, RestrunError):
    def __init__(self, template_path: Path, error: jinja2.TemplateSyntaxError) -> None:
        self.template_path = template_path
        self.error = error
        self.__traceback__ = error.__traceback__

    @property
    def message(self) -> str:
        return f'"{self.template_path}" template syntax error: {self.error}'


class JinjaTemplateRuntimeError(jinja2.TemplateRuntimeError, RestrunError):
    def __init__(self, template_path: Path, error: jinja2.TemplateRuntimeError) -> None:
        self.template_path = template_path
        self.error = error
        self.__traceback__ = error.__traceback__

    @property
    def message(self) -> str:
        return f'"{self.template_path}" jinja runtime error: {self.error}'


class JinjaRenderError(RestrunError):
    def __init__(self, template_path: Path, error: Exception) -> None:
        self.template_path = template_path
        self.error = error
        self.__traceback__ = error.__traceback__

    @property
    def message(self) -> str:
        return f'"{self.template_path}" jinja render error: {self.error}'


class UnknownOperationTypeError(RestrunError, TypeError):
    def __init__(self, operation_type: "Type[Operation]") -> None:
        self.operation_type = operation_type

    @property
    def message(self) -> str:
        return f'Unknown operation type "{self.operation_type}".'


class DuplicateOperationTypeError(RestrunError, TypeError):
    def __init__(
        self,
        method: "http.Method",
        path: str,
        class_infos: "list[ClassInfo[Operation]]",
    ):
        self.method = method
        self.path = path
        self.class_infos = class_infos

    @property
    def message(self) -> str:
        request_types = [
            f"{info.module_name}.{info.class_name}" for info in self.class_infos
        ]

        return (
            f'Duplicate operation type for {self.method} "{self.path}".'
            f" Operation types: {request_types}"
        )


class OperationURLInvalidError(RestrunError, ValueError):
    def __init__(self, operations: "list[ClassInfo[Operation]]") -> None:
        self.operations = operations

    @property
    def message(self) -> str:
        method_map = "\n".join(
            f"{operation.class_name}.path: {operation.class_type.path}"
            for operation in self.operations
        )
        return (
            f"Operation URL is invalid."
            f" Please set unique URL on Operation class in same resource folder."
            f" Operation method map:\n{method_map}"
        )


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
        self.__traceback__ = error.__traceback__

    @property
    def message(self) -> str:
        return f'"{self.filepath}" execution failed: {self.error}'


class ResponseJsonBodyParseError(RestrunError, ValueError):
    def __init__(
        self,
        method: "http.Method",
        url: "http.URL",
        content: bytes,
    ) -> None:
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
        method: "http.Method",
        url: "http.URL",
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
        method: "http.Method",
        url: "http.URL",
        response_body: dict | list,
        error: Exception,
    ) -> None:
        self.method = method
        self.url = url
        self.response_body = response_body
        self.error = error
        self.__traceback__ = error.__traceback__

    @property
    def message(self) -> str:
        return (
            f'Failed to validate the response json body of {self.method} "{self.url}":'
            f" Error: {self.error}, Response body: {self.response_body}"
        )


class OpenAPIRequestError(RestrunError):
    def __init__(
        self,
        method: "http.Method",
        url: "pydantic.HttpUrl",
        content: bytes,
    ) -> None:
        self.method = method
        self.url = url
        self.content = content

    @property
    def message(self) -> str:
        return (
            f'Failed to request the OpenAPI of {self.method} "{self.url}": '
            f"{self.content}"
        )


class ProjectNameRequiredError(RestrunError, ValueError):
    @property
    def message(self) -> str:
        return "Project name is required."
