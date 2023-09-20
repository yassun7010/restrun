import sys
from argparse import ArgumentParser, FileType, Namespace, _SubParsersAction
from logging import getLogger

logger = getLogger(__name__)


def add_subparser(subparsers: _SubParsersAction, **kwargs) -> None:
    parser: ArgumentParser = subparsers.add_parser(
        "config",
        description="display config.",
        help="display config.",
        **kwargs,
    )

    parser.add_argument(
        "--output",
        type=FileType("w"),
        default=sys.stdout,
        help="output filepath. default is [literal]stdout[/].",
    )

    parser.set_defaults(handler=get_config_command)


def get_config_command(space: Namespace) -> None:
    from restrun.config import find_config_file

    config_path = find_config_file(space.config)

    with open(config_path, "r") as file:
        print(file.read(), file=space.output)
