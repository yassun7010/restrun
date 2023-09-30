from restrun.cli import app
from tests.__data__ import DATA_DIR


class TestCliAppGetConfigCommand:
    def test_get_config_command(self) -> None:
        app.run(
            [
                "--config",
                str(DATA_DIR / "restrun.yml"),
                "get",
                "config",
            ]
        )
