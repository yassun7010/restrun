from pathlib import Path
from typing import TYPE_CHECKING

from restrun.generator import render_template

if TYPE_CHECKING:
    from restrun.config import Config
    from restrun.generator import GeneratedPythonCode
    from restrun.generator.context.restrun_context import RestrunContext
    from restrun.generator.context.schema_context import SchemaContext


class SchemaGenerator:
    def generate(
        self,
        config: "Config",
        restrun_context: "RestrunContext",
        schema_context: "SchemaContext",
        template_path: Path | None = None,
    ) -> "GeneratedPythonCode":
        if template_path is None:
            template_path = Path(__file__).parent / "schema.py.jinja"

        return render_template(
            template_path,
            config=config,
            restrun=restrun_context,
            schema=schema_context,
        )
