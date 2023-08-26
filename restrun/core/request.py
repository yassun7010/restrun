from abc import abstractmethod
from dataclasses import dataclass

from typing_extensions import Literal

from restrun.core.http import URL
from restrun.core.resource import Resource

RequestMethod = Literal[
    "DELETE",
    "GET",
    "PATCH",
    "POST",
    "PUT",
]


@dataclass(frozen=True)
class Request:
    method: RequestMethod
    url: URL


class RequestResource(Resource):
    @classmethod
    @abstractmethod
    def request(cls) -> Request:
        ...
