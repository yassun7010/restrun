from pathlib import Path
from typing import Annotated, Literal

from pydantic import Field

from restrun.config.v1.format import V1BlackConfig, V1FormatterConfig
from restrun.config.v1.format.isort_config import V1IsortConfig
from restrun.config.v1.lint import V1LinterConfig
from restrun.config.v1.lint.ruff_config import V1RuffConfig
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
        bool | V1FormatterConfig | list[V1FormatterConfig],
        Field(title="format generated code. default formatter is 'black'"),
    ] = True

    lint: Annotated[
        bool | V1LinterConfig | list[V1LinterConfig],
        Field(title="lint generated code. default linter is 'ruffo'"),
    ] = True

    @property
    def sources(self) -> list[V1Source]:
        if isinstance(self.source, list):
            return self.source
        return [self.source]

    @property
    def formats(self) -> list[V1FormatterConfig] | None:
        if self.format is False:
            return None

        elif self.format is True:
            return [V1IsortConfig(formatter="isort"), V1BlackConfig(formatter="black")]

        elif not isinstance(self.format, list):
            return [self.format]

        else:
            return self.format

    @property
    def lints(self) -> list[V1LinterConfig] | None:
        if self.lint is False:
            return None

        elif self.lint is True:
            return [V1RuffConfig(linter="ruff")]

        elif not isinstance(self.lint, list):
            return [self.lint]

        else:
            return self.lint
