import logging
from argparse import ArgumentParser, BooleanOptionalAction
from logging import getLogger

from rich.console import Console as RichConsole
from rich.logging import RichHandler

import restrun
from restrun.cli.commands import generate


class App:
    @classmethod
    def run(cls, args: list[str] | None = None) -> None:
        parser = ArgumentParser(
            prog="restrun",
            description="A tool to generate REST API clients.",
        )

        parser.add_argument(
            "--version",
            action="version",
            version=f"%(prog)s {restrun.__version__}",
        )

        parser.add_argument(
            "--verbose",
            action=BooleanOptionalAction,
            help="output verbose log.",
        )

        subparser = parser.add_subparsers(dest="command", required=True)
        generate.add_subparser(subparser)

        space = parser.parse_args(args)

        level = logging.DEBUG if space.verbose else logging.INFO
        logging.basicConfig(
            format="%(message)s",
            level=level,
            handlers=[
                RichHandler(
                    level=level,
                    console=RichConsole(stderr=True),
                    show_time=False,
                    show_path=False,
                    rich_tracebacks=True,
                )
            ],
        )
        logger = getLogger(__name__)

        try:
            if hasattr(space, "handler"):
                space.handler(space)
            else:
                parser.print_help()
        except Exception as e:
            if space.verbose:
                logger.exception(e)
            else:
                logger.error(e)

            raise e