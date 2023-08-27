from abc import ABC, abstractmethod
from typing import Type, Union

from typing_extensions import final

from restrun.core.http import (
    URL,
    Headers,
    Method,
    QuryParameters,
    RequestJsonBody,
    ResponseModelBody,
)
from restrun.core.resource import Resource
from restrun.exception import (
    MockResponseNotFoundError,
    MockResponseTypeError,
    RestrunError,
)


class Request(Resource):
    pass


class GetRequest(Request):
    @property
    @final
    def has_get_method(self) -> bool:
        return True


class PostRequest(Request):
    @property
    @final
    def has_post_method(self) -> bool:
        return True


class PutRequest(Request):
    @property
    @final
    def has_put_method(self) -> bool:
        return True


class PatchRequest(Request):
    @property
    @final
    def has_patch_method(self) -> bool:
        return True


class DeleteRequest(Request):
    @property
    @final
    def has_delete_method(self) -> bool:
        return True


def downcast(
    request: Union[
        DeleteRequest,
        GetRequest,
        PatchRequest,
        PostRequest,
        PutRequest,
    ]
) -> Request:
    return request


class RequestClient(ABC):
    @abstractmethod
    def get(
        self,
        *,
        url: URL,
        response_body_type: Type[ResponseModelBody],
        query: QuryParameters | None = None,
    ) -> ResponseModelBody:
        ...

    @abstractmethod
    def post(
        self,
        *,
        url: URL,
        response_body_type: Type[ResponseModelBody],
        headers: Headers | None = None,
        query: QuryParameters | None = None,
        body: RequestJsonBody | None = None,
    ) -> ResponseModelBody:
        ...

    @abstractmethod
    def put(
        self,
        *,
        url: URL,
        response_body_type: Type[ResponseModelBody],
        headers: Headers | None = None,
        query: QuryParameters | None = None,
        body: RequestJsonBody | None = None,
    ) -> ResponseModelBody:
        ...

    @abstractmethod
    def patch(
        self,
        *,
        url: URL,
        response_body_type: Type[ResponseModelBody],
        headers: Headers | None = None,
        query: QuryParameters | None = None,
        body: RequestJsonBody | None = None,
    ) -> ResponseModelBody:
        ...

    @abstractmethod
    def delete(
        self,
        *,
        url: URL,
        response_body_type: Type[ResponseModelBody],
        headers: Headers | None = None,
        query: QuryParameters | None = None,
        body: RequestJsonBody | None = None,
    ) -> ResponseModelBody:
        ...


class RequestRealClient(RequestClient):
    pass


class RequestMockClient(RequestClient):
    def __init__(self) -> None:
        self._store: list[
            tuple[tuple[Method, URL], Union[ResponseModelBody, RestrunError]]
        ] = []

    def inject_get_response_body(
        self,
        url: URL,
        response_body: Union[ResponseModelBody, RestrunError],
    ):
        self._store.append((("GET", url), response_body))

    def inject_post_response_body(
        self,
        url: URL,
        response_body: Union[ResponseModelBody, RestrunError],
    ):
        self._store.append((("POST", url), response_body))

    def inject_put_response_body(
        self,
        url: URL,
        response_body: Union[ResponseModelBody, RestrunError],
    ):
        self._store.append((("PUT", url), response_body))

    def inject_patch_response_body(
        self,
        url: URL,
        response_body: Union[ResponseModelBody, RestrunError],
    ):
        self._store.append((("PATCH", url), response_body))

    def inject_delete_response_body(
        self,
        url: URL,
        response_body: Union[ResponseModelBody, RestrunError],
    ):
        self._store.append((("DELETE", url), response_body))

    def _extract_response_body(self, method: Method, url: URL) -> ResponseModelBody:
        if len(self._store) == 0:
            raise MockResponseNotFoundError()

        method_url, response_body = self._store.pop(0)
        expected_method, expected_url = method_url

        if method != expected_method or url != expected_url:
            raise MockResponseTypeError(method, url, expected_method, expected_url)

        if isinstance(response_body, RestrunError):
            raise response_body

        return response_body
