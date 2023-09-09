import jinja2
from humps import pascalize


def module_name(name: str) -> str:
    """Convert string to python module name."""
    return _convert_unavailable_chars_to_underbar(name.strip("/")).lower()


def class_name(name: str) -> str:
    """Convert string to python class name."""
    return "".join(
        [pascalize(s) for s in _convert_unavailable_chars_to_underbar(name).split("_")]
    )


def _convert_unavailable_chars_to_underbar(name: str) -> str:
    return name.replace("-", "_").replace(".", "_").replace("/", "_")


def add_strcase_filters(env: jinja2.Environment) -> jinja2.Environment:
    env.filters["module_name"] = module_name
    env.filters["class_name"] = class_name
    return env
