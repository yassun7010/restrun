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
    path_parameters: "PythonPathParameters | None" = None
    header_parameters: "PythonHeaderParameters | None" = None
    query_parameters: "PythonQueryParameters | None" = None
    cookie_parameters: "PythonCookieParameters | None" = None
    request_json_body: "PythonRequestJsonBody | None" = None
    request_text_body: "PythonRequestTextBody | None" = None
    response_json_body: "PythonResponseJsonBody | None" = None
    response_text_body: "PythonResponseTextBody | None" = None

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
    def request_body(self) -> "PythonRequestBody | None":
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
            return PythonRequestBody(
                class_name=class_name,
                origin_type=classes[0],
                allow_empty=allow_empty,
            )
        else:
            return PythonRequestBody(
                class_name=class_name,
                origin_type="|".join(classes),
                allow_empty=allow_empty,
            )

    @property
    def response_body(self) -> "PythonRequestBody":
        allow_empty = False
        classes: list[str] = []
        class_name = self.class_name + "RequestBody"
        if self.response_json_body is not None:
            classes.append(self.response_json_body.class_name)
            allow_empty = self.response_json_body.allow_empty
        if self.response_text_body is not None:
            classes.append(self.response_text_body.class_name)

        if len(classes) == 0:
            raise ValueError("request_body must be specified.")
        elif len(classes) == 1:
            return PythonRequestBody(
                class_name=class_name,
                origin_type=classes[0],
                allow_empty=allow_empty,
            )
        else:
            return PythonRequestBody(
                class_name=class_name,
                origin_type="|".join(classes),
                allow_empty=allow_empty,
            )


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
    fields: dict[str, PythonPathParameter]


@dataclass(frozen=True)
class PythonHeaderParameter:
    data_type: PythonDataType
    description: str | None = None
    required: bool = False
    allow_empty_value: bool = False


@dataclass(frozen=True)
class PythonHeaderParameters:
    class_name: str
    fields: dict[str, PythonHeaderParameter]


@dataclass(frozen=True)
class PythonQueryParameter:
    data_type: PythonDataType
    description: str | None = None
    required: bool = False
    allow_empty_value: bool = False


@dataclass(frozen=True)
class PythonQueryParameters:
    class_name: str
    fields: dict[str, PythonQueryParameter]


@dataclass(frozen=True)
class PythonCookieParameter:
    data_type: PythonDataType
    description: str | None = None
    required: bool = False
    allow_empty_value: bool = False


@dataclass(frozen=True)
class PythonCookieParameters:
    class_name: str
    fields: dict[str, PythonCookieParameter]


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
    allow_empty: bool = False
