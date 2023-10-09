from pathlib import Path
from typing import TYPE_CHECKING

from restrun.generator import render_template


if TYPE_CHECKING:
    from restrun.config import Config
    from restrun.generator import GeneratedPythonCode
    from restrun.generator.context.resource_context import ResourceContext
    from restrun.generator.context.restrun_context import RestrunContext


def generate_resource_module(
    config: "Config",
    restrun_context: "RestrunContext",
    resource_context: "ResourceContext",
    template_path: Path | None = None,
) -> "GeneratedPythonCode":
    if template_path is None:
        template_path = Path(__file__).parent / "resource_module.py.jinja"

    return render_template(
        template_path,
        config=config,
        restrun=restrun_context,
        resource=resource_context,
    )
