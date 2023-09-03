from pathlib import Path
from typing import Literal

from restrun.core.model import ExtraForbidModel


class V1BlackConfig(ExtraForbidModel):
    formatter: Literal["black"]
    options: dict[str, str | int | None] | None = None
    config_path: Path | None = None

    @property
    def args(self) -> list[str]:
        args = []
        if self.options is not None:
            for key, value in self.options.items():
                if value is not None:
                    args.append(f"{key}={repr(value)}")
                else:
                    args.append(key)

        if self.config_path is not None and "--config" not in (self.options or {}):
            args.append(f"--config={self.config_path}")

        return args
