class Singleton(type):
    _instances = {}  # type: ignore

    def __call__(cls, *args, **kwargs):
        print("oi")
        if cls not in cls._instances:
            print("Criando ...")
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
