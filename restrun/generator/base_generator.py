from pathlib import Path
from typing import TYPE_CHECKING

from jinja2 import BaseLoader, Environment

import restrun
from restrun.exception import RestrunFileNotFoundError

if TYPE_CHECKING:
    from restrun.generator import GeneratedPythonCode
    from restrun.generator.context import Context


class BaseGenerator:
    def generate(
        self, context: "Context", template_path: Path | None = None
    ) -> "GeneratedPythonCode":
        if template_path is None:
            raise ValueError("template_path must be specified.")

        elif not template_path.exists():
            raise RestrunFileNotFoundError(template_path)

        with open(template_path, "r") as f:
            return (
                Environment(loader=BaseLoader())
                .from_string(f.read())
                .render(
                    context.model_dump(),
                    version=restrun.__version__,
                )
            )
