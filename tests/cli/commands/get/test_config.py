from restrun.cli.app import App
from tests.data import DATA_DIR


class TestCliAppGetConfigCommand:
    def test_get_config_command(self) -> None:
        App.run(
            [
                "--config",
                str(DATA_DIR / "restrun.yml"),
                "get",
                "config",
            ]
        )
