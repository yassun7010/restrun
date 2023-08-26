from pathlib import Path
from typing import Annotated, Literal

from pydantic import Field

from restrun.core.model import ExtraForbidModel


class V1Config(ExtraForbidModel):
    version: Literal["1"]

    name: Annotated[str, Field(title="client name.")]

    output: Annotated[Path | None, Field(title="output directory.")] = None

    lint: Annotated[
        bool,
        Field(title="lint generated code. default linter is 'ruffo'"),
    ] = True
