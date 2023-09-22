from argparse import ArgumentParser, BooleanOptionalAction, Namespace, _SubParsersAction
from logging import getLogger
from pathlib import Path

from restrun.generator.context.operation_context import make_operation_contexts
from restrun.generator.context.schema_context import make_schema_contexts
from restrun.writer import write_operations, write_schemas

logger = getLogger(__name__)


def add_subparser(subparsers: _SubParsersAction, **kwargs) -> None:
    parser: ArgumentParser = subparsers.add_parser(
        "generate",
        description="generate clients.",
        help="generate clients.",
        **kwargs,
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
    from restrun.config import find_config_file, load
    from restrun.generator.context.restrun_context import make_rustrun_context
    from restrun.writer import write_clients, write_resources

    config_path = find_config_file(space.config)

    with open(config_path) as file:
        config = load(file)

    base_dir = config_path.parent / strcase.module_name(config.name)

    restrun_context = make_rustrun_context(base_dir, config)

    for source in config.root.sources:
        if source.type == "openapi":
            if (
                isinstance(source.location, Path)
                and not source.location.exists()
                and (config_path.parent / source.location).exists()
            ):
                source.location = config_path.parent / source.location

            write_schemas(
                base_dir, config, restrun_context, make_schema_contexts(source)
            )

            write_operations(
                base_dir,
                config,
                restrun_context,
                make_operation_contexts(source.server_urls, source),
            )

    write_resources(base_dir, config, restrun_context)

    write_clients(base_dir, config, restrun_context)

    if space.format is not False:
        for format in config.formats or []:
            if format.formatter == "isort":
                from restrun.formatter.isort import IsortFormatter

                IsortFormatter().format(base_dir, *format.args)

            if format.formatter == "black":
                from restrun.formatter.black import BlackFormatter

                BlackFormatter().format(base_dir)

    if space.lint is not False:
        for lint in config.lints or []:
            if lint.linter == "ruff":
                from restrun.linter.ruff import RuffLinter

                RuffLinter().lint(base_dir)

    logger.info("Successfully generated clients.")
