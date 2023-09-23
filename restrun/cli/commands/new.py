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
    from restrun.cli.prompt.project_name import prompt_project_name
    from restrun.cli.prompt.source import prompt_source
    from restrun.config import DEFAULT_CONFIG_FILE
    from restrun.exceptions import FileAlreadyExistsError
    from restrun.strcase import module_name

    config_path: Path | None = space.config
    if config_path and config_path.exists() and not space.overwrite:
        raise FileAlreadyExistsError(config_path)

    project_name = prompt_project_name(space.project)
    source = prompt_source(space.openapi)
    project_path = Path(module_name(project_name))
    if not project_path.exists():
        project_path.mkdir()

    config = prompt_config(space.project, space.openapi)

    if config_path is None:
        config_path = project_path / DEFAULT_CONFIG_FILE

        if config_path.exists() and not space.overwrite:
            raise FileAlreadyExistsError(config_path)

    with open(config_path, "w") as file:
        from restrun import yaml

        file.write(yaml.dump(config))

    logger.info(f'Create a new project: "{project_name}" 🚀')
