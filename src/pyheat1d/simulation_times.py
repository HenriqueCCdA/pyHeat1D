"""Módulo com as funcionalidades de medição de tempos da analise."""

from dataclasses import dataclass
from functools import wraps
from json import dump as json_dump
from pathlib import Path
from time import perf_counter

from rich.console import Console

from pyheat1d.errors import TimeLogWriteFileError


@dataclass
class Times:
    """Class com os tempos da analise."""

    cell_loop: float = 0.0
    solver: float = 0.0
    edp: float = 0.0

    def reset(self):
        """Zera todos os tempos."""
        self.cell_loop = 0.0
        self.solver = 0.0
        self.edp = 0.0

    def print_stdout_simulation_times(self) -> None:
        """Escreve os tempos no console."""

        console = Console()

        console.print(f"Edp      : {self.edp:.3f}")
        console.print(f"Cell loop: {self.cell_loop:.3f}")
        console.print(f"Solver   : {self.solver:.3f}")

    def write_log_simulation_times(self, folder=Path) -> None:
        """Escreve os tempos em um arquivo.
        Parameters:
            folder: Diretorio onde o arquivo será escrito.
        """

        new_file = folder / "time_log.json"

        try:
            json_dump(
                {
                    "edp": self.edp,
                    "solver": self.solver,
                    "cell_loop": self.cell_loop,
                },
                new_file.open(mode="w", encoding="utf8"),
            )

        except FileNotFoundError as e:
            raise TimeLogWriteFileError(file=str(new_file)) from e


run_times = Times()


def register_timer(name: str):
    """Registra função ou método que será registrado o tempo.

    Parameters:
        name: O nome referente a dataclasses Times.
    """

    def decorator_register_timer(func):
        @wraps(func)
        def inner(*args, **kwargs):
            start = perf_counter()
            value = func(*args, **kwargs)
            delta = perf_counter() - start
            setattr(run_times, name, getattr(run_times, name) + delta)
            return value

        return inner

    return decorator_register_timer

    def print_stdout_simulation_times(self) -> None:
        """Escreve os tempos no console."""

        console = Console()

        console.print(f"Edp      : {run_times.edp:.3f}")
        console.print(f"Cell loop: {run_times.cell_loop:.3f}")
        console.print(f"Solver   : {run_times.solver:.3f}")

    def write_log_simulation_times(self, folder=Path) -> None:
        """Escreve os tempos em um arquivo.
        Parameters:
            folder: Diretorio onde o arquivo será escrito.
        """

        new_file = folder / "time_log.json"

        try:
            json_dump(
                {
                    "edp": run_times.edp,
                    "solver": run_times.solver,
                    "cell_loop": run_times.cell_loop,
                },
                new_file.open(mode="w", encoding="utf8"),
            )

        except FileNotFoundError as e:
            raise TimeLogWriteFileError(file=str(new_file)) from e
