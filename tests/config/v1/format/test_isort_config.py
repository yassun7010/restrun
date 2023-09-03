from pathlib import Path

from restrun.config.v1.format.isort_config import V1IsortConfig


class TestIsortConfig:
    def test_no_args(self) -> None:
        config = V1IsortConfig(
            formatter="isort",
        )

        assert config.args == []

    def test_settings_path(self) -> None:
        config = V1IsortConfig(
            formatter="isort",
            settings_path=Path("pyproject.toml"),
        )

        assert config.args == ["--settings-path=pyproject.toml"]

    def test_options(self) -> None:
        config = V1IsortConfig(
            formatter="isort",
            options={
                "--line-length": 120,
                "--force-grid-wrap": None,
            },
        )

        assert config.args == ["--line-length=120", "--force-grid-wrap"]

    def test_options_and_settings_path(self) -> None:
        config = V1IsortConfig(
            formatter="isort",
            options={
                "--line-length": 120,
                "--force-grid-wrap": None,
                "--settings-path": "pyproject.toml",
            },
            settings_path=Path("this_path_is_not_used"),
        )

        assert config.args == [
            "--line-length=120",
            "--force-grid-wrap",
            "--settings-path='pyproject.toml'",
        ]
