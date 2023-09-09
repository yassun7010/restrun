from typing import (
    Literal,
)

from typing_extensions import TypeAlias

from restrun.core.model import Model

URL: TypeAlias = str
Headers: TypeAlias = dict
QuryParameters: TypeAlias = dict
RequestJsonBody: TypeAlias = dict
ResponseBody: TypeAlias = str
ResponseJsonBody: TypeAlias = dict
ResponseModelBody: TypeAlias = Model

Method: TypeAlias = Literal[
    "DELETE",
    "GET",
    "PATCH",
    "POST",
    "PUT",
]
