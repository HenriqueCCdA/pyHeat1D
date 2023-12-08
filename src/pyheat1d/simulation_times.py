"""Módulo com as funcionalidades de medição de tempos da analise."""

from dataclasses import dataclass
from functools import wraps
from time import perf_counter


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
