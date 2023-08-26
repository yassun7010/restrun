from dataclasses import dataclass, field
from typing import Self

import restrun
from restrun.config import Config

from .request_resource_map import RequestResourceMap


@dataclass
class RestrunContext:
    config: Config
    client_prefix: str

    client_middleware_classes: list[str] = field(default_factory=list)

    real_client_middleware_classes: list[str] = field(default_factory=list)

    mock_client_middleware_classes: list[str] = field(default_factory=list)

    resources: RequestResourceMap = field(default_factory=RequestResourceMap)

    @property
    def version(self):
        return restrun.__version__

    @classmethod
    def from_config(cls, config: Config) -> Self:
        return RestrunContext(
            config=config,
            client_prefix=config.name,
        )
