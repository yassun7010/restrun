from argparse import ArgumentParser, Namespace
from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING, Annotated, NotRequired, TypedDict

import tomllib
from typer import Option

from restrun.config import DEFAULT_CONFIG_FILENAME, Config
from restrun.linter.ruff import RuffLinter

if TYPE_CHECKING:
    from argparse import _SubParsersAction


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
        config = Config.model_validate(tomllib.load(file))

    context = config.to_context()
    base_path = config_path.parent

    if GenerateTarget.CLIENT in targets:
        from restrun.generator.client import ClientGenerator
        from restrun.generator.mock_client import MockClientGenerator

        for filename, generator in [
            ("client.py", ClientGenerator()),
            ("mock_client.py", MockClientGenerator()),
        ]:
            with open(base_path / config.name / "client" / filename, "w") as file:
                file.write(generator.generate(context))

    RuffLinter().lint(base_path)


def get_targets(targets: list[GenerateTarget]) -> list[GenerateTarget]:
    for target in targets:
        if target == GenerateTarget.ALL:
            return list([t for t in GenerateTarget if t != GenerateTarget.ALL])

    return targets
