from typing import Type, Union

from restrun.core.http import (
    Method,
)
from restrun.core.resource import Resource
from restrun.exceptions import (
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


def get_method(operation: Type[Operation]) -> Method:
    if issubclass(operation, GetOperation):
        return "GET"
    elif issubclass(operation, PostOperation):
        return "POST"
    elif issubclass(operation, PutOperation):
        return "PUT"
    elif issubclass(operation, PatchOperation):
        return "PATCH"
    elif issubclass(operation, DeleteOperation):
        return "DELETE"
    else:
        raise UnknownOperationTypeError(operation)


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
