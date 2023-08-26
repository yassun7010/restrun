import glob
from argparse import ArgumentParser, Namespace
from enum import Enum
from logging import getLogger
from pathlib import Path
from typing import TYPE_CHECKING, Annotated, NotRequired, TypedDict

from typer import Option

from restrun import strcase
from restrun.config import DEFAULT_CONFIG_FILENAME, Config, load
from restrun.generator import ClassInfo, find_class_from_code, is_auto_generated
from restrun.generator.context.restrun import RestrunContext
from restrun.linter.ruff import RuffLinter

if TYPE_CHECKING:
    from argparse import _SubParsersAction

logger = getLogger(__name__)


class GenerateTarget(Enum):
    ALL = "all"
    CLIENT = "client"
    RESOURCE = "resource"

    def __str__(self) -> str:
        return self.value


class GenerateArgs(TypedDict):
    target: NotRequired[
        Annotated[
            GenerateTarget | list[GenerateTarget],
            Option(default="all"),
        ]
    ]


def add_subparser(subparsers: "_SubParsersAction") -> None:
    parser: ArgumentParser = subparsers.add_parser(
        "generate",
        help="Generate REST API clients.",
    )

    parser.add_argument(
        "--config",
        type=Path,
        default=Path(DEFAULT_CONFIG_FILENAME),
        help="Path to config file.",
    )

    parser.add_argument(
        "--target",
        nargs="*",
        type=GenerateTarget,
        choices=list(GenerateTarget),
        default=[GenerateTarget.ALL],
        help="Target to generate.",
    )

    parser.set_defaults(handler=generate_command)


def generate_command(space: Namespace) -> None:
    targets = get_targets(space.target)
    config_path: Path = space.config

    with open(config_path, "br") as file:
        config = load(file)

    base_path = config_path.parent / strcase.module_name(config.name)
    context = make_rustrun_context(base_path, config)

    if GenerateTarget.CLIENT in targets:
        write_clients(base_path, context)

    if GenerateTarget.RESOURCE in targets:
        write_resources(base_path, context)

    if config.lint:
        RuffLinter().lint(base_path)


def get_targets(targets: list[GenerateTarget]) -> list[GenerateTarget]:
    for target in targets:
        if target == GenerateTarget.ALL:
            return list([t for t in GenerateTarget if t != GenerateTarget.ALL])

    return targets


def make_rustrun_context(base_path: Path, config: Config) -> RestrunContext:
    client_mixins_dir = base_path / "client" / "mixins"

    client_mixins: list[ClassInfo] = []
    real_client_mixins: list[ClassInfo] = []
    mock_client_mixins: list[ClassInfo] = []

    if client_mixins_dir.exists():
        from restrun.core.client import (
            RestrunClientMixin,
            RestrunMockClientMixin,
            RestrunRealClientMixin,
        )

        for pyfile in glob.glob(str(client_mixins_dir / "*.py")):
            pypath = Path(pyfile)

            if mixin := find_class_from_code(pypath, RestrunClientMixin):
                client_mixins.append(mixin)

            if mixin := find_class_from_code(pypath, RestrunRealClientMixin):
                real_client_mixins.append(mixin)

            if mixin := find_class_from_code(pypath, RestrunMockClientMixin):
                mock_client_mixins.append(mixin)

    return RestrunContext(
        config=config,
        client_prefix=config.name,
        client_mixins=client_mixins,
        real_client_mixins=real_client_mixins,
        mock_client_mixins=mock_client_mixins,
    )


def write_clients(base_path: Path, context: RestrunContext) -> None:
    from restrun.generator.client import ClientGenerator
    from restrun.generator.client_mixins_module import ClientMixinsModuleGenerator
    from restrun.generator.client_module import ClientModuleGenerator
    from restrun.generator.mock_client import MockClientGenerator
    from restrun.generator.real_client import RealClientGenerator

    for filename, generator in [
        ("client.py", ClientGenerator()),
        ("real_client.py", RealClientGenerator()),
        ("mock_client.py", MockClientGenerator()),
        ("__init__.py", ClientModuleGenerator()),
        (Path("mixins") / "__init__.py", ClientMixinsModuleGenerator()),
    ]:
        filepath = base_path / "client" / filename

        if not filepath.exists() or is_auto_generated(filepath):
            with open(filepath, "w") as file:
                file.write(generator.generate(context))


def write_resources(base_path: Path, context: RestrunContext) -> None:
    from restrun.generator.get_request import GetRequestGenerator
    from restrun.generator.resources_module import ResourcesModuleGenerator

    resources = context.resources
    for resource in resources.get_requests:
        with open(base_path / "resources" / f"{resource}.py", "w") as file:
            file.write(GetRequestGenerator().generate(context))

    with open(base_path / "resources" / "__init__.py", "w") as file:
        file.write(ResourcesModuleGenerator().generate(context))
