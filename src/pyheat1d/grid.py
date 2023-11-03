import numpy as np


class Mesh:
    def __init__(self, length: float, n_div: int):
        self.length = length
        self.n_cells = n_div
        self.n_points = n_div + 1
        self.dx = length / n_div

        self.x = np.zeros(self.n_points, dtype=float)
        self.cells = np.zeros((self.n_cells, 2), dtype=int)
        self.centroid = np.zeros(self.n_cells, dtype=float)

    def _mk_points(self) -> None:
        """
        Método que gera os pontos do grid.
        """

        for i in range(1, self.n_points - 1):
            self.x[i] = self.x[i - 1] + self.dx
        self.x[-1] = self.length

    def _mk_cells(self) -> None:
        """
        Método que gera as celulas.
        """

        for i in range(self.n_cells):
            self.cells[i][0], self.cells[i][1] = i + 1, i + 2

    def _mk_centroid(self) -> None:
        """
        Método que gera os centriodes.
        """

        for i in range(self.n_cells):
            self.centroid[i] = (self.x[i + 1] + self.x[i]) * 0.5

    def mk_grid(self) -> None:
        """
        Método que gera o grid
        """

        self._mk_points()
        self._mk_cells()
        self._mk_centroid()

    @property
    def infos(self) -> dict[str, float | int]:
        return {
            "dx": self.dx,
            "n_points": self.n_points,
            "n_cells": self.n_cells,
            "length": self.length,
        }
