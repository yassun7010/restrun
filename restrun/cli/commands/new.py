import os
from argparse import ArgumentParser, Namespace, _SubParsersAction
from logging import getLogger

from restrun.cli.prompt.select_prompt import select_prompt

logger = getLogger(__name__)


def add_subparser(subparsers: _SubParsersAction, **kwargs) -> None:
    parser: ArgumentParser = subparsers.add_parser(
        "new",
        description="create new [restrun]RESTRUN[/] project.",
        help="create new RESTRUN project.",
        **kwargs,
    )

    parser.add_argument(
        "project",
        type=str,
        metavar="PROJECT",
        nargs="?",
        help="project name.",
    )

    parser.add_argument(
        "--source",
        type=str,
        metavar="SOURCE_TYPE",
        choices=["manual", "openapi"],
        required=False,
        help="resource source type.",
    )

    parser.set_defaults(handler=new_command)


def new_command(space: Namespace) -> None:
    from pathlib import Path

    from rich.console import Console
    from rich.prompt import Prompt

    from restrun.exceptions import ProjectNameRequiredError
    from restrun.strcase import module_name

    console = Console()

    project_name: str | None = space.project
    if project_name is None:
        project_name = Prompt.ask(
            "[dark_orange]Project Name[/]",
            default=module_name(Path(os.getcwd()).name),
        )
        if len(project_name) == 0:
            raise ProjectNameRequiredError()

    source: str | None = space.source
    if source is None:
        console.print("[dark_orange]Source Type[/]:")
        source = select_prompt(
            options=["manual", "openapi"],
        )

    logger.info(f"Create a new project: {project_name}")
