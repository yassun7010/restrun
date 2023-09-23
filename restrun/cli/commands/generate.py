from argparse import ArgumentParser, BooleanOptionalAction, Namespace, _SubParsersAction
from logging import getLogger


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
    import importlib.util
    import sys

    from pathlib import Path

    from restrun import strcase
    from restrun.config import find_config_file, load
    from restrun.generator.context.operation_context import make_operation_contexts
    from restrun.generator.context.resources_context import make_resources_context
    from restrun.generator.context.restrun_context import make_rustrun_context
    from restrun.generator.context.schema_context import make_schema_contexts
    from restrun.writer import (
        write_clients,
        write_module,
        write_operations,
        write_resources,
        write_schemas,
    )

    config_path = find_config_file(space.config)

    with open(config_path) as file:
        config = load(file)

    base_dir = config_path.parent / strcase.module_name(config.name)

    restrun_context = make_rustrun_context(base_dir, config)

    write_module(base_dir, config, restrun_context)

    # import root module of generated code.
    if spec := importlib.util.spec_from_file_location(
        str(base_dir), base_dir / "__init__.py"
    ):
        if spec.loader is not None:
            if module := importlib.util.module_from_spec(spec):
                sys.modules[spec.name] = module

    resources_context = make_resources_context(base_dir)

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

    write_resources(base_dir, config, restrun_context, resources_context)

    write_clients(base_dir, config, restrun_context, resources_context)

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
