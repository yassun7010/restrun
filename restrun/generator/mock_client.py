from pathlib import Path
from typing import TYPE_CHECKING

from .restrun import RestrunGenerator

if TYPE_CHECKING:
    from restrun.generator import GeneratedPythonCode
    from restrun.generator.context.restrun import RestrunContext


class MockClientGenerator(RestrunGenerator):
    def generate(
        self, context: "RestrunContext", template_path: Path | None = None
    ) -> "GeneratedPythonCode":
        if template_path is None:
            template_path = Path(__file__).parent / "mock_client.py.jinja"

        return super().generate(context, template_path)
