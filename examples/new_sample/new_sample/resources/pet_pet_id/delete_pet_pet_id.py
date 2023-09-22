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

from restrun.core import http
from restrun.core.operation import (
    DeleteOperation,
)

DeletePetPetIdResponseBody = typing.Literal[None]


class DeletePetPetId(DeleteOperation):
    @classmethod
    @property
    def path(cls) -> "http.URL":
        return "/pet/{petId}"

    def delete(
        self,
        petId: "int",
    ) -> "DeletePetPetIdResponseBody":
        """
        Deletes a pet
        """

        return self._client.delete(
            self.path,
            response_type=DeletePetPetIdResponseBody,
        )
