from dataclasses import dataclass, field
from typing import Self

import restrun
from restrun.config import Config
from restrun.generator import ClassInfo


@dataclass
class RestrunContext:
    config: Config

    client_prefix: str

    version: str = field(default=restrun.__version__)

    client_mixins: list[ClassInfo] = field(default_factory=list)

    real_client_mixins: list[ClassInfo] = field(default_factory=list)

    mock_client_mixins: list[ClassInfo] = field(default_factory=list)

    @classmethod
    def from_config(cls, config: Config) -> Self:
        return RestrunContext(
            config=config,
            client_prefix=config.name,
        )

    @property
    def client_mixin_path_names(self) -> list[str]:
        return [
            f"{mixin.module_path}.{mixin.class_name}" for mixin in self.client_mixins
        ]

    @property
    def real_client_mixin_path_names(self) -> list[str]:
        return [
            f"{mixin.module_path}.{mixin.class_name}"
            for mixin in self.real_client_mixins
        ]

    @property
    def mock_client_mixin_path_names(self) -> list[str]:
        return [
            f"{mixin.module_path}.{mixin.class_name}"
            for mixin in self.mock_client_mixins
        ]
