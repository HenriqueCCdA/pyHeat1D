import json
from pathlib import Path

import numpy as np


class WriterResults:
    """
    Gerenciador de context usado para escrever os resultados.

    Parameters:
        path (Path): Número de passos.
        intentdt (None | int): Indentação do json
    """

    def __init__(self, path: Path, indent: int | None = None) -> None:
        """
        Parameters:
            path (Path): Número de passos.
            intentdt (None | int): Indentação do json
        """
        self.results: list[dict] = []
        self.indent = indent
        self.path = path

    def __enter__(self):
        self.fp = open(self.path, mode="w", encoding="utf8")
        return self

    def append_in_buffer(self, t: float, u: np.ndarray) -> None:
        """
        Guarda os resultados no buffer em memória.

        Parameters:
            t: tempo
            u: valor do campo
        """
        dict_ = {"t": t, "u": u.tolist()}
        self.results.append(dict_)

    def dump(self) -> None:
        """Tranfere os resultados do buffer me memoria para o arquivo."""
        json.dump(self.results, self.fp, indent=self.indent)
        self.results.clear()

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.fp.close()
