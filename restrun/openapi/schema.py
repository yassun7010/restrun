from collections import OrderedDict
from enum import Enum
from functools import cached_property
from typing import Self

from attr import dataclass

from restrun.exception import NeverReachError
from restrun.strcase import class_name

from .openapi import (
    DataType,
    DataType_v3_0_3,
    DataType_v3_1_0,
    OpenAPI,
    Reference,
    Reference_v3_0_3,
    Schema,
    Schema_v3_0_3,
    Schema_v3_1_0,
    SchemaName,
)


class PythonLiteralType(str, Enum):
    NONE = "None"
    INT = "int"
    FLOAT = "float"
    BOOL = "bool"
    STR = "str"
    DATETIME = "datetime"
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


class PythonLiteralUnion:
    def __init__(
        self,
        type: PythonLiteralType,
        items: list[str] | list[int] | list[float],
    ):
        self.type = type
        self.items = items

    def __eq__(self, value: Self) -> bool:
        return self.type == value.type and self.items == value.items

    def __str__(self) -> str:
        return f"Literal[{','.join(map(repr, self.items))}]"


class PythonCustomStr:
    def __init__(self, name: str):
        self.name = name

    def __str__(self) -> str:
        return self.name


@dataclass(frozen=True)
class PythonArray:
    name: str
    items: "PythonDataType"


@dataclass(frozen=True)
class PythonObjectProperty:
    type: "PythonDataType"
    required: bool = False
    description: str | None = None


@dataclass(frozen=True)
class PythonObject:
    class_name: str
    properties: dict[str, PythonObjectProperty]
    additional_properties: bool = True


@dataclass(frozen=True)
class PythonReference:
    ref: str
    target: "PythonDataType"

    @cached_property
    def name(self) -> str:
        return self.ref.split("/")[-1]


PythonDataType = (
    PythonLiteralType
    | PythonCustomStr
    | PythonLiteralUnion
    | PythonArray
    | PythonObject
    | PythonReference
)


def get_data_type(
    name: SchemaName,
    schema: Schema | Reference,
    schemas: dict[str, Schema_v3_1_0] | dict[str, Schema_v3_0_3 | Reference_v3_0_3],
    type: DataType | None = None,
) -> PythonDataType:
    if isinstance(schema, Reference):
        schma_name = schema.ref.split("/")[-1]
        return PythonReference(
            ref=schema.ref,
            target=get_data_type(schma_name, schemas[schma_name], schemas),
        )

    schema_type = type or schema.type

    if schema_type:
        match schema_type:
            case list():
                # NOTE: `openapi_pydantic` defined it case,
                #       but we do not expect list to come.
                return PythonLiteralType(
                    " | ".join(
                        [
                            str(get_data_type(name, schema, schemas, s))
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
                            return PythonLiteralType.DATETIME

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

                elif schema.enum:
                    return PythonLiteralUnion(PythonLiteralType.STR, schema.enum)

                else:
                    return PythonLiteralType.STR

            case DataType_v3_1_0.NUMBER | DataType_v3_0_3.NUMBER:
                if schema.enum:
                    return PythonLiteralUnion(PythonLiteralType.FLOAT, schema.enum)
                else:
                    return PythonLiteralType.FLOAT

            case DataType_v3_1_0.INTEGER | DataType_v3_0_3.INTEGER:
                if schema.enum:
                    return PythonLiteralUnion(PythonLiteralType.INT, schema.enum)
                else:
                    return PythonLiteralType.INT

            case DataType_v3_1_0.BOOLEAN | DataType_v3_0_3.BOOLEAN:
                return PythonLiteralType.BOOL

            case DataType_v3_1_0.ARRAY | DataType_v3_0_3.BOOLEAN:
                return PythonArray(
                    name=name,
                    items=(
                        get_data_type(name, schema.items, schemas)
                        if schema.items is not None
                        else PythonLiteralType.ANY
                    ),
                )

            case DataType_v3_1_0.OBJECT | DataType_v3_0_3.OBJECT:
                properties = schema.properties or OrderedDict()
                if isinstance(properties, dict):
                    required_properties = schema.required or []
                    properties = OrderedDict(
                        [
                            (
                                name,
                                PythonObjectProperty(
                                    type=get_data_type(name, property, schemas),
                                    required=name in required_properties,
                                    description=(
                                        property.description
                                        if isinstance(property, Schema)
                                        else None
                                    ),
                                ),
                            )
                            for name, property in properties.items()
                            if not isinstance(property, list)
                        ]
                    )

                return PythonObject(
                    class_name=class_name(name),
                    properties=properties,
                    additional_properties=schema.additionalProperties is not False,
                )

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


def get_schemas(openapi: OpenAPI) -> list[PythonDataSchema]:
    schemas = []
    if not openapi.root.components or not openapi.root.components.schemas:
        return schemas

    for name, schema in openapi.root.components.schemas.items():
        schemas.append(
            PythonDataSchema(
                name=name,
                type=get_data_type(name, schema, openapi.root.components.schemas),
            )
        )

    return schemas
