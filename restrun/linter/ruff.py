import os
import subprocess
import sys
from logging import getLogger
from pathlib import Path

from typing_extensions import override

from .linter import Linter

logger = getLogger(__name__)


class RuffLinter(Linter):
    @override
    def lint(self, target_dir: Path, *args: str) -> None:
        from ruff.__main__ import find_ruff_bin

        if len(args) == 0:
            args = ("--fix",)

        ruff = find_ruff_bin()
        completed_process = subprocess.run(
            [os.fsdecode(ruff), "check", *args, target_dir], capture_output=True
        )

        if len(completed_process.stderr) > 0:
            logger.error("ruff error: \n" + completed_process.stderr.decode())
        else:
            logger.debug("ruff success")

        if len(completed_process.stdout) > 0:
            logger.debug("ruff output: \n" + completed_process.stdout.decode())

        if completed_process.returncode != 0:
            sys.exit(completed_process.returncode)
