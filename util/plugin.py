class Plugin:
    def __init__(self, name: str, abilities: dict):
        self.__name__: str = name
        self.__dict__.update(abilities)
