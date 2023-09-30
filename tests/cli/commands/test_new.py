import contextlib

from tempfile import TemporaryDirectory

from restrun.cli import app


class TestCliAppNewCommand:
    def test_new_command(self) -> None:
        with TemporaryDirectory() as dir:
            with contextlib.chdir(dir):
                app.run(
                    [
                        "new",
                        "new_command_sample",
                        "--openapi",
                        "https://petstore3.swagger.io/api/v3/openapi.json",
                    ]
                )

    def test_new_command_with_overwrite(self) -> None:
        with contextlib.chdir("examples"):
            app.run(
                [
                    "new",
                    "new_command_sample",
                    "--openapi",
                    "https://petstore3.swagger.io/api/v3/openapi.json",
                    "--overwrite",
                ]
            )
