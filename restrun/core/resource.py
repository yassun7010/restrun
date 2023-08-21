class HttpClient:
    pass


class ApiResource:
    def __init__(self, client: HttpClient) -> None:
        self.client = client
