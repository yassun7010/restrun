from pathlib import Path
from typing import TYPE_CHECKING

from .operation import OperationGenerator

if TYPE_CHECKING:
    from restrun.config import Config
    from restrun.generator import GeneratedPythonCode
    from restrun.generator.context.operation_context import OperationContext
    from restrun.generator.context.restrun_context import RestrunContext


class GetOperationGenerator(OperationGenerator):
    def generate(
        self,
        config: "Config",
        restrun_context: "RestrunContext",
        operation_context: "OperationContext",
        template_path: Path | None = None,
    ) -> "GeneratedPythonCode":
        if template_path is None:
            template_path = Path(__file__).parent / "get_operation.py.jinja"

        return super().generate(
            config, restrun_context, operation_context, template_path
        )
