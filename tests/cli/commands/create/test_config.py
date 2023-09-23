import os

from tempfile import TemporaryDirectory

from restrun.cli.app import App
from tests.data import DATA_DIR


class TestCliAppCreateConfigCommand:
    def test_create_config(self) -> None:
        with TemporaryDirectory() as dir:
            os.chdir(dir)
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
