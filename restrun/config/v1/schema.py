from typing import Annotated, Literal

from pydantic import Field

from restrun.core.model import ExtraForbidModel


class V1Schema(ExtraForbidModel):
    schema_type: Annotated[
        Literal["pydantic", "typed_dict"],
        Field(
            title="schema type.",
            description="`pydantic` or `typed_dict`.",
        ),
    ] = "pydantic"
