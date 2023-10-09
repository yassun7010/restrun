import os

from pathlib import Path

from rich.prompt import Prompt

from restrun.utils.strcase import module_name


def prompt_project_name(project_name: str | None) -> str:
    while not project_name:
        project_name = Prompt.ask(
            "[dark_orange]Project Name[/]",
            default=module_name(Path(os.getcwd()).name),
        )

    return project_name
