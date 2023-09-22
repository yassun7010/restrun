import os
from argparse import ArgumentParser, Namespace, _SubParsersAction
from logging import getLogger

import yaml

from restrun.cli.prompt.select_prompt import select_prompt
from restrun.config import DEFAULT_CONFIG_FILE
from restrun.config.v1 import V1Config
from restrun.config.v1.source import SourceType
from restrun.config.v1.source.openapi_source import V1OpenAPISource
from restrun.exceptions import NeverReachError

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
        "--openapi",
        type=str,
        metavar="OPENAPI_LOCATION",
        required=False,
        help="openapi file location.",
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

    openapi_location: str | None = space.openapi
    source_type: SourceType | None = None
    if openapi_location is not None:
        source_type = "openapi"

    if source_type is None:
        options: list[SourceType] = ["manual", "openapi"]

        console.print("[dark_orange]Source Type[/]:")
        source_type = select_prompt(
            options=options,
        )

    match source_type:
        case "openapi":
            if openapi_location is None:
                openapi_location = Prompt.ask(
                    "[dark_orange]OpenAPI Location[/]",
                )
            source = V1OpenAPISource(
                type=source_type,
                location=Path(openapi_location),
            )

        case "manual":
            source = None

        case _:
            raise NeverReachError(source_type)

    project_path = Path(module_name(project_name))
    if not project_path.exists():
        project_path.mkdir()

    config = V1Config(
        version="1",
        name=project_name,
        source=source,
    )

    with open(project_path / DEFAULT_CONFIG_FILE, "w") as file:
        file.write(
            yaml.dump(
                config.model_dump(
                    exclude_none=True,
                    exclude_unset=True,
                ),
                sort_keys=False,
            )
        )

    logger.info(f'Create a new project: "{project_name}" 🚀')
