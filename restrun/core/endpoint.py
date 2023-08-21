from dataclasses import dataclass

from typing_extensions import Literal

from restrun.core.http import URL

EndpointMethod = Literal[
    "DELETE",
    "GET",
    "PATCH",
    "POST",
    "PUT",
]


@dataclass(frozen=True)
class Endpoint:
    method: EndpointMethod
    url: URL
