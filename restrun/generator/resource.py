from pathlib import Path
from typing import TYPE_CHECKING

import jinja2
from jinja2 import BaseLoader, Environment

from restrun.exception import (
    FileNotFoundError,
    JinjaRenderError,
    JinjaTemplateRuntimeError,
    JinjaTemplateSyntaxError,
)
from restrun.strcase import add_strcase_filters

if TYPE_CHECKING:
    from restrun.config import Config
    from restrun.generator import GeneratedPythonCode
    from restrun.generator.context.resource_context import ResourceContext
    from restrun.generator.context.restrun_context import RestrunContext


class ResourceGenerator:
    def generate(
        self,
        config: "Config",
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
                    add_strcase_filters(
                        Environment(
                            loader=BaseLoader(),
                            undefined=jinja2.StrictUndefined,
                        )
                    )
                    .from_string(f.read())
                    .render(
                        config=config,
                        restrun=restrun_context,
                        resource=resource_context,
                    )
                ).strip() + "\n"

            except jinja2.TemplateSyntaxError as error:
                raise JinjaTemplateSyntaxError(template_path, error)

            except jinja2.TemplateRuntimeError as error:
                raise JinjaTemplateRuntimeError(template_path, error)

            except Exception as error:
                raise JinjaRenderError(template_path, error)
