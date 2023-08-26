from typing import Union

from typing_extensions import Literal, final

from restrun.core.resource import Resource

RequestMethod = Literal[
    "DELETE",
    "GET",
    "PATCH",
    "POST",
    "PUT",
]


class Request(Resource):
    pass


class GetRequest(Request):
    @property
    @final
    def has_get_method(self) -> bool:
        return True


class PostRequest(Request):
    @property
    @final
    def has_post_method(self) -> bool:
        return True


class PutRequest(Request):
    @property
    @final
    def has_put_method(self) -> bool:
        return True


class PatchRequest(Request):
    @property
    @final
    def has_patch_method(self) -> bool:
        return True


class DeleteRequest(Request):
    @property
    @final
    def has_delete_method(self) -> bool:
        return True


def downcast(
    request: Union[
        DeleteRequest,
        GetRequest,
        PatchRequest,
        PostRequest,
        PutRequest,
    ]
) -> Request:
    return request
