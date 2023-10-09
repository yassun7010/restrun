from argparse import ArgumentParser, _SubParsersAction
from logging import getLogger


logger = getLogger(__name__)


def add_subparser(subparsers: _SubParsersAction, **kwargs) -> None:
    from . import config, operation

    description = "create resource."

    parser: ArgumentParser = subparsers.add_parser(
        "create",
        description=description,
        help=description,
        **kwargs,
    )

    subparsers = parser.add_subparsers(
        title="commands",
        metavar="COMMAND",
    )

    for add_subparser in (config.add_subparser, operation.add_subparser):
        add_subparser(
            subparsers,
            formatter_class=parser.formatter_class,
        )

    parser.set_defaults(handler=lambda _: parser.print_help())
