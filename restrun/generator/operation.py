from pathlib import Path
from typing import TYPE_CHECKING

from restrun.generator import render_template


if TYPE_CHECKING:
    from restrun.config import Config
    from restrun.generator import GeneratedPythonCode
    from restrun.generator.context.operation_context import OperationContext
    from restrun.generator.context.restrun_context import RestrunContext


class OperationGenerator:
    def generate(
        self,
        config: "Config",
        restrun_context: "RestrunContext",
        operation_context: "OperationContext",
        template_path: Path | None = None,
    ) -> "GeneratedPythonCode":
        if template_path is None:
            template_path = Path(__file__).parent / "operation.py.jinja"

        return render_template(
            template_path,
            config=config,
            restrun=restrun_context,
            operation=operation_context,
        )
