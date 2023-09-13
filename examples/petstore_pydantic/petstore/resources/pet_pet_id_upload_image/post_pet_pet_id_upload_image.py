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
    PostOperation,
)

from ...schemas import api_response


class PetPetIdUploadImageQueryParameters(typing.TypedDict):
    additionalMetadata: "str"


class PetPetIdUploadImageJsonResponse(typing.TypedDict):
    pass


class PostPetPetIdUploadImageResponseBody(api_response.ApiResponse):
    pass


class PostPetPetIdUploadImage(PostOperation):
    @classmethod
    @property
    def path(cls) -> "http.URL":
        return "/pet/{petId}/uploadImage"

    def post(
        self,
        query: "PetPetIdUploadImageQueryParameters| None" = None,
    ) -> "PostPetPetIdUploadImageResponseBody":
        """
        uploads an image
        """

        return self._client.get(
            self.path,
            response_body_type=PostPetPetIdUploadImageResponseBody,
            query=query,
        )
