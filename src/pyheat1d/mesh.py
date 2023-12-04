"""
Módulo com representação da Malha
"""


from dataclasses import dataclass

import numpy as np


@dataclass
class BoundaryCondition:
    """
    Condição de contorno.

    Parameters:
        type (int): Tipo da condiçãao de contorno.
        params (dict): Parametros da condição de contorno.

    Info:
        Tipos de condições de contorno disponiveis:

        * 1 - Valor constante.
        * 2 - Fluxo de calor constante.
        * 3 - Fluxo de calor por Convecção.
    """

    type: int
    params: dict


@dataclass
class MatPropsRef:
    """
    Propriedades do material.

    Parameters:
        k (float|np.ndarray): Condutividade térmica.
        ro (float|np.ndarray): Massa específica.
        cp (float|np.ndarray): Calor específico.
    """

    k: float
    ro: float
    cp: float


@dataclass
class MatProps:
    """
    Propriedades do material.

    Parameters:
        k (float|np.ndarray): Condutividade térmica.
        ro (float|np.ndarray): Massa específica.
        cp (float|np.ndarray): Calor específico.
    """

    k: np.ndarray
    ro: np.ndarray
    cp: np.ndarray


@dataclass
class Nodes:
    """
    Classe que representa os nos

    Parameters:
        x (np.ndarray): Coordenadas nodais.
    """

    x: np.ndarray


@dataclass
class ResultFields:
    """
    Classe que representa os resultadoss

    Parameters:
        u (np.ndarray): Valores do campo escalar.
    """

    u: np.ndarray


@dataclass
class Cells:
    """
    Classe que representa as células

    Parameters:
        nodes (np.ndarray): Conecitividade da malha.
        centroids (np.ndarray): Centroide dos elemetos.
        props (MatProps): Propriedades das células.
        results (ResultFields): Resultados.
    """

    nodes: np.ndarray
    centroids: np.ndarray
    props: MatProps
    results: ResultFields


class Mesh:
    """
    Classe que representa a malha.

    Parameters:
        length (float): Dimensão do domínio.
        n_cells (int): Número de celulas.
        n_points (int): Número de pontos.
        dx (float): Tamanho da célula.
        cells (Cells): Células da malha.
        nodes (Nodes): Nos da malha.
        lbc (BoundaryCondition): Condição de contorno a esquerda.
        rbc (BoundaryCondition): Condição de contorno a direita.
    """

    length: float
    n_cells: int
    n_points: int
    dx: float
    cells: Cells
    nodes: Nodes
    lbc: BoundaryCondition
    rbc: BoundaryCondition

    def __init__(
        self,
        length: float,
        n_div: int,
        lbc: BoundaryCondition,
        rbc: BoundaryCondition,
    ) -> None:
        """
        Parameters:
            length: Dimensão do domínio.
            n_div: Número de divisões.
            lbc: Condição de contorno a esquerda.
            rbc: Condição de contorno a direita.
        """

        self.length = length
        self.n_cells = n_div
        self.n_points = n_div + 1
        self.dx = length / n_div
        self.lbc = lbc
        self.rbc = rbc

        self.cells = Cells(
            nodes=np.zeros((self.n_cells, 2), dtype=int),
            centroids=np.zeros(self.n_cells, dtype=float),
            props=MatProps(
                k=np.zeros(self.n_cells, dtype=float),
                ro=np.zeros(self.n_cells, dtype=float),
                cp=np.zeros(self.n_cells, dtype=float),
            ),
            results=ResultFields(u=np.zeros(self.n_cells, dtype=float)),
        )

        self.nodes = Nodes(
            x=np.zeros(self.n_points, dtype=float),
        )

    def _mk_points(self) -> None:
        """Método que gera os pontos do grid."""

        for i in range(1, self.n_points - 1):
            self.nodes.x[i] = self.nodes.x[i - 1] + self.dx
        self.nodes.x[-1] = self.length

    def _mk_cells(self) -> None:
        """Método que gera as celulas."""

        for i in range(self.n_cells):
            self.cells.nodes[i][0], self.cells.nodes[i][1] = i + 1, i + 2

    def _mk_centroid(self) -> None:
        """Método que gera os centriodes."""

        for i in range(self.n_cells):
            self.cells.centroids[i] = (self.nodes.x[i + 1] + self.nodes.x[i]) * 0.5

    def mk_grid(self) -> None:
        """Método que gera o grid."""

        self._mk_points()
        self._mk_cells()
        self._mk_centroid()

    @property
    def infos(self) -> dict[str, float | int]:
        """Retorna as principais informações da malha."""
        return {
            "dx": self.dx,
            "n_points": self.n_points,
            "n_cells": self.n_cells,
            "length": self.length,
        }

    def update_prop(self, prop_name: str, value: float) -> None:
        """Atualiza a propriedade desejada

        Parameters:
            value: Valor da propriedade.
            prop_name: Nome da propriedade.
        """
        vector = getattr(self.cells.props, prop_name)
        vector[:] = value

    def update_cells_results(self, prop_name: str, value: float | np.ndarray) -> None:
        """Atualiza o resultado das células

        Parameters:
            value: Valor da célula
            prop_name: Nome do resultado.
        """
        vector = getattr(self.cells.results, prop_name)
        vector[:] = value


# TODO: Addicionar tipagem
def init_mesh(length, ndiv, lbc, rbc, prop, initialt) -> Mesh:
    """Inicializa a malha com as informações lidas

    Parameters:
        length: Dimensão do domínio.
        n_div: Número de divisões.
        lbc: Condição de contorno a esquerda.
        rbc: Condição de contorno a direita.
        prop: Propriedades iniciais.
        initialt: Temperatura inicial.

    Returns:
        Retorna a malha inicializada
    """

    mesh = Mesh(length, ndiv, lbc, rbc)
    mesh.mk_grid()

    mesh.update_prop(prop_name="k", value=prop.k)
    mesh.update_prop(prop_name="cp", value=prop.cp)
    mesh.update_prop(prop_name="ro", value=prop.ro)

    mesh.update_cells_results(prop_name="u", value=initialt)

    return mesh
