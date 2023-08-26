from abc import ABC, abstractmethod


class HttpClient:
    pass


class Resource(ABC):
    def __init__(self, client: HttpClient) -> None:
        self.client = client

    @property
    @classmethod
    @abstractmethod
    def url(cls) -> str:
        ...

    @property
    def has_get_method(self) -> bool:
        return False

    @property
    def has_post_method(self) -> bool:
        return False

    @property
    def has_put_method(self) -> bool:
        return False

    @property
    def has_patch_method(self) -> bool:
        return False

    @property
    def has_delete_method(self) -> bool:
        return False
