from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Self

from restrun.core import http
from restrun.core.model import Model
from restrun.core.request import RequestMockClient
from restrun.exception import RestrunError

if TYPE_CHECKING:
    from restrun.core.resource import Resource


class RestrunClient(ABC):
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
        raise NotImplementedError()

    def inject_post_response_body(
        self, url: http.Method, response_body: Model | RestrunError
    ) -> Self:
        self._client.inject_post_response_body(url, response_body)

        raise NotImplementedError()

    def inject_put_response_body(
        self, url: http.Method, response_body: Model | RestrunError
    ) -> Self:
        self._client.inject_put_response_body(url, response_body)

        raise NotImplementedError()

    def inject_patch_response_body(
        self, url: http.Method, response_body: Model | RestrunError
    ) -> Self:
        self._client.inject_patch_response_body(url, response_body)

        raise NotImplementedError()

    def inject_delete_response_body(
        self, url: http.Method, response_body: Model | RestrunError
    ) -> Self:
        self._client.inject_delete_response_body(url, response_body)

        raise NotImplementedError()


class RestrunMockClientMixin(RestrunMockClient):
    pass
