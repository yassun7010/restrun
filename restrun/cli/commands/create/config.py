from argparse import ArgumentParser, Namespace, _SubParsersAction
from logging import getLogger


logger = getLogger(__name__)


def add_subparser(subparsers: _SubParsersAction, **kwargs) -> None:
    parser: ArgumentParser = subparsers.add_parser(
        "config",
        description="create config.",
        help="create config.",
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

    parser.set_defaults(handler=create_config_command)


def create_config_command(space: Namespace) -> None:
    from pathlib import Path

    from restrun import yaml
    from restrun.cli.prompt.config import prompt_config
    from restrun.config import DEFAULT_CONFIG_FILE
    from restrun.exceptions import FileAlreadyExistsError

    config_path = Path(space.config or str(DEFAULT_CONFIG_FILE))

    if config_path.exists():
        raise FileAlreadyExistsError(config_path)

    config = prompt_config(space.project, space.openapi)

    with open(config_path, "w") as file:
        from restrun import yaml

        file.write(yaml.dump(config))
