from abc import abstractmethod


class RestrunException(Exception):
    @property
    @abstractmethod
    def message(self) -> str:
        ...

    def __str__(self) -> str:
        return self.message


class RestrunError(RestrunException):
    pass


class MockResponseNotFound(RestrunError):
    @property
    def message(self) -> str:
        return "Mock response data does not found. Please set use `MockClient.inject_*` methods."
