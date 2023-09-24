from argparse import ArgumentParser, Namespace, _SubParsersAction
from logging import getLogger


logger = getLogger(__name__)


def add_subparser(subparsers: _SubParsersAction, **kwargs) -> None:
    help = "create operation."

    parser: ArgumentParser = subparsers.add_parser(
        "operation",
        description=help,
        help=help,
        **kwargs,
    )

    parser.add_argument(
        "--path",
        type=str,
        metavar="PATH",
        required=False,
        help='operation path like [literal]"/pets/{petId}"[/].',
    )

    parser.add_argument(
        "--overwrite",
        action="store_true",
        default=False,
        help="overwrite existing file.",
    )

    parser.set_defaults(handler=create_operation_command)


def create_operation_command(space: Namespace) -> None:
    from restrun.cli.prompt.resource_path import prompt_resource_path
    from restrun.config import find_config_file, load

    config_path = find_config_file(space.config)
    with open(config_path) as file:
        load(file)

    prompt_resource_path(space.path)

    logger.info("Successfully created operation 🎉")
