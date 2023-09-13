from dataclasses import dataclass
from typing import Generic, ItemsView, Literal, TypeVar

from restrun.openapi.schema import (
    PythonDataType,
    PythonLiteralType,
    PythonObject,
    as_typed_dict_field,
)


@dataclass(frozen=True)
class PythonPathParameter:
    data_type: PythonDataType
    description: str | None = None
    required: bool = True

    @property
    def typed_dict_field(self) -> str:
        return as_typed_dict_field(self.data_type, self.required)


@dataclass(frozen=True)
class PythonHeaderParameter:
    data_type: PythonDataType
    description: str | None = None
    required: bool = True


@dataclass(frozen=True)
class PythonQueryParameter:
    data_type: PythonDataType
    description: str | None = None
    required: bool = True


@dataclass(frozen=True)
class PythonCookieParameter:
    data_type: PythonDataType
    description: str | None = None
    required: bool = True


PythonParameter = TypeVar(
    "PythonParameter",
    PythonPathParameter,
    PythonHeaderParameter,
    PythonQueryParameter,
    PythonCookieParameter,
)


@dataclass(frozen=True)
class PythonParameters(Generic[PythonParameter]):
    class_name: str
    parameters: dict[str, PythonParameter]

    @property
    def allow_empty(self) -> bool:
        return not any(parameter.required for parameter in self.parameters.values())

    def items(self) -> ItemsView[str, PythonParameter]:
        return self.parameters.items()


@dataclass(frozen=True)
class PythonRequestJsonBody:
    class_name: str
    data_type: PythonObject
    description: str | None = None
    allow_empty: bool = False


@dataclass(frozen=True)
class PythonRequestTextBody:
    class_name: str
    data_type: PythonDataType
    description: str | None = None


@dataclass(frozen=True)
class PythonRequestBody:
    class_name: str
    origin_type: str
    allow_empty: bool = False


@dataclass(frozen=True)
class PythonResponseJsonBody:
    class_name: str
    data_type: PythonDataType
    description: str | None = None
    allow_empty: bool = False


@dataclass(frozen=True)
class PythonResponseTextBody:
    class_name: str
    data_type: Literal[PythonLiteralType.STR]
    description: str | None = None


@dataclass(frozen=True)
class PythonResponseBody:
    class_name: str
    origin_type: str
