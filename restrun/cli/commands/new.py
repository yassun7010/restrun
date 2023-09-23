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

    parser.add_argument(
        "--overwrite",
        action="store_true",
        default=False,
        help="overwrite existing config.",
    )

    parser.set_defaults(handler=new_command)


def new_command(space: Namespace) -> None:
    from pathlib import Path

    from restrun.cli.prompt.config import prompt_config
    from restrun.config import DEFAULT_CONFIG_FILE
    from restrun.exceptions import FileAlreadyExistsError
    from restrun.strcase import module_name

    config = prompt_config(space.project, space.openapi)

    project_path = Path(module_name(config.name))
    if not project_path.exists():
        project_path.mkdir()

    config_path = project_path / DEFAULT_CONFIG_FILE
    if config_path.exists() and not space.overwrite:
        raise FileAlreadyExistsError(config_path)

    with open(config_path, "w") as file:
        from restrun import yaml

        file.write(yaml.dump(config))

    logger.info(f'Create a new project: "{config.name}" 🚀')
