from dataclasses import dataclass
from typing import Self

from restrun.config.v1.source.openapi_source import V1OpenAPISource
from restrun.exceptions import NeverReachError
from restrun.openapi.openapi import OpenAPI
from restrun.openapi.schema import (
    PythonArray,
    PythonCustomStr,
    PythonLiteralType,
    PythonLiteralUnion,
    PythonNamedDataType,
    PythonObject,
    PythonReference,
    PythonSchema,
    get_import_modules,
    get_named_schema,
    get_schemas,
)
from restrun.strcase import module_name


@dataclass(frozen=True)
class SchemaContext:
    file_name: str
    data_type: PythonNamedDataType

    @property
    def type_name(self) -> str:
        return self.data_type.type_name

    @property
    def type(self) -> str:
        match self.data_type:
            case PythonSchema():
                data_type = self.data_type.data_type
                match data_type:
                    case PythonLiteralType():
                        return data_type.name.lower()

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
        if isinstance(self.data_type, PythonSchema):
            return isinstance(self.data_type.data_type, PythonLiteralType)
        else:
            return False

    @property
    def array_item_schema(self) -> Self | None:
        if not isinstance(self.data_type, PythonSchema):
            return None

        data_type = self.data_type.data_type
        if not isinstance(data_type, PythonArray):
            return None

        item_type_name = self.type_name + "Item"
        item_data_type = data_type.item_data_type

        match item_data_type:
            case PythonObject():
                item_data_type = item_data_type

            case PythonReference():
                item_data_type = item_data_type

            case PythonSchema():
                item_data_type = item_data_type

            case _:
                item_data_type = PythonSchema(item_type_name, item_data_type)

        return SchemaContext(
            file_name=self.file_name,
            data_type=item_data_type,
        )

    @property
    def title_and_description(self) -> str | None:
        if isinstance(self.data_type, PythonReference):
            return None

        return self.data_type.title_and_description

    @property
    def import_field_types(self) -> list[str]:
        return get_import_modules(self.data_type)


def make_schema_contexts(source: V1OpenAPISource) -> list[SchemaContext]:
    return [
        SchemaContext(
            file_name=module_name(schema.name),
            data_type=get_named_schema(schema.name, schema.data_type),
        )
        for schema in get_schemas(OpenAPI.from_url(source.location))
    ]
