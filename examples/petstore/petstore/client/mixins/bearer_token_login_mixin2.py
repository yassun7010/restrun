from restrun.core.client import RestrunClientMixin


class BearerTokenLoginMixin(RestrunClientMixin):
    def from_bearer_token(self, token: str):
        ...
