from pathlib import Path

from restrun.config.v1.lint.ruff_config import V1RuffConfig


class TestRuffConfig:
    def test_no_args(self) -> None:
        config = V1RuffConfig(
            linter="ruff",
        )

        assert config.args == []

    def test_config_path(self) -> None:
        config = V1RuffConfig(
            linter="ruff",
            config_path=Path("ruff.toml"),
        )

        assert config.args == ["--config=ruff.toml"]

    def test_options(self) -> None:
        config = V1RuffConfig(
            linter="ruff",
            options={
                "--quiet": None,
                "--target-version": "py311",
            },
        )

        assert config.args == [
            "--quiet",
            "--target-version='py311'",
        ]
