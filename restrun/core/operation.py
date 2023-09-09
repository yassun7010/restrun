from typing import Type, Union

from restrun.core.http import (
    Method,
)
from restrun.core.resource import Resource
from restrun.exception import (
    UnknownOperationTypeError,
)


class Operation(Resource):
    pass


class GetOperation(Operation):
    pass


class PostOperation(Operation):
    pass


class PutOperation(Operation):
    pass


class PatchOperation(Operation):
    pass


class DeleteOperation(Operation):
    pass


def get_method(request: Type[Operation]) -> Method:
    if issubclass(request, GetOperation):
        return "GET"
    elif issubclass(request, PostOperation):
        return "POST"
    elif issubclass(request, PutOperation):
        return "PUT"
    elif issubclass(request, PatchOperation):
        return "PATCH"
    elif issubclass(request, DeleteOperation):
        return "DELETE"
    else:
        raise UnknownOperationTypeError(request)


def downcast(
    request: Union[
        DeleteOperation,
        GetOperation,
        PatchOperation,
        PostOperation,
        PutOperation,
    ]
) -> Operation:
    return request
