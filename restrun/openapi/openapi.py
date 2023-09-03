from typing import TypeAlias

from openapi_pydantic.v3.v3_0_3 import DataType as DataType_v3_0_3
from openapi_pydantic.v3.v3_0_3 import OpenAPI as OpenAPI_v3_0_3
from openapi_pydantic.v3.v3_0_3 import Reference as Reference_v3_0_3
from openapi_pydantic.v3.v3_0_3 import Schema as Schema_v3_0_3
from openapi_pydantic.v3.v3_1_0 import DataType as DataType_v3_1_0
from openapi_pydantic.v3.v3_1_0 import OpenAPI as OpenAPI_v3_1_0
from openapi_pydantic.v3.v3_1_0 import Reference as Reference_v3_1_0
from openapi_pydantic.v3.v3_1_0 import Schema as Schema_v3_1_0
from pydantic import RootModel

DataType: TypeAlias = DataType_v3_1_0 | DataType_v3_0_3
Schema: TypeAlias = Schema_v3_1_0 | Schema_v3_0_3
Reference: TypeAlias = Reference_v3_1_0 | Reference_v3_0_3

SchemaName: TypeAlias = str


class OpenAPI(RootModel):
    root: OpenAPI_v3_1_0 | OpenAPI_v3_0_3
