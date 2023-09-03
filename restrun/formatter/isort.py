from logging import getLogger
from pathlib import Path

from isort.__main__ import main as isort
from typing_extensions import override

from .formatter import Formatter

logger = getLogger(__name__)


class IsortFormatter(Formatter):
    @override
    def format(self, target_dir: Path, *args: str) -> None:
        isort([str(target_dir)] + list(args))
