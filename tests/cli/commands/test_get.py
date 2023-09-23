import pytest

from restrun.cli.app import App


class TestCliAppGetCommand:
    def test_get_command(self) -> None:
        with pytest.raises(SystemExit):
            App.run(
                [
                    "get",
                    "--help",
                ]
            )
