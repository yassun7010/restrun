from restrun.core.client import (
    RestrunClientMixin,
    RestrunMockClientMixin,
    RestrunRealClientMixin,
)


class RealBearTokenLoginMixin(RestrunRealClientMixin):
    @classmethod
    def from_bearer_token(cls, token: str):
        raise NotImplementedError()


class MockBearTokenLoginMixin(RestrunMockClientMixin):
    @classmethod
    def from_bearer_token(cls, token: str):
        from ..mock_client import PetstoreMockClient

        return PetstoreMockClient()


class BearerTokenLoginMixin(RestrunClientMixin):
    @classmethod
    def from_bearer_token(cls, token: str):
        return RealBearTokenLoginMixin.from_bearer_token(token)
