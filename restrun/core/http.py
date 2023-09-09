from typing import (
    Literal,
    TypeVar,
)

from typing_extensions import TypeAlias

from restrun.core.model import Model

URL: TypeAlias = str
Headers: TypeAlias = dict
QuryParameters: TypeAlias = dict
RequestJsonBody: TypeAlias = dict
ResponseBody: TypeAlias = str
ResponseJsonBody: TypeAlias = dict
ResponseModelBody = TypeVar("ResponseModelBody", bound=Model)

Method = Literal[
    "DELETE",
    "GET",
    "PATCH",
    "POST",
    "PUT",
]
