import os

from pathlib import Path

from rich.prompt import Prompt

from restrun.exceptions import ProjectNameRequiredError
from restrun.strcase import module_name


def prompt_project_name(project_name: str | None) -> str:
    if project_name is None:
        project_name = Prompt.ask(
            "[dark_orange]Project Name[/]",
            default=module_name(Path(os.getcwd()).name),
        )
        if len(project_name) == 0:
            raise ProjectNameRequiredError()

    return project_name
