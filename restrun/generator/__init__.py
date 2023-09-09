import re
from dataclasses import dataclass
from pathlib import Path
from typing import Generic, Type, TypeAlias, TypeVar

import jinja2

import restrun
from restrun.exception import (
    JinjaRenderError,
    JinjaTemplateRuntimeError,
    JinjaTemplateSyntaxError,
    PythonFileExecutionError,
)
from restrun.strcase import add_strcase_filters

PythonCode: TypeAlias = str
GeneratedPythonCode: TypeAlias = str

T = TypeVar("T")

AUTO_GENERATED_DOC_COMMENT_PATTERN = re.compile(
    r"# Code generated by restrun \".+\"\.\n"
)
AUTO_GENERATED_DOC_COMMENT = f"""
#
# Code generated by restrun "{ restrun.__version__ }".
#
# Removing this comment from this file will exclude it from automatic generation target
# and it will not be updated, unless the file contents are empty.
# If you wish to make special modifications to the auto-generated code,
# please remove this comment.
#
# For more information about restrun,
# please refer to https://github.com/yassun7010/restrun .
#
""".strip()


def is_auto_generated_or_empty(source: Path | PythonCode) -> bool:
    if isinstance(source, Path):
        with open(source, "r") as file:
            # NOTE: Considering that comments are placed at the top of the file,
            #       it is not necessary to read that many characters.
            code = file.read(200)
    else:
        code = source

    if code.strip() == "":
        return True

    return re.search(AUTO_GENERATED_DOC_COMMENT_PATTERN, code) is not None


@dataclass(frozen=True)
class ClassInfo(Generic[T]):
    module_name: str
    class_name: str
    class_type: Type[T]


def load_python_code(source: Path) -> dict:
    locals = {}
    with open(source, "r") as file:
        code = file.read()

    try:
        exec(code, None, locals)
    except Exception as error:
        raise PythonFileExecutionError(source, error=error)

    return locals


def find_classes_from_code(
    source: Path,
    *class_types: Type,
) -> dict[Type, list[ClassInfo]]:
    locales = load_python_code(source)
    result = {class_type: [] for class_type in class_types}
    for name, variable in locales.items():
        for class_type in class_types:
            try:
                if issubclass(variable, class_type) and variable is not class_type:
                    result[class_type].append(
                        ClassInfo(
                            module_name=source.stem,
                            class_name=name,
                            class_type=variable,
                        )
                    )

            except TypeError:
                pass

    return result


def render_template(template_path: Path, **kwargs) -> "GeneratedPythonCode":
    if template_path is None:
        raise ValueError("template_path must be specified.")

    elif not template_path.exists():
        raise FileNotFoundError(template_path)

    with open(template_path, "r") as f:
        try:
            return (
                add_strcase_filters(
                    jinja2.Environment(
                        loader=jinja2.BaseLoader(),
                        undefined=jinja2.StrictUndefined,
                    )
                )
                .from_string(f.read())
                .render(
                    auto_generated_doc_comment=AUTO_GENERATED_DOC_COMMENT,
                    **kwargs,
                )
            ).strip() + "\n"

        except jinja2.TemplateSyntaxError as error:
            raise JinjaTemplateSyntaxError(template_path, error)

        except jinja2.TemplateRuntimeError as error:
            raise JinjaTemplateRuntimeError(template_path, error)

        except Exception as error:
            raise JinjaRenderError(template_path, error)
