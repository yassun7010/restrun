from argparse import ArgumentParser, _SubParsersAction
from logging import getLogger


logger = getLogger(__name__)


def add_subparser(subparsers: _SubParsersAction, **kwargs) -> None:
    from . import config

    description = "display resource."

    parser: ArgumentParser = subparsers.add_parser(
        "get",
        description=description,
        help=description,
        **kwargs,
    )

    subparsers = parser.add_subparsers(
        title="commands",
        metavar="COMMAND",
        required=True,
    )

    config.add_subparser(subparsers, formatter_class=parser.formatter_class)
