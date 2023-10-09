from argparse import ArgumentParser, Namespace, _SubParsersAction
from logging import getLogger


logger = getLogger(__name__)


def add_subparser(subparsers: _SubParsersAction, **kwargs) -> None:
    from typing import get_args

    from restrun.core.http import Method

    description = "create operation."

    parser: ArgumentParser = subparsers.add_parser(
        "operation",
        description=description,
        help=description,
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
        "--method",
        type=str,
        choices=get_args(Method),
        required=False,
        help="operation method.",
    )

    parser.add_argument(
        "--overwrite",
        action="store_true",
        default=False,
        help="overwrite existing file.",
    )

    parser.set_defaults(handler=create_operation_command)


def create_operation_command(space: Namespace) -> None:
    from restrun.cli.prompt.operation_method import prompt_operation_method
    from restrun.cli.prompt.resource_path import prompt_resource_path
    from restrun.config import find_config_file, get_base_path, load
    from restrun.generator.context.operation_context import make_operation_context
    from restrun.generator.context.restrun_context import make_rustrun_context
    from restrun.openapi.openapi import Operation_v3_1_0
    from restrun.writer import write_operation

    config_path = find_config_file(space.config)
    with open(config_path) as file:
        config = load(file)

    path = prompt_resource_path(space.path)
    method = prompt_operation_method(space.method)

    base_dir = get_base_path(config, config_path)
    restrun_context = make_rustrun_context(base_dir, config)

    if operation_context := make_operation_context(
        method,
        ["https://petstore.swagger.io/"],
        path,
        Operation_v3_1_0(),
        {},
    ):
        write_operation(
            base_dir,
            config,
            restrun_context,
            operation_context,
        )

        logger.info("Successfully created operation 🎉")
