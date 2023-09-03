from pathlib import Path
from typing import Annotated, Literal

from pydantic import Field, HttpUrl

from restrun.core.model import ExtraForbidModel


class V1OpenAPISource(ExtraForbidModel):
    type: Literal["openapi"]
    location: Annotated[Path | HttpUrl, Field(title="openapi file location.")]
