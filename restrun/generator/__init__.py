import re
from pathlib import Path
from typing import TypeAlias

GeneratedPythonCode: TypeAlias = str


AUTO_GENERATED_COMMENT = re.compile(
    r"# Code generated by restrun \".+\"\. DO NOT EDIT\.\n"
)


def is_auto_generated(source: Path | str) -> bool:
    if isinstance(source, Path):
        with open(source, "r") as file:
            # NOTE: Considering that comments are placed at the top of the file,
            #       it is not necessary to read that many characters.
            code = file.read(200)
    else:
        code = source
    return re.search(AUTO_GENERATED_COMMENT, code) is not None
