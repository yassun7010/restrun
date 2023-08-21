from typing import LiteralString

from typing_extensions import TypeAlias, TypeVar

from restrun.core.model import Model

URL: TypeAlias = LiteralString
Headers = TypeVar("Headers", bound=dict)
QuryParameters = TypeVar("QuryParameters", bound=dict)
RequestJsonBody = TypeVar("RequestJsonBody", bound=dict)
ResponseJsonBody = TypeVar("ResponseJsonBody", bound=dict)
ResponseModelBody = TypeVar("ResponseModelBody", bound=Model)
