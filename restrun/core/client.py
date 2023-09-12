from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Literal, Self, Type, overload

from typing_extensions import override

from restrun.core import http
from restrun.core.http import (
    URL,
    Headers,
    Method,
    QuryParameters,
    RequestJsonBody,
    ResponseModelBody,
)
from restrun.core.model import Model
from restrun.exceptions import (
    MockRequestError,
    MockResponseBodyRemainsError,
    MockResponseNotFoundError,
    MockResponseTypeError,
    RestrunError,
)

if TYPE_CHECKING:
    from restrun.core.resource import Resource


class RestrunClient(ABC):
    @property
    def _client(self) -> "RequestClient":
        ...

    @abstractmethod
    def request(self, url: str) -> "Resource":
        ...

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> Self:
        self._client.__enter__()

        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self._client.__exit__(exc_type, exc_value, traceback)


class RestrunClientMixin(RestrunClient):
    pass


class RestrunRealClient(RestrunClient):
    pass


class RestrunRealClientMixin(RestrunRealClient):
    pass


class RestrunMockClient(RestrunClient):
    def __init__(self) -> None:
        self._mock_client = RequestMockClient()

    @property
    def _client(self) -> "RequestMockClient":
        return self._mock_client

    def inject_get_response_body(
        self, url: http.URL, response_body: Model | Literal[None] | RestrunError
    ) -> Self:
        raise NotImplementedError(
            "RestrunMockClient.inject_get_response_body is not implemented."
        )

    def inject_post_response_body(
        self, url: http.URL, response_body: Model | Literal[None] | RestrunError
    ) -> Self:
        raise NotImplementedError(
            "RestrunMockClient.inject_post_response_body is not implemented."
        )

    def inject_put_response_body(
        self, url: http.URL, response_body: Model | Literal[None] | RestrunError
    ) -> Self:
        raise NotImplementedError(
            "RestrunMockClient.inject_put_response_body is not implemented."
        )

    def inject_patch_response_body(
        self, url: http.URL, response_body: Model | Literal[None] | RestrunError
    ) -> Self:
        raise NotImplementedError(
            "RestrunMockClient.inject_patch_response_body is not implemented."
        )

    def inject_delete_response_body(
        self, url: http.URL, response_body: Model | Literal[None] | RestrunError
    ) -> Self:
        raise NotImplementedError(
            "RestrunMockClient.inject_delete_response_body is not implemented."
        )


class RestrunMockClientMixin(RestrunMockClient):
    pass


class RequestClient(ABC):
    @overload
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

    @overload
    @abstractmethod
    def get(
        self,
        url: URL,
        *,
        response_body_type: Type[None],
        headers: Headers | None = None,
        query: QuryParameters | None = None,
    ) -> None:
        ...

    @abstractmethod
    def get(
        self,
        url,
        *,
        response_body_type: Type[ResponseModelBody] | Type[None],
        headers=None,
        query=None,
    ) -> ResponseModelBody | None:
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
        self._store: list[
            tuple[tuple[Method, URL], Model | Literal[None] | RestrunError]
        ] = []

    def inject_get_response_body(
        self,
        url: URL,
        response_body: Model | Literal[None] | RestrunError,
    ):
        self._store.append((("GET", url), response_body))

    def inject_post_response_body(
        self,
        url: URL,
        response_body: Model | Literal[None] | RestrunError,
    ):
        self._store.append((("POST", url), response_body))

    def inject_put_response_body(
        self,
        url: URL,
        response_body: Model | Literal[None] | RestrunError,
    ):
        self._store.append((("PUT", url), response_body))

    def inject_patch_response_body(
        self,
        url: URL,
        response_body: Model | Literal[None] | RestrunError,
    ):
        self._store.append((("PATCH", url), response_body))

    def inject_delete_response_body(
        self,
        url: URL,
        response_body: Model | Literal[None] | RestrunError,
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
