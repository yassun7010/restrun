from pathlib import Path
from typing import Annotated, Literal

from pydantic import Field

from restrun.core.model import ExtraForbidModel


class V1OpenAPISource(ExtraForbidModel):
    type: Literal["openapi"]
    location: Annotated[Path, Field(title="openapi file location.")]
