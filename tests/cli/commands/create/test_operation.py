import pytest

from restrun.cli import app
from restrun.config import Config
from tests.conftest import new_restrun_project


class TestCliAppCreateOperationCommand:
    def test_create_config_command_help(self) -> None:
        with pytest.raises(SystemExit):
            app.run(["create", "operation", "--help"])

    def test_create_config_command(self, config: Config) -> None:
        with new_restrun_project(config):
            app.run(
                [
                    "create",
                    "operation",
                    "--method",
                    "GET",
                    "--path",
                    "/pets",
                ]
            )
