from typing import Literal

from restrun.core.model import ExtraForbidModel


class V1IsortConfig(ExtraForbidModel):
    formatter: Literal["isort"]
    options: list[str] | None = None
