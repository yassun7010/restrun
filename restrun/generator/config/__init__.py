from pydantic import RootModel

from restrun.generator.config.v1.v1_config import V1Config


class Config(RootModel):
    root: V1Config
