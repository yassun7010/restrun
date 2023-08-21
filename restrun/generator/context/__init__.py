from typing import Annotated

from pydantic import Field

from restrun.core.model import ExtraForbidModel


class Context(ExtraForbidModel):
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
