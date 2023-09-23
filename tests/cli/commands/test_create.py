import pytest

from restrun.cli.app import App


class TestCliAppCreateCommand:
    def test_create_command(self) -> None:
        with pytest.raises(SystemExit):
            App.run(
                [
                    "create",
                    "--help",
                ]
            )
