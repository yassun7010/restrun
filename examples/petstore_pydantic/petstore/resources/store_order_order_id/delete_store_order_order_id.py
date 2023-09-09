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

DeleteStoreOrderOrderIdResponseBody = typing.Literal[None]


class DeleteStoreOrderOrderId(DeleteOperation):
    @classmethod
    @property
    def path(cls) -> "http.URL":
        return "/store/order/{orderId}"

    def delete(
        self,
    ) -> "DeleteStoreOrderOrderIdResponseBody":
        """
        Delete purchase order by ID

        For valid response try integer IDs with value < 1000. Anything above
        1000 or nonintegers will generate API errors
        """

        return self._client.get(
            self.path,
            response_body_type=DeleteStoreOrderOrderIdResponseBody,
        )
