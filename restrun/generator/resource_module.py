from pathlib import Path
from typing import TYPE_CHECKING

from restrun.generator.resource import ResourceGenerator

if TYPE_CHECKING:
    from restrun.generator import GeneratedPythonCode
    from restrun.generator.context.resource import ResourceContext
    from restrun.generator.context.restrun import RestrunContext


class ResourceModuleGenerator(ResourceGenerator):
    def generate(
        self,
        restrun_context: "RestrunContext",
        resource_context: "ResourceContext",
        template_path: Path | None = None,
    ) -> "GeneratedPythonCode":
        if template_path is None:
            template_path = Path(__file__).parent / "resource_module.py.jinja"

        string = super().generate(restrun_context, resource_context, template_path)

        return string
