from argparse import ArgumentParser, BooleanOptionalAction
from enum import Enum
from logging import getLogger
from pathlib import Path
from typing import TYPE_CHECKING, Iterable

if TYPE_CHECKING:
    from argparse import Namespace, _SubParsersAction

    from restrun.config import Config
    from restrun.generator.context.restrun import RestrunContext

logger = getLogger(__name__)


class GenerateTarget(Enum):
    ALL = "all"
    CLIENT = "client"
    RESOURCE = "resource"

    def __str__(self) -> str:
        return self.value


def add_subparser(subparsers: "_SubParsersAction", **kwargs) -> None:
    parser: ArgumentParser = subparsers.add_parser(
        "generate",
        description="Generate REST API clients.",
        help="Generate REST API clients.",
        **kwargs,
    )

    parser.add_argument(
        "--target",
        nargs="*",
        type=GenerateTarget,
        choices=list(GenerateTarget),
        default=[GenerateTarget.ALL],
        help="target to generate.",
    )

    parser.add_argument(
        "--format",
        action=BooleanOptionalAction,
        help="format generated code. default is [literal]true[/].",
    )

    parser.add_argument(
        "--lint",
        action=BooleanOptionalAction,
        help="lint generated code. default is [literal]true[/].",
    )

    parser.set_defaults(handler=generate_command)


def generate_command(space: "Namespace") -> None:
    from restrun import strcase
    from restrun.config import DEFAULT_CONFIG_FILE, get_path, load
    from restrun.generator.context.restrun import make_rustrun_context

    targets = get_targets(space.target)
    config_path = get_path(space.config, DEFAULT_CONFIG_FILE)

    with open(config_path) as file:
        config = load(file)

    base_dir = config_path.parent / strcase.module_name(config.name)
    context = make_rustrun_context(base_dir, config)

    if GenerateTarget.RESOURCE in targets:
        write_resources(base_dir, config, context)

    if GenerateTarget.CLIENT in targets:
        write_clients(base_dir, config, context)

    if space.format if space.format is not None else config.format:
        from restrun.formatter.black import BlackFormatter

        BlackFormatter().format(base_dir)

    if space.lint if space.lint is not None else config.lint:
        from restrun.linter.ruff import RuffLinter

        RuffLinter().lint(base_dir)


def get_targets(
    targets: Iterable[GenerateTarget],
) -> set[GenerateTarget]:
    for target in targets:
        if target == GenerateTarget.ALL:
            return set([t for t in GenerateTarget if t != GenerateTarget.ALL])

    return set(targets)


def write_clients(base_dir: Path, config: "Config", context: "RestrunContext") -> None:
    from restrun.generator import is_auto_generated_or_empty
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
        filepath = base_dir / "client" / filename

        if filepath.exists() and not is_auto_generated_or_empty(filepath):
            continue

        code = generator.generate(config, context)
        with open(filepath, "w") as file:
            file.write(code)


def write_resources(
    base_dir: Path, config: "Config", context: "RestrunContext"
) -> None:
    from restrun.generator import is_auto_generated_or_empty
    from restrun.generator.resource_module import ResourceModuleGenerator
    from restrun.generator.resources_module import ResourcesModuleGenerator

    for resource_context in context.resources:
        filepath = base_dir / "resources" / resource_context.module_name / "__init__.py"
        if filepath.exists() and not is_auto_generated_or_empty(filepath):
            continue

        code = ResourceModuleGenerator().generate(config, context, resource_context)
        with open(
            base_dir / "resources" / resource_context.module_name / "__init__.py", "w"
        ) as file:
            file.write(code)

    filepath = base_dir / "resources" / "__init__.py"
    if filepath.exists() and not is_auto_generated_or_empty(filepath):
        return

    code = ResourcesModuleGenerator().generate(config, context)
    with open(filepath, "w") as file:
        file.write(code)
