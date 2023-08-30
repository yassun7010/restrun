from pathlib import Path
from typing import Annotated, Literal

from pydantic import Field

from restrun.core.model import ExtraForbidModel

from .source import V1Source


class V1Config(ExtraForbidModel):
    version: Literal["1"]

    name: Annotated[str, Field(title="client name.")]

    output: Annotated[Path | None, Field(title="output directory.")] = None

    source: V1Source | list[V1Source] = Field(
        title="source files.", default_factory=list
    )

    format: Annotated[
        bool,
        Field(title="format generated code. default formatter is 'black'"),
    ] = True

    lint: Annotated[
        bool,
        Field(title="lint generated code. default linter is 'ruffo'"),
    ] = True

    @property
    def sources(self) -> list[V1Source]:
        if isinstance(self.source, list):
            return self.source
        return [self.source]
