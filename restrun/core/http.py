from typing import Any, Literal, Mapping, TypeVar

from typing_extensions import TypeAlias

from restrun.core.model import Model

URL: TypeAlias = str
Headers: TypeAlias = dict
QuryParameters: TypeAlias = Mapping
RequestJsonBody: TypeAlias = Mapping
ResponseBody: TypeAlias = str
ResponseDictBody = TypeVar("ResponseDictBody", bound=Mapping)
ResponseModelBody = TypeVar("ResponseModelBody", bound=Model)
_SingleResponseType = (
    Model | ResponseModelBody | Mapping[str, Any] | ResponseDictBody | str | int | float
)
ResponseType = _SingleResponseType | list[_SingleResponseType] | None

Method: TypeAlias = Literal[
    "DELETE",
    "GET",
    "PATCH",
    "POST",
    "PUT",
]
