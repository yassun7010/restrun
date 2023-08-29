from pathlib import Path
from typing import TYPE_CHECKING

import jinja2
from jinja2 import BaseLoader, Environment

from restrun.exception import (
    FileNotFoundError,
    JinjaTemplateRuntimeError,
    JinjaTemplateSyntaxError,
)
from restrun.strcase import add_strcase_filters

if TYPE_CHECKING:
    from restrun.generator import GeneratedPythonCode
    from restrun.generator.context.resource import ResourceContext
    from restrun.generator.context.restrun import RestrunContext


class ResourceGenerator:
    def generate(
        self,
        restrun_context: "RestrunContext",
        resource_context: "ResourceContext",
        template_path: Path | None = None,
    ) -> "GeneratedPythonCode":
        if template_path is None:
            raise ValueError("template_path must be specified.")

        elif not template_path.exists():
            raise FileNotFoundError(template_path)

        with open(template_path, "r") as f:
            try:
                return (
                    add_strcase_filters(Environment(loader=BaseLoader()))
                    .from_string(f.read())
                    .render(
                        restrun=restrun_context,
                        resource=resource_context,
                    )
                ).strip() + "\n"

            except jinja2.TemplateSyntaxError as error:
                raise JinjaTemplateSyntaxError(template_path, error)

            except jinja2.TemplateRuntimeError as error:
                raise JinjaTemplateRuntimeError(template_path, error)
