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
        help="project name.",
    )

    parser.set_defaults(handler=new_command)


def new_command(space: Namespace) -> None:
    project_name = space.project
    logger.info(f"Create a new project: {project_name}")
