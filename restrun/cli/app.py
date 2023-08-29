import logging
import sys
from argparse import ArgumentParser, BooleanOptionalAction
from logging import getLogger
from typing import NoReturn

from rich.console import Console as RichConsole
from rich.logging import RichHandler
from rich_argparse import RichHelpFormatter

import restrun
from restrun.cli.commands import generate


class RestrunArgumentParser(ArgumentParser):
    def error(self, message: str) -> NoReturn:
        self.print_usage(sys.stderr)
        raise RuntimeError(message)


class App:
    @classmethod
    def run(cls, args: list[str] | None = None) -> None:
        RichHelpFormatter.styles["argparse.restrun"] = "bold itaric green"

        parser = RestrunArgumentParser(
            prog="restrun",
            description=(
                "[argparse.restrun]RESTRUN[/] is a tool to generate REST API clients."
            ),
            formatter_class=RichHelpFormatter,
        )

        parser.add_argument(
            "--version",
            action="version",
            version=f"[argparse.prog]%(prog)s[/] {restrun.__version__}",
        )

        parser.add_argument(
            "--verbose",
            action=BooleanOptionalAction,
            help="output verbose log.",
        )

        subparser = parser.add_subparsers(dest="command", required=True)
        generate.add_subparser(subparser, formatter_class=parser.formatter_class)

        logging.basicConfig(
            format="%(message)s",
            level=logging.INFO,
            handlers=[
                RichHandler(
                    level=logging.DEBUG,
                    console=RichConsole(stderr=True),
                    show_time=False,
                    show_path=False,
                    rich_tracebacks=True,
                )
            ],
        )
        logger = getLogger(__name__)

        try:
            space = parser.parse_args(args)

        except Exception as e:
            logger.error(e)

            raise e

        logging.root.setLevel(logging.DEBUG if space.verbose else logging.INFO)

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
