import contextlib

from tempfile import TemporaryDirectory

from restrun.cli.app import App
from tests.data import DATA_DIR


class TestCliAppCreateConfigCommand:
    def test_create_config_command(self) -> None:
        with TemporaryDirectory() as dir:
            with contextlib.chdir(dir):
                App.run(
                    [
                        "create",
                        "config",
                        "--project",
                        "test",
                        "--openapi",
                        str(DATA_DIR / "petstore.openapi_v3_0_2.json"),
                    ]
                )

    def test_create_config_command_another_filepath(self) -> None:
        with TemporaryDirectory() as dir:
            with contextlib.chdir(dir):
                App.run(
                    [
                        "--config",
                        "resturn.json",
                        "create",
                        "config",
                        "--project",
                        "test",
                        "--openapi",
                        str(DATA_DIR / "petstore.openapi_v3_0_2.json"),
                    ]
                )
