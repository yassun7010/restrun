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


class PetFindByTagsQueryParameters(typing_extensions.TypedDict):
    tags: "typing.NotRequired[list[str]]"


class PetFindByTagsJsonResponse(typing_extensions.TypedDict):
    pass


GetPetFindByTagsResponseBody = list[pet.Pet]


class GetPetFindByTags(GetOperation):
    @classmethod
    @property
    def path(cls) -> "http.URL":
        return "/pet/findByTags"

    def get(
        self,
        query: "PetFindByTagsQueryParameters| None" = None,
    ) -> "GetPetFindByTagsResponseBody":
        """
        Finds Pets by tags

        Multiple tags can be provided with comma separated strings. Use tag1, tag2,
        tag3 for testing.
        """

        return self._client.get(
            self.path,
            response_type=GetPetFindByTagsResponseBody,
            query=query,
        )