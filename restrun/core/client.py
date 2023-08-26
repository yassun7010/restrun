from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from restrun.core.resource import Resource


class RestrunClient(ABC):
    @abstractmethod
    def request(self, url: str) -> "Resource":
        ...


class RestrunClientMixin:
    pass


class RestrunMockClient(RestrunClient):
    pass


class RestrunMockClientMixin:
    pass
