from pathlib import Path

from restrun.cli.prompt.project_name import prompt_project_name
from restrun.cli.prompt.source import prompt_source
from restrun.config.v1 import V1Config
from restrun.strcase import module_name


def prompt_config(
    project_name: str | None,
    openapi_location: str | None = None,
) -> V1Config:
    project_name = prompt_project_name(project_name)
    source = prompt_source(openapi_location)
    project_path = Path(module_name(project_name))
    if not project_path.exists():
        project_path.mkdir()

    return V1Config(
        version="1",
        name=project_name,
        source=source,
    )
