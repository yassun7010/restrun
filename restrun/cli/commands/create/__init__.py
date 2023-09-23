from argparse import ArgumentParser, _SubParsersAction
from logging import getLogger


logger = getLogger(__name__)


def add_subparser(subparsers: _SubParsersAction, **kwargs) -> None:
    from . import config

    parser: ArgumentParser = subparsers.add_parser(
        "create",
        description="create resource.",
        help="create resource.",
        **kwargs,
    )

    subparsers = parser.add_subparsers(
        title="commands",
        metavar="COMMAND",
        required=True,
    )

    config.add_subparser(subparsers, formatter_class=parser.formatter_class)
