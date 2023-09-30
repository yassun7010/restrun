import pytest

from restrun.cli import app


class TestCliAppCreateCommand:
    def test_create_command(self) -> None:
        with pytest.raises(SystemExit):
            app.run(
                [
                    "create",
                    "--help",
                ]
            )
