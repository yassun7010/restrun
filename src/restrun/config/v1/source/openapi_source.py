from functools import cached_property
from pathlib import Path
from typing import Annotated, Literal

from pydantic import Field, HttpUrl

from restrun.core.http import URL
from restrun.core.model import ExtraForbidModel
from restrun.openapi.openapi import OpenAPI


class V1OpenAPIServer(ExtraForbidModel):
    url: URL


class V1IOpenAPI(ExtraForbidModel):
    servers: list[V1OpenAPIServer]


class V1OpenAPISource(ExtraForbidModel):
    type: Literal["openapi"]
    location: Annotated[Path | HttpUrl, Field(title="openapi file location.")]
    openapi: Annotated[
        V1IOpenAPI | None,
        Field(title="server urls"),
    ] = None

    @property
    def server_urls(self) -> list[URL] | None:
        if self.openapi is None:
            return None

        return [url.url for url in self.openapi.servers]

    @cached_property
    def openapi_model(self) -> OpenAPI:
        return OpenAPI.from_url(self.location)
