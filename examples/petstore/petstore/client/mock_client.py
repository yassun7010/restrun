#
# Code generated by restrun "0.1.0".
#
# Removing this comment from this file will exclude it from automatic generation target
# and it will not be updated.
# If you wish to make special modifications to the auto-generated code,
# please remove this comment.
#
# For more information about restrun,
# please refer to https://github.com/yassun7010/restrun .
#

from restrun.core.client import RestrunMockClient

from .client import PetstoreClient
from .mixins import (
    bearer_token_login_mixin,
)


class PetstoreMockClient(
    bearer_token_login_mixin.MockBearTokenLoginMixin, RestrunMockClient, PetstoreClient
):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def request(self, url):
        raise NotImplementedError()
