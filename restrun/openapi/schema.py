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
    EMAIL = "str"
    IDN_EMAIL = "str"
    HOSTNAME = "str"
    IDN_HOSTNAME = "str"
    IP_V4 = "str"
    IP_V6 = "str"
    UUID = "uuid"
    URI = "str"
    URI_REFERENCE = "str"
    IRI = "str"
    IRI_REFERENCE = "str"
    URI_TEMPLATE = "str"
    JSON_POINTER = "str"
    RELATIVE_JSON_POINTER = "str"
    REGEX = "re.Pattern"
    ANY = "Any"
    DICT = "dict"
    LIST = "list"


class PythonCustomDataType:
    def __init__(self, name: str):
        self.name = name

    def __str__(self) -> str:
        return self.name


class PythonDataTypeStr(str):
    @classmethod
    def from_schema(
        cls, schema: Schema | Reference, type: DataType | None = None
    ) -> PythonDataType | PythonCustomDataType | Self:
        if isinstance(schema, Reference):
            return PythonDataType.ANY
        schema_type = type or schema.type

        if schema_type:
            match schema_type:
                case list():
                    # NOTE: `openapi_pydantic` defined it case,
                    #       but we do not expect list to come.
                    return PythonDataTypeStr(
                        " | ".join(
                            [
                                str(cls.from_schema(schema, s))
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

                            case "email":
                                return PythonDataType.EMAIL

                            case "idn-email":
                                return PythonDataType.IDN_EMAIL

                            case "hostname":
                                return PythonDataType.HOSTNAME

                            case "idn-hostname":
                                return PythonDataType.IDN_HOSTNAME

                            case "ipv4":
                                return PythonDataType.IP_V4

                            case "ipv6":
                                return PythonDataType.IP_V6

                            case "uuid":
                                return PythonDataType.UUID

                            case "uri":
                                return PythonDataType.URI

                            case "uri-reference":
                                return PythonDataType.URI_REFERENCE

                            case "iri":
                                return PythonDataType.IRI

                            case "iri-reference":
                                return PythonDataType.IRI_REFERENCE

                            case "uri-template":
                                return PythonDataType.URI_TEMPLATE

                            case "json-pointer":
                                return PythonDataType.JSON_POINTER

                            case "relative-json-pointer":
                                return PythonDataType.RELATIVE_JSON_POINTER

                            case "regex":
                                return PythonDataType.REGEX

                            case _:
                                return PythonCustomDataType(schema.schema_format)

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
