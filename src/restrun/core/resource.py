from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from restrun.core import http


if TYPE_CHECKING:
    from restrun.core.client import RequestClient


class Resource(ABC):
    def __init__(self, client: "RequestClient") -> None:
        self._client = client

    @classmethod
    @property
    @abstractmethod
    def path(cls) -> http.URL:
        ...
