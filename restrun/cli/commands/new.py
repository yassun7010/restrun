from argparse import ArgumentParser, Namespace, _SubParsersAction
from logging import getLogger

logger = getLogger(__name__)


def add_subparser(subparsers: _SubParsersAction, **kwargs) -> None:
    parser: ArgumentParser = subparsers.add_parser(
        "new",
        description="Create new [restrun]RESTRUN[/] project.",
        help="Create new RESTRUN project.",
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
    from rich.prompt import Prompt

    from restrun.exceptions import ProjectNameRequiredError

    project_name: str | None = space.project
    if project_name is None:
        project_name = Prompt.ask("Project name")
        if len(project_name) == 0:
            raise ProjectNameRequiredError()

    source: str | None = space.source
    if source is None:
        source = Prompt.ask(
            "Resource source type",
            choices=["manual", "openapi"],
            default="manual",
            show_default=True,
        )

    logger.info(f"Create a new project: {project_name}")
