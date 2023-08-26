from dataclasses import dataclass, field
from typing import Iterator

from restrun.core.request import (
    DeleteRequest,
    GetRequest,
    PatchRequest,
    PostRequest,
    PutRequest,
    Request,
    RequestMethod,
    downcast,
)


@dataclass(frozen=True)
class RequestResourceMap:
    get_requests: list[GetRequest] = field(default_factory=list)
    post_requests: list[PostRequest] = field(default_factory=list)
    put_requests: list[PutRequest] = field(default_factory=list)
    patch_requests: list[PatchRequest] = field(default_factory=list)
    delete_requests: list[DeleteRequest] = field(default_factory=list)

    def __iter__(
        self,
    ) -> Iterator[tuple[RequestMethod, Iterator[Request]]]:
        return iter(
            [
                ("GET", map(downcast, self.get_requests)),
                ("POST", map(downcast, self.post_requests)),
                ("PUT", map(downcast, self.put_requests)),
                ("PATCH", map(downcast, self.patch_requests)),
                ("DELETE", map(downcast, self.delete_requests)),
            ]
        )
