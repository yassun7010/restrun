import typer

app = typer.Typer()


@app.command()
def new() -> None:
    print("New command")


@app.command()
def generate() -> None:
    print("Generate command")
