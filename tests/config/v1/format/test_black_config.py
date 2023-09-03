from pathlib import Path

from restrun.config.v1.format.black_config import V1BlackConfig


class TestBlackConfig:
    def test_no_args(self) -> None:
        config = V1BlackConfig(
            formatter="black",
        )

        assert config.args == []

    def test_config_path(self) -> None:
        config = V1BlackConfig(
            formatter="black",
            config_path=Path("pyproject.toml"),
        )

        assert config.args == ["--config=pyproject.toml"]

    def test_options(self) -> None:
        config = V1BlackConfig(
            formatter="black",
            options={
                "--quit": None,
                "--line-length": 120,
                "--target-version": "py311",
            },
        )

        assert config.args == [
            "--quit",
            "--line-length=120",
            "--target-version='py311'",
        ]

    def test_options_and_config_path(self) -> None:
        config = V1BlackConfig(
            formatter="black",
            options={
                "--quit": None,
                "--line-length": 120,
                "--target-version": "py311",
                "--config": "pyproject.toml",
            },
            config_path=Path("this_path_is_not_used"),
        )

        assert config.args == [
            "--quit",
            "--line-length=120",
            "--target-version='py311'",
            "--config='pyproject.toml'",
        ]
