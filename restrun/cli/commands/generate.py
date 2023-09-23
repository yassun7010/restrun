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
    from restrun import strcase
    from restrun.config import find_config_file, load
    from restrun.formatter import format_python_codes
    from restrun.linter import lint_python_codes
    from restrun.writer import write_python_codes

    config_path = find_config_file(space.config)
    with open(config_path) as file:
        config = load(file)

    base_dir = config_path.parent / strcase.module_name(config.name)

    write_python_codes(base_dir, config, config_path)

    if space.format is not False:
        format_python_codes(base_dir, config)

    if space.lint is not False:
        lint_python_codes(base_dir, config)

    logger.info("Successfully generated clients.")
