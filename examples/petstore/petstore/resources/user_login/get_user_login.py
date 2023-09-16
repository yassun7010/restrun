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


class UserLoginQueryParameters(typing_extensions.TypedDict):
    username: "typing.NotRequired[str]"

    password: "typing.NotRequired[str]"


class UserLoginJsonResponse(typing_extensions.TypedDict):
    pass


GetUserLoginResponseBody = str


class GetUserLogin(GetOperation):
    @classmethod
    @property
    def path(cls) -> "http.URL":
        return "/user/login"

    def get(
        self,
        query: "UserLoginQueryParameters| None" = None,
    ) -> "GetUserLoginResponseBody":
        """
        Logs user into the system
        """

        return self._client.get(
            self.path,
            response_type=GetUserLoginResponseBody,
            query=query,
        )