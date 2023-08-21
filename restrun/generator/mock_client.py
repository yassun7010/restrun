from pathlib import Path
from typing import TYPE_CHECKING

from jinja2 import BaseLoader, Environment

if TYPE_CHECKING:
    from restrun.generator import GeneratedPythonCode
    from restrun.generator.context import Context


class MockClientGenerator:
    def generate(
        self, context: "Context", template_path: Path | None = None
    ) -> "GeneratedPythonCode":
        if template_path is None:
            template_path = Path(__file__).parent / "mock_client.py.jinja"

        with open(template_path, "r") as f:
            return (
                Environment(loader=BaseLoader())
                .from_string(f.read())
                .render(context.model_dump())
            )
