from abc import ABC, abstractmethod
from typing import Self, Type, Union

from typing_extensions import override

from restrun.core.http import (
    URL,
    Headers,
    Method,
    QuryParameters,
    RequestJsonBody,
    ResponseModelBody,
)
from restrun.core.model import Model
from restrun.core.resource import Resource
from restrun.exception import (
    MockRequestError,
    MockResponseBodyRemainsError,
    MockResponseNotFoundError,
    MockResponseTypeError,
    RestrunError,
    UnknownRequestTypeError,
)


class Request(Resource):
    pass


class GetRequest(Request):
    pass


class PostRequest(Request):
    pass


class PutRequest(Request):
    pass


class PatchRequest(Request):
    pass


class DeleteRequest(Request):
    pass


def get_method(request: Type[Request]) -> Method:
    if issubclass(request, GetRequest):
        return "GET"
    elif issubclass(request, PostRequest):
        return "POST"
    elif issubclass(request, PutRequest):
        return "PUT"
    elif issubclass(request, PatchRequest):
        return "PATCH"
    elif issubclass(request, DeleteRequest):
        return "DELETE"
    else:
        raise UnknownRequestTypeError(request)


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
        url: URL,
        *,
        response_body_type: Type[ResponseModelBody],
        headers: Headers | None = None,
        query: QuryParameters | None = None,
    ) -> ResponseModelBody:
        ...

    @abstractmethod
    def post(
        self,
        url: URL,
        *,
        response_body_type: Type[ResponseModelBody],
        headers: Headers | None = None,
        query: QuryParameters | None = None,
        body: RequestJsonBody | None = None,
    ) -> ResponseModelBody:
        ...

    @abstractmethod
    def put(
        self,
        url: URL,
        *,
        response_body_type: Type[ResponseModelBody],
        headers: Headers | None = None,
        query: QuryParameters | None = None,
        body: RequestJsonBody | None = None,
    ) -> ResponseModelBody:
        ...

    @abstractmethod
    def patch(
        self,
        url: URL,
        *,
        response_body_type: Type[ResponseModelBody],
        headers: Headers | None = None,
        query: QuryParameters | None = None,
        body: RequestJsonBody | None = None,
    ) -> ResponseModelBody:
        ...

    @abstractmethod
    def delete(
        self,
        url: URL,
        *,
        response_body_type: Type[ResponseModelBody],
        headers: Headers | None = None,
        query: QuryParameters | None = None,
        body: RequestJsonBody | None = None,
    ) -> ResponseModelBody:
        ...

    @abstractmethod
    def close(self) -> None:
        ...

    @abstractmethod
    def __enter__(self) -> Self:
        ...

    @abstractmethod
    def __exit__(self, exc_type, exc_value, traceback) -> None:
        ...


class RequestRealClient(RequestClient):
    pass


class RequestMockClient(RequestClient):
    def __init__(self) -> None:
        self._store: list[tuple[tuple[Method, URL], Model | RestrunError]] = []

    def inject_get_response_body(
        self,
        url: URL,
        response_body: Model | RestrunError,
    ):
        self._store.append((("GET", url), response_body))

    def inject_post_response_body(
        self,
        url: URL,
        response_body: Model | RestrunError,
    ):
        self._store.append((("POST", url), response_body))

    def inject_put_response_body(
        self,
        url: URL,
        response_body: Model | RestrunError,
    ):
        self._store.append((("PUT", url), response_body))

    def inject_patch_response_body(
        self,
        url: URL,
        response_body: Model | RestrunError,
    ):
        self._store.append((("PATCH", url), response_body))

    def inject_delete_response_body(
        self,
        url: URL,
        response_body: Model | RestrunError,
    ):
        self._store.append((("DELETE", url), response_body))

    def _extract_response_body(
        self, method: Method, url: URL, *, response_body_type: Type[ResponseModelBody]
    ) -> ResponseModelBody:
        if len(self._store) == 0:
            raise MockResponseNotFoundError()

        method_url, response_body = self._store.pop(0)
        expected_method, expected_url = method_url

        if method != expected_method or url != expected_url:
            raise MockRequestError(method, url, expected_method, expected_url)

        if isinstance(response_body, RestrunError):
            raise response_body

        if not isinstance(response_body, response_body_type):
            raise MockResponseTypeError(method, url, response_body, response_body_type)

        return response_body

    @override
    def get(
        self,
        url: URL,
        *,
        response_body_type: Type[ResponseModelBody],
        headers: Headers | None = None,
        query: QuryParameters | None = None,
    ) -> ResponseModelBody:
        return self._extract_response_body(
            "GET",
            url,
            response_body_type=response_body_type,
        )

    @override
    def post(
        self,
        url: URL,
        *,
        response_body_type: Type[ResponseModelBody],
        headers: Headers | None = None,
        query: QuryParameters | None = None,
        body: RequestJsonBody | None = None,
    ) -> ResponseModelBody:
        return self._extract_response_body(
            "POST",
            url,
            response_body_type=response_body_type,
        )

    @override
    def put(
        self,
        url: URL,
        *,
        response_body_type: Type[ResponseModelBody],
        headers: Headers | None = None,
        query: QuryParameters | None = None,
        body: RequestJsonBody | None = None,
    ) -> ResponseModelBody:
        return self._extract_response_body(
            "PUT",
            url,
            response_body_type=response_body_type,
        )

    @override
    def patch(
        self,
        url: URL,
        *,
        response_body_type: Type[ResponseModelBody],
        headers: Headers | None = None,
        query: QuryParameters | None = None,
        body: RequestJsonBody | None = None,
    ) -> ResponseModelBody:
        return self._extract_response_body(
            "PATCH",
            url,
            response_body_type=response_body_type,
        )

    @override
    def delete(
        self,
        url: URL,
        *,
        response_body_type: Type[ResponseModelBody],
        headers: Headers | None = None,
        query: QuryParameters | None = None,
        body: RequestJsonBody | None = None,
    ) -> ResponseModelBody:
        return self._extract_response_body(
            "DELETE",
            url,
            response_body_type=response_body_type,
        )

    def close(self) -> None:
        if len(self._store) != 0:
            raise MockResponseBodyRemainsError()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()
