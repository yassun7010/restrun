from pathlib import Path
from typing import TYPE_CHECKING

from restrun.generator.restrun import RestrunGenerator

if TYPE_CHECKING:
    from restrun.config import Config
    from restrun.generator import GeneratedPythonCode
    from restrun.generator.context.restrun import RestrunContext


class ClientModuleGenerator(RestrunGenerator):
    def generate(
        self,
        config: "Config",
        context: "RestrunContext",
        template_path: Path | None = None,
    ) -> "GeneratedPythonCode":
        if template_path is None:
            template_path = Path(__file__).parent / "client_module.py.jinja"

        string = super().generate(config, context, template_path)

        return string
