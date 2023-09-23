from argparse import ArgumentParser, Namespace, _SubParsersAction
from logging import getLogger

from restrun.exceptions import FileExtensionError


logger = getLogger(__name__)


def add_subparser(subparsers: _SubParsersAction, **kwargs) -> None:
    from restrun.config import DEFAULT_CONFIG_FILE

    help = f'create [literal]"{DEFAULT_CONFIG_FILE}"[/].'

    parser: ArgumentParser = subparsers.add_parser(
        "config",
        description=help,
        help=help,
        **kwargs,
    )

    parser.add_argument(
        "--project",
        type=str,
        metavar="PROJECT",
        required=False,
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
        help="overwrite existing file.",
    )

    parser.set_defaults(handler=create_config_command)


def create_config_command(space: Namespace) -> None:
    from pathlib import Path

    from restrun import yaml
    from restrun.cli.prompt.config import prompt_config
    from restrun.config import DEFAULT_CONFIG_FILE
    from restrun.exceptions import FileAlreadyExistsError

    config_path = Path(space.config or str(DEFAULT_CONFIG_FILE))

    if config_path.exists() and not space.overwrite:
        raise FileAlreadyExistsError(config_path)

    extension = config_path.suffix
    if extension not in (".json", ".yml", ".yaml"):
        raise FileExtensionError(config_path, extension)

    config = prompt_config(space.project, space.openapi)

    with open(config_path, "w") as file:
        from restrun import yaml

        match extension:
            case ".json":
                file.write(config.model_dump_json())

            case ".yml" | ".yaml":
                file.write(yaml.dump(config))

            case _:
                raise FileExtensionError(config_path, extension)
