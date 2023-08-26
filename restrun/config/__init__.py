from pydantic import RootModel

from .v1 import V1Config

DEFAULT_CONFIG_FILENAME = "restrun.toml"


class Config(RootModel):
    root: V1Config

    @property
    def name(self) -> str:
        return self.root.name

    @property
    def lint(self) -> bool:
        return self.root.lint
