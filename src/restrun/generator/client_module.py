from pathlib import Path
from typing import TYPE_CHECKING

from restrun.generator import render_template


if TYPE_CHECKING:
    from restrun.config import Config
    from restrun.generator import GeneratedPythonCode
    from restrun.generator.context.resources_context import ResourcesContext
    from restrun.generator.context.restrun_context import RestrunContext


def generate_client_module(
    config: "Config",
    restrun_context: "RestrunContext",
    resources_context: "ResourcesContext",
    template_path: Path | None = None,
) -> "GeneratedPythonCode":
    if template_path is None:
        template_path = Path(__file__).parent / "client_module.py.jinja"

    string = render_template(
        template_path,
        config=config,
        restrun=restrun_context,
        resources=resources_context,
    )

    return string
