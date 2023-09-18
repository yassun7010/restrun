from dataclasses import dataclass
from typing import Self

from restrun.config.v1.source.openapi_source import V1OpenAPISource
from restrun.exceptions import NeverReachError
from restrun.openapi.openapi import OpenAPI
from restrun.openapi.schema import (
    PythonArray,
    PythonCustomStr,
    PythonDataType,
    PythonLiteralType,
    PythonLiteralUnion,
    PythonObject,
    PythonReference,
    get_import_modules,
    get_schemas,
)
from restrun.strcase import class_name, module_name


@dataclass(frozen=True)
class SchemaContext:
    type_name: str
    file_name: str
    data_type: PythonDataType

    @property
    def type(self) -> str:
        match self.data_type:
            case PythonLiteralType():
                return self.data_type.name.lower()

            case PythonCustomStr():
                return "custom_str"

            case PythonLiteralUnion():
                return "literal_union"

            case PythonArray():
                return "array"

            case PythonObject():
                return "object"

            case PythonReference():
                return "ref"

            case _:
                raise NeverReachError(self.data_type)

    @property
    def is_literal_type(self) -> bool:
        return isinstance(self.data_type, PythonLiteralType)

    @property
    def array_item_schema(self) -> Self | None:
        if not isinstance(self.data_type, PythonArray):
            return None

        return SchemaContext(
            type_name=self.type_name,
            file_name=self.file_name,
            data_type=self.data_type.item_data_type,
        )

    @property
    def import_field_types(self) -> list[str]:
        return get_import_modules(self.data_type)


def make_schema_contexts(source: V1OpenAPISource) -> list[SchemaContext]:
    return [
        SchemaContext(
            type_name=class_name(schema.name),
            file_name=module_name(schema.name),
            data_type=schema.data_type,
        )
        for schema in get_schemas(OpenAPI.from_url(source.location))
    ]
