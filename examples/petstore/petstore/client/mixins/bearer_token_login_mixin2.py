from restrun.core.client import RestrunClientMixin


class bearerTokenLoginMixin(RestrunClientMixin):
    def from_bearer_token(self, token: str):
        ...
