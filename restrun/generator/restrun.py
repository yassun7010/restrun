from pathlib import Path
from typing import TYPE_CHECKING

from jinja2 import BaseLoader, Environment

from restrun.exception import FileNotFoundError
from restrun.strcase import add_strcase_filters

if TYPE_CHECKING:
    from restrun.generator import GeneratedPythonCode
    from restrun.generator.context.restrun import RestrunContext


class RestrunGenerator:
    def generate(
        self, context: "RestrunContext", template_path: Path | None = None
    ) -> "GeneratedPythonCode":
        if template_path is None:
            raise ValueError("template_path must be specified.")

        elif not template_path.exists():
            raise FileNotFoundError(template_path)

        with open(template_path, "r") as f:
            return (
                add_strcase_filters(Environment(loader=BaseLoader()))
                .from_string(f.read())
                .render(
                    restrun=context,
                )
            ).strip() + "\n"
