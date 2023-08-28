from pathlib import Path
from typing import TYPE_CHECKING

from restrun.generator.restrun import RestrunGenerator

if TYPE_CHECKING:
    from restrun.generator import GeneratedPythonCode
    from restrun.generator.context.restrun import RestrunContext


class ClientMixinsModuleGenerator(RestrunGenerator):
    def generate(
        self, context: "RestrunContext", template_path: Path | None = None
    ) -> "GeneratedPythonCode":
        if template_path is None:
            template_path = Path(__file__).parent / "client_mixins_module.py.jinja"

        string = super().generate(context, template_path)

        return string
