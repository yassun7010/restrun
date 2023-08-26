from abc import ABC


class HttpClient:
    pass


class Resource(ABC):
    def __init__(self, client: HttpClient) -> None:
        self.client = client
