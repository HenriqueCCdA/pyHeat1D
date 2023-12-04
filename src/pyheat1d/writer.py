import json
from abc import ABC, abstractmethod
from pathlib import Path

import numpy as np


class WriterBase(ABC):
    """Gerenciador de context usado para escrever os resultados."""

    def __init__(self, path: Path, indent: int | None = None) -> None:
        """
        Parameters:
            path (Path): Caminho do arquivo.
            indent (None | int): Indentação do json
        """
        self.buffer: list[dict] = []
        self.indent = indent
        self.path = path

    def __enter__(self):
        self.fp = open(self.path, mode="w", encoding="utf8")
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.fp.close()

    @abstractmethod
    def append_in_buffer(self):
        ...

    def dump(self) -> None:
        """Tranfere os resultados do buffer para a memória para o arquivo."""
        json.dump(self.buffer, self.fp, indent=self.indent)
        self.buffer.clear()


class ResultsResults(WriterBase):
    def append_in_buffer(self, t: float, u: np.ndarray) -> None:  # type: ignore
        """
        Guarda os resultados no buffer em memória.

        Parameters:
            t: tempo
            u: valor do campo
        """
        dict_ = {"t": t, "u": u.tolist()}
        self.buffer.append(dict_)


class MeshWriter:
    def __init__(self, path: Path, indent: int | None = None) -> None:
        """
        Parameters:
            path (Path): Caminho do arquivo.
            indent (None | int): Indentação do json
        """
        self.buffer: list[dict] = []
        self.indent = indent
        self.path = path

    def dump(self, cell_nodes: np.ndarray, centroid: np.ndarray, x: np.ndarray) -> None:
        """
        Escreve a malha em arquivo json.

        Parameters:
            cell_nodes: Conetiviade nodal
            centroid: Centroide da celula
            x: Coordenadas nodais
        """
        with open(self.path, mode="w", encoding="utf8") as fp:
            dict_ = {"cell_nodes": cell_nodes.tolist(), "x": x.tolist(), "xp": centroid.tolist()}
            json.dump(dict_, fp, indent=self.indent)
