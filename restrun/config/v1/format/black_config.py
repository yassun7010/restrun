from typing import Literal

from restrun.core.model import ExtraForbidModel


class V1BlackConfig(ExtraForbidModel):
    formatter: Literal["black"]
    options: list[str] | None = None
