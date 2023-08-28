import os
import uuid
from contextlib import contextmanager
from pathlib import Path

from pytest import fixture

from restrun.config import Config
from restrun.config.v1 import V1Config
from restrun.generator.context.resource import ResourceContext
from restrun.generator.context.restrun import RestrunContext


@contextmanager
def tempfilepath(path: Path):
    _path = path / f"{uuid.uuid4()}.py" if path.is_dir() else path

    with open(_path, "w"):
        pass

    yield _path

    os.remove(_path)


@fixture
def restrun_context() -> RestrunContext:
    return RestrunContext.from_config(
        Config(
            root=V1Config(
                name="my",
                version="1",
            )
        )
    )


@fixture
def resource_context() -> ResourceContext:
    return ResourceContext(
        name="v1_pets",
        method_map={},
        url="https://example.com/v1/pets",
    )
