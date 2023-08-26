from pathlib import Path
from typing import TYPE_CHECKING

from restrun.generator.base_generator import BaseGenerator

if TYPE_CHECKING:
    from restrun.generator import GeneratedPythonCode
    from restrun.generator.context import Context


class ClientGenerator(BaseGenerator):
    def generate(
        self, context: "Context", template_path: Path | None = None
    ) -> "GeneratedPythonCode":
        if template_path is None:
            template_path = Path(__file__).parent / "client.py.jinja"

        return super().generate(context, template_path)
