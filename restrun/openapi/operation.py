from dataclasses import dataclass
from typing import ItemsView

from restrun.openapi.schema import PythonDataType, PythonObject, as_typed_dict_field


@dataclass(frozen=True)
class PythonPathParameter:
    data_type: PythonDataType
    description: str | None = None
    required: bool = False
    allow_empty_value: bool = False

    @property
    def typed_dict_field(self) -> str:
        return as_typed_dict_field(self.data_type, self.required)


@dataclass(frozen=True)
class PythonPathParameters:
    class_name: str
    parameters: dict[str, PythonPathParameter]

    def items(self) -> ItemsView[str, PythonPathParameter]:
        return self.parameters.items()


@dataclass(frozen=True)
class PythonHeaderParameter:
    data_type: PythonDataType
    description: str | None = None
    required: bool = False
    allow_empty_value: bool = False


@dataclass(frozen=True)
class PythonHeaderParameters:
    class_name: str
    parameters: dict[str, PythonHeaderParameter]

    def items(self) -> ItemsView[str, PythonHeaderParameter]:
        return self.parameters.items()


@dataclass(frozen=True)
class PythonQueryParameter:
    data_type: PythonDataType
    description: str | None = None
    required: bool = False
    allow_empty_value: bool = False


@dataclass(frozen=True)
class PythonQueryParameters:
    class_name: str
    parameters: dict[str, PythonQueryParameter]

    def items(self) -> ItemsView[str, PythonQueryParameter]:
        return self.parameters.items()


@dataclass(frozen=True)
class PythonCookieParameter:
    data_type: PythonDataType
    description: str | None = None
    required: bool = False
    allow_empty_value: bool = False


@dataclass(frozen=True)
class PythonCookieParameters:
    class_name: str
    parameters: dict[str, PythonCookieParameter]

    def items(self) -> ItemsView[str, PythonCookieParameter]:
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
    data_type: PythonObject
    description: str | None = None
    allow_empty: bool = False


@dataclass(frozen=True)
class PythonResponseTextBody:
    class_name: str
    data_type: PythonDataType
    description: str | None = None


@dataclass(frozen=True)
class PythonResponseBody:
    class_name: str
    origin_type: str
