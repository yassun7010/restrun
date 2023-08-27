from typing import (
    Literal,
    LiteralString,
)

from typing_extensions import TypeAlias

from restrun.core.model import Model

URL: TypeAlias = LiteralString
Headers: TypeAlias = dict
QuryParameters: TypeAlias = dict
RequestJsonBody: TypeAlias = dict
ResponseBody: TypeAlias = str
ResponseJsonBody: TypeAlias = dict
ResponseModelBody: TypeAlias = Model

Method = Literal[
    "DELETE",
    "GET",
    "PATCH",
    "POST",
    "PUT",
]
