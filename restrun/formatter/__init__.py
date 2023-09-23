from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from pathlib import Path

    from restrun.config import Config


def format_python_codes(base_dir: "Path", config: "Config") -> None:
    for format in config.formats or []:
        if format.formatter == "isort":
            from restrun.formatter.isort import IsortFormatter

            IsortFormatter().format(base_dir, *format.args)

        if format.formatter == "black":
            from restrun.formatter.black import BlackFormatter

            BlackFormatter().format(base_dir)
