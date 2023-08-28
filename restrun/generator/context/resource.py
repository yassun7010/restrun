from dataclasses import dataclass
from typing import NotRequired, TypedDict, cast

from restrun.core import http
from restrun.core.request import (
    DeleteRequest,
    GetRequest,
    PostRequest,
    PutRequest,
    Request,
)
from restrun.generator import ClassInfo


class RequestMethodMap(TypedDict):
    GET: NotRequired[ClassInfo[GetRequest]]
    POST: NotRequired[ClassInfo[PostRequest]]
    PUT: NotRequired[ClassInfo[PutRequest]]
    PATCH: NotRequired[ClassInfo[PutRequest]]
    DELETE: NotRequired[ClassInfo[DeleteRequest]]


@dataclass
class ResourceContext:
    name: str
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
    def patch_request(self) -> ClassInfo[PutRequest] | None:
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
