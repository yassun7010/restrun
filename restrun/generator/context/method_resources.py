from typing import Iterator

from pydantic import Field

from restrun.core.model import ExtraForbidModel
from restrun.core.request import RequestMethod, RequestResource


class RequestResourceMap(ExtraForbidModel):
    get: list[RequestResource] = Field(default_factory=list)
    post: list[RequestResource] = Field(default_factory=list)
    put: list[RequestResource] = Field(default_factory=list)
    patch: list[RequestResource] = Field(default_factory=list)
    delete: list[RequestResource] = Field(default_factory=list)

    def __iter__(
        self,
    ) -> Iterator[tuple[RequestMethod, list[RequestResource]]]:
        return iter(
            [
                ("GET", self.get),
                ("POST", self.post),
                ("PUT", self.put),
                ("PATCH", self.patch),
                ("DELETE", self.delete),
            ]
        )
