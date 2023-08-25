from typing import Annotated, Literal, NotRequired, TypedDict

from typer import Option

GenerateTarget = Literal["all", "model"]


class GenerateArgs(TypedDict):
    target: NotRequired[
        Annotated[
            GenerateTarget | list[GenerateTarget],
            Option(default="all"),
        ]
    ]
