from dataclasses import dataclass
from logging import getLogger
from pathlib import Path
from typing import NotRequired, Type, TypedDict, cast

from restrun.core.operation import (
    DeleteOperation,
    GetOperation,
    Operation,
    PatchOperation,
    PostOperation,
    PutOperation,
    get_method,
)
from restrun.exceptions import DuplicateOperationTypeError, OperationURLInvalidError
from restrun.generator import ClassInfo, find_classes_from_code
from restrun.strcase import class_name


logger = getLogger(__name__)


class OperationMethodMap(TypedDict):
    GET: NotRequired[ClassInfo[GetOperation]]
    POST: NotRequired[ClassInfo[PostOperation]]
    PUT: NotRequired[ClassInfo[PutOperation]]
    PATCH: NotRequired[ClassInfo[PatchOperation]]
    DELETE: NotRequired[ClassInfo[DeleteOperation]]


@dataclass(frozen=True)
class ResourceContext:
    module_name: str
    path: str
    operation_map: OperationMethodMap

    @property
    def class_name(self) -> str:
        return class_name(self.module_name) + "Resource"

    @property
    def operations(self) -> list[ClassInfo[Operation]]:
        return [
            cast(ClassInfo[Operation], operation_info)
            for operation_info in self.operation_map.values()
        ]

    @property
    def get_request(self) -> ClassInfo[GetOperation] | None:
        return self.operation_map.get("GET")

    @property
    def post_request(self) -> ClassInfo[PostOperation] | None:
        return self.operation_map.get("POST")

    @property
    def put_request(self) -> ClassInfo[PutOperation] | None:
        return self.operation_map.get("PUT")

    @property
    def patch_request(self) -> ClassInfo[PatchOperation] | None:
        return self.operation_map.get("PATCH")

    @property
    def delete_request(self) -> ClassInfo[DeleteOperation] | None:
        return self.operation_map.get("DELETE")

    @property
    def has_get_method(self) -> bool:
        return self.get_request is not None

    @property
    def has_post_method(self) -> bool:
        return self.post_request is not None

    @property
    def has_put_method(self) -> bool:
        return self.put_request is not None

    @property
    def has_patch_method(self) -> bool:
        return self.patch_request is not None

    @property
    def has_delete_method(self) -> bool:
        return self.delete_request is not None


def make_resource_context(resource_dir: Path) -> ResourceContext | None:
    operation_class_infos: dict[Type[Operation], list[ClassInfo[Operation]]] = {
        GetOperation: [],
        PostOperation: [],
        PutOperation: [],
        PatchOperation: [],
        DeleteOperation: [],
    }

    for operation_filepath in resource_dir.iterdir():
        if (
            not operation_filepath.is_file()
            or operation_filepath.suffix != ".py"
            or operation_filepath.name == "__init__.py"
        ):
            continue

        try:
            requests_map = find_classes_from_code(
                operation_filepath,
                GetOperation,
                PostOperation,
                PutOperation,
                PatchOperation,
                DeleteOperation,
            )
        except Exception as error:
            logger.warning(error)
            continue

        for operation_type in [
            GetOperation,
            PostOperation,
            PutOperation,
            PatchOperation,
        ]:
            operation_class_infos[operation_type].extend(requests_map[operation_type])

    resource_context = ResourceContext(
        module_name=resource_dir.name,
        path="",
        operation_map={},
    )
    for operation_type, class_infos in operation_class_infos.items():
        match len(class_infos):
            case 0:
                continue

            case 1:
                method = get_method(operation_type)
                resource_context.operation_map[method] = class_infos[0]  # type: ignore

            case _:
                raise DuplicateOperationTypeError(
                    get_method(operation_type),
                    operation_type.path,
                    class_infos,
                )

    paths = set(
        cast(ClassInfo[Operation], request).class_type.path
        for request in resource_context.operation_map.values()
    )

    match len(paths):
        case 0:
            return None

        case 1:
            return ResourceContext(
                module_name=resource_context.module_name,
                path=next(iter(paths)),
                operation_map=resource_context.operation_map,
            )

        case _:
            raise OperationURLInvalidError(resource_context.operations)
