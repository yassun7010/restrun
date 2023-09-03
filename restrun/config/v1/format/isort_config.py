from pathlib import Path
from typing import Literal

from restrun.core.model import ExtraForbidModel


class V1IsortConfig(ExtraForbidModel):
    formatter: Literal["isort"]
    options: dict[str, str | None] | None = None
    settings_path: Path | None = None

    @property
    def args(self) -> list[str]:
        args = []
        if self.options is not None:
            for key, value in self.options.items():
                if value is not None:
                    args.append(f"{key}={repr(value)}")
                else:
                    args.append(key)
        if (
            self.settings_path is not None
            and len(
                set(["--sp", "--settings-path", "--settings-file", "--settings"])
                & set((self.options or {}).keys())
            )
            == 0
        ):
            args.append(f"--settings-path={self.settings_path}")

        return args
