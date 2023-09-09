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
    PutOperation,
)

PutUserUsernameResponseBody = typing.Literal[None]


class PutUserUsername(PutOperation):
    @classmethod
    @property
    def path(cls) -> "http.URL":
        return "/user/{username}"

    def put(
        self,
    ) -> "PutUserUsernameResponseBody":
        """
        Update user

        This can only be done by the logged in user.
        """

        return self._client.get(
            self.path,
            response_body_type=PutUserUsernameResponseBody,
        )
