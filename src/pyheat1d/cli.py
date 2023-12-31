import json
from pathlib import Path
from typing import Annotated

import matplotlib.pyplot as plt
import typer
from click import Context
from rich.console import Console

from pyheat1d.controllers import run as run_controller
from pyheat1d.errors import FileMeshNotFoundError, FileResultshNotFoundError
from pyheat1d.simulation_times import run_times

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

    run_controller(input_file=input_file)
    run_times.print_stdout_simulation_times()


@app.command()
def plot(
    output_dir: Annotated[Path, typer.Argument(..., help="Caminho do diretorio de saida.")],
    steps: Annotated[str, typer.Option(prompt="Caminho do diretorio de saida.")],
):
    """Plotando o resultado da analise."""

    try:
        file_mesh = output_dir / "mesh.json"
        file_results = output_dir / "results.json"

        if not file_mesh.exists():
            raise FileMeshNotFoundError()

        if not file_results.exists():
            raise FileResultshNotFoundError()

        mesh = json.load(file_mesh.open())
        results = json.load(file_results.open())

        xp = mesh["xp"]
        fig, ax = plt.subplots()
        for istep in map(int, steps.split(",")):
            try:
                t = results[istep]["t"]
                u = results[istep]["u"]
                plt.plot(xp, u, label=f"time = {t} s")
            except IndexError:
                console.print(f"O step {istep} não existe portando será ignorado. O Ultimo step é {len(results)-1}.")
                break

        ax.set_xlabel("x")
        ax.set_ylabel("T(°C)")
        plt.legend()
        plt.grid()
        plt.show()
    except (FileMeshNotFoundError, FileResultshNotFoundError) as e:
        console.print(f"[red]Error[/red]: {e}")
        raise typer.Exit(1) from e
