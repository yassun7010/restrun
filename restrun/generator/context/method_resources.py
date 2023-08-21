from typing import Iterator

from pydantic import Field

from restrun.core.endpoint import EndpointMethod
from restrun.core.model import ExtraForbidModel
from restrun.core.resource import ApiResource


class MethodResources(ExtraForbidModel):
    get: list[ApiResource] = Field(default_factory=list)
    post: list[ApiResource] = Field(default_factory=list)
    put: list[ApiResource] = Field(default_factory=list)
    patch: list[ApiResource] = Field(default_factory=list)
    delete: list[ApiResource] = Field(default_factory=list)

    def __iter__(
        self,
    ) -> Iterator[tuple[EndpointMethod, list[ApiResource]]]:
        return iter(
            [
                ("GET", self.get),
                ("POST", self.post),
                ("PUT", self.put),
                ("PATCH", self.patch),
                ("DELETE", self.delete),
            ]
        )
