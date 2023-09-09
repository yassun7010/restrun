from dataclasses import dataclass

from restrun.config.v1.source.openapi_source import V1OpenAPISource
from restrun.core.http import URL, Method
from restrun.openapi.openapi import (
    OpenAPI,
    Operation,
    Reference_v3_0_3,
    Reference_v3_1_0,
    Schemas,
)
from restrun.openapi.operation import (
    PythonCookieParameters,
    PythonHeaderParameters,
    PythonPathParameters,
    PythonQueryParameters,
    PythonRequestBody,
    PythonRequestJsonBody,
    PythonRequestTextBody,
    PythonResponseJsonBody,
    PythonResponseTextBody,
)
from restrun.openapi.schema import PythonObject, get_data_type
from restrun.strcase import class_name, module_name


@dataclass(frozen=True)
class OperationContext:
    """
    See https://swagger.io/specification/#operation-object
    """

    class_name: str
    path_name: str
    method: Method
    urls: list[URL]
    summary: str | None = None
    description: str | None = None
    path_parameters: PythonPathParameters | None = None
    header_parameters: PythonHeaderParameters | None = None
    query_parameters: PythonQueryParameters | None = None
    cookie_parameters: PythonCookieParameters | None = None
    request_json_body: PythonRequestJsonBody | None = None
    request_text_body: PythonRequestTextBody | None = None
    response_json_body: PythonResponseJsonBody | None = None
    response_text_body: PythonResponseTextBody | None = None

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


def make_operation_contexts(
    urls: list[URL] | None, source: V1OpenAPISource
) -> list[OperationContext]:
    openapi = OpenAPI.from_url(source.location)
    paths = openapi.root.paths

    if paths is None:
        return []

    urls = openapi.get_urls(urls)

    schemas = {}
    if openapi.root.components is not None:
        schemas = openapi.root.components.schemas or {}

    contexts: list[OperationContext] = []
    for path_name, path_item in paths.items():
        if get_operation := make_operation_context(
            "GET", urls, path_name, path_item.get, schemas
        ):
            contexts.append(get_operation)

    return []


def make_operation_context(
    method: Method,
    urls: list[URL],
    path_name: str,
    operation: Operation | None,
    schemas: Schemas,
) -> OperationContext | None:
    if operation is None:
        return None

    response_json_body = None
    if operation.responses is not None:
        for status_code, response in operation.responses.items():
            if status_code == 200:
                if isinstance(response, (Reference_v3_1_0, Reference_v3_0_3)):
                    continue

                if response.content is None:
                    continue

                if "application/json" in response.content:
                    name = class_name(path_name) + "JsonResponse"
                    schema = response.content["application/json"].media_type_schema
                    if schema is None:
                        continue

                    data_type = get_data_type(name, schema, schemas)

                    if isinstance(data_type, PythonObject):
                        response_json_body = PythonResponseJsonBody(
                            class_name=name,
                            data_type=data_type,
                            allow_empty=False,
                        )

    return OperationContext(
        class_name=method.capitalize(),
        path_name=module_name(path_name),
        method=method,
        urls=urls,
        summary=operation.summary,
        description=operation.description,
        response_json_body=response_json_body,
    )
