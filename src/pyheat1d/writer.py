import json
from abc import ABC, abstractmethod
from pathlib import Path

import numpy as np

from pyheat1d.jsonencoder import JSONEncoderNumpy


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
        json.dump(self.buffer, self.fp, cls=JSONEncoderNumpy, indent=self.indent)
        self.buffer.clear()


class ResultsWriterEveryTime(WriterBase):
    def append_in_buffer(self, istep: int, t: float, u: np.ndarray) -> None:  # type: ignore
        """
        Guarda os resultados no buffer em memória.

        Parameters:
            istep: passo de tempo
            t: tempo
            u: valor do campo
        """

        dict_ = {"istep": istep, "t": t, "u": u.copy()}
        self.buffer.append(dict_)


class ResultsWriterEveryNSteps(WriterBase):
    def __init__(self, path: Path, indent: int | None = None, write_every_steps: int | None = None) -> None:
        """
        Parameters:
            path: Caminho do arquivo.
            indent: Indentação do json.
            write_every_steps: Escrever a cada n passos.
        """
        super().__init__(path, indent)
        self.writer_count = 1
        self.write_every_steps = write_every_steps

    def append_in_buffer(self, istep: int, t: float, u: np.ndarray) -> None:  # type: ignore
        """
        Guarda os resultados no buffer acada n passos.

        Parameters:
            istep: passo de tempo
            t: tempo
            u: valor do campo
        """

        if istep == 0:
            self._append_in_buffer(istep, t, u)
            return

        if not self.write_every_steps or self.writer_count == self.write_every_steps:
            self._append_in_buffer(istep, t, u)
            self.writer_count = 0

        self.writer_count += 1

    def _append_in_buffer(self, istep: int, t: float, u: np.ndarray) -> None:
        dict_ = {"istep": istep, "t": t, "u": u.copy()}
        self.buffer.append(dict_)


def results_writer_strategy(
    path: Path, indent: int | None = None, write_every_steps: int | None = None
) -> ResultsWriterEveryTime | ResultsWriterEveryNSteps:
    """
    Seleciona a estrategia de escrita dos resuldos.

    Parameters:
        path: Caminho do arquivo.
        indent: Indentação do json.
        write_every_steps: Escrever a cada n passos.
    """

    if write_every_steps:
        return ResultsWriterEveryNSteps(path, indent, write_every_steps)
    else:
        return ResultsWriterEveryTime(path, indent)


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
            dict_ = {"cell_nodes": cell_nodes, "x": x.tolist(), "xp": centroid}
            json.dump(dict_, fp, cls=JSONEncoderNumpy, indent=self.indent)
