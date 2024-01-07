"""Módulo com os erros"""


class Pyheat1ErrorsBase(Exception):
    errno: int | None = None


class InputFileNotFoundError(Pyheat1ErrorsBase):
    """Arquivo de enrada não achado."""

    errno = 2


class MissingInputInfoError(Pyheat1ErrorsBase):
    """Chave de configuração faltando."""

    errno = 3

    def __init__(self, key: str):
        msg = f"O valor '{key}' é necessário no arquivo de entrada."
        super().__init__(msg)


class BoundaryConditionMissingKeyError(Pyheat1ErrorsBase):
    """Chave da condição de contorno faltando."""

    errno = 4

    def __init__(self, key: str, bc: str):
        msg = f"O valor '{key}' é necessário na condição de contorno '{bc}'."
        super().__init__(msg)


class MatPropsMissingKeyError(Pyheat1ErrorsBase):
    """Chave da propriedade do material faltando."""

    errno = 5

    def __init__(self, key: str):
        msg = f"O valor '{key}' é necessário na propriedade do material."
        super().__init__(msg)


class FileMeshNotFoundError(Pyheat1ErrorsBase):
    """Arquivo com a malha não foi achado."""

    errno = 6

    def __init__(self):
        msg = "Arquivo 'mesh.json' não achado."
        super().__init__(msg)


class FileResultshNotFoundError(Pyheat1ErrorsBase):
    """Arquivo com os resultado foi achado."""

    errno = 7

    def __init__(self):
        msg = "Arquivo 'results.json' não achado."
        super().__init__(msg)


class TimeLogWriteFileError(Pyheat1ErrorsBase):
    errno = 8

    def __init__(self, file: str):
        msg = f"O arquivo '{file}' não pode ser escrito."
        super().__init__(msg)
