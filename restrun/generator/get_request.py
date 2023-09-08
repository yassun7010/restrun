from pathlib import Path
from typing import TYPE_CHECKING

from .request import RequestGenerator

if TYPE_CHECKING:
    from restrun.config import Config
    from restrun.generator import GeneratedPythonCode
    from restrun.generator.context.request_context import RequestContext
    from restrun.generator.context.restrun_context import RestrunContext


class GetRequestGenerator(RequestGenerator):
    def generate(
        self,
        config: "Config",
        restrun_context: "RestrunContext",
        request_context: "RequestContext",
        template_path: Path | None = None,
    ) -> "GeneratedPythonCode":
        if template_path is None:
            template_path = Path(__file__).parent / "get_request.py.jinja"

        return super().generate(config, restrun_context, request_context, template_path)
