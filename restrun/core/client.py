from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from restrun.core.resource import ApiResource


class RestrunClient(ABC):
    @abstractmethod
    def request(self, url: str) -> "ApiResource":
        ...


class RestrunMockClient(RestrunClient):
    pass
