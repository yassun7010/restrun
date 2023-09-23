import sys

from logging import getLogger
from pathlib import Path

from typing_extensions import override

from .formatter import Formatter


logger = getLogger(__name__)


class BlackFormatter(Formatter):
    @override
    def format(self, target_dir: Path, *args: str) -> None:
        import black

        from click.testing import CliRunner

        if len(args) == 0:
            args = ("--quiet",)

        result = CliRunner(mix_stderr=False).invoke(
            black.main, list(args) + [str(target_dir)], catch_exceptions=True
        )

        errors = list(
            filter(lambda x: x.startswith("error: "), result.stderr.splitlines())
        )
        if len(errors) != 0:
            logger.error("black error: \n" + "\n".join(errors))
        else:
            logger.debug("black success")

        if result.exit_code != 0:
            sys.exit(result.exit_code)
