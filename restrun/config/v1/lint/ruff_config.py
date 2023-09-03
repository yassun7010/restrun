from typing import Literal

from restrun.core.model import ExtraForbidModel


class V1RuffConfig(ExtraForbidModel):
    linter: Literal["ruff"]
    options: list[str] | None = None
