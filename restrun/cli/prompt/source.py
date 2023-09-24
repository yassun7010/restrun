import rich

from rich.prompt import Prompt

from restrun.cli.prompt.select import select_prompt
from restrun.config.v1.source import SourceType
from restrun.config.v1.source.openapi_source import V1OpenAPISource
from restrun.exceptions import NeverReachError


def prompt_source(openapi_location: str | None) -> V1OpenAPISource | None:
    source_type: SourceType | None = None
    if openapi_location is not None:
        source_type = "openapi"

    if source_type is None:
        options: list[SourceType] = ["manual", "openapi"]

        rich.get_console().print("[dark_orange]Source Type[/]:")
        source_type = select_prompt(
            options=options,
        )

    match source_type:
        case "openapi":
            while not openapi_location:
                openapi_location = Prompt.ask(
                    "[dark_orange]OpenAPI Location[/]",
                    default="https://petstore.swagger.io/v2/swagger.json",
                )

            return V1OpenAPISource(
                type=source_type,
                location=openapi_location,  # type: ignore
            )

        case "manual":
            return None

        case _:
            raise NeverReachError(source_type)
