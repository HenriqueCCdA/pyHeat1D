"""Modulo do arquivo de entrada."""
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from pyheat1d.errors import (
    BoundaryConditionMissingKeyError,
    InputFileNotFoundError,
    MatPropsMissingKeyError,
    MissingInputInfoError,
)
from pyheat1d.mesh import BoundaryCondition, MatProps, MatPropsRef


@dataclass
class Input:
    """Infomações no arquivo entrada

    Parameters:
        length (float): Dimensão do domínio.
        ndiv (int): Número de divisões.
        nstep (int): Número de passos.
        dt (float): Passo de tempo.
        lbc (BoundaryCondition): Condição de contorno a esquerda.
        rbc (BoundaryCondition): Condição de contorno a direita.
        prop (PropRef): Propriedades iniciais.
        initialt (float): Temperatura inicial
    """

    length: float
    ndiv: int
    dt: float
    nstep: int
    lbc: BoundaryCondition
    rbc: BoundaryCondition
    initialt: float
    prop: MatPropsRef
    write_every_steps: Optional[int] = None


def load_input_file(path: Path) -> Input:
    """
    Le o arquivo de entrada

    Parameters:
        path: Caminho do arquivo de entrada.

    Raises:
        InputFileNotFount: Arquivo de entrada não achado.

    Returns:
        Retorna as informações do arquivo de entrada.
    """

    try:
        with open(path, encoding="utf-8") as fp:
            dict_ = json.load(fp)
    except FileNotFoundError as e:
        raise InputFileNotFoundError(f"O arquivo de entrada não foi achado: {path}.") from e

    validated(dict_)

    lbc = BoundaryCondition(**dict_.pop("lbc"))
    rbc = BoundaryCondition(**dict_.pop("rbc"))
    prop = MatPropsRef(**dict_.pop("prop"))

    in_ = Input(
        **dict_,
        lbc=lbc,
        rbc=rbc,
        prop=prop,
    )
    return in_


LIST_VALUES = (
    "length",
    "nstep",
    "dt",
    "nstep",
    "lbc",
    "rbc",
    "initialt",
    "prop",
)


def validated(infos: dict) -> None:
    """
    Valida as informações do arquivo de entrada.

    Parameters:
        infos: Informações lidas no arquivo de entrada.

    Raises:
        MissingInputInfoError: Valor faltando no arquivo de entrada.
    """

    for k in LIST_VALUES:
        if k not in infos:
            raise MissingInputInfoError(k)

    try:
        BoundaryCondition(**infos["lbc"])
    except TypeError as e:
        key = find.group() if (find := re.search("(?<=').+(?=')", e.args[0])) else e.args[0]
        raise BoundaryConditionMissingKeyError(key=key, bc="lbc") from e

    try:
        BoundaryCondition(**infos["rbc"])
    except TypeError as e:
        key = find.group() if (find := re.search("(?<=').+(?=')", e.args[0])) else e.args[0]
        raise BoundaryConditionMissingKeyError(key=key, bc="rbc") from e

    try:
        MatProps(**infos["prop"])
    except TypeError as e:
        key = find.group() if (find := re.search("(?<=').+(?=')", e.args[0])) else e.args[0]
        raise MatPropsMissingKeyError(key=key) from e
