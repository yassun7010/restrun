import pytest

from restrun.cli import app


class TestCliAppGetCommand:
    def test_get_command(self) -> None:
        with pytest.raises(SystemExit):
            app.run(
                [
                    "get",
                    "--help",
                ]
            )
