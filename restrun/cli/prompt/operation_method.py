from typing import get_args

import rich

from restrun.cli.prompt.select import prompt_select
from restrun.core.http import Method


def prompt_operation_method(operation_method: Method | None) -> Method:
    while not operation_method:
        rich.get_console().print("[dark_orange]Operation Method[/]:")
        operation_method = prompt_select(
            options=get_args(Method),
        )

    return operation_method
