from dataclasses import dataclass
from pathlib import Path
from typing import NotRequired, Type, TypedDict, cast

from restrun.core import http
from restrun.core.request import (
    DeleteRequest,
    GetRequest,
    PatchRequest,
    PostRequest,
    PutRequest,
    Request,
    get_method,
)
from restrun.exception import DuplicateRequestTypeError, RequestURLInvalidError
from restrun.generator import ClassInfo, find_classes_from_code


class RequestMethodMap(TypedDict):
    GET: NotRequired[ClassInfo[GetRequest]]
    POST: NotRequired[ClassInfo[PostRequest]]
    PUT: NotRequired[ClassInfo[PutRequest]]
    PATCH: NotRequired[ClassInfo[PatchRequest]]
    DELETE: NotRequired[ClassInfo[DeleteRequest]]


@dataclass
class ResourceContext:
    module_name: str
    url: http.URL
    method_map: RequestMethodMap

    @property
    def methods(self) -> list[ClassInfo[Request]]:
        return [
            cast(ClassInfo[Request], request) for request in self.method_map.values()
        ]

    @property
    def get_request(self) -> ClassInfo[GetRequest] | None:
        return self.method_map.get("GET")

    @property
    def post_request(self) -> ClassInfo[PostRequest] | None:
        return self.method_map.get("POST")

    @property
    def put_request(self) -> ClassInfo[PutRequest] | None:
        return self.method_map.get("PUT")

    @property
    def patch_request(self) -> ClassInfo[PatchRequest] | None:
        return self.method_map.get("PATCH")

    @property
    def delete_request(self) -> ClassInfo[DeleteRequest] | None:
        return self.method_map.get("DELETE")

    @property
    def has_get_method(self) -> bool:
        return self.get_request is not None

    @property
    def has_post_method(self) -> bool:
        return self.post_request is not None

    @property
    def has_put_method(self) -> bool:
        return self.put_request is not None

    @property
    def has_patch_method(self) -> bool:
        return self.patch_request is not None

    @property
    def has_delete_method(self) -> bool:
        return self.delete_request is not None


def make_resource_contexts(base_dir: Path) -> list[ResourceContext]:
    resource_contexts = []

    for resource_dir in (base_dir / "resources").iterdir():
        if not resource_dir.is_dir():
            continue

        resource_context = make_resource_context(resource_dir)
        if (resource_context) is not None:
            resource_contexts.append(resource_context)

    return resource_contexts


def make_resource_context(resource_dir: Path) -> ResourceContext | None:
    request_class_infos: dict[Type[Request], list[ClassInfo[Request]]] = {
        GetRequest: [],
        PostRequest: [],
        PutRequest: [],
        PatchRequest: [],
        DeleteRequest: [],
    }

    for request_file in resource_dir.iterdir():
        if (
            not request_file.is_file()
            or request_file.suffix != ".py"
            or request_file.name == "__init__.py"
        ):
            continue

        requests_map = find_classes_from_code(
            request_file,
            GetRequest,
            PostRequest,
            PutRequest,
            PatchRequest,
            DeleteRequest,
        )

        for request_type in [GetRequest, PostRequest, PutRequest, PatchRequest]:
            request_class_infos[request_type].extend(requests_map[request_type])
    resource_context = ResourceContext(
        module_name=resource_dir.name, url="", method_map={}
    )
    for request_type, class_infos in request_class_infos.items():
        match len(class_infos):
            case 0:
                continue
            case 1:
                method = get_method(request_type)
                resource_context.method_map[method] = class_infos[0]  # type: ignore
            case _:
                raise DuplicateRequestTypeError(
                    get_method(request_type),
                    request_type.url(),
                    class_infos,
                )
    urls = set(
        cast(ClassInfo[Request], request).class_type.url
        for request in resource_context.method_map.values()
    )

    match len(urls):
        case 0:
            return None
        case 1:
            return resource_context
        case _:
            raise RequestURLInvalidError(resource_context.methods)
