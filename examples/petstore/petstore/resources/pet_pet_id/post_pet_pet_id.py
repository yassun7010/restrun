#
# Code generated by restrun "0.1.0".
#
# Removing this comment from this file will exclude it from automatic generation target
# and it will not be updated, unless the file contents are empty.
# If you wish to make special modifications to the auto-generated code,
# please remove this comment.
#
# For more information about restrun,
# please refer to https://github.com/yassun7010/restrun .
#
import typing

import typing_extensions
from restrun.core import http
from restrun.core.operation import (
    PostOperation,
)


class PetPetIdQueryParameters(typing_extensions.TypedDict):
    name: "typing.NotRequired[str]"

    status: "typing.NotRequired[str]"


PostPetPetIdResponseBody = typing.Literal[None]


class PostPetPetId(PostOperation):
    @classmethod
    @property
    def path(cls) -> "http.URL":
        return "/pet/{petId}"

    def post(
        self,
        query: "PetPetIdQueryParameters| None" = None,
    ) -> "PostPetPetIdResponseBody":
        """
        Updates a pet in the store with form data
        """

        return self._client.post(
            self.path,
            response_type=PostPetPetIdResponseBody,
            query=query,
        )
