from dataclasses import dataclass

from restrun.core.http import URL, Method
from restrun.openapi.schema import PythonDataType, PythonObject, as_typed_dict_field


@dataclass(frozen=True)
class OperationContext:
    """
    See https://swagger.io/specification/#operation-object
    """

    class_name: str
    method: Method
    url: URL
    summary: str | None = None
    description: str | None = None
    path_parameters: "PathParameters | None" = None
    header_parameters: "HeaderParameters | None" = None
    query_parameters: "QueryParameters | None" = None
    cookie_parameters: "CookieParameters | None" = None
    request_json_body: "RequestJsonBody | None" = None
    request_text_body: "RequestTextBody | None" = None

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
    def request_body(self) -> "RequestBody | None":
        allow_empty = False
        classes: list[str] = []
        class_name = self.class_name + "RequestBody"
        if self.request_json_body is not None:
            classes.append(self.request_json_body.class_name)
            allow_empty = self.request_json_body.allow_empty
        if self.request_text_body is not None:
            classes.append(self.request_text_body.class_name)

        if len(classes) == 0:
            return None
        elif len(classes) == 1:
            return RequestBody(
                class_name=class_name,
                origin_type=classes[0],
                allow_empty=allow_empty,
            )
        else:
            return RequestBody(
                class_name=class_name,
                origin_type="|".join(classes),
                allow_empty=allow_empty,
            )


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
class PathParameters:
    class_name: str
    fields: dict[str, PathParameter]


@dataclass(frozen=True)
class HeaderParameter:
    data_type: PythonDataType
    description: str | None = None
    required: bool = False
    allow_empty_value: bool = False


@dataclass(frozen=True)
class HeaderParameters:
    class_name: str
    fields: dict[str, HeaderParameter]


@dataclass(frozen=True)
class QueryParameter:
    data_type: PythonDataType
    description: str | None = None
    required: bool = False
    allow_empty_value: bool = False


@dataclass(frozen=True)
class QueryParameters:
    class_name: str
    fields: dict[str, QueryParameter]


@dataclass(frozen=True)
class CookieParameter:
    data_type: PythonDataType
    description: str | None = None
    required: bool = False
    allow_empty_value: bool = False


@dataclass(frozen=True)
class CookieParameters:
    class_name: str
    fields: dict[str, CookieParameter]


@dataclass(frozen=True)
class RequestJsonBody:
    class_name: str
    data_type: PythonObject
    description: str | None = None
    allow_empty: bool = False


@dataclass(frozen=True)
class RequestTextBody:
    class_name: str
    data_type: PythonDataType
    description: str | None = None


@dataclass(frozen=True)
class RequestBody:
    class_name: str
    origin_type: str
    allow_empty: bool = False
