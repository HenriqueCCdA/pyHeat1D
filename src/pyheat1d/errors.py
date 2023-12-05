class Pyheat1ErrorsBase(Exception):
    errno: int | None = None


class InputFileNotFoundError(Pyheat1ErrorsBase):
    errno = 2


class MissingInputInfoError(Pyheat1ErrorsBase):
    errno = 3

    def __init__(self, key: str):
        msg = f"O valor '{key}' é necessário no arquivo de entrada."
        super().__init__(msg)


class BoundaryConditionMissingKeyError(Pyheat1ErrorsBase):
    errno = 4

    def __init__(self, key: str, bc: str):
        msg = f"O valor '{key}' é necessário na condição de contorno '{bc}'."
        super().__init__(msg)


class MatPropsMissingKeyError(Pyheat1ErrorsBase):
    errno = 5

    def __init__(self, key: str):
        msg = f"O valor '{key}' é necessário na propriedade do material."
        super().__init__(msg)


class FileMeshNotFoundError(Pyheat1ErrorsBase):
    errno = 6

    def __init__(self):
        msg = "Arquivo 'mesh.json' não achado."
        super().__init__(msg)


class FileResultshNotFoundError(Pyheat1ErrorsBase):
    errno = 7

    def __init__(self):
        msg = "Arquivo 'results.json' não achado."
        super().__init__(msg)
