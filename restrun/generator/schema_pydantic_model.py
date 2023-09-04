from pathlib import Path
from typing import TYPE_CHECKING

from restrun.generator.schema import SchemaGenerator

if TYPE_CHECKING:
    from restrun.config import Config
    from restrun.generator import GeneratedPythonCode
    from restrun.generator.context.restrun_context import RestrunContext
    from restrun.generator.context.schema_context import SchemaContext


class SchemaPydanticModelGenerator(SchemaGenerator):
    def generate(
        self,
        config: "Config",
        restrun_context: "RestrunContext",
        schema_context: "SchemaContext",
        template_path: Path | None = None,
    ) -> "GeneratedPythonCode":
        if template_path is None:
            template_path = Path(__file__).parent / "schema_pydantic_model.py.jinja"

        return super().generate(config, restrun_context, schema_context, template_path)
