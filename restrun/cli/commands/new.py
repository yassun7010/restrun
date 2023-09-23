import os

from argparse import ArgumentParser, Namespace, _SubParsersAction
from logging import getLogger


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

    from restrun.cli.app import App
    from restrun.cli.prompt.project_name import prompt_project_name
    from restrun.cli.prompt.source import prompt_source
    from restrun.config import DEFAULT_CONFIG_FILE
    from restrun.config.v1 import V1Config
    from restrun.strcase import module_name

    project_name = prompt_project_name(space.project)
    source = prompt_source(space.openapi)
    project_path = Path(module_name(project_name))
    if not project_path.exists():
        project_path.mkdir()

    config = V1Config(
        version="1",
        name=project_name,
        source=source,
    )

    config_path = project_path / DEFAULT_CONFIG_FILE
    with open(config_path, "w") as file:
        from restrun import yaml

        file.write(yaml.dump(config))

    os.chdir(project_path)

    App.run(["--config", str(DEFAULT_CONFIG_FILE), "generate"])

    logger.info(f'Create a new project: "{project_name}" 🚀')
