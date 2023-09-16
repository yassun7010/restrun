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
    GetOperation,
)

from ...schemas import pet


class PetFindByStatusQueryParameters(typing_extensions.TypedDict):
    status: "typing.NotRequired[typing.Literal['available','pending','sold']]"


class PetFindByStatusJsonResponse(typing_extensions.TypedDict):
    pass


GetPetFindByStatusResponseBody = list[pet.Pet]


class GetPetFindByStatus(GetOperation):
    @classmethod
    @property
    def path(cls) -> "http.URL":
        return "/pet/findByStatus"

    def get(
        self,
        query: "PetFindByStatusQueryParameters| None" = None,
    ) -> "GetPetFindByStatusResponseBody":
        """
        Finds Pets by status

        Multiple status values can be provided with comma separated strings
        """

        return self._client.get(
            self.path,
            response_type=GetPetFindByStatusResponseBody,
            query=query,
        )
