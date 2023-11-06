"""Módulo dos solvers"""

from dataclasses import dataclass

import numpy as np

from pyheat1d.system import System


@dataclass
class Solver:
    """
    Classe solver.

    Parameters:
        system (System): Sistema de equações a ser resolvido.
    """

    system: System

    def solver(self) -> np.ndarray:
        """
        Resolução de sistemas tridiagonais pelo método `TDMA` [[ref]](https://en.wikipedia.org/wiki/Tridiagonal_matrix_algorithm).

        Returns:
            Vetor de solução do sistema.

        """

        a, b0, neq = self.system.a, self.system.b, self.system.neq

        lower = a[:, 0]
        diag = a[:, 1]
        upper = a[:, 2]
        b = b0.copy()

        x = np.empty_like(b)

        upper[0] /= diag[0]
        b[0] /= diag[0]
        for i in range(1, neq - 1):
            upper[i] /= diag[i] - upper[i - 1] * lower[i]
            b[i] = (b[i] - b[i - 1] * lower[i]) / (diag[i] - upper[i - 1] * lower[i])
        b[-1] = (b[-1] - b[-2] * lower[-1]) / (diag[-1] - upper[-2] * lower[-1])

        x[-1] = b[-1]
        for i in range(neq - 2, -1, -1):
            x[i] = b[i] - upper[i] * x[i + 1]

        return x.copy()
