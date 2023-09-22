import os
from restrun.cli.app import App


class TestCliAppNewCommand:
    def test_new_command(self) -> None:
        os.chdir("examples")
        App.run(
            [
                "new",
                "new_command_sample",
                "--openapi",
                "https://petstore3.swagger.io/api/v3/openapi.json",
            ]
        )
