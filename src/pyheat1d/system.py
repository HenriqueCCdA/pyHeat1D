import numpy as np


class System:
    """
    Classe que representa o sistema de equações.

    Parameters:
        neq (int): Numero de equações.
        a (ndarray): Matriz de coeficientes.
        b (ndarray): Vetor de forças.

    Infos:
        A matriz de coeficiente é tridiagonal.

        * a[:,0] - diagonal inferior
        * a[:,1] - diagonal princial
        * a[:,2] - diagonal princial
    """

    neq: int
    a: np.ndarray
    b: np.ndarray

    def __init__(self, neq: int) -> None:
        self.neq = neq
        self.a = np.zeros((self.neq, 3), dtype=float)
        self.b = np.zeros(self.neq, dtype=float)
