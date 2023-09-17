import json
import os
from io import StringIO
from pathlib import Path
from typing import IO

import jinja2
import tomllib
import yaml
from pydantic import RootModel

from restrun.config.v1.format import V1FormatConfig
from restrun.config.v1.lint import V1LintConfig
from restrun.core import http
from restrun.exceptions import FileExtensionError, RestrunConfigNotFoundError

from .v1 import V1Config

DEFAULT_CONFIG_FILES = [
    Path("restrun.yaml"),
    Path("restrun.yml"),
    Path("restrun.json"),
    Path("restrun.toml"),
]
DEFAULT_CONFIG_FILE = DEFAULT_CONFIG_FILES[0]


class Config(RootModel):
    root: V1Config

    @property
    def name(self) -> str:
        return self.root.name

    @property
    def server_urls(self) -> list[http.URL]:
        urls: list[http.URL] = []
        for source in self.root.sources:
            if server_urls := source.server_urls:
                urls.extend(server_urls)

        return urls

    @property
    def formats(self) -> list[V1FormatConfig] | None:
        return self.root.formats

    @property
    def lints(self) -> list[V1LintConfig] | None:
        return self.root.lints


def find_config_file(path: Path | None) -> Path:
    if path is not None:
        if path.exists():
            return path
        else:
            raise RestrunConfigNotFoundError(path)

    for filename in DEFAULT_CONFIG_FILES:
        if filename.exists():
            return filename

    else:
        raise RestrunConfigNotFoundError(DEFAULT_CONFIG_FILE)


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
