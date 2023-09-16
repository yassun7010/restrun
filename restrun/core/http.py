from typing import Any, Literal, Mapping, TypeVar

from typing_extensions import TypeAlias

from restrun.core.model import Model

URL: TypeAlias = str
Headers: TypeAlias = dict
QuryParameters: TypeAlias = Mapping
RequestJsonBody: TypeAlias = Mapping
ResponseDictBody = TypeVar("ResponseDictBody", bound=Mapping)
ResponseModelBody = TypeVar("ResponseModelBody", bound=Model)
_SingleResponse = (
    Model | ResponseModelBody | Mapping[str, Any] | ResponseDictBody | str | int | float
)
Response = _SingleResponse | list[_SingleResponse] | None

Method: TypeAlias = Literal[
    "DELETE",
    "GET",
    "PATCH",
    "POST",
    "PUT",
]
