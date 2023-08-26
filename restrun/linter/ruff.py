import os
import subprocess
import sys
from logging import getLogger
from pathlib import Path

from .linter import Linter

logger = getLogger(__name__)


class RuffLinter(Linter):
    def lint(self, target_dir: Path, *args: str) -> None:
        from ruff.__main__ import find_ruff_bin

        if len(args) == 0:
            args = ("--fix",)

        ruff = find_ruff_bin()
        completed_process = subprocess.run(
            [os.fsdecode(ruff), *args, target_dir], capture_output=True
        )

        if len(completed_process.stderr) > 0:
            logger.error("Ruff error: \n" + completed_process.stderr.decode())

        logger.debug("Ruff output: \n" + completed_process.stdout.decode())

        sys.exit(completed_process.returncode)
