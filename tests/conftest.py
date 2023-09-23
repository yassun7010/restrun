import os
import uuid

from contextlib import contextmanager
from pathlib import Path

from pytest import fixture

from restrun.config import Config
from restrun.config.v1 import V1Config
from restrun.generator.context.resource_context import ResourceContext
from restrun.generator.context.resources_context import ResourcesContext
from restrun.generator.context.restrun_context import RestrunContext


@contextmanager
def tempfilepath(path: Path):
    _path = path / f"{uuid.uuid4()}.py" if path.is_dir() else path

    with open(_path, "w"):
        pass

    yield _path

    os.remove(_path)


@fixture
def config() -> Config:
    return Config(
        root=V1Config(
            name="my",
            version="1",
        )
    )


@fixture
def restrun_context(config: Config) -> RestrunContext:
    return RestrunContext(
        server_urls=["https://example.com"],
        client_prefix=config.root.name,
        client_mixins=[],
        real_client_mixins=[],
        mock_client_mixins=[],
    )


@fixture
def resources_context(config: Config) -> ResourcesContext:
    return ResourcesContext(
        resources=[],
    )


@fixture
def resource_context() -> ResourceContext:
    return ResourceContext(
        module_name="v1_pets",
        operation_map={},
        path="/v1/pets",
    )


def format_by_black(contents: str) -> str:
    from black import Mode, format_str

    return format_str(contents, mode=Mode(preview=True))
