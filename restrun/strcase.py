import jinja2
from humps import depascalize, pascalize


def module_name(name: str) -> str:
    """Convert string to python module name."""
    return depascalize(_sanitize(name))


def class_name(name: str) -> str:
    """Convert string to python class name."""
    return "".join([pascalize(s) for s in _sanitize(name).split("_")])


def _sanitize(name: str) -> str:
    return _convert_unavailable_chars_to_underbar(_remove_bracket(name.strip("/")))


def _remove_bracket(name: str) -> str:
    return name.replace("{", "").replace("}", "")


def _convert_unavailable_chars_to_underbar(name: str) -> str:
    return name.replace("-", "_").replace(".", "_").replace("/", "_")


def add_strcase_filters(env: jinja2.Environment) -> jinja2.Environment:
    env.filters["module_name"] = module_name
    env.filters["class_name"] = class_name
    return env
