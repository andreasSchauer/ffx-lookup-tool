import typer

app = typer.Typer()

@app.command()
def hello():
    typer.echo("hello")

@app.command()
def bye():
    typer.echo("bye")

@app.command()
def hush():
    typer.echo("hush")