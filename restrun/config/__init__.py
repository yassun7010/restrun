from typing import TYPE_CHECKING

from pydantic import RootModel

from .v1.v1_config import V1Config

if TYPE_CHECKING:
    from restrun.generator.context import Context

DEFAULT_CONFIG_FILENAME = "restrun.toml"


class Config(RootModel):
    root: V1Config

    @property
    def name(self) -> str:
        return self.root.name

    def to_context(self) -> "Context":
        return self.root.to_context()


def load(config_file: str) -> Config:
    return Config.parse_file(config_file)
