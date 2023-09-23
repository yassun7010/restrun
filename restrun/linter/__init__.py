from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from pathlib import Path

    from restrun.config import Config


def lint_python_codes(base_dir: "Path", config: "Config") -> None:
    for lint in config.lints or []:
        if lint.linter == "ruff":
            from restrun.linter.ruff import RuffLinter

            RuffLinter().lint(base_dir)
