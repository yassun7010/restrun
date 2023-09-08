from dataclasses import dataclass

from restrun.core.http import URL, Method
from restrun.openapi.schema import PythonDataType, as_typed_dict_field


@dataclass(frozen=True)
class RequestContext:
    class_name: str
    method: Method
    url: URL
    summary: str | None = None
    description: str | None = None
    path_parameters: "dict[str, PathParameter]" | None = None
    header_parameters: "dict[str, HeaderParameter]" | None = None
    query_parameters: "dict[str, QueryParameter]" | None = None
    cookie_parameters: "dict[str, CookieParameter]" | None = None
    request_json_body: "RequestJsonBody" | None = None
    request_text_body: "RequestTextBody" | None = None

    @property
    def summary_and_description(self) -> str | None:
        if self.summary and self.description:
            return f"{self.summary}\n\n{self.description}"
        elif self.summary:
            return self.summary
        elif self.description:
            return self.description
        else:
            return None

    @property
    def response_body_class(self) -> str | None:
        classes: list[str] = []
        if self.request_json_body is not None:
            classes.append(self.request_json_body.class_name)
        if self.request_text_body is not None:
            classes.append(self.request_text_body.class_name)

        if len(classes) == 0:
            return None
        elif len(classes) == 1:
            return classes[0]
        else:
            return "|".join(classes)


@dataclass(frozen=True)
class PathParameter:
    data_type: PythonDataType
    description: str | None = None
    required: bool = False
    allow_empty_value: bool = False

    @property
    def typed_dict_field(self) -> str:
        return as_typed_dict_field(self.data_type, self.required)


@dataclass(frozen=True)
class HeaderParameter:
    data_type: PythonDataType
    description: str | None = None
    required: bool = False
    allow_empty_value: bool = False


@dataclass(frozen=True)
class QueryParameter:
    data_type: PythonDataType
    description: str | None = None
    required: bool = False
    allow_empty_value: bool = False


@dataclass(frozen=True)
class CookieParameter:
    data_type: PythonDataType
    description: str | None = None
    required: bool = False
    allow_empty_value: bool = False


@dataclass(frozen=True)
class RequestJsonBody:
    class_name: str
    data_type: PythonDataType
    description: str | None = None


@dataclass(frozen=True)
class RequestTextBody:
    class_name: str
    data_type: PythonDataType
    description: str | None = None
