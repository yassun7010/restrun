import logging
import sys
from argparse import ArgumentParser, BooleanOptionalAction
from logging import getLogger
from pathlib import Path
from typing import NoReturn

from rich.console import Console as RichConsole
from rich.logging import RichHandler
from rich_argparse import RichHelpFormatter

import restrun
from restrun.cli.commands import generate, new
from restrun.config import DEFAULT_CONFIG_FILE


class RestrunArgumentParser(ArgumentParser):
    def error(self, message: str) -> NoReturn:
        self.print_usage(sys.stderr)
        raise RuntimeError(message)


class App:
    @classmethod
    def run(cls, args: list[str] | None = None) -> None:
        RichHelpFormatter.styles["restrun"] = "italic bold green"

        parser = RestrunArgumentParser(
            prog="restrun",
            description="[restrun]RESTRUN[/] is a tool to generate REST API clients.",
            formatter_class=RichHelpFormatter,
        )

        parser.add_argument(
            "--config",
            type=Path,
            help=(
                f'config filepath. default is [argparse.metavar]"{DEFAULT_CONFIG_FILE}"[/].'
            ),
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

        subparser = parser.add_subparsers(
            title="commands",
            metavar="command",
            required=True,
        )

        new.add_subparser(subparser, formatter_class=parser.formatter_class)
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
