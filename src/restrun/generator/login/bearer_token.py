from abc import abstractmethod


class BearerTokenLogin:
    @classmethod
    @abstractmethod
    def from_bearer_token(cls, bearer_token: str) -> None:
        ...
