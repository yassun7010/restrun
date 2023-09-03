from enum import Enum
from typing import Self

from attr import dataclass

from restrun.exception import NeverReachError

from .openapi import (
    DataType,
    DataType_v3_0_3,
    DataType_v3_1_0,
    OpenAPI,
    Reference,
    Schema,
)


class PythonDataType(str, Enum):
    NONE = "None"
    INT = "int"
    FLOAT = "float"
    BOOL = "bool"
    STR = "str"
    DATATIME = "datetime"
    DATE = "date"
    TIME = "time"
    TIMEDELTA = "timedelta"
    ANY = "Any"
    DICT = "dict"
    LIST = "list"


class PythonDataTypeStr(str):
    @classmethod
    def from_schema(
        cls, schema: Schema | Reference, type: DataType | None = None
    ) -> PythonDataType | Self:
        if isinstance(schema, Reference):
            return PythonDataType.ANY
        schema_type = type or schema.type

        if schema_type:
            match schema_type:
                case list():
                    # NOTE: `openapi_pydantic` defined it case,
                    #       but we do not expect arrays to come.
                    return PythonDataTypeStr(
                        " | ".join(
                            [
                                cls.from_schema(schema, s)
                                for s in schema_type
                                if not isinstance(s, list)
                            ]
                        )
                    )

                case DataType_v3_1_0.NULL:
                    return PythonDataType.NONE

                case DataType_v3_1_0.STRING | DataType_v3_0_3.STRING:
                    # NOTE: JsonSchema build-in formats.
                    #       See: https://json-schema.org/understanding-json-schema/reference/string.html#id8
                    if schema.schema_format:
                        match schema.schema_format:
                            case "date-time":
                                return PythonDataType.DATATIME

                            case "date":
                                return PythonDataType.DATE

                            case "time":
                                return PythonDataType.TIME

                            case "duration":
                                return PythonDataType.TIMEDELTA

                    else:
                        return PythonDataType.STR

                case DataType_v3_1_0.NUMBER | DataType_v3_0_3.NUMBER:
                    if schema.enum:
                        return PythonDataTypeStr(f"Literal[{','.join(schema.enum)}]")
                    else:
                        return PythonDataType.FLOAT

                case DataType_v3_1_0.INTEGER | DataType_v3_0_3.INTEGER:
                    if schema.enum:
                        return PythonDataTypeStr(f"Literal[{','.join(schema.enum)}]")
                    else:
                        return PythonDataType.INT

                case DataType_v3_1_0.BOOLEAN | DataType_v3_0_3.BOOLEAN:
                    return PythonDataType.BOOL

                case DataType_v3_1_0.ARRAY | DataType_v3_0_3.BOOLEAN:
                    return PythonDataType.LIST

                case DataType_v3_1_0.OBJECT | DataType_v3_0_3.OBJECT:
                    return PythonDataType.DICT

                case _:
                    raise NeverReachError(schema_type)

        return PythonDataTypeStr("Any")


@dataclass
class PythonDataField:
    description: str | None = None
    default: str | None = None

    # string
    min_length: int | None = None
    max_length: int | None = None
    pattern: str | None = None

    # numeric
    minimum: float | None = None
    maxmum: float | None = None
    exclusive_minimum: bool | None = None
    exclusive_maxmum: bool | None = None
    multiple_of: float | None = None


@dataclass
class PythonDataSchema:
    name: str
    type: PythonDataType | PythonDataTypeStr
    field: PythonDataField | None = None


def get_schemas(openapi: OpenAPI) -> list[PythonDataSchema]:
    schemas = []
    if not openapi.root.components or not openapi.root.components.schemas:
        return schemas

    for name, schema in openapi.root.components.schemas.items():
        schemas.append(
            PythonDataSchema(
                name=name,
                type=PythonDataTypeStr.from_schema(schema),
            )
        )

    return schemas
