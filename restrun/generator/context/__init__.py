from typing import Annotated, Self

from pydantic import Field

from restrun.config import Config
from restrun.core.model import ExtraForbidModel


class Context(ExtraForbidModel):
    config: Annotated[Config, Field()]
    client_prefix: Annotated[str, Field()]

    client_middleware_classes: list[str] = Field(
        default_factory=list,
    )

    real_client_middleware_classes: list[str] = Field(
        default_factory=list,
    )

    mock_client_middleware_classes: list[str] = Field(
        default_factory=list,
    )

    @classmethod
    def from_config(cls, config: Config) -> Self:
        return Context(
            config=config,
            client_prefix=config.name,
        )
