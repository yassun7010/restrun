from collections import OrderedDict
from enum import Enum

from attr import dataclass

from restrun.exception import NeverReachError

from .openapi import (
    DataType,
    DataType_v3_0_3,
    DataType_v3_1_0,
    OpenAPI,
    Reference,
    Schema,
    SchemaName,
)


class PythonLiteralType(str, Enum):
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


class PythonCustomStr:
    def __init__(self, name: str):
        self.name = name

    def __str__(self) -> str:
        return self.name


@dataclass
class PythonArray:
    name: str
    items: "list[PythonDataType]"


@dataclass
class PythonDict:
    name: str
    properties: OrderedDict[str, "PythonDataType"]


PythonDataType = PythonLiteralType | PythonCustomStr | PythonArray | PythonDict


def get_data_type(
    name: SchemaName, schema: Schema | Reference, type: DataType | None = None
) -> PythonDataType:
    if isinstance(schema, Reference):
        return PythonLiteralType.ANY
    schema_type = type or schema.type

    if schema_type:
        match schema_type:
            case list():
                # NOTE: `openapi_pydantic` defined it case,
                #       but we do not expect list to come.
                return PythonLiteralType(
                    " | ".join(
                        [
                            str(get_data_type(name, schema, s))
                            for s in schema_type
                            if not isinstance(s, list)
                        ]
                    )
                )

            case DataType_v3_1_0.NULL:
                return PythonLiteralType.NONE

            case DataType_v3_1_0.STRING | DataType_v3_0_3.STRING:
                # NOTE: JsonSchema build-in formats.
                #       See: https://json-schema.org/understanding-json-schema/reference/string.html#id8
                if schema.schema_format:
                    match schema.schema_format:
                        case "date-time":
                            return PythonLiteralType.DATATIME

                        case "date":
                            return PythonLiteralType.DATE

                        case "time":
                            return PythonLiteralType.TIME

                        case "duration":
                            return PythonLiteralType.TIMEDELTA

                        case "email":
                            return PythonLiteralType.EMAIL

                        case "idn-email":
                            return PythonLiteralType.IDN_EMAIL

                        case "hostname":
                            return PythonLiteralType.HOSTNAME

                        case "idn-hostname":
                            return PythonLiteralType.IDN_HOSTNAME

                        case "ipv4":
                            return PythonLiteralType.IP_V4

                        case "ipv6":
                            return PythonLiteralType.IP_V6

                        case "uuid":
                            return PythonLiteralType.UUID

                        case "uri":
                            return PythonLiteralType.URI

                        case "uri-reference":
                            return PythonLiteralType.URI_REFERENCE

                        case "iri":
                            return PythonLiteralType.IRI

                        case "iri-reference":
                            return PythonLiteralType.IRI_REFERENCE

                        case "uri-template":
                            return PythonLiteralType.URI_TEMPLATE

                        case "json-pointer":
                            return PythonLiteralType.JSON_POINTER

                        case "relative-json-pointer":
                            return PythonLiteralType.RELATIVE_JSON_POINTER

                        case "regex":
                            return PythonLiteralType.REGEX

                        case _:
                            return PythonCustomStr(schema.schema_format)

                else:
                    return PythonLiteralType.STR

            case DataType_v3_1_0.NUMBER | DataType_v3_0_3.NUMBER:
                if schema.enum:
                    return PythonLiteralType(f"Literal[{','.join(schema.enum)}]")
                else:
                    return PythonLiteralType.FLOAT

            case DataType_v3_1_0.INTEGER | DataType_v3_0_3.INTEGER:
                if schema.enum:
                    return PythonLiteralType(f"Literal[{','.join(schema.enum)}]")
                else:
                    return PythonLiteralType.INT

            case DataType_v3_1_0.BOOLEAN | DataType_v3_0_3.BOOLEAN:
                return PythonLiteralType.BOOL

            case DataType_v3_1_0.ARRAY | DataType_v3_0_3.BOOLEAN:
                return PythonArray(name=name, items=[])

            case DataType_v3_1_0.OBJECT | DataType_v3_0_3.OBJECT:
                return PythonDict(name=name, properties=OrderedDict())

            case _:
                raise NeverReachError(schema_type)

    return PythonLiteralType("Any")


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
    type: PythonDataType
    field: PythonDataField | None = None


def get_schemas(openapi: OpenAPI) -> list[PythonDataSchema]:
    schemas = []
    if not openapi.root.components or not openapi.root.components.schemas:
        return schemas

    for name, schema in openapi.root.components.schemas.items():
        schemas.append(
            PythonDataSchema(
                name=name,
                type=get_data_type(name, schema),
            )
        )

    return schemas
