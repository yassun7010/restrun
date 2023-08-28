from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from restrun.core import http

if TYPE_CHECKING:
    from restrun.core.request import RequestClient


class Resource(ABC):
    def __init__(self, client: "RequestClient") -> None:
        self._client = client

    @property
    @classmethod
    @abstractmethod
    def url(cls) -> http.URL:
        ...
