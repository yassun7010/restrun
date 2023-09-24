import pytest

from restrun.cli.app import App
from restrun.config import Config
from tests.conftest import new_restrun_project


class TestCliAppCreateOperationCommand:
    def test_create_config_command_help(self) -> None:
        with pytest.raises(SystemExit):
            App.run(["create", "operation", "--help"])

    def test_create_config_command(self, config: Config) -> None:
        with new_restrun_project(config):
            App.run(
                [
                    "create",
                    "operation",
                    "--method",
                    "GET",
                    "--path",
                    "/pets",
                ]
            )
