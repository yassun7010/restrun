from typing import (
    Literal,
    Mapping,
    TypeVar,
)

from typing_extensions import TypeAlias

from restrun.core.model import Model

URL: TypeAlias = str
Headers: TypeAlias = dict
QuryParameters: TypeAlias = Mapping
RequestJsonBody: TypeAlias = Mapping
ResponseBody: TypeAlias = str
ResponseJsonBody: TypeAlias = Mapping
ResponseModelBody = TypeVar("ResponseModelBody", bound=Model)

Method: TypeAlias = Literal[
    "DELETE",
    "GET",
    "PATCH",
    "POST",
    "PUT",
]
