from logging import getLogger
from pathlib import Path

from isort.main import main as isort
from typing_extensions import override

from .formatter import Formatter

logger = getLogger(__name__)


class IsortFormatter(Formatter):
    @override
    def format(self, target_dir: Path, *args: str) -> None:
        if len(args) == 0:
            args = ("--quiet",)

        try:
            isort([str(target_dir)] + list(args))
            logger.debug("isort success")

        except SystemExit as exit:
            logger.error(f"isort error: {exit}")
