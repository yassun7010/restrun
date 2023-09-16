from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Literal, Self, overload

from typing_extensions import override

from restrun.core import http
from restrun.core.http import (
    URL,
    Headers,
    Method,
    QuryParameters,
    RequestJsonBody,
    ResponseDictBody,
    ResponseModelBody,
    Response,
)
from restrun.exceptions import (
    MockRequestError,
    MockResponseBodyRemainsError,
    MockResponseNotFoundError,
    MockResponseError,
    RestrunError,
)

if TYPE_CHECKING:
    from restrun.core.resource import Resource


class RestrunClient(ABC):
    @property
    def _client(self) -> "RequestClient":
        ...

    @abstractmethod
    def resource(self, url: str) -> "Resource":
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

    def inject_get_response(
        self,
        url: http.URL,
        *,
        response: "Response | RestrunError",
    ) -> Self:
        raise NotImplementedError(
            "RestrunMockClient.inject_get_response is not implemented."
        )

    def inject_post_response(
        self,
        url: http.URL,
        *,
        response: "Response | RestrunError",
    ) -> Self:
        raise NotImplementedError(
            "RestrunMockClient.inject_post_response is not implemented."
        )

    def inject_put_response(
        self,
        url: http.URL,
        *,
        response: "Response | RestrunError",
    ) -> Self:
        raise NotImplementedError(
            "RestrunMockClient.inject_put_response is not implemented."
        )

    def inject_patch_response(
        self,
        url: http.URL,
        *,
        response: "Response | RestrunError",
    ) -> Self:
        raise NotImplementedError(
            "RestrunMockClient.inject_patch_response is not implemented."
        )

    def inject_delete_response(
        self,
        url: http.URL,
        *,
        response: "Response | RestrunError",
    ) -> Self:
        raise NotImplementedError(
            "RestrunMockClient.inject_delete_response is not implemented."
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
        response_type: type[None],
        headers: Headers | None = None,
        query: QuryParameters | None = None,
    ) -> Literal[None]:
        ...

    @overload
    @abstractmethod
    def get(
        self,
        url: URL,
        *,
        response_type: type[str],
        headers: Headers | None = None,
        query: QuryParameters | None = None,
    ) -> str:
        ...

    @overload
    @abstractmethod
    def get(
        self,
        url: URL,
        *,
        response_type: type[list[str]],
        headers: Headers | None = None,
        query: QuryParameters | None = None,
    ) -> list[str]:
        ...

    @overload
    @abstractmethod
    def get(
        self,
        url: URL,
        *,
        response_type: type[ResponseDictBody],
        headers: Headers | None = None,
        query: QuryParameters | None = None,
    ) -> ResponseDictBody:
        ...

    @overload
    @abstractmethod
    def get(
        self,
        url: URL,
        *,
        response_type: type[list[ResponseDictBody]],
        headers: Headers | None = None,
        query: QuryParameters | None = None,
    ) -> list[ResponseDictBody]:
        ...

    @overload
    @abstractmethod
    def get(
        self,
        url: URL,
        *,
        response_type: type[ResponseModelBody],
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
        response_type: type[list[ResponseModelBody]],
        headers: Headers | None = None,
        query: QuryParameters | None = None,
    ) -> list[ResponseModelBody]:
        ...

    @abstractmethod
    def get(
        self,
        url,
        *,
        response_type: type[Response],
        headers=None,
        query=None,
    ) -> Response:
        ...

    @overload
    @abstractmethod
    def post(
        self,
        url: URL,
        *,
        response_type: type[None],
        headers: Headers | None = None,
        query: QuryParameters | None = None,
        body: RequestJsonBody | None = None,
    ) -> Literal[None]:
        ...

    @overload
    @abstractmethod
    def post(
        self,
        url: URL,
        *,
        response_type: type[str],
        headers: Headers | None = None,
        query: QuryParameters | None = None,
        body: RequestJsonBody | None = None,
    ) -> str:
        ...

    @overload
    @abstractmethod
    def post(
        self,
        url: URL,
        *,
        response_type: type[list[str]],
        headers: Headers | None = None,
        query: QuryParameters | None = None,
        body: RequestJsonBody | None = None,
    ) -> list[str]:
        ...

    @overload
    @abstractmethod
    def post(
        self,
        url: URL,
        *,
        response_type: type[ResponseDictBody],
        headers: Headers | None = None,
        query: QuryParameters | None = None,
        body: RequestJsonBody | None = None,
    ) -> ResponseDictBody:
        ...

    @overload
    @abstractmethod
    def post(
        self,
        url: URL,
        *,
        response_type: type[list[ResponseDictBody]],
        headers: Headers | None = None,
        query: QuryParameters | None = None,
        body: RequestJsonBody | None = None,
    ) -> list[ResponseDictBody]:
        ...

    @overload
    @abstractmethod
    def post(
        self,
        url: URL,
        *,
        response_type: type[ResponseModelBody],
        headers: Headers | None = None,
        query: QuryParameters | None = None,
        body: RequestJsonBody | None = None,
    ) -> ResponseModelBody:
        ...

    @overload
    @abstractmethod
    def post(
        self,
        url: URL,
        *,
        response_type: type[list[ResponseModelBody]],
        headers: Headers | None = None,
        query: QuryParameters | None = None,
        body: RequestJsonBody | None = None,
    ) -> list[ResponseModelBody]:
        ...

    @abstractmethod
    def post(
        self,
        url: URL,
        *,
        response_type: type[Response],
        headers: Headers | None = None,
        query: QuryParameters | None = None,
        body: RequestJsonBody | None = None,
    ) -> Response:
        ...

    @overload
    @abstractmethod
    def put(
        self,
        url: URL,
        *,
        response_type: type[None],
        headers: Headers | None = None,
        query: QuryParameters | None = None,
        body: RequestJsonBody | None = None,
    ) -> Literal[None]:
        ...

    @overload
    @abstractmethod
    def put(
        self,
        url: URL,
        *,
        response_type: type[str],
        headers: Headers | None = None,
        query: QuryParameters | None = None,
        body: RequestJsonBody | None = None,
    ) -> str:
        ...

    @overload
    @abstractmethod
    def put(
        self,
        url: URL,
        *,
        response_type: type[list[str]],
        headers: Headers | None = None,
        query: QuryParameters | None = None,
        body: RequestJsonBody | None = None,
    ) -> list[str]:
        ...

    @overload
    @abstractmethod
    def put(
        self,
        url: URL,
        *,
        response_type: type[ResponseDictBody],
        headers: Headers | None = None,
        query: QuryParameters | None = None,
        body: RequestJsonBody | None = None,
    ) -> ResponseDictBody:
        ...

    @overload
    @abstractmethod
    def put(
        self,
        url: URL,
        *,
        response_type: type[list[ResponseDictBody]],
        headers: Headers | None = None,
        query: QuryParameters | None = None,
        body: RequestJsonBody | None = None,
    ) -> list[ResponseDictBody]:
        ...

    @overload
    @abstractmethod
    def put(
        self,
        url: URL,
        *,
        response_type: type[ResponseModelBody],
        headers: Headers | None = None,
        query: QuryParameters | None = None,
        body: RequestJsonBody | None = None,
    ) -> ResponseModelBody:
        ...

    @overload
    @abstractmethod
    def put(
        self,
        url: URL,
        *,
        response_type: type[list[ResponseModelBody]],
        headers: Headers | None = None,
        query: QuryParameters | None = None,
        body: RequestJsonBody | None = None,
    ) -> list[ResponseModelBody]:
        ...

    @abstractmethod
    def put(
        self,
        url: URL,
        *,
        response_type: type[Response],
        headers: Headers | None = None,
        query: QuryParameters | None = None,
        body: RequestJsonBody | None = None,
    ) -> Response:
        ...

    @overload
    @abstractmethod
    def patch(
        self,
        url: URL,
        *,
        response_type: type[None],
        headers: Headers | None = None,
        query: QuryParameters | None = None,
        body: RequestJsonBody | None = None,
    ) -> Literal[None]:
        ...

    @overload
    @abstractmethod
    def patch(
        self,
        url: URL,
        *,
        response_type: type[str],
        headers: Headers | None = None,
        query: QuryParameters | None = None,
        body: RequestJsonBody | None = None,
    ) -> str:
        ...

    @overload
    @abstractmethod
    def patch(
        self,
        url: URL,
        *,
        response_type: type[list[str]],
        headers: Headers | None = None,
        query: QuryParameters | None = None,
        body: RequestJsonBody | None = None,
    ) -> list[str]:
        ...

    @overload
    @abstractmethod
    def patch(
        self,
        url: URL,
        *,
        response_type: type[ResponseDictBody],
        headers: Headers | None = None,
        query: QuryParameters | None = None,
        body: RequestJsonBody | None = None,
    ) -> ResponseDictBody:
        ...

    @overload
    @abstractmethod
    def patch(
        self,
        url: URL,
        *,
        response_type: type[list[ResponseDictBody]],
        headers: Headers | None = None,
        query: QuryParameters | None = None,
        body: RequestJsonBody | None = None,
    ) -> list[ResponseDictBody]:
        ...

    @overload
    @abstractmethod
    def patch(
        self,
        url: URL,
        *,
        response_type: type[ResponseModelBody],
        headers: Headers | None = None,
        query: QuryParameters | None = None,
        body: RequestJsonBody | None = None,
    ) -> ResponseModelBody:
        ...

    @overload
    @abstractmethod
    def patch(
        self,
        url: URL,
        *,
        response_type: type[list[ResponseModelBody]],
        headers: Headers | None = None,
        query: QuryParameters | None = None,
        body: RequestJsonBody | None = None,
    ) -> list[ResponseModelBody]:
        ...

    @abstractmethod
    def patch(
        self,
        url: URL,
        *,
        response_type: type[Response],
        headers: Headers | None = None,
        query: QuryParameters | None = None,
        body: RequestJsonBody | None = None,
    ) -> Response:
        ...

    @overload
    @abstractmethod
    def delete(
        self,
        url: URL,
        *,
        response_type: type[None],
        headers: Headers | None = None,
        query: QuryParameters | None = None,
        body: RequestJsonBody | None = None,
    ) -> Literal[None]:
        ...

    @overload
    @abstractmethod
    def delete(
        self,
        url: URL,
        *,
        response_type: type[str],
        headers: Headers | None = None,
        query: QuryParameters | None = None,
        body: RequestJsonBody | None = None,
    ) -> str:
        ...

    @overload
    @abstractmethod
    def delete(
        self,
        url: URL,
        *,
        response_type: type[list[str]],
        headers: Headers | None = None,
        query: QuryParameters | None = None,
        body: RequestJsonBody | None = None,
    ) -> list[str]:
        ...

    @overload
    @abstractmethod
    def delete(
        self,
        url: URL,
        *,
        response_type: type[ResponseDictBody],
        headers: Headers | None = None,
        query: QuryParameters | None = None,
        body: RequestJsonBody | None = None,
    ) -> ResponseDictBody:
        ...

    @overload
    @abstractmethod
    def delete(
        self,
        url: URL,
        *,
        response_type: type[list[ResponseDictBody]],
        headers: Headers | None = None,
        query: QuryParameters | None = None,
        body: RequestJsonBody | None = None,
    ) -> list[ResponseDictBody]:
        ...

    @overload
    @abstractmethod
    def delete(
        self,
        url: URL,
        *,
        response_type: type[ResponseModelBody],
        headers: Headers | None = None,
        query: QuryParameters | None = None,
        body: RequestJsonBody | None = None,
    ) -> ResponseModelBody:
        ...

    @overload
    @abstractmethod
    def delete(
        self,
        url: URL,
        *,
        response_type: type[list[ResponseModelBody]],
        headers: Headers | None = None,
        query: QuryParameters | None = None,
        body: RequestJsonBody | None = None,
    ) -> list[ResponseModelBody]:
        ...

    @abstractmethod
    def delete(
        self,
        url: URL,
        *,
        response_type: type[Response],
        headers: Headers | None = None,
        query: QuryParameters | None = None,
        body: RequestJsonBody | None = None,
    ) -> Response:
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
        self._store: list[tuple[tuple[Method, URL], "Response | RestrunError"]] = []

    def inject_get_response(
        self,
        url: URL,
        response: "Response | RestrunError",
    ):
        self._store.append((("GET", url), response))

    def inject_post_response(
        self,
        url: URL,
        response: "Response | RestrunError",
    ):
        self._store.append((("POST", url), response))

    def inject_put_response(
        self,
        url: URL,
        response: "Response | RestrunError",
    ):
        self._store.append((("PUT", url), response))

    def inject_patch_response(
        self,
        url: URL,
        response: "Response | RestrunError",
    ):
        self._store.append((("PATCH", url), response))

    def inject_delete_response(
        self,
        url: URL,
        response: "Response | RestrunError",
    ):
        self._store.append((("DELETE", url), response))

    def _extract_response(
        self, method: Method, url: URL, *, response_type: type[Response]
    ) -> Response:
        if len(self._store) == 0:
            raise MockResponseNotFoundError()

        method_url, response = self._store.pop(0)
        expected_method, expected_url = method_url

        if method != expected_method or url != expected_url:
            raise MockRequestError(method, url, expected_method, expected_url)

        if isinstance(response, RestrunError):
            raise response

        if not isinstance(response, response_type):
            raise MockResponseError(method, url, response, response_type)

        return response

    @override
    def get(
        self,
        url: URL,
        *,
        response_type: type[Response],
        headers: Headers | None = None,
        query: QuryParameters | None = None,
    ) -> Response:
        return self._extract_response(
            "GET",
            url,
            response_type=response_type,
        )

    @override
    def post(
        self,
        url: URL,
        *,
        response_type: type[Response],
        headers: Headers | None = None,
        query: QuryParameters | None = None,
        body: RequestJsonBody | None = None,
    ) -> Response:
        return self._extract_response(
            "POST",
            url,
            response_type=response_type,
        )

    @override
    def put(
        self,
        url: URL,
        *,
        response_type: type[Response],
        headers: Headers | None = None,
        query: QuryParameters | None = None,
        body: RequestJsonBody | None = None,
    ) -> Response:
        return self._extract_response(
            "PUT",
            url,
            response_type=response_type,
        )

    @override
    def patch(
        self,
        url: URL,
        *,
        response_type: type[Response],
        headers: Headers | None = None,
        query: QuryParameters | None = None,
        body: RequestJsonBody | None = None,
    ) -> Response:
        return self._extract_response(
            "PATCH",
            url,
            response_type=response_type,
        )

    @override
    def delete(
        self,
        url: URL,
        *,
        response_type: type[Response],
        headers: Headers | None = None,
        query: QuryParameters | None = None,
        body: RequestJsonBody | None = None,
    ) -> Response:
        return self._extract_response(
            "DELETE",
            url,
            response_type=response_type,
        )

    def close(self) -> None:
        if len(self._store) != 0:
            raise MockResponseBodyRemainsError()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()
