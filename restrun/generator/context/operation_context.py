from dataclasses import dataclass
from functools import cached_property

from restrun.config.v1.source.openapi_source import V1OpenAPISource
from restrun.core.http import URL, Method
from restrun.openapi.openapi import (
    Operation,
    Reference_v3_0_3,
    Reference_v3_1_0,
    Schemas,
)
from restrun.openapi.operation import (
    PythonCookieParameter,
    PythonHeaderParameter,
    PythonParameters,
    PythonPathParameter,
    PythonQueryParameter,
    PythonRequestBody,
    PythonRequestJsonBody,
    PythonRequestTextBody,
    PythonResponseBody,
    PythonResponseJsonBody,
    PythonResponseTextBody,
)
from restrun.openapi.schema import (
    PythonArray,
    PythonDataType,
    PythonLiteralType,
    PythonReference,
    get_data_type,
    is_object,
    title_and_description,
)
from restrun.strcase import class_name


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
    path_parameters: PythonParameters[PythonPathParameter] | None = None
    header_parameters: PythonParameters[PythonHeaderParameter] | None = None
    query_parameters: PythonParameters[PythonQueryParameter] | None = None
    cookie_parameters: PythonParameters[PythonCookieParameter] | None = None
    request_json_body: PythonRequestJsonBody | None = None
    request_text_body: PythonRequestTextBody | None = None
    response_json_body: PythonResponseJsonBody | None = None
    response_text_body: PythonResponseTextBody | None = None

    @cached_property
    def summary_and_description(self) -> str | None:
        return title_and_description(self.summary, self.description)

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
    def response_body(self) -> "PythonResponseBody":
        allow_empty = False
        bodies: list[PythonResponseJsonBody | PythonResponseTextBody] = []
        class_name = self.class_name + "ResponseBody"

        if self.response_json_body is not None:
            bodies.append(self.response_json_body)
            allow_empty = self.response_json_body.allow_empty

        if self.response_text_body is not None:
            bodies.append(self.response_text_body)

        if len(bodies) == 0:
            return PythonResponseBody(
                class_name=class_name,
                origin_type=PythonLiteralType.NONE,
                allow_empty=allow_empty,
            )

        elif len(bodies) == 1:
            body = bodies[0]
            data_type = body.data_type
            match data_type:
                case PythonReference():
                    origin_type = data_type.module_name + "." + data_type.type_name

                case _:
                    origin_type = data_type

            return PythonResponseBody(
                class_name=class_name,
                origin_type=str(origin_type),
                allow_empty=allow_empty,
                is_object=is_object(data_type),
            )

        else:
            return PythonResponseBody(
                class_name=class_name,
                origin_type="|".join([body.class_name for body in bodies]),
                allow_empty=allow_empty,
            )

    @property
    def schema_module_names(self) -> list[str]:
        module_names: set[str] = set()
        if self.response_json_body:
            module_names.update(
                get_schema_module_names(self.response_json_body.data_type)
            )

        return list(sorted(module_names))


def get_schema_module_names(data_type: PythonDataType) -> set[str]:
    module_names: set[str] = set()
    match data_type:
        case PythonReference():
            module_names.add(data_type.module_name)
        case PythonArray():
            module_names.update(get_schema_module_names(data_type.item_data_type))

    return module_names


def make_operation_contexts(
    urls: list[URL] | None, source: V1OpenAPISource
) -> list[OperationContext]:
    openapi = source.openapi_model
    paths = openapi.root.paths

    if paths is None:
        return []

    urls = openapi.get_urls(urls)

    schemas = {}
    if openapi.root.components is not None:
        schemas = openapi.root.components.schemas or {}

    contexts: list[OperationContext] = []
    for path_name, path_item in paths.items():
        operations: dict[Method, Operation | None] = {
            "GET": path_item.get,
            "POST": path_item.post,
            "PUT": path_item.put,
            "PATCH": path_item.patch,
            "DELETE": path_item.delete,
        }

        for method, operation in operations.items():
            if context := make_operation_context(
                method, urls, path_name, operation, schemas
            ):
                contexts.append(context)

    return contexts


def make_operation_context(
    method: Method,
    urls: list[URL],
    path_name: str,
    operation: Operation | None,
    schemas: Schemas,
) -> OperationContext | None:
    if operation is None:
        return None

    path_parameters: dict[str, PythonPathParameter] = {}
    query_parameters: dict[str, PythonQueryParameter] = {}
    for parameter in operation.parameters or []:
        if isinstance(parameter, (Reference_v3_1_0, Reference_v3_0_3)):
            continue

        if (schema := parameter.param_schema) is None:
            continue

        match parameter.param_in:
            case "path":
                path_parameters[parameter.name] = PythonPathParameter(
                    data_type=get_data_type(parameter.name, schema, schemas),
                    description=parameter.description,
                    required=parameter.required,
                )

            case "query":
                query_parameters[parameter.name] = PythonQueryParameter(
                    data_type=get_data_type(parameter.name, schema, schemas),
                    description=parameter.description,
                    required=parameter.required,
                )

    response_json_body = None
    for status_code, response in (operation.responses or {}).items():
        if status_code == "200":
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

                response_json_body = PythonResponseJsonBody(
                    class_name=name,
                    data_type=data_type,
                    allow_empty=False,
                )

    return OperationContext(
        class_name=method.capitalize() + class_name(path_name),
        path_name=path_name,
        method=method,
        urls=urls,
        summary=operation.summary,
        description=operation.description,
        path_parameters=(
            PythonParameters(
                class_name=class_name(path_name) + "PathParameters",
                parameters=path_parameters,
            )
            if len(path_parameters) != 0
            else None
        ),
        query_parameters=(
            PythonParameters(
                class_name=class_name(path_name) + "QueryParameters",
                parameters=query_parameters,
            )
            if len(query_parameters) != 0
            else None
        ),
        response_json_body=response_json_body,
    )
