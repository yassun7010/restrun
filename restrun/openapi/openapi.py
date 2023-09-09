import json
from pathlib import Path
from typing import Self, TypeAlias

import httpx
import pydantic_core
from openapi_pydantic.v3.v3_0_3 import DataType as DataType_v3_0_3
from openapi_pydantic.v3.v3_0_3 import OpenAPI as OpenAPI_v3_0_3
from openapi_pydantic.v3.v3_0_3 import Operation as Operation_v3_0_3
from openapi_pydantic.v3.v3_0_3 import Reference as Reference_v3_0_3
from openapi_pydantic.v3.v3_0_3 import Schema as Schema_v3_0_3
from openapi_pydantic.v3.v3_1_0 import DataType as DataType_v3_1_0
from openapi_pydantic.v3.v3_1_0 import OpenAPI as OpenAPI_v3_1_0
from openapi_pydantic.v3.v3_1_0 import Operation as Operation_v3_1_0
from openapi_pydantic.v3.v3_1_0 import Reference as Reference_v3_1_0
from openapi_pydantic.v3.v3_1_0 import Schema as Schema_v3_1_0
from pydantic import HttpUrl, RootModel

from restrun.core.http import URL
from restrun.exception import OpenAPIRequestError

DataType: TypeAlias = DataType_v3_1_0 | DataType_v3_0_3
Schema: TypeAlias = Schema_v3_1_0 | Schema_v3_0_3
Schemas = dict[str, Schema_v3_1_0] | dict[str, Schema_v3_0_3 | Reference_v3_0_3]
Reference: TypeAlias = Reference_v3_1_0 | Reference_v3_0_3
Operation: TypeAlias = Operation_v3_1_0 | Operation_v3_0_3


SchemaName: TypeAlias = str


class OpenAPI(RootModel):
    root: OpenAPI_v3_1_0 | OpenAPI_v3_0_3

    @classmethod
    def from_url(cls, location: Path | HttpUrl) -> Self:
        match location:
            case Path():
                with open(location) as file:
                    data = json.load(file)
            case pydantic_core.Url():
                response = httpx.get(str(location))
                if response.is_error:
                    raise OpenAPIRequestError(
                        method="GET",
                        url=location,
                        content=response.content,
                    )

                data = response.json()

        return OpenAPI.model_validate(data)

    def get_urls(
        self,
        override: list[URL] | None = None,
    ) -> list[URL]:
        if override is not None:
            return override

        urls = [server.url for server in self.root.servers]

        return urls
