from argparse import ArgumentParser, BooleanOptionalAction, Namespace, _SubParsersAction
from logging import getLogger

from restrun.generator import generate_python_code


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
    from restrun.config import find_config_file

    generate_python_code(
        find_config_file(space.config),
        space.format,
        space.lint,
    )

    logger.info("Successfully generated clients.")
