from typing import Annotated, Literal

from pydantic import DirectoryPath, Field

from restrun.config.v1.format import V1BlackConfig, V1FormatConfig
from restrun.config.v1.format.isort_config import V1IsortConfig
from restrun.config.v1.lint import V1LintConfig
from restrun.config.v1.lint.ruff_config import V1RuffConfig
from restrun.core.model import ExtraForbidModel

from .source import V1Source


class V1Config(ExtraForbidModel):
    version: Literal["1"]

    name: Annotated[str, Field(title="client name.")]

    output_dir: Annotated[
        DirectoryPath | None,
        Field(title="output directory."),
    ] = None

    source: Annotated[
        V1Source | list[V1Source] | None,
        Field(title="source settings."),
    ] = None

    @property
    def sources(self) -> list[V1Source]:
        if self.source is None:
            return []

        if isinstance(self.source, list):
            return self.source

        return [self.source]

    format: Annotated[
        bool | V1FormatConfig | list[V1FormatConfig],
        Field(
            title="format generated code. default formatters are 'isort' and 'black'.",
        ),
    ] = True

    @property
    def formats(self) -> list[V1FormatConfig] | None:
        if self.format is False:
            return None

        elif self.format is True:
            return [
                V1IsortConfig(formatter="isort"),
                V1BlackConfig(formatter="black"),
            ]

        elif not isinstance(self.format, list):
            return [self.format]

        else:
            return self.format

    lint: Annotated[
        bool | V1LintConfig | list[V1LintConfig],
        Field(title="lint generated code. default linter is 'ruffo'"),
    ] = True

    @property
    def lints(self) -> list[V1LintConfig] | None:
        if self.lint is False:
            return None

        elif self.lint is True:
            return [V1RuffConfig(linter="ruff")]

        elif not isinstance(self.lint, list):
            return [self.lint]

        else:
            return self.lint
