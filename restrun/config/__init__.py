import json
import os
from io import StringIO
from typing import IO

import jinja2
import tomllib
import yaml
from pydantic import RootModel

from restrun.exception import FileExtensionError

from .v1 import V1Config

DEFAULT_CONFIG_FILENAME = "restrun.toml"


class Config(RootModel):
    root: V1Config

    @property
    def name(self) -> str:
        return self.root.name

    @property
    def format(self) -> bool:
        return self.root.format

    @property
    def lint(self) -> bool:
        return self.root.lint


def load(file: IO, **kwargs) -> Config:
    root, extension = os.path.splitext(file.name)
    match extension:
        case ".json":
            config = json.load(file)

        case ".yaml" | ".yml":
            config = yaml.full_load(file)

        case ".toml":
            config = tomllib.load(file)

        case ".jinja" | "jinja2" | ".j2":
            data: bytes | str = file.read()
            if isinstance(data, bytes):
                data = data.decode("utf-8")

            rendered_file = StringIO(jinja2.Template(data).render(os.environ, **kwargs))
            rendered_file.name = root

            return load(rendered_file, **kwargs)

        case _:
            raise FileExtensionError(file.name, extension)

    return Config.model_validate(config)
