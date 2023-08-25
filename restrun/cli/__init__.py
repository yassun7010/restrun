from typing import Unpack

import typer

from restrun.cli.commands.generate import GenerateArgs

app = typer.Typer()


@app.command()
def new() -> None:
    print("New command")


@app.command()
def generate(**kwargs: Unpack[GenerateArgs]) -> None:
    print("Generate command")
