from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Self

from restrun.core import http
from restrun.core.model import Model
from restrun.core.request import RequestMockClient
from restrun.exception import RestrunError

if TYPE_CHECKING:
    from restrun.core.request import RequestClient
    from restrun.core.resource import Resource


class RestrunClient(ABC):
    @property
    def _client(self) -> "RequestClient":
        ...

    @abstractmethod
    def request(self, url: str) -> "Resource":
        ...


class RestrunClientMixin(RestrunClient):
    pass


class RestrunRealClient(RestrunClient):
    pass


class RestrunRealClientMixin(RestrunRealClient):
    pass


class RestrunMockClient(RestrunClient):
    def __init__(self) -> None:
        self._client = RequestMockClient()

    def inject_get_response_body(
        self, url: http.Method, response_body: Model | RestrunError
    ) -> Self:
        raise NotImplementedError(
            "RestrunMockClient.inject_get_response_body is not implemented."
        )

    def inject_post_response_body(
        self, url: http.Method, response_body: Model | RestrunError
    ) -> Self:
        raise NotImplementedError(
            "RestrunMockClient.inject_post_response_body is not implemented."
        )

    def inject_put_response_body(
        self, url: http.Method, response_body: Model | RestrunError
    ) -> Self:
        raise NotImplementedError(
            "RestrunMockClient.inject_put_response_body is not implemented."
        )

    def inject_patch_response_body(
        self, url: http.Method, response_body: Model | RestrunError
    ) -> Self:
        raise NotImplementedError(
            "RestrunMockClient.inject_patch_response_body is not implemented."
        )

    def inject_delete_response_body(
        self, url: http.Method, response_body: Model | RestrunError
    ) -> Self:
        raise NotImplementedError(
            "RestrunMockClient.inject_delete_response_body is not implemented."
        )


class RestrunMockClientMixin(RestrunMockClient):
    pass
