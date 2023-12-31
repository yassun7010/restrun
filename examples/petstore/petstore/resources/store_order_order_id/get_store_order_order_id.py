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

import typing_extensions
from restrun.core import http
from restrun.core.operation import (
    GetOperation,
)

from ...schemas import order


class StoreOrderOrderIdJsonResponse(typing_extensions.TypedDict):
    pass


class GetStoreOrderOrderIdResponseBody(order.Order):
    pass


class GetStoreOrderOrderId(GetOperation):
    @classmethod
    @property
    def path(cls) -> "http.URL":
        return "/store/order/{orderId}"

    def get(
        self,
        orderId: "int",
    ) -> "GetStoreOrderOrderIdResponseBody":
        """
        Find purchase order by ID

        For valid response try integer IDs with value <= 5 or > 10. Other values will
        generate exceptions.
        """

        return self._client.get(
            self.path,
            response_type=GetStoreOrderOrderIdResponseBody,
        )
