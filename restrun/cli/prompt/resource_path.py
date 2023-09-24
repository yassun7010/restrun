def prompt_resource_path(resource_path: str | None) -> str:
    from rich.prompt import Prompt

    while not resource_path:
        resource_path = Prompt.ask(
            '[dark_orange]Resource Path[/] (like [green]"/ptes/{petId}"[/])',
        )

    return resource_path
