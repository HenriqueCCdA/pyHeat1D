from pathlib import Path
from typing import Annotated

import typer
from click import Context
from rich.console import Console

from pyheat1d.edp import Edo
from pyheat1d.input_files import load_input_file

console = Console()

app = typer.Typer(add_completion=False, pretty_exceptions_show_locals=False)


def version_callback(value: bool):
    if value:
        import importlib

        version = importlib.metadata.version("pyheat1d")
        console.print(f"pyheat1d {version}")
        raise typer.Exit()


@app.callback(invoke_without_command=True)
def typer_callback(
    ctx: Context,
    version: Annotated[
        bool, typer.Option("--version", "-v", help="Versão do FORM.", callback=version_callback)
    ] = False,
):
    if ctx.invoked_subcommand:
        return
    console.print("[yellow]Usage[/yellow]: [green]pyheat1D[/green] [OPTIONS] COMMAND [ARGS]...\n")
    console.print("[blue]--help[/blue] for more informations.")


@app.command()
def run(input_file: Annotated[Path, typer.Argument(..., help="Caminho do arquivos de entra.")]):
    """Rodando a analise."""
    input_file_path = input_file.absolute()
    base_dir_path = input_file_path.parent

    input_data = load_input_file(input_file_path)

    edo = Edo(input_data, base_dir_path)

    edo.resolve()
