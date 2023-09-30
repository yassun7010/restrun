from restrun.cli import app
from restrun.config import Config
from tests.conftest import new_restrun_project


class TestCliAppGenerateCommand:
    def test_generate_command(self, config: Config) -> None:
        with new_restrun_project(config):
            app.run(
                [
                    "generate",
                ]
            )
